# Module file, this is used to test the include files functionality

import NetTechnology
import ProcessData

wifi = NetTechnology.NetTechnology()

print(f'wifi: {wifi.connection}')
print(f'wifi: {wifi.deviceName}')
print(f'wifi: {wifi.getInterface()}')
print(f'wifi: {wifi.type}')

loopback = NetTechnology.NetTechnology("loopback")

print(f'loopback: {loopback.connection}')
print(f'loopback: {loopback.deviceName}')
print(f'loopback: {loopback.getInterface()}')
print(f'loopback: {loopback.type}')

ethernet = NetTechnology.NetTechnology("ethernet")

print(f'ethernet: {ethernet.connection}')
print(f'ethernet: {ethernet.deviceName}')
print(f'ethernet: {ethernet.getInterface()}')
print(f'ethernet: {ethernet.type}')

for i in range(1, 11):
    try:
        dataFrame = ProcessData.ProcessData(f'test{ProcessData.ProcessData.SEPERATOR}'*i)
        print(f'{i}] Data: {dataFrame.data}, timestamp: {dataFrame.timestamp}, pTime: {dataFrame.pTime}')
        builtFrame = dataFrame.buildFrame()
        unpacked = ProcessData.ProcessData.unpackFrame(builtFrame)
        print(f'{i}] Data: {unpacked.data}, timestamp: {unpacked.timestamp}, pTime: {unpacked.pTime}')
        print()
    except Exception as e:
        print(e.with_traceback())