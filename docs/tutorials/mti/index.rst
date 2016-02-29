=============================
Multi-table inheritance (MTI)
=============================


.. how to test:
    $ python setup.py test -s tests.DocsTests.test_mti



.. currentmodule:: lino.utils.mti

.. contents::
   :local:
   :depth: 2   

.. The following lines are here for running doctest 
  on this document. Sphinx removes them because they are a 
  comment, but doctest executes them.
  
  >>> from __future__ import print_function
  >>> from lino.api.shell import *
  >>> Person = mti.Person
  >>> Restaurant = mti.Restaurant
  >>> Place = mti.Place
  >>> Visit = mti.Visit
  >>> Meal = mti.Meal


The example database
--------------------

Here is the :xfile:`models.py` file used for this example.  This is
classical Django know-how: `Restaurant` inherits from `Place`, and
`Place` is *not* abstract.  That's what Django calls `multi table
inheritance
<https://docs.djangoproject.com/en/1.7/topics/db/models/#multi-table-inheritance>`_.

.. literalinclude:: models.py

The only Non-Django things in this code are that we have the `Place`
model inherit from :class:`Polymorphic
<lino.mixins.polymorphic.Polymorphic>`, that the `Meal` model has a
class attribute :attr:`allow_cascaded_delete
<lino.core.model.Model.allow_cascaded_delete>`, and the last line
which imports things from `tables.py`.  We'll talk about these later.



Create some initial data:

>>> Person(name="Alfred").save()
>>> Person(name="Bert").save()
>>> Person(name="Claude").save()
>>> Person(name="Dirk").save()
>>> r = Restaurant(id=1, name="First")
>>> r.save()
>>> for i in 1, 2:
...     r.owners.add(Person.objects.get(pk=i))
>>> for i in 3, 4:
...     r.cooks.add(Person.objects.get(pk=i))

Here is our data:

>>> Person.objects.all()
[<Person: Alfred>, <Person: Bert>, <Person: Claude>, <Person: Dirk>]

