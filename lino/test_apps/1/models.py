"""
Metamorphose : converting between different MTI models
------------------------------------------------------

.. currentmodule:: lino.utils.mti

This document explains my work on a topic also touched by
Erik Stein's question 
`Promote a Place to a Restaurant? 
<http://groups.google.com/group/django-users/browse_thread/thread/3c9d7c97a8f01da0>`_
at django-users (Oct 17, 2008).

My work is not finished because I hope to hear comments 
of other people before I invest more time into this
(after all there is danger that I have been reinventing the wheel!).

Comments and suggestions are welcome. 
    
Introduction
------------

Malcolm's answer to Erik's questions was 
"There's no concept of "promotion". Just create a new Restaurant object 
with the requisite information.", and I basically agree with him.

However, when we have models 
like `Place` and `Restaurant` 
in an application,
then our users do encounter the problem 
of needing to "promote a Place to a Restaurant",
or "reduce a Restaurant to a simple Place".
And especially when there is a lot of other related data, 
there should be a possibility to do this in a user-friendly way.

I thought that "metamorphose" is a good name for this thing.

- Django's documentation on
  `multi-table inheritance
  <http://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`_,
  
- Source code:

  - This document: :srcref:`/lino/lino/test_apps/1/models.py`.
  - The :func:`convert` function itself: :srcref:`/lino/lino/utils/mti.py`.
  

Let's go
--------


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

Now the user discovers that this Place isn't actually a Restaurant, 
and would like to "remove it's Restaurant data" from the database.

The following might drop at mind, but doesn't work:

>>> p = Place.objects.get(id=1)
>>> p.restaurant = None
Traceback (most recent call last):
...
ValueError: Cannot assign None: "Place.restaurant" does not allow null values.

I wrote a function :func:`convert` that 
deletes the Restaurant instance after having 
taken a copy of its data in memory, 
excluding the fields that are specific to Restaurants,
then creates a new Place instance using that data.
The primary key and related objects remain unchanged.
The cooks will loose their job, but the owners remain.

>>> from lino.utils.mti import convert
>>> new_place = convert(r,Place)

`convert()` returns a newly created instance of the specified 
model:

>>> new_place
<Place: #1 (name=First,owners=Alfred,Bert)>

The place now no longer exists as a restaurant:

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
>>> obj = convert(obj,Restaurant)
>>> for i in 3,4:
...     obj.cooks.add(Person.objects.get(pk=i))
>>> obj
<Restaurant: #2 (name=Second,owners=Bert,cooks=Claude,Dirk)>


Pitfall
-------

There is a pitfall with :func:`convert`.

Calling :func:`lino.utils.mdi.convert` 
will invalidate the original model instance.
This means that the variable used by the caller 
will refer to something does not represent any existing record. 

Best practice is to call::

  obj = convert(obj,...)
  
To make sure that your variable "obj" is thrown away.
Here is an example of what happens if you don't.

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

If you continue to use this variable, you would get 
unpredictable behaviour.
To avoid further damage, :func:`convert` changes the 
`__class__` attribute. 

>>> obj
<lino.utils.mti.InvalidModelInstance object at ...>

>>> obj.owners.add(Person.objects.get(pk=1))
Traceback (most recent call last):
...
AttributeError: 'InvalidModelInstance' object has no attribute 'owners'


Virtual fields
--------------

This section shows how :func:`convert` is being used by Lino's virtual 
fields, and thus is Lino-specific

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

TODO: ForeignKey
----------------

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
The following should work, but doesn't 

>>> Visit.objects.all() # SKIP
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]
>>> second.visit_set.all() # SKIP
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]

That's still to fix.

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
          self.purpose, self.person, self.place.name
        )
    