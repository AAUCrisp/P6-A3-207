from plottingFunctions import *

def delay_s1():
    sensor, backend = getData_s1()

    sensor_rto, sensor_gt, sensor_startTime = divideIntoList_old(sensor)
    backend_deliveryTime = dict_to_list(backend)

    sensor_delay, sensor_rto_delay, sensor_gt_delay = measureDelay_upX_2_N(sensor_rto, sensor_gt, sensor_startTime, backend_deliveryTime)
    sensor_Accuracy_rto, sensor_Accuracy_gt = measureAccuracy_upX_2_B(sensor_rto, sensor_gt, sensor_startTime, backend_deliveryTime)

    delay_ms = [1000 * x for x in sensor_delay]
    delay_rto_ms = [1000 * x for x in sensor_rto_delay]
    delay_gt_ms = [1000 * x for x in sensor_gt_delay]

    x = np.linspace(1, len(sensor_rto), len(sensor_rto))

    fig, dp = plt.subplots()
    fig.suptitle("Topology #1: Delay estimation")
    dp.plot(x, sensor_delay, "r", label="no synch delay")
    dp.plot(x, sensor_rto_delay, "b", label= "reference time offset")
    dp.plot(x, sensor_gt_delay, "g", label="Ground truth")
    dp.legend(loc='best')
    dp.set_xlabel("Packet Transfer #")
    dp.set_ylabel("Delay / seconds")

    fig.savefig("include/test/s1w/topology_1_delay.png")

    fig2, acc = plt.subplots()
    fig2.suptitle("Topology #1: Accuracy in delay estimation")
    acc.plot(x, sensor_Accuracy_rto, "r", label="Accuracy RTO")
    acc.plot(x, sensor_Accuracy_gt, "b", label= "Accuracy GT")
    acc.legend(loc='best')
    acc.set_xlabel("Packet Transfer #")
    acc.set_ylabel("Offset values")
    fig2.savefig("include/test/s1w/topology_1_Accuracy.png")
    plt.show()

def delay_s2():
    sensor1, sensor2, backend_S1, backend_S2 = getData_s2()
    
    sensor1_rto, sensor1_gt, sensor1_startTime = divideIntoList(sensor1)
    sensor2_rto, sensor2_gt, sensor2_startTime = divideIntoList(sensor2) 
    backend_s1_rx = dict_to_list(backend_S1)
    backend_s2_rx = dict_to_list(backend_S2)

    sensor1_delay, sensor1_rto_delay, sensor1_gt_delay = measureDelay_upX_2_N(sensor1_rto, sensor1_gt, sensor1_startTime, backend_s1_rx)
    sensor2_delay, sensor2_rto_delay, sensor2_gt_delay = measureDelay_upX_2_N(sensor2_rto, sensor2_gt, sensor2_startTime, backend_s2_rx)

    sensor1_accuracy_rto, sensor1_accuracy_gt = measureAccuracy_upX_2_B(sensor1_rto, sensor1_gt, sensor1_startTime, backend_s1_rx)
    sensor2_accuracy_rto, sensor2_accuracy_gt = measureAccuracy_upX_2_B(sensor2_rto, sensor2_gt, sensor2_startTime, backend_s2_rx)
    x = np.linspace(1, len(sensor1_rto), len(sensor1_rto))
    x2 = np.linspace(1, len(sensor2_rto), len(sensor2_rto))

    fig, dp = plt.subplots()
    fig.suptitle("Topology #6: Delay estimation")
    dp.plot(x, sensor1_delay, "r", label="sensor1: no synch delay")
    dp.plot(x, sensor1_rto_delay, "b", label= "sensor1: reference time offset")
    dp.plot(x, sensor1_gt_delay, "g", label="sensor1: Ground truth")
    dp.plot(x2, sensor2_delay, label="sensor2: no synch delay")
    dp.plot(x2, sensor2_rto_delay, label= "sensor2: reference time offset")
    dp.plot(x2, sensor2_gt_delay, label="sensor2: Ground truth")
    dp.legend(loc='best')
    dp.set_xlabel("Packet Transfer #")
    dp.set_ylabel("Delay / seconds")

  
    fig.savefig("include/test/s2w/topology_6_delay.png")

    fig2, acc = plt.subplots()
    fig2.suptitle("Topology #6: Accuracy in delay estimation")
    acc.plot(x, sensor1_accuracy_rto, "r", label="sensor1: Accuracy RTO")
    acc.plot(x, sensor1_accuracy_gt, "b", label= "sensor1: Accuracy GT")
    acc.plot(x2, sensor2_accuracy_rto, "r", label="sensor2: Accuracy RTO")
    acc.plot(x2, sensor2_accuracy_gt, "b", label= "sensor2: Accuracy GT")
    acc.legend(loc='best')
    acc.set_xlabel("Packet Transfer #")
    acc.set_ylabel("Offset values")
    fig2.savefig("include/test/s2w/topology_6_Accuracy.png")
    plt.show()

