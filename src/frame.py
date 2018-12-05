#! python3
# coding: utf-8

class frame(object):

    def __init__(self, pred = None):
        self._pred = pred
        self._succ = None

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
