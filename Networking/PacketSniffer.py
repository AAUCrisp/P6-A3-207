from scapy.all import *

def generate_trace_file(interface, count=25):
    capture = sniff(iface=interface, count=count)
    wrpcap(f"files/captures/{'test'}.pcap", capture)