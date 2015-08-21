Django 1.6
==========

Under Django 1.6 we will have:

>>> from django import VERSION
>>> VERSION[:2]
(1, 6)

>>> from main.models import PizzeriaBar
>>> p = PizzeriaBar(name="Mike's", pizza_bar_specific_field="Doodle")

>>> len(p.name)
0
>>> print(p.name)
<BLANKLINE>
>>> p.pizza_bar_specific_field
'Doodle'

That is, the `name` field has not been initialized because it is being
inherited from a grand-parent.
