from vertebra.actor import actor

class test_actor:
  def test_instantiate(self):
    """actor: can instantiate a base actor"""
    a = actor()
    assert isinstance(a,actor), "instantiated actor is actually an actor"
