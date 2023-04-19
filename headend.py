#!/usr/bin/python3.11
from twisted.internet import protocol, reactor
from include.setup import *
#CMT - Adapted from https://robertheaton.com/2018/08/31/how-to-build-a-tcp-proxy-3/
# Adapted from http://stackoverflow.com/a/15645169/221061

HEADENDIP = "192.168.1.189" #IP Address of the device running this script
BACKENDIP = int(ipOut)           #IP Address of target Backend sever (192.168.1.107 by default)


class TCPProxyProtocol(protocol.Protocol):
    """
    TCPProxyProtocol listens for TCP connections from a
    client (eg. a sensor node) and forwards them on to a
    specified destination (eg. the backend or another headend) over
    a second TCP connection, using a ProxyToServerProtocol.
    It assumes that neither leg of this trip is encrypted.
    """
    def __init__(self):
        self.buffer = None
        self.proxy_to_server_protocol = None
        self.sensorIP = '0.0.0.0'   
        self.sensorPort = 0
        self.txTime = -1
        self.GTTxTime = -1
        self.postTxTime = -1
        self.GTPostTxTime = -1
 
    def connectionMade(self):
        """
        Called by twisted when a client connects to the
        proxy. Makes an connection from the headend to the
        backend to complete the chain.
        """
        
        self.sensorIP = self.transport.client[0]
        self.sensorPort = self.transport.client[1]
        print(type(self.sensorPort))
        #print(self.sensorIP)
        print("Connection made from Client %s:%d => Headend" % (self.sensorIP, self.sensorPort))
        proxy_to_server_factory = protocol.ClientFactory()
        proxy_to_server_factory.protocol = ProxyToServerProtocol
        proxy_to_server_factory.server = self

 
        reactor.connectTCP(DST_IP, DST_PORT,
                           proxy_to_server_factory)
 
    def processData(self, data):       
        # initialize the dataframe object
        dataframe = ProcessData()

        # Capture the time the data has been generated
        dataTime = SVTClock.get()
        GTDataTime = GTClock.get()

        # attach the data time to the dataframe
        dataframe.setDataTime(dataTime)
        dataframe.setGTDataTime(GTDataTime)  

        # attach the previous transmit time to the dataframe
        dataframe.setTxTime(self.txTime)
        dataframe.setGTTxTime(self.GTTxTime) 

        # attach the post transmission time to the dataframe
        dataframe.setPostTxTime(self.postTxTime)
        dataframe.setGTPostTxTime(self.GTPostTxTime)

        #attach sender data to dataframe
        print(type(self.sensorIP))
        print(self.sensorIP)
        dataframe.setReceivedIP(self.sensorIP)
        # attach the payload to the dataframe
        dataframe.setPayload(data)

        #build dataframe into string form
        packet = dataframe.buildHeadendFrame()
        # Capture the time the data has begun transmission
        self.txTime = SVTClock.get()
        self.GTTxTime = GTClock.get()

        #encode packet into binary and return
        return packet.encode("utf-8")

    def dataReceived(self, data):
        """
        Called by twisted when the headend receives data from
        the client. Sends the data on to the server.
        CLIENT ===> HEADEND ===> DST
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
 
    def clientConnectionLost(self, transport, reason):
        reactor.stop()

    def write(self, data):
        self.transport.write(data)
      #  self.transport.loseConnection()
        self.postTxTime = SVTClock.get()

 
 
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
 
    def clientConnectionLost(self, transport, reason):
        reactor.stop()

    def write(self, data):
        if data:
            #print(type(data))
            self.transport.write(data)
            #self.transport.loseConnection()


def _noop(data):
    return data

def get_local_ip(iface):
   # ni.ifaddresses(iface)                               #should enable autodetection of network interfaces, but was unstable on the up boards
   # return ni.ifaddresses(iface)[ni.AF_INET][0]['addr'] #can be uncommented if desired, the "iface" string should match the network manager device name
   return HEADENDIP

FORMAT_FN = _noop

LISTEN_PORT = int(portIn)
DST_PORT = int(portOut)
DST_HOST = "backend" #string only needed if identifying backend by domain name
local_ip = HEADENDIP
DST_IP = int(portOut)
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

print("exited program")