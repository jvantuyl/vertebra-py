from vertebra.conn.base import baseConnection
from time import sleep

class mock_base(baseConnection):
  def setup(self,*args,**kwargs):
    self.awoken = False
    self.connected = False
    self.processed = False
    return super(mock_base,self).setup(self,*args,**kwargs)

  def wake(self):
    self.awoken = True

  def connect(self):
    self.connected = True

  def process(self):
    sleep(0.5)
    self.processed = True
    self.keep_running = False

class test_conn_base:
  @classmethod
  def setupClass(self):
    self.stanzas = []
    self.mock = mock_base()
    self.mock.setup(deliver = self.deliver)
    self.mock.start()
    self.mock.wake()
    self.mock.join(5.0)

  def deliver(self,x):
    self.stanzas.append(x)

  def test_mock_woken(self):
    """conn.base: did we get our wakeup call?"""
    assert self.mock.awoken

  def test_mock_connected(self):
    """conn.base: did we attempt to connect?"""
    assert self.mock.connected

  def test_mock_processed(self):
    """conn.base: did we attempt to process data?"""
    assert self.mock.processed
