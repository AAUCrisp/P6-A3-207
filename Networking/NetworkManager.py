from subprocess import check_output

SEPERATOR = "\uFFFF"

class Device:
    data:dict[str, str] = {}

    def __init__(self, name) -> None:
        device_data = check_output(f'nmcli -t d show {name}'.split(" ")).decode()
        self.data = {key:value for key, value in [(item for item in line.split(":", 1)) for line in device_data.split("\n") if not line == ""]}
        self.name = self.data["GENERAL.DEVICE"]
        self.type = self.data["GENERAL.TYPE"]
        
        self.connection = Connection(self.data["GENERAL.CONNECTION"]) if not self.data["GENERAL.CONNECTION"] == "" else None


    def getInterface(self) -> str:
        match self.type:
            case "gsm":
                nmcli = check_output(["nmcli"]).decode("utf-8").split("\n")
                index = nmcli.index(f'{self.name}: connected to {self.connection.name}')+2
                for line in nmcli[index].split(", "):
                    if "iface" in line:
                        return line.replace("iface ", "")
                
            case _:
                return self.name

class Connection:
    data:dict[str, str] = {}
    def __init__(self, name) -> None:
        connection_data = check_output(["nmcli", "-t", "c", "show", name]).decode()
        self.data = {key:value for key, value in [(item for item in line.split(":", 1)) for line in connection_data.split("\n") if not line == ""]}
        self.name = self.data["connection.id"]



class NMCLI:
    devices:list[Device] = []

    def __init__(self) -> None:
        device_data = check_output("nmcli -t d".split(" ")).decode()
        for device_name in [line.replace("\\:", SEPERATOR).split(":")[0].replace(SEPERATOR, ":") for line in device_data.split("\n") if not line == ""]:
            self.devices.append(Device(device_name))

if "main" in __name__:
    import os
    import sys

    sys.path.append(f"../{os.path.abspath('.').split('/').pop()}")
    from Terminal.Formatting import Table

    nmcli = NMCLI()

    print("DEVICES")
    for device in nmcli.devices:
        table = Table(device.data, f'{device.name}:')
        table.print(55)

    
    print("\nCONNECTIONS")
    for device, connection in [(device, device.connection) for device in nmcli.devices]:
        table = Table(connection.data, f'{device.name}->{connection.name}:')
        table.print(55)
