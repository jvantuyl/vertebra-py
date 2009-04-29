from vertebra.scheduler.handler import Handler
from vertebra.scheduler.sentinel import DONE

class Task(object):
  def iterate(self,triggeredby):
    raise NotImplementedError()
  
class TaskHandler(Handler):
  TYPES = ( Task, )
  def handle(self,scheduler,task,newtask):
    scheduler.schedule(task)  # Schedule New Task
    scheduler.schedule(newtask) # Schedule Old Task Too
    return True

class NoopOnceTask(Task):
  def iterate(self,scheduler,who):
    return DONE

class NoopCountTask(Task):
  def __init__(self,times):
    super(Task,self).__init__()
    self.count = 0
    self.max = times

  def iterate(self,scheduler,who):
    if self.count < self.max:
      self.count += 1
      return self
    else:
      return DONE

class IteratorTask(Task):
  def __init__(self,iterator):
    self.iterator = iterator

  def iterate(self,scheduler,who):
    try:
      pass # TODO: Finish
    except StopIteration:
      return DONE
