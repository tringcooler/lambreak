#! python3
# coding: utf-8

class opex_base(Exception):
    pass

class opex_scan_done(opex_base):
    pass

class opex_scan_bypass(opex_base):
    pass
