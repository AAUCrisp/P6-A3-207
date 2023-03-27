import time


class ProcessData:
    SEPERATOR = "\uFFFF"
    timestamp:float = None
    data:str = None
    pTime:float = None


    def __init__(self, data:str, packed=False) -> None:
        self.pTimeStart = time.time()
        if packed:
            self.timestamp = data.split(self.SEPERATOR)[0]
            self.pTime = data.split(self.SEPERATOR, 2)[1]
            self.data = data.split(self.SEPERATOR)[2]
        else:
            self.data = data

    def buildFrame(self):
        return self.SEPERATOR.join([
            str(time.time()) if self.timestamp is None else self.timestamp,
            str(time.time()-self.pTimeStart) if self.pTime is None else self.pTime,
            str(self.data)
        ])
    def unpackFrame(data):
        return ProcessData(data, True)
