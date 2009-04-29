from select import select
from vertebra.util import StablePrioQueue,Full
from weakref import ref,WeakKeyDictionary,WeakValueDictionary
from logging import warn,error
from vertebra.scheduler.handler import Handler,NoopHandler
from vertebra.scheduler.task import TaskHandler,Task
from vertebra.scheduler.trigger import TriggerHandler,Trigger

class BaseScheduler(object):
  DEFAULT_PRIO = 100

  def __init__(self):
    self.active = StablePrioQueue()
    self.triggers = dict()
    nh = NoopHandler()
    bsh = BaseSentinelHandler()
    tah = TaskHandler()
    trh = TriggerHandler()
    self.handlers = [nh,bsh,tah,trh]

  def handle(self,task,ret):
    if type(ret) is list: # Lists are SPECIAL
      for ret in list:
        self.handle(task,ret)
    else:
      for handler in self.handlers:
        if isinstance(ret,handler.TYPES):
          try:
            if handler.handle(scheduler,task,ret):
              return
          except:
            warn("handler %s crashed handling %s from %s",
                 handler,ret,task,exc_info=True)
      warn("unhandled %s from %s",ret,task)
      return
    self.schedule(task)

  def schedule(self,task,who = None):
    if who is None: # This is Who Triggered The Task
      who = self # If unspecified, just give them the scheduler
    try:
      prio = task.prio
    except AttributeError:
      prio = self.DEFAULT_PRIO
    self.active.put_nowait(prio, (who,task,) )

  def run_active(self):
    if not self.active.empty():
      (prio,(who,task,)) = self.active.get()
      try:
        ret = task.iterate(scheduler,who)
      except Exception, e:
        ret = e
      self.handle(task,ret)
      return True
    else:
      return False

  def process_triggers(self):
    woken = False
    for trigger in self.triggers.keys():
      if trigger.ready(self):
        self.wake_sleeping(trigger)
        woken = True
    return woken

  def wake_sleeping(self,trigger):
    try:
      T = self.triggers[trigger]
      while 1:
        try:
          sleeping_task = T[0]
        except IndexError:
          del self.triggers[trigger]
          break
        self.schedule(task,trigger)
        del T[0]
    except Full:
      pass # Queue Got Full, Try The Rest Next Time

  def loop(self):
    try:
      while 1:
        while self.process_triggers():
          while self.run_active():
            pass
        self.idle()
    except StopIteration:
      # Time to stop
      return

  def idle(self):
    raise NotImplementedError()

  def wake(self): # With No Idle Function, This Does Nothing
    pass

class BusyScheduler(BaseScheduler):
  def idle(self):
    if self.triggers:
      raise RuntimeError("Busy-Scheduler Went Idle With Work, Uh-Oh")
    else:
      raise StopIteration()
