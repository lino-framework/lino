# -*- coding: UTF-8 -*-
# Copyright 2013-2014 by Rumma & Ko Ltd.
# License: BSD, see LICENSE for more details.

"""
Turns a list of items into an endless loop.
Useful when generating demo fixtures.

>>> from lino.utils import Cycler
>>> def myfunc():
...     yield "a"
...     yield "b"
...     yield "c"

>>> c = Cycler(myfunc())
>>> s = ""
>>> for i in range(10):
...     s += c.pop()
>>> print (s)
abcabcabca

An empty Cycler or a Cycler on an empty list will endlessly pop None values:

>>> c = Cycler()
>>> print (c.pop(), c.pop(), c.pop())
None None None

>>> c = Cycler([])
>>> print (c.pop(), c.pop(), c.pop())
None None None

>>> c = Cycler(None)
>>> print (c.pop(), c.pop(), c.pop())
None None None
"""

from __future__ import unicode_literals
from __future__ import print_function
from builtins import object


class Cycler(object):

    def __init__(self, *args):
        """
        If there is exactly one argument, then this must be an iterable
        and will be used as the list of items to cycle on.
        If there is more than one positional argument, then these
        arguments themselves will be the list of items.
        """

        if len(args) == 0:
            self.items = []
        elif len(args) == 1:
            if args[0] is None:
                self.items = []
            else:
                self.items = list(args[0])
        else:
            self.items = args
        self.current = 0

    def pop(self):
        if len(self.items) == 0:
            return None
        item = self.items[self.current]
        self.current += 1
        if self.current >= len(self.items):
            self.current = 0
        if isinstance(item, Cycler):
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
