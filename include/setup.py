# General setup for all nodes
import argparse         # For parsing terminal arguments
import sys
from threading import Thread, Lock
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


#######################################
#  --  Preset Connection Setup  --
#               Start

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

#                End
#  --  Preset Connection Info  --
#######################################
#  --  Argument Parsing Setup  --
#               Start

parser = argparse.ArgumentParser()
parser.add_argument('-target', type=str, required=False)
parser.add_argument('-tech', type=str, required=False)
parser.add_argument('-portOut', type=int, required=False)
parser.add_argument('-portIn', type=int, required=False)
parser.add_argument('-gt', type=str, required=False)
parser.add_argument('-gtTech', type=str, required=False)
parser.add_argument('-loop', action=argparse.BooleanOptionalAction)
parser.add_argument('-dev', action=argparse.BooleanOptionalAction)
parser.add_argument('-v', action=argparse.BooleanOptionalAction)
parser.add_argument('-delay', type=int, required=False)
parser.add_argument('-cwd', type=str, required=False)
args = parser.parse_args()    # The array containing our arguments

# print(args)
argsMsg = ' - Arguments Inserted' if len(sys.argv) > 1 else " - Program running without arguments"
print(argsMsg)

# General System Arguments
interfaceTarget = str(args.tech) if args.tech else 'wifi'
ipOut = ips[str(args.target)][interfaceTarget] if args.target else ips['up2'][interfaceTarget]
portOut = str(args.port) if args.portOut else 8888
portIn = str(args.port) if args.portIn else 8888
txInterval = int(args.delay) if args.delay else 3

# GT Arguments
interfaceGT = str(args.gtTech) if args.gtTech else "ethernet"
ipGT = ips[str(args.gt)][interfaceGT] if args.gt else ips['up2'][interfaceGT]

# SVT Variables
interfaceSVT = interfaceTarget
ipSVT = ips['up2'][interfaceSVT]


# Development Arguments
if args.cwd:
    os.chdir(args.cwd)

verbose = True if args.v else False

if args.dev:
    interfaceGT = 'wifi'
    ipGT = ips['up2'][interfaceGT]

if args.loop or args.dev: 
    ipOut = '127.0.0.1'
    interfaceTarget = 'loopback'
    interfaceSVT = 'wifi'
    ipSVT = ips['up2'][interfaceSVT]

#                End
#  --  Argument Parsing Setup  --
#######################################
#######################################
#  --   General Thingy Stuff   --
#               Start


if verbose:
    print(f"Set GT Interface is:  {interfaceGT}")
    print(f"Set GT IP is:         {ipGT}")
    print(f"Set Forward-Node is:  {interfaceTarget}")
    print(f"Set Forward IP is:    {ipOut}")
    print(f"Set Forward Port is:  {portIn}")
    print(f"Absolute Path is:     {os.getcwd()}\n")


def frPrint(payload):
    print(payload.replace(SEP, green(" | ")).replace(DSEP, blue(" | ")).replace(EOP, magenta(" | ")))


def dict_depth(dic, level = 1):

    str_dic = str(dic)
    counter = 0
    for i in str_dic:
        if i == "{" or i == "[":
            counter += 1
        elif i == "}" or i == "]":
            break

    return(counter)