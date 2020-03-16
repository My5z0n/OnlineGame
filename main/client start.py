import pickle
import time
from threading import Thread
import queue
import CLIENT
import user_input

s1 = queue.Queue()
r1 = queue.Queue()
t1 = Thread(target=CLIENT.start, args=(s1, r1))
t1.start()

nowa = queue.Queue()
nowa2 = queue.Queue()
t2 = Thread(target=user_input.game2, args=(nowa, nowa2))
t2.start()
while True:
    try:
        data = nowa.get(block=False)
    except queue.Empty:
        continue
    binary = pickle.dumps(data)
    s1.put(binary)
