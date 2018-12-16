#! python3
# coding: utf-8

class _es_iter(object):

    def __init__(self, src):
        self._iter = iter(src)
        self._cur = None
        self._peek = None

    @property
    def cur(self):
        assert self._cur
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

class _eval_scanner(object):

    def __init__(self, seq_in, tab_rep):
        self._src = seq_in.walk_gen()
        self._out = _eval_seq()
        self._tab = tab_rep
        self._stat = 'init'

    def _find_act_op(self, src, out):
        while self._src.next():
            if self._src.cur.can('feed') and self._src.peek.can('eval'):
                break
            self._out.append(self._src.cur)

    def scan(self):
        self._find_act_op()
        eval_op = self._src.next()
        if not eval_op:
            return

class evmac(object):

    def __init__(self, seq_in):
        self._seq_in = seq_in
        self._tab_rep = _replace_table()

    def eval(self):
        pass
