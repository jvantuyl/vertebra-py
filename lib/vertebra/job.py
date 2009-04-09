from random import randint
from vertebra.token import token

class job(object):
  def init(self,incall,tok = None):
    if tok is None:
      tok = token()
    self.token = tok
    self.incall = incall

  def __repr__(self):
    return '<job "%s">' % self.token

