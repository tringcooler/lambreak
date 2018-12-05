#! python3
# coding: utf-8

class _eval_stack(object):

    def __init__(self):
        pass

    def push(self, dst):
        pass

    def pop(self):
        pass

    def walk(self):
        pass

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
    def succ(self):
        if not self._succ:
            self._append_new()
        return self._succ

    @property
    def pred(self):
        return self._pred

    @property
    def last(self):
        cur = self
        while cur._succ:
            cur = cur._succ
        return cur

    @property
    def first(self):
        cur = self
        while cur._pred:
            cur = cur._pred
        return cur
