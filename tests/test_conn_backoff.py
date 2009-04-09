from vertebra.conn.backoff import exponential_backoff as BO
from itertools import izip,count

FLOAT_ERROR = 0.000001

class backoff_checker(object):
  def test_stable(self):
    def backoff_test(self):
      bo = BO(self.base,self.max,self.rate,False)
      for cnt,exp,act in izip(count(1),self.expected,bo):
        assert (act - exp) < FLOAT_ERROR, "nonrandom, try %d" % cnt
    backoff_test.description = \
      "backoff: not random(%s,%s,%s)" % (self.base,self.max,self.rate)
    yield backoff_test,self

  def test_randomized(self):
    def backoff_test(self):
      bo = BO(self.base,self.max,self.rate,True)
      for cnt,exp,act in izip(count(1),self.expected,bo):
        assert act <= exp + FLOAT_ERROR, "random, try %d" % cnt
    backoff_test.description = \
      "backoff: random(%s,%s,%s)" % (self.base,self.max,self.rate)
    yield backoff_test,self

class test_binary_cap10k(backoff_checker):
  base = 1
  rate = 2
  max = 10000
  expected = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]

class test_binary_cap500(backoff_checker):
  base = 1
  rate = 2
  max = 500
  expected = [1,2,4,8,16,32,64,128,256,500,500,500,500,500,500,500]

class test_binary_cap10k(backoff_checker):
  base = 1
  rate = 2
  max = 10000
  expected = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,10000,10000]

class test_real_slow(backoff_checker):
  base = 0.050
  rate = 1.1
  max = 1.0
  expected = [0.050,0.055,0.0605,0.06655,0.073205,0.0805255,0.08857805,
              0.097435855,1.0,1.0,1.0]
