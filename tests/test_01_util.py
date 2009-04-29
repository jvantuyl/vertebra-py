from vertebra.util import *
from vertebra.util import symbol
from re import compile
from pickle import dumps as pickle,loads as unpickle,HIGHEST_PROTOCOL

class test_00_hex_functions:
  def test_00_hexify(self):
    "util.hex: convert hexadecimal to unadorned, lowercase string"
    assert hexify(0) == '0'
    assert hexify(0,2) == '00'
    assert hexify(255) == 'ff'
    assert hexify(256) == '100'
    assert hexify(255,4) == '00ff'
    assert hexify(256,4) == '0100'

  def test_01_unhexify(self):
    "util.hex: convert unadorned hex string to integer"
    assert unhexify('0') == 0
    assert unhexify('00') == 0
    assert unhexify('ff') == 255
    assert unhexify('100') == 256
    assert unhexify('00ff') == 255
    assert unhexify('0100') == 256

SYMBOL_REPR = compile('\(symbol .*\)')
class test_01_symbol:
  def test_00_create(self):
    'util.symbol: basic creation'
    sy_a = symbol.abc
    assert symbol(sy_a)
    assert sy_a.symname() == 'abc'
  
  def test_01_repr(self):
    'util.symbol: text representation'
    assert SYMBOL_REPR.match( repr( symbol.a ) )

  def test_02_factory(self):
    'util.symbol: factory creation'
    fact_repr = '%r creates symbols' % symbol # for code coverage
    sy_a = _symbol('a')
    sf_a = symbol.a
    assert sy_a is sf_a

  def test_03_identity(self):
    'util.symbol: symbol identity'
    sy_a0 = symbol.a
    sy_b0 = symbol.b
    sy_a1 = symbol.a
    sy_b1 = symbol.b
    assert sy_a0 is sy_a1
    assert sy_b0 is sy_b1
    assert sy_a0 is not sy_b0
    assert sy_a0 is not sy_b1
    assert sy_a1 is not sy_b0
    assert sy_a1 is not sy_b1
  
  def test_04_pickle(self):
    'util.symbol: pickling'
    cucumber = symbol.cucumber
    gerkin = pickle(cucumber,HIGHEST_PROTOCOL) #NOTE: MUST be protocol 2+
    veggie = unpickle(gerkin)
    assert veggie is cucumber
  
