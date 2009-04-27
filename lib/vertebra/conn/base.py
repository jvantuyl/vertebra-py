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
from weakref import WeakValueDictionary

class baseConnection(object):

  class codec(object):
    def marshall(self,msg):
      raise NotImplementedError()

    def unmarshall(self,rawmsg):
      raise NotImplementedError()

  class identity(object): # Identity Factory Class
    def __new__(self,cls):
      raise NotImplementedError()

  def setup(self,config,name='Connection'):
    self.config = config
    self.crash_fatal = False
    self.router = None

  def idle(self):
    raise NotImplementedError()

  def start(self):
    raise NotImplementedError()

  def stop(self,wait=True):
    raise NotImplementedError()

  def accept_ident(self,ident):
    return isinstance(ident,self.identity)

  def handle_crash(self,e): # Returns True if crash is handled
    error("Unhandled Error In Connection Processing: %s", e, exc_info=True)
    is_handled = not self.crash_fatal
    return is_handled

  def connect(self):
    raise NotImplementedError()

  def process(self):
    raise NotImplementedError()

  def recv(self,rawmsg):
    try:
      u = self.codec.unmarshall(rawmsg)
    except MarshalError:
      warn("failed to unmarshall raw message %s",rawmsg,exc_info=True)
    else:
      r = self.router
      if r is not None:
        r.recv(u)

  def send(self,msg):
    try:
      m = self.codec.marshall(msg)
    except MarshalError:
      error("failed to marshall message %s",msg,exc_info=True)
    else:
      c = self.client
      if c is not None:
        c.send(m)

class threadedConnection(baseConnection):
  def setup(self,config,name="ThreadedConnection"):
    super(threadedConnection,self).setup(config,name)
    self.thread = Thread(target=self.run,name=name)
    self.keep_running = True

  def join(self,*args,**kwargs):
    self.thread.join(*args,**kwargs)

  def run(self):
    raise NotImplementedError()

  def start(self):
    self.thread.start()
    return True

  def wake(self):
    return True

  def stop(self,wait=True): # API, runs outside of thread
    self.keep_running = False
    self.wake()
    if wait and not self.thread.isDaemon() and currentThread() != self.thread:
      self.join()
    return True
