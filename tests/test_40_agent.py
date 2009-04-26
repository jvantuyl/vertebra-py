from vertebra.config import config
from mock_agent import mock_agent
from mock_conn_base import mock as mock_conn
from support import raises

class test_00_agent:
  def setUp(self):
    conf = config()
    conf.load()
    conn = mock_conn()
    self.dummy = mock_agent()
    self.dummy.setup(conf,conn)

  @raises(ImportError)
  def test_00_actor_load_failure(self):
    """agent: load nonexistent actor fails?"""
    self.dummy.load_actor('this_actor_doesnt_exist')
