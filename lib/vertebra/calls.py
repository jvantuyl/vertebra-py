from vertebra.util.symbol import sym
from logging import info

class incall(object):
  pass

class incall_local(incall):
  pass

class incall_net(incall):
  pass

class incall_initcall(incall):
  pass

class outcall(object):
  pass

class outcall_local(outcall):
  pass

class outcall_net(outcall):
  pass

# Init Calls
class initcall(incall):
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
