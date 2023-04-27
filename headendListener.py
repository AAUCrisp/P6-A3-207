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
        print("Headend recv socket is now listening.....")
        print("")
        
        #connect to backend
        try:
            self.net.connect(SERVERADDR, SERVERPORT)
        except:
            sys.exit("ERROR: Could not connect to backend")


        
        try:
            while True:
                if self.net.data.qsize() > 0:
                    data = self.net.popData()
                    ip = data["id"]
                    rxTime = data["recvTime"]
                    payload = data["data"]

                    print(f"\nReceived data from node: %s"% ip)

                    # Get sensor packet from input buffer                      


                    #start creating new frame
                    dataframe = ProcessData()
                    # Capture the time the data has been generated
                    dataTime = rxTime

                    # attach the data time to the dataframe
                    dataframe.setDataTime(dataTime)
                        

                    # attach the previous transmit time to the dataframe
                    dataframe.setTxTime(self.txTime)


                    # attach the post transmission time to the dataframe
                    dataframe.setPostTxTime(self.postTxTime)
                      

                    #attach sender data to dataframe
                    dataframe.receivedIP=ip
                        
                    # attach the payload to the dataframe
                    dataframe.setPayload(payload)

                    if not self.RTOdifference == RTO.offset or not self.GTdifference == GT.offset:
                        dataframe.setRTO(RTO.offset)
                        self.RTOdifference = RTO.offset
                        dataframe.setGT(GT.offset)
                        self.GTdifference = GT.offset

                    #build dataframe into string form
                    packet = dataframe.buildHeadendFrame()
                    # Capture the time the data has begun transmission
                    self.txTime = VKT.get()              
                        
                    #transmit packet
                    self.net.transmit(packet)
                    self.postTxTime = VKT.get()                  

                    if verbose:
                        print("Recieved Packet:")
                        frPrint(data['data'])
                        print("")

                        print("Transmitting Packet: ")
                        frPrint(packet)           
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
