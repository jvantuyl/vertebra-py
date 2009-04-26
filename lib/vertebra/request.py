from vertebra.resource import res
import re

SCOPES = ['direct','all','any','single']

class request:
  def __init__(self,name):
    self._name = name
    self._called = False

  def __call__(self,**kwargs):
    args = {}
    for key,val in kwargs.items():
      if key[-1] == '_':
        args[key[:-1]] = res(val)
      else:
        args[key] = val
    self._args = args
    self._called = True
    return self

  def __getattr__(self,key):
    if self._called:
      raise AttributeError("Can't derive sub-operation after args specified")
    else:
      self._name += '.' + key
      return self
    raise AttributeError("request has no attribute %s" % key)

  def __getitem__(self,key):
    if type(key) is not tuple:
      key = (key,)
    key,args = key[0],key[1:]
    if self._called:
      raise IndexError("Can't set scope after args specified")
    if key not in SCOPES:
      raise IndexError("Unknown scope %s" % key)
    self._scope = key
    self._scope_args = args
    return self

  def __repr__(self):
    r = '<request %s(%r)/%s' % (self._name,self._args,self._scope)
    if self._scope_args:
      first = True
      r += '('
      for a in self._scope_args:
        if first:
          first = False
        else:
          r += ','
        r += repr(a)
      r += ')'
    r += '>'
    return r

PRIV_PATTERN = re.compile("^_.*")

class request_factory(object):
  _REQUEST_CLASS = request

  def __getattr__(self,key):
    return self._REQUEST_CLASS(key)

cloud = request_factory()

def merge(*args):
  pass
