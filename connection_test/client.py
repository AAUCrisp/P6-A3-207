import subprocess
import socket
import sys
import time
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

    def ntp():
        return time.time() #change to an ntp function later


    # args:
    device = getDevice() if not "--device" in sys.argv else [device for device in devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]
    address = input("Specify target address: ") if not "--address" in sys.argv else sys.argv[sys.argv.index("--address")+1]
    message = "ping" if not "--message" in sys.argv else sys.argv[sys.argv.index("--message")+1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))
    s.connect((address, 44261 if address == "skademaskinen.win" else 8123))

    processing_t1 = time.time()
    dataframe = {
        "timestamp":ntp(),
        "data":message,
        "device":base64.b64encode(pickle.dumps(device)).decode("ascii"),
        "p_time":time.time()-processing_t1
    }

    s.send(json.dumps(dataframe).encode("utf-8"))
    s.close()

if "main" in __name__:
    main()