"""
>>> def fn(arg1,arg2): pass
>>> co = fn.func_code
>>> co.co_argcount
2
>>> co.co_varnames
('arg1', 'arg2')

"""

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

