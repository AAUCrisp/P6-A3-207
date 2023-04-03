# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

SEP =   "\uFFFF"
"""Regular field seperator"""
DSEP =  "\uFFFE"
"""Piggyback data field seperator"""
EOP =   "\uFFFD"
"""End Of Packet seperator"""


class ProcessData:
    """This class will define a data frame and build it, it can also recursively unpack a data frame"""

    # This is the received timestamp
    rxTime:float = None

    # This is the transmitted timestamp of the PREVIOUS frame
    txTime:float = None

    # This is the timestamp taken after transmitting the PREVIOUS frame
    postTxTime:float = None

    # This is the payload of the packet
    payload:str = None

    # This is the piggybacked data, it can be null
    piggy:str = None

    # This is the IP address of the data received
    receivedIP:str = None

    # This is the constructor, it takes parameters and sets attributes based on the variables
    def __init__(self, rxTime=None, dataTime=None, txTime=None, postTxTime=None, payload=None, piggy=None, receivedIP=None) -> None:
        self.rxTime = rxTime if rxTime else dataTime
        self.txTime = txTime
        self.postTxTime = postTxTime
        self.payload = payload
        self.piggy = piggy
        self.receivedIP = receivedIP

    def setRxTime(self, value:float):
        """Setter for the rxTime attribute"""
        self.rxTime = value
        return self
    
    def setDataTime(self, value:float):
        """Setter for the rxTime attribute to be used for sensor packets"""
        self.rxTime = value
        return self

    
    def setTxTime(self, value:float):
        """Setter for the txTime attribute"""
        self.txTime = value
        return self
    
    def setPostTxTime(self, value:float):
        """Setter for the postTxTime attribute"""
        self.postTxTime = value
        return self
    
    def setPayload(self, value:str):
        """Setter for the payload attribute"""
        self.payload = value
        return self
    
    def setPiggy(self, value:str):
        """Setter for the piggy attribute"""
        self.piggy = value
        return self
    
    def setReceivedIP(self, value:str):
        """Setter for the receivedIP attribute"""
        self.receivedIP = value
        return self
    
    def buildSensorFrame(self):
        """"""
        data = SEP.join([str(self.rxTime), str(self.txTime), str(self.postTxTime), str(self.payload)])
        data += EOP

        return data
    
    def buildHeadendFrame(self):
        data = SEP.join([str(self.rxTime), str(self.txTime), str(self.postTxTime)])
        data += f'{DSEP}{str(self.piggy)}{SEP}'
        data += SEP.join([str(self.receivedIP), str(self.payload)])
        data += EOP

        return data
    
    def unpack(dataframe:str) -> dict[str, str | dict[str, str]]:
        isHeadend = False if dataframe.count(SEP) == 3 else True

        seperated = dataframe.split(SEP)
        if isHeadend:
            return {
                "rxTime":seperated[0],
                "txTime":seperated[1],
                "postTxTime":seperated[2].split(DSEP)[0],
                "piggy":seperated[2].split(DSEP)[1] if len(seperated[2].split(DSEP)) > 1 else None,
                "receivedIP":seperated[3],
                "payload":ProcessData.unpack(dataframe.split(SEP, 4)[4])
            }
        else:
            return {
                "dataTime":seperated[0],
                "txTime":seperated[1],
                "postTxTime":seperated[2],
                "payload":seperated[3].split(EOP)[0],
                "numHeaders":dataframe.count(EOP)
            }
            

