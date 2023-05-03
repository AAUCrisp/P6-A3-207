from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def getData(fileName = "include/db.db3", ):
    db = Database(fileName)
    params = { 
    'select': 'HeadendTransfer.RTO, HeadendTransfer.GT, PayloadTransfer.dataTime, PayloadTransfer.deliveryTime',
    'join':{
        'HeadendTransfer': 'PayloadToHeadend.jumpId=HeadendTransfer.id',
        'PayloadTransfer': 'PayloadToHeadend.payloadId=PayloadTransfer.id'
        },
    'limit': 100
    }

    return db.fetch("PayloadToHeadend", params)


def divideIntoList(sqlFetch: dict, key1 = "RTO", key2 = "GT", key3 = "dataTime", key4 = "deliveryTime"):
    rto = []
    gt = []
    dataTime = []
    deliveryTime = []

    for i in range(len(sqlFetch)):
        rto.append(sqlFetch[i].get(key1))
        gt.append(sqlFetch[i].get(key2))
        dataTime.append(sqlFetch[i].get(key3))
        deliveryTime.append(sqlFetch[i].get(key4))
    return rto, gt, dataTime, deliveryTime

def measureAccuracy(RTO: list, GT:list, dataTime: list, deliveryTime: list):
    estimatedDataTimeRTO = []
    estimatedDataTimeGT = []
    Delay = []
    EstimatedDelayRTO = []
    EstimatedDelayGT = []
    AccuracyRTO = []
    AccuracyGT = []

    for i in range(len(RTO)):
        estimatedDataTimeRTO.append(dataTime[i] + RTO[i])
        estimatedDataTimeGT.append(dataTime[i] + GT[i])
    
    for i in range (len(RTO)):
        Delay.append(deliveryTime[i] - dataTime[i])
        EstimatedDelayRTO.append(deliveryTime[i] - estimatedDataTimeRTO[i])
        EstimatedDelayGT.append(deliveryTime[i] - estimatedDataTimeGT[i])

    for i in range (len(Delay)):
        AccuracyRTO.append(Delay[i] - EstimatedDelayRTO[i])
        AccuracyGT.append(Delay[i] - EstimatedDelayGT[i])
    
    return AccuracyRTO, AccuracyGT

def measureAccuracyError(AccuracyRTO: list, AccuracyGT:list):
    ErrorAccuracy = []
    for i in range (len(AccuracyRTO)):
        ErrorAccuracy.append(AccuracyRTO[i] - AccuracyGT[i])
    return ErrorAccuracy


def run():
    sqlFetch = getData()

    RTO_list, GT_list, dataTime_list, deliverTime_list   = divideIntoList(sqlFetch=sqlFetch)

    AccuracyRTO, AccuracyGT = measureAccuracy(RTO_list, GT_list, dataTime_list, deliverTime_list)

    ErrorAccuracyMeasure = measureAccuracyError(AccuracyRTO, AccuracyGT)


    x = np.linspace(1, 317, 317)

    fig, ax = plt.subplots()
    fig2, error = plt.subplots()


    ax.plot(x, AccuracyRTO, "-b", label="Reference Time Offset")
    ax.plot(x, AccuracyGT, "-r", label="Ground Truth")
    ax.legend(loc="best")
    error.plot(x,ErrorAccuracyMeasure,"-g", label="Error Estimation of the accuracy")
    error.legend(loc="best")
    
    

    plt.show()


run()