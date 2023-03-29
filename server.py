import include.setup

ADDR = ""
PORT= 12345

s = n.Network()
s.listener(ADDR, PORT)
print("Server socket is now listening.")

