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
from pyxmpp.interface import implements
from pyxmpp.interfaces import IStanzaHandlersProvider,IFeaturesProvider
from logging import debug,info,error
from time import time,sleep
from socket import error as socket_error
from os import fdopen,pipe
from vertebra.conn import router
from vertebra.conn.base import threadedConnection
from vertebra.conn.backoff import exponential_backoff
from vertebra.conn.local import localConnection
from vertebra.conn.xmpp.client import vxClient
from vertebra.conn.xmpp.marshall import registry as codec
from vertebra.util import atom

VERTEBRA_NS = ('vertebra','http://xmlschema.engineyard.com/agent/0.5')
IDLE_INTERVAL=0.25
SUCCESS_TIME=5.0 # seconds of connectivity sufficient to reset backoff

class xmppConnection(threadedConnection):
  implements(IStanzaHandlersProvider,IFeaturesProvider)

  codec = codec

  def get_iq_get_handlers(self):
    return [VERTEBRA_NS + (self.recv,)]

  def get_iq_set_handlers(self):
    return [VERTEBRA_NS + (self.recv,)]

  def get_message_handlers(self):
    return []

  def get_presence_handlers(self):
    return [('available',self.sink,)]

  def get_features(self):
    return []

  class identity(atom):
    def __str__(self):
      return self._symname

  def setup(self,config):
    super(xmppConnection,self).setup(config)

    self.jid = pyxmpp.all.JID(config['conn.xmpp.jid'])
    try:
      self.server = config['conn.xmpp.server']
    except KeyError:
      self.server = None
    if not self.jid.resource:
      self.jid = pyxmpp.all.JID(jid + '/vertebra-debug')
    self.password = config['conn.xmpp.passwd']

    self.client = None
    self.resetBackoff()

  def localIdentities(self):
    return [self.identity(self.jid)]

  def wake(self):
    debug("waking up connection")
    if self.client:
      self.client.wake()

  def resetBackoff(self):
    self.backoff = exponential_backoff(0.4,30.0,2.0)

  def run(self):
    delay = 0.0
    while self.keep_running:
      sleep(delay)

      try:
        info("xmpp connecting")
        if self.connect():
          info("xmpp connected")
          tick = time()
          self.process()
          if time() - tick >= SUCCESS_TIME:
            self.resetBackoff()
      except (socket_error,pyxmpp.all.FatalStreamError), e:
        error("Error in XMPP processing: %s",e,exc_info=True)
        # TODO: Should we catch getting booted off to better handle when two
        # agents are knocking each other off?
      except Exception, e:
        error("Unhandled Error In XMPP Processing: %s", e, exc_info=True)
        raise # TODO: Is this right?

      if not self.keep_running: # This check prevents spurious backoff logs
        break

      delay = self.backoff.next()

  def connect(self):
    # Assume we're not connected
    kw = {}

    if self.server:
      kw['server'] = self.server

    client = vxClient(jid=self.jid,password=self.password,keepalive=15,**kw)
    client.interface_providers.append(self)

    try:
      client.connect()
    except socket_error:
      debug("Socket Error Establishing Connection")
      return False
    debug("Connection Established")
    self.client = client

    return True

  def process(self):
    debug("start processing")
    self.client.loop(conn=self,timeout=10)
    debug("done processing")

  def __repr__(self):
    return u'<xmpp %s>' % self.jid.as_utf8()
