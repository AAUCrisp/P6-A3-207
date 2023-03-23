import subprocess
import socket
import sys
import time
import json
import pickle
import base64

from Terminal.Formatting import *
from Networking.NetworkManager import NMCLI, SEPERATOR
from Networking.TCP import TCP_INFO

def main():
    nmcli = NMCLI()

    def getDevice():
        print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {nmcli.devices[i].name}' for i in range(len(nmcli.devices))]))
        return nmcli.devices[int(input(f"Choose the {yellow('index')} of a device to use: "))]



    # args:
    device = getDevice() if not "--device" in sys.argv else [device for device in nmcli.devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]
    address = input("Specify target address: ") if not "--address" in sys.argv else sys.argv[sys.argv.index("--address")+1]
    message = "ping" if not "--message" in sys.argv else sys.argv[sys.argv.index("--message")+1]
    numPackets = 1 if not "--packets" in sys.argv else int(sys.argv[sys.argv.index("--packets")+1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(True)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))
    s.connect((address, 44261 if address == "skademaskinen.win" else 8123))

    for packetIndex in range(numPackets):
        t1 = time.time()
        dataframe = {
            "data":message,
            "index":packetIndex,
            "lost packets":TCP_INFO(s)["tcpi_lost"],
            "RTT":TCP_INFO(s)["tcpi_rtt"],
            "delays":{
                "start_meas":t1,
                "end_meas":time.time()
            }
            
        }

        s.send(f'{json.dumps(dataframe)}{SEPERATOR}'.encode())
    s.send(SEPERATOR.encode())
    s.close()

if "main" in __name__:
    main()