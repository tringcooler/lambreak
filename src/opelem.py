#! python3
# coding: utf-8

from opex import *

class opelem(object):

    def __init__(self, id):
        self._id = id

    def eval(self, out, pool, srci, t = 0):
        stat = pool.get_base('stat', 'idle')
        if t == 0:
            out.append(self)
            print('eval', self._id)
    
    def __repr__(self):
        return '<op:' + self._id + '>'

class comb_sym(opelem):
    pass
        
class comb(comb_sym):

    def __init__(self):
        super(comb, self).__init__('comb')

    def eval(self, out, pool, srci, t = 0):
        super(comb, self).eval(out, pool, srci, t)
        pool.cur['comb_cnt'] = pool.get('comb_cnt', 0) + 1
        pool.cur['comb_ref'] = True
        
class comb_rcptr(comb_sym):

    def __init__(self):
        super(comb_rcptr, self).__init__('comb_rcptr')

    def eval(self, out, pool, srci, t = 0):
        super(comb_rcptr, self).eval(out, pool, srci, t)
        if pool.get('comb_ref', False):
            pool.cur['comb_ref'] = False
            pool.cur['comb_cnt'] = pool.get('comb_cnt', 0) - 1
            out.pop()
            out.pop()
            out.append(self)
        else:
            if not isinstance(srci.peek, comb_sym):
                out.append(srci.peek)
                raise opex_scan_bypass()

class rtab_sym(opelem):
    pass

class rtab_reg(rtab_sym):
    
    def __init__(self):
        super(rtab_reg, self).__init__('rtab_reg')
    
    def eval(self, out, pool, srci, t = 0):
        super(rtab_reg, self).eval(out, pool, srci, t)
        

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
        print(src_s.out._seq)
    test()

