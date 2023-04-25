from include.setup import *
from include.Database import *

SERVERADDR = ""
SERVERPORT = portIn

def unpack(packet, recvIP, recvTime):

    layers = packet.count(EOP)      # Check the number of headend jumps
    nodes = packet.split(EOP)       # Split the frames from each headend

    lastIP = recvIP

    if layers > 0:
        # for i, key in enumerate(nodes):
        for i in range(layers-1):
            frameData = nodes[i].split(SEP)
            if verbose:
                print(f"\nCurrent Frame Number:       {i}")
                # print(f" -  Current Frama Data:         {key}")
                print(f" -  Current rxTime:             {frameData[0]}")
                print(f" -  Current txTime:             {frameData[1]}")
            if len(frameData.count(DSEP)) > 0:
                pigFrame = frameData[2].split(DSEP)
                if verbose:
                    print(f" -  Current prevTxTime:         {pigFrame[0]}")
                    print(f" -  Current Piggy:              {pigFrame[1]}")
            else:
                if verbose:
                    print(f" -  Current prevTxTime:         {frameData[2]}")
                
            if verbose:
                print(f" -  Current Receive IP:         {frameData[3]}")
                print(f" -  Current Payload:            {frameData[4]}")
            lastIP = frameData[3]



    frameData = nodes[layers].split(SEP)
    if verbose:
        print(f"\nSensor Frame:")
        print(f" -  Sensor genTime:            {frameData[0]}")
        print(f" -  Sensor txTime:             {frameData[1]}")
        print(f" -  Sensor prevTxTime:         {frameData[2]}")
        print(f" -  Sensor Payload:            {frameData[3]}")

    comDelay = float(recvTime) - float(frameData[0])

    sensorParams = { 
        'where': {
            'ip5g': lastIP,
            'OR': None,
            'ipWifi': lastIP
            }, 
        }

    if verbose:
        print(f"\nWhere parameters in Backend is: {sensorParams['where']}\n")
        print(f"Where OR key is: {sensorParams['where']['ip5g']}\n")

    sensorData = db.fetch('Node', sensorParams)

    if verbose:
        print(f"Fetched Node Data is: {sensorData}")

    # Needs updates for the GT data...
    comTrans = { 
        'sensorId': sensorData[0]['id'],
        'combinedDelay': comDelay,
        'combinedDelayGT': comDelay,
        'dataTime': frameData[0],
        'dataTimeGT': frameData[0],
        'deliveryTime': recvTime,
        'deliveryTimeGT': recvTime,
        'technology': interfaceTarget
        }

    db.insert('CombinedTransfer', comTrans)

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

