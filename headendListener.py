from include.setup import *

SERVERADDR = "192.168.1.107"
SERVERPORT= 8888

class headendlistener:

    def __init__(self, addr, tech) -> None:
        self.net = Network(interfaceTarget)

        self.buffer = None
        self.proxy_to_server_protocol = None
        self.sensorIP = '0.0.0.0'   
        self.sensorPort = 0
        self.txTime = -1
        self.GTTxTime = -1
        self.postTxTime = -1
        self.GTPostTxTime = -1
        self.sent = 0
        self.RTOdifference = None
        self.GTdifference = None
    
    
    def run(self):
        #start listener in thread
        Thread(target=self.net.listener, args=[SERVERPORT], daemon=True).start()
        print("Headend recv socket is now listening.")
        print("")
        
        #connect to backend
        try:
            self.net.connect("192.168.1.107", 8888)
        except:
            sys.exit("ERROR: Could not connect to backend")


        
        try:
            while True:
                for key in self.net.data.keys():
                    if len(self.net.data[key]) > 0:
                        print(f"\nData Received from Node\n___________")

                        # Get sensor packet from input buffer                      
                        data = self.net.data[key].pop(0)


                        #start creating new frame
                        dataframe = ProcessData()
                        # Capture the time the data has been generated
                        dataTime = data["recvTime"]

                        # attach the data time to the dataframe
                        dataframe.setDataTime(dataTime)
                        

                        # attach the previous transmit time to the dataframe
                        dataframe.setTxTime(self.txTime)


                        # attach the post transmission time to the dataframe
                        dataframe.setPostTxTime(self.postTxTime)
                      

                        #attach sender data to dataframe
                        dataframe.receivedIP=key
                        
                        # attach the payload to the dataframe
                        dataframe.setPayload(data["data"])

                        if not self.RTOdifference == RTO.offset or not self.GTdifference == GT.offset:
                            dataframe.setRTO(RTO.offset)
                            self.RTOdifference = RTO.offset
                            dataframe.setGT(GT.offset)
                            self.GTdifference = GT.offset

                        #build dataframe into string form
                        packet = dataframe.buildHeadendFrame()
                        # Capture the time the data has begun transmission
                        self.txTime = VKT.get()              
                        

                       # print("Transmitting packet:")
                        #frPrint(packet)

                        #transmit packet
                        self.net.transmit(packet)                  

                        if verbose:
                            print("Recieved Packet:")
                            frPrint(data['data'])
                            print("")

                            print("Transmitting Packet: ")
                            frPrint(packet)
                            #print(f"\nDataframe using Key is: {self.net.data[key]}")
                            # print(f"Dataframe is using Key: {net.data[key][0]['data']}")
                            # print(proc.unpack(net.data[key]['data']))             
                        print(f"______________________________________\n")

                    else:
                        sleep(1)
        except KeyboardInterrupt:
            print("\rClosing network, please don't keyboardinterrupt again...")

        self.net.close()

# The main of this program
if "main" in __name__:
    #define a synchronization object for the clock GT
    syncGT = Sync(
        address=ipGT,
        interface=interfaceGT,
        clock=GT
    )
    #start the synchronization thread
    syncGT.start()

    syncRTO = Sync(
        address=ipSVT,
        interface=interfaceSVT,
        clock=RTO
    )
    syncRTO.start()

    #if NTP is desired, then also define and start a VKT synchronization object
    if syncMode == "ntp":
        syncVKT = Sync(
            address=ipSVT,
            interface=interfaceSVT,
            clock=VKT
        )
        syncVKT.start() 

    headend = headendlistener((ipOut, int(portOut)), interfaceTarget)
    headend.run()    
