"""
Multi-table inheritance: converting between child and parent
============================================================

.. currentmodule:: lino.utils.mti

This document presents the :mod:`lino.utils.mti` module, 
a collection of tools for doing multi-table child/parent 
conversions.

It is certainly not perfect, but works for me. 
I wrote it mainly to solve my ticket :doc:`/tickets/22`.
If you find any bugs, please let me know.

This article is part of Lino's tests suite,
it's source code is at 
:srcref:`/lino/test_apps/1/models.py`.


Let's go
--------


For this example we use the following models::

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

That's a case where :func:`delete_child` is needed:

>>> from lino.utils.mti import delete_child
>>> p = Place.objects.get(id=1)
>>> delete_child(p,Restaurant)

The Place now no longer exists as a Restaurant:

>>> Restaurant.objects.get(pk=1)
Traceback (most recent call last):
...
DoesNotExist: Restaurant matching query does not exist.

The opposite operation, "promoting a simple Place to a Restaurant", 
is done using :func:`insert_child`:

>>> obj = Place(id=2,name="Second")
>>> obj.save()
>>> obj.owners.add(Person.objects.get(pk=2))
>>> obj.save()
>>> obj
<Place: #2 (name=Second,owners=Bert)>

We just created a new Place #2 with a single owner.
Later this Place becomes a Restaurant and hires 2 cooks:

>>> from lino.utils.mti import insert_child
>>> obj = insert_child(obj,Restaurant)
>>> for i in 3,4:
...     obj.cooks.add(Person.objects.get(pk=i))
>>> obj
<Restaurant: #2 (name=Second,owners=Bert,cooks=Claude,Dirk)>

If you try to promote a Person to a Restaurant, you'll get an exception:

>>> person = Person.objects.get(pk=2)
>>> insert_child(person,Restaurant)
Traceback (most recent call last):
...
ValidationError: [u'A Person cannot be parent for a Restaurant']


Virtual fields
--------------

This section shows how the :class:`EnableChild` virtual field is being 
used by Lino, and thus is Lino-specific.

After the above examples our database looks like this:

>>> Place.objects.all()
[<Place: #1 (name=First,owners=Alfred,Bert)>, <Place: #2 (name=Second,owners=Bert)>]
>>> Restaurant.objects.all()
[<Restaurant: #2 (name=Second,owners=Bert,cooks=Claude,Dirk)>]

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

This is not implemented because the only 
need for it would be to make the following 
examples more elegant...

Before using virtual fields, we must setup 
the Lino application. 
In a Django project this is usually done 
when the web server gets a first request and 
imports it's  :setting:`ROOT_URLCONF`.
This is needed to discover virtual fields:

>>> from django.conf import settings
>>> settings.LINO.setup()

To access the values that are "stored" in virtual fields,
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

Let's promote First (currently a simple Place) to a Restaurant:

>>> Place.is_restaurant.set_value_in_object(None,obj,True)
>>> Restaurant.objects.get(pk=1)
<Restaurant: #1 (name=First,owners=Alfred,Bert,cooks=)>

And Second stops being a Restaurant:

>>> second = Place.objects.get(pk=2)
>>> Place.is_restaurant.value_from_object(None,second)
True

>>> Place.is_restaurant.set_value_in_object(None,second,False) 

This operation has removed the related Restaurant instance:

>>> Restaurant.objects.get(pk=2) 
Traceback (most recent call last):
...
DoesNotExist: Restaurant matching query does not exist.


And finally, rather to explain why Restaurants sometimes 
close and later reopen:

>>> bert = Person.objects.get(pk=2)
>>> second = Place.objects.get(pk=2)
>>> Place.is_restaurant.set_value_in_object(None,second,True) 

Now we can see this place again as a Restaurant

>>> second = Restaurant.objects.get(pk=2)
>>> second.cooks.add(bert)
>>> second
<Restaurant: #2 (name=Second,owners=Bert,cooks=Bert)>



Related ForeignKeys 
-------------------

In order to demonstrate what happens when there are ForeignKeys, 
we add two more models::

  class Visit(models.Model):
      person = models.ForeignKey(Person)
      place = models.ForeignKey(Place)
      purpose = models.CharField(max_length=50)
      def __unicode__(self):
          return "%s visit by %s at %s" % (
            self.purpose, self.person, self.place.name)

  class Meal(models.Model):
      person = models.ForeignKey(Person)
      restaurant = models.ForeignKey(Restaurant)
      what = models.CharField(max_length=50)
      def __unicode__(self):
          return "%s eats %s at %s" % (
            self.person, self.what, self.restaurant.name)




Bert, the owner of Restaurant #2 does two visits:

>>> second = Restaurant.objects.get(pk=2)
>>> Visit(purpose="Say hello",person=bert,place=second).save()
>>> Visit(purpose="Hang around",person=bert,place=second).save()
>>> second.visit_set.all()
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]

Claude and Dirk, now workless, still go to eat in restaurants:

>>> Meal(what="Fish",person=Person.objects.get(pk=3),restaurant=second).save()
>>> Meal(what="Meat",person=Person.objects.get(pk=4),restaurant=second).save()
>>> second.meal_set.all()
[<Meal: Claude eats Fish at Second>, <Meal: Dirk eats Meat at Second>]

Now we reduce Second to a Place. 

>>> second = Place.objects.get(pk=2)
>>> delete_child(second,Restaurant)
>>> second
<Place: #2 (name=Second,owners=Bert)>

The owner and visits have been taken over, but the meals have been deleted:

>>> second = Place.objects.get(pk=2)
>>> second.visit_set.all()
[<Visit: Say hello visit by Bert at Second>, <Visit: Hang around visit by Bert at Second>]
>>> Meal.objects.all()
[]



Related documents
-----------------

- `Promote a Place to a Restaurant? 
  <http://groups.google.com/group/django-users/browse_thread/thread/3c9d7c97a8f01da0>`_
  (Erik Stein at django-users, 17 Oct 2008).
  
- `Multi-table Inheritance: How to add child to parent model?
  <http://www.mail-archive.com/django-users@googlegroups.com/msg110455.html>`_
  (ringemup at django-users, 04 Nov 2010).

- Django documentation on
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

class Meal(models.Model):
    person = models.ForeignKey(Person)
    restaurant = models.ForeignKey(Restaurant)
    what = models.CharField(max_length=50)
    def __unicode__(self):
        return "%s eats %s at %s" % (
          self.person, self.what, self.restaurant.name)

