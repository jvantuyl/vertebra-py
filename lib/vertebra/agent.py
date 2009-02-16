from __future__ import with_statement
from threading import Thread,Condition
from actor import actor as actor_class
from logging import debug,info
from types import ModuleType,StringTypes

class agent(Thread):
  def __init__(self,actors=[],initop=None,idle="wait"):
    super(agent,self).__init__(
      target = self.main,
      kwargs={'actors':actors, 'initop':initop, 'idle':idle}
    )
    self.incalls = {}
    self.outcalls = {}
    self.jobs = []
    self.jobexit = Condition()
    self.actors = []
    debug("agent initialized")

  def main(self,actors,initop,idle):
    info("agent starting")
    self.run = True
    info("loading actors")
    self.load_actor('actor_core')
    self.load_actors(actors)
    with self.jobexit:
      if initop:
        info("running bootstrap operation: %r" % initop)
        self.start_job(initop)
      while 1:
        debug("main loop exit check")
        if not self.run:
          break
        if not self.jobs and idle == "exit":
          break
        self.jobexit.wait()
    if not self.run:
      debug("triggered exit")
    elif idle == "exit" and not self.jobs:
      debug("finished exit")
    info("agent terminating")

  def load_actor(self,actor):
    if isinstance(actor,ModuleType):
      for obj in dir(actor):
        obj = getattr(actor,obj,None)
        if isinstance(obj,actor_class):
          self.load_actor(obj)
    elif isinstance(actor,actor_class):
      info("loaded actor %r" % actor.__class__.__name__)
      self.actors.append(actor)
    elif isinstance(actor,StringTypes):
      self.load_actor(__import__(actor))
    else:
      raise NotImplementedError
      
  def load_actors(self,actors):
    for actor in actors:
      self.load_actor(actor)

  def start_job(self,op):
    from time import sleep
    sleep(5)
    with self.jobexit:
      self.jobexit.notifyAll()

if __name__ == '__main__':
  import logging

  logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
  Agent = agent(initop='blah',idle='exit')
  Agent.start()
  Agent.join()
