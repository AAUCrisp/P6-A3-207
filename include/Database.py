import sqlite3
# import subprocess


##########################################
#  Remove after figuring shit out!!!

from ProcessData import *
from Formatting import *

SEP =   "\uFFFF"
"""Regular field seperator"""
DSEP =  "\uFFFE"
"""Piggyback data field seperator"""
EOP =   "\uFFFD"
"""End Of Packet seperator"""
interfaceTarget = "wifi"


def unpack(packet, recvIP, recvTime):

    layers = packet.count(EOP) + 1  # Check the number of headend jumps
    nodes = packet.split(EOP)       # Split the frames from each headend

    nodeData = [{key: value for key, value in []} for i in range(layers)]

    lastIP = recvIP

    print(f"Frame Layers: {layers}\n")

    if layers > 0:
        # for i, key in enumerate(nodes):
        # for i in range(layers-1):
        for i in range(layers-1):
            frameData = nodes[i].split(SEP)

            print(f"\nHeadend Frame Number:       {i+1}\n")
            # print(f" -  Current Frama Data:         {key}")
            print(f" -  Current rxTime:             {frameData[0]}")
            print(f" -  Current txTime:             {frameData[1]}")
            nodeData[i]['rxTime'] = frameData[0]
            nodeData[i]['txTime'] = frameData[1]

            # pigLen = frameData[2].count(DSEP)
            # print(f"Piggy Frame: {pigLen}")

            if frameData[2].count(DSEP) > 0:
                pigFrame = frameData[2].split(DSEP)
                print(f" -  Current prevTxTime:         {pigFrame[0]}")
                print(f" -  Current Piggy:              {pigFrame[1]}")
                nodeData[i]['prevTxTime'] = pigFrame[0]
                nodeData[i]['piggy'] = pigFrame[1]

                ###  OH SHIT!!! Need to add Piggy-data as a Combined !!

            else:
                print(f" -  Current prevTxTime:         {frameData[2]}")
                nodeData[i]['prevTxTime'] = frameData[2]
                
            print(f" -  Current Receive IP:         {lastIP}")
            nodeData[i]['recvIP'] = frameData[3]
            # print(f" -  Current Payload:            {frameData[4]}")
            lastIP = frameData[3]



    frameData = nodes[layers-1].split(SEP)

    print(f"\nSensor Frame Number:        {layers}")
    print(f" -  Sensor genTime:             {frameData[0]}")
    print(f" -  Sensor txTime:              {frameData[1]}")
    print(f" -  Sensor prevTxTime:          {frameData[2]}")
    print(f" -  Sensor Payload:             {frameData[3]}")
    nodeData[layers-1]['rxTime'] = frameData[0]
    nodeData[layers-1]['txTime'] = frameData[1]
    nodeData[layers-1]['prevTxTime'] = frameData[2]
    nodeData[layers-1]['recvIP'] = lastIP
    nodeData[layers-1]['payload'] = frameData[3]

    comDelay = float(recvTime) - float(frameData[0])

    sensorParams = { 
        'where': {
            'ip5g': lastIP,
            'OR': None,
            'ipWifi': lastIP
            }, 
        }


    print(f"\nNodeData Dict Contains:")
    db.insertData(nodeData)

    # for i in range(layers):
    #     print(nodeData[i])

    print(f"\nSensor fetch parameters in Backend is: {sensorParams['where']}\n")

    sensorData = db.fetch('Node', sensorParams)

    print(f"Fetched Node Data is: {sensorData}")

    # Needs updates for the GT data...
    comTrans = { 
        'sensorId': sensorData[0]['id'],
        'combinedDelay': comDelay,
        'combinedDelayGT': comDelay,
        'dataTime': frameData[0],
        'dataTimeGT': frameData[0],
        'deliveryTime': recvTime,
        'deliveryTimeGT': recvTime,
        'technology': interfaceTarget
        }

    db.insert('CombinedTransfer', comTrans)


#  Remove after figuring shit out!!!
###########################################



