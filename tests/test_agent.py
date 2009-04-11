from mock_agent import mock_agent
from support import raises

class agent_tests:
  def setUp(self):
    self.dummy = mock_agent()

  @raises(ImportError)
  def test_actor_load_failure(self):
    """agent: load nonexistent actor fails?"""
    self.dummy.load_actor('this_actor_doesnt_exist')
