import os
from subprocess import check_output

SEPERATOR = "\uFFFF"

class NetTechnology:
    deviceName:str
    type:str
    connection:str


    def __init__(self, type="wifi") -> None:
        nmcliDevices = check_output("nmcli -t d".split(" ")).decode().split("\n")
        nmcliDevices.remove("")

        nmcliDict = {
            line.replace("\\:", SEPERATOR).split(":")[0].replace(SEPERATOR, ":"):{
                "type":line.replace("\\:", SEPERATOR).split(":")[1],
                "state":line.replace("\\:", SEPERATOR).split(":")[2],
                "connection":line.replace("\\:", SEPERATOR).split(":")[3]
            } for line in nmcliDevices
        }
        self.deviceName = [key for key, value in nmcliDict.items() if value["type"] == type][0]
        self.type = type
        self.connection = [value["connection"] for key, value in nmcliDict.items() if value["type"] == type][0]

    def getInterface(self):
        match self.type:
            case "gsm":
                nmcli = check_output(["nmcli"]).decode("utf-8").split("\n")
                index = nmcli.index(f'{self.deviceName}: connected to {self.connection}')+2
                for line in nmcli[index].split(", "):
                    if "iface" in line:
                        return line.replace("iface ", "")
                
            case _:
                return self.deviceName