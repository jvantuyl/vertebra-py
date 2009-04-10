from vertebra.agent import mock_agent

def test_load_core():
  """actors.core: actor loads"""
  agent = mock_agent()
  agent.load_actor("actor_core")
