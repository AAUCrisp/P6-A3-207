import include.Network as n

c = n.Network()

port = 12345
addr = ''
message = "Random sensor data !!!!!!"

c.connect(addr, port, "loopback")
c.transmit(message)