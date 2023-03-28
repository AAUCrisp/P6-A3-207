import socket 
import threading
import netifaces as ni

interface = "wlp7s0"
# The class that will handle all the networking tasks, such that we dont have to 
# repeat trivial connection commands multiple times throughout the report. 

REMOTESOCKADDR = ''
REMOTESOCKPORT = 12345

class Network():
   
    # A constructor, whose job is to create a socket, which is connected to the given interface. 
    def __init__(self):
        pass
        

    
    def listener(self, addr, port):
        self.receiveSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiveSock.bind((addr, port))
        self.receiveSock.listen(2)
        while True:
            """Accepts a connection request and stores two parameters, conn which is a socket
             object for the connected user, and addr which contains the IP address
             if the client that just connected"""
            self.conn, self.addr = self.receiveSock.accept()

            print("connected to: ", self.addr)

            """Need to start a thread for the connected client, that will recieve
            all the information send by them."""

            new_thread = threading.Thread(name="receiving thread", target =self.receive, args=(self.conn,))
            new_thread.start()


            #start_new_thread(self.receive,(self.conn))

    def receive(self, conn):
        while True:
            sensorData = conn.recv(2048).decode()
            if sensorData:
                print("Sensor data received: ", sensorData)
                

    # This method will establish the connection between client socket and server socket. 
    def connect(self, addr, port):
        self.transmitSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.port = port
        self.addr = addr
        self.transmitSock.connect((self.addr, self.port))

        message = "Give me data!"

        self.transmit(self.transmitSock, message)

      
    
   



    def transmit(self,sock, message):
        self.sock = sock
        self.message = message
        self.sock.sendall(message.encode("utf8"))
        

    



