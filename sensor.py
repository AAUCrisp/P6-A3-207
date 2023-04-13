# from include.NetTechnology import *
# from include.Formatting import *
# from include.Network import *
# from include.ProcessData import *
from include.setup import *

# from time import sleep
# from threading import Thread, Lock


# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

# txInterval = 3

syncLock = Condition()

class Sensor:
    """This is the main class of the sensor. it will use the programs defined under `include/` to emulate the functionality of a sensor."""

    def __init__(self, addr, tech) -> None:
        """This is the constructor of the sensor class, it will initialize a network type and connect to a headend server."""
        # initialize the loopback network
        self.network = Network(tech)

        # Connect to the address passed to the constructor
        # self.network.connect(addr[0], addr[1])
        self.network.connect(ipOut, portOut)
    
    def run(self):
        """This method runs the sensor program, it will send data using the network every <txInterval> seconds"""
        # try/catch clause to restore terminal state after a keyboardinterrupt
        try: 
            # hide the cursor
            hide()

            # set default values for some post processing data
            txTime = -1
            GTTxTime = -1
            postTxTime = -1
            GTPostTxTime = -1
            sent = 0

            # run infinitely
            while True:
                # acquire the lock for synchronization
                syncLock.acquire()
                # initialize the dataframe object
                dataframe = ProcessData()

                # Capture the time the data has been generated
                dataTime = SVTClock.get()
                GTDataTime = GTClock.get()
                # attach the data time to the dataframe
                dataframe.setDataTime(dataTime)
                dataframe.setGTDataTime(GTDataTime)
                # attach the previous transmit time to the dataframe
                dataframe.setTxTime(txTime)
                dataframe.setGTTxTime(GTTxTime)
                # attach the post transmission time to the dataframe
                dataframe.setPostTxTime(postTxTime)
                dataframe.setGTPostTxTime(GTPostTxTime)
                # attach the payload to the dataframe
                dataframe.setPayload("some data")

                # Build the dataframe into a string form
                packet = dataframe.buildSensorFrame()
                # Capture the time the data has begun transmission
                txTime = SVTClock.get()
                GTTxTime = GTClock.get()
                # Send the built dataframe object over the network
                self.network.transmit(packet)
                # Capture the post transmission time
                postTxTime = SVTClock.get()
                GTPostTxTime = GTClock.get()

                # Define when the next packet should be transmitted
                sleepEnd = SVTClock.get() + txInterval
                # Increment a value to keep track of time
                sent = sent+1

                # A while loop that runs while the sensor should not be transmitting
                while sleepEnd > SVTClock.get():
                    # Define a countdown until this while loop should end
                    countdown = int(sleepEnd-SVTClock.get()+1)
                    # Print a formatted string with the aforementioned count of sent data, and a countdown to the next transmission
                    print(f"{UP}Transfers: {sent}   Next transfer in: {countdown}")

                    if self.network.isClosed: return
                    # Sleep to preserve system resources
                    sleep(1)
                # Release the syncronization lock
                syncLock.release()
                # Sleep for a while to allow the syncronization to take the lock
                sleep(.1)

        # Catch keyboardinterrupts to exit the program
        except KeyboardInterrupt: 
            # show the cursor again
            unhide()

# This method defines synchronization of the SVTClock and GTClock every 30 seconds
def runSync():
    # define global variables to be used in other functions
    global SVTClock, GTClock, syncLock
    # Define a local synchronization object
    s = Sync(
        addressGT=  ipGT,
        address=    ipSVT,
        interfaceGT=interfaceGT,
        interface=  interfaceSVT
    )
    # A while loop to run while the program is running, synchronizing every 30 seconds
    while True:
        # acquire the synchronization lock
        syncLock.acquire()
        # set the "Ground Truth" clock using the synchronization object
        GTClock.set(s.syncGT())
        # Set the "System Virtual Time" clock using the synchronization object
        SVTClock.set(s.sync())
        # Release the Synchronization lock
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
    