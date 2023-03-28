from include.NetTechnology import *
from include.Formatting import *
from include.Network import *
from include.ProcessData import *

from time import sleep
from sys import argv

interval = 10

# command line arguments:
headendAddr = input("Specify a headend address (format: <addr>:<port>): ") if not "--addr" in argv else argv[argv.index("--addr")+1]
headendAddr = (str(headendAddr.split(":")[0]), int(headendAddr.split(":")[1]))

class Sensor:
    def __init__(self) -> None:
        network = Network()
        network.connect(headendAddr)
        
        try: pass
        except KeyboardInterrupt:
            while True:
                network.transmit()
                time.sleep(interval)



#class SingletonException(Exception): pass
#
#class Network:
#    singleton = None
#    def __init__(self) -> None:
#        if Network.singleton is None:
#            Network.singleton = self
#        else: raise SingletonException