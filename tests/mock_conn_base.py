from vertebra.conn.base import baseConnection
from time import sleep

# Mock Connection Implementation, No Retries, Successful Loop
class mock(baseConnection):
  def setup(self,*args,**kwargs):
    r = super(mock,self).setup(self,*args,**kwargs)
    self.loops = 5
    self.awoken = False
    self.reconnected = False
    self.connected = False
    self.processed = False
    self.stopped = False
    self.died = False # Exited Main Loop Without Command to Stop
    self.crashed = False # External API raised exception
    self.crash_fatal = True # To Detect Crashes
    return r

  def run(self):
    super(mock,self).run()
    if self.keep_running:
      self.died = True

  def stop(self,wait=True):
    self.stopped = True
    return super(mock,self).stop(wait)

  def wake(self):
    self.awoken = True

  def connect(self):
    if self.connected:
      self.reconnected = True
    else:
      self.connected = True

  def process(self):
    sleep(0.05)
    self.processed = True
    if self.loops:
      self.loops -= 1
    else:
      self.keep_running = False

  def handle_crash(self,e):
    r = super(mock,self).handle_crash(e)
    if not r:
      self.died = True
    return r

# Mock Connection Implementation, Retries, Broken Loop
class mock_broken(mock):
  def setup(self,*args,**kwargs):
    r = super(mock_broken,self).setup(*args,**kwargs)
    self.crash_fatal = False
    return r

  def process(self):
    raise Exception("EEK")

# Mock Connection Implementation, No Retries, Broken Loop
class mock_broken_noretry(mock):
  def process(self):
    raise Exception("EEK")

