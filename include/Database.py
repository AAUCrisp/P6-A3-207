# from include.setup import *
import sqlite3
# import subprocess

# rto = None
# gt = None

##########################################
#  Remove after figuring shit out!!!

from ProcessData import *
from Formatting import *

   # The array containing our arguments
verbose = True


def frPrint(payload):
    print(payload.replace(SEP, green(" | ")).replace(PB, blue(" | ")).replace(EON, magenta(" | ")).replace(OFF, cyan(" | ")))



# SEP =   "\uFFFF"
# """Regular field seperator"""
# PB =  "\uFFFE"
# """Piggyback data field seperator"""
# EON =   "\uFFFD"
# """End Of Packet seperator"""
interfaceTarget = "wifi"


def unpack(packet, recvIP, recvTime):

    layers = packet.count(EON)      # Check the number of headend jumps
    # layers = packet.count(EON) + 1  # Check the number of headend jumps
    nodes = packet.split(EON)       # Split the frames from each headend

    nodeData = [{key: value for key, value in []} for i in range(layers)]

    lastIP = recvIP
    newRTO = None
    newGT = None

    print(f"Frame Layers: {layers}\n")

    for i in range(layers):
        frameData = nodes[i].split(SEP)

        if verbose:
            print(f"\nHeadend Frame Number:       {i+1}\n")
            # print(f" -  Current Frama Data:         {key}")
            print(f" -  Current Receive IP:         {lastIP}")
            print(f" -  Current rxTime:             {frameData[0]}")
            print(f" -  Current txTime:             {frameData[1]}")

        nodeData[i]['nodeIP'] = lastIP
        nodeData[i]['rxTime'] = frameData[0]
        # nodeData[i]['rxTimeGT'] = frameData[0]
        nodeData[i]['txTime'] = frameData[1]
        # nodeData[i]['txTimeGT'] = frameData[1]
        # print(f" -  Current Payload:            {frameData[4]}")


        optFrame = frameData[2].split(PB)

        # print(f"OptFrame contains:   {optFrame}")



        #  --  If there's new Offsets  --
        if optFrame[0].count(OFF) > 0:

            # print(f"Inside Offset Area")

            offsetFrame = optFrame[0].split(OFF)
            nodeData[i]['postTxTime'] = offsetFrame[0]
            newRTO = offsetFrame[1]
            newGT = offsetFrame[2]
            nodeData[i]['RTO'] = offsetFrame[1]
            nodeData[i]['GT']= offsetFrame[2]

            if verbose:
                print(f" -  Current postTxTime:         {offsetFrame[0]}")


        else:
            if verbose:
                print(f" -  Current postTxTime:         {optFrame[0]}")
            nodeData[i]['postTxTime'] = optFrame[0]

        
        
        #  --  If there's Piggy Data  --
        # if optFrame[1]:
        if len(optFrame) > 1:
        # if frameData[2].count(PB) > 0:
            pigFrame = frameData[2].split(PB)
            # pigFrame = optFrame[1].split(PB)

            # print(f"Inside Piggy Area")

            if verbose:
                # print(f" -  Current postTxTime:         {optFrame[0].split(OFF)[0]}")
                print(f" -  Current Piggy:              {optFrame[1]}")

            nodeData[i]['payload'] = pigFrame[1]
        
        if i < layers - 1:
            lastIP = frameData[3]
        
        else:
            nodeData[i]['payload'] = nodes[i+1]


    # nodeData[layers-1]['payload'] = nodes[layers-1]
    print(f" -  Sensor Payload:             {nodeData[layers-1]['payload']}")


    db.insertData(nodeData, 101.23)




