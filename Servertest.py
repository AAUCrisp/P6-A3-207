import include.Network as n


ADDR = ""
PORT= 12345

s = n.Network()
s.listener(ADDR, PORT, "loopback")
print("socket is now listening.")

