========================================
Assigning float values to a DecimalField
========================================

.. This document is part of the test suite.  
   To test only this  document, run:

    $ python setup.py test -s tests.DocsTests.test_float2decimal

    doctest init:

    >>> from __future__ import print_function
    >>> from lino.api.shell import *
    >>> globals().update(float2decimal.__dict__)

When using Python 2.7 or later together with older Django versions, it
wasn't a good idea to assign float values to a DecimalField because
although Django doesn't complain at first, and although the values get
stored in the instance object, you'll get a TypeError when you try to
save the object::

    >> a = A(price=2.50, qty=8.0)
    >> a.total()
    20.00
    >> a.save() #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert float to Decimal.  First convert the float to a string  
      
This document shows that the problem has been removed. It is being
tested only when using Python 2.7 or later because with earlier Python
versions the exception would raise already before storing the value.

This test article uses a single model:

.. literalinclude:: models.py

It is okay to assign integer values to DecimalFields:

>>> a = A(price=10, qty=2)
>>> a.total()
20

>>> a.save()
>>> pk = a.pk
>>> a = A.objects.get(pk=pk)
>>> print '{0:.2f}'.format(a.total())
20.00

(Note: unformatted output of above snippet differs between Django
versions 1.6 and 1.8)

>>> a = A(price=2.50, qty=8.0)
>>> a.total()
20.0
>>> a.save()

>>> import decimal
>>> a = A(price=decimal.Decimal('2.50'), qty=8)
>>> a.total()
Decimal('20.00')
>>> a.save()

>>> a = A(price=decimal.Decimal('2.20'), qty=decimal.Decimal('2.2'))
>>> a.total()
Decimal('4.840')
>>> a.save()

