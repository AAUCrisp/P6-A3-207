# import include.Network as n
from include.setup import *


net = Network("loopback")

addr = ''
message = "Random sensor data !!!!!!"

net.connect(addr, portTarget)
net.transmit(message)