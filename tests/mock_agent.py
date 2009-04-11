from vertebra.agent import base_agent

class mock_agent(base_agent):
  """Mock Agent for Testing"""
  def setup(self,config,connection):
    self.config = config
    self.connection = connection

  def start(self): pass
  def stop(self): pass
