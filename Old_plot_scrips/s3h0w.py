from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def getData(fileName = "include/test/s3w/db.db3", ):
    db = Database(fileName)
    Sensor1Param = {
        'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
        'where': {'nodeId': 1},
    }
    Sensor2Param = {
        'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
        'where': {'nodeId': 2},
    }
    Sensor3Param = {
        'select':'TransferJump.RTO, TransferJump.GT, TransferJump.startTime, TransferJump.nodeId',
        'where': {'nodeId': 4},
    }

    backendParam = {
         'select': 'PayloadTransfer.deliveryTime',
    }
    node1fetch = db.fetch("TransferJump", Sensor1Param)
    node2fetch = db.fetch("TransferJump", Sensor2Param)
    node3fetch = db.fetch("TransferJump", Sensor3Param)
    backendfetch = db.fetch("PayloadTransfer", backendParam)

    return node1fetch, node2fetch, node3fetch, backendfetch

def divideIntoList(sqlfetch: dict):
    RTO = []
    GT = []
    rxTime = []

    for i in range(len(sqlfetch)):
        RTO.append(sqlfetch[i].get("RTO"))
        GT.append(sqlfetch[i].get("GT"))
        rxTime.append(sqlfetch[i].get("startTime"))
    return RTO, GT, rxTime


def dict_to_list(sqlfetch: dict):
    deliveryTime = []
    for i in range(len(sqlfetch)):
        deliveryTime.append(sqlfetch[i].get("deliveryTime"))
    return deliveryTime

def measureAccuracyS2B(n1RTO: list, n1GT:list, n1rxTime:list, n2rxTime:list):
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


def measureErrorInAccuracy(AccuracyRTO: list, AccuracyGT: list):
    ErrorAccuracy = []
    for i in range(len(AccuracyRTO)):
        ErrorAccuracy.append(AccuracyRTO[i] - AccuracyGT[i])
    return ErrorAccuracy

