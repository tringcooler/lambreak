#! python3
# coding: utf-8

from opex import *

class opelem(object):

    def __init__(self, id):
        self._id = id

    def eval(self, out, pool, srci, t = 0):
        if t == 0:
            print('eval', self._id)
    
    def outself(self, out, t):
        if t == 0:
            out.append(self)
    
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
        self.outself(out, t)
        
class comb_rcptr(comb_sym):

    def __init__(self):
        super(comb_rcptr, self).__init__('comb_rcptr')

    def eval(self, out, pool, srci, t = 0):
        super(comb_rcptr, self).eval(out, pool, srci, t)
        self.eval_comb(out, pool)
        self.outself(out, t)
    
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
            raise opex_scan_bypass()
        else:
            self.outself(out, t)

class expr_sym(opelem):
    pass

class expr_bypass(expr_sym):
    
    def __init__(self):
        super(expr_bypass, self).__init__('expr_bypass')
    
    def eval(self, out, pool, srci, t = 0):
        super(expr_bypass, self).eval(out, pool, srci, t)
        self.outself(out, t)
        if t == 0:
            pool.cur['expr_st_cnt'] = pool.get('expr_cnt', 0)
        if t == 0 or pool.get('expr_cnt', 0) > pool.get('expr_st_cnt', 0):
            nxop = srci.peek
            if nxop:
                if isinstance(nxop, expr_sym):
                    nxop.eval(out, pool, None, 0)
                    out.append(nxop)
                elif isinstance(nxop, var):
                    nxop.eval(out, pool, None, 0)
                else:
                    out.append(nxop)
            raise opex_scan_bypass()

class expr_rng(expr_sym):
    pass

class expr_start(expr_rng):
    
    def __init__(self):
        super(expr_start, self).__init__('expr_start')
    
    def eval(self, out, pool, srci, t = 0):
        super(expr_start, self).eval(out, pool, srci, t)
        pool.cur['expr_cnt'] = pool.get('expr_cnt', 0) + 1

class expr_end(expr_rng):
    
    def __init__(self):
        super(expr_end, self).__init__('expr_end')
    
    def eval(self, out, pool, srci, t = 0):
        super(expr_end, self).eval(out, pool, srci, t)
        pool.cur['expr_cnt'] = pool.get('expr_cnt', 0) - 1

class stack_sym(opelem):
    
    def _stack(self, pool):
        stack = pool.get_base('__evm_stack', [])
        pool.base['__evm_stack'] = stack
        return stack
    
    def _shallow_clone(self, src):
        return {k: src[k] for k in src if k[:5] != '__evm'}
    
    def stack_push(self, pool):
        cur = self._shallow_clone(pool.cur)
        self._stack(pool).append(cur)
        pool.cur = cur
    
    def stack_pop(self, pool):
        stack = self._stack(pool)
        if len(stack) == 0:
            raise opex_error_syntax()
        stack.pop()
        if len(stack) > 0:
            pool.cur = stack[-1]
        else:
            pool.reset()

class stack_reg(stack_sym):
    
    def __init__(self):
        super(stack_reg, self).__init__('stack_reg')
    
    def eval(self, out, pool, srci, t = 0):
        super(stack_reg, self).eval(out, pool, srci, t)
        self.stack_push(pool)

class stack_rel(stack_sym):
    
    def __init__(self):
        super(stack_rel, self).__init__('stack_rel')
    
    def eval(self, out, pool, srci, t = 0):
        super(stack_rel, self).eval(out, pool, srci, t)
        self.stack_pop(pool)

class rtab_sym(opelem):
    
    def _rtab(self, pool):
        rtab = pool.get_base('__evm_rtab', [])
        pool.base['__evm_rtab'] = rtab
        return rtab
        
    def rtab_push(self, pool, name):
        rtab = self._rtab(pool)
        itm = {'name': name, 'tab':[]}
        rtab.append(itm)
    
    def rtab_pop(self, pool):
        rtab = self._rtab(pool)
        rtab.pop()

class var(rtab_sym):
    
    def __init__(self, id):
        super(var, self).__init__('var_' + id)
        self.name = id
    
    def eval(self, out, pool, srci, t = 0):
        super(var, self).eval(out, pool, srci, t)
        self.outself(out, t)

class rtab_reg(rtab_sym):
    
    def __init__(self):
        super(rtab_reg, self).__init__('rtab_reg')
    
    def eval(self, out, pool, srci, t = 0):
        super(rtab_reg, self).eval(out, pool, srci, t)
        prevop = out.pop()
        if not isinstance(prevop, var):
            raise opex_error_syntax()
        self.rtab_push(pool, prevop.name)

class find_comb(opelem):
    
    def __init__(self):
        pass

class appl(opelem):
    
    def __init__(self):
        super(appl, self).__init__('appl')
    
    def eval(self, out, pool, srci, t = 0):
        super(appl, self).eval(out, pool, srci, t)

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
        src_q.append(comb_rcptr())
        src_q.append(var('a0'))
        src_q.append(comb_rcptr_tbp())
        src_q.append(expr_bypass())
        src_q.append(expr_start())
        src_q.append(var('a1'))
        src_q.append(expr_start())
        src_q.append(var('b1'))
        src_q.append(expr_start())
        src_q.append(var('c1'))
        src_q.append(expr_end())
        src_q.append(expr_end())
        src_q.append(expr_start())
        src_q.append(var('b2'))
        src_q.append(expr_end())
        src_q.append(expr_end())
        src_q.append(var('a2'))
        src_q.append(comb())
        src_q.append(comb_rcptr())
        src_q.append(var('a3'))
        src_s = _eval_scanner(src_q, _base_pool())
        src_s.scan()
        print(src_s.out._seq)
    test2()

