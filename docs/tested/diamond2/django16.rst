Django 1.6
==========

Here is how we can fix this under Django 1.6 by running
:func:`lino.core.inject.django_patch`.

>>> from django import VERSION
>>> VERSION[:2]
(1, 6)

>>> from lino.core.inject import django_patch
>>> django_patch()

And now we have the correct behaviour:

>>> from main.models import Person
>>> p = Person(a="A", b="B", c="C", d="D", e="E")
>>> p.full_clean()
>>> print(p.a)
A
