# Copyright 2015-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

'''This defines the :class:`Counter` class, a utility used in Jinja
templates to generate self-incrementing counters for sections,
subsections and any other sequences.

.. to run only this test:

  $ python setup.py test -s tests.DocsTests.test_jinja


Installation
============

You can add the `Counter` class either to your local context or to the
`global namespace
<http://jinja.pocoo.org/docs/dev/api/#global-namespace>`__.

>>> from jinja2 import Environment
>>> from lino.utils.jinja import Counter
>>> env = Environment()
>>> env.globals.update(Counter=Counter)


Basic usage in a template
=========================

Using the `Counter` in your template is easy: You instantiate a
template variable of type :class:`Counter`, and then call that counter
each time you want a new number.  For example:

>>> s = """
... {%- set art = Counter() -%}
... Easy as {{art()}}, {{art()}} and {{art()}}!
... """

Here is how this template will render :

>>> print(env.from_string(s).render())
Easy as 1, 2 and 3!


Counter parameters
==================

When defining your counter, you can set optional parameters.

>>> s = """
... {%- set art = Counter(start=17, step=2) -%}
... A funny counter: {{art()}}, {{art()}} and {{art()}}!
... """
>>> print(env.from_string(s).render())
A funny counter: 19, 21 and 23!


Resetting a counter
===================

When calling your counter, you can pass optional parameters. One of
them is `value`, which you can use to restart numbering, or to start
numbering at some arbitrary place:

>>> s = """
... {%- set art = Counter() -%}
... First use: {{art()}}, {{art()}} and {{art()}}
... Reset: {{art(value=1)}}, {{art()}} and {{art()}}
... Arbitrary start: {{art(value=10)}}, {{art()}} and {{art()}}
... """
>>> print(env.from_string(s).render())
First use: 1, 2 and 3
Reset: 1, 2 and 3
Arbitrary start: 10, 11 and 12


Nested counters
===============

Counters can have another counter as parent. When a parent increases,
all children are automatically reset to their start value.


>>> s = """
... {%- set art = Counter() -%}
... {%- set par = Counter(art) -%}
... = Article {{art()}}
... == # {{par()}}
... == # {{par()}}
... = Article {{art()}}
... == # {{par()}}
... == # {{par()}}
... == # {{par()}}
... Article {{art()}}.
... == # {{par()}}
... """
>>> print(env.from_string(s).render())
= Article 1
== # 1
== # 2
= Article 2
== # 1
== # 2
== # 3
Article 3.
== # 1

'''

from __future__ import print_function
from builtins import object


class Counter(object):
    """Represents a counter. Usage see """
    def __init__(self, parent=None, start=0, step=1):
        self.children = []
        self.start = start
        self.step = step
        self.current = start
        self.named_items = dict()
        if parent is not None:
            parent.add_child(self)

    def add_child(self, ch):
        self.children.append(ch)

    def reset(self):
        self.current = self.start
        for ch in self.children:
            ch.reset()

    def __call__(self, name=None, value=None):
        if value is None:
            self.current += self.step
        else:
            self.current = value
        for ch in self.children:
            ch.reset()
        if name:
            if name in self.named_items:
                raise Exception("Cannot redefine name '{0}'.".format(name))
            self.named_items[name] = self.current
        return self.current

    def get(self, name):
        return self.named_items[name]()


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
