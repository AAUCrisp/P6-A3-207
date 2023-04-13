# import include.Network as n
from include.setup import *


net = Network("loopback")

addr = '127.0.0.1'
message = "Random sensor data !!!!!!"

net.connect(addr, portIn)
net.transmit(message)
print("Message Sent")