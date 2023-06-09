from twisted.internet import protocol, reactor
#CMT - Adapted from https://robertheaton.com/2018/08/31/how-to-build-a-tcp-proxy-3/
# Adapted from http://stackoverflow.com/a/15645169/221061

HEADENDIP = "192.168.1.189"
BACKENDIP = "192.168.1.107"


class TCPProxyProtocol(protocol.Protocol):
    """
    TCPProxyProtocol listens for TCP connections from a
    client (eg. a phone) and forwards them on to a
    specified destination (eg. an app's API server) over
    a second TCP connection, using a ProxyToServerProtocol.
    It assumes that neither leg of this trip is encrypted.
    """
    def __init__(self):
        self.buffer = None
        self.proxy_to_server_protocol = None
 
    def connectionMade(self):
        """
        Called by twisted when a client connects to the
        proxy. Makes an connection from the proxy to the
        server to complete the chain.
        """
        print("Connection made from CLIENT => PROXY")
        proxy_to_server_factory = protocol.ClientFactory()
        proxy_to_server_factory.protocol = ProxyToServerProtocol
        proxy_to_server_factory.server = self
 
        reactor.connectTCP(DST_IP, DST_PORT,
                           proxy_to_server_factory)
 
    def dataReceived(self, data):
        """
        Called by twisted when the proxy receives data from
        the client. Sends the data on to the server.
        CLIENT ===> PROXY ===> DST
        """
        print("")
        print("CLIENT => SERVER")
        print(FORMAT_FN(data))
        print("")
        if self.proxy_to_server_protocol:
            self.proxy_to_server_protocol.write(data)
        else:
            self.buffer = data
 
    def write(self, data):
        self.transport.write(data)
 
 
class ProxyToServerProtocol(protocol.Protocol):
    """
    ProxyToServerProtocol connects to a server over TCP.
    It sends the server data given to it by an
    TCPProxyProtocol, and uses the TCPProxyProtocol to
    send data that it receives back from the server on
    to a client.
    """

    def connectionMade(self):
        """
        Called by twisted when the proxy connects to the
        server. Flushes any buffered data on the proxy to
        server.
        """
        print("Connection made from PROXY => SERVER")
        self.factory.server.proxy_to_server_protocol = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
 
    def dataReceived(self, data):
        """
        Called by twisted when the proxy receives data
        from the server. Sends the data on to to the client.
        DST ===> PROXY ===> CLIENT
        """
        print("")
        print("SERVER => CLIENT")
        print(FORMAT_FN(data))
        print("")
        self.factory.server.write(data)
 
    def write(self, data):
        if data:
            self.transport.write(data)


def _noop(data):
    return data

def get_local_ip(iface):
   # ni.ifaddresses(iface)
   # return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
   return HEADENDIP

FORMAT_FN = _noop

LISTEN_PORT = 8888
DST_PORT = 8888
DST_HOST = "backendq"
local_ip = HEADENDIP
DST_IP = BACKENDIP
print("Headend IP: %s" % local_ip)
print("Backend IP: %s" % DST_IP)

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
 
print("""
Listening for requests on %s:%d...
""" % (local_ip, LISTEN_PORT))

factory = protocol.ServerFactory()
factory.protocol = TCPProxyProtocol
reactor.listenTCP(LISTEN_PORT, factory)
reactor.run()












"""from twisted.internet import protocol, reactor
import netifaces as ni


class TCPForward(protocol.Protocol):
    def __init__(self):
        self.buffer = None
        self.sensorToHeadendProtocol = None
    
    def connectionMade(self):
        print("Connection made from SENSOR -> HEADEND")
        sensorToHeadendFactory = protocol.ClientFactory()
        sensorToHeadendFactory.protocol = headEndToBackEndProtocol
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
#-#-#-#-#-#-RUNNING  TCP PROXY-#-#-#-#-#-
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
"""Dst IP:\t%s
Dst port:\t%d
Dst hostname:\t%s
Listen port:\t%d
Local IP:\t%s """
""" % (DST_IP, DST_PORT, DST_HOST, LISTEN_PORT, local_ip))

"""#print(""" Listening for requests on %s:%d...
#""" % (local_ip, DST_HOST, local_ip, LISTEN_PORT)) 

"""factory = protocol.ServerFactory()
factory.protocol = TCPForward
reactor.listenTCP(LISTEN_PORT, factory)
reactor.run() """






