# from include.NetTechnology import *
# from include.Formatting import *
# from include.Network import *
# from include.ProcessData import *
from include.setup import *

# from time import sleep
# from threading import Thread, Lock


# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

# txInterval = 3

syncLock = Lock()

class Sensor:
    """This is the main class of the sensor. it will use the programs defined under `include/` to emulate the functionality of a sensor."""

    def __init__(self, addr, tech) -> None:
        """This is the constructor of the sensor class, it will initialize a network type and connect to a headend server."""
        # initialize the loopback network
        self.network = Network(tech)

        # Connect to the address passed to the constructor
        self.network.connect(ipOut, portOut)
    
    def run(self):
        """This method runs the sensor program, it will send data using the network every <txInterval> seconds"""
        # try/catch clause to restore terminal state after a keyboardinterrupt
        try: 
            # hide the cursor
            hide()
            # run infinitely
            txTime = -1
            postTxTime = -1
            syncLock.acquire()
            sent = 0

            while True:
                dataTime = SVTClock.get()
                dataframe = ProcessData()

                dataframe.setDataTime(dataTime)
                dataframe.setTxTime(txTime)
                dataframe.setPostTxTime(postTxTime)
                dataframe.setPayload("some data")

                txTime = SVTClock.get()
                packet = dataframe.buildSensorFrame()
                self.network.transmit(packet)
                postTxTime = SVTClock.get()
                syncLock.release()

                sent = sent+1

                sleep(.1)

                syncLock.acquire()
                sleepEnd = SVTClock.get() + txInterval
                while sleepEnd > SVTClock.get():
                    countdown = int(sleepEnd-SVTClock.get()+1)
                    print(f"Transfers: {sent}   Next transfer in: {countdown}", end="\r")
                    sleep(1)


        except KeyboardInterrupt: unhide()

def runSync():
    global SVTClock, GTClock, syncLock
    s = Sync(
        addressGT=  ipGT,
        address=    ipSVT,
        interfaceGT=interfaceGT,
        interface=  interfaceSVT
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
    sensor = Sensor((ipOut, portOut), interfaceTarget)
    # run the sensor
    sensor.run()
    