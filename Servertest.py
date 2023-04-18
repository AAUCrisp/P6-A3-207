from include.setup import *

PORT = int(portIn)
s = Network(interfaceTarget)
Thread(target=s.listener, args=(PORT,), daemon=True).start()

try:
    while True:
        for key in s.data.keys():
            if len(s.data[key]) > 0:
                for _ in range(len(s.data.keys())):
                    data = s.data[key].pop(0)
                    print(data["data"].replace(SEP, red("\t| ")).replace(PB, blue("\t| ")).replace(EON, magenta("\t| ")))
            else:
                sleep(1)
except KeyboardInterrupt:
    print("\rClosing network, please don't keyboardinterrupt again...")
    s.close()