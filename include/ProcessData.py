import time

# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

class ProcessData:
    """This class will handle processing of data, it will attach timestamps, build the data into a dataframe containing SEPERATOR between data points
    
    The dataframe structure:

    <timestamp>SEPERATOR<pTime>SEPERATOR<data>
    """


    SEPERATOR = "\uFFFF"
    DATASEPERATOR = "\uFFFE"
    """ This seperator will be used to seperate data in the packet, this will be a constant and can be changed at any time.

    It is initially set to the unicode character \uFFFF as its an unused character and is unlikely to be found in the dataframe """

    timestamp:float = None
    """The timestamp of when the dataframe was initially built"""
    data:str = None
    """The payload data to be sent in the dataframe"""
    pTime:float = None
    """Processing time, the time taken to process the data"""
    receivedId:str = None
    """The received IP address, it can be null if its the source node"""
    piggy:str = None
    """If the current node is adding its own sensor data to the node, it can be null"""
    receivedTimestamp:float = None
    """The timestamp of when the packet has been received"""


    def __init__(self, data:str, packed=False) -> None:
        """The constructor of this class, it unpacks the data if it is packed or just sets the data of the frame if it isn't already packed"""
        # Start the processing time timer
        self.pTimeStart = time.time()
        # if the data is packed
        if packed:
            # unpack the timestamp at the first index
            self.timestamp = data.split(self.SEPERATOR)[0]
            # unpack the processing time at the second index
            self.pTime = data.split(self.SEPERATOR)[1]
            if data.count(self.SEPERATOR) == 1: # this is a sensor packet
                # unpack the rest as data
                self.data = data.split(self.DATASEPERATOR, 2)[1]
            else: # if the packet is a headend
                # unpack received timestamp
                self.receivedTimestamp = data.split(self.SEPERATOR)[2]
                # unpack the received id, this might be between a seperator and a data seperator
                self.receivedId = data.split(self.SEPERATOR)[3].split(self.DATASEPERATOR)[0]
                # if there is a data seperator in the 3rd index
                if self.DATASEPERATOR in data.split(self.SEPERATOR)[3]:
                    # unpack the piggy data
                    self.piggy = data.split(self.SEPERATOR)[3].split(self.DATASEPERATOR)[1]
                # unpack the rest of the data and save it in the data attribute
                self.data = data.split(self.SEPERATOR, 4)[4]
        else:
            # save all the data into the data attribute
            self.data = data

    def buildFrame(self):
        """This method builds the dataframe from data saved, if its a frame that has been unpacked, it will just repack it with the same data"""

        # add timestamp
        data = f'{str(time.time()) if self.timestamp is None else self.timestamp}'
        # add processing time
        data += f'{self.SEPERATOR}{str(time.time()-self.pTimeStart) if self.pTime is None else self.pTime}'
        # add received timestamp
        data += f'{self.SEPERATOR+str(self.receivedTimestamp) if self.receivedTimestamp else ""}'
        # add received IP
        data += f'{self.SEPERATOR+self.receivedId if self.receivedId else ""}'
        # add any piggybacked data
        data += f'{self.DATASEPERATOR+self.piggy if self.piggy else ""}{self.SEPERATOR}'
        # add the rest of the data
        data += self.data

        # Return a data frame, a string of data seperated by SEPERATOR. <string>.join() will create a string from a list where list entries are seperated by <string>
        return data
    
    def unpackFrame(data):
        """This method just returns the constructor with the packed data and the packed flag turned on"""
        return ProcessData(data, True)
    
    def setReceivedId(self, address:str):
        """This method sets the received id, this will be an IP address"""
        self.receivedId = address
    
    def setPiggy(self, data:str):
        """Sets the piggybacked data"""
        self.piggy = data

    def setReceivedTimestamp(self, timestamp):
        self.receivedTimestamp = timestamp