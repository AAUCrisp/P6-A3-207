# General setup for all nodes
import argparse         # For parsing terminal arguments
import sys
from threading import Thread, Condition, Lock
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
        'wifi': '192.168.1.61',
        'gsm': '10.31.0.103',
        'ethernet': '10.0.0.40',
        'port': '8888',
    },
    'up1': {
        'wifi': '192.168.1.80',
        'gsm': '10.31.0.13',
        'ethernet': '10.0.0.10',
        'port': '8889',
    },
    'up2': {                        # has the NTP server
        'wifi': '192.168.1.107', 
        'gsm': '100.74.189.1',
        'ethernet': '10.0.0.20',
        'port': '8890',
    },                              #############################
    'up3': {                        ##  FIND THE ETHERNET IPs  ##
        'wifi': '192.168.1.251',     #############################
        'gsm': '10.31.0.12',
        'ethernet': '10.0.0.30',
        'port': '8891',
    },
    'cal': {
        'wifi': '192.168.1.189',    # Insert the right one here
        'ethernet': '192.168.0.1',
        'port': '8892',
    },
    'ste': {
        'wifi': '192.168.1.76',
        'ethernet': '127.0.0.1',     # Tricked ya'!!, don't have ethernet
        'port': '8893',
    },
    'tho': {
        'wifi': '192.168.1.176',
        'ethernet': '192.168.0.1',
        'port': '8894',
    },
    'ub8': {
        'wifi': '192.168.1.182',
        'ethernet': '192.168.0.1',
        'port': '8895',
    }
}

#                End
#  --  Preset Connection Info  --
#######################################
#  --  Argument Parsing Setup  --
#               Start

parser = argparse.ArgumentParser()
parser.add_argument('-payload', type=str, required=False)
parser.add_argument('-target', type=str, required=False)
parser.add_argument('-tech', type=str, required=False)
parser.add_argument('-portOut', type=int, required=False)
parser.add_argument('-portIn', type=int, required=False)
parser.add_argument('-gt', type=str, required=False)
parser.add_argument('-gtTech', type=str, required=False)
parser.add_argument('-loop', action=argparse.BooleanOptionalAction)
parser.add_argument('-dev', action=argparse.BooleanOptionalAction)
parser.add_argument('-v', action=argparse.BooleanOptionalAction)
parser.add_argument('-delay', type=float, required=False)
parser.add_argument('-RTOint', type=int, required=False)
parser.add_argument('-GTint', type=int, required=False)
parser.add_argument('-VKTint', type=int, required=False)
parser.add_argument('-cwd', type=str, required=False)
parser.add_argument('-sync', type=int, required=False, default=0)

args, _ = parser.parse_known_args()    # The array containing our arguments

# print(args)
argsMsg = ' - Arguments Inserted' if len(sys.argv) > 1 else " - Program running without arguments"
print(argsMsg)

# General System Arguments
payload = str(args.payload) if args.payload else 'some data2'
interfaceTarget = str(args.tech) if args.tech else 'wifi'
ipOut = ips[str(args.target)][interfaceTarget] if args.target else ips['up2'][interfaceTarget]
portOut = str(args.portOut) if args.portOut else 8888
# portOut = str(args.portOut) if args.portOut else ips['up2']['port']
portIn = str(args.portIn) if args.portIn else 8888
txInterval = int(args.delay) if not args.delay == None  else 3
intervalRTO = int(args.RTOint) if not args.RTOint == None else 30
intervalGT = int(args.GTint) if not args.GTint == None else 5
intervalVKT = int(args.VKTint) if not args.VKTint == None else 30

# GT Arguments
interfaceGT = str(args.gtTech) if args.gtTech else "ethernet"
ipGT = ips[str(args.gt)][interfaceGT] if args.gt else ips['up2'][interfaceGT]

# SVT Variables
interfaceRTO = interfaceTarget
ipRTO = ips['up2'][interfaceRTO]

# Synchronization mode
modes = {
    0:"none",
    1:"ntp"
}
syncMode = modes[int(args.sync)]

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
    interfaceRTO = 'wifi'
    ipRTO = ips['up2'][interfaceRTO]

#                End
#  --  Argument Parsing Setup  --
#######################################
#######################################
#  --   General Thingy Stuff   --
#               Start


if verbose:
    print(f"Set Payload is:       {payload}")
    print(f"Set GT Interface is:  {interfaceGT}")
    print(f"Set GT IP is:         {ipGT}")
    print(f"Set Forward-Node is:  {interfaceTarget}")
    print(f"Set Forward IP is:    {ipOut}")
    print(f"Set Forward Port is:  {portIn}")
    print(f"Absolute Path is:     {os.getcwd()}")
    print(f"GT Sync Interval is:  {intervalGT}")
    print(f"RTO Sync Interval is: {intervalRTO}\n")


#                End
#  --   General Thingy Stuff   --
#######################################
#######################################
#  --    Function Creation     --
#               Start



def frPrint(payload):
    print(payload.replace(SEP, green(" | ")).replace(PB, blue(" | ")).replace(EON, magenta(" | ")).replace(OFF, cyan(" | ")))




def dict_depth(dic, level = 1):

    str_dic = str(dic)
    counter = 0
    for i in str_dic:
        if i == "{" or i == "[":
            counter += 1
        elif i == "}" or i == "]":
            break

    return(counter)



def transposeArray(matrix):
    
    # print(f"Array in Transpose is: {matrix}")

    length = len(matrix)

    for i, key in enumerate(matrix):
        
        depth = len(matrix[key])
        global result

        if i == 0:
            result = [[None for j in range(length)] for i in range(depth)]
            # print(f"Empty array has structure {result}")

        for j, value in enumerate(matrix[key]):

            result[j][i] = value

            # print(f"""
            # In Transpose:
            #     i is: {i}
            #     key is: {key}
            #     j is: {j}
            #     value is: {value}
            #     array is now: {array}""")
     
    return result


# Synchronization setup
VKT = Clock()
GT = Clock()
RTO = Clock()