def old_unpack(packet, recvIP, recvTime):

    # layers = packet.count(EON)      # Check the number of headend jumps
    layers = packet.count(EON) + 1  # Check the number of headend jumps
    nodes = packet.split(EON)       # Split the frames from each headend

    nodeData = [{key: value for key, value in []} for i in range(layers)]

    lastIP = recvIP
    newRTO = None
    newGT = None

    print(f"Frame Layers: {layers}\n")

    if layers > 0:
        for i in range(layers-1):
            frameData = nodes[i].split(SEP)

            if verbose:
                print(f"\nHeadend Frame Number:       {i+1}\n")
                # print(f" -  Current Frama Data:         {key}")
                print(f" -  Current Receive IP:         {lastIP}")
                print(f" -  Current rxTime:             {frameData[0]}")
                print(f" -  Current txTime:             {frameData[1]}")

            nodeData[i]['nodeIP'] = lastIP
            nodeData[i]['rxTime'] = frameData[0]
            # nodeData[i]['rxTimeGT'] = frameData[0]
            nodeData[i]['txTime'] = frameData[1]
            # nodeData[i]['txTimeGT'] = frameData[1]
            # print(f" -  Current Payload:            {frameData[4]}")
            lastIP = frameData[3]

            optFrame = frameData[2].split(PB)

            # print(f"OptFrame contains:   {optFrame}")

            #  --  If there's Piggy Data  --
            if optFrame[1]:
            # if frameData[2].count(PB) > 0:
                pigFrame = frameData[2].split(PB)
                # pigFrame = optFrame[1].split(PB)

                # print(f"Inside Piggy Area")

                if verbose:
                    print(f" -  Current postTxTime:         {optFrame[0].split(OFF)[0]}")
                    print(f" -  Current Piggy:              {optFrame[1]}")
                    # print(f" -  Current postTxTime:         {pigFrame[0]}")
                    # print(f" -  Current Piggy:              {pigFrame[1]}")
                # nodeData[i]['postTxTime'] = pigFrame[0]
                # nodeData[i]['postTxTimeGT'] = optFrame[0]
                nodeData[i]['payload'] = pigFrame[1]

            #  --  If there's new Offsets  --
            if optFrame[0].count(OFF) > 0:

                # print(f"Inside Offset Area")

                offsetFrame = optFrame[0].split(OFF)
                nodeData[i]['postTxTime'] = offsetFrame[0]
                newRTO = offsetFrame[1]
                newGT = offsetFrame[2]

                if verbose:
                    print(f" -  Current postTxTime:         {offsetFrame[0]}")


            else:
                if verbose:
                    print(f" -  Current postTxTime:         {optFrame[0]}")
                nodeData[i]['postTxTime'] = optFrame[0]
                nodeData[i]['postTxTimeGT'] = frameData[2]


    ####################################################
    ##  --  Outdated Last Frame Area  --  ##


    frameData = nodes[layers-1].split(SEP)

    nodeData[layers-1]['nodeIP'] = lastIP
    nodeData[layers-1]['rxTime'] = frameData[0]
    nodeData[layers-1]['txTime'] = frameData[1]
    nodeData[layers-1]['payload'] = frameData[3]

    optFrame = frameData[2].split(PB)

    # print(f"OptFrame contains:   {optFrame}")

    #  --  If there's new Offsets  --
    if optFrame[0].count(OFF) > 0:

        print(f"Inside Offset Area")

        offsetFrame = optFrame[0].split(OFF)
        # nodeData[i]['postTxTime'] = offsetFrame[0]
        nodeData[layers-1]['postTxTime'] = offsetFrame[0]
        newRTO = offsetFrame[1]
        newGT = offsetFrame[2]

        if verbose:
            print(f" -  Current postTxTime:         {optFrame[0].split(OFF)[0]}")


    else:
        if verbose:
            print(f" -  Current postTxTime:         {optFrame[0]}")
        nodeData[layers-1]['postTxTime'] = optFrame[0]



    if verbose:
        print(f"\nSensor Frame Number:        {layers}")
        print(f" -  Current Receive IP:         {nodeData[layers-1]['nodeIP']}")
        print(f" -  Sensor genTime:             {nodeData[layers-1]['rxTime']}")
        print(f" -  Sensor txTime:              {nodeData[layers-1]['txTime']}")
        print(f" -  Sensor postTxTime:          {nodeData[layers-1]['postTxTime']}")
        print(f" -  Sensor Payload:             {nodeData[layers-1]['payload']}")

        if newGT or newRTO:
            print(f" -  New RTO Offset:             {newRTO}")
            print(f" -  New GT Offset:              {newGT}")




    # comDelay = float(recvTime) - float(frameData[0])

    # print(f"\nNodeData Dict Contains:")
    # for i in range(len(nodeData)):
    #     print(nodeData[i])

    db.insertData(nodeData, 101.23)





