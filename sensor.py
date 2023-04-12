# from include.NetTechnology import *
from include.Formatting import *
# from include.Network import *
# from include.ProcessData import *
from include.setup import *

from time import sleep
from threading import Thread, Lock


# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

rxInterval = 3

class Sensor:
    """This is the main class of the sensor. it will use the programs defined under `include/` to emulate the functionality of a sensor."""

    def __init__(self, addr, tech) -> None:
        """This is the constructor of the sensor class, it will initialize a network type and connect to a headend server."""
        # initialize the loopback network
        self.network = Network(tech)

        # Connect to the address passed to the constructor
        # self.network.connect(addr[0], addr[1])
        self.network.connect(ipTarget, portTarget)
    
    def run(self):
        """This method runs the sensor program, it will send data using the network every <rxInterval> seconds"""
        # try/catch clause to restore terminal state after a keyboardinterrupt
        try: 
            # hide the cursor
            hide()
            # run infinitely
            txTime = -1
            postTxTime = -1
            while True:
                dataTime = time()
                dataframe = ProcessData()

                dataframe.setDataTime(dataTime)
                dataframe.setTxTime(txTime)
                dataframe.setPostTxTime(postTxTime)
                dataframe.setPayload(payload)

                txTime = SVTClock.get()
                self.network.transmit(dataframe.buildSensorFrame())
                postTxTime = SVTClock.get()
                syncLock.release()
                sleep(.1)

                sleepEnd = time() + rxInterval
                while sleepEnd > time():
                    print(int(sleepEnd-time()+1), end="\r")
                    sleep(1)


                sleepEnd = time() + rxInterval
                while sleepEnd > time():
                    print(int(sleepEnd-time()+1), end="\r")
                    sleep(1)


        except KeyboardInterrupt: unhide()

def runSync():
    global SVTClock, GTClock, syncLock
    s = Sync(
        addressGT=  ips["up2"]["ethernet"],
        address=    ips["up2"]["wifi"],
        interfaceGT="ethernet",
        interface=  "wifi"
    )
    while True:
        syncLock.acquire()
        GTClock.set(s.syncGT())
        SVTClock.set(s.sync())
        syncLock.release()
        sleep(30) # only sync every 30 seconds

# The main of this program
if "main" in __name__:
    # start a synchronizing thread
    syncThread =  Thread(target=runSync, daemon=True)
    syncThread.start()

    # create a sensor object with the headend address as an argument
    sensor = Sensor((ipTarget, portTarget), interfaceTarget)
    # run the sensor
    sensor.run()
    