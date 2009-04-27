__all__ = ['base','xmpp','local']

# NOTES
#
# Connections implement communication.  Each contains an identity factory that
# is used to create identities.  They also have priorities, that determine the
# order in which they are tried.  By default, the local connection is highest
# priority, and much assumes that the local handler gets first crack at
# identities.
#
# A special local connection can be used to create entirely internal networks.
# This is mostly useful for testing and early provisioning.  Any connection
# which must hairpin (i.e. XMPP) can register a number of identities as local,
# in which case the local connection will snag them and route them internally
# via the local connection.
