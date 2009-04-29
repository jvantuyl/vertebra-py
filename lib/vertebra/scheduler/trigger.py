from vertebra.scheduler.handler import Handler

class Trigger(object):
  def ready(self,scheduler):
    raise NotImplementedError()

class TriggerHandler(handler):
  TYPES = ( trigger, )
  def handle(self,scheduler,task,trigger):
    if trigger not in scheduler.triggers:
      scheduler.triggers[trigger] = []
    scheduler.triggers[trigger].append(task)
    return True
