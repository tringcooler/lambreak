#! python3
# coding: utf-8

from functools import wraps

class frame(object):

    def __init__(self, pred = None):
        self._pred = pred
        self._succ = None
        self._stack = _eval_stack()
        self._stat = 'init'

    def _append_new(self):
        assert self._succ == None 
        new_frame = frame(self)
        self._succ = new_frame

    @property
    def is_last(self):
        return not self._succ

    @property
    def is_first(self):
        return not self._pred

    @property
    def succ(self):
        if self.is_last:
            self._append_new()
        return self._succ

    @property
    def pred(self):
        return self._pred

    @property
    def last(self):
        cur = self
        while not cur.is_last:
            cur = cur._succ
        return cur

    @property
    def first(self):
        cur = self
        while not cur.is_first:
            cur = cur._pred
        return cur

    def dec_stat(stat):
        def _dec(meth):
            @wraps(meth)
            def _wrapper(self, *args, **kargs):
                if not self._stat == stat:
                    raise RuntimeError('frame is not ' + stat)
                return meth(self, *args, **kargs)
            return _wrapper
        return _dec

    @dec_stat('init')
    def raw(self, code):
        for elamb in code:
            self._stack.push(elamb)
        self._stat = 'ready'

    @dec_stat('ready')
    def eval_gen(self):
        succ = self.succ
        self._stat = 'run'
        for elamb in self._stack.walk_gen():
            yield
        self.succ._stat = 'ready'
        self._stat = 'done'


