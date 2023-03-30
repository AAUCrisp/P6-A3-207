from include.NetTechnology import *
from include.Formatting import *
from include.Network import *
from include.ProcessData import *

from time import sleep
from sys import argv

# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

interval = 10
"""This is the interval the sensor will transmit data in"""


class Sensor:
    """This is the main class of the sensor. it will use the programs defined under `include/` to emulate the functionality of a sensor."""

    def __init__(self, addr) -> None:
        """This is the constructor of the sensor class, it will initialize a network type and connect to a headend server."""
        # initialize the loopback network
        self.network = Network("loopback")

        # Connect to the address passed to the constructor
        self.network.connect(addr[0], addr[1])
    
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

                dataFrame.setReceivedId("localhost")
                dataFrame.setPiggy("n2")
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
    # command line arguments:
    # receive an address from the command line, it should have the format: <addr>:<port>.
    headendAddr = input(f"Specify a headend address (format: {hexcolor('<addr>', 'FF8800')}:{hexcolor('<port>', 'FF8800')}): ") if not "--addr" in argv else argv[argv.index("--addr")+1]
    # split address and port into a tuple, to be used with the socket object
    headendAddr = (str(headendAddr.split(":")[0]), int(headendAddr.split(":")[1]))

    # create a sensor object with the headend address as an argument
    sensor = Sensor(headendAddr)
    # run the sensor
    sensor.run()
    