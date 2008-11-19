"""Vertebra: Actors

   An actor contains the code which is exposed as Operations in Vertebra.

   Herein we provide the structures and helper functions necessary to wrap
   your code.

   In our implementation, actors are spawned off as separate processes
   by the agent runtime and communicate via interprocess message
   passing.
"""

from multiprocessing import Process, Pipe

def op(op_prefix="/debug",**op_resources):
    """Decorator To Add Metadata Necessary For A Vertebra Operation
    """

    def set_op(func,prefix=op_prefix,res=op_resources):
        func.vop = True
        func.vop_prefix = prefix
        func.vop_res = res
        return func

    return set_op

class base_actor(Process):
    """Vertebra Actor Base Class
    """

    def __init__(self,*args,**kwargs):
        name = "actor<%s>" % self.__class__.__name__
        self.pipe,pipe = Pipe(duplex=True)
        return super(actor,self).__init__(None,None,name,pipe,*args,**kwargs)

    def run(pipe,*args,**kwargs):
        raise NotImplementedError

    def ops(self):
        return [ op for op in dir(self) 
                 if getattr(getattr(self,op,None),'vop',False) ]

class async_actor(base_actor):
    pass

class sync_actor(base_actor):
    pass

class static_actor(base_actor):
    pass

def __test__():
    class TestActor(actor):
        @op(a="/test",b="/test2")
        def ping(self):
            print "blah"
    return TestActor
