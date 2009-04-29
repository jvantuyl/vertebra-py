from select import select
from vertebra.util import StablePrioQueue,Full,Empty
from weakref import ref,WeakKeyDictionary,WeakValueDictionary
from logging import warn,error,debug
from vertebra.scheduler.sentinel import BaseSentinelHandler
from vertebra.scheduler.handler import Handler,NoneHandler,ExceptionHandler
from vertebra.scheduler.task import TaskHandler,Task
from vertebra.scheduler.trigger import TriggerHandler,Trigger

class BaseScheduler(object):
  def __init__(self):
    self.triggers = dict()
    nh = NoneHandler()
    bsh = BaseSentinelHandler()
    tah = TaskHandler()
    trh = TriggerHandler()
    eh = ExceptionHandler()
    self.handlers = [nh,trh,tah,bsh,eh]

  def __repr__(self):
    return '<%s 0x%x>' % (self.__class__.__name__,id(self))

  def handle(self,task,ret):
    if type(ret) is list: # Lists are SPECIAL
      for ret in list:
        self.handle(task,ret)
    else:
      for handler in self.handlers:
        if isinstance(ret,handler.TYPES):
          try:
            if handler.handle(self,task,ret):
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
    self.set_active(who,task)

  def set_active(self,task,who):
    raise NotImplementedError()

  def get_active(self):
    raise NotImplementedError()

  def run_active(self):
    taskspec = self.get_active()

    if taskspec is None:
      return False

    (who,task) = taskspec
    debug("%r: attempting task %r",self,task)

    try:
      ret = task.iterate(self,who)
    except Exception, e:
      ret = e
    self.handle(task,ret)

    return True

  def process_triggers(self):
    woken = False
    for trigger in self.triggers.keys():
      if trigger.ready(self):
        self.wake_sleeping(trigger)
        woken = True
    return woken

  def wake_sleeping(self,trigger):
    debug("%r: waking trigger %r",self,trigger)
    try:
      T = self.triggers[trigger]
      while 1:
        try:
          sleeping_task = T[0]
        except IndexError:
          del self.triggers[trigger]
          break
        debug("%r: waking task %r",self,task)
        self.schedule(task,trigger)
        del T[0]
    except Full:
      pass # Queue Got Full, Try The Rest Next Time

  def loop(self):
    debug("%r: starting",self)
    try:
      while 1:
        debug("%r: processing triggers",self)
        worked = self.process_triggers()
        debug("%r: running active tasks",self)
        while self.run_active():
          worked = True
        if worked:
          continue
        debug("%r: going idle",self)
        self.idle()
    except StopIteration:
      # Time to stop
      return

  def idle(self):
    raise NotImplementedError()

  def wake(self): # With No Idle Function, This Does Nothing
    pass

class PrioScheduler(BaseScheduler):
  DEFAULT_PRIO = 100

  def get_prio(self,task):
    try:
      return task.prio
    except AttributeError:
      return self.DEFAULT_PRIO

class SimplePQueue(PrioScheduler):
  def __init__(self):
    super(SimplePQueue,self).__init__()
    self.active = []

  @staticmethod
  def compare_prio(x,y):
    (prio0,junk0) = x
    (prio1,junk1) = y
    return cmp(x,y)

  def get_active(self):
    try:
      (prio,taskspec) = self.active[0]
      del self.active[0]
      return taskspec
    except IndexError:
      return

  def set_active(self,who,task):
    taskspec = (who,task,)
    self.active.append( (self.get_prio(task), taskspec, ) )
    self.active.sort(cmp=self.compare_prio)

class ThreadSafePQueue(PrioScheduler):
  def __init__(self):
    super(ThreadSafePQueue,self).__init__()
    self.active = StablePrioQueue()

  def get_active(self):
    try:
      taskspec = self.active.get(block=False)
      return taskspec
    except Empty:
      return

  def set_active(self,who,task):
    taskspec = (who,task,)
    self.active.put_nowait(self.get_prio(task), taskspec)

class BusyScheduler(BaseScheduler):
  def idle(self):
    if self.triggers:
      raise RuntimeError("Busy-Scheduler Went Idle With Work, Uh-Oh")
    else:
      raise StopIteration()
