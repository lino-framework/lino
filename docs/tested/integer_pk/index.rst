Do not define IntegerField as explicit primary_key field
========================================================

.. include:: /include/wip.rst

.. This document is part of the test suite.  To test only this
   document, run::

     $ python setup.py test -s tests.DocsTests.test_integer_pk

.. 
    >>> from __future__ import print_function
    >>> from lino.api.shell import *
    >>> globals().update(integer_pk.__dict__)

Here are the models used for this test:

.. literalinclude:: models.py

If you define an IntegerField as explicit primary_key field, you'll 
get unexpected behaviour:

  >>> p = IntegerPerson(name="Luc")
  >>> p.save() 
  >>> p.save() 
  >>> IntegerPerson.objects.all()
  [<IntegerPerson: Luc>, <IntegerPerson: Luc>]

Oops! The second `save()` has created a second instance!
That's not normal. 

It is not normal because there's nothing wrong with 
saving your object a second time.
A second call to save is just useless but should not 
create a second instance.
Here are some examples:

  >>> p = AutoPerson(name="Luc")
  >>> p.save() 
  >>> p.save() 
  >>> AutoPerson.objects.all()
  [<AutoPerson: Luc>]
  
Implicit primary key:  

  >>> p = Person(name="Luc")
  >>> p.save() 
  >>> p.save() 
  >>> Person.objects.all()
  [<Person: Luc>]

CharField as primary key:

>>> p = CharPerson(name="Luc")
>>> p.save() 
>>> p.save() 
>>> CharPerson.objects.all()
[<CharPerson: Luc>]

