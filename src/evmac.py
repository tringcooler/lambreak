#! python3
# coding: utf-8

class _es_iter(object):

    def __init__(self, src):
        self._iter = iter(src)
        self._peek = None
        self.next()

    @property
    def cur(self):
        return self._cur

    @property
    def peek(self):
        if not self._peek:
            self._peek = next(self._iter, None)
        return self._peek

    def next(self):
        self._cur = self.peek
        self._peek = None
        return self.cur

class _eval_stack(object):

    def __init__(self):
        self._seq = []

    def push(self, dst):
        self._seq.append(dst)

    def pop(self):
        return self._seq.pop()

    def walk_gen(self):
        return _es_iter(self._seq)

class _replace_table(object):

    def __init__(self):
        pass

class evmac(object):

    def __init__(self, seq_in):
        self._seq_in = seq_in
        self._tab_rep = _replace_table()

    def _find_act_op(self, src):
        seq_out = _eval_stack()
        while src.cur:
            if not src.cur.can('eval'):
                break
            src.next()
        return src

    def _scan_1(self):
        src = seq_in.walk_gen()
        self._find_act_op(src)

    def eval(self):
        pass
