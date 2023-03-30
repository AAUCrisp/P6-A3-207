from include.setup import *

# SERVERADDR = ""
SERVERPORT= 8888

# adapt = NetTechnology()


net = Network(interfaceTarget)
net.listener(SERVERPORT)
print("Server socket is now listening.")

