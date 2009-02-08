import sys
import os.path
import ConfigParser
from util import infinity

if sys.platform == 'win32':
  CONFIG_SYS = sys.prefix
  CONFIG_USER = os.path.join(os.path.expanduser('~'),
    "Application Data","Vertebra")
  assert not CONFIG_USER == '~'
if sys.platform in ['darwin','linux2']:
  CONFIG_SYS = '/etc/vertebra'
  CONFIG_USER = os.path.expanduser('~/.vertebra') 

def _unwrap(H):
  return H[1]

def _wrap(H,axes):
  return ( tuple( 
             ( (axis in H and H[axis] or infinity) for axis in axes ) 
                ), H )

def sort_hashes(axes,HASHES):
  return [_unwrap(H) for H in sorted(
      [ _wrap(H,axes) for H in HASHES ],
      cmp=infinity.sorter
    )]

