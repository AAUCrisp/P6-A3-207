from include.setup import *

HEADENDADDR = ""        #Set constants for node address and port
HEADENDPORT = 8888

print(f"Target Interface is: " + interfaceTarget) # from include.setup, print target interface and IP
print(f"Target IP is: " + ipTarget)

net = Network(interfaceTarget)
Thread(target=net.listener, args=[HEADENDPORT]).start()
print("Headend recieve socket is now listening...")

txTime = -1         #initialize variables
postTxTime = -1

while True:
    for packet in net.data: #for every packet that comes in the buffer
        if len(net.data) > 0:   #as long as it isn't null       
            dataframe = ProcessData()
            dataframe.setTxTime(txTime)
            dataframe.setPostTxTime(postTxTime)
            dataframe.setPayload(net.data)
            txTime = time()
            net.transmit(dataframe.buildHeadendFrame())
            postTxTime = time()

        




'''while True:
    for key in net.data.keys():
        if len(net.data[key]) > 0:
            print(net.data[key].pop(0))
        else:
            sleep(1) '''






