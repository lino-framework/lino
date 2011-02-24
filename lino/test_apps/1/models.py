"""
Multi-table inheritance: converting between child and parent
============================================================

.. currentmodule:: lino.utils.mti


Request for comments
--------------------
    
This document explains my work on a topic also touched by
Erik Stein's question 
`Promote a Place to a Restaurant? 
<http://groups.google.com/group/django-users/browse_thread/thread/3c9d7c97a8f01da0>`_
(17 Oct 2008)
and ringemup's question
`Multi-table Inheritance: How to add child to parent model?
<http://www.mail-archive.com/django-users@googlegroups.com/msg110455.html>`_
(04 Nov 2010)
at django-users.

I decided to make a break here 
because I now hope for comments 
before investing more time into this.
If you know (or imagine) 
a better way to solve my 
problem (:doc:`/tickets/22`), please let me know!

Introduction
------------

Malcolm's answer to Erik's questions was 
"There's no concept of "promotion". Just create a new Restaurant object 
with the requisite information.".

I basically agree with Malcolm.

On the other hand my users *will* come and ask
how to "promote a Place to a Restaurant",
or "reduce a Restaurant to a simple Place".
Especially when there is a lot of other related data, 
there should be a possibility to do this in a user-friendly way.
See :doc:`/tickets/22` for some examples if you are not convinced.

Let's go
--------

To see the data models used in the following examples,
please look at the source code of this document at
:srcref:`/lino/test_apps/1/models.py`.

Create some data:

>>> Person(name="Alfred").save()
>>> Person(name="Bert").save()
>>> Person(name="Claude").save()
>>> Person(name="Dirk").save()
>>> r = Restaurant(id=1,name="First")
>>> r.save()
>>> for i in 1,2:
...     r.owners.add(Person.objects.get(pk=i))
>>> for i in 3,4:
...     r.cooks.add(Person.objects.get(pk=i))

Here is our data:

>>> Person.objects.all()
[<Person: Alfred>, <Person: Bert>, <Person: Claude>, <Person: Dirk>]
>>> Restaurant.objects.all()
[<Restaurant: #1 (name=First,owners=Alfred,Bert,cooks=Claude,Dirk)>]
>>> Place.objects.all()
[<Place: #1 (name=First,owners=Alfred,Bert)>]

Now the user discovers that Place #1 isn't actually a Restaurant, 
and would like to "remove it's Restaurant data" from the database.
But the primary key and related objects should remain unchanged.

The following might drop at mind, but doesn't work:

>>> p = Place.objects.get(id=1)
>>> p.restaurant = None
Traceback (most recent call last):
...
ValueError: Cannot assign None: "Place.restaurant" does not allow null values.

I wrote a function :func:`convert` 
(the source code 
is :srcref:`here </lino/utils/mti.py>`)
that 
deletes the Restaurant instance after having 
taken a copy of its data in memory, 
including related objects, 
excluding things that are specific to Restaurants,
then creates a new Place instance using that data.
The primary key and related objects remain unchanged.
The cooks will loose their job, but the owners remain.

>>> from lino.utils.mti import convert
>>> new_place = convert(r,Place)

:func:`convert` returns a newly created instance of the specified 
model:

>>> new_place
<Place: #1 (name=First,owners=Alfred,Bert)>

The Place now no longer exists as a Restaurant:

>>> Restaurant.objects.get(pk=1)
Traceback (most recent call last):
...
DoesNotExist: Restaurant matching query does not exist.

The opposite operation, "promoting a simple Place to a Restaurant", 
is similar:

>>> obj = Place(id=2,name="Second")
>>> obj.save()
>>> obj.owners.add(Person.objects.get(pk=2))
>>> obj.save()
>>> obj
<Place: #2 (name=Second,owners=Bert)>

We just created a nice Place #2 with a single owner.
Later this Place becomes a Restaurant and hires 2 cooks:

>>> obj = convert(obj,Restaurant)
>>> for i in 3,4:
...     obj.cooks.add(Person.objects.get(pk=i))
>>> obj
<Restaurant: #2 (name=Second,owners=Bert,cooks=Claude,Dirk)>


Pitfall
-------

There is a pitfall with :func:`convert`:
it will invalidate the in-memory description of 
the original model instance.
The variable specified by the caller as first argument
will refer to something that
does not represent any existing record. 

Best practice is to call

::

  obj = convert(obj,...)
  
to make sure that your variable "obj" is thrown away.
Here is an example of what happens if you don't:

>>> obj = Place(id=3,name="Third")
>>> obj.save()
>>> obj
<Place: #3 (name=Third,owners=)>
>>> convert(obj,Restaurant)
<Restaurant: #3 (name=Third,owners=,cooks=)>

Until now everything is fine. Just notice that we wrote
``convert(obj,...)``
and not ``obj = convert(obj,...)``.
The problem with this is that our variable `obj` 
now refers to a model instance of a deleted object.

If we'd let you continue to use this variable, 
you would get unpredictable behaviour.
To avoid further damage, :func:`convert` changes the 
`__class__` attribute of your variable in order to make 
it unusable:

>>> obj.owners.add(Person.objects.get(pk=1))
Traceback (most recent call last):
...
AttributeError: 'InvalidModelInstance' object has no attribute 'owners'
>>> obj
<lino.utils.mti.InvalidModelInstance object at ...>


Virtual fields
--------------

This section shows how :func:`convert` is being used by Lino's virtual 
fields, and thus is Lino-specific and even less definitive 
than the rest of this document.

After the above examples our database looks like this:

>>> Place.objects.all()
[<Place: #1 (name=First,owners=Alfred,Bert)>, <Place: #2 (name=Second,owners=Bert)>, <Place: #3 (name=Third,owners=)>]
>>> Restaurant.objects.all()
[<Restaurant: #2 (name=Second,owners=Bert,cooks=Claude,Dirk)>, <Restaurant: #3 (name=Third,owners=,cooks=)>]


Let's take Place #1 and look at it.

>>> obj = Place.objects.get(pk=1)
>>> obj
<Place: #1 (name=First,owners=Alfred,Bert)>

:class:`lino.fields.VirtualField` instances are 
no Django fields, Django ignores them and so doesn't 
install the simple attribute instance get/set 
access for them.
That's why the following ``obj.is_restaurant`` does not 
give ``False`` as you might expect.

>>> obj.is_restaurant
<lino.utils.mti.EnableChild instance at ...>

This is not implemented because there currently 
the need for it would be to make the following 
examples more elegant.

Before using virtual fields, we must 
trigger Lino site setup. 
This is needed to discover virtual fields:

>>> from lino.core import site 

To access the values "stored" in virtual fields,
we must behave like a lino.ui would do, 
by calling the methods
:meth:`lino.fields.VirtualField.value_from_object`
and
:meth:`lino.fields.VirtualField.set_value_in_object`:


>>> for instance in Place.objects.all():
...    value = instance.is_restaurant.value_from_object(None,instance)
...    print value, instance
False #1 (name=First,owners=Alfred,Bert)
True #2 (name=Second,owners=Bert)
True #3 (name=Third,owners=)

Let's promote First (currently a simple Place) into a Restaurant:

>>> Place.is_restaurant.set_value_in_object(obj,True)
<Restaurant: #1 (name=First,owners=Alfred,Bert,cooks=)>

Note that `set_value_in_object` returns the modified instance.
This is because it might be a new object, as explained in 
the previous section.

>>> Restaurant.objects.get(pk=1)
<Restaurant: #1 (name=First,owners=Alfred,Bert,cooks=)>

And Second stops being a Restaurant:

>>> obj = Place.objects.get(pk=2)
>>> Place.is_restaurant.value_from_object(None,obj)
True

>>> Place.is_restaurant.set_value_in_object(obj,False) 
<Place: #2 (name=Second,owners=Bert)>

This operation has removed the related Restaurant instance:

>>> Restaurant.objects.get(pk=2) 
Traceback (most recent call last):
...
DoesNotExist: Restaurant matching query does not exist.

TODO: related ForeignKeys 
-------------------------

There is some more work to do because 
the current implementation of :func:`convert` forgets to 
convert objects that point to our Place or Restaurant using 
a ForeignKey.

To demonstrate this, we added the Visit model.

Bert, the owner of Place #2 (which is a Restaurant) does two visits:

>>> bert = Person.objects.get(pk=2)
>>> second = Place.objects.get(pk=2)
>>> Visit(purpose="Say hello",person=bert,place=second).save()
>>> Visit(purpose="Hang around",person=bert,place=second).save()
>>> second.visit_set.all()
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]

Now we convert Second to a Place. 
Both the owner and the visits should remain.

>>> second = convert(second,Place)
>>> second
<Place: #2 (name=Second,owners=Bert)>

The owner has been taken over (because it is a ManyToManyField).

But oops! The visits have been deleted! 
The following currently doesn't work:

>>> Visit.objects.all()
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]

That's still to fix.


Related documents
-----------------

- Django's documentation on
  `multi-table inheritance
  <http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`_,
  
  
- :djangoticket:`Child models overwrite data of Parent model
  <11618>`

- :djangoticket:`Multi-table inheritance does not 
  allow linking new instance of child model to existing parent model 
  instance <7623>`
  
- Carl Meyer's `django-model-utils project <https://github.com/carljm/django-model-utils>`_
  
- `Figure out child type with Django MTI or specify type as field? <http://stackoverflow.com/questions/3990470/figure-out-child-type-with-django-mti-or-specify-type-as-field>`_
  


"""

from django.db import models
from lino.utils.mti import EnableChild

class Person(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Place(models.Model):  
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(Person)
    is_restaurant = EnableChild('Restaurant',verbose_name="is a restaurant")
    def __unicode__(self):
        return "#%s (name=%s,owners=%s)" % (
            self.pk,self.name, 
            ','.join([unicode(o) for o in self.owners.all()]))
        
class Restaurant(Place):  
    serves_hot_dogs = models.BooleanField()
    cooks = models.ManyToManyField(Person)
    def __unicode__(self):
        return "#%d (name=%s,owners=%s,cooks=%s)" % (
            self.pk,self.name, 
            ','.join([unicode(o) for o in self.owners.all()]),
            ','.join([unicode(o) for o in self.cooks.all()]))

class Visit(models.Model):
    person = models.ForeignKey(Person)
    place = models.ForeignKey(Place)
    purpose = models.CharField(max_length=50)
    def __unicode__(self):
        return "%s visit by %s at %s" % (
          self.purpose, self.person, self.place.name)
