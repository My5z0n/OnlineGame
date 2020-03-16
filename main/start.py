from datetime import datetime
import socket  # Import socket module
import pickle
import time
from threading import Thread
import queue
import HOST
import game


def main():
    print("Main zyje!")
    s1 = queue.Queue()
    r1 = queue.Queue()
    s2 = queue.Queue()
    r2 = queue.Queue()
    t1 = Thread(target=HOST.start, args=(s1, r1, s2, r2))
    t1.start()

    control1 = queue.Queue()
    control2 = queue.Queue()
    t2 = Thread(target=game.game, args=(control1, control2))
    t2.start()
    while True:
        try:
            data = r1.get(block=False)
        except queue.Empty:
            continue
        new_contol = pickle.loads(data)
        control1.put(new_contol)


if __name__ == "__main__":
    main()
