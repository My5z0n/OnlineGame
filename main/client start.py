import _pickle
import pickle
import time
from threading import Thread
import queue
import _thread
import CLIENT
import user_input
from MyQueue import MyQueue

HEADERSIZE= 10

s1 = MyQueue()
r1 = MyQueue()
t1 = _thread.start_new_thread(CLIENT.start,(s1, r1))
#t1.start()

nowa = MyQueue()
nowa2 = MyQueue()

hostdata = MyQueue()
t2 = _thread.start_new_thread(user_input.game2, (nowa, nowa2,hostdata))
#t2.start()
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



