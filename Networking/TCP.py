import socket
import struct

class TCP_INFO:
    data = {
    "tcpi_state":           "",
    "tcpi_ca_state":        "",
    "tcpi_retransmits":     "",
    "tcpi_probes":          "",
    "tcpi_backoff":         "",
    "tcpi_options":         "",
    "tcpi_snd_wscale":      "",
    "tcpi_rto":             "",
    "tcpi_ato":             "",
    "tcpi_snd_mss":         "",
    "tcpi_rcv_mss":         "",
    "tcpi_unacked":         "",
    "tcpi_sacked":          "",
    "tcpi_lost":            "",
    "tcpi_retrans":         "",
    "tcpi_fackets":         "",
    "tcpi_last_data_sent":  "",
    "tcpi_last_ack_sent":   "",
    "tcpi_last_data_recv":  "",
    "tcpi_last_ack_recv":   "",
    "tcpi_pmtu":            "",
    "tcpi_rcv_ssthresh":    "",
    "tcpi_rtt":             "",
    "tcpi_rttvar":          "",
    "tcpi_snd_ssthresh":    "",
    "tcpi_snd_cwnd":        "",
    "tcpi_advmss":          "",
    "tcpi_reordering":      "",
    "tcpi_rcv_rtt":         "",
    "tcpi_rcv_space":       "",
    "tcpi_total_retrans":   "" 
    }

    def __init__(self, s:socket.socket) -> None:
        tcp_info = struct.unpack("B"*7+"I"*24, s.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, struct.calcsize("B"*7+"I"*24)))
        for key, value in zip(self.data.keys(), tcp_info):
            self.data[key] = value
    
    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
        
if "main" in __name__:
    import os
    import sys

    sys.path.append(f"../{os.path.abspath('.').split('/').pop()}")
    from Terminal.Formatting import Table

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    info = TCP_INFO(s)

    table = Table(info.data, "TCP_INFO:")
    table.print()

    s.close()