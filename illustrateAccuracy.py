from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def getData(fileName = "include/test/s1h1s1w/db.db3"):
    db = Database(fileName)
    backend_headend_Param = {
         'select': 'PayloadTransfer.deliveryTime',
         'where': {'sensorid' : 1}
    }

    backend_sensor1_Param = {
         'select': 'PayloadTransfer.deliveryTime',
         'where': {'sensorId' : 2}
    }

    backend_sensor2_Param = {
         'select': 'PayloadTransfer.deliveryTime',
         'where': {'sensorId' : 4}
    
    }
    HeadendParam = {
        'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
        'where': {'nodeId': 1},
    }
    Sensor1Param = {
         'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
         'where': {'nodeId': 2},
    }
    Sensor2Param = {
         'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
         'where': {'nodeId': 4},
    }

    up0 = db.fetch("TransferJump", HeadendParam)
    up1 = db.fetch("TransferJump", Sensor1Param)
    up3 = db.fetch("TransferJump", Sensor2Param)
    up2_from_up0 = db.fetch("PayloadTransfer", backend_headend_Param)
    up2_from_up1 = db.fetch("PayloadTransfer", backend_sensor1_Param)
    up2_from_up3 = db.fetch("PayloadTransfer", backend_sensor2_Param)
    return up0, up1, up3, up2_from_up0, up2_from_up1, up2_from_up3 

def getData_s1h2w(fileName = "include/test/s1h2w/db.db3"):
    db = Database()

    headend2Param = {
        'select':'HeadendTransfer.rxTime, HeadendTransfer.RTO, HeadendTransfer.GT',
        'where': {'nodeid': 1}
    }
    headend1Param = {
        'select':'HeadendTransfer.rxTime, HeadendTransfer.RTO, HeadendTransfer.GT',
        'where': {'nodeid': 2}
    }
    sensorparam = {
        'select':'HeadendTransfer.rxTime, HeadendTransfer.RTO, HeadendTransfer.GT',
        'where': {'nodeid':4}
    }
    backendparam = {
        'select':'PayloadTransfer.deliveryTime'
    }
    up0 = db.fetch('HeadendTransfer', headend2Param)

def divideIntoList(sqlfetch: dict):
    rto = []
    gt = []
    rxTime = []

    for i in range(len(sqlfetch)):
        rto.append(sqlfetch[i].get("RTO"))
        gt.append(sqlfetch[i].get("GT"))
        rxTime.append(sqlfetch[i].get("startTime"))
    return rto, gt, rxTime


def dict_to_list(sqlfetch: dict):
    deliveryTime = []
    for i in range(len(sqlfetch)):
        deliveryTime.append(sqlfetch[i].get("deliveryTime"))
    return deliveryTime

def measure_ObservedTime(n1RTO: list, n1GT: list):
    observedTime = []

    for i in range(len(n1RTO)):
        observedTime.append(n1RTO[i] - n1GT[i])
    return observedTime



def run():

    up0, up1, up3, up2_from_up0, up2_from_up1, up2_from_up3 = getData()

    up0_rto, up0_gt, up0_startTime = divideIntoList(up0)
    up1_rto, up1_gt, up1_startTime = divideIntoList(up1)
    up3_rto, up3_gt, up3_startTime = divideIntoList(up3)
    up2_up0_deliverytime = dict_to_list(up2_from_up1)
    up2_up1_deliverytime = dict_to_list(up2_from_up1)
    up2_up3_deliverytime = dict_to_list(up2_from_up3)

    up0_observedTime = measure_ObservedTime(up0_rto, up0_gt)
    up1_observedTime = measure_ObservedTime(up1_rto, up1_gt)
    up3_observedTime = measure_ObservedTime(up3_rto, up3_gt)
    up1_vkt = up1_gt
    up0_vkt = up0_gt

    firstTime = up2_up1_deliverytime[0]
    # startTime = time.time()

    for i in range(len(up2_from_up1)):
        up2_up1_deliverytime[i] = up2_up1_deliverytime[i] - firstTime
        up1_vkt[i] = abs(up1_vkt[i]) - 13.3
        up0_vkt[i] = abs(up0_vkt[i]) - 13.3
        up0_observedTime[i] = abs(up0_observedTime[i])
        up1_observedTime[i] = abs(up1_observedTime[i])
        
    
    fig, acc = plt.subplots()
    acc.plot(up2_up1_deliverytime, up1_vkt, "b", label="UP1: Non Adjusted VKC")
    acc.plot(up2_up1_deliverytime, up1_observedTime, "r", label="UP1:Accuracy Adjusted VKC")

    acc.plot(up2_up1_deliverytime, up0_vkt, label="UP0: Non Adjusted VKC")
    acc.plot(up2_up1_deliverytime, up0_observedTime, label="UP0: Accuracy Adjusted VKC")
    
    # acc.plot(up2_up3_deliverytime, up3_observedTime, label="UP3: RTO - GT")
    # acc.plot(up2_up3_deliverytime, up3_gt, label="UP3: VKT")

    acc.legend(loc="upper left")
    acc.set_xlabel("Actual Time/ seconds")
    acc.set_ylabel("Observed Time Inaccuracy")
    fig.suptitle("Accuracy of the VKC on different nodes")

    fig.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h1s1w/IllustrationOfAccuracy.png")

    plt.show()

run()