def transposeArray(matrix):
    
    # print(f"Array in Transpose is: {matrix}")

    length = len(matrix)

    for i, key in enumerate(matrix):
        
        depth = len(matrix[key])
        global result

        if i == 0:
            result = [[None for j in range(length)] for i in range(depth)]
            # print(f"Empty array has structure {result}")

        for j, value in enumerate(matrix[key]):

            result[j][i] = value

            # print(f"""
            # In Transpose:
            #     i is: {i}
            #     key is: {key}
            #     j is: {j}
            #     value is: {value}
            #     array is now: {array}""")
    
    
    return result


def dict_depth(dic, level = 1):

    str_dic = str(dic)
    counter = 0
    for i in str_dic:
        if i == "{" or i == "[":
            counter += 1
        elif i == "}" or i == "]":
            break

    return(counter)

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


    def array_to_string(self, array):
        str_values = str(array)
        str_values = str_values.replace("[", "(")
        str_values = str_values.replace("]", ")")
        str_values = str_values[2:-2]

        return str_values


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
            `dict`: with `sensorId` and `lastTxId` keys
        """    

        sensorParams = { 
            'select': "PayloadTransfer.sensorId, PayloadTransfer.technology, PayloadTransfer.id AS lastTxId",
            'where': {
                'ip5g': nodeIP,
                'OR': None,
                'ipWifi': nodeIP
                },
            'join':{
                'PayloadTransfer': 'Node.id=PayloadTransfer.sensorId'
                },
            'order': {
                'PayloadTransfer.id': 'DESC'
                },
            'limit': 1
            }


        sensorData = self.fetch('Node', sensorParams)

        return sensorData

    def fetchOldTransfer(self, txId):
        """Fetches the needed info for inserting the new sensor data.

        ______  

        Args:
        ---
            `nodeIP (str)`: IP address for the origin-sensor

        ______  

        Returns:
        ---
            `dict`: with `sensorId` and `lastTxId` keys
        """    

        params = { 
            'select': 'PayloadToHeadend.jumpId, HeadendTransfer.rxTime, HeadendTransfer.RTO, HeadendTransfer.GT',
            # 'select': {
            #     "PayloadToHeadend.jumpId",
            #     "HeadendTransfer.rxTime",
            #     "HeadendTransfer.rxTimeGT"
            # },
            'where': {
                'PayloadToHeadend.payloadId': txId
                },
            'join':{
                'HeadendTransfer': 'PayloadToHeadend.jumpId=HeadendTransfer.id'
                },
            # 'order': {
            #     'PayloadTransfer.id': 'DESC'
            #     },
            # 'limit': 1
            }


        result = self.fetch('PayloadToHeadend', params)

        return result



##########################################
##  --  Insert Area --
############


    ######################################
    #  --  General fetch function  --
    def insert(self, table, params):
        print("\n\n  NEW INSERT  \nInside DB Insert\n")
        # print("Inside DB Insert")

        self.con = sqlite3.connect(self.filePath, detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()


        sql = f"""
            INSERT INTO '{table}'
            ("""

        sql_end = ""

        
        depth = dict_depth(params)
        global values

        if depth > 1:
            # print(f"Several Inserts Entered")
            values = transposeArray(params)
            # print(f"Transposed Values Array is: {values}")
            
            str_values = self.array_to_string(values)
            # print(f"\n\nProbable Insert thing!! :  {str_values}\n")

            sql_end += str_values



        print(f"\n\nParams in Insert is: {params}\n")
        # print(f"Param Array Depth is: {depth}")


        for i, key in enumerate(params):
            if i>0:     # If not first column
                sql += ", "
       
            sql += f"{key}"

            if depth == 1:
                if i>0:     # If not first column
                    sql_end += ", "

                sql_end += f"'{params[key]}'"


        # if depth > 1:
        #     str_values = self.array_to_string(values)

        #     print(f"\n\nProbable Insert thing!! :  {str_values}\n")

        #     sql_end += str_values


        sql += f""")
            VALUES ({sql_end})"""
            # RETURNING 'id'"""


        print(f"\nSQL Statement is:{sql}\n\n")
        self.cur.execute(sql)
        self.con.commit()

        # lastRow = self.cur.lastrowid()

        print(f"Inserted at row in {table} table: {self.cur.lastrowid}")
        # print(f"Inserted at row in {table} table: {lastRow}")

        return self.cur.lastrowid
        return lastRow


    # Method to run through the frames from each node and insert it into the database
    def insertData(self, nodeData, endTime):
        
        payloadFrames = []
        oldDelays = []
        newHeadInput = []
        sensorInfo = {'txId':[], 'fromFrame':[]}
        oldTransfers = []

        deliveryTime = endTime

        newRTO = False
        newGT = False


        print("Full NodeData is:")
        for i in range(len(nodeData)):
            print(nodeData[i])


        for i, frame in enumerate(nodeData):

            oldHeadInput = {
                'nodeIP': frame['nodeIP'],
                'txTime': frame['txTime'],
                'postTxTime': frame['postTxTime'],
            }

            oldDelays.append(oldHeadInput)


            newHeadData = {
                'nodeIP': frame['nodeIP'],
                'rxTime': frame['rxTime'],
            }

            # if frame['RTO']:
            if 'RTO' in frame:
                # newHeadData.append(frame['RTO'])
                newHeadData.__setitem__('RTO', frame['RTO'])
                newRTO = True
            # if frame['GT']:
            if 'GT' in frame:
                # newHeadData.append(frame['GT'])
                newHeadData.__setitem__('GT', frame['GT'])
                newGT = True

            newHeadInput.append(newHeadData)


            ##  --  Payload Present  --  ##
            if 'payload' in frame:

                newHeadInput[i].__setitem__('payload', frame['payload'])

                sensorFetch = self.fetchSensorInfo(frame['nodeIP'])[0]
                comDelay = float(deliveryTime) - float(frame['rxTime'])

                oldTransfers.append(sensorFetch['lastTxId'])

                print(f"Fetched Node-info is:\n    {sensorFetch}")

                # global interfaceTarget

                combinedParams = {
                    'sensorId': sensorFetch['sensorId'],
                    'combinedDelay': comDelay,
                    # 'combinedDelayGT': comDelay,
                    'dataTime': frame['rxTime'],
                    # 'dataTimeGT': frame['rxTime'],
                    'deliveryTime': deliveryTime,
                    # 'deliveryTimeGT': deliveryTime,
                    # 'technology': sensorFetch['technology'],
                    'technology': interfaceTarget,
                    'payload': frame['payload']
                }

                idFetch = self.insert('PayloadTransfer', combinedParams)
                txId = idFetch if idFetch else 8
                sensorInfo['txId'].append(txId)
                payloadFrames.append(i)


        piggyCount = len(payloadFrames) - 1
        print(f"Piggy count is: {piggyCount}")

        headendParams = {
            'nodeId': [],
            'rxTime': [],
            'piggyData': [],
            'RTO': [],
            'GT': []
        }


        sensorInfo['fromFrame'].extend(payloadFrames)

        # print(f"\n\nPayload Frames between loops are: {payloadFrames}\n\nSensor Frames between loops are: {sensorFrames}\n\n")

        # print(f"Old Transfers Array contains: {oldTransfers}")
        oldTransfers.reverse()

        #######################################################
        ##  --  Run over each node-jump
        for i, newFrame in enumerate(newHeadInput):            

            ##  -- Start by updating the last transfer with the new delays
            if len(oldTransfers) > 0:

                oldHeadendData = self.fetchOldTransfer(oldTransfers[0])

                if len(oldHeadendData) > 0:
                    oldHeadendData.reverse()
                    print(f"""\n\nOld Headend Data is Found\n    Update Data (oldDelays) is:""")
                    for j in range(len(oldDelays)):
                        print(oldDelays[j])

                    print(f"""\n    Old Headend Data (oldHeadendData) is:""")
                    for j in range(len(oldHeadendData)):
                        print(oldHeadendData[j])

                    print(f"""\n\n    New Headend Input Data is:""")
                    for j in range(len(newHeadInput)):
                        print(newHeadInput[j])

                    if 'RTO' not in newFrame:
                        print(f"\n\nAdding old Offset, as there isn't a new one\n\n")
                        newHeadInput[i].__setitem__('RTO', oldHeadendData[i]['RTO'])

                    if 'GT' not in newFrame:
                        print(f"\n\nAdding old Offset, as there isn't a new one\n\n")
                        newHeadInput[i].__setitem__('GT', oldHeadendData[i]['GT'])


                    processDelay = float(oldDelays[i]['txTime']) - float(oldHeadendData[i]['rxTime'])
                    interfaceDelay = float(oldDelays[i]['postTxTime']) - float(oldDelays[i]['txTime'])

                    updateParams = {
                        'values': {
                            'txTime': oldDelays[i]['txTime'],
                            'postTxTime': oldDelays[i]['postTxTime'],
                            'processDelay': processDelay,
                            'txInterfaceDelay': interfaceDelay
                        },
                        'where': {'id': oldHeadendData[i]['jumpId']}
                    }

                    self.update('HeadendTransfer', updateParams)

                    oldTransfers.pop

                else:
                    print(f"No old Headend data found.\n")
                    newHeadInput[i].__setitem__('RTO', 0)
                    newHeadInput[i].__setitem__('GT', 0)

            print(f"Payload Frames are: {payloadFrames}")



            nodeInfo = self.fetchSensorInfo(newFrame['nodeIP'])

            # print(f"NodeInfo Contains: {nodeInfo}")

            headendParams['nodeId'].append(nodeInfo[0]['sensorId'])
            headendParams['rxTime'].append(newFrame['rxTime'])
            headendParams['piggyData'].append(piggyCount)
            headendParams['RTO'].append(newHeadInput[i]['RTO'])
            headendParams['GT'].append(newHeadInput[i]['GT'])


            if payloadFrames[0] == i:
                piggyCount = piggyCount -1

                # print(f"\n\nSensor Frame before Payload Pop: {sensorInfo['fromFrame']}\n\n")
                payloadFrames.pop(0)


        # if len(updateParams['values']['txTime']) > 0:
        #     self.update('HeadendTransfer', updateParams)

        # sensorInfo['txId'].pop(0)

        if dict_depth(sensorInfo['txId']) > 1:
            print(f"Insert the piggyback ones also")

        print(f"\n__________________________\nNewTxId is: {sensorInfo['txId']}")
        print(f"Headend Parameters is: {headendParams}")



        relationParams = {
            'payloadId': [],
            'jumpId': []
        }

        headRow = self.insert('HeadendTransfer', headendParams)

        for i, txId in reversed(list(enumerate(sensorInfo['txId']))):

            stopFrame = sensorInfo['fromFrame'][i] + 1

            for j in range(stopFrame):
                # print(f"\nIn Relation loop, j is: {j}")
                relationParams['payloadId'].append(txId)
                relationParams['jumpId'].append(headRow - j)
            

        self.insert('PayloadToHeadend', relationParams)


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

        print(f"Params in Update is:")

        for i, key in enumerate(params):

            print(f"{params[key]}")

        sql = f"""
            UPDATE '{table}'
            SET """


        for i, key in enumerate(params['values']):

            if i>0:     # If not first column
                sql += ", "
            
            sql += f"{key} = {params['values'][key]}"



        for i, key in enumerate(params['where']):

            if i>0:     # If not first column
                sql += """ 
            AND """

            else:       # If first column
                sql += """
            WHERE """
        
            sql += f"""{key}={params['where'][key]}"""



        print(f"\nSQL Statement is:{sql}\n\n")
        self.cur.execute(sql)
        self.con.commit()

        # print(f"Inserted at row in {table} table: {self.cur.lastrowid}")

        return self.cur.lastrowid

    # def updateHeadend(self, data):



