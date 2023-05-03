from include.setup import *
from include.Database import *

SERVERADDR = ""
SERVERPORT = portIn


def unpack(packet, recvIP, recvTime):

    layers = packet.count(EON)      # Check the number of headend jumps
    # layers = packet.count(EON) + 1  # Check the number of headend jumps
    nodes = packet.split(EON)       # Split the frames from each headend

    nodeData = [{key: value for key, value in []} for i in range(layers)]

    lastIP = recvIP
    newRTO = None
    newGT = None

    print(f"Frame Layers: {layers}\n")

    for i in range(layers):
        frameData = nodes[i].split(SEP)

        if verbose:
            print(f"\nHeadend Frame Number:       {i+1}\n")
            # print(f" -  Current Frama Data:         {key}")
            print(f" -  Current Receive IP:         {lastIP}")
            print(f" -  Current rxTime:             {frameData[0]}")
            print(f" -  Current txTime:             {frameData[1]}")

        nodeData[i]['nodeIP'] = lastIP
        nodeData[i]['rxTime'] = frameData[0]
        nodeData[i]['txTime'] = frameData[1]


        optFrame = frameData[2].split(PB)

        # print(f"OptFrame contains:   {optFrame}")



        #  --  If there's new Offsets  --
        if optFrame[0].count(OFF) > 0:

            # print(f"Inside Offset Area")

            offsetFrame = optFrame[0].split(OFF)
            nodeData[i]['postTxTime'] = offsetFrame[0]
            newRTO = offsetFrame[1]
            newGT = offsetFrame[2]
            nodeData[i]['RTO'] = offsetFrame[1]
            nodeData[i]['GT']= offsetFrame[2]

            if verbose:
                print(f" -  Current postTxTime:         {offsetFrame[0]}")


        else:
            if verbose:
                print(f" -  Current postTxTime:         {optFrame[0]}")
            nodeData[i]['postTxTime'] = optFrame[0]

        
        
        #  --  If there's Piggy Data  --
        # if optFrame[1]:
        if len(optFrame) > 1:
        # if frameData[2].count(PB) > 0:
            pigFrame = frameData[2].split(PB)
            # pigFrame = optFrame[1].split(PB)

            # print(f"Inside Piggy Area")

            if verbose:
                # print(f" -  Current postTxTime:         {optFrame[0].split(OFF)[0]}")
                print(f" -  Current Piggy:              {optFrame[1]}")

            nodeData[i]['payload'] = pigFrame[1]
        
        if i < layers - 1:
            lastIP = frameData[3]
        
        else:
            nodeData[i]['payload'] = nodes[i+1]


    # nodeData[layers-1]['payload'] = nodes[layers-1]
    print(f" -  Sensor Payload:             {nodeData[layers-1]['payload']}")


    db.insertData(nodeData, recvTime)






#                End
#  --   General Thingy Stuff   --
#######################################
#######################################
#  --    Function Creation     --
#               Start


# adapt = NetTechnology()

net = Network(interfaceTarget)
Thread(target=net.listener, args=[SERVERPORT], daemon=True).start()
print("Server socket is now listening.")


dbPath = str(os.getcwd()) + "/include/db.db3"
db = Database(dbPath)     # Prepare the database
try:
    while True:
                

        # for key in net.data.keys():
        #     if len(net.data[key]) > 0:
        #         print(f"\nData Received from Node\n___________")

        #         # Thomas' formating thing...
        #         data = net.data[key].pop(0)
                
        QueueSize =  net.data.qsize() #get size of packet queue
        # print("Queue Size: %d"%QueueSize)
        #if self.net.data.qsize() > 0:
        if QueueSize > 0: #if quee isn't empty, then pop first item
            data = net.popData()
            # ip = data["id"]
            # rxTime = data["recvTime"]
            # payload = data["data"]

            # print(f"\nReceived data from node: %s"% ip)

                
                
            if verbose:
                frPrint(data['data'])
                print(f"\nDataframe using Key is: {data['id']}")
                # print(f"Dataframe is using Key: {net.data[key][0]['data']}")
                # print(proc.unpack(net.data[key]['data']))

            unpack(data['data'], data['id'], data['recvTime'])

            # process = ProcessData()
            # unpacked = process.unpack()
            # unpacked = process.unpack(data['data'])
            # unpacked = unpack(data['data'])

            # print(f"Unpacked Array is: {unpacked}")
            
            # net.data[key].pop(0)
            print(f"______________________________________\n")

        else:
            sleep(1)
except KeyboardInterrupt:
    print("\rClosing network, please don't keyboardinterrupt again...")

net.close()
