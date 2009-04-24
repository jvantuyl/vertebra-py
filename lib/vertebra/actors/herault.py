from vertebra.actor import actor
from logging import debug,info

__all__ = ['load','dummy']

def load(agent):
  info("core actor loaded")

class herault(actor):
  def load(self,agent):
    super(advertiser,self).load(agent)
    self.advertisements = []
