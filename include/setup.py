# General setup for all nodes
import argparse         # For parsing terminal arguments
import sys
from threading import Thread
from time import time, sleep
import os
testPath = os.path.abspath("")
testPath = os.getcwd()
print(testPath)

# Own includes
from include.Formatting import *
from include.NetTechnology import *       # For finding netinterface IDs
from include.Network import *
from include.ProcessData import *
from include.Sync import *

ips = {
    'up0': {
        'wifi': '192.168.1.105',
        'gsm': '10.31.0.102',
        'ethernet': '10.0.0.40',
    },
    'up1': {
        'wifi': '192.168.1.80',
        'gsm': '10.31.0.13',
        'ethernet': '10.0.0.10',
    },
    'up2': {                        # has the NTP server
        'wifi': '192.168.1.107', 
        'gsm': '10.31.0.102',
        'ethernet': '10.0.0.20',
    },                              #############################
    'up3': {                        ##  FIND THE ETHERNET IPs  ##
        'wifi': '192.168.1.109',    #############################
        'gsm': '10.31.0.102',
        'ethernet': '10.0.0.30',
    },
    'cal': {
        'wifi': '192.168.1.189',    # Insert the right one here
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
parser.add_argument('-target', type=str, required=False)
parser.add_argument('-int', type=str, required=False)
parser.add_argument('-port', type=int, required=False)
parser.add_argument('-gt', type=str, required=False)
parser.add_argument('-gtInt', type=str, required=False)
parser.add_argument('-loop', action=argparse.BooleanOptionalAction)
parser.add_argument('-dev', action=argparse.BooleanOptionalAction)
parser.add_argument('-v', action=argparse.BooleanOptionalAction)
parser.add_argument('-delay', type=int, required=False)
parser.add_argument('-cwd', type=str, required=False)
args = parser.parse_args()    # The array containing our arguments

# print(args)
argsMsg = ' - Arguments Inserted' if len(sys.argv) > 1 else " - Program running without arguments"
print(argsMsg)

interfaceGT = str(args.gtInt) if args.gtInt else "ethernet"
ipGT = ips[str(args.gt)][interfaceGT] if args.gt else ips['up2'][interfaceGT]
interfaceTarget = str(args.int) if args.int else 'wifi'
ipTarget = ips[str(args.target)][interfaceTarget] if args.target else ips['up2'][interfaceTarget]
portTarget = str(args.port) if args.port else 8888

# Set working directory
global path
path = args.cwd if args.cwd else ""
if path != "":
    os.chdir(path)


"""This is the interval the sensor will transmit data in"""
rxInterval = int(args.delay) if args.delay else 3
global verbose
verbose = True if args.v else False

# If 'dev' argument is called
if args.dev: 
    ipTarget = '127.0.0.1'
    interfaceTarget = 'loopback'
    interfaceGT = 'wifi'
    ipGT = ips['up2'][interfaceGT]

# If 'loopback' argument is called
if args.loop: 
    ipTarget = '127.0.0.1'
    interfaceTarget = 'loopback'

if verbose:
    print(f"Set GT Interface is:  {interfaceGT}")
    print(f"Set GT IP is:         {ipGT}")
    print(f"Set Forward-Node is:  {interfaceTarget}")
    print(f"Set Forward IP is:    {ipTarget}")
    print(f"Set Forward Port is:  {portTarget}")
    print(f"Absolute Path is:     {path}")
    # dbPath = path + "/include/Database.py"
    # print(f"Absolute Path is:     {dbPath}")

    def frPrint(payload):
        print(payload.replace(SEP, red(" | ")).replace(DSEP, blue(" | ")).replace(EOP, magenta(" | ")))
