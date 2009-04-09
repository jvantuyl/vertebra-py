from vertebra.util import hexify, unhexify
from random import randint
import re

# Constants
TOKEN_LEN_BITS = 128 # bits
TOKEN_LEN_BYTES = TOKEN_LEN_BITS / 8
TOKEN_LEN_HEX = TOKEN_LEN_BITS / 4

TOKEN_HALF_BITS = TOKEN_LEN_BITS / 2
TOKEN_HALF_BYTES = TOKEN_HALF_BITS / 8
TOKEN_HALF_HEX = TOKEN_HALF_BITS / 4

TOKEN_LO_MASK =  2 ** TOKEN_HALF_BITS - 1
TOKEN_HI_MASK = TOKEN_LO_MASK << TOKEN_HALF_BITS
TOKEN_HALF_MASK = TOKEN_LO_MASK
TOKEN_MASK = TOKEN_HI_MASK | TOKEN_LO_MASK

TOKEN_MIN = 0
TOKEN_MAX = TOKEN_MASK
TOKEN_HALF_MAX = TOKEN_HALF_MASK

TOKEN_RE = re.compile('([0-9A-Fa-f]{%d}):([0-9A-Fa-f]{%d})' % \
  (TOKEN_HALF_HEX,TOKEN_HALF_HEX))

# Token Implementation
class token(long):
  @classmethod
  def from_string(cls,st):
    match = TOKEN_RE.match(st)
    assert match is not None
    parent,base = match.groups()
    return cls(unhexify(base),unhexify(parent))

  def __new__(cls,base = None,parent=0):
    if base is None:
      base = randint(TOKEN_MIN,TOKEN_HALF_MAX)

    assert (parent & TOKEN_LO_MASK) == parent
    assert (base & TOKEN_LO_MASK) == base

    newtoken = (parent << TOKEN_HALF_BITS) | base
    return super(cls,token).__new__(cls,newtoken)
  
  def parent(self):
    return (self & TOKEN_HI_MASK) >> TOKEN_HALF_BITS
  
  def base(self):
    return self & TOKEN_LO_MASK
  
  def spawn(self):
    return self.__class__(parent=self.base())

  def __nonzero__(self):
    return True # Tokens always are True, Use None for no token
    
  def __str__(self):
    return hexify(self.parent(),pad=TOKEN_HALF_HEX) + ':' + \
           hexify(self.base(),  pad=TOKEN_HALF_HEX)

  def __repr__(self):
    return '<token "%s">' % self
