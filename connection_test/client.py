import subprocess
import socket
import sys
import time
import json
import pickle
import base64

from formatting import *
from Networking.NetworkManager import NMCLI
from Networking.TCP import TCP_INFO

def main():
    nmcli = NMCLI()

    def getDevice():
        print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {nmcli.devices[i].name}' for i in range(len(nmcli.devices))]))
        return nmcli.devices[int(input(f"Choose the {yellow('index')} of a device to use: "))]

    def ntp():
        return time.time() #change to an ntp function later


    # args:
    device = getDevice() if not "--device" in sys.argv else [device for device in nmcli.devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]
    address = input("Specify target address: ") if not "--address" in sys.argv else sys.argv[sys.argv.index("--address")+1]
    message = "ping" if not "--message" in sys.argv else sys.argv[sys.argv.index("--message")+1]
    numPackets = 1 if not "--packets" in sys.argv else int(sys.argv[sys.argv.index("--packets")+1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))
    s.connect((address, 44261 if address == "skademaskinen.win" else 8123))
    tcp_info = TCP_INFO(s)

    processing_t1 = time.time()
    for packetIndex in range(numPackets):
        dataframe = {
            "timestamp":ntp(),
            "data":message,
            "p_time":time.time()-processing_t1,
            "packet_index":packetIndex,
            "lost_packets":tcp_info["tcpi_lost"]
        }

        s.send(f'{json.dumps(dataframe)}\n'.encode())
    s.send(b"")
    s.close()

if "main" in __name__:
    main()