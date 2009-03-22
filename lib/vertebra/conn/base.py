"""
Base Connection for Vertebra
============================

This is the base all of Vertebra connections.
"""

import threading
from logging import debug,info,error
from time import sleep
from socket import error as socket_error
from backoff import exponential_backoff

class baseConnection(threading.Thread):
  def setup(self,config,deliver):
    self.config = config
    self.deliver = deliver

  def wake(self): # Called from Main Thread
    raise NotImplemented

  def run(self):
    while 1:
      try:
        self.connect()
        self.process()
      except Exception, e:
        info("Unhandled Error In Connection Processing: %s", e, exc_info=True)
        sleep(5.0)

  def connect(self):
    raise NotImplemented

  def process(self):
    raise NotImplemented

  def disconnected(self):
    pass

  def reconnected(self):
    pass