def delay_s3():
    sensor1, sensor2, sensor3, backend_S1, backend_S2, backend_S3 = getData_s3()
    
    sensor1_rto, sensor1_gt, sensor1_startTime = divideIntoList(sensor1)
    sensor2_rto, sensor2_gt, sensor2_startTime = divideIntoList(sensor2)
    sensor3_rto, sensor3_gt, sensor3_startTime = divideIntoList(sensor3) 
    backend_s1_rx = dict_to_list(backend_S1)
    backend_s2_rx = dict_to_list(backend_S2)
    backend_s3_rx = dict_to_list(backend_S3)

    sensor1_delay, sensor1_rto_delay, sensor1_gt_delay = measureDelay_upX_2_N(sensor1_rto, sensor1_gt, sensor1_startTime, backend_s1_rx)
    sensor2_delay, sensor2_rto_delay, sensor2_gt_delay = measureDelay_upX_2_N(sensor2_rto, sensor2_gt, sensor2_startTime, backend_s2_rx)
    sensor3_delay, sensor3_rto_delay, sensor3_gt_delay = measureDelay_upX_2_N(sensor3_rto, sensor3_gt, sensor3_startTime, backend_s3_rx)

    sensor1_accuracy_rto, sensor1_accuracy_gt = measureAccuracy_upX_2_B(sensor1_rto, sensor1_gt, sensor1_startTime, backend_s1_rx)
    sensor2_accuracy_rto, sensor2_accuracy_gt = measureAccuracy_upX_2_B(sensor2_rto, sensor2_gt, sensor2_startTime, backend_s2_rx)
    sensor3_accuracy_rto, sensor3_accuracy_gt = measureAccuracy_upX_2_B(sensor3_rto, sensor3_gt, sensor3_startTime, backend_s3_rx)
    x = np.linspace(1, len(sensor1_rto), len(sensor1_rto))
    x2 = np.linspace(1, len(sensor2_rto), len(sensor2_rto))
    x3 = np.linspace(1, len(sensor3_rto), len(sensor3_rto))

    fig, dp = plt.subplots()
    fig.suptitle("Topology #7: Delay estimation")
    dp.plot(x, sensor1_delay, "r", label="sensor1: no synch delay")
    dp.plot(x, sensor1_rto_delay, "b", label= "sensor1: reference time offset")
    dp.plot(x, sensor1_gt_delay, "g", label="sensor1: Ground truth")
    dp.plot(x2, sensor2_delay, label="sensor2: no synch delay")
    dp.plot(x2, sensor2_rto_delay, label= "sensor2: reference time offset")
    dp.plot(x2, sensor2_gt_delay, label="sensor2: Ground truth")
    dp.plot(x3, sensor3_delay, label="sensor3: no synch delay")
    dp.plot(x3, sensor3_rto_delay, label= "sensor3: reference time offset")
    dp.plot(x3, sensor3_gt_delay, label="sensor3: Ground truth")
    dp.legend(loc='best')
    dp.set_xlabel("Packet Transfer #")
    dp.set_ylabel("Delay / seconds")

  
    fig.savefig("include/test/s3w/topology_7_delay.png")

    fig2, acc = plt.subplots()
    fig2.suptitle("Topology #7: Accuracy in delay estimation")
    acc.plot(x, sensor1_accuracy_rto, "r", label="sensor1: Accuracy RTO")
    acc.plot(x, sensor1_accuracy_gt, "b", label= "sensor1: Accuracy GT")
    acc.plot(x2, sensor2_accuracy_rto, label="sensor2: Accuracy RTO")
    acc.plot(x2, sensor2_accuracy_gt, label= "sensor2: Accuracy GT")
    acc.plot(x3, sensor3_accuracy_rto, label="sensor3: Accuracy RTO")
    acc.plot(x3, sensor3_accuracy_gt, label= "sensor3: Accuracy GT")
    acc.legend(loc='best')
    acc.set_xlabel("Packet Transfer #")
    acc.set_ylabel("Offset values")
    fig2.savefig("include/test/s3w/topology_7_Accuracy.png")
    plt.show()

