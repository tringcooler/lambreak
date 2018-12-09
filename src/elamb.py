#! python3
# coding: utf-8

class _elamb:

    def __init__(self, in_stack, out_stack):
        self._stat = 'init'

    

class meta_elamb(type):

    def __new__(meta_cls, name, base_cls, attrs):
        base_cls = base_cls + (_elamb,)
        return super(meta_elamb, meta_cls).__new__(
            meta_cls, name, base_cls, attrs)
