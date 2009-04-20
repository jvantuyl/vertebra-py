from vertebra.config import config,DEFAULT_CONFIG
from os import tempnam,unlink
from warnings import catch_warnings
from support import raises,suppress_logging

# Test Data
bad_data = "["

sample_data0 = """
agent.actors: [foo,bar,baz]
conn.xmpp.jid: vertebra@test.net/agent0
conn.xmpp.passwd: supersekret
"""

sample_data1 = """
agent.actors: [qux]
"""

# Helpful Decorator
def swapconfigdefault(tempconfig):
  """decorator to safely swap default config file around during function run"""
  def decorate(f):
    def func(*args,**kwargs):
      oldfile = DEFAULT_CONFIG['agent.configfile']
      if tempconfig:
        DEFAULT_CONFIG['agent.configfile'] = tempconfig
      else:
        del DEFAULT_CONFIG['agent.configfile']
      try:
        return f(*args,**kwargs)
      finally:
        DEFAULT_CONFIG['agent.configfile'] = oldfile
    func.func_name = f.func_name
    func.func_doc = f.func_doc
    return func
  return decorate

# Tests
class test_0_config:
  def setup(self):
    self.tempfiles = {}
    self.create_temp('sample0',sample_data0)
    self.create_temp('sample1',sample_data1)
    self.create_temp('bad_sample',bad_data)
    # Monkey Patch Default File Out

  def create_temp(self,name,data):
    with catch_warnings(record=True):
      self.tempfiles[name] = tempnam()
    f = open(self.tempfiles[name],'w')
    f.write(data)
    f.close()

  def make_config(self,data,*args):
    cfg = config()
    if data:
      cfg.load(self.tempfiles[data],args)
    else:
      cfg.load(None,args)
    return cfg

  def teardown(self):
    [ unlink(target) for target in self.tempfiles.itervalues() ]

  @raises(Exception)
  def test_00_not_loaded(self):
    """config: SHOULD give an error if accessed before config is loaded"""
    cfg = config()
    x = cfg['foo']
    
  def test_01_defaults(self):
    """config: defaults?"""
    cfg = self.make_config('sample0')
    assert 'agent.exit' in cfg
    assert cfg['agent.exit'] == 'idle'

  def test_02_file(self):
    """config: file?"""
    cfg = self.make_config('sample0')
    assert 'conn.xmpp.jid' in cfg
    assert cfg['conn.xmpp.passwd'] == 'supersekret'

  @suppress_logging()
  @swapconfigdefault("/dev/null")
  def test_03_load_empty_config(self):
    """config: load empty config?"""
    cfg = self.make_config(None)
    # TODO: Test for Warning?

  @suppress_logging()
  @swapconfigdefault("/dev/null")
  def test_04_load_empty_config_defaults(self):
    """config: load empty config, get defaults?"""
    cfg = self.make_config(None)
    assert 'conn.xmpp.passwd' not in cfg

  @suppress_logging()
  @swapconfigdefault(None)
  def test_05_no_config_at_all(self):
    """config: no config at all?"""
    cfg = self.make_config(None)

  @suppress_logging()
  def test_06_missing_config_file(self):
    """config: nonexistant config file?"""
    cfg = self.make_config(None,'-c','nonexistant file')
    assert 'conn.xmpp.passwd' not in cfg
    # TODO: Test for Warning?

  @suppress_logging()
  def test_07_bad_config(self):
    """config: config doesn't parse?"""
    cfg = self.make_config('bad_sample')
    # TODO: Test for Warning?

  @suppress_logging()
  def test_08_missing_config(self):
    """config: file missing?"""
    cfg = self.make_config(None,'-c','i_dont_exist')
    # TODO: Test for Warning?
    
  @suppress_logging()
  @swapconfigdefault(None)
  def test_09_cli_configfile(self):
    """config: get config file from command line?"""
    cfg = self.make_config(None,'-c','/dev/null')
    used_config = cfg['agent.configfile']
    assert used_config == '/dev/null'

  def test_10_config_keys(self):
    """config: key enumeration?"""
    cfg = self.make_config('sample0')
    assert len( cfg.keys() )

  def test_11_args(self):
    """config: args?"""
    cfg = self.make_config('sample0','-X','1','2','4')
    assert 'magic' in cfg
    assert list(cfg['magic']) == [1,2,4]

  @suppress_logging()
  def test_12_unrecognized_arg(self):
    """config: unrecognized arg?"""
    cfg = self.make_config('sample0','-BLAH')
    # TODO: Test for Warning?
    
  def test_13_config_toggle_arg(self):
    """config: toggle argument, nonexistent default"""
    cfg = self.make_config('sample0','-Z')
    assert 'toggletest' in cfg
    assert cfg['toggletest']

  @suppress_logging()
  def test_14_config_arg_parse_error(self):
    """config: argument fails its parse function?"""
    cfg = self.make_config('sample0','-X','1','2','a')
    # TODO: Test for Warning?

  @suppress_logging()
  def test_15_arg_short(self):
    """config: data runs short for argument?"""
    cfg = self.make_config('sample0','-X','1','2')
    assert 'magic' not in cfg
    # TODO: Test for Warning?

  @raises(KeyError)
  def test_16_missing(self):
    """config: missing values raise error on []?"""
    cfg = self.make_config('sample0')
    cfg['i am not here']

  def test_17_argcombine(self):
    """config: certain arguments should combine"""
    cfg = self.make_config('sample0','-a','qux')
    assert cfg['agent.actors'] == ['foo','bar','baz','qux']

  def test_18_argsplit(self):
    """config: certain arguments should split"""
    cfg = self.make_config('sample0','-a','qux fizz','-a','bang')
    assert cfg['agent.actors'] == ['foo','bar','baz','qux','fizz','bang']
