"""
Implementation of Connection Backoff
"""
from logging import debug
from random import random

def exponential_backoff(wait_0,wait_max,rate,randomize=True):
  current_try = 0
  while 1:
    backoff_max = (rate ** current_try) * wait_0
    if wait_max is not None:
      backoff_max = min(backoff_max,wait_max)
    if randomize:
      backoff = random() * backoff_max
    else:
      backoff = backoff_max
    debug("backing off: actual=%s, max=%s",backoff,backoff_max)
    yield backoff
    current_try += 1

