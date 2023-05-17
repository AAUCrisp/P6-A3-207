from include.setup import *
from include.Database import *
from numpy import mean



if __name__ == "__main__":
    
    t1DbPath = str(os.getcwd()) + "/data/syncInterval_3/database.db3"
    t1Db = Database(t1DbPath)
    t1S1data = t1Db.fetchPlotDelays(2)
    t1S2data = t1Db.fetchPlotDelays(4)


    t2DbPath = str(os.getcwd()) + "/data/syncInterval_15/database.db3"
    t2Db = Database(t2DbPath)
    t2S1data = t2Db.fetchPlotDelays(2)
    t2S2data = t2Db.fetchPlotDelays(4)


    t3DbPath = str(os.getcwd()) + "/data/syncInterval_30/database.db3"
    t3Db = Database(t3DbPath)
    t3S1data = t3Db.fetchPlotDelays(2)
    t3S2data = t3Db.fetchPlotDelays(4)

    print(f"The extracted data is:\n")
    for i in enumerate(t1S1data):
        print(i)



    # S1meanGT = delay + GT for delay, GT in zip(S1data['combinedDelay'], S1data['GT'])

    # S1meanGT = mean([value - rto for value, rto in zip(float(S1data['combinedDelay']), float(S1data['GT']))])

    # print(f"Mean is: {S1meanGT}")