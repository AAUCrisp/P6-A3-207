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

    def __init__(self, tech, target=lambda: "some data2") -> None:
        """This is the constructor of the sensor class, it will initialize a network type and connect to a headend server."""
        # initialize the loopback network
        self.network = Network(tech)

        # target sensor collection function, the default just contains the string "some data"
        self.target = target

        # Connect to the address passed to the constructor
        # self.network.connect(addr[0], addr[1])
        self.network.connect(ipOut, int(portOut))
        Thread(target=self.printThread, daemon=True).start()
    
    def run(self):
        """This method runs the sensor program, it will send data using the network every <txInterval> seconds"""
        # try/catch clause to restore terminal state after a keyboardinterrupt
        try: 
            # hide the cursor
            hide()

            # set default values for some post processing data
            txTime = -1
            postTxTime = -1
            self.sent = 0
            RTOdifference = None
            GTdifference = None

            # run infinitely
            while True:
                # Make sure the synchronziation
                Sync.suspend()
                # initialize the dataframe object
                dataframe = ProcessData()

                # Capture the time the data has been generated
                dataTime = VKT.get()
                # attach the data time to the dataframe
                dataframe.setDataTime(dataTime)
                # attach the previous transmit time to the dataframe
                dataframe.setTxTime(txTime)
                # attach the post transmission time to the dataframe
                dataframe.setPostTxTime(postTxTime)
                # attach the payload to the dataframe
                dataframe.setPayload(self.target())
                # attach offsets if they have changed
                if not RTOdifference == RTO.offset or not GTdifference == GT.offset:
                    dataframe.setRTO(RTO.offset)
                    RTOdifference = RTO.offset
                    dataframe.setGT(GT.offset)
                    GTdifference = GT.offset

                # Build the dataframe into a string form
                packet = dataframe.buildSensorFrame()
                # Capture the time the data has begun transmission
                txTime = VKT.get()
                # Send the built dataframe object over the network
                self.network.transmit(packet)
                # Capture the post transmission time
                postTxTime = VKT.get()

                # Define when the next packet should be transmitted
                self.sleepEnd = VKT.get() + txInterval
                # Increment a value to keep track of time
                self.sent += 1
                self.lastDataframe = dataframe
                sleep(txInterval)
                    
                if not self.network.running: return unhide()

                Sync.resume()

        # Catch keyboardinterrupts to exit the program
        except KeyboardInterrupt: 
            # show the cursor again
            unhide()
            self.network.close()

    def printThread(self):
        lastPrintedDataframe = None
        print("\n"*6)
        while self.network.running:
            sleep(1)
            countdown = int(self.sleepEnd-VKT.get()+1)
            print(f"{UP}Transfers: {green(self.sent)}   Next transfer in: {green(countdown)}")
            if verbose:
                if not self.lastDataframe == lastPrintedDataframe:
                    lastPrintedDataframe = self.lastDataframe
                    print(f'{UP*7}', end="")
                    print(f'{UP}{"_"*50}')
                    for label, field in zip(
                        ["dataTime", "txTime", "postTxTime", "payload", "GT", "RTO"],
                        [self.lastDataframe.startTime, self.lastDataframe.txTime, self.lastDataframe.postTxTime, self.lastDataframe.payload, self.lastDataframe.GT, self.lastDataframe.RTO]):
                        print(f'{label}:\r\t\t{green(field)}{CLEAR}')
                    print()



# The main of this program
if "main" in __name__:

    #define a synchronization object for the clock GT
    syncGT = Sync(
        address=ipGT,
        interface=interfaceGT,
        clock=GT,
        interval = intervalGT
    )
    #start the synchronization thread
    syncGT.start()

    syncRTO = Sync(
        address=ipRTO,
        interface=interfaceRTO,
        clock=RTO,
        interval = intervalRTO
    )
    syncRTO.start()

    #if NTP is desired, then also define and start a VKT synchronization object
    if syncMode == "ntp":
        syncVKT = Sync(
            address=ipRTO,
            interface=interfaceRTO,
            clock=VKT,
            interval = intervalVKT
        )
        syncVKT.start()

    # create a sensor object with the headend address as an argument
    sensor = Sensor(interfaceTarget, lambda: payload)
    # run the sensor
    sensor.run()
    