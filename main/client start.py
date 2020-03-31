import _pickle
import pickle
import time
from threading import Thread
import queue
import CLIENT
import user_input

HEADERSIZE= 10

s1 = queue.Queue()
r1 = queue.Queue()
t1 = Thread(target=CLIENT.start, args=(s1, r1))
t1.start()

nowa = queue.Queue()
nowa2 = queue.Queue()

hostdata = queue.Queue()
t2 = Thread(target=user_input.game2, args=(nowa, nowa2,hostdata))
t2.start()
while True:
    try:
        data = nowa.get(block=False)
        binary = pickle.dumps(data)
        binary = bytes(f"{len(binary):<{HEADERSIZE}}", 'utf-8') + binary
        s1.put(binary)
    except queue.Empty:
        pass
    try:
        data = r1.get(block=False)
        array = pickle.loads(data)
        hostdata.put(array)
    except queue.Empty:
        pass



