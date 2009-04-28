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
