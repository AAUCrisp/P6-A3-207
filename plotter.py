from subprocess import check_output as co
from json import loads
import matplotlib.pyplot as plt
from numpy import mean, transpose, sort
import statistics
from math import sqrt, floor, ceil
from sys import argv

from include.Database import Database

_exec = lambda cmd: co(cmd, shell=True).decode()

def z(p:float = 95.0):
    return statistics.NormalDist().inv_cdf(p/100) # std norm dist

def addData(ax:plt.Axes, Z:float, values:list[float], xIndex:int, color:str, a:float, lineWidth:float=0.25, options:list[bool] = [False,False,False,False]):
    assert type(ax) is plt.Axes
    assert type(Z) is float
    assert type(values) is list
    assert type[values[0]] is float or int
    assert type(xIndex) is int or float
    #print(values)
    zscore = z()
    print(f'Z-SCORE:\t{zscore}')
    interval = zscore * statistics.stdev(values) / sqrt(len(values))
    top = mean(values) - interval
    bottom = mean(values) + interval
    left = xIndex - (lineWidth/2)
    right = xIndex + (lineWidth/2)

    maxVal = max(values)
    minVal = min(values)

    # plotting the confidence interval
    if options[2]:
        ax.plot([xIndex, xIndex], [top, bottom], color=color)
        ax.plot([left, right], [top, top], color=color)
        ax.plot([left, right], [bottom, bottom], color=color)
    
    # Plotting the max and min values
    if options[0]:
        ax.plot([xIndex], maxVal, marker='x', color=color)
        ax.plot([xIndex], minVal, marker='x', color=color)

    values95 = sort(values)[ceil(len(values)*0.05):floor(len(values)*0.95)]
    median = sort(values)[floor(len(values)/2)]

    values95bottom = min(values95)
    values95top = max(values95)
    values95left = xIndex - (lineWidth/4)
    values95right = xIndex + (lineWidth/4)

    # 95% of values is in this range
    if options[1]:
        ax.fill_between([values95right, values95left, values95left, values95right], [values95top, values95top, values95bottom, values95bottom], values95bottom, color=color, alpha=a)

    #ax.plot([values95left, values95right], [values95top, values95top], color=color)
    #ax.plot([values95left, values95right], [values95bottom, values95bottom], color=color)
    #ax.plot([values95left, values95left], [values95top, values95bottom], color=color)
    #ax.plot([values95right, values95right], [values95top, values95bottom], color=color)

    # median
    if options[3]:
        ax.plot([left - (((values95left - left)/2))*2, values95right], [median, median], color=color)