def delay_s1h1s1():
    sensor1, sensor2, backend_S1, backend_S2 = getData_s1h1s1()
    
    sensor1_rto, sensor1_gt, sensor1_startTime = divideIntoList(sensor1)
    sensor2_rto, sensor2_gt, sensor2_startTime = divideIntoList(sensor2) 
    backend_s1_rx = dict_to_list(backend_S1)
    backend_s2_rx = dict_to_list(backend_S2)

    sensor1_delay, sensor1_rto_delay, sensor1_gt_delay = measureDelay_upX_2_N(sensor1_rto, sensor1_gt, sensor1_startTime, backend_s1_rx)
    sensor2_delay, sensor2_rto_delay, sensor2_gt_delay = measureDelay_upX_2_N(sensor2_rto, sensor2_gt, sensor2_startTime, backend_s2_rx)

    sensor1_accuracy_rto, sensor1_accuracy_gt = measureAccuracy_upX_2_B(sensor1_rto, sensor1_gt, sensor1_startTime, backend_s1_rx)
    sensor2_accuracy_rto, sensor2_accuracy_gt = measureAccuracy_upX_2_B(sensor2_rto, sensor2_gt, sensor2_startTime, backend_s2_rx)
    x = np.linspace(1, len(sensor1_rto), len(sensor1_rto))
    x2 = np.linspace(1, len(sensor2_rto), len(sensor2_rto))

    fig, dp = plt.subplots()
    fig.suptitle("Topology #5: Delay estimation")
    dp.plot(x, sensor1_delay, "r", label="sensor1: no synch delay")
    dp.plot(x, sensor1_rto_delay, "b", label= "sensor1: reference time offset")
    dp.plot(x, sensor1_gt_delay, "g", label="sensor1: Ground truth")
    dp.plot(x2, sensor2_delay, label="sensor2: no synch delay")
    dp.plot(x2, sensor2_rto_delay, label= "sensor2: reference time offset")
    dp.plot(x2, sensor2_gt_delay, label="sensor2: Ground truth")
    dp.legend(loc='best')
    dp.set_xlabel("Packet Transfer #")
    dp.set_ylabel("Delay / seconds")

  
    fig.savefig("include/test/s1h1s1w/topology_5_delay.png")

    fig2, acc = plt.subplots()
    fig2.suptitle("Topology #5: Accuracy in delay estimation")
    acc.plot(x, sensor1_accuracy_rto, "r", label="sensor1: Accuracy RTO")
    acc.plot(x, sensor1_accuracy_gt, "b", label= "sensor1: Accuracy GT")
    acc.plot(x2, sensor2_accuracy_rto, label="sensor2: Accuracy RTO")
    acc.plot(x2, sensor2_accuracy_gt, label= "sensor2: Accuracy GT")
 
    acc.legend(loc='best')
    acc.set_xlabel("Packet Transfer #")
    acc.set_ylabel("Offset values")
    fig2.savefig("include/test/s1h1s1w/topology_5_Accuracy.png")
    plt.show()
  
