"""Helpers to Help With Nose Testing"""
import logging

class ExceptionFailure(Exception):
   """Test Didn't Raise Expected Exception"""

def raises(e):
  """Decorator that Detects If A Test Raises A Certain Exception"""
  def decorate(f):
    """Decorator that Detects If A Test Raises A Certain Exception"""
    def func(*args,**kwargs):
      try:
        f(*args,**kwargs)
      except e:
        return True
      raise ExceptionFailure()
    func.func_name = f.func_name
    func.func_doc = f.func_doc
    return func
  return decorate

