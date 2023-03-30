# General setup for all nodes
import argparse         # For parsing terminal arguments
import sys
from threading import Thread
from time import sleep

# Own includes
from include.NetTechnology import *       # For finding netinterface IDs
from include.Network import *       # 
from include.ProcessData import *

ips = {
    'up0': {
        'wifi': '192.168.1.105',
        'gsm': '10.31.0.102',   # Not correct
        'ethernet': '192.168.0.1',
    },
    'up1': {
        'wifi': '192.168.1.80',
        'gsm': '10.31.0.13',
        'ethernet': '192.168.0.1'
    },
    'up2': {
        'wifi': '192.168.1.107',
        'gsm': '10.31.0.102',
        'ethernet': '192.168.0.1'
    },                              #############################
    'up3': {                        ##  FIND THE ETHERNET IPs  ##
        'wifi': '192.168.1.109',    #############################
        'gsm': '10.31.0.102',   # Not correct
        'ethernet': '192.168.0.1'
    },
    'cal': {
        'wifi': '192.168.1.109',    # Insert the right one here
        'ethernet': '192.168.0.1'
    },
    'ste': {
        'wifi': '192.168.1.76',
        'ethernet': '127.0.0.1'     # Tricked ya'!!, don't have ethernet
    },
    'tho': {
        'wifi': '192.168.1.176',
        'ethernet': '192.168.0.1'
    },
    'ub8': {
        'wifi': '192.168.1.182',
        'ethernet': '192.168.0.1'
    }
}

# Argument Parsing Setup
parser = argparse.ArgumentParser()
parser.add_argument('-ip', type=str, required=False)
parser.add_argument('-int', type=str, required=False)
parser.add_argument('-port', type=int, required=False)
parser.add_argument('-gtIp', type=str, required=False)
parser.add_argument('-gtInt', type=str, required=False)
parser.add_argument('-loop', action=argparse.BooleanOptionalAction)
args = parser.parse_args()    # The array containing our arguments

print(args)
argsMsg = ' - Arguments Inserted' if len(sys.argv) > 1 else " - Program running without arguments"
print(argsMsg)

interfaceGT = ips[str(args.gtInt)] if args.gtInt else "ethernet"
ipGT = ips[str(args.gtIp)] if args.gtIp else ips['up2']
interfaceTarget = ips[str(args.int)] if args.int else 'wifi'
ipTarget = ips[str(args.ip)] if args.ip else ips['up2']
portTarget = ips[str(args.port)] if args.port else 8888

# If 'loopback' argument is called
if args.loop: 
    ipTarget = '127.0.0.1'
    interfaceTarget = 'loopback'
