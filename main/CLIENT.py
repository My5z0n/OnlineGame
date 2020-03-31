import socket  # Import socket module
import pickle
from threading import Thread
from queue import Queue
HEADERSIZE= 10

class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, c, addr, tosend, toreceive):
        self.c = c
        self.addr = addr
        self.tosend = tosend
        self.toreceive = toreceive

    def sending(self):
        while 1:
            data = self.c.recv(HEADERSIZE)
            datalen = int(data[:HEADERSIZE])
            data = self.c.recv(datalen)
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


def start(tosend1, toreceive1):
    # local host IP '127.0.0.1'
    host = socket.gethostname()

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))
    x = MySocket(s, host, tosend1, toreceive1)
    t1 = Thread(target=x.run)
    t1.start()