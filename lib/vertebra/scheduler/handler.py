class Handler(object):
  TYPES = () # NOTE: THIS MUST BE A TUPLE, NO LISTS!
  
  def handle(self,scheduler,task,ret): # returns True if handled
    return False

class NoopHandler(Handler):
  TYPES = ( type(None), )
  def handle(self,scheduler,task,nothin):
    scheduler.schedule(task)
    return True
