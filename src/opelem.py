#! python3
# coding: utf-8

class opelem(object):

    def __init__(self):
        pass

    def eval(self, out, pool, nxop):
        stat = pool.get_base('stat', 'idle')
        
