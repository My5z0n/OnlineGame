from datetime import datetime
import socket  # Import socket module
import pickle
import time
from threading import Thread
import _thread
import queue
import HOST
import game
from MyQueue import MyQueue

HEADERSIZE = 10


# Glowna klasa odpowiedzialna za zarzadzanie cala reszta
def main():
    print("Main zyje!")
    # Tworzymy kolejki ktore beda synchronizowaly nasze watki i pozwala nam na komunikacje miedzy nimi
    # s1 r1 - wyslanie/pobranie dla klienta 1
    # s1 r1 - wyslanie/pobranie dla klienta 2
    s1 = MyQueue()
    r1 = MyQueue()
    s2 = MyQueue()
    r2 = MyQueue()

    # odpalamy watki odpowiadajace za komunikacje
    t1 = _thread.start_new_thread(HOST.start, (s1, r1, s2, r2))

    # tworzymy dodatkowe 2 kolejki tym razem do komunikacji bezposiernio z gra
    control1 = MyQueue()
    control2 = MyQueue()
    # do tej kolejki bedzie trafialo wyjscie z serwera
    output = MyQueue()
    # odpalamy gre
    t2 = _thread.start_new_thread(game.game, (control1, control2, output))

    # ponizej sprawdzamy czy w kolejce pojawily sie jakies odebrane dane jesli tak dekodujemy je i wysylamy dalej
    while True:
        try:
            data = r1.get(block=False)  # sprawdzamy czy klient 1 coś wysłał
            new_control = pickle.loads(data)
            control1.put(new_control)  # wstawiamy dane z klienta 1 do kolejki gry
        except queue.Empty:
            pass
        try:
            data = r2.get(block=False)  # sprawdzamy czy klient 2 coś wysłał
            new_control = pickle.loads(data)
            control2.put(new_control)  # wstawiamy dane z klienta 2 do kolejki gry
        except queue.Empty:
            pass
        try:
            data = output.get(block=False)  # sprawdzamy kolejke gry
            binary = pickle.dumps(data)
            binary = bytes(f"{len(binary):<{HEADERSIZE}}", 'utf-8') + binary
            s1.put(binary)  # wysyłamy do klienta 1
            s2.put(binary)  # wysyłamy do klienta 2
        except queue.Empty:
            pass


if __name__ == "__main__":
    main()
