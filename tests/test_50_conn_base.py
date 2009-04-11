from vertebra.conn.base import baseConnection
from time import sleep
from support import raises,suppress_logging
from mock_conn_base import mock,mock_broken,mock_broken_noretry

class mocked_conn_base:
  @classmethod
  def setupClass(self):
    self.stanzas = []
    self.mock = self.MOCK_TYPE()
    self.runtest()

  @classmethod
  @suppress_logging()
  def runtest(self): # Not working reconnect, internal delay, give 0.5 sec
    try:
      self.mock.setup(deliver = self.deliver)
      self.mock.start()
      self.mock.wake()
      sleep(0.5)
      self.mock.stop()
      self.mock.join(4.5)
    except:
      self.mock.crashed = True

  def deliver(self,x):
    self.stanzas.append(x)

class test_00_conn_base(mocked_conn_base):
  MOCK_TYPE = mock

  def test_00_mock_didnt_crash(self):
    """conn.base: did it crash?"""
    assert not self.mock.crashed

  def test_01_mock_didnt_die(self):
    """conn.base: did it die unexpectedly?"""
    assert not self.mock.died

  def test_02_mock_woken(self):
    """conn.base: did we get our wakeup call?"""
    assert self.mock.awoken

  def test_03_mock_connected(self):
    """conn.base: did we attempt to connect?"""
    assert self.mock.connected

  def test_04_mock_processed(self):
    """conn.base: did we attempt to process data?"""
    assert self.mock.processed

  def test_05_mock_stopped(self):
    """conn.base: did we stop?"""
    assert self.mock.stopped

class test_01_conn_base_broken(mocked_conn_base):
  MOCK_TYPE = mock_broken

  @classmethod
  @suppress_logging()
  def runtest(self): # Will have retry, give enough time for one retry, 4 sec
    try:
      self.mock.setup(deliver = self.deliver)
      self.mock.start()
      self.mock.wake()
      sleep(4.0)
      self.mock.stop()
    except:
      self.mock.crashed = True

  def test_00_mock_broken_didnt_die(self):
    """conn.base: broken-with-retry mock SHOULD NOT die"""
    assert not self.mock.died

  def test_01_mock_broken_crash(self):
    """conn.base: broken-with-retry mock SHOULD NOT crash"""
    assert not self.mock.crashed

  def test_02_mock_broken_reconnected(self):
    """conn.base: broken-with-retry mock SHOULD reconnect"""
    assert self.mock.reconnected

class test_02_conn_base_broken_noretry(mocked_conn_base):
  MOCK_TYPE = mock_broken_noretry

  # No Retries, Just Inherits Quick Exit Test Runner
  
  def test_00_mock_broken_noretry_died(self):
    """conn.base: broken-without-retry mock SHOULD die"""
    assert self.mock.died

  def test_01_mock_broken_noretry_crash(self):
    """conn.base: broken-without-retry mock SHOULD NOT crash"""
    assert not self.mock.crashed

  def test_02_mock_broken_noretry_reconnected(self):
    """conn.base: broken-without-retry mock SHOULD NOT reconnect"""
    assert not self.mock.reconnected

class test_03_base_abstract:
  def setup(self):
    self.bc = baseConnection()

  @raises(NotImplementedError)
  def test_00_base_notimplemented_wake(self):
    """conn.base: wake function must be overridden?"""
    self.bc.wake()

  @raises(NotImplementedError)
  def test_01_base_notimplemented_connect(self):
    """conn.base: connect function must be overridden?"""
    self.bc.connect()

  @raises(NotImplementedError)
  def test_02_base_notimplemented_process(self):
    """conn.base: process function must be overridden?"""
    self.bc.process()

