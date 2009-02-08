"""Vertebra: Miscellaneous Utility Functions
"""

def normalize_path(path,sep="/",forceLeading=True,forceTrailing=False):
  """Processes path strings to remove doubled separators and 
     correctly process leading and trailing separators.

     Note, for root paths, leading overrides trailing.

     For forcing options, True forces, False doesn't, and None leaves
     whatever is there.
  """
  double = 2 * sep

  # Remove Doubles
  while double in path:
    path = path.replace(double,sep)

  # Root Paths
  if not path or path == sep:
    if forceLeading is True: # Force
      return sep
    elif forceLeading is False: # Strip
      return ''
    else:
      return path

  # Detect Leading and Trailing Slashes
  hasLeading = path[0] == sep
  hasTrailing = path[-1] == sep

  # At this point, we have a non-root path, possibly with leading or trailing
  # separators.  Now we just hit all possible force options, and we're done.
  # We process the leading first, then return the correct trailing.
  if forceLeading is True and not hasLeading: # Force
    path = sep + path
  if forceLeading is False and hasLeading: # Strip
    path = path[1:]
  if forceTrailing is True and not hasTrailing: # Force
    path = path + sep
  if forceTrailing is False and hasTrailing: # Strip
    path = path[:-1]

  # Return what's left
  return path

class infinite(object):
  """A singleton that, when sorted with its sorter method, always compares as
     larger than any other type.  It compares equal to itself to keep sorts
     stable.

     When sorting tuples, if nonexistent values are replaced with None, they
     sort before any actual values.  This may be undesireable when the tuples
     are being used as the index to a Schwartzian Transform to achieve sorts
     on multiple values with descending priorities.  Using the infinity
     singleton allows them to fall at the end of the sort, which may be
     more appropriate for your use case.
  """

  def __new__(klass):
    try:
      return klass.__single__
    except:
      klass.__single__ = super(infinite,klass).__new__(klass)
      return klass.__single__

  def __repr__(self):
    return "<infinite>"

  @classmethod
  def infinitize(klass,cmp):
    """wraps a standard comparison function with logic to handle comparing
       infinities
    """
    def sorter(self,other,klass=klass,cmp=cmp):
      return klass.sorter(self,other,cmp)
    return sorter

  @classmethod
  def sorter(klass,self,other,cmp=cmp):
    """standard comparison function with logic to handle comparing infinities
    """
    s = self  is klass.__single__
    o = other is klass.__single__
    if s and o:
      return 0
    if s:
      return 1
    if o:
      return -1
    return cmp(self,other)

infinity = infinite()
