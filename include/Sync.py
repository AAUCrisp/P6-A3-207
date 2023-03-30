from ntplib import NTPPacket, system_to_ntp_time, time, NTPException, NTPStats
import socket
import os
from NetTechnology import *



class Sync:
    """```markdown
    
    This class is used to synchronize the testbed, it will have 2 attributes and 3 methods:
    # Attributes:
    *   address:    The address of the server to be synchronized with
    *   interface:  The network interface to synchronize over
    # Methods:
    *   syncGT():   synchronizes the system with NTP
    *   syncTime(): synchronizes the system with the local time of the other systems in the network
    *   syncVclk(): synchronizes using a vector clock
    ```"""

    def __init__(self, addressGT, address = '127.0.0.1', interface='wifi', interfaceGT = 'ethernet') -> None:
        """```markdown
        
        This is the constructor of this class, it takes 2 parameters
        # Parameters:
        *   interface:  The network interface to synchronize over
        *   address:    The address of the server to be synchronized with
        """
        self.address = address
        self.interface = interface
        self.addressGT = addressGT
        self.interfaceGT = interfaceGT


    def syncGT(self):
        """This method synchronizes the "Ground Truth", this is interpreted as NTP synchronization, here a method of ntplib has been modified as shown below to use a specific interface."""
        # get the NTP timestamp
        ethernet = NetTechnology(self.interfaceGT)

        NTP = requestNTP(self.addressGT, interface=ethernet.getInterface())
        # set the NTP timestamp on the system, this will only be changed for the running process if NTP synchronization is automatic on the system its running on.
        os.system(f'date -s @{NTP}')







# This function is a modified version of the one found at: https://github.com/cf-natali/ntplib/blob/08d0f7ef766715a52f472901de5e382c8f773855/ntplib.py#L286
def requestNTP(host, version=2, port="ntp", timeout=5, address_family=socket.AF_UNSPEC, interface:str = "lo"):  # pylint: disable=no-self-use,too-many-arguments
        """Query a NTP server.
        Parameters:
        host           -- server name/address
        version        -- NTP version to use
        port           -- server port
        timeout        -- timeout on socket operations
        address_family -- socket address family
        Returns:
        NTPStats object
        """

        # lookup server address
        addrinfo = socket.getaddrinfo(host, port, address_family)[0]
        family, sockaddr = addrinfo[0], addrinfo[4]

        # create the socket
        sock = socket.socket(family, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode())

        try:
            sock.settimeout(timeout)

            # create the request packet - mode 3 is client
            query_packet = NTPPacket(
                version=version,
                mode=3,
                tx_timestamp=system_to_ntp_time(time.time())
            )

            # send the request
            sock.sendto(query_packet.to_data(), sockaddr)

            # wait for the response - check the source address
            src_addr = (None,)
            while src_addr[0] != sockaddr[0]:
                response_packet, src_addr = sock.recvfrom(256)

            # build the destination timestamp
            dest_timestamp = system_to_ntp_time(time.time())
        except socket.timeout:
            raise NTPException("No response received from %s." % host)
        finally:
            sock.close()

        # construct corresponding statistics
        stats = NTPStats()
        stats.from_data(response_packet)
        stats.dest_timestamp = dest_timestamp

        return stats.tx_time


# The main of this program
if "main" in __name__:

    sync = Sync(addressGT='10.0.0.20')
    sync.syncGT()