def run ():
    sensor1, sensor2, sensor3, backend = getData()

    sensor1_rto, sensor1_gt, sensor1_startTime = divideIntoList(sensor1)
    sensor2_rto, sensor2_gt, sensor2_startTime = divideIntoList(sensor2)
    sensor3_rto, sensor3_gt, sensor3_startTime = divideIntoList(sensor3)
    backend_delivery = dict_to_list(backend)

    sensor1ToBackend_accuracyRTO, sensor1ToBackend_accuracyGT = measureAccuracyS2B(sensor1_rto, sensor1_gt, sensor1_startTime, backend_delivery)
    sensor2ToBackend_accuracyRTO, sensor2ToBackend_accuracyGT = measureAccuracyS2B(sensor2_rto, sensor2_gt, sensor2_startTime, backend_delivery)
    sensor3ToBackend_accuracyRTO, sensor3ToBackend_accuracyGT = measureAccuracyS2B(sensor3_rto, sensor3_gt, sensor3_startTime, backend_delivery)

    S1_To_B_Error = measureErrorInAccuracy(sensor1ToBackend_accuracyRTO, sensor1ToBackend_accuracyGT)
    S2_To_B_Error = measureErrorInAccuracy(sensor2ToBackend_accuracyRTO, sensor2ToBackend_accuracyGT)
    S3_To_B_Error = measureErrorInAccuracy(sensor3ToBackend_accuracyRTO, sensor3ToBackend_accuracyGT)
    x = np.linspace(1, 4631, 4631)
    x2 = np.linspace(1,4638,4638)
    x3 = np.linspace(1,4633,4633)
    fig, S1ToB = plt.subplots()
    S1ToB.set_title("Accuracy between Sensor1(up0) and Backend(up2)")
    S1ToB.plot(x, sensor1ToBackend_accuracyRTO, "-b", label="Reference Time Offset")
    S1ToB.plot(x, sensor1ToBackend_accuracyGT, "-r", label="Ground Truth")
    S1ToB.legend(loc="best")
    S1ToB.set_xlabel("Packet Transfer")
    S1ToB.set_ylabel("Offset values")
    fig.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/Accuracy_Sensor1_To_Backend.png")


    fig2, S2ToB = plt.subplots()
    S2ToB.set_title("Accuracy between Sensor2(up1) and Backend(up2)")
    S2ToB.plot(x2, sensor2ToBackend_accuracyRTO, "-b", label="Reference Time Offset")
    S2ToB.plot(x2, sensor2ToBackend_accuracyGT, "-r", label="Ground Truth")
    S2ToB.legend(loc="best")
    S2ToB.set_xlabel("Packet Transfer")
    S2ToB.set_ylabel("Offset values")
    fig2.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/Accuracy_Sensor2_To_Backend.png")

    fig7, S3ToB = plt.subplots()
    S3ToB.set_title("Accuracy between Sensor3(up3) and Backend(up2)")
    S3ToB.plot(x3, sensor3ToBackend_accuracyRTO, "-b", label="Reference Time Offset")
    S3ToB.plot(x3, sensor3ToBackend_accuracyGT, "-r", label="Ground Truth")
    S3ToB.legend(loc="best")
    S3ToB.set_xlabel("Packet Transfer")
    S3ToB.set_ylabel("Offset values")
    fig7.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/Accuracy_Sensor3_To_Backend.png")


    fig3, errorS1ToB = plt.subplots()
    errorS1ToB.set_title("Error in accuracy estimation between Sensor1(up0) and Backend(up2)")
    errorS1ToB.plot(x, S1_To_B_Error, "-b", label="Error estimation of accuracy")
    errorS1ToB.legend(loc="best")
    errorS1ToB.set_xlabel("Packet Transfer")
    errorS1ToB.set_ylabel("Difference Between RTO and GT Offsets")
    fig3.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/ErrorInAccuracyEstimation_Sensor1_To_Backend.png")

    fig4, errorS2ToB = plt.subplots()
    errorS2ToB.set_title("Error in accuracy estimation between Sensor2(up1) and Backend(up2)")
    errorS2ToB.plot(x2, S2_To_B_Error, "-b", label="Error estimation of accuracy")
    errorS2ToB.legend(loc="best")
    errorS2ToB.set_xlabel("Packet Transfer")
    errorS2ToB.set_ylabel("Difference Between RTO and GT Offsets")
    fig4.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/ErrorInAccuracyEstimation_Sensor2_To_Backend.png")

    fig8, errorS3ToB = plt.subplots()
    errorS3ToB.set_title("Error in accuracy estimation between Sensor2(up3) and Backend(up2)")
    errorS3ToB.plot(x3, S3_To_B_Error, "-b", label="Error estimation of accuracy")
    errorS3ToB.legend(loc="best")
    errorS3ToB.set_xlabel("Packet Transfer")
    errorS3ToB.set_ylabel("Difference Between RTO and GT Offsets")
    fig8.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/ErrorInAccuracyEstimation_Sensor3_To_Backend.png")


    counts, bins = np.histogram(S1_To_B_Error)
    counts2, bins2 = np.histogram(S2_To_B_Error)
    counts3, bins3 = np.histogram(S3_To_B_Error)


    fig5, histogramError_S1_To_B = plt.subplots()
    histogramError_S1_To_B.stairs(counts, bins)
    histogramError_S1_To_B.hist(bins[:-1], bins, weights=counts, label="Histogram over Error estimation of accuracy: Sensor1 to Backend")
    histogramError_S1_To_B.legend(loc="best")
    histogramError_S1_To_B.set_xlabel("Difference Between RTO and GT Offsets")
    histogramError_S1_To_B.set_ylabel("Number of packets")
    fig5.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/Histogram_Error_estimation_Sensor1_To_Backend.png")

    fig6, histogramError_S2_To_B = plt.subplots()
    histogramError_S2_To_B.stairs(counts2, bins2)
    histogramError_S2_To_B.hist(bins2[:-1], bins2, weights=counts2, label="Histogram over Error estimation of accuracy: Sensor2 to Backend")
    histogramError_S2_To_B.legend(loc="best")
    histogramError_S2_To_B.set_xlabel("Difference Between RTO and GT Offsets")
    histogramError_S2_To_B.set_ylabel("Number of packets")
    fig6.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/Histogram_Error_estimation_Sensor2_To_Backend.png")

    fig9, histogramError_S3_To_B = plt.subplots()
    histogramError_S3_To_B.stairs(counts3, bins3)
    histogramError_S3_To_B.hist(bins3[:-1], bins3, weights=counts3, label="Histogram over Error estimation of accuracy: Sensor3 to Backend")
    histogramError_S3_To_B.legend(loc="best")
    histogramError_S3_To_B.set_xlabel("Difference Between RTO and GT Offsets")
    histogramError_S3_To_B.set_ylabel("Number of packets")
    fig9.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s3w/Histogram_Error_estimation_Sensor3_To_Backend.png")

    plt.show()


run()





