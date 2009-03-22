"""
XMPP Connection for Vertebra
============================

This XMPP connection runs as another thread.  In this thread, it will run in a
loop, handling XMPP processing.

Like all connections, it has to be given a thread-safe "receive" method, which
will be called in its thread, and it has a thread-safe "transmit" method.
"""

import threading
import pyxmpp.all
from logging import debug,info,error
from time import sleep
from socket import error as socket_error
from random import random
from os import fdopen,pipe
try:
  from Queue import Queue,Empty
except ImportError:
  from queue import Queue,Empty

CS = pyxmpp.all.ClientStream

class vxClientStream(CS):
  def __init__(self,*args,**kwargs):
    CS.__init__(self,*args,**kwargs)
    self.outstanding = Queue()
    r,w = pipe()
    self.wake_recv,self.wake_send = fdopen(r,'r'), fdopen(w,'w')
    
  def wake(self):
    self.wake_send.write('W')
    self.wake_send.flush()

  def woke(self):
    # Clear Byte That Woke Us Up
    self.wake_recv.read(1)
    try:
      while 1:
        stanza = self.outstanding.get(False)
        self.send(stanza)
    except Empty:
      pass
    
  def _loop_iter(self,timeout):
    """Same as `Stream.loop_iter` but assume `self.lock` is acquired."""
    from select import select,error
    self.lock.release()
    try:
      socket = self.socket
      wait_pipe = self.wake_recv
      try:
        ifd, _unused, efd = select( [socket,wait_pipe],
                                    [], 
                                    [socket,wait_pipe],
                                    timeout )
      except error,e:
        if e.args[0]!=errno.EINTR:
          raise
        ifd, _unused, efd=[], [], []
    finally:
        self.lock.acquire()
    debug("selected: %r, %r" % (ifd, efd))
    if wait_pipe in ifd or wait_pipe in efd:
      self.woke()
    if socket in ifd or socket in efd:
      self._process()
      return True
    else:
      return False

class vxClient(pyxmpp.all.Client):
  def __init__(self,*args,**kwargs):
    pyxmpp.all.Client.__init__(self,*args,**kwargs) #Client is old-style class
    self.stream_class = vxClientStream # Use Our Modified Stream Class

  def wake(self):
    if self.stream:
      self.stream.wake()
      
  def send(self,iq):
    if self.stream:
      self.stream.outstanding.put(iq)
      self.stream.wake()