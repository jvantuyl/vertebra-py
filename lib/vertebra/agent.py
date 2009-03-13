from __future__ import with_statement
from threading import Thread,Condition
from job import job
from logging import debug,info,warn
from types import ModuleType,StringTypes
import fibra
import fibra.handlers.sleep
import time
from sys import exit

# HACK HACK HACK
fibra.handlers.sleep.time_func = time.time

class agent(Thread):
  def __init__(self,actors=[],idle="wait"):
    if isinstance(actors,StringTypes): # Catch strings here
      actors = [actors]
    super(agent,self).__init__(
      target = self.main,
      kwargs={'actors':actors, 'idle':idle}
    )
    self.incalls = {}
    self.outcalls = {}
    self.jobs = []
    self.jobexit = Condition()
    self.actors = []
    self.sched = fibra.schedule()
    debug("agent initialized")

  def main(self,actors,idle):
    sched = self.sched
    info("agent starting")
    sched.install(self.idle())
    sched.install(self.recv())
    sched.install(self.xmit())
    info("loading actors")
    self.load_actor('actor_core')
    for actor in actors:
      try:
        self.load_actor(actor)
      except :
        warn("unable to load %s",actor,exc_info=True)
    info("agent operational")
    self.sched.run()
    info("agent terminating")

  def idle(self): # Puts the agent to sleep when there's nothing to be done
    from time import sleep # FIXME: get this fixed in Fibra
    ready = True
    while 1:
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

  def load_actor(self,actor):
    debug("Trying to load actor %s" % actor)
    if isinstance(actor,ModuleType):
      actor.load(self) # Ask the actor module to load itself into this agent
    elif isinstance(actor,StringTypes):
      self.load_actor(__import__(actor))
    else:
      raise NotImplementedError     

  def do_exit(self):
    exit(1)
    yield None

  def stop(self):
    debug("start shutdown")
    self.sched.install(self.do_exit())

if __name__ == '__main__':
  import logging

  logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
  Agent = agent(actors=['opstub'],idle='exit')
  Agent.start()
  try:
    while 1:
      Agent.join(0.05)
  except KeyboardInterrupt:
    Agent.stop()
  except:
    Agent.stop()
    raise
