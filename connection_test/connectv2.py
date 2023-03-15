import subprocess
import socket
import os
import sys

from escape_codes import *

class Device:
    def __init__(self, nmcli_line) -> None:
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

nmcli_d = subprocess.check_output("nmcli -t d".split(" ")).decode("utf-8").split("\n")
nmcli_d.remove("")
devices:list[Device] = []
for line in nmcli_d:
    if ":connected" in line:
        devices.append(Device(line))

def getDevice():
    print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {devices[i].name}' for i in range(len(devices))]))
    return devices[int(input(f"Choose the {yellow('index')} of a device to use: "))]

# args:
device = getDevice() if not "--device" in sys.argv else [device for device in devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]
address = input("Specify target address: ") if not "--address" in sys.argv else sys.argv[sys.argv.index("--address")+1]
message = green("Hello ")+"\033[5m"+magenta("World!") if not "--message" in sys.argv else sys.argv[sys.argv.index("--message")+1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))
s.connect((address, 44261 if address == "skademaskinen.win" else 8123))

s.send(message.encode("utf-8"))
s.close()
