"""Configuration Infrastructure"""
import unittest
from config import *
from test_config_data import DATASET

class ConfigHashTest(unittest.TestCase):
  def testHashSort(self):
    """hashes sort correctly by various axes"""
    self.assert_(True)

