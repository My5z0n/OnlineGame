import _thread as th
import queue
from collections import deque


class MyQueue:
    def __init__(self):
        self.q = deque()
        self.lock= th.allocate_lock()

    def get(self,block=False):
        data=None
        if not block:
            if self.lock.acquire(blocking=block):
                if len(self.q) !=0:
                    data = self.q.popleft()
                self.lock.release()
            if data is not None:
                return data
            else:
                raise queue.Empty
        else:
            self.lock.acquire(blocking=block)
            if len(self.q) != 0:
                data = self.q.popleft()
            self.lock.release()
            if data is not None:
                return data
            else:
                raise queue.Empty

    def put(self,data,block=False):
        self.lock.acquire(blocking=True)
        self.q.append(data)
        self.lock.release()

