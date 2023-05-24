from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

filename = "include/test/s1h2w/db.db3"

def getData(fileName = filename):
    db = Database(fileName)

    headend1Param = {
        'select':'HeadendTransfer.RTO, HeadendTransfer.GT, HeadendTransfer.rxTime, HeadendTransfer.nodeId',
        'where': {'nodeId': 1},
        }
    Headend2Param = {
         'select':'HeadendTransfer.RTO, HeadendTransfer.GT, HeadendTransfer.rxTime, HeadendTransfer.nodeId',
         'where': {'nodeId': 2},
        }
    backendParam = {
         'select': 'PayloadTransfer.deliveryTime',
        }
    sensorParam = {
        'select':'HeadendTransfer.RTO, HeadendTransfer.GT, HeadendTransfer.rxTime, HeadendTransfer.nodeId',
        'where' : {'nodeId': 4},
    }

    node1fetch = db.fetch("HeadendTransfer", headend1Param)
    node2fetch = db.fetch("HeadendTransfer", Headend2Param)
    backendfetch = db.fetch("PayloadTransfer", backendParam)
    up3fetch = db.fetch('HeadendTransfer', sensorParam)

    return node1fetch, node2fetch, backendfetch, up3fetch



def divideIntoList(sqlfetch: dict):
    RTO = []
    GT = []
    rxTime = []

    for i in range(len(sqlfetch)):
        RTO.append(sqlfetch[i].get("RTO"))
        GT.append(sqlfetch[i].get("GT"))
        rxTime.append(sqlfetch[i].get("rxTime"))
    return RTO, GT, rxTime

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
    Headend1, Headend2, Backend, Sensor = getData()
    
    Headend1_rto, Headend1_gt, Headend1_rxTime = divideIntoList(Headend1)
    Headend2_rto, Headend2_gt, Headend2_rxTime = divideIntoList(Headend2)
    Sensor_rto, Sensor_gt, Sensor_rxTime = divideIntoList(Sensor)
    Backend_delivery = dict_to_list(Backend)

    Sensor2Headend_AccuracyRTO, Sensor2Headend_AccuracyGT = measureAccuracy(Sensor_rto, Sensor_gt, Sensor_rxTime, Headend2_rto, Headend2_gt, Headend2_rxTime)

    Sensor2Backend_AccuracyRTO, Sensor2Backend_AccuracyGT = measureAccuracyH2B(Sensor_rto, Sensor_gt, Sensor_rxTime, Backend_delivery)

    Headend2Headend_AccuracyRTO, Headend2Headend_AccuracyGT = measureAccuracy(Headend2_rto, Headend2_gt, Headend2_rxTime, Headend1_rto, Headend1_gt, Headend1_rxTime)
    Headend2Backend_AccuracyRTO, Headend2Backend_AccuracyGT = measureAccuracyH2B(Headend1_rto, Headend1_gt, Headend1_rxTime, Backend_delivery)

    S2B_Error = measureErrorInAccuracy(Sensor2Backend_AccuracyRTO, Sensor2Backend_AccuracyGT)

    S2H_Error = measureErrorInAccuracy(Sensor2Headend_AccuracyRTO, Sensor2Headend_AccuracyGT)
    H2H_Error = measureErrorInAccuracy(Headend2Headend_AccuracyRTO, Headend2Headend_AccuracyGT)
    H2B_Error = measureErrorInAccuracy(Headend2Backend_AccuracyRTO, Headend2Backend_AccuracyGT)

    x = np.linspace(1, 4631, 4631)
    ###################     PLOTS over ACCURACY BETWEEN SENSOR(UP3) AND HEADEND1(UP1) 
    fig, S2H = plt.subplots()
    S2H.set_title("Accuracy between Sensor(up3) and Headend(up1)")
    S2H.plot(x, Sensor2Headend_AccuracyRTO, "-b", label="Reference Time Offset")
    S2H.plot(x, Sensor2Headend_AccuracyGT, "-r", label="Ground Truth")
    S2H.legend(loc="best")
    S2H.set_xlabel("Packet Transfer")
    S2H.set_ylabel("Offset values")
    fig.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Accuracy_S2H.png")
    

    fig2, H2H = plt.subplots()
    H2H.set_title("Accuracy between Headend(up1) and Headend(up0)")
    H2H.plot(x, Headend2Headend_AccuracyRTO, "-b", label="Reference Time Offset")
    H2H.plot(x, Headend2Headend_AccuracyGT, "-r", label="Ground Truth")
    H2H.legend(loc="best")
    H2H.set_xlabel("Packet Transfer")
    H2H.set_ylabel("Offset values")
    fig2.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Accuracy_H2H.png")
   

    fig3, H2B = plt.subplots()
    H2B.set_title("Accuracy between Headend(up0) and Backend(up2)")
    H2B.plot(x, Headend2Backend_AccuracyRTO, "-b", label="Reference Time Offset")
    H2B.plot(x, Headend2Backend_AccuracyGT, "-r", label="Ground Truth")
    H2B.legend(loc="best")
    H2B.set_xlabel("Packet Transfer")
    H2B.set_ylabel("Offset values")
    fig3.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Accuracy_H2B.png")

    fig10, S2B = plt.subplots()

    S2B.set_title("Accuracy between Sensor(up3) and Backend(up2)")
    S2B.plot(x, Sensor2Backend_AccuracyRTO, "-b", label="Reference Time Offset")
    S2B.plot(x, Sensor2Backend_AccuracyGT, "-r", label="Ground Truth")
    S2B.legend(loc="best")
    S2B.set_xlabel("Packet Transfer")
    S2B.set_ylabel("Offset values")
    fig10.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Accuracy_S2B.png")
   

    ############ ERROR PLOTS

    fig4, errorS2H = plt.subplots()
    errorS2H.set_title("Error in accuracy estimation For Sensor(up3) to Headend(up1)")
    errorS2H.plot(x,S2H_Error,"-g", label="Error Estimation of the accuracy")
    errorS2H.legend(loc="best")
    errorS2H.set_xlabel("Packet Transfer")
    errorS2H.set_ylabel("Difference Between RTO and GT Offsets")
    fig4.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/ErrorEstimation_S2H.png")

    fig5, errorH2H = plt.subplots()
    errorH2H.set_title("Error in accuracy estimation For Headend(up1) To Headend (up0)")
    errorH2H.plot(x,H2H_Error,"-g", label="Error Estimation of the accuracy")
    errorH2H.legend(loc="best")
    errorH2H.set_xlabel("Packet Transfer")
    errorH2H.set_ylabel("Difference Between RTO and GT Offsets")
    fig5.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/ErrorEstimation_H2H.png")

    fig6, errorH2B = plt.subplots()
    errorH2B.set_title("Error in accuracy estimation For Headend(up0) to Backend(up2)")
    errorH2B.plot(x,H2B_Error,"-g", label="Error Estimation of the accuracy")
    errorH2B.legend(loc="best")
    errorH2B.set_xlabel("Packet Transfer")
    errorH2B.set_ylabel("Difference Between RTO and GT Offsets")
    fig6.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/ErrorEstimation_H2B.png")

    fig11, errorS2B = plt.subplots()
    errorS2B.set_title("Error in accuracy estimation For Sensor(up3) to Backend(up2)")
    errorS2B.plot(x,S2B_Error,"-g", label="Error Estimation of the accuracy")
    errorS2B.legend(loc="best")
    errorS2B.set_xlabel("Packet Transfer")
    errorS2B.set_ylabel("Difference Between RTO and GT Offsets")
    fig6.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/ErrorEstimation_S2B.png")

    ############ ERROR HISTOGRAMS:

    counts, bins = np.histogram(S2H_Error)
    counts2, bins2 = np.histogram(H2H_Error)
    counts3, bins3 = np.histogram(H2B_Error)
    counts4, bins4 = np.histogram(S2B_Error)

    fig7, S2H_error_hist = plt.subplots()
    S2H_error_hist.stairs(counts, bins)
    S2H_error_hist.hist(bins[:-1], bins, weights=counts, label="Histogram over Error estimation of accuracy: Sensor to headend")
    S2H_error_hist.legend(loc="best")
    S2H_error_hist.set_xlabel("Difference Between RTO and GT Offsets")
    S2H_error_hist.set_ylabel("Number of packets")
    fig7.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Histogram_Error_estimation_S2H.png")
    

    fig8, H2H_error_hist = plt.subplots()
    H2H_error_hist.stairs(counts2, bins2)
    H2H_error_hist.hist(bins2[:-1], bins2, weights=counts2, label="Histogram over Error estimation of accuracy: Headend to headend")
    H2H_error_hist.legend(loc="best")
    H2H_error_hist.set_xlabel("Difference Between RTO and GT Offsets")
    H2H_error_hist.set_ylabel("Number of packets")
    fig8.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Histogram_Error_estimation_H2H.png")

    fig9, H2B_error_hist = plt.subplots()
    H2B_error_hist.stairs(counts3, bins3)
    H2B_error_hist.hist(bins3[:-1], bins3, weights=counts3, label="Histogram over Error estimation of accuracy: Headend to Backend")
    H2B_error_hist.legend(loc="best")
    H2B_error_hist.set_xlabel("Difference Between RTO and GT Offsets")
    H2B_error_hist.set_ylabel("Number of packets")
    fig9.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Histogram_Error_estimation_H2B.png")

    fig11, S2B_error_hist = plt.subplots()
    S2B_error_hist.stairs(counts4, bins4)
    S2B_error_hist.hist(bins4[:-1], bins4, weights=counts4, label="Histogram over Error estimation of accuracy: Sensor to Backend")
    S2B_error_hist.legend(loc="best")
    S2B_error_hist.set_xlabel("Difference Between RTO and GT Offsets")
    S2B_error_hist.set_ylabel("Number of packets")
    fig11.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h2w/Histogram_Error_estimation_S2B.png")

    plt.show()
   
run()


