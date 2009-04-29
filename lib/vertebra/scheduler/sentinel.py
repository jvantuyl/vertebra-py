from vertebra.util import atom
from vertebra.scheduler.handler import Handler

class sentinel(atom): pass

sent = sentinel.factory()

DONE = sent.DONE

class BaseSentinelHandler(Handler):
  TYPES = ( sentinel, )
  def handle(self,scheduler,task,sentinel):
    if sentinel is DONE:
      return True
    warn("unknown sentinel %r" % sentinel)
    return False
