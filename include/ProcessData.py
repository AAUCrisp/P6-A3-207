# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

SEP =   "\uFFFF"
"""Regular field seperator"""
PB =  "\uFFFE"
"""Piggyback data field seperator"""
EON =   "\uFFFD"
"""End Of Packet seperator"""
OFF = "\uFFFC"

EOT = "\uFFFB"


class ProcessData:
    """This class will define a data frame and build it, it can also recursively unpack a data frame"""

    # This is the received timestamp
    startTime:float = None

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

    RTO:float = None

    GT:float = None

    # This is the constructor, it takes parameters and sets attributes based on the variables
    def __init__(self, startTime=None, dataTime=None, txTime=None, postTxTime=None, payload=None, piggy=None, receivedIP=None) -> None:
        """This is the constructor, it takes the following optional parameters: 
        
        ```
        startTime:     The timestamp of when the packet was received
        dataTime:   The timestamp the data was collected at the sensor
        txTime:     The timestamp of transmission, adding this to the frame means it is the timestamp of the previous transmission
        postTxTime: The timestamp of when the transmission finished at the previous transmission
        payload:    The payload of the dataframe, it can be either sensor data or data received from another node
        piggy:      If a headend will transmit its own sensor data it will attach it here
        receivedIP: The IP address that this dataframe has been received from
        ```
        
        """

        self.startTime     = startTime if startTime else dataTime
        self.txTime     = txTime
        self.postTxTime = postTxTime
        self.payload    = payload
        self.piggy      = piggy
        self.receivedIP = receivedIP

    def setstartTime(self, value:float):
        """Setter for the startTime attribute"""
        self.startTime = value
        return self
    
    def setDataTime(self, value:float):
        """Setter for the startTime attribute to be used for sensor packets"""
        self.startTime = value
        return self
    
    def setTxTime(self, value:float):
        """Setter for the txTime attribute"""
        self.txTime = value
        return self
    
    def setPostTxTime(self, value:float):
        """Setter for the postTxTime attribute"""
        self.postTxTime = value
        return self
    
    def setRTO(self, value:float):
        """Setter for the Reference Time Offset"""
        self.RTO = value
        return self
    
    def setGT(self, value:float):
        """Setter for the Ground Truth"""
        self.GT = value
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
        """Build a sensor frame that is structured as follows:

        data collection time `R|` transmitted time of previous packet `R|` post transmission time of previous packet `R|` payload

        * where;

        `R|` is a regular seperator
        """
        data = SEP.join([
            str(self.startTime),
            str(self.txTime),
            str(self.postTxTime)
        ])
        if self.RTO:
            data += f'{OFF}{str(self.RTO)}'
        if self.GT:
            data += f'{OFF}{str(self.GT)}'
        data += f'{EON}{str(self.payload)}'

        return data
    
    def buildHeadendFrame(self):
        """Build a headend frame that is structured as follows:

        received time `R|` transmitted time of previous packet `R|` post transmission time of previous packet `D|` optional headend data `R|` received data's IP address `E|` payload (sensor or more headend data)

        * where;

        `R|` is a regular seperator

        `D|` is a data seperator, indicating the headend wants to send additional data

        `E|` EOP seperator, indicating End Of Packet
        """
        data = SEP.join([
            str(self.startTime), 
            str(self.txTime),
            str(self.postTxTime)])
        if self.RTO:
            data += f'{OFF}{str(self.RTO)}'
        if self.GT:
            data += f'{OFF}{str(self.GT)}'
        if self.piggy:
            data += f'{PB}{str(self.piggy)}'
        data += f'{SEP}{str(self.receivedIP)}'
        data+= f'{EON}{str(self.payload)}'

        return data
    
    def unpack(dataframe:str) -> dict[str, str | dict[str, str]]:
        """This static method unpacks received data into a dictionary of data, it will unpack recursively and return a dict of the following structure:
        
        values are just written as the type, the value will be a variable of that type, this example is for one headend and one sensor
        ```json 
        {
            "txTime":float,
            "startTime":float,
            "postTxTime":float,
            "piggy":string or Null,
            "receivedIP":string,
            "payload":{
                "dataTime":float,
                "txTime":float,
                "postTxTime":float,
                "payload": str
            }
        }
        ```
        
        """
        isHeadend = not dataframe.count(EON) == 1
        layer = dataframe.split(EON)[0].split(SEP)
        nextLayer = dataframe.split(EON)[1]
        if isHeadend:
            return {
                "txTime":       float(layer[0]),
                "startTime":       float(layer[1]),
                "postTxTime":   float(layer[2].split(OFF)[0]),
                "RTO":          float(layer[2].split(OFF)[1]) if dataframe.count(OFF) > 0 else None,
                "GT":           float(layer[2].split(OFF)[2]) if dataframe.count(OFF) > 1 else None,
                "piggy":        layer[2].split(PB)[1] if layer[2].count(PB) == 1 else None,
                "receivedIP":   layer[3],
                "payload":      ProcessData.unpack(nextLayer)
            }
        else:
            return {
                "dataTime":     float(layer[0]),
                "txTime":       float(layer[1]),
                "postTxTime":   float(layer[2].split(OFF)[0]),
                "RTO":          float(layer[2].split(OFF)[1]) if dataframe.count(OFF) > 0 else None,
                "GT":           float(layer[2].split(OFF)[2]) if dataframe.count(OFF) > 1 else None,
                "payload":      nextLayer
            }



            

