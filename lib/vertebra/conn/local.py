from vertebra.conn.base import baseConnection
from vertebra.util import singleton

class localConnection(baseConnection):

  class codec(object):
    def marshall(self,msg):
      return msg

    def unmarshall(self,rawmsg):
      return rawmsg

  class identity(singleton):
    pass

  def setup(self,config):
    super(localConnection,self).setup(config)
    self.idents = set()

  def start(self):
    return True

  def stop(self,wait=True):
    return True

  def registerIdentity(self,ident):
    self.idents.add(ident)

  def localIdentities(self):
    return [self.identity()]

  def accept_ident(self,ident):
    return ident in self.idents

  def __repr__(self):
    return u'<local>'
