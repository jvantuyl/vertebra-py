"""Helpers to Help With Nose Testing"""
import logging
from logging import CRITICAL, NOTSET

class ExceptionFailure(Exception):
   """Test Didn't Raise Expected Exception"""

def raises(e):
  """decorator that detects if a test raises a certain exception"""
  def decorate(f):
    """decorator that detects if a test raises a certain exception"""
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

def suppress_logging(f):
  """decorator to suppress logging during a function call"""
  def func(*args,**kwargs):
    logging.disable(CRITICAL)
    try:
      return f(*args,**kwargs)
    finally:
      logging.disable(NOTSET)
  func.func_name = f.func_name
  func.func_doc = f.func_doc
  return func
