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
import yaml.parser
from os.path import expanduser,join,exists,sep
from types import DictionaryType
from logging import error,fatal,info,debug,warning
import re
from copy import deepcopy
from sys import exit

DEFAULT_CONFIG = {
  'agent.path': [],
  'agent.config_dir': ["~/.vertebra/",'.'],
  'agent.actors':     [],
  'agent.exit':       'idle',
}

def delim(D):
  def process(X):
    return X.split(D)
  return process

def shadow(X,Y):
  return Y

def combine(X,Y):
  return X + Y

# Arg, Number of SubArgs, Arg Processor, Composition
ARGMAP = {
  'A': ('agent.path',           1, delim(' '), combine),
  'a': ('agent.actors',         1, delim(' '), combine),
  'C': ('agent.config_dir',     1, delim(' '), combine),
  'c': ('agent.config_file',    1, str,        shadow),
  'p': ('agent.profile',        1, str,        shadow),
  'U': ('conn.xmpp.jid',        1, str,        shadow),
  'P': ('conn.xmpp.passwd',     1, str,        shadow),
  'H': ('conn.xmpp.server',     1, str,        shadow),
  'X': ('magic',                3, lambda *X: tuple(map(int,X)), shadow),
  'Z': ('toggletest',           0, bool,       shadow),
}
ARGMIX = dict( [ (agent,comb) for (agent,x,y,comb) in ARGMAP.values() ] )

ARG_RE = re.compile('^-([' + ''.join(ARGMAP) + '])$')

class config(object):
  def __init__(self):
    super(config,self).__init__()
    self.default_config = DEFAULT_CONFIG
    self.config = None
    self.loaded = False
    self.reducers = dict([ (k,v) for (k,x,y,v) in ARGMAP.values() ])

  def process_args(self,args):
    # FIXME: Use getopt or something
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
          (cur_arg,arg_count,arg_cvt,arg_mix) = ARGMAP[arg_code] # Arg Info
          if arg_count == 0: # No Count Means Toggle Arg, Flip Default
            config[cur_arg] = not self.default_config.get(cur_arg,False)
            cur_arg = None # No Parameters
          arg_stack = [] # Zero Stack
        else:
          warning("unrecognized argument: %s", tok)
      else: # Collecting Parameters
        arg_stack.append(tok) # Next Parameter for Stack
        if len(arg_stack) == arg_count: # Have All Parameters
          try: # Attempt Conversion
            prev = config.get(cur_arg,None)
            val = arg_cvt(*arg_stack)
            if prev is not None:
              config[cur_arg] = arg_mix(prev,val)
            else:
              config[cur_arg] = val
            debug("cli config: %s=%r",cur_arg,config[cur_arg])
          except Exception:
            warning("invalid argument: %s (-%s), %r",cur_arg,arg_code,
                    arg_stack,exc_info=True)
          cur_arg = None
    if cur_arg is not None:
      warning("incomplete argument: %s (-%s), %r",cur_arg,arg_code,arg_stack)
    self.cli_config = config

  def arg_combine(self,*args):
    s = {}
    for x in args:
      for k,v in x.iteritems():
        try:
          comb = ARGMIX[k]
        except KeyError:
          comb = shadow
        if k in s:
          s[k] = comb(s[k],v)
        else:
          s[k] = v
    return s
    
  def which_config_file(self,settings):
    if 'agent.config_file' in settings:
      filename = settings['agent.config_file']
      if sep in filename:
        return filename
    elif 'agent.profile' in settings:
      profile = settings['agent.profile'] # from args
      filename = profile + '.yml'
    else:
      filename = 'agent.yml'
    config_dir = settings['agent.config_dir'] # default or from args

    for d in reversed(config_dir):
      path = expanduser(join(d,filename))
      if exists(path):
        return path

    return None

  def load(self,defaults=None,config_file=None,args=[]):
    if defaults is None:
      self.default_config = deepcopy(DEFAULT_CONFIG)
    else:
      self.default_config = defaults

    self.process_args(args)
    self.file_config = {}

    # Use Passed In File With Asolute Preference
    if config_file is None:
      if 'agent.config_file' in self.file_config:
        config_file = self.file_config['agent.config_file']
      else:
        # Try to find one from defaults + args
        tentative_settings = self.arg_combine(
          self.default_config,
          self.cli_config
        )
        config_file = self.which_config_file(tentative_settings)

    # What we got?
    self.used_config = config_file

    # I got nothing...
    if config_file is None:
      warning("No Config File Exists")
      self.loaded = True
      return
    
    try:
      info("loaded config from %s" % (config_file,))
      file_settings = yaml.load(open(config_file,'r'))
      assert type(file_settings) is DictionaryType
      self.file_config = file_settings
    except (yaml.parser.ParserError,AssertionError,):
      fatal("Config File Format Not Recognized: %s", config_file)
    except IOError:
      fatal("Unable to Open Config File: %s", config_file)
    except Exception,e:
      fatal("Unexpected Loading Configuration: %s, %r",config_file,e,
              exc_info=True)
      raise # TODO: Custom Error

    self.loaded = True

  def keys(self):
    s = set()
    s.update(self.cli_config)
    s.update(self.file_config)
    s.update(self.default_config)
    return s

  def bootstrap_get(self,idx,early=False):
    if not early and not self.loaded:
      raise Exception("Config Not Loaded") # TODO: Make Custom Exception
    vals = []
    for settings in [
                      self.default_config,
                      self.file_config,
                      self.cli_config,
                    ]:
      if idx in settings:
        vals.append(settings[idx])
    if vals:    
      return reduce(self.reducers.get(idx,shadow),vals)
    raise KeyError('Value Not Found')

  def dump(self):
    return (self.default_config, self.file_config, self.cli_config)

  def __contains__(self,idx):
    return idx in self.cli_config or \
           idx in self.file_config or \
           idx in self.default_config

  def __getitem__(self,idx):
    return self.bootstrap_get(idx)
