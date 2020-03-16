import socket  # Import socket module
import pickle
from threading import Thread
from queue import Queue


class MySocket:
    def __init__(self, c, addr, tosend, toreceive):
        self.c = c
        self.addr = addr
        self.tosend = tosend
        self.toreceive = toreceive

    def sending(self):
        while 1:
            data = self.c.recv(8192)
            self.toreceive.put(data)

    def receiving(self):
        while 1:
            data = self.tosend.get()
            self.c.send(data)

    def run(self):
        t1 = Thread(target=self.sending, args=())
        t2 = Thread(target=self.receiving, args=())
        t1.start()
        t2.start()


def start(tosend1, toreceive1,tosend2, toreceive2):
    print("Start")
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port
    print("socket binded to port", port)

    s.listen(5)
    print("socket is listening")

    # Now wait for client connection.
    c, addr = s.accept()  # Establish connection with client.
    print('Connected to :', addr[0], ':', addr[1])
    x = MySocket(c, addr, tosend1, toreceive1)
    t1 = Thread(target=x.run)
    t1.start()
    c, addr = s.accept()  # Establish connection with client.
    print('Connected to :', addr[0], ':', addr[1])
    x = MySocket(c, addr, tosend2, toreceive2)
    t1 = Thread(target=x.run)
    t1.start()
