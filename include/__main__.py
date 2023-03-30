# Module file, this is used to test the include files functionality

import sys
import time
print(sys.path)
print(sys.path.append(sys.path[0]+"/.."))

from include.NetTechnology import NetTechnology
from include.ProcessData import ProcessData
from include.Sync import Sync


wifi = NetTechnology()

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

for i in range(1, 11):
    try:
        dataframe = ProcessData("hello").buildFrame()
        print(f'dataframe: {dataframe}')
        unpacked = ProcessData.unpackFrame(dataframe)
        print(f'timestamp: {unpacked.timestamp}, ptime: {unpacked.pTime}, data: {unpacked.data}')
    except Exception as e:
        print(e)

for i in range(1, 11):
    try:
        dataframe = ProcessData(ProcessData("hello").buildFrame()).setReceivedId("localhost").setReceivedTimestamp(time.time()).setPiggy("world!").buildFrame()
        print(f'dataframe: {dataframe}')
        unpacked = ProcessData.unpackFrame(dataframe)
        print(f'timestamp: {unpacked.timestamp}, ptime: {unpacked.pTime}, received IP: {unpacked.receivedId}, received time: {unpacked.receivedTimestamp}, piggyData: {unpacked.piggy}, data: {unpacked.data}')
    except Exception as e:
        print(e)

sync = Sync(interfaceGT = wifi.getInterface(), addressGT="dk.pool.ntp.org")
sync.syncGT()