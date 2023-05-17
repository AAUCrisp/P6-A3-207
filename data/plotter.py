from subprocess import check_output as co
from json import loads
import matplotlib.pyplot as plt
from numpy import mean, sum
from include.Database import Database

payload10_db = "data/syncInterval_30/database.db3"
payload100_db = "data/payload100/database.db3"
payload1000_db = "data/payload1000/database.db3"
payload10_s1pings = "data/syncInterval_30/up1_ping.log"
payload10_s2pings = "data/syncInterval_30/up3_ping.log"
payload10_hpings = "data/syncInterval_30/up0_ping.log"
payload100_s1pings = "data/payload100/up1_ping.log"
payload100_s2pings = "data/payload100/up3_ping.log"
payload100_hpings = "data/payload100/up0_ping.log"
payload1000_s1pings = "data/payload1000/up1_ping.log"
payload1000_s2pings = "data/payload1000/up3_ping.log"
payload1000_hpings = "data/payload1000/up0_ping.log"

datarateU_db = "data/syncInterval_30/database.db3"
datarate1kb_db = "data/datarate1kbps/database.db3"
datarate2kb_db = "data/datarate2kbps/database.db3"
datarateU_s1pings = "data/syncInterval_30/up1_ping.log"
datarateU_s2pings = "data/syncInterval_30/up3_ping.log"
datarateU_hpings = "data/syncInterval_30/up0_ping.log"
datarate1kb_s1pings = "data/datarate1kbps/up1_ping.log"
datarate1kb_s2pings = "data/datarate1kbps/up3_ping.log"
datarate1kb_hpings = "data/datarate1kbps/up0_ping.log"
datarate2kb_s1pings = "data/datarate2kbps/up1_ping.log"
datarate2kb_s2pings = "data/datarate2kbps/up3_ping.log"
datarate2kb_hpings = "data/datarate2kbps/up0_ping.log"

transferInterval3_db = "data/syncInterval_30/database.db3"
transferInterval10_db = "data/datarate1kbps/database.db3"
transferInterval30_db = "data/datarate2kbps/database.db3"
transferInterval3_s1pings = "data/syncInterval_30/up1_ping.log"
transferInterval3_s2pings = "data/syncInterval_30/up3_ping.log"
transferInterval3_hpings = "data/syncInterval_30/up0_ping.log"
transferInterval10_s1pings = "data/datarate1kbps/up1_ping.log"
transferInterval10_s2pings = "data/datarate1kbps/up3_ping.log"
transferInterval10_hpings = "data/datarate1kbps/up0_ping.log"
transferInterval30_s1pings = "data/datarate2kbps/up1_ping.log"
transferInterval30_s2pings = "data/datarate2kbps/up3_ping.log"
transferInterval30_hpings = "data/datarate2kbps/up0_ping.log"

syncInterval3_db = "data/syncInterval_30/database.db3"
syncInterval10_db = "data/datarate1kbps/database.db3"
syncInterval30_db = "data/datarate2kbps/database.db3"
syncInterval3_s1pings = "data/syncInterval_30/up1_ping.log"
syncInterval3_s2pings = "data/syncInterval_30/up3_ping.log"
syncInterval3_hpings = "data/syncInterval_30/up0_ping.log"
syncInterval10_s1pings = "data/datarate1kbps/up1_ping.log"
syncInterval10_s2pings = "data/datarate1kbps/up3_ping.log"
syncInterval10_hpings = "data/datarate1kbps/up0_ping.log"
syncInterval30_s1pings = "data/datarate2kbps/up1_ping.log"
syncInterval30_s2pings = "data/datarate2kbps/up3_ping.log"
syncInterval30_hpings = "data/datarate2kbps/up0_ping.log"

