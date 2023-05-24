from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def getData(sensorid, fileName):
    db = Database(fileName)

    combinedDelayParam = {
        'select' : 'PayloadTransfer.combinedDelay',
        'where' : {'sensorId': sensorid}
    }

    offsetParam = {
        'select' : 'TransferJump.RTO, TransferJump.GT',
        'where' : {'nodeid' : sensorid}
    }

    combinedDelay = db.fetch('PayloadTransfer', combinedDelayParam)
    offset = db.fetch('TransferJump', offsetParam)

    return combinedDelay, offset

def divideIntoList(sqlfetch: dict):
    rto = []
    gt = []
    
    for i in range(len(sqlfetch)):
        rto.append(sqlfetch[i].get("RTO"))
        gt.append(sqlfetch[i].get("GT"))
    return rto, gt

def dict_to_list(sqlfetch: dict):
    combinedDelay = []
    for i in range(len(sqlfetch)):
        combinedDelay.append(sqlfetch[i].get("combinedDelay"))
    return combinedDelay

def accuracy_adjust(combinedDelay: list, rto: list, gt: list):
    combinedDelay_RTO = []
    combinedDelay_GT = []

    for i in range(len(combinedDelay)):
        combinedDelay_RTO.append(combinedDelay[i] - rto[i])
        combinedDelay_GT.append(combinedDelay[i] - gt[i])
        print("gt", combinedDelay[i], "-", gt[i])
        print("RTO",combinedDelay[i], "-", rto[i])

    
    return combinedDelay_RTO, combinedDelay_GT

def averageDelay(combinedDelay: list):
    sum: float
    for i in range (len(combinedDelay)):
        sum =+ combinedDelay[i]
    average = sum / len(combinedDelay)
    return average

def readping_syncInterval_3():
    with open("include/test/syncInterval_3/up0_ping.log", "r") as log:
        times1 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    with open("include/test/syncInterval_3/up1_ping.log", "r") as log:
        times2 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    with open("include/test/syncInterval_3/up3_ping.log", "r") as log:
        times3 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    
    return times1, times2, times3

def readping_syncInterval_15():
    with open("include/test/syncInterval_15/up0_ping.log", "r") as log:
        times1 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    with open("include/test/syncInterval_15/up1_ping.log", "r") as log:
        times2 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    with open("include/test/syncInterval_15/up3_ping.log", "r") as log:
        times3 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    
    return times1, times2, times3

def readping_syncInterval_30():
    with open("include/test/syncInterval_30/up0_ping.log", "r") as log:
        times1 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    with open("include/test/syncInterval_30/up1_ping.log", "r") as log:
        times2 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    with open("include/test/syncInterval_30/up3_ping.log", "r") as log:
        times3 = [float(line.split("time=")[1].split(" ms")[0]) for line in log]
    
    return times1, times2, times3

def addlist(list1: list, list2: list):
    list3 = []
    for i in range(len(list1)):
        list3.append(list1[i] + list2[i])

    for i in range(len(list3)):
        list3[i] = int(list3[i])/2

    return list3

