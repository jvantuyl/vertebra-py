from vertebra.util import symbol,symfactory as factory

__all__ = ['msg','st','fsm']

class message(symbol): pass
class enter(message): pass
class exit(message): pass
class state(symbol): pass

ent = factory(enter)
ext = factory(exit)
st = factory(state)

class fsm(object): # NOTE: Technically, this is a Transducer (Mealey Machine)
  #inputs = [] 
  #outputs = []
  states = []
  state = None # Set to initial
  transit_table = {} # mapping of tuples (state,input) -> (new_state,output)
  
  def step(self,input):
    assert self.state
    new_state,output = self.transit_table[ (self.state,input) ]
    