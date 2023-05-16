from ntplib import NTPPacket, system_to_ntp_time, time, NTPException, NTPStats
import socket
import os
import threading
from include.NetTechnology import *


class Clock:
    offset = 0
    parent = None

    def __init__(self, parentClock = time.time) -> None:
        self.parent = parentClock

    def get(self) -> float:
        return self.parent() + self.offset

    def set(self, value):
        self.offset = value - self.parent()


class Sync(threading.Thread):
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
    lock = threading.Lock()

    def __init__(self, clock:Clock, address = '192.168.1.107', interface='wifi', interval = 30) -> None:
        """```markdown
        
        This is the constructor of this class, it takes 2 parameters
        # Parameters:
        *   interface:  The network interface to synchronize over
        *   address:    The address of the server to be synchronized with
        """
        self.address = address
        self.interface = interface
        self.clock = clock
        self.interval = interval
        super().__init__(daemon=True)

    def sync(self):
        """This method synchronizes the "System Virtual Time", this is interpreted as NTP synchronization, here a method of ntplib has been modified as shown below to use a specific interface."""
        # get the NTP timestamp
        medium = NetTechnology(self.interface)
        try:
            return requestNTP(self.address, self.clock, interface=medium.getInterface())
        except NTPException as e:
            print("NTP DIED, retrying")
            return self.sync()
        # set the NTP timestamp on the system, this will only be changed for the running process if NTP synchronization is automatic on the system its running on.
        #os.system(f'date -s @{NTP}') <- deprecated functionality

    def suspend():
        Sync.lock.acquire()
    def resume():
        Sync.lock.release()
        time.sleep(.1)

    def run(self) -> None:
        print(f"\n\nSync Interval is: {self.interval}\n\n")
        while True:
            Sync.lock.acquire()
            self.clock.set(self.sync())
            Sync.lock.release()
            time.sleep(self.interval)

    


# This function is a modified version of the one found at: https://github.com/cf-natali/ntplib/blob/08d0f7ef766715a52f472901de5e382c8f773855/ntplib.py#L286
def requestNTP(host, clock:Clock, version=2, port="ntp", timeout=5, address_family=socket.AF_UNSPEC, interface:str = "lo"):  # pylint: disable=no-self-use,too-many-arguments
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
                mode=3,
                version=version,
                tx_timestamp=system_to_ntp_time(clock.get())
            )

            # send the request
            sock.sendto(query_packet.to_data(), sockaddr)

            # wait for the response - check the source address
            src_addr = (None,)
            while src_addr[0] != sockaddr[0]:
                response_packet, src_addr = sock.recvfrom(256)

            # build the destination timestamp
            dest_timestamp = system_to_ntp_time(clock.get())
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

    sync = Sync()
    sync.syncGT()