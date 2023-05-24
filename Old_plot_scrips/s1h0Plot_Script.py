from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def getData(fileName = "include/test/s1w/db.db3", ):
    db = Database(fileName)
    params = { 
    'select': 'HeadendTransfer.RTO, HeadendTransfer.GT, PayloadTransfer.dataTime, PayloadTransfer.deliveryTime',
    'join':{
        'HeadendTransfer': 'PayloadToHeadend.jumpId=HeadendTransfer.id',
        'PayloadTransfer': 'PayloadToHeadend.payloadId=PayloadTransfer.id'
        },
    # 'limit': 100
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



    counts, bins = np.histogram(ErrorAccuracyMeasure)
    counts2, bins2 = np.histogram(AccuracyRTO)
    counts3, bins3 = np.histogram(AccuracyGT)
    
    x = np.linspace(1, 4630, 4630)

    ############### ACCURACY PLOTS
    fig, ax = plt.subplots()
    ax.set_title("Accuracy of the two synch techs")
    ax.plot(x, AccuracyRTO, "-b", label="Reference Time Offset")
    ax.plot(x, AccuracyGT, "-r", label="Ground Truth")
    ax.legend(loc="best")
    ax.set_xlabel("Packet Transfer")
    ax.set_ylabel("Offset values")
    fig.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1w/Accuracy_of_the_two_synch_techs.png")

    ############### ERROR PLOTS
    fig2, error = plt.subplots()
    error.set_title("Error in accuracy estimation")
    error.plot(x,ErrorAccuracyMeasure,"-g", label="Error Estimation of the accuracy")
    error.legend(loc="best")
    error.set_xlabel("Packet Transfer")
    error.set_ylabel("Difference Between RTO and GT Offsets")
    fig2.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1w/Error_in_accuracy_estimation.png")

    ############### ERROR HISTOGRAM PLOT
    fig3, Errorhist = plt.subplots()
    Errorhist.stairs(counts, bins)
    Errorhist.hist(bins[:-1], bins, weights=counts, label="Histogram over Error estimation of accuracy")
    Errorhist.legend(loc="best")
    Errorhist.set_xlabel("Difference Between RTO and GT Offsets")
    Errorhist.set_ylabel("Number of packets")
    fig3.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1w/Histogram_Error_estimation.png")

    ############### ACCURACY HISTOGRAM PLOTS
    fig4, AccuracyRTOhist=plt.subplots()
    fig5, AccuracyGThist=plt.subplots()

    
    AccuracyRTOhist.hist(bins2[:-1],bins2, weights=counts2, label="Histogram over Accuracy over RTO")
    AccuracyGThist.hist(bins3[:-1],bins3, weights=counts3, label="Histogram over Accuracy over GT")

 
    AccuracyRTOhist.legend(loc="lower left")
    AccuracyGThist.legend(loc="lower left")
    
    AccuracyGThist.set_xlabel("Offset values")
    AccuracyRTOhist.set_xlabel("Offset values")

    AccuracyGThist.set_ylabel("Number of packets")
    AccuracyRTOhist.set_ylabel("Number of packets")

    fig4.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1w/AccuracyRTOHistorgram.png")
    fig5.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1w/AccuracyGTHistorgram.png")
    

    plt.show()


run()