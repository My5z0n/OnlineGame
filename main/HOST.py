import _thread
import queue
import socket  # Import socket module
import pickle
from threading import Thread
from queue import Queue
HEADERSIZE= 10

# Klasa sluzy do obslugiwania nawiazanego polaczenia
class MySocket:
    def __init__(self, c, addr, tosend, toreceive):
        self.c = c
        self.addr = addr
        self.tosend = tosend
        self.toreceive = toreceive

    # obsluga wysylan
    def sending(self):
        while 1:
            data = self.c.recv(HEADERSIZE)
            datalen = int(data[:HEADERSIZE])
            data = self.c.recv(datalen)
            self.toreceive.put(data)

    # obsluga pobran danych
    def receiving(self):
        while 1:
            try:
                data = self.tosend.get(block=True)
                self.c.send(data)
            except queue.Empty:
                pass

    # Po odpaleniu watku najpierw pojdzie tutaj
    def run(self):
        # tworzymy watki do odbierania danych i ich wysylania
        t1 = _thread.start_new_thread(self.sending, ())
        t2 = _thread.start_new_thread(self.receiving, ())
        #t1.start()
        #t2.start()


def start(tosend1, toreceive1, tosend2, toreceive2):
    print("Start")
    # Uswatawianie połączenia
    s = socket.socket()  # Stworz socketa
    host = socket.gethostname()  # Weź nazwe swojej maszyny
    port = 12345  # Ustawiamy port
    s.bind((host, port))  # Bidnujemy port
    print("socket binded to port", port)

    # Odpal nasłuchwania
    s.listen(5)
    print("socket is listening")

    # Czekamy na klientów
    c, addr = s.accept()  # Czekaj tak dlugo az pojawi sie klient
    print('Connected to :', addr[0], ':', addr[1])
    # Ustawilismy polaczenie przekazujemy do innego watku ktory zaraz utworzymy by obslugiwal komunikacje
    # A my pojdziemy dalej
    x = MySocket(c, addr, tosend1, toreceive1)  # stworz obiekt klasy
    t1 = _thread.start_new_thread(x.run,())  # stworz watek
   # t1.start()  # odpal watek

    c, addr = s.accept()  # Robimy to samo tylko z 2 klientem
    print('Connected to :', addr[0], ':', addr[1])
    x = MySocket(c, addr, tosend2, toreceive2)
    t1 = _thread.start_new_thread(x.run,())
   #t1.start()