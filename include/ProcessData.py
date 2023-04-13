# This module has been documented with DocString, it is a string format following a definition, it will show up in your VSCode documentation on hovering

SEP =   "\uFFFF"
"""Regular field seperator"""
PB =  "\uFFFE"
"""Piggyback data field seperator"""
EON =   "\uFFFD"
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
        """This is the constructor, it takes the following optional parameters: 
        
        ```
        rxTime:     The timestamp of when the packet was received
        dataTime:   The timestamp the data was collected at the sensor
        txTime:     The timestamp of transmission, adding this to the frame means it is the timestamp of the previous transmission
        postTxTime: The timestamp of when the transmission finished at the previous transmission
        payload:    The payload of the dataframe, it can be either sensor data or data received from another node
        piggy:      If a headend will transmit its own sensor data it will attach it here
        receivedIP: The IP address that this dataframe has been received from
        ```
        
        """

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
    
    def setGTRxTime(self, value:float):
        """Setter for the GTRxTime attribute"""
        self.GTRxTime = value
    
    def setDataTime(self, value:float):
        """Setter for the rxTime attribute to be used for sensor packets"""
        self.rxTime = value
        return self
    
    def setGTDataTime(self, value:float):
        """Setter for the GTDataTime attribute"""
        self.GTRxTime = value
        return self
    
    def setTxTime(self, value:float):
        """Setter for the txTime attribute"""
        self.txTime = value
        return self
    
    def setGTTxTime(self, value:float):
        """Setter for the GTTxTime attribute"""
        self.GTTxTime = value
        return self
    
    def setPostTxTime(self, value:float):
        """Setter for the postTxTime attribute"""
        self.postTxTime = value
        return self
    
    def setGTPostTxTime(self, value:float):
        """Setter for the GTPostTxTime attribute"""
        self.GTPostTxTime = value
        return value
    
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
            str(self.rxTime), 
            str(self.GTRxTime),
            str(self.txTime), 
            str(self.GTTxTime),
            str(self.postTxTime), 
            str(self.GTPostTxTime),
            str(self.payload)])

        return data
    
    def buildHeadendFrame(self):
        """Build a headend frame that is structured as follows:

        received time `R|` transmitted time of previous packet `R|` post transmission time of previous packet `D|` optional headend data `R|` received data's IP address `E|` payload (sensor or more headend data)

        * where;

        `R|` is a regular seperator

        `D|` is a data seperator, indicating the headend wants to send additional data

        `E|` EOP seperator, indicating End Of Packet
        """
        data = SEP.join([str(self.rxTime), str(self.txTime), str(self.postTxTime)])

        print(f"Piggy Variable Holds: {self.piggy}")
        if self.piggy != None:
            print("Entered Piggy Thing:")
            data += f'{PB}{str(self.piggy)}'
            self.piggy:str = None
            
        data += f'{SEP}{str(self.receivedIP)}'
        data += f'{EON}{str(self.payload)}'
        # data += SEP.join([str(self.receivedIP), str(self.payload)])
        # data += EOP.join([str(self.receivedIP), str(self.payload)])
        # data += EOP

        return data
    
    def unpack(dataframe:str) -> dict[str, str | dict[str, str]]:
        """This static method unpacks received data into a dictionary of data, it will unpack recursively and return a dict of the following structure:
        
        values are just written as the type, the value will be a variable of that type, this example is for one headend and one sensor
        ```json 
        {
            "txTime":float,
            "rxTime":float,
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
        if isHeadend:
            nextLayer = dataframe.split(EON)[1]
            return {
                "txTime":       float(layer[0]),
                "GTtxTime":     float(layer[1]),
                "rxTime":       float(layer[2]),
                "GTrxTime":     float(layer[3]),
                "postTxTime":   float(layer[4]),
                "GTpostTxTime": float(layer[5].split(PB)[0]),
                "piggy":        layer[5].split(PB)[1] if layer[5].count(PB) == 1 else None,
                "receivedIP":   layer[6],
                "payload":      ProcessData.unpack(nextLayer)
            }
        else:
            return {
                "dataTime":     float(layer[0]),
                "GTdataTime":   float(layer[1]),
                "txTime":       float(layer[2]),
                "GTtxTime":     float(layer[3]),
                "postTxTime":   float(layer[4]),
                "GTpostTxTime": float(layer[5]),
                "payload":      layer[6]
            }



            

