import include.Network as n


ADDR = ""
PORT= 12345

s = n.Network()
s.listener(ADDR, PORT)
print("socket is now listening.")

