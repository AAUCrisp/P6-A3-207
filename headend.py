from twisted.internet import protocol, reactor
from include.setup import *
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
 
    def processData(self, data):
        txTime = -1
        GTTxTime = -1
        postTxTime = -1
        GTPostTxTime = -1
        # initialize the dataframe object
        dataframe = ProcessData()

        # Capture the time the data has been generated
        dataTime = SVTClock.get()
        GTDataTime = GTClock.get()

        # attach the data time to the dataframe
        dataframe.setDataTime(dataTime)
        dataframe.setGTDataTime(GTDataTime)  

        # attach the previous transmit time to the dataframe
        dataframe.setTxTime(txTime)
        dataframe.setGTTxTime(GTTxTime) 

        # attach the post transmission time to the dataframe
        dataframe.setPostTxTime(postTxTime)
        dataframe.setGTPostTxTime(GTPostTxTime)
        # attach the payload to the dataframe
        dataframe.setPayload("some data")

        #build dataframe into string form
        packet = dataframe.buildHeadendFrame()
        #encode into binary packet
        packet.encode("utf-8")
        # Capture the time the data has begun transmission
        #txTime = SVTClock.get()
        #GTTxTime = GTClock.get()
        return packet
        '''txTime = -1
        postTxTime = -1
        dataTime = SVTClock.get()
        
        dataframe = ProcessData()
        dataframe.setDataTime(dataTime)
        dataframe.setTxTime(txTime)
        dataframe.setPostTxTime(postTxTime)
        dataframe.setPayload("some data")

        txTime = SVTClock.get()
        packet = dataframe.buildHeadendFrame()
        packet = packet.encode("utf-8") '''
        
        

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
       
       #annotate packet with monitoring data, then print
        toForward = self.processData(data)
        print("Forwarding: ")
        print(type(toForward))
        print(FORMAT_FN(toForward))

        #if connectiction is open, write annotated packet. Else write to buffer
        if self.proxy_to_server_protocol:
            self.proxy_to_server_protocol.write(toForward)
        else:
            self.buffer = toForward
 
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
            print(type(data))
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
print("")
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