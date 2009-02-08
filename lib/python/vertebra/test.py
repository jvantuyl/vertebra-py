#!/usr/bin/python
import unittest

modules = ['res','actor','agent','config','util']
suite = unittest.TestSuite()

class TestSuiteWithHeader(unittest.TestSuite):
  def run(self,result):
    if self.desc:
      result.stream.write("\nSUITE: " + self.desc + "\n")
    else:
      result.stream.write("\nSUITE: (anonymous)\n")
    super(TestSuiteWithHeader,self).run(result)

for mod in modules:
  modsuite = TestSuiteWithHeader()
  try:
    testmod = __import__('test_' + mod)
    if testmod.__doc__:
      modsuite.desc = testmod.__doc__.split("\n")[0].strip()
    else:
      modsuite.desc = None
    modsuite.addTest(unittest.TestLoader().loadTestsFromModule(testmod))
    suite.addTest(modsuite)
  except ImportError:
    pass

if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite)
