Django 1.7 and later
====================

In Django 1.7 the problem has been fixed:

>>> from django import VERSION
>>> VERSION[1] > 6
True

>>> from main.models import PizzeriaBar
>>> p = PizzeriaBar(name="Mike's", pizza_bar_specific_field="Doodle")
>>> print(p.name)
Mike's

>>> p.pizza_bar_specific_field
'Doodle'
