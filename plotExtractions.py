from include.setup import *
from include.Database import *
from numpy import mean



if __name__ == "__main__":
    
    dbPath = str(os.getcwd()) + "/include/db.db3"
    db = Database(dbPath)

    # S1data = db.fetchPlotDelays(6)
    S1data = db.fetchPlotDelays(2)
    S2data = db.fetchPlotDelays(4)

    print(f"The extracted data is:\n")
    for i in enumerate(S1data):
        print(i)



    # S1meanGT = delay + GT for delay, GT in zip(S1data['combinedDelay'], S1data['GT'])

    # S1meanGT = mean([value - rto for value, rto in zip(float(S1data['combinedDelay']), float(S1data['GT']))])

    # print(f"Mean is: {S1meanGT}")