from vertebra.calls import mock_incall
from vertebra.job import job
from re import compile

JOB_REPR = compile('<job .*>')

class test_00_job:
  def test_00_instantiate(self):
    """job: create job?"""
    i = mock_incall()
    j = job()
    j.setup(i)

  def test_01_repr(self):
    """job: displays correctly?"""
    i = mock_incall()
    j = job()
    j.setup(i)
    r = repr(j)
    assert JOB_REPR.match(r)

