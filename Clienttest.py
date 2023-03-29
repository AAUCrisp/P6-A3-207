import include.Network as n

c = n.Network("loopback")

port = 12345
addr = ''
message = "Random sensor data !!!!!!"

c.connect(addr, port)
c.transmit(message)