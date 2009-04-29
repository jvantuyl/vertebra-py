from vertebra.util import atom
from vertebra.scheduler.handler import Handler

__all__ = ['_scheduler_sentinel','Sentinels','DONE','BaseSentinelHandler']

class _scheduler_sentinel(atom): pass

Sentinels = _scheduler_sentinel.factory()

DONE = Sentinels.DONE

class BaseSentinelHandler(Handler):
  TYPES = ( Sentinels(), )
  def handle(self,scheduler,task,sentinel):
    if sentinel is DONE:
      return True
    warn("unknown sentinel %r" % sentinel)
    return False
