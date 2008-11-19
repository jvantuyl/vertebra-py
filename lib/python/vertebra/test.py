#!/usr/bin/python
import unittest

modules = ['res','actor','agent']
suite = unittest.TestSuite()

for mod in modules:
  try:
    suite.addTest(unittest.TestLoader().loadTestsFromName('test_' + mod))
  except ImportError:
    pass

if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite)
