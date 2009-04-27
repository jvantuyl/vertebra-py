from vertebra.util import memoize
from logging import error,fatal,info,warn

# NOTE: The registry has to have a local connection in order to accept
# registrations of local identities.

class router(list):
  def setup(self,agent,local):
    self._agent = agent
    self._local = local
    self.register(local)

  def register(self,conn):
    if not conn in self:
      self.append(conn)
      self.sort(key=self.getprio)
      #self.find_conn.flush()
      conn.router = self
    for ident in conn.localIdentities():
      self._local.registerIdentity(ident)

  def start(self):
    info("starting connections")
    started = False
    for c in list(self):
      try:
        info("starting connection %r",c)
        thisstart = c.start()
        if not thisstart:
          warn("failed to start connection %r",c)
        started |= bool(thisstart)
      except Exception:
        error("crash starting connection %r",c,exc_info=True)
        self.remove(c)
    if not started:
      fatal("failed to start any connections!")
    return started

  def stop(self):
    info("stopping connections")
    stopped = False
    for c in self:
      try:
        info("stopping connection %r",c)
        thisstop = c.stop()
        if not thisstop:
          warn("failed to stop connection %r",c)
        stopped |= bool(thisstop)
      except Exception:
        error("crash stopping connection %r",c,exc_info=True)
    return stopped

  @memoize
  def find_conn(self,ident):
    for conn in self:
      try:
        if conn.accept_ident(ident):
          return conn
      except Exception:
        error("connection %s crashed routing %s",conn,ident,exc_info=True)
    return None

  #@memoize
  def getprio(self,conn):
    try:
      return conn.priority
    except AttributeError:
      return 0

  def recv(self,msg):
    self._agent.recv(msg)

  def send(self,msg):
    c = conn.find_conn(msg.to)

    if c is None:
      error("no connection can handle %s to %s, dropping message" % (msg,to,))
      return False

    return c.send(msg)
  
  def __repr__(self):
    return '<router at %s>' % id(self)
