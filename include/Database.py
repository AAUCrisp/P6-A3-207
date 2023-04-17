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
            print(f" -  Current Receive IP:         {lastIP}")
            print(f" -  Current rxTime:             {frameData[0]}")
            print(f" -  Current txTime:             {frameData[1]}")
            nodeData[i]['nodeIP'] = lastIP
            nodeData[i]['rxTime'] = frameData[0]
            nodeData[i]['txTime'] = frameData[1]
            # print(f" -  Current Payload:            {frameData[4]}")
            lastIP = frameData[3]

            # pigLen = frameData[2].count(DSEP)
            # print(f"Piggy Frame: {pigLen}")

            if frameData[2].count(DSEP) > 0:
                pigFrame = frameData[2].split(DSEP)
                print(f" -  Current postTxTime:         {pigFrame[0]}")
                print(f" -  Current Piggy:              {pigFrame[1]}")
                nodeData[i]['postTxTime'] = pigFrame[0]
                nodeData[i]['payload'] = pigFrame[1]
                # nodeData[i]['piggy'] = pigFrame[1]

                ###  OH SHIT!!! Need to add Piggy-data as a Combined !!

            else:
                print(f" -  Current postTxTime:         {frameData[2]}")
                nodeData[i]['postTxTime'] = frameData[2]
                



    frameData = nodes[layers-1].split(SEP)

    print(f"\nSensor Frame Number:        {layers}")
    print(f" -  Current Receive IP:         {lastIP}")
    print(f" -  Sensor genTime:             {frameData[0]}")
    print(f" -  Sensor txTime:              {frameData[1]}")
    print(f" -  Sensor postTxTime:          {frameData[2]}")
    print(f" -  Sensor Payload:             {frameData[3]}")
    nodeData[layers-1]['nodeIP'] = lastIP
    nodeData[layers-1]['rxTime'] = frameData[0]
    nodeData[layers-1]['txTime'] = frameData[1]
    nodeData[layers-1]['postTxTime'] = frameData[2]
    nodeData[layers-1]['payload'] = frameData[3]

    comDelay = float(recvTime) - float(frameData[0])


    # print(f"\nNodeData Dict Contains:")
    # for i in range(len(nodeData)):
    #     print(nodeData[i])


    db.insertData(nodeData)



    sensorData = db.fetchSensorInfo(lastIP)

    print(f"Fetched Sensor Data is: {sensorData}")

    # Needs updates for the GT data...
    comTrans = { 
        'sensorId': sensorData[0]['sensorId'],
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
        """General Fetch Function
        -
        Will by default return everything in the requested table, as is configurable to whatever needed.

        
        Args:
        -----
        - `table (str)`: The table to get data from.
        - `setup (dict, optional)`: Configuration to specify the needs of your query.

        ________  

        Setup Options:
        -----
        Left ones are keys in the dict, right is values  

        - `select (str)`:  "column, other_column"  Really shouldn't be this way.
        - `where (dict)`:  {column: value}
        - `join (dict)`:  {join_table: 'OG_table.OG_column = join_table.join_column'}.  
        - `limit (int)`:  Limit number of returned rows.  
        - `order (dict)`:  {'column: 'ASC|DESC'}.  
        
        ________  
        
        Returns:
        -----
        `dict`: containing the retrieved data
        """        
        # print(setup)
        # print("Inside DB Fetch")


        self.con = sqlite3.connect(self.filePath, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()


        # Default fetch config
        config = {'select': '*', 
            'where': None,
            'join': None,
            'limit': None,
            'order': None
            }

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

        if config['order']:
            sql += f"""
            ORDER BY """
            for i, key in enumerate(config['order']):
                if i > 0:
                    sql += ", "
                sql += f"{key} {config['order'][key]}"
        if config['limit']:
            sql += f"""
            LIMIT {config['limit']}"""


        print(f"\nSQL Statement is:{sql}\n\n")
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



    def fetchSensorInfo(self, nodeIP):
        """Fetches the needed info for inserting the new sensor data.

        ______  

        Args:
        ---
            `nodeIP (str)`: IP address for the origin-sensor

        ______  

        Returns:
        ---
            `dict`: with `sensorId` and `txId` keys
        """    

        sensorParams = { 
            'select': "CombinedTransfer.sensorId, CombinedTransfer.id AS txId",
            'where': {
                'ip5g': nodeIP,
                'OR': None,
                'ipWifi': nodeIP
                },
            'join':{
                'CombinedTransfer': 'Node.id=CombinedTransfer.sensorId'
                },
            'order': {
                'CombinedTransfer.id': 'DESC'
                },
            'limit': 1
            }


        sensorData = db.fetch('Node', sensorParams)

        return sensorData


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

        payloadFrames = []
        oldDelays = []
        newInput = []
        sensorData = []
        oldHeadends = []


        # print("Full NodeData is:")
        # for i in range(len(nodeData)):
        #     print(nodeData[i])


        for i in range(len(nodeData)):

            # Update Last Transmissions tx and postTx data
            # - Fetch newest CompleteTransfer from this SensorIP
            # -- Then fetch the HeadendTransfer IDs attached to it
            # --- Update (insert) tx and postTx values in "old data"
            # ---- Can likely do it in a single SQL Sentence

            oldDelays.append({
                'nodeIP': nodeData[i]['nodeIP'],
                'txTime': nodeData[i]['txTime'],
                'postTxTime': nodeData[i]['postTxTime']
            })

            newInput.append({
                'nodeIP': nodeData[i]['nodeIP'],
                'rxTime': nodeData[i]['rxTime']
            })


            if 'payload' in nodeData[i]:
                # THIS IS SENSOR DATA!!!

                # Insert in CombinedTransfer Table
                print("Sensor Frame State, around line 400 in DB")

                newInput[i].__setitem__('payload', nodeData[i]['payload'])

                sensorData.append(db.fetchSensorInfo(nodeData[i]['nodeIP'])[0])


                payloadFrames.append(i)


            else:
                # Insert in HeadendTransfer Table
                print("Headend Frame State, around line 400 in DB")

            # print(nodeData[i])



        # print(f"Old Frame Data is:")
        # for i in range(len(oldHeadends)):
        #     print(oldHeadends)


        # print(f"\nSensorData is: {sensorData[1][0]['sensorId']}")
        # print(f"\nSensorData is: {sensorData}")

        for j, frameKey in enumerate(payloadFrames):

            print(f"\nJ is: {j}\nframeKey is: {frameKey}\n")

            oldParams = {
                'where': {
                    'transferId': sensorData[j]['txId']
                },
                'order': {
                    'id': 'DESC'
                }
            }

            oldHeadends = db.fetch('HeadendTransfer', oldParams)


            for i, frame in enumerate(newInput):

                print(f"Index number {i} has framedata {frame}")
                # updateParams = {
                #     'values': {
                #         'nodeId': oldHeadends[frameKey]['nodeId'],
                #         'txTime': frame['txTime'],
                #         'postTxTime': frame['postTxTime'],
                #     }
                # }



        print(f"\nData is in Frames: {payloadFrames}")
        print(f"Old Delays Data is:\n{oldDelays}\n")


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


