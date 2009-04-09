"""
Utility Functions for Vertebra
==============================
"""

__all__ = ['hexify','unhexify','symbol']

def hexify(val,pad=0):
  """convert integer to lower-case, zero-padded hexadecimal"""
  return ('%%0%dx' % pad) % val

def unhexify(st):
  """convert hexadecimal string to integer"""
  return int(st,16)
