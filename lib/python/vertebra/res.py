"""Resources provide a means for security and discovery in Vertebra
"""

class res(object):
  """A simple subclass of list
  
  When instantiated with a string representing a point hierarchy of resources,
  this class provides sensical semantics when faced with comparison and
  iteration.
  """
  def __init__(self,resstring):
    if resstring == '':
      raise ValueError("Invalid resource identifier (should you have used  /)")
      
    if resstring == '/':
      self.__data = []
      self.__resstring = resstring
      return
    
    if resstring[0] != '/':
      raise ValueError("Resources must begin with a /")
    
    if resstring[-1] == '/':
      resstring = resstring[:-1]
    
    self.__resstring = resstring
    self.__data = resstring.split('/')[1:]
  
  def __repr__(self):
    return "<res '%s'>" % self.__resstring

  def __eq__(self,other):
    return self.__data == other.__data
    
  def __gt__(self,other):
    return self.__data > other.__data

  def __lt__(self,other):
    return self.__data < other.__data

  def __iter__(self):
    return iter(self.__data)
      
  def __hash__(self):
    return hash(tuple(self.__data))

  def __len__(self):
    return len(self.__data)
    
  def contains(self,other):
    if not isinstance(other,res):
      raise TypeError("Resources can only contain other resources")
    x = self.__data
    y = other.__data
    return x == y[:len(x)]

class resset(set):
  """A special set that contains functionality specifically for comparing sets of resources"""
  
  def covers(self,other):
    """Determines if a set of resources completely covers another set of resources"""

    if not isinstance(other,resset):
      raise TypeError("Resource Sets can only cover other resource sets")
    
    outer = sorted(self)
    inner = sorted(other)
    
    while len(inner) > 0:
      if len(outer) == 0:     # There are inners but no outers to match them, key doesn't fit, fail!
        return False
      if inner[0] < outer[0]: # If the top inner < the top outer, then no outer can match that inner, fail!
        return False
      if outer[0].contains(inner[0]): # Outer matched inner. Eat Inner.
        del inner[0]
        continue
      # Top outer didn't match top inner, no inners can be matched by this outer. Eat outer.
      del outer[0]
    return True
  
  def normalize(self):
    """Normalizes a set by removing resources that are descendents of other resources."""
    res = sorted(self)

    if len(res) < 2:
      return self

    out = [res[0]]
    del res[0]
    
    while len(res) > 0:
      if not out[-1].contains(res[0]):
        out.append(res[0])
      del res[0]
    return self.__class__(out)
