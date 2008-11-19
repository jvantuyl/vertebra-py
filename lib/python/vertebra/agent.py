"""Vertebra: Agent Executor
"""

class base_agent(object):
    def __init__(self):
        self.initiators = {}
        self.targets = {}

    def authorize(self,op):
        raise NotImplementedError

class naive_agent(base_agent):
    def authorize(self,op):
        return True

# HeraultAgent implemented in herault.py

class agent(base_agent):
    def authorize(self,op):
        # TODO
        return False
