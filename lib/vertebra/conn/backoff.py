"""
Implementation of Connection Backoff
"""
from random import random

def exponential_backoff(wait_min,wait_max,rate):
  current_try = 0
  while 1:
    backoff_max = (rate ** current_try) * unit_min
    backoff_max = min(backoff_max,wait_max)
    backoff = random * backoff_max
    debug("backing off: actual=%s, max=%s",(backoff,backoff_max))
    yield backoff

