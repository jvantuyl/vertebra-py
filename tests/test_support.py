"""Helpers to Help With Nose Testing"""

from support import *

class test_raises:
  def divbyzero(self):
    return 1 / 0 # Raises ZeroDivisionError

  def intplusstr(self):
    return 3 + '' # Raises TypeError

  def outofbounds(self):
    return [1,2,3][5] # Raises IndexError

  def happy(self):
    return 2+2

  @raises(ZeroDivisionError)
  def test_catch1(self):
    """support: catch 1/0?"""
    self.divbyzero()

  @raises(TypeError)
  def test_catch2(self):
    """support: catch int + str?"""
    self.intplusstr()

  @raises(IndexError)
  def test_catch3(self):
    """support: catch walk off array?"""
    self.outofbounds()

  def test_miss(self):
    """support: no raise == fail?"""
    @raises(TypeError)
    def f(): self.happy()

    try:
      f()
    except ExceptionFailure:
      return True

    assert False, "shouldn't ever make it here"