if __name__ == "__main__":
    
    db = Database("db.db3")


    ################################
    ##  --  Frame Building  --

    ############################
    ##  Sensor Frame (IP0)

    frame = "12.34" + SEP + "23.45" + SEP + "34.56" + OFF + "-98.76" + OFF + "-87.65" +  SEP + "Random Sensor Data"
    frame = "12.34" + SEP + "23.45" + SEP + "34.56" + OFF + "-98.76" + OFF + "-87.65" +  EON + "Random Sensor Data"
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


    # print(f"Simulated Headend Packet is: ")
    # frPrint(packet)

   
    ##  Second Headend Frame (Localhost)
    dataframe.setDataTime("78.90")
    dataframe.setTxTime("89.01")
    dataframe.setPostTxTime("90.12")
    dataframe.setPayload(packet)
    dataframe.setReceivedIP("10.31.0.13")
    dataframe.setPiggy("Ms.Piggy?")

    doubet = dataframe.buildHeadendFrame()

    print(f"Simulated Headend Packet is: ")
    frPrint(doubet)
    # print(doubet.replace(SEP, green(" | ")).replace(PB, blue(" | ")).replace(EON, magenta(" | ")))

    recvIP = "127.0.0.1"
    recvTime = "109.87"


    # unpack(packet, recvIP, recvTime)
    unpack(doubet, recvIP, recvTime)


