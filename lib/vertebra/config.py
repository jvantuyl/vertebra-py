"""
Configuration Objects for Vertebra
==================================
Getting your configuration in Vertebra is a multilayered thing.  The list of
places that a value is search for goes something like this (in descending order
of precedence):

* Command Line
* Config File
* Network (disabled for bootstrap configs)
* Internal Defaults

Bootstrap Config
----------------
When an agent is being loaded, it does not have access to the network to
request configuration from Entrepot.  This proposes a chicken-and-egg problem,
since the configuration must be accessible.

For these situations, you use the bootstrap configuration API.

Runtime Config
--------------
When the network holds the authoritative data, you need to consult it.  Since
this API may block and issues an operation, its environment must be taken into
account.  The actual API is implemented as a yield-able Fibra request.  For
actor iplementations that abstract away the evented framework, you must wrap
this API to offer to actors using your implementation.
"""

import yaml
from os.path import expanduser
from types import DictionaryType
from logging import debug,warning
import re
from copy import deepcopy

DEFAULT_CONFIG = {
  'agent.configfile': '~/.vertebra/agent.yml',
  'agent.actors':     [],
  'agent.exit':       'idle',
}

ARGMAP = {
  'a': ('agent.actors',1,' '.split),
  'c': ('agent.configfile',1,str),
  'U': ('conn.xmpp.jid',1,str),
  'P': ('conn.xmpp.passwd',1,str),
  'H': ('conn.xmpp.server',1,str),
  'X': ('magic',3,lambda *X: tuple(map(int,X))),
}

ARG_RE = re.compile('^-([' + ''.join(ARGMAP) + '])$')

class config(object):
  def __init__(self):
    super(config,self).__init__()
    self.default_config = DEFAULT_CONFIG
    self.config = None
    self.loaded = False

  def process_args(self,args):
    # FIXME: Use getopt or something
    config_default = {}

    config = {}
    cur_arg = None
    arg_code = None
    arg_cvt = None
    arg_count = 0
    arg_stack = None

    for tok in args: # Scan Command Line
      if cur_arg is None: # Detecting Args
        match = ARG_RE.match(tok)
        if match: # Matched an Arg Code
          (arg_code,) = match.groups() # Extract Code
          (cur_arg,arg_count,arg_cvt) = ARGMAP[arg_code] # Find Arg Info
          if arg_count == 0: # No Count Means Toggle Arg
            config[cur_arg] = not self.default_config[cur_arg] # Flip Default
            cur_arg = None # No Parameters
          arg_stack = [] # Zero Stack
        else:
          warning("unrecognized argument: %s", tok)
      else: # Collecting Parameters
        arg_stack.append(tok) # Next Parameter for Stack
        if len(arg_stack) == arg_count: # Have All Parameters
          try: # Attempt Conversion
            config[cur_arg] = arg_cvt(*arg_stack)
            debug("cli config: %s=%r",cur_arg,config[cur_arg])
          except Exception:
            warning("invalid argument: %s (-%s), %r",cur_arg,arg_code,
                    arg_stack,exc_info=True)
          cur_arg = None
    if cur_arg is not None:
      warning("incomplete argument: %s (-%s), %r",cur_arg,arg_code,arg_stack)
    self.cli_config = config

  def load(self,config_file=None,args=[]):
    self.config = {}
    self.default_config = deepcopy(DEFAULT_CONFIG)
    self.process_args(args)
    self.file_config = {}

    if config_file:
      pass
    elif 'agent.configfile' in self.cli_config:
      config_file = self.cli_config['agent.configfile']
    elif 'agent.configfile' in self.default_config:
      config_file = self.default_config['agent.configfile']
    else:
      warning("No Config File (Not Even A Default?)")
      return

    try:
      file_settings = yaml.load(open(expanduser(config_file),'r'))
      assert type(file_settings) is DictionaryType
      self.file_config = file_settings
    except AssertionError:
      warning("Config File Format Not Recognized: %s", config_file)
    except IOError:
      warning("Unable to Open Config File: %s", config_file)
    except Exception,e:
      warning("Unexpected Loading Configuration: %s, %e",config_file,e,
              exc_info=True)

    self.loaded = True

  def keys(self):
    s = set()
    s.update(self.cli_config)
    s.update(self.file_config)
    s.update(self.default_config)
    return s

  def bootstrap_get(self,idx):
    if not self.loaded:
      raise Exception("Config Not Loaded")
    for settings in [
                      self.cli_config,
                      self.file_config,
                      self.default_config,
                    ]:
      if idx in settings:
        return settings[idx]
    raise KeyError('Value Not Found')

  def __contains__(self,idx):
    return idx in self.cli_config or \
           idx in self.file_config or \
           idx in self.default_config

  def __getitem__(self,idx):
    return self.bootstrap_get(idx)

