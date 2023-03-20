import socket
import sys
import subprocess
import threading
import json
import pickle
import base64

from formatting import *
from Networking.NetworkManager import Device, NMCLI

def main():
    nmcli = NMCLI()

    def getDevice():
        print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {nmcli.devices[i].name}' for i in range(len(nmcli.devices))]))
        return nmcli.devices[int(input(f"Choose the {yellow('index')} of a device to use: "))]
    # args
    device = getDevice() if not "--device" in sys.argv else [device for device in nmcli.devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))

    address = subprocess.check_output(f"nmcli -t d show {device.name} | grep IP4.ADDRESS", shell=True).decode("utf-8").split(":")[1].split("/")[0]
    print(f'Address: {".".join([cyan(num) for num in address.split(".")])}')
    s.bind((address, 8123))
    s.listen()

    def main():
        import time
        i= 0
        while True:
            c, _ = s.accept()
            while True:
                c.recv(1, socket.MSG_PEEK)
                prop_delay = time.time()
                packet_length = c.recv(1024, socket.MSG_PEEK).decode().find("}\n{")+1
                
                recv = c.recv(packet_length if packet_length > 0 else 1024).decode()
                if recv == "": break
                i+=1
                data:dict = json.loads(recv)
                print(f'\r\033[0K', end="")
                print(f'index: {yellow(i)}', end=",\t")
                for key in data.keys():
                    print(f'{key}: {data[key]}', end=",\t")
                print(f'propagation delay: {prop_delay-data["timestamp"]}')
    threading.Thread(target=main, daemon=True).start()
    hide()
    input("Press enter to exit...\r")
    s.close()
    unhide()

if "main" in __name__:
    main()