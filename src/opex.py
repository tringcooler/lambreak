#! python3
# coding: utf-8

class opex_base(Exception):
    pass

class opex_scan(opex_base):
    pass

class opex_scan_done(opex_scan):
    pass

class opex_scan_bypass(opex_scan):
    pass
    
class opex_error(opex_base):
    pass
    
class opex_error_syntax(opex_error):
    pass
