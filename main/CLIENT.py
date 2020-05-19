import _thread
import queue
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
            try:
                data = self.tosend.get()
                self.c.send(data)
            except queue.Empty:
                pass

    def run(self):
        t1 = _thread.start_new_thread(self.sending, ())
        t2 = _thread.start_new_thread(self.receiving, ())



def start(tosend1, toreceive1):
    # local host IP '127.0.0.1'
    host = socket.gethostname()

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))
    x = MySocket(s, host, tosend1, toreceive1)
    t1 = _thread.start_new_thread(x.run,())
