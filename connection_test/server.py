import socket
import sys
import subprocess
import threading
import json
import pickle
import base64

from formatting import *
from NetworkDevice import Device

def main():
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
    print(f'Address: {".".join([cyan(num) for num in address.split(".")])}')
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
                data = json.loads(recv)
                device = pickle.loads(base64.b64decode(data["device"].encode("ascii")))
                print(f'\033[0Kindex: {yellow(i)},\ttimestamp: {yellow(data["timestamp"])},\tp_time: {yellow(data["p_time"])},\tdev_data: {device.__dict__}\tdata: {data["data"]}\nPress enter to exit...', end="\r")
    threading.Thread(target=main, daemon=True).start()
    hide()
    input("Press enter to exit...\r")
    s.close()
    unhide()

if "main" in __name__:
    main()