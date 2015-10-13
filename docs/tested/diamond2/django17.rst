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


Unfortunately although above code snippet passes, there seems to be
still problems since :mod:`lino.projects.min2` which (under Django
1.7+) says::

  contacts.Person.addr1: (models.E006) The field 'addr1' clashes with the field 'addr1' from model 'contacts.partner'.

Let's look together into :mod:`lino.core.inject`.

The problem comes (probably) because the `name` field occurs *twice*
in the list of fields:
>>> from lino import AFTER17
>>> if AFTER17:
...     [f.name for f in PizzeriaBar._meta.get_fields()]
... else:
...     [f.name for f in PizzeriaBar._meta.get_fields()]
[u'id', 'street', 'name', 'specialty', u'pizzeria_ptr', 'street', 'name', 'min_age', 'pizza_bar_specific_field']
