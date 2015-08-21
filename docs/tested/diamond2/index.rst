.. _lino.tested.diamond2:

===============================
Diamond inheritance (continued)
===============================

.. This document is part of the test suite.  
   To test only this  document, run:

    $ python setup.py test -s tests.DocsTests.test_diamond2

    doctest init:

    >>> from __future__ import print_function

This document shows a more complex case of multi-table diamond
inheritance which is still broken in Django 1.7.
Compare :doc:`../diamond/index` 
for a predecessor of this problem.

This document also shows that Lino has a work-around for both
problems. Unfortunately that workaround works only until Django
1.6. We are trying to adapt it to newer Django versions.


Here is our database structure:

.. literalinclude:: main/models.py


The problem
===========


>>> from main.models import Person
>>> p = Person(a="A", b="B", c="C", d="D", e="E")

Despite the fact that we specify a non-blank value for `a`, we get:

>>> p.full_clean()
Traceback (most recent call last):
...
ValidationError: {'a': [u'This field cannot be blank.'], 'b': [u'This field cannot be blank.']}

And indeed the `a` field is blank, while the `e` field is not:

>>> print(p.a)
<BLANKLINE>
>>> print(p.e)
E


.. include:: django16.rst
.. include:: django17.rst


.. toctree::
    :hidden:

    django16
    django17
