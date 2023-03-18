import subprocess

class Device:
    def __init__(self, nmcli_line) -> None:
        #print(nmcli_line)
        data = nmcli_line.split(":")
        self.name = data[0]
        self.type = data[1]
        self.profile = data[3]

    def getInterface(self) -> str:
        match self.type:
            case "gsm":
                nmcli = subprocess.check_output(["nmcli"]).decode("utf-8").split("\n")
                index = nmcli.index(f'{self.name}: connected to {self.profile}')+2
                for line in nmcli[index].split(", "):
                    if "iface" in line:
                        return line.replace("iface ", "")
                
            case _:
                return self.name
