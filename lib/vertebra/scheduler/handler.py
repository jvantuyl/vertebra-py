from logging import warn

class Handler(object):
  TYPES = () # NOTE: THIS MUST BE A TUPLE, NO LISTS!
  
  def handle(self,scheduler,task,ret): # returns True if handled
    return False

class NoneHandler(Handler):
  TYPES = ( type(None), )
  
  def handle(self,scheduler,task,nothin):
    warn("%r task %r didn't return any instructions, cancelled",
         scheduler,task)
    return True

class ExceptionHandler(Handler):
  TYPES = ( Exception, )

  def handle(self,scheduler,task,exc):
    warn("%r: task %r raised exception %r",scheduler,task,exc,exc_info=True)
