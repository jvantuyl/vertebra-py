import unittest
from vertebra.actor import actor

class ResSetup(unittest.TestCase):
  def testInstatiate(self):
    """can instantiate a base actor"""
    a = actor()
    self.assertTrue(isinstance(a,actor))