def synchplot():

    up0_ping, up1_ping, up3_ping = readping_syncInterval_3()
    up0_ping_15, up1_ping_15, up3_ping_15 = readping_syncInterval_15()
    up0_ping_30, up1_ping_30, up3_ping_30 = readping_syncInterval_30()

    up1_up2_delay_ping = addlist(up1_ping, up0_ping)
    average_up1_up2_delay_ping = averageDelay(up1_up2_delay_ping)
    
    up3_up2_delay_ping = []

    for i in range(len(up3_ping)):
        up3_up2_delay_ping.append(up3_ping[i]/2)
    average_up3_up2_delay_ping = averageDelay(up3_up2_delay_ping)

    ####
    up1_up2_delay_ping_15 = addlist(up1_ping_15, up0_ping_15)
    average_up1_up2_delay_ping_15 = averageDelay(up1_up2_delay_ping_15)
    
    up3_up2_delay_ping_15 = []

    for i in range(len(up3_ping_15)):
        up3_up2_delay_ping_15.append(up3_ping_15[i]/2)
    average_up3_up2_delay_ping_15 = averageDelay(up3_up2_delay_ping_15)

    ####

    up1_up2_delay_ping_30 = addlist(up1_ping_30, up0_ping_30)
    average_up1_up2_delay_ping_30 = averageDelay(up1_up2_delay_ping_30)
    
    up3_up2_delay_ping_30 = []

    for i in range(len(up3_ping_30)):
        up3_up2_delay_ping_30.append(up3_ping_30[i]/2)
    average_up3_up2_delay_ping_30 = averageDelay(up3_up2_delay_ping_30)


    # 30, 15, 3
    ###################                     Synch interval 3 

    
    fileName_3 = "include/test/syncInterval_3/db.db3"
    sensor_up1_Delay_3, sensor_up1_offset_3 = getData(2, fileName_3)
    rto_3, gt_3 = divideIntoList(sensor_up1_offset_3)
    combinedDelay_3 = dict_to_list(sensor_up1_Delay_3)
    combinedDelay_RTO_3, combinedDelay_GT_3 = accuracy_adjust(combinedDelay_3, rto_3, gt_3)
    averageDelay_RTO_3 = averageDelay(combinedDelay_RTO_3)
    averageDelay_GT_3 = averageDelay(combinedDelay_GT_3)



    sensor_up2_Delay_3, sensor_up2_offset_3 = getData(4, fileName_3)
    sensor2_rto_3, sensor2_gt_3 = divideIntoList(sensor_up2_offset_3)
    sensor2_combinedDelay_3 = dict_to_list(sensor_up2_Delay_3)
    sensor2_combinedDelay_RTO_3, sensor2_combinedDelay_GT_3 = accuracy_adjust(sensor2_combinedDelay_3, sensor2_rto_3, sensor2_gt_3)
    sensor2_averageDelay_RTO_3 = averageDelay(sensor2_combinedDelay_RTO_3)
    sensor2_averageDelay_GT_3 = averageDelay(sensor2_combinedDelay_GT_3)

    #################3#                     Synch interval 15
    fileName_15 = "include/test/syncInterval_15/db.db3"

    Delay_15, offset_15 = getData(2, fileName_15)
    rto_15, gt_15 = divideIntoList(offset_15)
    combinedDelay_15 = dict_to_list(Delay_15)
    combinedDelay_RTO_15, combinedDelay_GT_15 = accuracy_adjust(combinedDelay_15, rto_15, gt_15)
    # print(combinedDelay_RTO_15)
    print(combinedDelay_GT_15)
    averageDelay_RTO_15 = averageDelay(combinedDelay_RTO_15)
    averageDelay_GT_15 = averageDelay(combinedDelay_GT_15)
    print("Average Delay GT", averageDelay_GT_15)
    print("Average Delay RTO",averageDelay_RTO_15)





    sensor_up2_Delay_15, sensor_up2_offset_15 = getData(4, fileName_15)
    sensor2_rto_15, sensor2_gt_15 = divideIntoList(sensor_up2_offset_15)
    sensor2_combinedDelay_15 = dict_to_list(sensor_up2_Delay_15)
    sensor2_combinedDelay_RTO_15, sensor2_combinedDelay_GT_15 = accuracy_adjust(sensor2_combinedDelay_15, sensor2_rto_15, sensor2_gt_15)
    sensor2_averageDelay_RTO_15 = averageDelay(sensor2_combinedDelay_RTO_15)
    sensor2_averageDelay_GT_15 = averageDelay(sensor2_combinedDelay_GT_15)

    print(sensor2_combinedDelay_RTO_15)
    print(sensor2_averageDelay_RTO_15)



    ######################                  Synch interval 30
    fileName_30 = "include/test/syncInterval_30/db.db3"


    Delay_30, offset_30= getData(2, fileName_30)
    rto_30, gt_30 = divideIntoList(offset_30)
    combinedDelay_30 = dict_to_list(Delay_30)
    combinedDelay_RTO_30, combinedDelay_GT_30 = accuracy_adjust(combinedDelay_30, rto_30, gt_30)
    averageDelay_RTO_30= averageDelay(combinedDelay_RTO_30)
    averageDelay_GT_30 = averageDelay(combinedDelay_GT_30)



    sensor_up2_Delay_30, sensor_up2_offset_30 = getData(4, fileName_30)
    sensor2_rto_30, sensor2_gt_30 = divideIntoList(sensor_up2_offset_30)
    sensor2_combinedDelay_30 = dict_to_list(sensor_up2_Delay_30)
    sensor2_combinedDelay_RTO_30, sensor2_combinedDelay_GT_30 = accuracy_adjust(sensor2_combinedDelay_30, sensor2_rto_30, sensor2_gt_30)
    sensor2_averageDelay_RTO_30 = averageDelay(sensor2_combinedDelay_RTO_30)
    sensor2_averageDelay_GT_30 = averageDelay(sensor2_combinedDelay_GT_30)


    averageDelay_RTO = [averageDelay_RTO_3, averageDelay_RTO_15, averageDelay_RTO_30]
    averageDelay_GT = [averageDelay_GT_3, averageDelay_GT_15, averageDelay_GT_30]
    averageDelay_ping_up0_up2 = [average_up1_up2_delay_ping, average_up1_up2_delay_ping_15, average_up1_up2_delay_ping_30]

    sensor2_averageDelay_RTO = [sensor2_averageDelay_RTO_3, sensor2_averageDelay_RTO_15, sensor2_averageDelay_RTO_30]
    sensor2_averageDelay_GT = [sensor2_averageDelay_GT_3, sensor2_averageDelay_GT_15, sensor2_averageDelay_GT_30]
    averageDelay_ping_up3_up2 = [average_up3_up2_delay_ping, average_up3_up2_delay_ping_15, average_up3_up2_delay_ping_30]

    for i in range(len(averageDelay_GT)):
        averageDelay_RTO[i] = averageDelay_RTO[i]*1000
        averageDelay_GT[i] = averageDelay_GT[i]*1000
        sensor2_averageDelay_RTO[i] = sensor2_averageDelay_RTO[i] * 1000
        sensor2_averageDelay_GT[i] = sensor2_averageDelay_GT[i] * 1000

    print("Sensor2 - Average Delay Ping",averageDelay_ping_up3_up2)
    print("Sensor1 - Average Delay Ping",averageDelay_ping_up0_up2)
    print("Sensor2 - Average Delay GT",sensor2_averageDelay_GT)
    print("Sensor2 - Average Delay RTO",sensor2_averageDelay_RTO)   
    x = [3, 15, 30]

    fig, sync = plt.subplots()

    fig.suptitle("Sensor:1Average delay for different synch intervals")
    sync.plot(x, averageDelay_GT, "r", label="Sensor1: AverageDelay of GT", marker="o" , linestyle=':')
    sync.plot(x, averageDelay_RTO, "b", label="sensor1: AverageDelay of RTO",marker="o", linestyle='dotted')
    sync.plot(x, averageDelay_ping_up0_up2, "g", label="sensor1: AverageDelay of Ping", marker="o",linestyle=':')
    sync.set_xlabel("synchronization interval")
    sync.set_ylabel("Average Delay")
    # sync.plot(x,sensor2_averageDelay_GT, "g", label="sensor2: AverageDelay of GT")
    # sync.plot(x,sensor2_averageDelay_RTO, "y", label="sensor2: AverageDelay of RTO")
    sync.legend(loc="best")
    fig.savefig("include/test/syncInterval_3/AverageDelay_syncInterval_sensor1")

    fig2, sync2 = plt.subplots()
    fig2.suptitle("Sensor2: Average delay for different synch intervals")
    sync2.plot(x,sensor2_averageDelay_GT, "g", label="sensor2: AverageDelay of GT",  marker="o",linestyle=':')
    sync2.plot(x,sensor2_averageDelay_RTO, "y", label="sensor2: AverageDelay of RTO",  marker="o",linestyle=':')
    sync2.plot(x, averageDelay_ping_up3_up2, "b", label="sensor2: AverageDelay of Ping",  marker="o",linestyle=':')
    sync2.legend(loc="best")
    sync2.set_xlabel("synchronization interval")
    sync2.set_ylabel("Average Delay")
    fig2.savefig("include/test/syncInterval_3/AverageDelay_syncInterval_sensor2")

    plt.show()

synchplot()



