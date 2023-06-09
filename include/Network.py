import socket 
import threading
from include.NetTechnology import NetTechnology
from include.ProcessData import EOT
from time import time
from queue import Queue

# The class that will handle all the networking tasks, such that we dont have to 
# repeat trivial connection commands multiple times throughout the report. 

REMOTESOCKADDR = ''
REMOTESOCKPORT = 12345

Message:str


class Network():
    data:Queue[dict[str, str]] = Queue()    # A variable to store the thread/sensor id and the data received by each thread
    lock = threading.Lock()                         # A variable for locking data that can cause race conditions
    threads:list[tuple[threading.Thread, socket.socket]] = []             # A list for maintaining the list of threads  
    # A constructor, whose job is to create a socket, which is connected to the given interface. 
    receiveSock: socket.socket = None
    transmitSock: socket.socket = None
    isClosed = False
    running:bool = True


    def __init__(self, tech="wifi"):
        self.tech = tech
        pass
        

    
    def listener(self, port):
        # This function is called at the headend, and backend. It main functions
        # is to handle all incoming connections from the sensors.
        addr = ""
        self.receiveSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # socket for receiving all incoming connections

        interface = NetTechnology(self.tech).getInterface() # call the NetTechnology class and get the interface name of the technology module
        self.receiveSock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode()) # set the socket to use this interface
        
        self.receiveSock.bind((addr, port))     # Bind the socket
        self.receiveSock.listen()               # Listens and wait for connections

        while True:
            conn, id = self.receiveSock.accept()            # Accept all incoming connections. each connection is associated with a socket and an Address   


            #print("Transmission Received")

            new_thread = threading.Thread(name="receiving thread", target =self.receive, args=(conn,id[0]), daemon=True)   # Create a thread, handling each connections, by calling the receive method. 
            self.threads.append((new_thread, conn))
            new_thread.start()
            
    def receive(self, conn:socket.socket, threadID):
        frame = ""
        #print("The thread for receiving data has been started ", threading.get_ident())
        while self.running:    
            sensorData = conn.recv(2048).decode()           # Receive incoming data. 
            recvTime = time()
            readyCount = sensorData.count(EOT)
            for partition in sensorData.split(EOT):
                if not partition == "":
                    print(partition)
                    frame += partition
                    if readyCount > 0:
                        self.data.put({"recvTime":recvTime, "data":frame, "id":threadID})
                        frame = ""
                        readyCount -= 1
                else:
                    self.threads.remove((threading.current_thread(), conn))
                    return                                            # catch keyboardinterrupts to shut down socket elegantly
            
    def popData(self) -> dict:
        return self.data.get()
            
                
                

    # This method will establish the connection between client socket and server socket. 
    def connect(self, addr, port):
        self.transmitSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # creating the socket for transmitting data

        interface = NetTechnology(self.tech).getInterface() # use the NetTechnology to get the network enterface of the technology
        self.transmitSock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode()) # set the socket option such that the socket uses the specified technology

        self.port = port        # Set the port number given as a parameter
        self.addr = addr        # Set the address given as a paramater
        self.transmitSock.connect((self.addr, self.port))   # connect to the socket bounded on the given address and port. 
        #self.message = message  # Set the message for transmission to the one given as a parameter. 

        #self.transmit(self.transmitSock, self.message)  # transmit the shit!



    def transmit(self, message:str):
        try:
            self.transmitSock.sendall(message.encode("utf8"))
        except:
            self.close()
        
    def close(self):
        self.running = False
        if self.receiveSock is not None: 
            self.receiveSock.close()
        if self.transmitSock is not None:
            self.transmitSock.close()
    



