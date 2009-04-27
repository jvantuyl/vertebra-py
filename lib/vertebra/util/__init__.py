"""
Utility Functions for Vertebra
==============================
"""

__all__ = ['hexify','unhexify','symbol']

import symbol

def hexify(val,pad=0):
  """convert integer to lower-case, zero-padded hexadecimal"""
  return ('%%0%dx' % pad) % val

def unhexify(st):
  """convert hexadecimal string to integer"""
  return int(st,16)

class memoize:
  """simple memoize, remembers results of a certain function call"""
  # NOTE: Currently don't ever bother to clear out old entries
  # FIXME: Implement LRU or something
  def __init__(self, f):
    self.f = f
    self.cache = {}

  def __call__(self, *args):
    # I think this is only okay for immutable args
    res = self.cache.get(args,None)

    # Can't memoize functions that return None, but it would be kind of
    # pointless anyway
    if res is None:
      res = self.f(*args)
      self.cache[args] = res

    return res

  def clear(self):
    self.cache = {}

class singleton(object):
  """singleton classes, there is only ever one of these"""
  def __new__(cls, *args, **kwargs):
    if not hasattr(cls,'_theone'):
      cls._theone = super(singleton,cls).__new__(cls, *args, **kwargs)
    return cls._theone
