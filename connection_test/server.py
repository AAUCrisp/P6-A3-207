import socket
import sys
import subprocess
import threading
import json
import time

from formatting import *
from Networking.NetworkManager import NMCLI


jobs = []

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


    def mainloop():
        while True:
            c, _ = s.accept()
            while True:
                c.recv(1, socket.MSG_PEEK)
                prop_delay = time.time()
                sample = c.recv(1024, socket.MSG_PEEK).decode()
                packet_length = sample.find("}\n{")+1
                if sample == "": break
                if not packet_length > 0 and not sample[-2:-1] == "}": continue
                recv = c.recv(packet_length if not packet_length == 0 else 1024).decode()

                jobs.append((recv, prop_delay))
    
    def worker():
        global jobs
        while True:
            if len(jobs) > 0: process_data(jobs.pop(0))
            else: time.sleep(.1)

    def process_data(data):
        recv, prop_delay = data

        data:dict = json.loads(recv)
        print(f'{UP}\r\033[0K', end="")
        for key in data.keys():
            print(f'{key}: {yellow(data[key])}', end=",\t")
        print(f'propagation delay: {yellow(prop_delay-data["timestamp"])}')
        print("Press enter to exit...\r")

    threading.Thread(target=mainloop, daemon=True).start()
    threading.Thread(target=worker, daemon=True).start()
    hide()
    input("Press enter to exit...\n\r")
    s.close()
    unhide()

if "main" in __name__:
    main()