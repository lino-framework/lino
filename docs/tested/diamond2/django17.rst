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

And now it works also with abstract parents:

>>> from main.models import PizzeriaBar
>>> p = PizzeriaBar(name="A", min_age="B", specialty="C",
...     pizza_bar_specific_field="Doodle")
>>> print(p.name)
A
>>> print(p.pizza_bar_specific_field)
Doodle

