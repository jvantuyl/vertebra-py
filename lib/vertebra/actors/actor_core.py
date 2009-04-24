from vertebra.actor import actor,bind_op,init_call,restart
from logging import debug,info

__all__ = ['load','advertiser','dummy']

def load(agent):
  info("core actor loaded")

@init_call("/core/security/advertiser",{},restart)
class advertiser(actor):
  def load(self,agent):
    super(advertiser,self).load(agent)
    self.advertisements = []

  @bind_op("/core/security/advertiser")
  def advertiser(self,request):
    pass

class dummy(actor):
  pass
