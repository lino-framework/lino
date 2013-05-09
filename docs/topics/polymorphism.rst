.. _polymorphism:

============
Polymorphism
============

There are different methods to implement `Polymorphism 
<http://stackoverflow.com/questions/45621/how-do-you-deal-with-polymorphism-in-a-database>`__.
in a relational database.
To use Martin Frowler's classification:

- `Single Table Inheritance <http://www.martinfowler.com/eaaCatalog/singleTableInheritance.html>`__:
  corresponds to Django's single-table model inheritance.
  
- `Class Table Inheritance <http://www.martinfowler.com/eaaCatalog/classTableInheritance.html>`__
  corresponds to Django's multi-table model inheritance
  and Lino adds some tools for using it: :doc:`mti`.

- `Concrete Table Inheritance <http://www.martinfowler.com/eaaCatalog/concreteTableInheritance.html>`__

Lino also provides methods to make the implementation 
choice itself transparent
(we are working on it: :doc:`/tickets/72`)

Polymorphism without using MTI:

- See :mod:`lino.modlib.partners` for example.

- :meth:`lino.core.model.Model.get_typed_instance` 


