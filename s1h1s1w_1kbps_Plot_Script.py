from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

filename = "include/test/s1h1s1w/db.db3"

def getData(fileName = filename):
    db = Database(fileName)

    headendParam = {
        'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
        'where': {'nodeId': 1},
        }
    sensor1Param = {
         'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
         'where': {'nodeId': 2},
        }
    backend_from_sensor1Param = {
         'select': 'PayloadTransfer.deliveryTime',
         'where' : {'sensorId' : 2}
        }
    sensor2Param = {
        'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
        'where' : {'nodeId': 4},
    }
    backend_from_sensor2Param = {
         'select': 'PayloadTransfer.deliveryTime',
         'where' : {'sensorId' : 4}
        }

    node1fetch = db.fetch("TransferJump", headendParam)
    node2fetch = db.fetch("TransferJump", sensor1Param)
    backend_node2_fetch = db.fetch("PayloadTransfer", backend_from_sensor1Param)
    up3fetch = db.fetch('TransferJump', sensor2Param)
    backend_node3_fetch = db.fetch("PayloadTransfer", backend_from_sensor2Param)
    return node1fetch, node2fetch, up3fetch, backend_node2_fetch, backend_node3_fetch



def divideIntoList(sqlfetch: dict):
    RTO = []
    GT = []
    startTime = []

    for i in range(len(sqlfetch)):
        RTO.append(sqlfetch[i].get("RTO"))
        GT.append(sqlfetch[i].get("GT"))
        startTime.append(sqlfetch[i].get("startTime"))
    return RTO, GT, startTime

def measureAccuracy(n1RTO: list, n1GT:list, n1rxTime:list, n2RTO:list, n2GT: list, n2rxTime:list):
    n1EstimatedRxTimeRTO = []
    n1EstimatedRxTimeGT = []
    n2EstimatedRxTimeRTO = []
    n2EstimatedRxTimeGT = []

    delay = []
    EstimatedDelayRTO = []
    EstimatedDelayGT = []

    AccuracyRTO = []
    AccuracyGT = []

    for i in range(len(n1RTO)):
        n1EstimatedRxTimeRTO.append(n1rxTime[i] + n1RTO[i])
        n1EstimatedRxTimeGT.append(n1rxTime[i] + n1GT[i])

        n2EstimatedRxTimeRTO.append(n2rxTime[i] + n2RTO[i])
        n2EstimatedRxTimeGT.append(n2rxTime[i] + n2GT[i])
    
    for i in range(len(n1RTO)):
        delay.append(n2rxTime[i] - n1rxTime[i])
        EstimatedDelayRTO.append(n2EstimatedRxTimeRTO[i]- n1EstimatedRxTimeRTO[i])
        EstimatedDelayGT.append(n2EstimatedRxTimeGT[i] - n1EstimatedRxTimeGT[i])
    
    for i in range(len(n1RTO)):
        AccuracyRTO.append(delay[i] - EstimatedDelayRTO[i])
        AccuracyGT.append(delay[i] - EstimatedDelayGT[i])
    return AccuracyRTO, AccuracyGT

def dict_to_list(sqlfetch: dict):
    deliveryTime = []
    for i in range(len(sqlfetch)):
        deliveryTime.append(sqlfetch[i].get("deliveryTime"))
    return deliveryTime

def measureErrorInAccuracy(AccuracyRTO: list, AccuracyGT: list):
    ErrorAccuracy = []
    for i in range(len(AccuracyRTO)):
        ErrorAccuracy.append(AccuracyRTO[i] - AccuracyGT[i])
    return ErrorAccuracy

def measureAccuracyH2B(n1RTO: list, n1GT:list, n1rxTime:list, n2rxTime:list):
    n1EstimatedRxTimeRTO = []
    n1EstimatedRxTimeGT = []
    delay = []
    EstimatedDelayRTO = []
    EstimatedDelayGT = []

    AccuracyRTO = []
    AccuracyGT = []

    for i in range(len(n1RTO)):
        n1EstimatedRxTimeRTO.append(n1rxTime[i] + n1RTO[i])
        n1EstimatedRxTimeGT.append(n1rxTime[i] + n1GT[i])
    
    for i in range(len(n1RTO)):
        delay.append(n2rxTime[i] - n1rxTime[i])
        EstimatedDelayRTO.append(n2rxTime[i] - n1EstimatedRxTimeRTO[i])
        EstimatedDelayGT.append(n2rxTime[i] - n1EstimatedRxTimeGT[i])

    for i in range(len(EstimatedDelayRTO)):
        AccuracyRTO.append(delay[i] - EstimatedDelayRTO[i])
        AccuracyGT.append(delay[i] - EstimatedDelayGT[i])
    return AccuracyRTO, AccuracyGT


def run():
    headend, sensor1, sensor2, backend_sensor1, backend_sensor2 = getData()

    rto_headend, gt_headend, startTime_headend = divideIntoList(headend)
    rto_sensor1, gt_sensor1, startTime_sensor1 = divideIntoList(sensor1)
    rto_sensor2, gt_sensor2, startTime_sensor2 = divideIntoList(sensor2)
    deliveryTime_sensor1 = dict_to_list(backend_sensor1)
    deliveryTime_sensor2 = dict_to_list(backend_sensor2)

    Accuracy_RTO_sensor1, Accuracy_GT_sensor1 = measureAccuracyH2B(rto_sensor1, gt_sensor1, startTime_sensor1, deliveryTime_sensor1)
    Accuracy_RTO_sensor2, Accuracy_GT_sensor2 = measureAccuracyH2B(rto_sensor2, gt_sensor2, startTime_sensor2, deliveryTime_sensor2)

    Error_sensor1 = measureErrorInAccuracy(Accuracy_RTO_sensor1, Accuracy_GT_sensor1)
    Error_sensor2 = measureErrorInAccuracy(Accuracy_RTO_sensor2, Accuracy_GT_sensor2)

    x1 = np.linspace(1, len(Accuracy_GT_sensor1), len(Accuracy_GT_sensor1))
    x2 = np.linspace(1, len(Accuracy_GT_sensor2), len(Accuracy_GT_sensor2))
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.plot(x1, Accuracy_RTO_sensor1, "r", label="sensor1:Accuracy RTO")
    ax.plot(x1, Accuracy_GT_sensor1, "b", label="sensor1: Accuracy GT")
    ax2.plot(x2, Accuracy_RTO_sensor2, "y", label="Sensor2: Accuracy RTO")
    ax2.plot(x2, Accuracy_GT_sensor2, "g", label="Sensor2: Accuracy GT")

    ax.legend(loc="best")
    ax2.legend(loc="best")

    plt.show()
   
run()


