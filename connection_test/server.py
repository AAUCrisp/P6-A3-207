import socket
import sys
import subprocess
import threading
import json
import time

from Terminal.Formatting import *
from Networking.NetworkManager import NMCLI, SEPERATOR
from Networking.TCP import TCP_INFO


jobs = []
packets = 0
c = None

def main():
    global packets
    nmcli = NMCLI()

    def getDevice():
        print("Devices connected:\n"+"\n".join([f'{yellow(i)}: {nmcli.devices[i].name}' for i in range(len(nmcli.devices))]))
        return nmcli.devices[int(input(f"Choose the {yellow('index')} of a device to use: "))]
    # args
    device = getDevice() if not "--device" in sys.argv else [device for device in nmcli.devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))

    address = device.data["IP4.ADDRESS[1]"].split("/")[0]
    print(f'Address: {".".join([cyan(num) for num in address.split(".")])}')
    s.bind((address, 8123))
    s.listen()


    def mainloop():
        global packets, c
        while True:
            c, _ = s.accept()
            while True:
                try: sample = c.recv(8192, socket.MSG_PEEK).decode()
                except UnicodeDecodeError: continue
                if sample == "": break
                if not SEPERATOR in sample: continue

                packet_length = sample.find(SEPERATOR)
                recv = c.recv(packet_length if not packet_length <= 0 else 8192).decode()
                c.recv(len(SEPERATOR.encode())) #remove the seperator after transmission ended

                jobs.append(recv)
    
    def worker():
        global jobs
        while True:
            if len(jobs) > 0: process_data(jobs.pop(0))
            else: time.sleep(.1)

    def process_data(recv):
        global packets, c
        packets+=1
        info = TCP_INFO(c)


        data:dict = json.loads(recv)

        data["lost packets"] = info["tcpi_lost"]

        table = Table(data, cyan("TOTAL PACKETS")+": "+magenta(packets) + f" received data to be processed: {len(jobs)}")
        print(f'{UP}{CLEAR}')
        table.print()
        print("Press enter to exit...\r")

    threading.Thread(target=mainloop, daemon=True).start()
    threading.Thread(target=worker, daemon=True).start()
    hide()
    input("Press enter to exit...\n\r")
    s.close()
    unhide()

if "main" in __name__:
    main()