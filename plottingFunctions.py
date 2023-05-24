from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

s1h1s1 = "include/test/s1h1s1w/db.db3" 
s1h2 = "include/test/s1h2w/db.db3"
s1 = "include/test/s1w/db.db3"
s2 = "include/test/s2w/db.db3"
s3 = "include/test/s3w/db.db3"
s1h1 = "include/test/data/s1h1w/db.db3"
up2 = "include/test/database.db3"



def getData_s1h1s1(fileName = s1h1s1):
    db = Database(fileName)
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
    up0 = db.fetch("TransferJump", HeadendParam)
    up1 = db.fetch("TransferJump", Sensor1Param)
    up3 = db.fetch("TransferJump", Sensor2Param)
    up2_from_up0 = db.fetch("PayloadTransfer", backend_headend_Param)
    up2_from_up1 = db.fetch("PayloadTransfer", backend_sensor1_Param)
    up2_from_up3 = db.fetch("PayloadTransfer", backend_sensor2_Param)
    return up1, up3, up2_from_up1, up2_from_up3 

def getData_s1h1 (fileName = s1h1):
    db = Database(fileName)
    sensorparam = {
        'select' : 'TransferJump.RTO, TransferJump.GT, TransferJump.startTime',
        'where': {'nodeid': 1}
    }
    backendparam = {
        'select' : 'PayloadTransfer.deliveryTime', 
        'where' : {'sensorId' : 1}
    }

    
    backend = db.fetch("PayloadTransfer", backendparam)
    sensor = db.fetch("TransferJump", sensorparam)

    return sensor, backend

def getData_s1h2(fileName = s1h2):
    db = Database(fileName)
    sensorparam = {
        'select' : 'HeadendTransfer.RTO, HeadendTransfer.GT, HeadendTransfer.rxTime',
        'where': {'nodeid': 4}
    }
    backendparam = {
        'select' : 'PayloadTransfer.deliveryTime', 
        'where' : {'sensorId' : 4}
    }
    
    backend = db.fetch("PayloadTransfer", backendparam)
    sensor = db.fetch("HeadendTransfer", sensorparam)

    return sensor, backend

def getData_s1(fileName = s1):
    db = Database(fileName)
    sensorparam = {
        'select' : 'HeadendTransfer.RTO, HeadendTransfer.GT, HeadendTransfer.rxTime'
    }
    backendparam = {
        'select' : 'PayloadTransfer.deliveryTime'
    }

    backend = db.fetch("PayloadTransfer", backendparam)
    sensor = db.fetch("HeadendTransfer", sensorparam)

    return sensor, backend

def getData_s2(fileName = s2):
    db = Database(fileName)
    sensor1param = {
        'select' : 'TransferJump.RTO, TransferJump.GT, TransferJump.startTime',
        'where' : {'nodeId ': 1}
    }
    sensor2param = {
        'select' : 'TransferJump.RTO, TransferJump.GT, TransferJump.startTime',
        'where' : {'nodeId ': 2}
    }
    
    backend_s1param = {
        'select' : 'PayloadTransfer.deliveryTime',
        'where' : {'SensorId' : 1}
    }

    backend_s2param = {
        'select' : 'PayloadTransfer.deliveryTime',
        'where' : {'SensorId' : 2}
    }



    backend_s1 = db.fetch("PayloadTransfer", backend_s1param)
    backend_s2 = db.fetch("PayloadTransfer", backend_s2param)
    sensor1 = db.fetch("TransferJump", sensor1param)
    sensor2 = db.fetch("TransferJump", sensor2param)

    return sensor1, sensor2, backend_s1, backend_s2


def getData_s3(fileName = s3):
    db = Database(fileName)
    sensor1param = {
        'select' : 'TransferJump.RTO, TransferJump.GT, TransferJump.startTime',
        'where' : {'nodeId ': 1}
    }
    sensor2param = {
        'select' : 'TransferJump.RTO, TransferJump.GT, TransferJump.startTime',
        'where' : {'nodeId ': 2}
    }
    sensor3param = {
        'select' : 'TransferJump.RTO, TransferJump.GT, TransferJump.startTime',
        'where' : {'nodeId ': 4}
    }

    backend_s1param = {
        'select' : 'PayloadTransfer.deliveryTime',
        'where' : {'SensorId' : 1}
    }

    backend_s2param = {
        'select' : 'PayloadTransfer.deliveryTime',
        'where' : {'SensorId' : 2}
    }
    backend_s3param = {
        'select' : 'PayloadTransfer.deliveryTime',
        'where' : {'SensorId' : 4}
    }



    backend_s1 = db.fetch("PayloadTransfer", backend_s1param)
    backend_s2 = db.fetch("PayloadTransfer", backend_s2param)
    backend_s3 = db.fetch("PayloadTransfer", backend_s3param)
    sensor1 = db.fetch("TransferJump", sensor1param)
    sensor2 = db.fetch("TransferJump", sensor2param)
    sensor3 = db.fetch("TransferJump", sensor3param)
    return sensor1, sensor2, sensor3, backend_s1, backend_s2, backend_s3

def getData_up2_to_up2(filename = up2):
    db = Database(filename)
    ground_truth = {
        'select' : 'TransferJump.GT, TransferJump.RTO'
    }
    gt = db.fetch("TransferJump", ground_truth)

    return gt




def divideIntoList(sqlfetch: dict):
    rto = []
    gt = []
    rxTime = []

    for i in range(len(sqlfetch)):
        rto.append(sqlfetch[i].get("RTO"))
        gt.append(sqlfetch[i].get("GT"))
        rxTime.append(sqlfetch[i].get("startTime"))
    return rto, gt, rxTime

def divideIntoList_old(sqlfetch: dict):
    rto = []
    gt = []
    rxTime = []

    for i in range(len(sqlfetch)):
        rto.append(sqlfetch[i].get("RTO"))
        gt.append(sqlfetch[i].get("GT"))
        rxTime.append(sqlfetch[i].get("rxTime"))
    return rto, gt, rxTime

def dict_to_list(sqlfetch: dict):
    deliveryTime = []
    for i in range(len(sqlfetch)):
        deliveryTime.append(sqlfetch[i].get("deliveryTime"))
    return deliveryTime

def dict_to_list_gt(sqlfetch: dict):
    deliveryTime = []
    random = []
    for i in range(len(sqlfetch)):
        deliveryTime.append(sqlfetch[i].get("GT"))
        random.append(sqlfetch[i].get("RTO"))
    return deliveryTime, random


def measureDelay_upX_2_N(n1RTO: list, n1GT:list, n1rxTime:list, n2rxTime:list):
    n1EstimatedRxTimeRTO = []
    n1EstimatedRxTimeGT = []
    delay = []
    EstimatedDelayRTO = []
    EstimatedDelayGT = []

    for i in range(len(n1RTO)):
        n1EstimatedRxTimeRTO.append(n1rxTime[i] + n1RTO[i])
        n1EstimatedRxTimeGT.append(n1rxTime[i] + n1GT[i])
    
    for i in range(len(n1RTO)):
        delay.append(n2rxTime[i] - n1rxTime[i])
        EstimatedDelayRTO.append(n2rxTime[i] - n1EstimatedRxTimeRTO[i])
        EstimatedDelayGT.append(n2rxTime[i] - n1EstimatedRxTimeGT[i])
    
    return delay, EstimatedDelayRTO, EstimatedDelayGT

def measureAccuracy_upX_2_B(n1RTO: list, n1GT:list, n1rxTime:list, n2rxTime:list):
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



