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
            print(net.data[key].pop(0))
        else:
            sleep(1)