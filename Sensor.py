from include.NetTechnology import *
from include.Formatting import *
from include.Network import *
from include.ProcessData import *

from time import sleep
from sys import argv

interval = 10


class Sensor:
    def __init__(self, addr) -> None:
        self.network = Network("loopback")
        self.network.connect(addr[0], addr[1])
    
    def run(self):
        try: 
            hide()
            while True:
                dataFrame = ProcessData("something")
                self.network.transmit(dataFrame.buildFrame())
                for i in range(10):
                    print(f'{interval - i}{CLEAR}', end="\r")
                    sleep(1)
        except KeyboardInterrupt: unhide()


if "main" in __name__:
    # command line arguments:
    headendAddr = input(f"Specify a headend address (format: {hexcolor('<addr>', 'FF8800')}:{hexcolor('<port>', 'FF8800')}): ") if not "--addr" in argv else argv[argv.index("--addr")+1]
    headendAddr = (str(headendAddr.split(":")[0]), int(headendAddr.split(":")[1]))

    sensor = Sensor(headendAddr)
    sensor.run()
    