from mock_agent import mock_agent
from support import raises

class test_00_agent:
  def setUp(self):
    self.dummy = mock_agent()

  @raises(ImportError)
  def test_00_actor_load_failure(self):
    """agent: load nonexistent actor fails?"""
    self.dummy.load_actor('this_actor_doesnt_exist')
