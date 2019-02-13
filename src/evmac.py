#! python3
# coding: utf-8

from opex import *

class _es_iter(object):

    def __init__(self, src):
        self._iter = iter(src)
        self._cur = None
        self._peek = None
        self._ahead = []

    @property
    def cur(self):
        #assert self._cur
        return self._cur

    @property
    def peek(self):
        if self._peek is None:
            if self._ahead:
                self._peek = self._ahead.pop()
            else:
                self._peek = next(self._iter, None)
        return self._peek

    def next(self):
        self._cur = self.peek
        self._peek = None
        return self.cur

    def ahead(self, val):
        if self._peek:
            self._ahead.append(self._peek)
        self._peek = val

    def second(self, val):
        self.peek
        self._ahead.append(val)

class _eval_seq(object):

    def __init__(self):
        self._seq = []

    def append(self, dst):
        self._seq.append(dst)

    def walk_gen(self):
        return _es_iter(self._seq)

class _replace_table(object):

    def __init__(self):
        pass

class _base_pool(object):

    def __init__(self):
        self._base = {}
        self.reset()

    def reset(self):
        self._cur = self._base

    @property
    def base(self):
        return self._base

    @property
    def cur(self):
        return self._cur

    @cur.setter
    def cur(self, val):
        self._cur = val

    def _get(self, pool, func, dv):
        try:
            if callable(func):
                val = func(pool)
            else:
                val = pool[func]
        except:
            val = dv
        return val

    def get(self, func, dv = None):
        return self._get(self.cur, func, dv)

    def get_base(self, func, dv = None):
        return self._get(self.base, func, dv)

class _eval_scanner(object):

    def __init__(self, seq_in, base_pool):
        self._src = seq_in.walk_gen()
        self.out = _eval_seq()
        self.pool = base_pool

    def _find_act_op(self):
        if self._src.cur.can('feed') and self._src.peek.can('eval'):
            self._stat = 'eval'
        self.out.append(self._src.cur)

    def _eval_op(self, op = None):
        if op is None:
            op = self._src.cur
        try:
            op.eval(self.out, self.pool, self._src)
        except opex_scan_done:
            return True
        except opex_scan_bypass:
            if not self._src.next():
                return True
            return self._eval_op(op)
        return False

    def scan(self):
        self.pool.reset()
        while self._src.next():
            if self._eval_op():
                break

class evmac(object):

    def __init__(self, seq_in):
        self._seq_in = seq_in
        self._base_pool = _base_pool()

    def eval(self):
        pass
