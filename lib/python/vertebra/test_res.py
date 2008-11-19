import unittest
from res import *

class ResSetup(unittest.TestCase):
  def setUp(self):
    super(ResSetup,self).setUp()
    self.root  = res('/')
    self.usa   = res('/usa')
    self.ca    = res('/usa/california')
    self.sf    = res('/usa/california/san_francisco')
    self.mo    = res('/usa/missouri')
    self.kc    = res('/usa/missouri/kansas_city')
    self.stl   = res('/usa/missouri/st_louis')
    self.jp    = res('/japan')
    self.kyoto = res('/japan/kyoto')
    self.tokyo = res('/japan/tokyo')
    self.in_us = [self.sf,self.kc,self.stl]
    self.in_jp = [self.kyoto,self.tokyo]
    self.on_earth = [self.usa,self.jp] + self.in_us + self.in_jp

class ResTests(ResSetup):
  def testRoot(self):
    """root resource is correctly generated"""
    self.assertEqual(len(self.root),0)
  
  def testBare(self):
    """resource must have a leading slash"""
    self.assertRaises(ValueError,self.helpBare)
    x = res("/test")

  def helpBare(self):
    """helper for testBare"""
    x = res("test")

  def testTrailing(self):
    """resource is correctly created with a trailing slash"""
    self.assertEquals(res('/test'),res('/test/'))
    
  def testEmpty(self):
    """empty resource should fail with a TypeError"""
    self.assertRaises(ValueError,self.helpEmpty)
  
  def helpEmpty(self):
    """helper for testEmpty"""
    x = res("")

  def testRootContains(self):
    """root should contain any resource, including itself"""
    self.assert_(self.root.contains(self.root))
    for r in self.on_earth:
      self.assert_(    self.root.contains(r))
      self.assert_(not r.contains(self.root))

  def testUsaVersusJapan(self):
    """verify that containment is correct"""
    usa = self.usa
    jp  = self.jp
    self.assert_(not usa.contains(jp))
    self.assert_(not jp.contains(usa))
    for in_us in self.in_us:
      self.assert_(    usa.contains(in_us))
      self.assert_(not in_us.contains(usa))
      self.assert_(not in_us.contains(jp ))
    for in_jp in self.in_jp:
      self.assert_(    jp.contains(in_jp ))
      self.assert_(not in_jp.contains(jp ))
      self.assert_(not in_jp.contains(usa))

class SetTests(ResSetup):
  def setUp(self):
    super(SetTests,self).setUp()
    self.s_usa  = resset([self.usa])
    self.s_jp   = resset([self.jp])
    self.s_usai = resset(self.in_us)
    self.s_jpi  = resset(self.in_jp)
    
  def testCover(self):
    """set coverage works"""
    usa  = self.s_usa
    jp   = self.s_jp
    usai = self.s_usai
    jpi  = self.s_jpi
    
    self.assert_(usa.covers(usa))
    self.assert_(jp.covers(jp))
    
    self.assert_(not usa.covers(jp))
    self.assert_(not jp.covers(usa))
    
    self.assert_(usa.covers(usai))
    self.assert_(jp.covers(jpi))
    
    self.assert_(not usa.covers(jpi))
    self.assert_(not jp.covers(usai))
    
    self.assert_((usa  | jp ).covers(usai | jpi))
    self.assert_((usa  | jpi).covers(usai | jpi))
    self.assert_((usa  | jp ).covers(usai | jpi))
    self.assert_((usai | jp).covers(usai | jpi))
    
    self.assert_(not (usa | usai | jpi).covers(usa | jp))
  
  def testNormalize(self):
    """set normalization works"""
    usa  = self.s_usa
    jp   = self.s_jp
    usai = self.s_usai
    jpi  = self.s_jpi

    self.assertEquals(usa,        (usai | usa).normalize())
    self.assertEquals(jp,         (jpi  | jp ).normalize())
    self.assertEquals(usai | jp,  (usai | jp ).normalize())
    self.assertEquals(jpi  | usa, (jpi  | usa).normalize())
