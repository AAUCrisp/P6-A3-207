import include.Network as n
from sys import argv
from threading import Thread
from time import sleep
from include.Formatting import blue, red, magenta, white, black
from include.ProcessData import EOP, SEP, DSEP

ADDR = ""
PORT= 12345 if not "--port" in argv else int(argv[argv.index("--port")+1])
s = n.Network("loopback")
Thread(target=s.listener, args=(PORT,)).start()

while True:
    for key in s.data.keys():
        if len(s.data[key]) > 0:
            for _ in range(len(s.data.keys())):
                data = s.data[key].pop(0)
                print(data["data"].replace(SEP, red("\t| ")).replace(DSEP, blue("\t| ")).replace(EOP, magenta("\t| ")))
        else:
            sleep(1)