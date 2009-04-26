"""Helpers to Help With Nose Testing"""
from vertebra.config import config,DEFAULT_CONFIG
import logging
from logging import CRITICAL, NOTSET
from copy import deepcopy

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

def suppress_logging():
  """decorator to suppress logging during a function call"""
  def decorate(f):
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
  return decorate

def swapconfig(config_file=None,config_dirs=None,profile=None):
  """decorator to safely swap default config file around during test"""
  def decorate(f):
    def func(*args,**kwargs):
      oldconfig = deepcopy(DEFAULT_CONFIG)
      if config_file is not None:
        DEFAULT_CONFIG['agent.config_file'] = config_file
      if config_dirs is not None:
        DEFAULT_CONFIG['agent.config_dirs'] = config_dirs
      if profile is not None:
        DEFAULT_CONFIG['agent.profile'] = profile
      try:
        return f(*args,**kwargs)
      finally:
        DEFAULT_CONFIG.clear()
        DEFAULT_CONFIG.update(oldconfig)
    func.func_name = f.func_name
    func.func_doc = f.func_doc
    return func
  return decorate

