import include.Network as n
from sys import argv
from threading import Thread
from time import sleep

ADDR = ""
PORT= 12345 if not "--port" in argv else int(argv[argv.index("--port")+1])
s = n.Network("loopback")
Thread(target=s.listener, args=(PORT,)).start()

while True:
    for key in s.data.keys():
        if len(s.data[key]) > 0:
            data = s.data[key].pop(0)
            print(f'{data["data"]} timestamp: {data["recvTime"]}')
        else:
            sleep(1)