from vertebra.actor import actor,bind_op,init_call,once
from vertebra.scope import single
from vertebra.request import request as req,merge
from vertebra.resource import res as r
from threading import Lock

def load(agent):
  pass

class counter_server(actor):
  def load(self,agent):
    self.last_id_map = {}
    self.lock = Lock()

  @bind_op("/counter/get_id")
  def get_id(self,request):
    with self.lock:
      wanted = request['counter']
      last = self.last_id_map.get(wanted,0)
      self.last_id_map[wanted] = last + 1
    yield { counter: wanted, id: last }

@init_call("/counter/test",{},once)
class counter_getter(actor):
  def load(self,agent):
    self.agent = agent

  @bind_op("/counter/test")
  def test(self,request):
    counters = merge(
      single.req("/counter/get_id",counter="foo"),
      single.req("/counter/get_id",counter="bar"),
      single.req("/counter/get_id",counter="foo"),
      single.req("/counter/get_id",counter="baz"),
      single.req("/counter/get_id",counter="qux"),
    )
    for result in counters:
      print repr(result)
    agent.stop()

