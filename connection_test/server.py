import socket
import sys
import subprocess
import os
import threading
from _thread import interrupt_main

from escape_codes import *

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

nmcli_d = subprocess.check_output("nmcli -t d".split(" ")).decode("utf-8").split("\n")
nmcli_d.remove("")
devices:list[Device] = []
for line in nmcli_d:
    if ":connected" in line:
        devices.append(Device(line))

def getDevice():
    print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {devices[i].name}' for i in range(len(devices))]))
    return devices[int(input(f"Choose the {yellow('index')} of a device to use: "))]
# args
device = getDevice() if not "--device" in sys.argv else [device for device in devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))

address = subprocess.check_output(f"nmcli -t d show {device.name} | grep IP4.ADDRESS", shell=True).decode("utf-8").split(":")[1].split("/")[0]
print(address)
s.bind((address, 8123))
s.listen()

def main():
    i= 0
    while True:
        c, _ = s.accept()
        while True:
            recv = c.recv(1024).decode("utf-8")
            if recv == "": break
            i+=1
            print_up(f'{yellow(i)}: [{recv}]\033[0K')
threading.Thread(target=main, daemon=True).start()
hide()
input("\nPress enter to exit...\r")
s.close()
unhide()
