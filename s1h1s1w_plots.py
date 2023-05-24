from include.Database import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def getData(fileName = "include/test/s1h1s1w/db.db3"):
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
    return up0, up1, up3, up2_from_up0, up2_from_up1, up2_from_up3 

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
        delay.append(abs(n2rxTime[i] - n1rxTime[i]))
        # delay.append(n2rxTime[i] - n1rxTime[i])
        print(delay[i])
        # print("lenght of n2Rxtime array and RTO", len(n2rxTime), len(n1RTO) )
        # print(n2rxTime[i], "-", n1rxTime[i])
        # EstimatedDelayRTO.append(n2rxTime[i] - n1EstimatedRxTimeRTO[i])
        EstimatedDelayRTO.append(abs(n2rxTime[i] - n1EstimatedRxTimeRTO[i]))
        # print(n2rxTime[i], "-" ,n1EstimatedRxTimeRTO[i])
        # EstimatedDelayGT.append(n2rxTime[i] - n1EstimatedRxTimeGT[i])
        EstimatedDelayGT.append(abs(n2rxTime[i] - n1EstimatedRxTimeGT[i]))
    
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
        n1EstimatedRxTimeRTO.append(n1rxTime[i] - n1RTO[i])
        n1EstimatedRxTimeGT.append(n1rxTime[i] - n1GT[i])
    
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


def run():
    # up0, up1, up3, up2_from_up0, up2_from_up1, up2_from_up3 = getData()

    # up0_rto, up0_gt, up0_startTime = divideIntoList(up0)
    # up1_rto, up1_gt, up1_startTime = divideIntoList(up1)
    # up3_rto, up3_gt, up3_startTime = divideIntoList(up3)
    # up2_up0_deliverytime = dict_to_list(up2_from_up0)
    # up2_up1_deliverytime = dict_to_list(up2_from_up1)
    # up2_up3_deliverytime = dict_to_list(up2_from_up3)


    # up0_AccuracyRTO, up0_AccuracyGT = measureAccuracy_upX_2_B(up0_rto, up0_gt, up0_startTime, up2_up1_deliverytime)
    # up1_AccuracyRTO, up1_AccuracyGT = measureAccuracy_upX_2_B(up1_rto, up1_gt, up1_startTime, up2_up1_deliverytime)
    # up3_AccuracyRTO, up3_AccuracyGT = measureAccuracy_upX_2_B(up3_rto, up3_gt, up3_startTime, up2_up3_deliverytime)

    # up0_ErrorInAccuracy = measureErrorInAccuracy(up0_AccuracyRTO, up0_AccuracyGT)
    # up1_ErrorInAccuracy = measureErrorInAccuracy(up1_AccuracyRTO, up1_AccuracyGT)
    # up3_ErrorInAccuracy = measureErrorInAccuracy(up3_AccuracyRTO, up3_AccuracyGT)

    # x0 = np.linspace(1, len(up0_AccuracyRTO), len(up0_AccuracyRTO))
    # x1 = np.linspace(1, len(up1_AccuracyRTO), len(up1_AccuracyRTO))
    # x3 = np.linspace(1, len(up3_AccuracyRTO), len(up3_AccuracyRTO))

    plotDelay()
    # plotaccuracy()



    # fig_up0, (up0_Accuracy, up0_Error) = plt.subplots(2)
    # fig_up0.suptitle("Headend to backend estimation of delay accuracy")
    # up0_Accuracy.plot(x0, up0_AccuracyRTO)
    # up0_Accuracy.plot(x0, up0_AccuracyGT)
    # up0_Accuracy.set_xlabel("Packet number")
    # up0_Accuracy.set_ylabel("Seconds")
    # up0_Error.plot(x0, up0_ErrorInAccuracy)
    # up0_Error.set_xlabel("Packet Number")
    # up0_Error.set_ylabel("Seconds")

    plt.show()


