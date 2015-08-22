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

>>> from main.models import PizzeriaBar
>>> p = PizzeriaBar(name="A", min_age="B", specialty="C",
...     pizza_bar_specific_field="Doodle")
>>> print(p.name)
A
