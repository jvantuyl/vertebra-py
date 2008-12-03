"""Vertebra: Actors

   An actor contains the code which is exposed as Operations in Vertebra.

   Herein we provide the structures and helper functions necessary to wrap
   your code.

   In our implementation, actors are spawned off as separate processes
   by the agent runtime and communicate via interprocess message
   passing.
"""

from multiprocessing import Process, Pipe

def op(func,op_prefix="/debug",op_name=None,op_memo=False,**op_resources):
    """Decorator To Add Metadata Necessary For A Vertebra Operation
    """
    if not op_name:
      name = func.func_name
    op_name = op_prefix + '/' + op_name
    while '//' in op_name:
      op_name = op_name.replace('//','/')
    func.vop = True
    func.vop_name = op_name
    func.vop_memo = op_memo
    func.vop_memoed = False
    func.vop_memoval = None
    func.vop_res = op_resources
    return func

class base_actor(Process):
    """Vertebra Actor Base Class
    """

    def __init__(self,*args,**kwargs):
        name = "actor<%s>" % self.__class__.__name__
        self.pipe,pipe = Pipe(duplex=True)
        return super(actor,self).__init__(None,None,name,pipe,*args,**kwargs)

    def run(self,pipe,*args,**kwargs):
        raise NotImplementedError
    
    @op("/internal")
    def main(self,*args,**kwargs):
      raise NotImplementedError

    def ops(self):
        return [ op for op in dir(self) 
                 if getattr(getattr(self,op,None),'vop',False) ]

class async_actor(base_actor):
    pass

class sync_actor(base_actor):
    pass

def __test__():
    class TestActor(async_actor):
        @op(a="/test",b="/test2")
        def ping(self):
            print "blah"
    return TestActor
