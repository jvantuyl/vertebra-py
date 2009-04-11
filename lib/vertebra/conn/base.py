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
    self.crash_fatal = False

  def wake(self): # Called from Main Thread
    raise NotImplementedError()

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
        if self.handle_crash:
          break
        sleep(5.0)

  def handle_crash(self): # Returns True if crash is handled
    error('connection crashed in main loop')
    return self.crash_fatal

  def connect(self):
    raise NotImplementedError()

  def process(self):
    raise NotImplementedError()

