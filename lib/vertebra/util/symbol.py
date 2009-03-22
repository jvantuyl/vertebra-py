from weakref import WeakValueDictionary

__all__ = ['symbol','sym','factory']

# Helper Classes
class symbol(object):
  """A class for creating named singletons for use as sentinel values."""
  def __new__(cls,name):
    if not hasattr(cls,'_pool'):
      cls._pool = WeakValueDictionary()
    pool = cls._pool
    if not name in pool:
      sym = super(symbol,cls).__new__(cls)
      sym.__symname__ = name
      pool[name] = sym
    else:
      sym = pool[name]
    return sym
    # NOTE: This is arranged so that sym won't go out of scope and delete our
    # new instance too early

  def __getnewargs__(self):
    return tuple([self.__symname__])

  def __repr__(self):
    return '(%s %s)' % (self.__class__.__name__,self.__symname__,)

class factory(object):
  """
     A class to facilitate creating sentinels by opportunistically
     instantiating a class on attribute access.
  """
  def __init__(self,cls):
    self._what = cls

  def __getattribute__(self,name):
    if '_' in name:
      return super(factory,self).__getattribute__(name)
    else:
      return self._what(name)

  def __repr__(self):
    return '<factory for %s instances>' % self._what.__name__

# Symbol Factory
sym = factory(symbol)
