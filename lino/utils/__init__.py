## Copyright 2009-2010 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""


>>> constrain(-1,2,5)
2
>>> constrain(1,2,5)
2
>>> constrain(0,2,5)
2
>>> constrain(2,2,5)
2
>>> constrain(3,2,5)
3
>>> constrain(5,2,5)
5
>>> constrain(6,2,5)
5
>>> constrain(10,2,5)
5


:func:`iif` (inline ``if``)
---------------------------

>>> iif(1>2,'yes','no')
'no'

:func:`str2hex` and :func:`hex2str`
-----------------------------------

>>> str2hex('-L')
'2d4c'

>>> hex2str('2d4c')
'-L'

>>> hex2str('')
''
>>> str2hex('')
''


"""


import os, sys, locale, types, datetime
from dateutil import parser as dateparser
import stat

def constrain(value,lowest,highest):
    return min(highest,max(value,lowest))

def confirm(prompt=None):
    while True:
        ln = raw_input(prompt)
        if ln.lower() in ('y','j','o'):
            return True
        if ln.lower() == 'n':
            return False
        print "Please anwer Y or N"

def iif(l,y,f): 
    if l: return y 
    return f
    
def isiterable(x):
    "Returns `True` if the specified object is iterable."
    try:
        it = iter(x)
    except TypeError: 
        return False
    return True
    
    
def ispure(s):
    """Returns `True` if the specified string `s` is either a unicode 
    string or contains only ASCII characters."""
    if s is None: return True 
    if type(s) == types.UnicodeType:
        return True
    if type(s) == types.StringType:
        try:
            s.decode('ascii')
        except UnicodeDecodeError,e:
            return False
        return True
    return False

def assert_pure(s):
    assert ispure(s), "%r: not pure" % s
     

def join_words(*words):
    """Removes any None. Calls unicode on each.
    """
    #~ words = filter(lambda x:x,words)
    return ' '.join([unicode(x) for x in words if x])
      

def d2iso(d):
    "Supports also dates before 1900."
    return "%04d-%02d-%02d" % (d.year, d.month, d.day)

def i2d(i):
    d = dateparser.parse(str(i))
    d = datetime.date(d.year,d.month,d.day)
    #print i, "->", v
    return d
    
def get_class_attr(cl,name):
    value = getattr(cl,name,None)
    if value is not None:
        return value
    for b in cl.__bases__:
        value = getattr(b,name,None)
        if value is not None:
            return value
            
def class_dict_items(cl,exclude=None):
    if exclude is None:
        exclude = set()
    for k,v in cl.__dict__.items(): 
        if not k in exclude:
            yield k,v
            exclude.add(k)
    for b in cl.__bases__:
        for k,v in class_dict_items(b,exclude): 
            yield k,v


def call_optional_super(cls,self,name,*args,**kw):
    """
    Doesn't work. See :doc:`/blog/2011/0914`.
    """
    s = super(cls,self)
    m = getattr(s,'name',None)
    if m is not None:
        return m(*args,**kw)

def call_on_bases(cls,name,*args,**kw):
    """
    Doesn't work. See :doc:`/blog/2011/0914`.
    This is necessary because we want to call `setup_report`
    on the model and all base classes of the model.
    We cannot use super() for this because the `setup_report` 
    method is optional.
    """
    for b in cls.__bases__: call_on_bases(b,name,*args,**kw)
    if True:
        m = getattr(cls,name,None)
        # getattr will also return the classmethod defined on a base class, 
        # which has already been called. 
        if m is not None and m.im_class is cls:
            m(cls,*args,**kw)
        
    """Note: the following algorithm worked in Python 2.7 but not in 2.6,
    a classmethod object in 2.6 has no attribute `im_func`
    """
      
    #~ m = cls.__dict__.get(name)
    #~ if m:
        #~ func = getattr(m,'im_func',None)
        #~ if func is None:
            #~ raise Exception("Oops, %r in %s (%r) has no im_func" % (name,cls,m))
        #~ func(cls,*args,**kw)
        #~ # m.__func__(cls,*args,**kw)




def str2hex(s):
    """Convert a string to its hexadecimal representation."""
    r = ''
    for c in s:
        r += hex(ord(c))[2:]
    return r
    
def hex2str(value):
    """Convert the hexadecimal representation of a string to the original string."""
    if len(value) % 2 != 0:
        raise Exception("hex2str got value %r" % value)
    r = ''
    for i in range(len(value) / 2):
       s = value[i*2:i*2+2]
       h = int(s,16)
       r += chr(h)
    return r
    
# http://snippets.dzone.com/posts/show/2375
curry = lambda func, *args, **kw:\
            lambda *p, **n:\
                 func(*args + p, **dict(kw.items() + n.items()))
                 
    

def codetime():
    """
    Return the modification time of the youngest source code in memory.
    Used by :mod:`lino.ui.extjs3.ext_ui` to avoid generating lino.js files if not necessary.
    Inspired by the code_changed() function in django.utils.autoreload.
    """
    code_mtime = None
    for filename in filter(lambda v: v, map(lambda m: getattr(m, "__file__", None), sys.modules.values())):
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"
        if not os.path.exists(filename):
            continue # File might be in an egg, so it can't be reloaded.
        stat = os.stat(filename)
        mtime = stat.st_mtime
        #~ print filename, time.ctime(mtime)
        if code_mtime is None or code_mtime < mtime:
            code_mtime = mtime
    return code_mtime
    
    
class IncompleteDate:
    """
    Naive representation of an incomplete gregorian date.
    
    >>> print IncompleteDate(2011,0,0).strftime("%d.%m.%Y")
    00.00.2011
    >>> print IncompleteDate(1532,0,0)
    1532-00-00
    >>> print IncompleteDate(1990,0,1)
    1990-00-01
    >>> print IncompleteDate(0,6,1)
    0000-06-01
    
    Christ's birth date:
    
    >>> print IncompleteDate(-7,12,25)
    -7-12-25
    >>> print IncompleteDate(-7,12,25).strftime("%d.%m.%Y")
    25.12.-7
    
    An IncompleteDate is allowed to be complete:
    
    >>> d = IncompleteDate.parse('2011-11-19')
    >>> print d
    2011-11-19
    >>> d.is_complete()
    True
    
    """
    
    def __init__(self,year,month,day):
        self.year, self.month, self.day = year, month, day
        
    @classmethod
    def parse(cls,s):
        if s.startswith('-'):
            bc = True
            s = s[1:]
        else:
            bc = False
        y,m,d = map(int,s.split('-'))
        if bc: y = - y
        return cls(y,m,d)
        
    @classmethod
    def from_date(cls,date):
        return cls(date.year,date.month,date.day)
        
        
    def is_complete(self):
        if self.year and self.month and self.day:
            return True
        return False
        
    def __eq__(self,other):
        return str(self) == str(other)
        
    def __ne__(self,other):
        return str(self) != str(other)

    def __len__(self):
        return len(str(self))
        
    def __repr__(self):
        return "IncompleteDate(%r)" % str(self)
        
    def __str__(self):
        return self.strftime()
        
    def strftime(self,fmt="%Y-%m-%d"):
        #~ s = fmt.replace("%Y",iif(self.bc,'-','')+str(self.year))
        if self.year == 0:
            s = fmt.replace("%Y",'0000')
        else:
            s = fmt.replace("%Y",str(self.year))
        s = s.replace("%m","%02d" % self.month)
        s = s.replace("%d","%02d" % self.day)
        return s
        
        #~ return self.strftime_(fmt,
            #~ iif(self.bc,-1,1)*self.year,
            #~ self.month,
            #~ self.day)
        
        
    def as_date(self):
        return datetime.date(
            #~ (self.year * iif(self.bc,-1,1)) or 1900, 
            self.year or 1900, 
            self.month or 1, 
            self.day or 1)
        



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

