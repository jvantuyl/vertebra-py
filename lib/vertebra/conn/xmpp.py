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
from os import fdopen,pipe
from backoff import exponential_backoff
from vertebra.conn.vxmpp import vxClient
from base import baseConnection

IDLE_INTERVAL=0.25

class xmppConnection(baseConnection):
  def __init__(self):
    super(xmppConnection,self).__init__(name="xmpp_connection")
    self.setDaemon(True) # This Connection Can Tolerate Not Being Cleaned Up

  def setup(self,config,deliver):
    super(xmppConnection,self).setup(config,deliver)

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

  def wake(self):
    debug("waking up connection")
    if self.client:
      self.client.wake()

  def resetBackoff(self):
    self.backoff = exponential_backoff(0.4,30.0,2.0)

  def run(self):
    while 1:
      try:
        self.connect()
        self.process()
      except Exception, e:
        info("Unhandled Error In XMPP Processing: %s", e, exc_info=True)
        sleep(5.0)

  def connect(self):
    # Assume we're not connected
    kw = {}

    if self.server:
      kw['server'] = self.server

    client = vxClient(jid=self.jid,password=self.password,**kw)
    client.connect()
    debug("Connection Established")
    self.client = client

  def send(self,msg):
    # FIXME: Marshalling anyone?
    if self.client:
      self.client.send(msg)
      
  def disconnected(self):
    # FIXME: What do we have to clean up here?  Anything?
    pass

  def reconnected(self):
    # FIXME: What do we have to do here?  Should we retransmit outstanding?
    pass

  def process(self):
    debug("start processing")
    self.client.loop()
    debug("done processing")

if __name__ == '__main__':
  from getpass import getpass
  import logging

  def printer(it):
    print repr(it)

  jid = raw_input("Jabber ID: ")
  pwd = getpass("Password: ")
  svr = raw_input("Server (or enter to use default): ")
  jid = jid.strip()
  if not svr.strip():
    svr = svr.strip()

  logging.basicConfig(level=logging.DEBUG)

  conn = xmppConnection(jid=jid,password=pwd,server=svr,deliver=printer)
  conn.start()

  while 1: # This allows a KeyboardInterrupt to be processed even though we're in a thread
    conn.wake()
    conn.join(5.0)

