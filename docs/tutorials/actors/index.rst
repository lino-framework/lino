======================
The label of the actor
======================

This is a rather subtle tutorial about the 
:attr:`label <lino.core.actors.Actor.label>`. 
of an :class:`Actor<lino.core.actors.Actor>`
It was started as a doctest for
:blogref:`20130907`.

.. include:: /include/wip.rst

Actors are one of the concepts which Lino adds to Django.

Here is the :xfile:`models.py` file we will use for this tutorial:

.. literalinclude:: models.py
  
Some setup for doctest:
  
>>> from lino.api.shell import *
>>> globals().update(actors.__dict__)


The `label` of an Actor
-----------------------

If a Table has no explicit `label` attribute, then it 
takes the verbose_name_plural meta option of the model:

>>> print(Partners.label)
Partners
>>> print(Persons.label)
Persons

You may specify an explicit constant `label` attribute:

>>> print(FunnyPersons.label)
Funny persons

In versions after :blogref:`20130907` this explicit label attribute 
is also inherited to subclasses:

>>> print(MyFunnyPersons.label)
Funny persons


Dynamic actor labels
--------------------

.. literalinclude:: dynamic_labels.py

The following fails:

>>> print(Customers.label) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
Traceback (most recent call last):
...
DoesNotExist: PartnerType matching query does not exist.

That's correct. Because accessing the `label` property will read it 
from the database. We must first fill these rows:

>>> PartnerType(id=Customers.partner_type_pk,name="Our customers").save()
>>> PartnerType(id=Providers.partner_type_pk,name="Our providers").save()

Now it works:

>>> print(Customers.label)
Our customers

>>> print(Providers.label)
Our providers




>>> # Customers.make_instance(name="Adams")
>>> # Customers.make_instance(name="Bowman")
>>> # Providers.make_instance(name="Carlsson")
>>> # Customers.make_instance(name="Dickens")




