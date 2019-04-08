#! python3
# coding: utf-8

from opex import *

class opunit(object):
    
    def __init__(self, id):
        self._id = id
    
    ctag = None
    def cond(self, context):
        if self.ctag:
            cond = context['pool'].cur.get('__evm_swi', {})
            if self.ctag in cond and cond[self.ctag]:
                return True
            else:
                return False
        else:
            return True
    
    def eval(self, context):
        pass
        
    def __repr__(self):
        return '<op:' + self._id + '>'

class opelem(object):

    def __init__(self, units):
        pass
    
    def eval(self, out, pool, srci, t = 0):
        if t == 0:
            print('eval', self._id)
    
    