def plotSensorDelay(datadirs:list[str], xlabels:list[str], title:str, xlabel:str, options=[False for _ in range(4)]):
    #delays = {x:[obj["combinedDelay"] for obj in loads(co(f"sqlite3 {db} 'select combinedDelay from PayloadTransfer where sensorId = {sensorId}' -json", shell=True).decode())] for db, x in zip(dbs, xvalues)}
    #rtos = {x:[obj["RTO"] for obj in loads(co(f"sqlite3 {db} 'select RTO from TransferJump where nodeId = {sensorId}' -json", shell=True).decode())] for db, x in zip(dbs, xvalues)}
    #gts = {x:[obj["GT"] for obj in loads(co(f"sqlite3 {db} 'select GT from TransferJump where nodeId = {sensorId}' -json", shell=True).decode())] for db, x in zip(dbs, xvalues)}

    xvalues = range(len(xlabels))

    routes = {"s1":["s1", "h"],"s2":["s2"]}
    fig, axs = plt.subplots(len(routes))
    for i, node, route in [(i, item[0], item[1]) for i, item in enumerate(routes.items())]:

        print(F"PLOTTING:\t{title} FOR {node}")

        nodeId = {"s1":2,"s2":4}[node]
        dbs = [f'{directory}/database.db3' for directory in datadirs]
        dbObjects = [Database(db) for db in dbs]
        dbData = [db.fetchPlotDelays(nodeId) for db in dbObjects]
        delays = {x:[float(row["combinedDelay"]) for row in table if not abs(float(row["combinedDelay"])) == float('inf')] for table, x in zip(dbData, xvalues)}
        rtos = {x:[float(row["RTO"]) for row in table] for table, x in zip(dbData, xvalues)}
        gts = {x:[float(row["GT"]) for row in table] for table, x in zip(dbData, xvalues)}
        RTODelays = [[(delay - rto)*1000 for delay, rto in zip(delays[key], rtos[key])] for key in xvalues]
        GTDelays = [[(delay - gt)*1000 for delay, gt in zip(delays[key], gts[key])] for key in xvalues]
        avgRTODelays = [mean([delay - rto for delay, rto in zip(delays[key], rtos[key])])*1000 for key in xvalues]
        avgGTDelays = [mean([delay - gt for delay, gt in zip(delays[key], gts[key])])*1000 for key in xvalues]

        routeFiles = [{"s1":"up1_ping.log","h":"up0_ping.log","s2":"up3_ping.log"}[node] for node in route]
        pings = [[_exec(f"cat {path}/{file}") for file in routeFiles] for path in datadirs]
        pingValues:list[float] = [sum([mean([float(line.split("time=")[1].split(" ms")[0].strip()) for line in ping.split("\n") if "time=" in line]) for ping in pingRoute])/2 for pingRoute in pings]

        axis:plt.Axes = axs[i]
        axis.set_xticks(xvalues)
        axis.set_xticklabels(xlabels)

        GTColor = "#3D4DFF"
        GTAlpha = .7
        RTOColor = "#FD2E2E"
        RTOAlpha = 1
        PingColor = "#E2E504"
        PingAlpha = .7

        axis.plot(xvalues, avgRTODelays, '--', label=f"Avg RTO delay", marker="o", color='r')
        for delay, x in zip(RTODelays, xvalues):
            addData(axis, 1.96, delay, x, RTOColor, RTOAlpha, abs(xvalues[0] - xvalues[-1])/40, options)
        axis.plot(xvalues, avgGTDelays, '--', label=f"Avg GT delay", marker="o", color='b')
        for delay, x in zip(GTDelays, xvalues):
            addData(axis, 1.96, delay, x, GTColor, GTAlpha, abs(xvalues[0] - xvalues[-1])/40, options)
        axis.plot(xvalues, pingValues, '--', label="Ping delay", marker="o", color='y')

        for pingRoute, x in zip(pings, xvalues):
            pingRouteValues = [[float(line.split("time=")[1].split(" ms")[0])/2 for line in pingNode.split("\n") if "time=" in line] for pingNode in pingRoute]

            pingSums = pingRouteValues[0]
            for i in range(len(pingRouteValues[0])):
                for j in range(1, len(pingRouteValues)):
                    if i < len(pingRouteValues[j]):
                        pingSums[i] += pingRouteValues[j][i]

            addData(axis, 1.96, pingSums, x, PingColor, PingAlpha, abs(xvalues[0] - xvalues[-1])/40, options)


        axis.set_ylabel(f"Delay (ms)")
        axis.set_title(f"Sensor {node[-1]}")
        axis.legend(loc="best")

        singleFig, singleAx = plt.subplots()
        singleAx.set_xticks(xvalues)
        singleAx.set_xticklabels(xlabels)
        singleAx.plot(xvalues, avgRTODelays, '--', label=f"Avg RTO delay", marker="o", color='r')
        for delay, x in zip(RTODelays, xvalues):
            addData(singleAx, 1.96, delay, x, RTOColor, RTOAlpha, abs(xvalues[0] - xvalues[-1])/40, options)
        singleAx.plot(xvalues, avgGTDelays, '--', label=f"Avg GT delay", marker="o", color='b')
        for delay, x in zip(GTDelays, xvalues):
            addData(singleAx, 1.96, delay, x, GTColor, GTAlpha, abs(xvalues[0] - xvalues[-1])/40, options)
        singleAx.plot(xvalues, pingValues, '--', label="Ping delay", marker="o", color='y')
        
        for pingRoute, x in zip(pings, xvalues):
            pingRouteValues = [[float(line.split("time=")[1].split(" ms")[0])/2 for line in pingNode.split("\n") if "time=" in line] for pingNode in pingRoute]

            pingSums = pingRouteValues[0]
            for i in range(len(pingRouteValues[0])):
                for j in range(1, len(pingRouteValues)):
                    if i < len(pingRouteValues[j]):
                        pingSums[i] += pingRouteValues[j][i]

            addData(singleAx, 1.96, pingSums, x, PingColor, PingAlpha, abs(xvalues[0] - xvalues[-1])/40, options)


        singleAx.set_ylabel(f"Delay (ms)")
        singleAx.legend(loc="best")
        singleAx.set_xlabel(xlabel)
        singleFig.suptitle(f"{title}\nSensor {node[-1]}")
        singleFig.savefig(f'/home/mast3r/Pictures/p6figs/{title}-s{node[-1]}{int(options[0])}{int(options[1])}{int(options[2])}{int(options[3])}.png'.replace(" ", "-"))
        
    axs[-1].set_xlabel(xlabel)
    fig.suptitle(title)
    fig.savefig(f'/home/mast3r/Pictures/p6figs/{title}-total{int(options[0])}{int(options[1])}{int(options[2])}{int(options[3])}.png'.replace(" ", "-"))
    

