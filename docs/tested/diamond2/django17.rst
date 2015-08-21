Django 1.7 and later
====================

Under Django 1.7 and later we have:

>>> from django import VERSION
>>> VERSION[1] > 6
True

Again we run :func:`lino.core.inject.django_patch` in order to fix the
problem:

>>> from lino.core.inject import django_patch
>>> django_patch()

But currently the following code still fails:

>>> from main.models import Person
>>> p = Person(a="A", b="B", c="C", d="D", e="E")
>>> p.full_clean()
>>> print(p.a)
A
