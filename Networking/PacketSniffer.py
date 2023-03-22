import scapy.all as scapy
from sys import argv


def generate_trace_file(interface):
    try: capture = scapy.sniff(iface=interface)
    except KeyboardInterrupt: scapy.wrpcap(f"files/captures/{'test'}.pcap", capture)

def monitor(interface):
    capture = scapy

if "main" in __name__:
    iface = "lo" if not "--interface" in argv else argv[argv.index("--interface")+1]

    if "--trace" in argv: generate_trace_file(iface)
    elif "--monitor" in argv: monitor(iface)