baseCase = "data/baseCase"
payload300 = "data/payload300.new"
payload600 = "data/payload600.new"
payload1000 = "data/payload1000.new"
payload1100 = "data/payload1100.new"
payload1200 = "data/payload1200.new"
payload1300 = "data/payload1300.new"
payload1400 = "data/payload1400.new"
sync15 = "data/sync15.new"
sync30 = "data/sync30.new"
sync60 = "data/sync60.new"
sync120 = "data/sync120.new"
sync240 = "data/sync240.new"
sync900 = "data/sync900.new"
datarate750bps = "data/datarate0.75kbps.new"
datarate1kbps = "data/datarate1kbps.new"
datarate2kbps = "data/datarate2kbps.new"
datarate4kbps = "data/datarate4kbps.new"
datarate8kbps = "data/datarate8kbps.new"
transfer13 = "data/transfer13ms.new"
transfer26 = "data/transfer26ms.new"
transfer52 = "data/transfer52ms.new"
transfer104 = "data/transfer104ms.new"
transfer208 = "data/transfer208ms.new"
foil2 = "data/tinfoil2"
foil4 = "data/tinfoil4"
foil6 = "data/tinfoil6"

if len(argv) == 1:
    types = input("specify types (seperated by comma): ").replace(", ", ",").split(",")
    options = [
        True if input("with max and min values?: ")[0] == "y" else False, 
        True if input("Draw box of 95% of the data?: ")[0] == "y" else False,
        True if input("Draw the confidence interval?: ")[0] == "y" else False,
        True if input("Draw median?: ")[0] == "y" else False]
else:
    types = argv[argv.index("--types")+1].replace(", ", ",").split(",") if "--types" in argv else argv[1].replace(", ", ",").split(",") if not "-" in argv[1] else exit("ERROR, please specify tests to plot")
    for arg in argv:
        if arg[0] == "-" and arg[1] != "-":
            for opt in arg:
                match opt:
                    case 'l':
                        argv.append("--maxmin")
                    case 'b':
                        argv.append("--box")
                    case 'c':
                        argv.append("--ci")
                    case 'm':
                        argv.append("--median")
    options = [
        True if "--maxmin" in argv else False,
        True if "--box" in argv else False,
        True if "--ci" in argv else False,
        True if "--median" in argv else False
    ]
if types == ["all"]:
    types = "payload,sync,datarate,transfer,foil".split(",")

for t in types:
    match t:
        case "payload":
            plotSensorDelay([baseCase, payload300, payload600, payload1000, payload1100, payload1200], ["10\nBase Case", "300", "600", "1000", "1100", "1200"], "Payload test", "Payload size (Bytes)", options)
        case "sync":
            plotSensorDelay([sync15, sync15, baseCase, sync60, sync120, sync240, sync900], ["3", "15", "30\nBase Case", "60", "120", "240", "900"], "Sync test", "Sync interval (s)", options)
        case "datarate":
            plotSensorDelay([datarate1kbps, datarate2kbps, datarate4kbps, datarate8kbps, baseCase], ["1", "2", "4", "8", "Unlimited\nBase Case"], "Datarate test", "Datarate (kbps)", options)
        case "transfer":
            plotSensorDelay([transfer13, transfer26, transfer52, transfer104, transfer208, baseCase], ["13", "26", "52", "104", "208", "3000\nBase Case"], "Transfer test", "Transfer interval (ms)", options)
        case "foil":
            plotSensorDelay([baseCase, foil2, foil4, foil6], ["0\nBase Case", "2", "4", "6"], "Foil test", "Layers", options)

plt.show()


