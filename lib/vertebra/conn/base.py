"""
Base Connection for Vertebra
============================

This is the base all of Vertebra connections.
"""

from threading import Thread,currentThread
from logging import debug,info,error
from time import sleep
from socket import error as socket_error
from backoff import exponential_backoff

class baseConnection(object):
  def setup(self,config,deliver,name='Connection'):
    self.config = config
    self.deliver = deliver
    self.thread = Thread(target=self.run,name=name)
    self.keep_running = True

  def wake(self): # Called from Main Thread
    raise NotImplemented

  def start(self):
    self.thread.start()

  def stop(self):
    self.keep_running = False
    self.wake()
    if not (self.thread.isDaemon() or currentThread() == self.thread):
      self.join()

  def join(self,*args,**kwargs):
    self.thread.join(*args,**kwargs)

  def run(self):
    while self.keep_running:
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

