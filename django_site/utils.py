class AttrDict(dict):
    """
    Usage example:
    
    >>> a = AttrDict()
    >>> a.define('foo',1)
    >>> a.define('bar','baz',2)
    >>> print a
    {'foo': 1, 'bar': {'baz': 2}}
    >>> print a.foo
    1
    >>> print a.bar.baz
    2
    >>> print a.resolve('bar.baz')
    2
    >>> print a.bar
    {'baz': 2}
    
    """
  
    def __getattr__(self, name):
        #~ if self.has_key(name):
        return self[name]
        #~ raise AttributeError("%r has no attribute '%s'" % (self,name))
        
    def define2(self,name,value):
        return self.define(*name.split('.')+[value])
        
    def define(self,*args):
        "args must be a series of names followed by the value"
        assert len(args) >= 2
        d = s = self
        for n in args[:-2]:
            d = s.get(n,None)
            if d is None:
                d = AttrDict()
                s[n] = d
            s = d
        oldvalue = d.get(args[-2],None)
        #~ if oldvalue is not None:
            #~ print 20120217, "Overriding %s from %r to %r" % (
              #~ '.'.join(args[:-1]),
              #~ oldvalue,
              #~ args[-1]
              #~ )
        d[args[-2]] = args[-1]
        return oldvalue
    
    def resolve(self,name,default=None):
        """
        return an attribute with dotted name
        """
        o = self
        for part in name.split('.'):
            o = getattr(o,part,default)
            # o = o.__getattr__(part)
        return o
        

class Cycler:
    """
    Turns a list of items into an endless loop.
    Useful when generating demo fixtures.
    
    >>> def myfunc():
    ...     yield "a"
    ...     yield "b"
    ...     yield "c"
    
    >>> c = Cycler(myfunc())
    >>> s = ""
    >>> for i in range(10):
    ...     s += c.pop()
    >>> print s
    abcabcabca
    
    A Cycler on an empty list will endlessly pop None values:
    
    >>> c = Cycler([])
    >>> print c.pop(), c.pop(), c.pop()
    None None None
    
    """
    def __init__(self,*args):
        if len(args) == 0:
            raise ValueError()
        elif len(args) == 1:
            self.items = list(args[0])
        else:
            self.items = args
        self.current = 0
        
    def pop(self):
        if len(self.items) == 0: return None
        item = self.items[self.current]
        self.current += 1
        if self.current >= len(self.items):
            self.current = 0
        if isinstance(item,Cycler):
            return item.pop()
        return item
        
    def __len__(self):
        return len(self.items)
        
    def reset(self):
        self.current = 0
        


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

