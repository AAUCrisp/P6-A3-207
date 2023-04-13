from twisted.internet import protocol, reactor
import netifaces as ni


class TCPForward(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.sensorToHeadendProtocol = None
    
    def connectionMade(self):
        print("Connection made from SENSOR -> HEADEND")
        sensorToHeadendFactory = protocol.ClientFactory()
        sensorToHeadendFactory.protocol = sensorToHeadendProtocol
        sensorToHeadendFactory.server = self

        reactor.connectTCP(DIST_IP, DST_PORT, sensorToHeadendFactory)

    def dataRecieved(self, data):
        print("")
        print("Sensor -> Headend")
        print(FORMAT_FN(data))
        print("")

        if self.sensorToHeadendProtocol: 
            self.sensorToHeadendProtocol.write(data)

        else: 
            self.buffer = data

class headEndToBackEndProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connection made form headend -> server")
        self.factory.server.headEndtoBackEndProtocol = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    def dataRecieved(self, data):
        print("")
        print("Headend -> Backend")
        print(FORMAT_FN(data))
        print("")
        self.factory.server.write(data)

    def write(self, data):
        if data:
            self.transport.write(data)

def _noop(data):
    return data

def get_local_ip(iface):
    ni.ifaddresses(iface)
    return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']

FORMAT_FN = _noop

LISTEN_PORT = 8888
DST_PORT = 8888
DST_HOST = "backend"
DST_IP = "192.168.1.107"

local_ip = get_local_ip("wlp3s0")


print("""
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
-#-#-#-#-#-RUNNING  TCP PROXY-#-#-#-#-#-
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
Dst IP:\t%s
Dst port:\t%d
Dst hostname:\t%s
Listen port:\t%d
Local IP:\t%s
""" % (DST_IP, DST_PORT, DST_HOST, LISTEN_PORT, local_ip))

#print(""" Listening for requests on %s:%d...
#""" % (local_ip, DST_HOST, local_ip, LISTEN_PORT)) 

factory = protocol.ServerFactory()
factory.protocol = TCPForward
reactor.listenTCP(LISTEN_PORT, factory)
reactor.run()





