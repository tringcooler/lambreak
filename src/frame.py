#! python3
# coding: utf-8

from functools import wraps

class _eval_stack(object):

    def __init__(self):
        self._seq = []

    def push(self, dst):
        self._seq.append(dst)

    def pop(self):
        return self._seq.pop()

    def walk_gen(self):
        return iter(self._seq)

class frame(object):

    def __init__(self, pred = None):
        self._pred = pred
        self._succ = None
        self._stack = _eval_stack()

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

    def dec_active(meth):
        @wraps(meth)
        def _wrapper(self, *args, **kargs):
            if not self.is_last:
                raise RuntimeError('frame is not active')
            return meth(self, *args, **kargs)
        return _wrapper

    @dec_active
    def eval(self):
        pass
