Multi-table inheritance 
=======================

Django's `Multi-table inheritance
<http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`__
(MTI) is a great feature to map 
`Polymorphism 
<http://stackoverflow.com/questions/45621/how-do-you-deal-with-polymorphism-in-a-database>`_.
into a relational database.

Lino provides an intuitive user interface for managing MTI
by adding some features:

- a special CheckBox widget 
  (:class:`EnableChild <lino.utils.mti.EnableChild>`) 
  that allows to 
  convert existing data records into a more specialized child model, 
  or back into a less specialized parent model.
  
- :doc:`/topics/layouts` can inherit from their MTI parent model's layout.


See also:

- :doc:`/tickets/22` gives an introduction to MTI
- :doc:`/autodoc/lino.test_apps.mti`.
