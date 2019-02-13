#! python3
# coding: utf-8

from opex import *

class opelem(object):

    def __init__(self, id):
        self._id = id

    def eval(self, out, pool, nxop):
        self._bypass(nxop)
        stat = pool.get_base('stat', 'idle')

    def _bypass(self, nxop):
        if pool.get('bypass_cnt', 0) > 0:
            pool.cur['bypass_cnt'] = pool.get('bypass_cnt', 0) - 1
        elif pool.get('bypass_until', lambda x:False)(nxop):
            pool.cur['bypass_until'] = None
        else:
            return
        raise opex_scan_bypass()

    def bypass(self, arg):
        if callable(arg):
            pool.cur['bypass_until'] = arg
        else:
            pool.cur['bypass_cnt'] = arg

class comb_sym(opelem):
    pass
        
class comb(comb_sym):

    def __init__(self):
        super(comb, self).__init__('comb')

    def eval(self, out, pool, nxop):
        super(comb, self).eval(out, pool, nxop)
        pool.cur['comb_cnt'] = pool.get('comb_cnt', 0) + 1
        pool.cur['comb_ref'] = True
        
class comb_rcptr(comb_sym):

    def __init__(self):
        super(comb, self).__init__('comb_rcptr')

    def eval(self, out, pool, nxop):
        super(comb, self).eval(out, pool, nxop)
        if pool.get('comb_ref', False):
            pool.cur['comb_ref'] = False
        else:
            self.bypass(1)

