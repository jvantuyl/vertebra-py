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

class vxClientStream(pyxmpp.all.ClientStream):
  def _loop_iter(self,timeout):
    """Same as `Stream.loop_iter` but assume `self.lock` is acquired."""
    from select import select,error
    self.lock.release()
    try:
      socket = self.socket
      wait_pipe = self.owner.wait_pipe
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
      wait_pipe.read(1)
    if socket in ifd or socket in efd:
      self._process()
      return True
    else:
      return False

class vxClient(pyxmpp.all.Client):
  def __init__(self,*args,**kwargs):
    wait_pipe = kwargs.pop('wait_pipe')
    pyxmpp.all.Client.__init__(self,*args,**kwargs) #Client is old-style class
    self.wait_pipe = wait_pipe
    self.stream_class = vxClientStream # Use Our Modified Stream Class

