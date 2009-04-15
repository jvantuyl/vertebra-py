from vertebra.security import agent_default_security,always_allow
from calls import (register_initcall,once,once_then_exit,restart,
                   restart_throttled)

class operation(object):
  def __init__(self,op_tree,impl,res = {}):
    self.op_tree = op_tree
    self.implementation = impl
    self.need_resources = res
    self.is_initcall = False

class actor(object):
  def load(self,agent):
    """actor loading initialization"""
    pass
  
  def collect_ops(self):
    for val in [ getattr(self,key) for key in dir(self) ]:
      if ininstance(val,operation):
        yield val

# Decorator that Transforms and Implementation Function into an Operation
def bind_op(op,security=agent_default_security):
  def create_op(impl):
    o = operation(op,impl)
    o.security_plugin = security
    return o
  return create_op

# Sets Operation to Not Require Authorization
def no_auth(o):
  assert isinstance(o,operation)
  o.security_plugin = always_allow
  return o

# Added Required Resources to an Operation
def bind_res(**kwargs):
  def update_op(op):
    assert isinstance(op,operation)
    op.need_resources.update(kwargs)
    return op
  return update_op

# Registers An Operation As An InitCall
def init_call(actual_op,args = {},scope = once_then_exit):
  def register(op):
    register_initcall(op,actual_op,args,scope)
    return op
  return register

