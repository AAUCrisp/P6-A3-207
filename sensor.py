from include.NetTechnology import *
from include.Formatting import *
from include.Network import *
from include.ProcessData import *
from include.setup import *

from time import sleep, time


# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

interval = 10
"""This is the interval the sensor will transmit data in"""


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
        """This method runs the sensor program, it will send data using the network every <interval> seconds"""
        # try/catch clause to restore terminal state after a keyboardinterrupt
        try: 
            # hide the cursor
            hide()
            # run infinitely
            txTime = -1
            postTxTime = -1
            while True:
                sleepEnd = time()+interval
                while sleepEnd > time():
                    print(int(sleepEnd-time()), end="\r")
                    sleep(1)
                    if (sleepEnd - time()) < 5 and (sleepEnd - time()) > 4:
                        dataTime = time()
                dataframe = ProcessData()

                dataframe.setDataTime(dataTime)
                dataframe.setTxTime(txTime)
                dataframe.setPostTxTime(postTxTime)
                dataframe.setPayload("some payload")

                txTime = time()
                self.network.transmit(dataframe.buildSensorFrame())
                postTxTime = time()

        except KeyboardInterrupt: unhide()

# The main of this program
if "main" in __name__:

    # create a sensor object with the headend address as an argument
    sensor = Sensor((ipTarget, portTarget), interfaceTarget)
    # run the sensor
    sensor.run()
    