from mock_agent import mock_agent

def test_00_load_core():
  """actors.core: actor loads"""
  agent = mock_agent()
  agent.load_actor("actor_core")