>>> Restaurant.objects.all()
[Restaurant #1 ('#1 (name=First, owners=Alfred, Bert, cooks=Claude, Dirk)')]
>>> Place.objects.all()
[Place #1 ('#1 (name=First, owners=Alfred, Bert)')]


The :func:`delete_child` function
---------------------------------

Imagine that a user of our application discovers that Restaurant #1
isn't actually a `Restaurant`, it's just a `Place`.  They would like
to "remove it's Restaurant data" from the database, but keep the
`Place` data.  Especially the primary key (#1) and the related objects
(the owners) should remain unchanged. But the cooks must be deleted
since they exist only for restaurants.

It seems that this is not trivial in Django (`How do you delete child
class object without deleting parent class object?
<http://stackoverflow.com/questions/9439730>`__).  That's why we wrote
the :func:`delete_child` function.

>>> from lino.utils.mti import delete_child

Here is how to "reduce" a Restaurant to a `Place` by 
calling the :func:`delete_child` function:

>>> p = Place.objects.get(id=1)
>>> delete_child(p, Restaurant)

The Place still exists, but no longer as a Restaurant:

>>> Place.objects.get(pk=1)
Place #1 ('#1 (name=First, owners=Alfred, Bert)')

>>> Restaurant.objects.get(pk=1)
Traceback (most recent call last):
...
DoesNotExist: Restaurant matching query does not exist.

The :func:`insert_child` function
----------------------------------

The opposite operation, "promoting a simple Place to a Restaurant", 
is done using :func:`insert_child`.

>>> from lino.utils.mti import insert_child
  
Let's first create a simple Place #2 with a single owner.

>>> obj = Place(id=2, name="Second")
>>> obj.save()
>>> obj.owners.add(Person.objects.get(pk=2))
>>> obj.save()
>>> obj
Place #2 ('#2 (name=Second, owners=Bert)')

Now this Place becomes a Restaurant and hires 2 cooks:

>>> obj = insert_child(obj, Restaurant)
>>> for i in 3, 4:
...     obj.cooks.add(Person.objects.get(pk=i))
>>> obj
Restaurant #2 ('#2 (name=Second, owners=Bert, cooks=Claude, Dirk)')

If you try to promote a Person to a Restaurant, you'll get an exception:

>>> person = Person.objects.get(pk=2)
>>> insert_child(person, Restaurant).save()
Traceback (most recent call last):
...
ValidationError: ['A Person cannot be parent for a Restaurant']


The :class:`EnableChild` virtual field 
--------------------------------------

This section shows how the :class:`EnableChild` virtual field is being 
used by Lino, and thus is Lino-specific.


After the above examples our database looks like this:

>>> Place.objects.all()
[Place #1 ('#1 (name=First, owners=Alfred, Bert)'), Place #2 ('#2 (name=Second, owners=Bert)')]
>>> Restaurant.objects.all()
[Restaurant #2 ('#2 (name=Second, owners=Bert, cooks=Claude, Dirk)')]

Let's take Place #1 and look at it.

>>> obj = Place.objects.get(pk=1)
>>> obj
Place #1 ('#1 (name=First, owners=Alfred, Bert)')

How to see whether a given Place is a Restaurant?

>>> for i in Place.objects.all():
...    print("{0} -> {1}".format(i, i.get_mti_child('restaurant')))
#1 (name=First, owners=Alfred, Bert) -> None
#2 (name=Second, owners=Bert) -> #2 (name=Second, owners=Bert, cooks=Claude, Dirk)

Let's promote First (currently a simple Place) to a Restaurant:

>>> insert_child(obj, Restaurant)
Restaurant #1 ('#1 (name=First, owners=Alfred, Bert, cooks=)')


And Second stops being a Restaurant:

>>> second = Place.objects.get(pk=2)
>>> delete_child(second, Restaurant)

This operation has removed the related Restaurant instance:

>>> Restaurant.objects.get(pk=2) 
Traceback (most recent call last):
...
DoesNotExist: Restaurant matching query does not exist.

And finally, rather to explain why Restaurants sometimes 
close and later reopen:

>>> bert = Person.objects.get(pk=2)
>>> second = Place.objects.get(pk=2)
>>> insert_child(second, Restaurant)
Restaurant #2 ('#2 (name=Second, owners=Bert, cooks=)')

Now we can see this place again as a Restaurant

>>> second = Restaurant.objects.get(pk=2)

And engage for example a new cook:

>>> second.cooks.add(bert)
>>> second
Restaurant #2 ('#2 (name=Second, owners=Bert, cooks=Bert)')



Related objects
---------------

Now let's have a more detailed look at what happens to the related 
objects (Person, Visit and Meal).

Bert, the owner of Restaurant #2 does two visits:

>>> second = Restaurant.objects.get(pk=2)
>>> Visit(purpose="Say hello", person=bert, place=second).save()
>>> Visit(purpose="Hang around", person=bert, place=second).save()
>>> second.visit_set.all()
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]

Claude and Dirk, now workless, still go to eat in restaurants:

>>> Meal(what="Fish",person=Person.objects.get(pk=3),restaurant=second).save()
>>> Meal(what="Meat",person=Person.objects.get(pk=4),restaurant=second).save()
>>> second.meal_set.all()
[<Meal: Claude eats Fish at Second>, <Meal: Dirk eats Meat at Second>]

Now we reduce Second to a Place:

>>> second = Place.objects.get(pk=2)
>>> delete_child(second, Restaurant)

Restaurant #2 no longer exists:

>>> Restaurant.objects.get(pk=2)
Traceback (most recent call last):
...
DoesNotExist: Restaurant matching query does not exist.

Note that `Meal` has :attr:`allow_cascaded_delete
<lino.core.model.Model.allow_cascaded_delete>` set to
`['restaurant']`, otherwise the above code would have raised a
ValidationError :message:`Cannot delete #2
(name=Second,owners=Bert,cooks=Bert) because 2 meals refer to it.` But
the meals have been deleted:

>>> Meal.objects.all()
[]

Of course, #2 remains as a Place
The owner and visits have been taken over:

>>> second = Place.objects.get(pk=2)
>>> second.visit_set.all()
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]


The :func:`create_mti_child` function
-------------------------------------

This function is for rather internal use.  :ref:`Python dumps <dpy>`
generated by :class:`lino.utils.dpy.Serializer` use this function for
creating MTI children instances without having to lookup their parent.

.. currentmodule:: lino.utils.dpy

In a Python dump we are in a special situation: All Place instances
are being generated first, and in another step we are going to create
all the Restaurant instances.  So how can we create a Restaurant whose
Place already exists *without first having to do a lookup of the Place
record*?  That's why :func:`create_mti_child` was written for.

>>> obj = Place(id=3, name="Third")
>>> obj.save()
>>> obj.owners.add(Person.objects.get(pk=2))
>>> obj.save()
>>> obj
Place #3 ('#3 (name=Third, owners=Bert)')

>>> from lino.utils.dpy import create_mti_child
>>> obj = create_mti_child(Place, 3, Restaurant)

The return value is technically a normal model instance,
but whose `save` and `full_clean` methods have been 
patched: `full_clean` is overridden to do nothing, 
and `save` will call a "raw" save to avoid the 
need of a proper Place instance for that Restaurant.
The only thing you can do with it is to save it:

>>> obj.save()

The `save` and `full_clean` methods are the only methods that 
will be called by 
:class:`lino.utils.dpy.Deserializer`.

To test whether :func:`create_mti_child` did her job, 
we must re-read an instance:

>>> Restaurant.objects.get(pk=3)
Restaurant #3 ('#3 (name=Third, owners=Bert, cooks=)')

Note that 
:func:`create_mti_child` doesn't allow to also change the `name`
because that field is defined in the Place model, 
not in Restaurant. 

>>> obj = Place(id=4, name="Fourth")
>>> obj.save()
>>> ow = create_mti_child(Place, 4, Restaurant, name="A new name")
Traceback (most recent call last):
...
Exception: create_mti_child() Restaurant 4 from Place : ignored non-local fields {'name': 'A new name'}

(Until 20120930 this it was silently ignored
for backwards compatibility (`/blog/2011/1210`).


The user interface
==================

Here is the :file:`tables.py` file:

.. literalinclude:: tables.py




Related documents
-----------------

- `Promote a Place to a Restaurant? 
  <http://groups.google.com/group/django-users/browse_thread/thread/3c9d7c97a8f01da0>`_
  (Erik Stein at django-users, 17 Oct 2008).
  
- `Multi-table Inheritance: How to add child to parent model?
  <http://www.mail-archive.com/django-users@googlegroups.com/msg110455.html>`_
  (ringemup at django-users, 04 Nov 2010).

- Django documentation on `multi-table inheritance
  <http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`_
  
- :djangoticket:`Child models overwrite data of Parent model
  <11618>`

- :djangoticket:`Multi-table inheritance does not 
  allow linking new instance of child model to existing parent model 
  instance <7623>`
  
- Carl Meyer's `django-model-utils project <https://github.com/carljm/django-model-utils>`_
  
- `Figure out child type with Django MTI or specify type as field? <http://stackoverflow.com/questions/3990470/figure-out-child-type-with-django-mti-or-specify-type-as-field>`_