def plotSensorDelay(dbs:list[str], pings:list[list[str]], xvalues:list[int], sensorId:int, title):
    #delays = {x:[obj["combinedDelay"] for obj in loads(co(f"sqlite3 {db} 'select combinedDelay from PayloadTransfer where sensorId = {sensorId}' -json", shell=True).decode())] for db, x in zip(dbs, xvalues)}
    #rtos = {x:[obj["RTO"] for obj in loads(co(f"sqlite3 {db} 'select RTO from TransferJump where nodeId = {sensorId}' -json", shell=True).decode())] for db, x in zip(dbs, xvalues)}
    #gts = {x:[obj["GT"] for obj in loads(co(f"sqlite3 {db} 'select GT from TransferJump where nodeId = {sensorId}' -json", shell=True).decode())] for db, x in zip(dbs, xvalues)}


    # do delays
    steffenDBs = [Database(db) for db in dbs]

    steffenDelays = [db.fetchPlotDelays(sensorId) for db in steffenDBs]
    
    delays = {x:[obj["combinedDelay"] for obj in delays] for delays, x in zip(steffenDelays, xvalues)}
    rtos = {x:[obj["RTO"] for obj in delays] for delays, x in zip(steffenDelays, xvalues)}
    gts = {x:[obj["GT"] for obj in delays] for delays, x in zip(steffenDelays, xvalues)}



    avgRTODelays = [mean([delay - rto for delay, rto in zip(delays[key], rtos[key])])*1000 for key in xvalues]
    avgGTDelays = [mean([delay - gt for delay, gt in zip(delays[key], gts[key])])*1000 for key in xvalues]

    # do pings
    pingContent:list[list[str]] = []
    for pingRoute in pings:
        pingRouteContent = []
        for ping in pingRoute:
            with open(ping) as file:
                pingRouteContent.append(file.read())
        pingContent.append(pingRouteContent)

    # pingValues = []
    # for pingRoute in pingContent:
    #     tempList1 = []
    #     for ping in pingRoute:
    #         tempList2 = []
    #         for line in ping.split("\n"):
    #             if "time=" in line:
    #                 tempList2.append(float(line.split("time=")[1].split(" ms")[0].strip())/2)
    #         tempList1.append(mean(tempList2))
    #     pingValues.append(sum(tempList1))

    pingValues = [sum([mean([float(line.split("time=")[1].split(" ms")[0].strip()) for line in ping.split("\n") if "time=" in line]) for ping in pingRoute])/2 for pingRoute in pingContent]

    # do plots
    fig, ax = plt.subplots()
    ax.plot(xvalues, avgRTODelays, 'b', label=f"avg RTO delay")
    ax.plot(xvalues, avgGTDelays, 'r', label=f"avg GT delay")
    ax.plot(xvalues, pingValues, 'y', label="Ping delay")
    fig.suptitle(f"{title}: sensor {1 if sensorId == 2 else 2}")
    ax.set_ylabel("ms")
    ax.legend(loc="best")


plotSensorDelay([payload10_db, payload100_db, payload1000_db], [[payload10_s1pings, payload10_hpings], [payload100_s1pings, payload100_hpings], [payload1000_s1pings, payload1000_hpings]], [10,100,1000], 2, "payload")
plotSensorDelay([payload10_db, payload100_db, payload1000_db], [[payload10_s2pings], [payload100_s2pings], [payload1000_s2pings]], [10,100,1000], 4, "payload")

plotSensorDelay([datarateU_db, datarate1kb_db, datarate2kb_db], [[datarateU_s1pings, datarateU_hpings], [datarate1kb_s1pings, datarate1kb_hpings], [datarate1kb_s2pings, datarate1kb_hpings]], [0, 1, 2], 2, "datarate")
plotSensorDelay([datarateU_db, datarate1kb_db, datarate2kb_db], [[datarateU_s2pings], [datarate1kb_s2pings], [datarate2kb_s2pings]], [0, 1, 2], 4, "datarate")

plotSensorDelay([syncInterval3_db, syncInterval10_db, syncInterval30_db], [[syncInterval3_s1pings, syncInterval3_hpings], [syncInterval10_s1pings, syncInterval10_hpings], [syncInterval30_s1pings, syncInterval30_hpings]], [3, 10, 30], 2, "transferInterval")
plotSensorDelay([syncInterval3_db, syncInterval10_db, syncInterval30_db], [[syncInterval3_s2pings], [syncInterval10_s2pings], [syncInterval30_s2pings]], [3, 10, 30], 4, "syncInterval")

plotSensorDelay([transferInterval3_db, transferInterval10_db, transferInterval30_db], [[transferInterval3_s1pings, transferInterval3_hpings], [transferInterval10_s1pings, transferInterval10_hpings], [transferInterval30_s1pings, transferInterval30_hpings]], [3, 10, 30], 2, "transferInterval")
plotSensorDelay([transferInterval3_db, transferInterval10_db, transferInterval30_db], [[transferInterval3_s2pings], [transferInterval10_s2pings], [transferInterval30_s2pings]], [3, 10, 30], 4, "transferInterval")
plt.show()
