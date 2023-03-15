import socket
import sys
import subprocess

from connection_test.escape_codes import *

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

print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {devices[i].name}' for i in range(len(devices))]))
device = devices[int(input(f"Choose the {yellow('index')} of a device to use: "))]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))
s.bind(("", 8123))
s.listen()
try:
    i= 0
    hide()
    print()
    while True:
        c, _ = s.accept()
        while True:
            recv = c.recv(1024).decode("utf-8")
            if recv == "": break
            i+=1
            print_up(f'{i}: [{recv}]')
except:
    s.close()
    unhide()