def plotDelay():
    up0, up1, up3, up2_from_up0, up2_from_up1, up2_from_up3 = getData()

    up0_rto, up0_gt, up0_startTime = divideIntoList(up0)
    up1_rto, up1_gt, up1_startTime = divideIntoList(up1)
    up3_rto, up3_gt, up3_startTime = divideIntoList(up3)
    up2_up0_deliverytime = dict_to_list(up2_from_up0)
    up2_up1_deliverytime = dict_to_list(up2_from_up1)
    up2_up3_deliverytime = dict_to_list(up2_from_up3)
    print(len(up0_startTime), len(up2_up0_deliverytime))
    headend_Delay, headend_RTO_Delay, headend_GT_Delay = measureDelay_upX_2_N(up0_rto, up0_gt, up0_startTime, up2_up1_deliverytime)
    sensor1_Delay, sensor1_RTO_Delay, sensor1_GT_Delay = measureDelay_upX_2_N(up1_rto, up1_gt, up1_startTime, up2_up1_deliverytime)
    sensor2_Delay, sensor2_RTO_Delay, sensor2_GT_Delay = measureDelay_upX_2_N(up3_rto, up3_gt, up3_startTime, up2_up3_deliverytime)
    # print(headend_RTO_Delay)
    up0_AccuracyRTO, up0_AccuracyGT = measureAccuracy_upX_2_B(up0_rto, up0_gt, up0_startTime, up2_up1_deliverytime)
    up1_AccuracyRTO, up1_AccuracyGT = measureAccuracy_upX_2_B(up1_rto, up1_gt, up1_startTime, up2_up1_deliverytime)
    up3_AccuracyRTO, up3_AccuracyGT = measureAccuracy_upX_2_B(up3_rto, up3_gt, up3_startTime, up2_up3_deliverytime)
    x0 = np.linspace(1, len(up0_rto), len(up0_rto))
    x1 = np.linspace(1, len(up1_rto), len(up1_rto))
    x3 = np.linspace(1, len(up3_rto), len(up3_rto))


    fig, dp = plt.subplots()
    fig.suptitle("Comparison of delay estimation: no syncronization, RTO and GT")
    dp.plot(x0, sensor1_Delay, "r", label="no synch delay")
    dp.plot(x0, sensor1_RTO_Delay, "b", label= "reference time offset")
    dp.plot(x0, sensor1_GT_Delay, "g", label="Ground truth")
    dp.set_title("Sensor1 delay estimation")
    dp.legend(loc='best')
    dp.set_xlabel("Packet Transfer #")
    dp.set_ylabel("Delay / seconds")

    fig.savefig("include/test/s1h1s1w/Delay_comparison.png")

    fig2, dp2 = plt.subplots()
    fig2.suptitle("Comparison of accuracy in delay estimation: RTO and GT")
    dp2.plot(x0, up1_AccuracyRTO, "r", label="Accuracy RTO")
    dp2.plot(x0, up1_AccuracyGT, "b", label= "Accuracy GT")
    # dp2.plot(x0, sensor1_GT_Delay, "g", label="Ground truth")
    dp2.set_title("Sensor 1: Accuracy of Offsets")
    dp2.legend(loc='best')
    dp2.set_xlabel("Packet Transfer #")
    dp2.set_ylabel("Offset values")

    fig2.savefig("include/test/s1h1s1w/Accuracy_comparison.png")



def plotaccuracy():
    up0, up1, up3, up2 = getData()

    up0_rto, up0_gt, up0_startTime = divideIntoList(up0)
    up1_rto, up1_gt, up1_startTime = divideIntoList(up1)
    up3_rto, up3_gt, up3_startTime = divideIntoList(up3)
    up2_deliverytime = dict_to_list(up2)

    up0_AccuracyRTO, up0_AccuracyGT = measureAccuracy_upX_2_B(up0_rto, up0_gt, up0_startTime, up2_deliverytime)
    up1_AccuracyRTO, up1_AccuracyGT = measureAccuracy_upX_2_B(up1_rto, up1_gt, up1_startTime, up2_deliverytime)
    up3_AccuracyRTO, up3_AccuracyGT = measureAccuracy_upX_2_B(up3_rto, up3_gt, up3_startTime, up2_deliverytime)

    fig, acc = plt.subplots()

    x0 = np.linspace(1, len(up0_AccuracyRTO), len(up0_AccuracyRTO))
    x1 = np.linspace(1, len(up1_AccuracyRTO), len(up1_AccuracyRTO))
    x3 = np.linspace(1, len(up3_AccuracyRTO), len(up3_AccuracyRTO))
    fig.suptitle("Accuracy of delay estimation for Headend to backend")

    acc.plot(x0,up0_AccuracyRTO, "r", label="reference time offset")
    acc.plot(x0, up0_AccuracyGT, "b", label= "ground truth")
    acc.legend(loc="best")
    acc.set_xlabel("packet transfer")
    acc.set_ylabel("Seconds")
    fig.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h1s1w/Accuracy_Headend.png")


    fig2, acc2 = plt.subplots()
    acc2.plot(x1,up1_AccuracyRTO, "r", label="reference time offset")
    acc2.plot(x1, up1_AccuracyGT, "b", label= "ground truth")
    acc2.legend(loc="best")
    acc2.set_xlabel("packet transfer")
    acc2.set_ylabel("Seconds")
    fig2.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h1s1w/Accuracy_Sensor1.png")
    fig2.suptitle("Accuracy of delay estimation for Sensor2 to backend")
    
    fig3, acc3 = plt.subplots()

    acc3.plot(x3,up3_AccuracyRTO, "r", label="reference time offset")
    acc3.plot(x3, up3_AccuracyGT, "b", label= "ground truth")
    acc3.legend(loc="best")
    acc3.set_xlabel("packet transfer")
    acc3.set_ylabel("Seconds")
    fig3.savefig("/home/ubeyd/AAU/6_semester/P6-A3-207/include/test/s1h1s1w/Accuracy_Sensor2.png")
    fig3.suptitle("Accuracy of delay estimation for Sensor2 to backend")

# This function will plot Accuracy of the vkt clocks
def experiment():

    up0, up1, up3, up2_from_up0, up2_from_up1, up2_from_up3 = getData()

    up0_rto, up0_gt, up0_startTime = divideIntoList(up0)
    up1_rto, up1_gt, up1_startTime = divideIntoList(up1)
    up3_rto, up3_gt, up3_startTime = divideIntoList(up3)
    up2_up0_deliverytime = dict_to_list(up2_from_up1)
    up2_up1_deliverytime = dict_to_list(up2_from_up1)
    up2_up3_deliverytime = dict_to_list(up2_from_up3)

run()