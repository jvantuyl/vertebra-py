from vertebra.util import atom,atomfactory

class _security_type(atom):
  pass

security_type = _security_type.factory()

# TODO: Make these full blown classes
agent_default_security = security_type.secure_default
herault_security = security_type.secure_herault
always_allow = security_type.secure_not_really
