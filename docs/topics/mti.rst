Polymorphism
============

Django's `Multi-table inheritance
<http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`__
(MTI) is a great feature,
but when using it in practice 
we face some typical "user-side" problems.
:doc:`Ticket #22 </tickets/22>` gives 
an introduction to these.

Lino adds some features to solve these problems using an
intuitive user interface for managing MTI:

- a special CheckBox widget that allows to create/delete MTI 
  children from an MTI parent's view.
- inheriting Detail forms from MTI parent model

See also:

- :mod:`lino.utils.mti`
- :mod:`lino.test_apps.1.models`
