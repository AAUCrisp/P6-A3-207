import nntplib
import socket

ntp = nntplib.NNTP(("localhost", 8888))
ntp.sock.setsockopt()


class Sync:
    pass