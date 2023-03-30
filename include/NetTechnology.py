import os
from subprocess import check_output

# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

SEPERATOR = "\uFFFF"
""" This seperator will be used to seperate data in the packet, this will be a constant and can be changed at any time.

It is initially set to the unicode character \uFFFF as its an unused character and is unlikely to be found in the dataframe """


class NetTechnology:
    """
    ```markdown

    This is the main NetTechnology class, its purpose is to define the technology type that we are using in an execution of the testbed 
    # Attributes:
    * deviceName:               The name of the network device used, this is a device name defined in NetworkManager
    * type:                     The type of the network, the type here could be one of the following: [wifi, ethernet, gsm, loopback]
    * connection:               The name of the connection that this network is connected to, could be the ssid of a wifi network
    # Methods: 
    * getInterface() -> str:    As some of the types of network will have different interface names saved in different places, this method identifies the method to obtain the interface and returns it.
    ```
    """
    deviceName:str
    type:str
    connection:str


    def __init__(self, type="wifi") -> None:
        """This is the constructor, it takes an optional type parameter, gets the networkmanager device data and saves it in a dictionary format for use later, the dictionary should have the following structure:
        ```py
        nmcliDevices = {
            "wlp3s0":{
                "type":"wifi",
                "state":"connected"
                "connection":"Bamses_Hytte"
            },
            "lo":{...}
        }
        ```
        """

        # Get the output of nmcli d split in lines and saved in a list of strings
        nmcliDevices = check_output("nmcli -t d".split(" ")).decode().split("\n")

        # remove the trailing newline
        nmcliDevices.remove("")

        # create the nmcli dict
        nmcliDict = {
            line.replace("\\:", SEPERATOR).split(":")[0].replace(SEPERATOR, ":"):{
                "type":line.replace("\\:", SEPERATOR).split(":")[1],
                "state":line.replace("\\:", SEPERATOR).split(":")[2],
                "connection":line.replace("\\:", SEPERATOR).split(":")[3]
            } for line in nmcliDevices
        }

        # get the name of the device based on the network type
        self.deviceName = [key for key, value in nmcliDict.items() if value["type"] == type][0]
        
        # save the type specified
        self.type = type
        # get the connection name from the device name specified
        self.connection = [value["connection"] for key, value in nmcliDict.items() if key == self.deviceName][0]

    def getInterface(self):
        """This method contains a state machine that determines the method to get the interface of a network technology
        
        It's only currently gsm(5g) that uses a different device name from the interface name, so upon calling this method with gsm selected it will handle getting the interface in a seperate state
        """

        # start the state machine on the type of the network
        match self.type:
            # first state, if its a gsm module
            case "gsm":
                # get the output of nmcli and split it in newlines
                nmcli = check_output(["nmcli"]).decode("utf-8").split("\n")
                # get the index of the line containing device name and connection and increment it by 2 to get to the line number desired
                index = nmcli.index(f'{self.deviceName}: connected to {self.connection}')+2
                # split the data in the line by ", " and iterate over it
                for line in nmcli[index].split(", "):
                    # check whether this data key is iface, meaning interface
                    if "iface" in line:
                        # return if it is found and remove the key identifier, resulting in the interface name
                        return line.replace("iface ", "")
            
            # for any unspecified technology, return the device name, as it will most likely be the same.
            case _:
                return self.deviceName