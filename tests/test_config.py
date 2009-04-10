from vertebra.config import config,DEFAULT_CONFIG
from os import tempnam,unlink
from warnings import catch_warnings

sample_data0 = """
agent.actors: [foo,bar,baz]
conn.xmpp.jid: vertebra@test.net/agent0
conn.xmpp.passwd: supersekret
"""

sample_data1 = """
agent.actors: [qux]
"""

def swapconfigdefault(tempconfig):
  """decorator to safely swap default config file around during function run"""
  def decorate(f):
    def func(*args,**kwargs):
      oldfile = DEFAULT_CONFIG['agent.configfile']
      del DEFAULT_CONFIG['agent.configfile']
      try:
        return f(*args,**kwargs)
      finally:
        DEFAULT_CONFIG['agent.configfile'] = oldfile
    func.func_name = f.func_name
    func.func_doc = f.func_doc
    return func
  return decorate

class test_config:
  def setup(self):
    self.tempfiles = {}
    self.create_temp('sample0',sample_data0)
    self.create_temp('sample1',sample_data1)
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
      cfg.load(args)
    return cfg

  def teardown(self):
    [ unlink(target) for target in self.tempfiles.itervalues() ]

  def test_defaults(self):
    """config: defaults?"""
    cfg = self.make_config('sample0')
    assert 'agent.exit' in cfg
    assert cfg['agent.exit'] == 'idle'

  def test_file(self):
    """config: file?"""
    cfg = self.make_config('sample0')
    assert 'conn.xmpp.jid' in cfg
    assert cfg['conn.xmpp.passwd'] == 'supersekret'

  def test_args(self):
    """config: args?"""
    cfg = self.make_config('sample0','-X','1','2','4')
    assert 'magic' in cfg
    assert list(cfg['magic']) == [1,2,4]

  def test_unrecognized_arg(self):
    """config: unrecognized arg?"""
    cfg = self.make_config('sample0','-BLAH')
    return True

  @swapconfigdefault("/dev/null")
  def test_load_default_config(self):
    """config: load default config?"""
    cfg = self.make_config(None)
    assert 'conn.xmpp.passwd' not in cfg

  @swapconfigdefault("~/this_config_does_not_exist")
  def test_missing_config(self):
    """config: no config?"""
    cfg = self.make_config(None)
    assert 'conn.xmpp.passwd' not in cfg

