Django 1.6
==========

Under Django 1.6 we will have:

>>> from django import VERSION
>>> VERSION[:2]
(1, 6)

>>> from main.models import PizzeriaBar
>>> p = PizzeriaBar(name="Michaels", min_age=21, specialty="Cheese", pizza_bar_specific_field="Doodle")
>>> print (p.name, p.min_age, p.specialty, p.pizza_bar_specific_field)
(u'', 21, 'Cheese', 'Doodle')

>>> len(p.name)
0
>>> print(p.name)
<BLANKLINE>
>>> p.pizza_bar_specific_field
'Doodle'

That is, the `name` field has not been initialized because it is being
inherited from a grand-parent.
