"""
Symbols and Atoms
=================

Theory
------
These can be a bit tricky to use.  The purpose is that you can be sure
that there is only ever one atom of the same class with the same name.
As such, they have an "identity" much like integers or other discrete
values.  As such, their use is to effectively ensure that nothing can
be mistaken for them, and they cannot be mistaken for something else.

This is most useful when you need to pass around some symbolic value such
some indicator of the state of the system.  These needs have alternately
been filled by classes or enums in various other languages.

Python's new-style classes allow us to focus on the issue of identity by
controlling the creation of the object through the __new__ method.

How To Use
----------
Atoms have two useful characteristics.  They have an identity (i.e. they
sport strong comparison using the 'is' operator) and they are grouped into
classes.  There is a default, of sorts, in the symbol class.

The purpose of the classes is that they allow you to use the isinstance
function to detect which group of atoms you are watching for.  This allows
you to easily mix-and-match atoms with other, user-supplied values with
no fear of getting them mixed up.  This even allows uses to use their own
atom classes.

Conventions
-----------

If you wish to use your own class of atoms, you should create the class by
subclassing the 'atom' class.  You can easily create a factory using the
factory method().  It will create a special object that will turn create
an atom with the name of whatever attribute you access.  For sanity of
implementation, atoms beginning with _ are excluded.

It is recommended that you prepend your class name with an underscore and
create a factory with the normal name.
"""

from weakref import WeakValueDictionary
import re

__all__ = ['atom','symbol','_symbol','atomfactory']

SPECIAL = re.compile('^_.*$')

class atomfactory(object):
  """
     A class to facilitate creating sentinels by opportunistically
     instantiating a class on attribute access.
  """
  def __init__(self,cls):
    self._what = cls

  def __getattribute__(self,name):
    if SPECIAL.match(name):
      return super(atomfactory,self).__getattribute__(name)
    else:
      return self._what(name)

  def __call__(self,thing):
    return isinstance(thing,self._what)

  def __repr__(self):
    return '<atomfactory for %s instances>' % self._what.__name__

class atom(object):
  """A class for creating named classes of sentinel values."""
  # FIXME: Make more efficient, use slots?

  @classmethod
  def factory(cls):
    if not hasattr(cls,'_factory'):
      cls._factory = atomfactory(cls)
    return cls._factory

  def __new__(cls,name):
    if cls is atom:
      raise TypeError("subclass me to identify what type of atom I am")
    if not hasattr(cls,'_pool'):
      cls._pool = WeakValueDictionary()
    pool = cls._pool
    if not name in pool:
      atm = super(atom,cls).__new__(cls)
      atm.__symname__ = name
      pool[name] = atm
    else:
      atm = pool[name]
    return atm
    # NOTE: This is arranged so that atom won't go out of scope and delete our
    # new instance too early

  def __getnewargs__(self):
    # WARNING: symbols must be pickled with protocol 2+ or things explode
    return tuple([self.symname()])

  def __getstate__(self):
    # WARNING: symbols must be pickled with protocol 2+ or things explode
    return False # Don't pickle any state

  def __repr__(self):
    return '(%s %s)' % (self.__class__.__name__,self.symname(),)

  def symname(self):
    return self.__symname__
  
# Symbols
class _symbol(atom): 
  pass

symbol = _symbol.factory()