def delay_s1h1():
    sensor, backend = getData_s1h1()

    sensor_rto, sensor_gt, sensor_startTime = divideIntoList(sensor)
    backend_deliveryTime = dict_to_list(backend)

    sensor_delay, sensor_rto_delay, sensor_gt_delay = measureDelay_upX_2_N(sensor_rto, sensor_gt, sensor_startTime, backend_deliveryTime)
    sensor_Accuracy_rto, sensor_Accuracy_gt = measureAccuracy_upX_2_B(sensor_rto, sensor_gt, sensor_startTime, backend_deliveryTime)


    x = np.linspace(1, len(sensor_rto), len(sensor_rto))

    fig, dp = plt.subplots()
    fig.suptitle("Topology #2: Delay estimation")
    dp.plot(x, sensor_delay, "r", label="no synch delay")
    dp.plot(x, sensor_rto_delay, "b", label= "reference time offset")
    dp.plot(x, sensor_gt_delay, "g", label="Ground truth")
    dp.legend(loc='best')
    dp.set_xlabel("Packet Transfer #")
    dp.set_ylabel("Delay / seconds")

    fig.savefig("include/test/data/s1h1w/topology_2_delay.png")

    fig2, acc = plt.subplots()
    fig2.suptitle("Topology #2: Accuracy in delay estimation")
    acc.plot(x, sensor_Accuracy_rto, "r", label="Accuracy RTO")
    acc.plot(x, sensor_Accuracy_gt, "b", label= "Accuracy GT")
    acc.legend(loc='best')
    acc.set_xlabel("Packet Transfer #")
    acc.set_ylabel("Offset values")
    fig2.savefig("include/test/data/s1h1w/topology_2_Accuracy.png")
    plt.show()

def delay_s1h2():
    sensor, backend = getData_s1h2()

    sensor_rto, sensor_gt, sensor_startTime = divideIntoList_old(sensor)
    backend_deliveryTime = dict_to_list(backend)

    sensor_delay, sensor_rto_delay, sensor_gt_delay = measureDelay_upX_2_N(sensor_rto, sensor_gt, sensor_startTime, backend_deliveryTime)
    sensor_Accuracy_rto, sensor_Accuracy_gt = measureAccuracy_upX_2_B(sensor_rto, sensor_gt, sensor_startTime, backend_deliveryTime)


    x = np.linspace(1, len(sensor_rto), len(sensor_rto))

    fig, dp = plt.subplots()
    fig.suptitle("Topology #3: Delay estimation")
    dp.plot(x, sensor_delay, "r", label="no synch delay")
    dp.plot(x, sensor_rto_delay, "b", label= "reference time offset")
    dp.plot(x, sensor_gt_delay, "g", label="Ground truth")
    dp.legend(loc='best')
    dp.set_xlabel("Packet Transfer #")
    dp.set_ylabel("Delay / seconds")

    fig.savefig("include/test/s1h2w/topology_3_delay.png")

    fig2, acc = plt.subplots()
    fig2.suptitle("Topology #3: Accuracy in delay estimation")
    acc.plot(x, sensor_Accuracy_rto, "r", label="Accuracy RTO")
    acc.plot(x, sensor_Accuracy_gt, "b", label= "Accuracy GT")
    acc.legend(loc='best')
    acc.set_xlabel("Packet Transfer #")
    acc.set_ylabel("Offset values")
    fig2.savefig("include/test/s1h2w/topology_3_Accuracy.png")
    plt.show()

def up2_groundtruth():
    gt = getData_up2_to_up2()
    gt_list, rto_list = dict_to_list_gt(gt)
    print(gt_list)
    x = np.linspace(1, len(gt_list), len(gt_list))
    fig, dp = plt.subplots()
    fig.suptitle("NTP Offset Tendencies")
    dp.plot(x, gt_list, "b", label="GT")
    dp.plot(x, rto_list, "r", label="RTO")
    dp.legend(loc='best')
    dp.set_xlabel("Sync #")
    dp.set_ylabel("Synch Value")
    dp.set_ylim(-0.00130,0.0000 )
    fig.savefig("/home/ubeyd/Desktop/NTP_Tendencies.png")

    
    
    # fig2, dp2 = plt.subplots()
    # fig2.suptitle("NTP Tendencies: RTO offset")
    # dp2.plot(x, rto_list, "r", label="RTO")
    # dp2.legend(loc='best')
    # dp2.set_xlabel("sync #")
    # dp2.set_ylabel("synch value")
    # dp2.set_ylim(-0.00150,0.00025 )
    # fig2.savefig("/home/ubeyd/Desktop/NTP_Tendencies_RTO.png")
    plt.show()
    


def run():
    # delay_s1()
    # delay_s2()
    # delay_s3()
    # delay_s1h1s1()
    # delay_s1h1()
    # delay_s1h2()
    up2_groundtruth()

run()
