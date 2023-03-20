from subprocess import check_output

class Device:
    data:dict[str, str] = {}

    def __init__(self, name) -> None:
        device_data = check_output(f'nmcli -t d show {name}'.split(" ")).decode()
        self.data = {key:value for key, value in [(item for item in line.split(":", 1)) for line in device_data.split("\n") if not line == ""]}
        self.name = self.data["GENERAL.DEVICE"]
        self.type = self.data["GENERAL.TYPE"]
        self.connection = Connection(self.data["GENERAL.CONNECTION"])


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
        for device_name in [line.split(":")[0] for line in device_data.split("\n") if not line == ""]:
            self.devices.append(Device(device_name))

if "main" in __name__:
    from os import get_terminal_size
    import os
    import math
    RESET = "\033[0m"
    UP = "\033[A"
    DOWN = "\033[B"
    RIGHT = "\033[C"
    LEFT = "\033[D"
    magenta = lambda s: "\033[35m"+str(s)+RESET
    cyan = lambda s: "\033[36m"+str(s)+RESET
    red = lambda s: "\033[31m"+str(s)+RESET

    nmcli = NMCLI()
    width = get_terminal_size().columns

    print(red("DEVICES"))

    for device in nmcli.devices:
        i = 0
        print(" "*(int(os.get_terminal_size().columns/2)-(int(len(device.name)/2)))+f"{device.name}:\n"+"-"*os.get_terminal_size().columns)
        spacing = 45
        cols = math.floor(os.get_terminal_size().columns/spacing)
        for key in device.data.keys():
            value = device.data[key]
            if i == cols:
                print(f"\r{RIGHT*os.get_terminal_size().columns}|{DOWN}|", end="")
                print("\n"+"-"*os.get_terminal_size().columns)
                i = 0
            print(f'| {cyan(key)}:')
            print(f'{f"{RIGHT*((i)*spacing)}"}| {magenta(value)}{UP}', end=f"\r{RIGHT*((i+1)*spacing)}")
            i+=1
        print(f"\r{RIGHT*os.get_terminal_size().columns}|{DOWN}|", end="")
        print("\n"+"-"*os.get_terminal_size().columns+"\n")
    
    print(red("\nCONNECTIONS"))

    for device, connection in [(device, device.connection) for device in nmcli.devices]:
        i = 0
        print(" "*(int(os.get_terminal_size().columns/2)-(int(len(f'{device.name}->{connection.name}')/2)))+f"{device.name}->{connection.name}:\n"+"-"*os.get_terminal_size().columns)
        spacing = 45
        cols = math.floor(os.get_terminal_size().columns/spacing)
        for key in device.data.keys():
            value = device.data[key]
            if i == cols:
                print(f"\r{RIGHT*os.get_terminal_size().columns}|{DOWN}|", end="")
                print("\n"+"-"*os.get_terminal_size().columns)
                i = 0
            print(f'| {cyan(key)}:')
            print(f'{f"{RIGHT*((i)*spacing)}"}| {magenta(value)}{UP}', end=f"\r{RIGHT*((i+1)*spacing)}")
            i+=1
        print(f"\r{RIGHT*os.get_terminal_size().columns}|{DOWN}|", end="")
        print("\n"+"-"*os.get_terminal_size().columns+"\n")
