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

    piggy:str = None

    receivedTimestamp:float = None


    def __init__(self, data:str, packed=False) -> None:
        """The constructor of this class, it unpacks the data if it is packed or just sets the data of the frame if it isn't already packed"""
        # Start the processing time timer
        self.pTimeStart = time.time()
        # if the data is packed
        if packed:
            self.timestamp = data.split(self.SEPERATOR)[0]
            self.pTime = data.split(self.SEPERATOR)[1]
            if data.count(self.SEPERATOR) == 1: # this is a sensor packet
                self.data = data.split(self.DATASEPERATOR)[1]
            else:
                self.receivedId = data.split(self.SEPERATOR)[2].split(self.DATASEPERATOR)[0]
                if self.DATASEPERATOR in data.split(self.SEPERATOR)[2]:
                    self.piggy = data.split(self.SEPERATOR)[2].split(self.DATASEPERATOR)[1]
                self.data = data.split(self.SEPERATOR, 3)[3]
        else:
            # save all the data into the data attribute
            self.data = data

    def buildFrame(self):
        """This method builds the dataframe from data saved, if its a frame that has been unpacked, it will just repack it with the same data"""

        data = []
        # measure the time if its a new packet, otherwise use the old timestamp
        data.append(str(time.time()) if self.timestamp is None else self.timestamp)
        # measure the processing time if its a new packet, otherwise use the old processing time
        data.append(str(time.time()-self.pTimeStart) if self.pTime is None else self.pTime)
        # add received id if there is any
        if self.receivedId: data.append(self.receivedId)
        # add piggyback data if there is any
        if self.piggy: data.append(self.piggy)
        # use the data saved in the constructor
        data.append(str(self.data))

        # Return a data frame, a string of data seperated by SEPERATOR. <string>.join() will create a string from a list where list entries are seperated by <string>
        return f'{str(time.time()) if self.timestamp is None else self.timestamp}{self.SEPERATOR}{str(time.time()-self.pTimeStart) if self.pTime is None else self.pTime}{self.SEPERATOR+self.receivedId if self.receivedId else ""}{self.DATASEPERATOR+self.piggy if self.piggy else ""}{self.SEPERATOR}{self.data}'
    
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