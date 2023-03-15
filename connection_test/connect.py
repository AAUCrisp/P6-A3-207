import subprocess
import socket
import os

RESET = "\u001B[0m"
black = lambda s: "\u001B[30m"+str(s)+RESET
red = lambda s: "\u001B[31m"+str(s)+RESET
green = lambda s: "\u001B[32m"+str(s)+RESET
yellow = lambda s: "\u001B[33m"+str(s)+RESET
blue = lambda s: "\u001B[34m"+str(s)+RESET
purple = lambda s: "\u001B[35m"+str(s)+RESET
cyan = lambda s: "\u001B[36m"+str(s)+RESET
white = lambda s: "\u001B[37m"+str(s)+RESET


def init():
    nmcli_d = subprocess.check_output("nmcli d".split(" ")).decode("utf-8")
    devices = [line.split(" ")[0] for line in nmcli_d.split("\n")][1:]
    devices.remove("")
    if "cdc-wdm0" in nmcli_d:
        state5g = " connected " in subprocess.check_output("nmcli d | grep cdc-wdm0", shell=True).decode("utf-8")
        print(f'5G state:         {yellow(state5g)}')
    if "wifi" in nmcli_d:
        statewifi = " connected " in subprocess.check_output("nmcli d | grep wlp4s0", shell=True).decode("utf-8")
        print(f'wifi state:       {yellow(statewifi)}')
    connectionCount = nmcli_d.count(" connected ")
    print(f'connection count: {yellow(connectionCount)}')
    if connectionCount == 1:
        deviceName = subprocess.check_output("nmcli d | grep \" connected \"", shell=True).decode("utf-8").split(" ")[0]
        if not input(f'[Device Name: {yellow(deviceName)}] Is this connection correct? ({green("y")}/{red("N")}): ')[0].lower() == "y":
            # change connection through script
            print(f'Device choices:\n'+'\n'.join([f'{yellow(i)}: {devices[i]}' for i in range(len(devices))]))
            index = input("Choose a device index to use for communication: ")
            os.system(f'nmcli d connect {devices.pop(index)}')
            for device in devices:
                os.system(f"nmcli d disconnect {device}")
    else:
        os.system("nmcli d | grep \" connected \"")
        name = input("Choose the name of the interface to disconnect: ")
        os.system(f"nmcli d disconnect {name} ")
        init()

def connect():
    #simple python socket stuff
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.31.0.102", 8123))
    s.send((green("Hello ")+purple("World!")).encode("utf-8"))
    s.close()

init()
connect()