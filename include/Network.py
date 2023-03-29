import socket 
import threading
from include.NetTechnology import NetTechnology

# The class that will handle all the networking tasks, such that we dont have to 
# repeat trivial connection commands multiple times throughout the report. 

type = "wifi"

REMOTESOCKADDR = ''
REMOTESOCKPORT = 12345

Message:str


class Network():
    data = {}                   # A variable to store the thread/sensor id and the data received by each thread
    lock = threading.Lock()     # A variable for locking data that can cause race conditions
    threads = list()            # A list for maintaining the list of threads  
    # A constructor, whose job is to create a socket, which is connected to the given interface. 
    receiveSock: socket.socket
    transmitSock: socket.socket


    def __init__(self, tech="wifi"):
        self.tech = tech
        pass
        

    
    def listener(self, addr, port):
        # This function is called at the headend, and backend. It main functions
        # is to handle all incoming connections from the sensors.  
        id = 0
        self.receiveSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # socket for receiving all incoming connections

        interface = NetTechnology(self.tech).getInterface() # call the NetTechnology class and get the interface name of the technology module
        self.receiveSock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode()) # set the socket to use this interface
        
        self.receiveSock.bind((addr, port))     # Bind the socket
        self.receiveSock.listen(3)              # Listens and wait for connections
        while True:
            
            print("socket is now listening.")

            conn, addr = self.receiveSock.accept()            # Accept all incoming connections. each connection is associated with a socket
                                                                        # and an Address    
            print("connected to: ", addr)
            
            new_thread = threading.Thread(name="receiving thread", target =self.receive, args=(conn,id))   # Create a thread, handling each connections, by calling the receive method. 
            self.threads.append(new_thread)
            self.data[id] = []
            new_thread.start()
            id = id + 1
            
        

            
       


    def receive(self, conn:socket.socket, threadID):
        #print("The thread for receiving data has been started ", threading.get_ident())
        while True:    
            sensorData = conn.recv(2048).decode()           # Receive incoming data. 
            if not sensorData == "":
                self.lock.acquire(blocking=True)            # Lock the following code, such that only one thread can access it. 
                self.data[threadID].append(sensorData)      # Write the received data from the thread to a variable shared by all the threads in this process. 
                self.lock.release()                         # Release the lock once the task above is finished. 
                print("The data dict: ", self.data)
            
                
                

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
        
        self.transmitSock.send(message.encode("utf8"))
        

    