class Database():

    filePath = "/include/db.db3"


    def __init__(self, filePath = None):
        if (filePath != None):
            self.filePath = filePath
        
        self.con = sqlite3.connect(self.filePath, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory    # Make dictionaries instead of lists
        self.cur = self.con.cursor()        # Create a cursor in the DB


    #  --  Function to create dictionary instead of list for fetched data
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d



##########################################
##  --  Fetch Area --
############

    ######################################
    #  --  General fetch function  --
    def fetch(self, table, setup = None):
        # print(setup)
        # print("Inside DB Fetch")


        self.con = sqlite3.connect(self.filePath, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()


        # Default fetch config
        config = {'select': '*', 
            'where': None,
            'join': None}

        # Replace defaults with set settings, if any exists
        if setup:
            config = dict(list(config.items()) + list(setup.items()))

        # print(config)

        sql = f"""
            SELECT {config['select']} 
            FROM '{table}'"""

        if config['join']:
            keys = list(config['join'].keys())

            for i, key in enumerate(config['join']):
                sql += f""" 
            FULL OUTER JOIN {keys[i]} 
            ON {config['join'][key]}"""


        if config['where']:
            
            # print(f"\nWhere parameters in DB is: {config['where']}\n")
            # print(f"Where OR key is: {config['where']['ip5g']}\n")

            orState = False

            for i, key in enumerate(config['where']):

                if i>0 and orState == False:     # If not first column
                    if key != "OR":
                        sql += """ 
            AND """
                    else:
                        sql += """ 
            OR """
                        orState = True

                elif i == 0:       # If first column
                    sql += """
            WHERE """

                if key != "OR":
                    sql += f"""{key}='{config['where'][key]}'"""


        # print(f"\nSQL Statement is:{sql}\n\n")
        self.cur.execute(sql)
        # print("Efter Execute")
        rows = self.cur.fetchall()
        # print("Efter Fetch All")
        # rows = self.cur.fetchone()


    ####################################
    ###  --  Test Printing Area  -- 
        # print(f"Fetched data is:")
        # for row in rows:
        #     print(f"{row}")

        return rows





##########################################
##  --  Insert Area --
############


    ######################################
    #  --  General fetch function  --
    def insert(self, table, params):
        # print("Inside DB Insert")

        self.con = sqlite3.connect(self.filePath, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()


        sql = f"""
            INSERT INTO '{table}'
            ("""

        sql_end = ""


        for i, key in enumerate(params):

            if i>0:     # If not first column
                sql += ", "
                sql_end += ", "
            
            sql += f"{key}"

            sql_end += f"'{params[key]}'"

        sql += f""")
            VALUES ({sql_end})"""


        # print(f"\nSQL Statement is:{sql}\n\n")
        # self.cur.execute(sql)
        # self.con.commit()

        # print(f"Inserted at row in {table} table: {self.cur.lastrowid}")

        return self.cur.lastrowid


    # Method to run through the frames from each node and insert it into the database
    def insertData(self, nodeData):
        
        # print(nodeData)

        piggyFrames = []

        for i in range(len(nodeData)):
            print(nodeData[i])

            # Update Last Transmissions tx and prevTx data
            # - Fetch newest CompleteTransfer from this SensorIP
            # -- Then fetch the HeadendTransfer IDs attached to it
            # --- Update (insert) tx and prevTx values in "old data"
            # ---- Can likely do it in a single SQL Sentence


            if 'payload' in nodeData[i]:
                # THIS IS SENSOR DATA!!!

                # Insert in CombinedTransfer Table
                print("Sensor Frame State, around line 300 in DB")

            elif 'piggy' in nodeData[i]:
                print("Sensor Frame State, around line 300 in DB")
                piggyFrames.append(i)

            else:
                # Insert in HeadendTransfer Table
                print("Headend Frame State, around line 300 in DB")

        print(piggyFrames)

        return 1



##########################################
##  --  Update Area --
############


    ######################################
    #  --  General update function  --
    def update(self, table, params):
        self.con = sqlite3.connect(self.filePath, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()


        sql = f"""
            UPDATE '{table}'
            SET """


        for i, key in enumerate(params['values']):

            if i>0:     # If not first column
                sql += ", "
            
            sql += f"{key} = {params['values'][key]}"


        sql += f"""
            WHERE """

        for i, key in enumerate(params['where']):

            if i>0:     # If not first column
                sql += """ 
            AND """

            else:       # If first column
                sql += """
            WHERE """
        
            sql += f"""{key}={params['where'][key]}"""



        # print(f"\nSQL Statement is:{sql}\n\n")
        self.cur.execute(sql)
        self.con.commit()

        # print(f"Inserted at row in {table} table: {self.cur.lastrowid}")

        return self.cur.lastrowid


if __name__ == "__main__":
    
    db = Database("db.db3")


    ################################
    ##  --  Frame Building  --

    ############################
    ##  Sensor Frame (IP0)
    frame = "12.34" + SEP + "23.45" + SEP + "34.56" + SEP + "Random Sensor Data"
    # - This from UP0
    ############################

    dataframe = ProcessData()

    ##  First Headend Frame (UP1)
    dataframe.setDataTime("45.67")
    dataframe.setTxTime("56.78")
    dataframe.setPostTxTime("67.89")
    dataframe.setPayload(frame)
    dataframe.setReceivedIP("10.31.0.102")  # UP0 IP
    dataframe.setPiggy("Piglet?")
    # - This from UP1

    packet = dataframe.buildHeadendFrame()

    print(f"Simulated Headend Packet is: ")
    print(packet.replace(SEP, green(" | ")).replace(DSEP, blue(" | ")).replace(EOP, magenta(" | ")))


    ##  Second Headend Frame
    dataframe.setDataTime("78.90")
    dataframe.setTxTime("89.01")
    dataframe.setPostTxTime("90.12")
    dataframe.setPayload(packet)
    dataframe.setReceivedIP("10.31.0.13")
    # dataframe.setPiggy("Ms.Piggy?")

    doubet = dataframe.buildHeadendFrame()

    print(f"Simulated Headend Packet is: ")
    print(doubet.replace(SEP, green(" | ")).replace(DSEP, blue(" | ")).replace(EOP, magenta(" | ")))

    recvIP = "127.0.0.1"
    recvTime = "78.90"


    # unpack(packet, recvIP, recvTime)
    unpack(doubet, recvIP, recvTime)


