from ntplib import NTPPacket, system_to_ntp_time, time, NTPException, NTPStats
import socket
import os



class Sync:
    def __init__(self, interface, address) -> None:
        self.address = address
        self.interface = interface

    def syncGT(self):
        NTP = requestNTP(self.address, interface=self.interface)
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
                mode=3,
                version=version,
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
