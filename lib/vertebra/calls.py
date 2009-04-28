from vertebra.util import sym
from logging import info

class incall(object):
  def setup(self,frm,request):
    pass

  def dispatch(self,request):
    pass

class outcall(object):
  def setup(self,to,request):
    pass

class invocation(object):
  pass

class invo_local(invocation):
  pass

class invo_net(invocation):
  pass

class evocation(object):
  pass

class evo_local(evocation):
  pass

class evo_net(evocation):
  pass

def register_initcall(op,args,scope):
  info("initcall registered %r",op)

# These should probably become classes
once = sym.once
once_then_exit = sym.once_then_exit
restart = sym.restart
restart_throttled = sym.restart_throttled

# Mocks for Testing
class mock_incall(object):
  pass
