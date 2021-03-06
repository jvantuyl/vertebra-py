from vertebra.token import token,TOKEN_HALF_MAX,TOKEN_HALF_BITS
from random import randint
from re import compile

TOKEN_REPR = compile('<token "[0-9A-Fa-f]{16}:[0-9A-Fa-f]{16}">')
class test_00_token_creation:
  def test_00_instantiate(self):
    """token.create: token factory makes tokens"""
    assert isinstance(token(),token), "token factory creates tokens"

  def test_01_from_string(self):
    """token.create: can create from a string"""
    tok = token.from_string('0123456789ABCDEF:FEDCBA9876543210')
    assert tok == 0x0123456789ABCDEFFEDCBA9876543210

  def test_02_from_parts(self):
    """token.create: creates from parts"""
    a = randint(0,TOKEN_HALF_MAX) # hi
    b = randint(0,TOKEN_HALF_MAX) # lo
    c = a << TOKEN_HALF_BITS | b
    tok = token(parent=a,base=b)
    tbase = tok.base()
    tparent = tok.parent()
    assert tok == c
    assert tbase == b
    assert tparent == a

  def test_03_token_repr(self):
    """token.create: text representation"""
    tok = token()
    assert TOKEN_REPR.match( repr(tok) )
    
class test_01_token_zero:
  def make_zero(self):
    return token(0)
    
  def test_00_instantiate(self):
    """token.zero: can instantiate a zero token"""
    assert self.make_zero() == 0, "token factory creates tokens"

  def test_01_evals_true(self):
    """token.zero: even zero token tests true"""
    assert bool(self.make_zero()) == True, "zero token tests true"

class test_02_parentage:
  def test_00_init_job(self):
    """token.spawn: create top-level token"""
    tok = token()
    assert tok.parent() == 0
  
  def test_01_sub_jobs(self):
    """token.spawn: create consistent sub-tokens"""
    top = token()
    s0 = top.spawn()
    s1 = top.spawn()
    assert top.base() == s0.parent()
    assert top.base() == s1.parent()
    
