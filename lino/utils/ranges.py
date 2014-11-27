# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.utils.ranges` module contains utility methods for
working with "ranges".

This docstring is part of the Lino test suite. To test only this
module, run::

  $ python setup.py test -s tests.UtilsTests.test_ranges

A range is basically a tuple of two values `a` and `b`, called also
limits, who indicate the start and the end of the range.

An open range is a range that has at least one limit set to `None`.



"""


def constrain(value, lowest, highest):
    """Test whether `value` is within the range `(highest, lowest)`.
    Return `value` if it is inside the range, otherwise return
    `highest` if the value is *above* the range or `lowest` it the value
    is *below* the range.

    >>> constrain(-1, 2, 5)
    2
    >>> constrain(1, 2, 5)
    2
    >>> constrain(0, 2, 5)
    2
    >>> constrain(2, 2, 5)
    2
    >>> constrain(3, 2, 5)
    3
    >>> constrain(5, 2, 5)
    5
    >>> constrain(6, 2, 5)
    5
    >>> constrain(10, 2, 5)
    5

    """
    return min(highest, max(value, lowest))


def encompass(a, b):
    """
    Test whether range `a` encompasses (is wider than) range `b`.
    
    >>> encompass((1, 4), (2, 3))
    True
    >>> encompass((1, 3), (2, 4))
    False
    >>> encompass((None, None), (1, 4))
    True
    >>> encompass((1, None), (1, 4))
    True
    >>> encompass((2, None), (1, None))
    False
    >>> encompass((1, None), (2, None))
    True
    >>> encompass((1, 4), (1, 4))
    True
    >>> encompass((1, 2), (1, None))
    False
    """
    if a[0] is None:
        if a[1] is None:
            return True
        if b[1] is None:
            return False
        return (b[1] <= a[1])
    else:
        if b[0] is None or b[0] < a[0]:
            return False
        if a[1] is None:
            return True
        if b[1] is None:
            return False
        return a[1] >= b[1]


def isrange(a, b):
    """
    Return True if the passed tuple `(a,b)` is a valid range
    (that is, `a` may not be greater than `b`).
    """
    #~ if r[0] is None or r[1] is None: return True
    #~ if r[0] <= r[1]: return True
    if a is None or b is None:
        return True
    if a <= b:
        return True
    return False


def overlap2(a, b):
    """
    Same as :func:`overlap` but with different signature.
    """
    return overlap(a[0], a[1], b[0], b[1])


def overlap(a1, a2, b1, b2):
    """Test whether two value ranges overlap.
    
    This function is typically used with date values, but it also
    works with integers or other comparable values.  The following
    examples use integer values to be more readable.

    Unlike the test presented at
    <http://bytes.com/topic/python/answers/457949-determing-whether-two-ranges-overlap>,
    this works also with "open" ranges (the open end being indicated
    by a `None` value).
    
    Types of constellations::
    
      -   o---o  o---o
      -   o---o  o--->
      -   <---o  o---o
      -   <---o  o--->
                
      -   o------------->
                o---o
                
      -   o---o
            o---o
                
      -   o---o
            o--->
      -   <---------o
               o---o
    


    >>> overlap(1,2,3,4)
    False
    >>> overlap(3,4,1,2)
    False
    >>> overlap(1,3,2,4)
    True
    >>> overlap(2,4,1,3)
    True
    >>> overlap(1,4,2,3)
    True
    >>> overlap(2,3,1,4)
    True
    
    
    >>> overlap(1,None,3,4)
    True
    >>> overlap(3,4,1,None)
    True
    
    
    >>> overlap(1,2,3,None)
    False
    >>> overlap(3,None,1,2)
    False
    
    >>> overlap(None,2,3,None)
    False
    >>> overlap(3,None,None,2)
    False
    
    >>> overlap(1,3,2,None)
    True
    
    Ranges that "only touch" each other are not considered overlapping:
        
    >>> overlap(1,2,2,3)
    False
    >>> overlap(2,3,1,2)
    False

    """

    #~ return a2 > b1 and a1 < b2

    if a2:
        if b1:
            if b1 >= a2:
                return False
            else:
                if b2 and a1:
                    if a1 > a2:
                        raise ValueError("Range 1 ends before it started.")
                    return b2 > a1
                else:
                    return True
        else:
            if b2 and a1:
                return b2 >= a1
            else:
                return True
    elif b2:
        if a1:
            return b2 > a1
        else:
            return True
    return True


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
