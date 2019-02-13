#! python3
# coding: utf-8

from opex import *

class opelem(object):

    def __init__(self, id):
        self._id = id

    def eval(self, out, pool, srci):
        stat = pool.get_base('stat', 'idle')
        print('eval', self._id)

class comb_sym(opelem):
    pass
        
class comb(comb_sym):

    def __init__(self):
        super(comb, self).__init__('comb')

    def eval(self, out, pool, srci):
        super(comb, self).eval(out, pool, srci)
        pool.cur['comb_cnt'] = pool.get('comb_cnt', 0) + 1
        pool.cur['comb_ref'] = True
        
class comb_rcptr(comb_sym):

    def __init__(self):
        super(comb_rcptr, self).__init__('comb_rcptr')

    def eval(self, out, pool, srci):
        super(comb_rcptr, self).eval(out, pool, srci)
        if pool.get('comb_ref', False):
            pool.cur['comb_ref'] = False
        else:
            if not isinstance(srci.peek, comb_sym):
                raise opex_scan_bypass()

if __name__ == '__main__':
    from evmac import _eval_seq, _eval_scanner, _base_pool
    def test():
        src_q = _eval_seq()
        src_q.append(comb())
        src_q.append(comb())
        src_q.append(comb_rcptr())
        src_q.append(opelem('a1'))
        src_q.append(comb_rcptr())
        src_q.append(opelem('a2'))
        src_q.append(comb())
        src_q.append(comb_rcptr())
        src_q.append(opelem('a3'))
        src_s = _eval_scanner(src_q, _base_pool())
        src_s.scan()
    test()

