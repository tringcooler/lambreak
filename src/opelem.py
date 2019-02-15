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
        print('comb')
        self.eval_comb(out, pool)
    
    def eval_comb(self, out, pool):
        if pool.get('comb_ref', False):
            pool.cur['comb_ref'] = False
            pool.cur['comb_cnt'] = pool.get('comb_cnt', 0) - 1
            return True
        else:
            return False

class comb_rcptr_tbp(comb_rcptr):

    def __init__(self):
        super(comb_sym, self).__init__('comb_rcptr_tbp')

    def eval(self, out, pool, srci, t = 0):
        super(comb_sym, self).eval(out, pool, srci, t)
        if self.eval_comb(out, pool):
            out.pop()
            out.pop()
            out.append(self)
            raise opex_scan_bypass()
            

class expr_sym(opelem):
    pass

class expr_bypass(expr_sym):
    
    def __init__(self):
        super(expr_bypass, self).__init__('expr_bypass')
    
    def eval(self, out, pool, srci, t = 0):
        super(expr_bypass, self).eval(out, pool, srci, t)
        if t == 0:
            self.eval_bypass(out, pool)
            if self.eval_comb(out, pool):
                out.pop()
                out.pop()
                out.append(self)
            else:
                self.bypass(out, pool, srci.peek)
        else:
            if pool.get('expr_cnt', 0) > 0:
                self.bypass(out, pool, srci.peek)
    
    def eval_bypass(self, out, pool):
        pool.cur['expr_cnt'] = pool.get('expr_cnt', 0) + 1
        
    def bypass(self, out, pool, nxop):
        if nxop:
            out.append(nxop)
        if isinstance(nxop, expr_sym):
            nxop.eval_bypass(out, pool)
            print('expr', pool.get('expr_cnt', 0))
        raise opex_scan_bypass()
        
class expr_end(expr_sym):
    
    def __init__(self):
        super(expr_end, self).__init__('expr_end')
    
    def eval(self, out, pool, srci, t = 0):
        super(expr_end, self).eval(out, pool, srci, t)
        self.eval_bypass(out, pool)
    
    def eval_bypass(self, out, pool):
        pool.cur['expr_cnt'] = pool.get('expr_cnt', 0) - 1

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
    def test2():
        src_q = _eval_seq()
        src_q.append(comb())
        src_q.append(comb())
        src_q.append(expr_bypass())
        src_q.append(opelem('a1'))
        src_q.append(expr_end())
        src_q.append(opelem('a2'))
        src_q.append(comb())
        src_q.append(comb_rcptr())
        src_q.append(opelem('a3'))
        src_s = _eval_scanner(src_q, _base_pool())
        src_s.scan()
        print(src_s.out._seq)
    #test2()

