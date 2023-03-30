from include.setup import *

SERVERADDR = ""
SERVERPORT= 8888

# adapt = NetTechnology()

print(f"Target Interface is: " + interfaceTarget)
print(f"Target IP is: " + ipTarget)

net = Network(interfaceTarget)
Thread(target=net.listener, args=[SERVERPORT]).start()
print("Server socket is now listening.")
