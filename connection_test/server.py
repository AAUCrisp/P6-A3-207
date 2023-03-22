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
bufferSize = 0

def receiver(c:socket.socket):
    while True:
        bufferSize = TCP_INFO(c)["tcpi_rcv_space"]
        try: sample = c.recv(bufferSize, socket.MSG_PEEK).decode()
        except UnicodeDecodeError: continue
        if sample == SEPERATOR: break
        if not SEPERATOR in sample: continue

        packet_length = sample.find(SEPERATOR)
        recv = c.recv(packet_length if not packet_length <= 0 else 8192).decode()
        c.recv(len(SEPERATOR.encode())) #remove the seperator after transmission ended

        jobs.append((recv, c))


def process_data():
    packets = 0
    up = False
    while True:
        time.sleep(.1)
        if len(jobs) == 0: pass
        else:
            recv, c = jobs.pop(0)

            packets+=1
            data:dict = json.loads(recv)

            data["rcv_buf"] = bufferSize
            if up:
                print(UP*10)
            else: up = True

            table = Table(data, cyan("TOTAL PACKETS")+": "+magenta(packets) + f" {cyan('TO BE PROCESSED')}: {magenta(len(jobs))}" + f'{cyan(" BUFFER SPACE")}: {percentage(len(c.recv(bufferSize, socket.MSG_PEEK)), bufferSize)}{CLEAR}')
            print(f'{UP}{CLEAR}')
            table.print(spacing=30)
            print("Press enter to exit...\r")

def server(s:socket.socket):
    while True:
        c, _ = s.accept()
        threading.Thread(target=receiver, args=(c,), daemon=True).start()

def main():
    global bufferSize
    nmcli = NMCLI()

    # args
    device = nmcli.devices[int(input(f'Devices connected:\n'+"\n".join([f"{yellow(i)}: {nmcli.devices[i].name}" for i in range(len(nmcli.devices))])+f"\nChoose the {yellow('index')} of a device to use: "))] if not "--device" in sys.argv else [device for device in nmcli.devices if device.name == sys.argv[sys.argv.index("--device")+1]][0]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, device.getInterface().encode("utf-8"))

    address = device.data["IP4.ADDRESS[1]"].split("/")[0]
    print(f'Address: {".".join([cyan(num) for num in address.split(".")])}')
    s.bind((address, 8123))
    s.listen()
    bufferSize = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

    threading.Thread(target=process_data, daemon=True).start()
    threading.Thread(target=server, args=(s,), daemon=True).start()
    hide()
    input("Press enter to exit...\n\r")
    unhide()


if "main" in __name__:
    main()