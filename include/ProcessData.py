import time

# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

class ProcessData:
    """This class will handle processing of data, it will attach timestamps, build the data into a dataframe containing SEPERATOR between data points
    
    The dataframe structure:

    <timestamp>SEPERATOR<pTime>SEPERATOR<data>
    """


    SEPERATOR = "\uFFFF"
    """ This seperator will be used to seperate data in the packet, this will be a constant and can be changed at any time.

    It is initially set to the unicode character \uFFFF as its an unused character and is unlikely to be found in the dataframe """

    timestamp:float = None
    """The timestamp of when the dataframe was initially built"""
    data:str = None
    """The payload data to be sent in the dataframe"""
    pTime:float = None
    """Processing time, the time taken to process the data"""


    def __init__(self, data:str, packed=False) -> None:
        """The constructor of this class, it unpacks the data if it is packed or just sets the data of the frame if it isn't already packed"""
        # Start the processing time timer
        self.pTimeStart = time.time()
        # if the data is packed
        if packed:
            # seperating the first index of the seperated data into the timestamp attribute
            self.timestamp = float(data.split(self.SEPERATOR)[0])
            # seperating the second index into the processing time attribute
            self.pTime = float(data.split(self.SEPERATOR, 2)[1])
            # seperating the rest of the data into the data attribute
            self.data = str(data.split(self.SEPERATOR, 2)[2])
        else:
            # save all the data into the data attribute
            self.data = data

    def buildFrame(self):
        """This method builds the dataframe from data saved, if its a frame that has been unpacked, it will just repack it with the same data"""
        # Return a data frame, a string of data seperated by SEPERATOR. <string>.join() will create a string from a list where list entries are seperated by <string>
        return self.SEPERATOR.join([
            # measure the time if its a new packet, otherwise use the old timestamp
            str(time.time()) if self.timestamp is None else self.timestamp,
            # measure the processing time if its a new packet, otherwise use the old processing time
            str(time.time()-self.pTimeStart) if self.pTime is None else self.pTime,
            # use the data saved in the constructor
            str(self.data)
        ])
    def unpackFrame(data):
        """This method just returns the constructor with the packed data and the packed flag turned on"""
        return ProcessData(data, True)
