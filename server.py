import socket
import sys
import subprocess

RESET = "\u001B[0m"
black = lambda s: "\u001B[30m"+str(s)+RESET
red = lambda s: "\u001B[31m"+str(s)+RESET
green = lambda s: "\u001B[32m"+str(s)+RESET
yellow = lambda s: "\u001B[33m"+str(s)+RESET
blue = lambda s: "\u001B[34m"+str(s)+RESET
purple = lambda s: "\u001B[35m"+str(s)+RESET
cyan = lambda s: "\u001B[36m"+str(s)+RESET
white = lambda s: "\u001B[37m"+str(s)+RESET

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
                
            case "wifi":
                return self.name
            case _:
                return self.name

nmcli_d = subprocess.check_output("nmcli -t d".split(" ")).decode("utf-8").split("\n")
nmcli_d.remove("")
devices:list[Device] = []
for line in nmcli_d:
    if ":connected" in line:
        devices.append(Device(line))

print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {devices[i].name}' for i in range(len(devices))]))
device = devices[int(input("Choose the index of a device to use: "))]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))
s.bind(("", 8123))
s.listen()
try:
    i= 0
    while True:
        c, _ = s.accept()
        while True:
            recv = c.recv(1024).decode("utf-8")
            if recv == "": break
            i+=1
            print(f'{i}: [{recv}]', end="\r")
except:
    s.close()
    print("\n")
