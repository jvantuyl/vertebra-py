from vertebra.util.symbol import symbol,factory

__all__ = ['msg','st','fsm']

class message(symbol): pass
class state(symbol): pass

msg = factory(message)
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
    