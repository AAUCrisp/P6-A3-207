# from include.NetTechnology import *
# from include.Formatting import *
# from include.Network import *
# from include.ProcessData import *
from include.setup import *

# from time import sleep
# from threading import Thread, Lock


# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

# txInterval = 3


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

            # set default values for some post processing data
            txTime = -1
            GTTxTime = -1
            postTxTime = -1
            GTPostTxTime = -1
            sent = 0

            # run infinitely
            while True:
                # acquire the lock for synchronization
                sync.lock.acquire()
                # initialize the dataframe object
                dataframe = ProcessData()

                # Capture the time the data has been generated
                dataTime = VKT.get()
                GTDataTime = VKT.get()
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
                txTime = VKT.get()
                GTTxTime = VKT.get()
                # Send the built dataframe object over the network
                self.network.transmit(packet)
                # Capture the post transmission time
                postTxTime = VKT.get()
                GTPostTxTime = VKT.get()

                # Define when the next packet should be transmitted
                sleepEnd = VKT.get() + txInterval
                # Increment a value to keep track of time
                sent = sent+1

                # A while loop that runs while the sensor should not be transmitting
                while sleepEnd > VKT.get():
                    # Define a countdown until this while loop should end
                    countdown = int(sleepEnd-VKT.get()+1)
                    # Print a formatted string with the aforementioned count of sent data, and a countdown to the next transmission
                    print(f"{UP}Transfers: {sent}   Next transfer in: {countdown}")

                    if not self.network.running: return unhide()
                    # Sleep to preserve system resources
                    sleep(1)
                # Release the syncronization lock
                sync.lock.release()
                # Sleep for a while to allow the syncronization to take the lock
                sleep(.1)

        # Catch keyboardinterrupts to exit the program
        except KeyboardInterrupt: 
            # show the cursor again
            unhide()
            self.network.close()

        # Catch keyboardinterrupts to exit the program
        except KeyboardInterrupt: 
            # show the cursor again
            unhide()


# The main of this program
if "main" in __name__:
    sync = Sync(
        addressGT=ipGT,
        interfaceGT=interfaceGT
    )
    sync.start()

    # create a sensor object with the headend address as an argument
    sensor = Sensor((ipOut, int(portOut)), interfaceTarget)
    # run the sensor
    sensor.run()
    
