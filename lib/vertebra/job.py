from random import randint

# TODO: unit test hexify
def __hexify__(val,pad=0):
  val = hex(val)
  if val[-1] == 'L':
    val = val[2:-1]
  else:
    val = val[2:]
  val = '0' * max(0, pad - len(val)) + val
  return val.lower()

TOKEN_LEN_BITS = 128 # bits
TOKEN_LEN_BYTES = TOKEN_LEN_BITS / 8
TOKEN_LEN_HEX = TOKEN_LEN_BITS / 4
TOKEN_MIN = 0
TOKEN_MAX = 2**TOKEN_LEN_BITS - 1

# TODO: unit test token
class token(object):
  def __init__(self,token = None,parent=0):
    if token is None:
      token = randint(TOKEN_MIN,TOKEN_MAX)
    self.token = token
    self.parent = parent

  def __str__(self):
    return __hexify__(self.parent,pad=TOKEN_LEN_HEX) + ':' + \
           __hexify__(self.token, pad=TOKEN_LEN_HEX)

  def __repr__(self):
    return '<token "%s">' % self

class job(object):
  def init(self,incall,tok = None):
    if tok is None:
      tok = token()
    self.token = tok
    self.incall = incall

  def __repr__(self):
    return '<job "%s">' % self.token

