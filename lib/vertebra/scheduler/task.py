from vertebra.scheduler.handler import Handler

class Task(object):
  def iterate(self,triggeredby):
    raise NotImplementedError()
  
class TaskHandler(Handler):
  TYPES = ( Task, )
  def handle(self,scheduler,task,newtask):
    scheduler.schedule(task)  # Schedule New Task
    scheduler.schedule(newtask) # Schedule Old Task Too
    return True

class IteratorTask(Task):
  def __init__(self,iterator):
    self.iterator = iterator

  def iterate(self,scheduler):
    try:
      pass # TODO: Finish
    except StopIteration:
      return