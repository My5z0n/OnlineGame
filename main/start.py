from datetime import datetime
import socket  # Import socket module
import pickle
import time
from threading import Thread
import queue
import HOST
import game


#Glowna klasa odpowiedzialna za zarzadzanie cala reszta
def main():
    print("Main zyje!")
    # Tworzymy kolejki ktore beda synchronizowaly nasze watki i pozwala nam na komunikacje miedzy nimi
    # s1 r1 - wyslanie/pobranie dla klienta 1
    # s1 r1 - wyslanie/pobranie dla klienta 2
    s1 = queue.Queue()
    r1 = queue.Queue()
    s2 = queue.Queue()
    r2 = queue.Queue()

    #odpalamy watki odpowiadajace za komunikacje
    t1 = Thread(target=HOST.start, args=(s1, r1, s2, r2))
    t1.start()

    #tworzymy dodatkowe 2 kolejki tym razem do komunikacji bezposiernio z gra
    control1 = queue.Queue()
    control2 = queue.Queue()
    #odpalamy gre
    t2 = Thread(target=game.game, args=(control1, control2))
    t2.start()
    #ponizej sprawdzamy czy w kolejce pojawily sie jakies odebrane dane jesli tak dekodujemy je i wysylamy dalej
    while True:
        try:
            data = r1.get(block=False)
            new_contol = pickle.loads(data)
            control1.put(new_contol)
        except queue.Empty:
            pass
        try:
            data = r2.get(block=False)
            new_contol = pickle.loads(data)
            control2.put(new_contol)
        except queue.Empty:
            pass


if __name__ == "__main__":
    main()
