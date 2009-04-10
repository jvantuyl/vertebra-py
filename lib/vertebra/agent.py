from __future__ import with_statement
from threading import Thread,Condition
from vertebra.job import job
from vertebra.config import config
from logging import debug,info,warn
from types import ModuleType,StringTypes
import fibra
import fibra.handlers.sleep
import time
from sys import argv,exit

# HACK HACK HACK
fibra.handlers.sleep.time_func = time.time

class base_agent(object):
  """Base Implementation and Interface for Vertebra Agent"""
  # Interface
  def setup(self,config,connection): raise NotImplementedError
  def start(self): raise NotImplementedError
  def stop(self): raise NotImplementedError

  # Implementation
  def load_actor(self,actor):
    debug("Trying to load actor %r" % actor)
    if isinstance(actor,ModuleType):
      actor.load(self) # Ask the actor module to load itself into this agent
    elif isinstance(actor,StringTypes):
      mod = __import__(name='vertebra.actors.' + actor,fromlist=['load'])
      debug('Imported %s as %r',actor,mod)
      self.load_actor(mod)
    else:
      raise NotImplementedError

class agent(base_agent):
  """Vertebra Agent Implementation"""
  def __init__(self):
    super(agent,self).__init__()
    self.thread = Thread(target = self.main)
    self.config = config
    self.incalls = {}
    self.outcalls = {}
    self.jobs = []
    self.actors = []
    self.setupped = False

  def setup(self,config,connection):
    self.thread.setDaemon(True)
    self.config = config
    self.conn = connection
    self.setupped = True
    debug("agent initialized")

  def main(self):
    assert self.setupped

    # Set Up Scheduler
    sched = fibra.schedule()
    self.sched = sched

    # Initialize Tasklets
    info("agent starting")
    sched.install(self.idle())
    sched.install(self.recv())
    sched.install(self.xmit())

    # Load Actors
    info("loading actors")
    for actor in ['actor_core'] + self.config['agent.actors']:
      try:
        self.load_actor(actor)
      except :
        warn("unable to load %s",actor,exc_info=True)

    # Start Connection
    self.conn.start()

    # Run
    info("agent operational")
    self.sched.run()
    info("agent terminating")

  def idle(self): # Puts the agent to sleep when there's nothing to be done
    from time import sleep
    ready = True
    while 1: # FIXME: Exit based on agent.idle
      yield 0.0
      sleep(0.05) # For now, punt by just sleeping a bit

  def recv(self): # Receive Threadlet
    info("recv: handler started")
    while 1:
      yield 1.0
      debug("recv: processing")

  def xmit(self): # Transmit Threadlet
    info("xmit: handler started")
    while 1:
      yield 1.0
      debug("xmit: processing")
      self.conn.wake()

  def do_exit(self):
    yield exit(1)

  def start(self):
    self.thread.start()

  def join(self,*args,**kwargs):
    self.thread.join(*args,**kwargs)

  def stop(self):
    debug("start shutdown")
    self.sched.install(self.do_exit()) # FIXME: Is this threadsafe?

class mock_agent(base_agent):
  """Mock Agent for Testing"""
  def setup(self,config,connection):
    self.config = config
    self.connection = connection

  def start(self): pass
  def stop(self): pass
