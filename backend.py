from include.setup import *

SERVERADDR = ""
SERVERPORT= 8888

# adapt = NetTechnology()

print(f"Target Interface is: " + interfaceTarget)
print(f"Target IP is: " + ipTarget)

net = Network(interfaceTarget)
Thread(target=net.listener, args=[SERVERPORT]).start()
print("Server socket is now listening.")

while True:
    for key in net.data.keys():
        if len(net.data[key]) > 0:
            packetData = net.data[key].pop(0)
            print(packetData)
            packet = ProcessData(packetData["data"], True)
            transDelay = packetData['recvTime'] - float(packet.timestamp)
            print("Sent Timestamp:       " + packet.timestamp)
            print("Receive Timestamp:    " + str(packetData["recvTime"]))
            print("Transmission Delay:   " + str(transDelay))

        else:
            sleep(1)