from __future__ import with_statement
from threading import Lock
from Queue import PriorityQueue,Empty,Full
from heapq import heappush, heappop

__all__ = ['StablePrioQueue','Empty','Full']

class StablePrioQueue:
  def __init__(self, maxsize = 0):
    self.c_lock = Lock()
    self.ctr = 0
    pq = PriorityQueue(maxsize)
    self.pq = pq
    self.qsize = pq.qsize
    self.full = pq.full
    self.get_nowait = pq.get_nowait
    self.task_done = pq.task_done
    self.join = pq.join

  def get(self,block=True,timeout=None):
    item = self.pq.get(block,timeout)
    return item[0],item[2]

  def put(self,key,val,block=True,timeout=None):
    with self.c_lock:
      item = (key,self.ctr,val)
      self.ctr += 1
    return self.pq.put(item,block,timeout)

  def put_nowait(self,key,val):
    return self.put(key,val,False)

  def empty(self):
    e = self.pq.empty()
    if e:
      with self.c_lock:
        self.ctr = 0
    return e
