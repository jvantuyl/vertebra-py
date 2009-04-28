from types import GeneratorType,DictType
from threading import Thread
from Queue import Queue,Empty
from vertebra.util import sym
from random import randint
from vertebra.token import token

class JobError(Exception): pass
class Aborted(JobError): pass
class BadData(JobError): pass

class job(object):
  def setup(self,incall,tok = None):
    if tok is None:
      tok = token()
    self.token = tok
    self.incall = incall

  def __repr__(self):
    return '<job "%s">' % self.token

class evented_runner(object): #TODO: Remove Threading, Adapt to Calls
  def setup(self,func,kwargs,notify = None):
    self.func = func
    self.kwargs = kwargs
    self.input = Queue()
    self.output = Queue()
    self.done = False
    self.do_notify = notify

  def send(self,x,block=False,timeout=None):
    self.input.put(x,block=block,timeout=timeout)

  def recv(self):
    r = []
    while 1:
      try:
        r.append(self.output.get(block=False))
      except Empty:
        return r

  def out(self,*args,**kwargs):
    for x in args:
      self.output.put(x,**kwargs)
    self.notify()

  def notify(self):
    if self.do_notify is not None:
      self.do_notify(self)

  def dispatch(self):
    self.thread = Thread(target=self.execute)
    self.thread.setDaemon(True)
    self.thread.start()

  def execute(self):
    print "executing job %r(%r)" % (self.func,self.kwargs,)
    delay = None
    self.running = None
    while 1:
      try:
        if self.running and delay is None:
          n = self.input.get(block=False)
        else:
          n = self.input.get(block=True,timeout=delay)
      except Empty:
        n = None
      if n is None:
        print "no commands, executing one run"
      elif n is sym.start:
        print "starting job function"
        self.out(sym.started)
        st = self.func(self,**self.kwargs)
        if type(st) is GeneratorType:
          print "got generator"
          self.running = st
        elif type(st) is DictType:
          print "single return"
          self.out( (sym.data, st,), sym.final )
          break
        elif st is None:
          print "null return"
          self.out( sym.final )
          break
        else:
          print "bad data"
          self.out( (sym.error, BadData(),) )
      elif n is sym.abort:
        print "abort job"
        if self.running:
          try:
            self.running.throw( Aborted() )
          except Exception,e:
            self.out( (sym.error,e) )
        self.running = None
        break
      else:
        print "Unknown Command"
      delay = None
      if self.running:
        try:
          print "executing iteration"
          r = self.running.next()
          if type(r) in [int,long,float]: # Delay
            print "delay %s" % r
            delay = r
          elif type(r) is DictType:
            print "return value"
            self.out( (sym.data, r) )
          elif r is None:
            print "skip iteration"
          else:
            print "bad data"
            self.running.throw( BadData() )
        except StopIteration:
          print "execution finished"
          self.out( sym.final )
          break
        except Exception, e:
          print "error"
          self.out( (sym.error, e) )
          break
    self.done = True
