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

class evmac(object):

    def __init__(self, seq_in):
        self._seq_in = seq_in
        self._tab_rep = _replace_table()

    def _find_act_op(self, src, out):
        while src.next():
            if src.cur.can('feed') and src.peek.can('eval'):
                src.next()
                break
            out.append(src.cur)

    def _scan_1(self):
        src = seq_in.walk_gen()
        seq_out = _eval_seq()
        self._find_act_op(src, seq_out)
        eval_op = src.cur
        if not eval_op:
            return
        

    def eval(self):
        pass
