# Module file, this is used to test the include files functionality

import sys
import time
print(sys.path)
print(sys.path.append(sys.path[0]+"/.."))

from include.NetTechnology import NetTechnology
from include.ProcessData import ProcessData, SEP, DSEP, EOP
from include.Sync import Sync
from include.Formatting import *


wifi = NetTechnology("wifi")

print(f'wifi: {wifi.connection}')
print(f'wifi: {wifi.deviceName}')
print(f'wifi: {wifi.getInterface()}')
print(f'wifi: {wifi.type}')

loopback = NetTechnology("loopback")

print(f'loopback: {loopback.connection}')
print(f'loopback: {loopback.deviceName}')
print(f'loopback: {loopback.getInterface()}')
print(f'loopback: {loopback.type}')

ethernet = NetTechnology("ethernet")

print(f'ethernet: {ethernet.connection}')
print(f'ethernet: {ethernet.deviceName}')
print(f'ethernet: {ethernet.getInterface()}')
print(f'ethernet: {ethernet.type}')

#sync = Sync(interfaceGT = wifi.getInterface(), addressGT="dk.pool.ntp.org")
#sync.syncGT()

dataframe = ProcessData(dataTime=time.time(), txTime=time.time(), postTxTime=time.time(), payload="dataframe")

print(ProcessData.unpack(dataframe.buildSensorFrame()))

headendDataframe = ProcessData(startTime=time.time(), txTime=time.time(), postTxTime=time.time(), piggy="piggyData", payload=dataframe.buildSensorFrame(), receivedIP="localhost")

print(ProcessData.unpack(headendDataframe.buildHeadendFrame()))

print()
print(headendDataframe.buildHeadendFrame().replace(SEP, green("|")).replace(DSEP, blue("|")).replace(EOP, magenta("|")))