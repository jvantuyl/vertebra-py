"""Utility Functions"""

import unittest
from util import *

infcmp = infinity.sorter

class UtilInfinityTest(unittest.TestCase):
  data = [1,5,1000000000000,-1000000000,'a','abc',u'abc',{'a':'b'},[],[1,2,3]]

  def test00_InfinityIsBig(self):
    """infinite sorting value is bigger than test data"""
    for i in self.data:
      self.assertTrue(infcmp(infinity,i) > 0)

  def test01_DataIsSmall(self):
    """test data is smaller than infinite sorting value"""
    for i in self.data:
      self.assertTrue(infcmp(i,infinity) < 0)

  def test02_InfinityIsntSmall(self):
    """infinite sorting value isn't smaller than test data"""
    for i in self.data:
      self.assertFalse(infcmp(infinity,i) < 0)

  def test03_DataIsntBigger(self):
    """test data isn't bigger than infinite sorting value"""
    for i in self.data:
      self.assertFalse(infcmp(i,infinity) > 0)

  def test04_DataIsntEqual(self):
    """test data isn't equal to infinite sorting value"""
    for i in self.data:
      self.assertFalse(infcmp(i,infinity) == 0)

  def test05_InfinityIsntEqualToItself(self):
    """multiple infinities shouldn't compare equal"""
    self.assertTrue(infcmp(infinity,infinity) == 0)

  def test06_TrichotomyRule(self):
    """verify that test data and infinity compare reflexively"""
    data = self.data[:]
    data.append(infinity)
    for a in data:
      for b in data:
        j = infcmp(a,b)
        k = infcmp(b,a)
        self.assertTrue(
                         ( j == 0 and k == 0) or
                         ( j <  0 and k >  0) or
                         ( j >  0 and k <  0)
                       )

class UtilityPathTest(unittest.TestCase):
  def test00_normalize_pathRemoveConsecutiveSeparators(self):
    """normalize_path removes consecutive separators"""
    def tslash(dirty,clean):
      self.assertEquals(normalize_path(dirty,"/",None,None),clean)
    def tcolon(dirty,clean):
      self.assertEquals(normalize_path(dirty,":",None,None),clean)

    # No Paths
    tslash( "",  "")
    tcolon( "",  "")
    tslash( "//", "/")
    tcolon( "::", ":")

    # No Separators
    tslash("no_seps", "no_seps")
    tcolon("no_seps", "no_seps")

    # Duplicate Leading Separators
    tslash("//lead","/lead")
    tcolon("::lead",":lead")
    tslash("/////lead","/lead")
    tcolon(":::::lead",":lead")

    # Duplicate Leading Separators
    tslash("trail//","trail/")
    tcolon("trail::","trail:")
    tslash("trail/////","trail/")
    tcolon("trail:::::","trail:")

    # Duplicated Separators
    tslash("///I////have///many/duplicate/separators//in/me//",
           "/I/have/many/duplicate/separators/in/me/")
    tcolon(":::I::::have:::many:duplicate:separators::in:me::",
           ":I:have:many:duplicate:separators:in:me:")

  def test01_normalize_pathLeadingAndTrailing(self):
    """normalize_path correctly handles leading and trailing separators"""
    def slash_stuff_slash(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,True,True),clean)
    def maybe_stuff_maybe(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,None,None),clean)
    def slash_stuff_maybe(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,True,None),clean)
    def maybe_stuff_slash(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,None,True),clean)
    def maybe_stuff(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,None,False),clean)
    def stuff_maybe(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,False,None),clean)
    def slash_stuff(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,True,False),clean)
    def stuff_slash(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,False,True),clean)
    def stuff(dirty,clean):
      self.assertEquals(normalize_path(dirty,sep,False,False),clean)

    for sep,ibare,ilead,itrail,iboth,obare,olead,otrail,oboth in [
        ("/","stuff//here","/stuff//here","stuff//here/","/stuff//here/",
             "stuff/here", "/stuff/here", "stuff/here/", "/stuff/here/"  ),
        (":","stuff::here",":stuff::here","stuff::here:",":stuff::here:",
             "stuff:here", ":stuff:here", "stuff:here:", ":stuff:here:"  ),
        ("|","stuff||here","|stuff||here","stuff||here|","|stuff||here|",
             "stuff|here", "|stuff|here", "stuff|here|", "|stuff|here|"  ),
      ]:

      maybe_stuff_maybe(ibare, obare)
      maybe_stuff_maybe(ilead, olead)
      maybe_stuff_maybe(itrail,otrail)
      maybe_stuff_maybe(iboth, oboth)
  
      maybe_stuff(ibare, obare)
      maybe_stuff(ilead, olead)
      maybe_stuff(itrail,obare)
      maybe_stuff(iboth, olead)
  
      stuff_maybe(ibare, obare)
      stuff_maybe(ilead, obare)
      stuff_maybe(itrail,otrail)
      stuff_maybe(iboth, otrail)
  
      slash_stuff_maybe(ibare, olead)
      slash_stuff_maybe(ilead, olead)
      slash_stuff_maybe(itrail,oboth)
      slash_stuff_maybe(iboth, oboth)
  
      maybe_stuff_slash(ibare, otrail)
      maybe_stuff_slash(ilead, oboth)
      maybe_stuff_slash(itrail,otrail)
      maybe_stuff_slash(iboth, oboth)
  
      slash_stuff(ibare, olead)
      slash_stuff(ilead, olead)
      slash_stuff(itrail,olead)
      slash_stuff(iboth, olead)
  
      stuff_slash(ibare, otrail)
      stuff_slash(ilead, otrail)
      stuff_slash(itrail,otrail)
      stuff_slash(iboth, otrail)
  
      slash_stuff_slash(ibare, oboth)
      slash_stuff_slash(ilead, oboth)
      slash_stuff_slash(itrail,oboth)
      slash_stuff_slash(iboth, oboth)

