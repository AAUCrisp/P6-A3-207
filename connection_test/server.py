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
c:socket.socket = None

def receiver(c:socket.socket):
    while True:
        try: sample = c.recv(8192, socket.MSG_PEEK).decode()
        except UnicodeDecodeError: continue
        if sample == "": break
        if not SEPERATOR in sample: continue

        packet_length = sample.find(SEPERATOR)
        recv = c.recv(packet_length if not packet_length <= 0 else 8192).decode()
        c.recv(len(SEPERATOR.encode())) #remove the seperator after transmission ended

        jobs.append((recv, TCP_INFO(c)))


def process_data():
    global jobs
    packets = 0
    while True:
        if len(jobs) == 0: time.sleep(.1)
        else:
            recv, info = jobs.pop(0)
            packets+=1
            data:dict = json.loads(recv)

            data["lost packets"] = info["tcpi_lost"]

            table = Table(data, cyan("TOTAL PACKETS")+": "+magenta(packets) + f" {cyan('TO BE PROCESSED')}: {magenta(len(jobs))}" + f'{cyan(" BUFFER SPACE")}: {percentage(len(c.recv(20000, socket.MSG_PEEK)), data["buf_max"])}')
            print(f'{UP}{CLEAR}')
            table.print()
            print("Press enter to exit...\r")

def server(s:socket.socket):
    while True:
        c, _ = s.accept()
        threading.Thread(target=receiver, args=(c,), daemon=True).start()

def main():
    nmcli = NMCLI()

    # args
    device = nmcli.devices[int(input(f'Devices connected:\n'+"\n".join([f"{yellow(i)}: {nmcli.devices[i].name}" for i in range(len(nmcli.devices))])+f"\nChoose the {yellow('index')} of a device to use: "))] if not "--device" in sys.argv else [device for device in nmcli.devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))

    address = device.data["IP4.ADDRESS[1]"].split("/")[0]
    print(f'Address: {".".join([cyan(num) for num in address.split(".")])}')
    s.bind((address, 8123))
    s.listen()

    threading.Thread(target=process_data, daemon=True).start()
    threading.Thread(target=server, args=(s,), daemon=True).start()
    hide()
    input("Press enter to exit...\n\r")
    unhide()


if "main" in __name__:
    main()