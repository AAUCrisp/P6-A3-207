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
            while True:
                # create a dataframe with the data "something"
                dataFrame = ProcessData(ProcessData("n3").buildFrame())
                # transmit the dataframe, here buildFrame is called to convert the processed data to a string
                self.network.transmit(dataFrame.buildFrame())
                # for loop to show a timer in the terminal showing when the next data will be transmitted
                for i in range(10):
                    # print the time left
                    print(f'{interval - i}{CLEAR}', end="\r")
                    # sleep for 1 second
                    sleep(1)
        # if a keyboardinterrupt happens, unhide the cursor
        except KeyboardInterrupt: unhide()

# The main of this program
if "main" in __name__:

    # create a sensor object with the headend address as an argument
    sensor = Sensor((ipTarget, portTarget), interfaceTarget)
    # run the sensor
    sensor.run()
    