"""
Base Connection for Vertebra
============================

This is the base all of Vertebra connections.
"""

import threading
from logging import debug,info,error
from time import sleep
from socket import error as socket_error
from os import fdopen,pipe
from backoff import exponential_backoff

class baseConnection(threading.Thread):
  def __init__(self,deliver,name='connection'):
    self.deliver = deliver
    super(baseConnection,self).__init__(name=name)
    r,w = pipe()
    self.wake_recv,self.wake_send = fdopen(r,'r'), fdopen(w,'w')

  def wake(self): # Called from Main Thread
    debug("waking up connection")
    self.wake_send.write('W')
    self.wake_send.flush()

  def run(self):
    while 1:
      try:
        self.connect()
        self.process()
      except Exception,e:
        info("Unhandled Error In Connection Processing: %s", e, exc_info=e)
        sleep(5.0)

  def connect(self):
    raise NotImplemented

  def process(self):
    raise NotImplemented

  def disconnected(self):
    pass

  def reconnected(self):
    pass

