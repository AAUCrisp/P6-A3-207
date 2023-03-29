import include.Network as n
from sys import argv


ADDR = ""
PORT= 12345 if not "--port" in argv else int(argv[argv.index("--port")+1])
s = n.Network("loopback")
s.listener(ADDR, PORT)
