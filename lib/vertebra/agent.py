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
from imp import find_module,load_module

# HACK HACK HACK
fibra.handlers.sleep.time_func = time.time

ACTORBASEPREFIX = 'vertebra.actors.'
import vertebra.actors as ACTORBASEMOD

class base_agent(object):
  """Base Implementation and Interface for Vertebra Agent"""
  # Interface
  def setup(self,config,router):
    self.config = config
    self.router = router

  def start(self): raise NotImplementedError
  def stop(self): raise NotImplementedError

  # Implementation
  def load_actor(self,actor):
    debug("Trying to load actor %r" % actor)
    if isinstance(actor,ModuleType):
      actor.load(self) # Ask the actor module to load itself into this agent
    elif isinstance(actor,StringTypes):
      try:
        modinfo = find_module(actor,self.config['agent.path'])
      except ImportError:
        modinfo = None
      if modinfo is not None:
        modname = ACTORBASEPREFIX + actor
        mod = load_module(modname,*modinfo)
        setattr(ACTORBASEMOD,actor,mod)
      else:
        mod = __import__(name=ACTORBASEPREFIX + actor,fromlist=['load'])
      debug('Imported %s as %r',actor,mod)
      info("loaded actor %s" % actor)
      self.load_actor(mod)
    else:
      raise NotImplementedError

  def recv(self,msg):
    warn("can't handle message: %r" % msg)

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

  def setup(self,config,router):
    super(agent,self).setup(config,router)
    self.thread.setDaemon(True)
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
    sched.install(self.xmit())

    # Load Actors
    info("loading actors")
    for actor in ['actor_core'] + self.config['agent.actors']:
      try:
        self.load_actor(actor)
      except:
        warn("unable to load %s",actor,exc_info=True)
    info("done loading actors")

    # Start Communications
    self.router.start()

    # Run
    try:
      info("agent operational")
      self.sched.run()
      info("agent terminating")
    finally:
      # Shut Down Communications
      self.router.stop()

  def idle(self): # Puts the agent to sleep when there's nothing to be done
    from time import sleep
    ready = True
    while 1: # FIXME: Exit based on agent.idle
      yield 0.00
      sleep(0.03) # For now, punt by just sleeping a bit

  def xmit(self): # Transmit Threadlet
    info("xmit: handler started")
    while 1:
      yield 5.0
      debug("xmit: processing")

  def do_exit(self):
    yield exit(1)

  def start(self):
    self.thread.start()

  def join(self,*args,**kwargs):
    self.thread.join(*args,**kwargs)

  def stop(self):
    debug("start shutdown")
    self.sched.install(self.do_exit()) # FIXME: Is this threadsafe?

