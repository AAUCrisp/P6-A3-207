from include.setup import *

PORT = int(portIn)
s = Network(interfaceTarget)
Thread(target=s.listener, args=(PORT,), daemon=True).start()

try:
    while True:
        if s.data.qsize() > 0:
            data:dict[str, str] = s.popData()
            print(data["data"].replace(SEP, red("\t| ")).replace(PB, blue("\t| ")).replace(EON, magenta("\t| ")).replace(OFF, green("\t| ")))
        else:
            sleep(1)
except KeyboardInterrupt:
    print("\rClosing network, please don't keyboardinterrupt again...")

s.close()
