from include.setup import *
from include.Database import *

SERVERADDR = ""
SERVERPORT = portIn

def unpack(packet, recvIP, recvTime):

    layers = packet.count(EOP) + 1  # Check the number of headend jumps
    nodes = packet.split(EOP)       # Split the frames from each headend

    nodeData = [{key: value for key, value in []} for i in range(layers)]

    lastIP = recvIP

    print(f"Frame Layers: {layers}\n")

    if layers > 0:
        for i in range(layers-1):
            frameData = nodes[i].split(SEP)

            if verbose:
                print(f"\nHeadend Frame Number:       {i+1}\n")
                # print(f" -  Current Frama Data:         {key}")
                print(f" -  Current Receive IP:         {lastIP}")
                print(f" -  Current rxTime:             {frameData[0]}")
                print(f" -  Current txTime:             {frameData[1]}")
                
            nodeData[i]['nodeIP'] = lastIP
            nodeData[i]['rxTime'] = frameData[0]
            nodeData[i]['rxTimeGT'] = frameData[0]
            nodeData[i]['txTime'] = frameData[1]
            nodeData[i]['txTimeGT'] = frameData[1]
            # print(f" -  Current Payload:            {frameData[4]}")
            lastIP = frameData[3]


            if frameData[2].count(DSEP) > 0:
                pigFrame = frameData[2].split(DSEP)

                if verbose:
                    print(f" -  Current postTxTime:         {pigFrame[0]}")
                    print(f" -  Current Piggy:              {pigFrame[1]}")
                nodeData[i]['postTxTime'] = pigFrame[0]
                nodeData[i]['postTxTimeGT'] = pigFrame[0]
                nodeData[i]['payload'] = pigFrame[1]

            else:
                if verbose:
                    print(f" -  Current postTxTime:         {frameData[2]}")
                nodeData[i]['postTxTime'] = frameData[2]
                nodeData[i]['postTxTimeGT'] = frameData[2]
                
                

    frameData = nodes[layers-1].split(SEP)

    if verbose:
        print(f"\nSensor Frame Number:        {layers}")
        print(f" -  Current Receive IP:         {lastIP}")
        print(f" -  Sensor genTime:             {frameData[0]}")
        print(f" -  Sensor txTime:              {frameData[1]}")
        print(f" -  Sensor postTxTime:          {frameData[2]}")
        print(f" -  Sensor Payload:             {frameData[3]}")
    nodeData[layers-1]['nodeIP'] = lastIP
    nodeData[layers-1]['rxTime'] = frameData[0]
    nodeData[layers-1]['rxTimeGT'] = frameData[0]
    nodeData[layers-1]['txTime'] = frameData[1]
    nodeData[layers-1]['txTimeGT'] = frameData[1]
    nodeData[layers-1]['postTxTime'] = frameData[2]
    nodeData[layers-1]['postTxTimeGT'] = frameData[2]
    nodeData[layers-1]['payload'] = frameData[3]


    # comDelay = float(recvTime) - float(frameData[0])

    # print(f"\nNodeData Dict Contains:")
    # for i in range(len(nodeData)):
    #     print(nodeData[i])

    db.insertData(nodeData, 101.23)





#                End
#  --   General Thingy Stuff   --
#######################################
#######################################
#  --    Function Creation     --
#               Start


# adapt = NetTechnology()

net = Network(interfaceTarget)
Thread(target=net.listener, args=[SERVERPORT]).start()
print("Server socket is now listening.")


dbPath = str(os.getcwd()) + "/include/db.db3"
db = Database(dbPath)     # Prepare the database

while True:
    for key in net.data.keys():
        if len(net.data[key]) > 0:
            data = net.data[key].pop(0)

            print(f"\n___________\nData Received from Node")
            frPrint(data['data'])   # Thomas' Formatting Thing

            if verbose:
                print(f"\nDataframe using Key is: {net.data[key]}")

            unpack(data['data'], key, data['recvTime'])
            print(f"______________________________________\n")

        else:
            sleep(1)

