"""
A Generic Marshalling Framework for Vertebra
============================================

This module provides a protocol for marshalling simple objects, a base class
for writing marshallers that speak that protocol, and a registry for tracking
and invoking those marshallers.
"""

from vertebra.util.symbol import sym

__all__ = ['NOT_MINE','MarshallError','Marshaller','Registry','takes_types','takes_keys']

# Sentinel Values
NOT_MINE = sym.NOT_MINE

def takes_types(types): # Called At Class Definition Time
  """Decorator for limiting a marshaller to a certain set of types"""
  def make_marshall(func): # Called At Instance Definition Time
    def marshall(self,obj,marshall): # Called On Instance
      for t in types:
        if isinstance(obj,t):
          return func(self,obj,marshall)
      return NOT_MINE
    marshall.func_name = func.func_name
    marshall.func_doc = func.func_doc
    return marshall
  return make_marshall    

def takes_keys(keys): # Called At Class Definition Time
  """Decorator for limiting a marshaller to a certain set of types"""
  def make_marshall(func): # Called At Instance Definition Time
    def marshall(self,key,obj,marshall): # Called On Instance
      if key in keys:
          return func(self,obj,marshall)
      return NOT_MINE
    marshall.func_name = func.func_name
    marshall.func_doc = func.func_doc
    return marshall
  return make_marshall    


class MarshallError(Exception):
  """Some problem was encountered tranforming an object"""

class Marshaller(object):
  """Base Class for Marshallers"""
  
  priority = 0
  
  # Higher Priority First
  def __lt__(self,other):
    if not isinstance(other,Marshaller):
      return super(Marshaller,self).__lt__(other)
    return self.priority > other.priority
    
  def __gt__(self,other):
    if not isinstance(other,Marshaller):
      return super(Marshaller,self).__gt__(other)
    return self.priority < other.priority

  def __eq__(self,other):
    if not isinstance(other,Marshaller):
      return super(Marshaller,self).__eq__(other)
    return self is other # NOTE: This breaks the trichotomy rule, is that bad?

  def marshall(self,obj,marshall):
    """
       convert a realized object into a serialized form of itself
       
       returns the sentinel NOT_MINE if can't marshall this object
    """
    return NOT_MINE

  def unmarshall(self,key,obj,unmarshall)  :
    """
       convert the serialized form of an object into a realized object
       
       returns the sentinel NOT_MINE if can't unmarshall this object
    """
    return NOT_MINE

class Registry(list):
  """
     Registry of Marshallers
     
     Holds references to all marshallers and provides interface to marshall
     and unmarshall objects.
  """
  def register(self,marshaller):
    """Register A Marshaller for a Type"""
    if marshaller not in self:
      self.append(marshaller)
      self.sort()
  
  def unregister(self,marshaller):
    """Unregister a marshaller"""
    self.remove(marshaller)

  def marshall(self,obj):
    """convert a realized object into a serialized form of itself"""
    for marshaller in self:
      encoded = marshaller.marshall(obj,self.marshall)
      if encoded is NOT_MINE:
        continue
      return encoded
    raise MarshallError("Unable to marshall object")

  def unmarshall(self,key,obj):
    """
       convert the serialized form of an object into a realized object
       
       The meaning of "key" is specific to an encoding
    """
    for marshaller in self:
      decoded = marshaller.unmarshall(key,obj,self.unmarshall)
      if decoded is NOT_MINE:
        continue
      return decoded
    raise MarshallError("Unable to unmarshall object")

  def __repr__(self):
    c = self.__class__
    n = c.__name__
    m = c.__module__
    return '<%s.%s %r>' % (n,m,list(self),)
