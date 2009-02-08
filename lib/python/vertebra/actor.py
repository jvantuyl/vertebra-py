"""Vertebra: Actors

   An actor contains the code which is exposed as Operations in Vertebra.

   Herein we provide the structures and helper functions necessary to wrap
   your code.

   In our implementation, actors are spawned off as separate processes
   by the agent runtime and communicate via interprocess message
   passing.
"""

import threading
import multiprocessing
from vertebra.util import normalize_path

class operation(object):
  """A class that supports the operation protocol.
  """
  def __init__(self,op_name,op_prefix="/debug",op_memo=False,**op_resources):
    self.prefix = op_prefix
    self.name = op_name
    self.memo = op_memo
    self.memoed = False
    self.memoval = None
    self.res = op_resources
  
  def __call__(self,code):
    self.code = code
    code.op = self
    return code
    
  def accept(self,**resources):
    return True # FIXME: Actually check resources
  
  def dispatch(self,**kwargs):
    raise NotImplementedError
    
  def next(self):
    raise NotImplementedError
  
  def cancel(self):
    pass

class job(object):
  """A class that supports the job protocol.
  """
  def __init__(self,job_name,pjid,**resources):
    self.name = job_name
    self.pjid = pjid
    super(job,self).__init__()
  
  def abort(self):
    raise NotImplementedError

  def pause(self):
    raise NotImplementedError

  def resume(self):
    raise NotImplementedError

class job_thread(job):
  """A class that implements a job process as a thread.
  """
  