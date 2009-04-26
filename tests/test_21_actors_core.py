from mock_agent import mock_agent
from mock_conn_base import mock as mock_conn
from vertebra.config import config

def test_00_load_core():
  """actors.core: actor loads"""
  conf = config()
  conf.load()
  conn = mock_conn()
  agent = mock_agent()
  agent.setup(conf,conn)
  agent.load_actor("actor_core")
