"""

This solves the same real-world problem as 
:mod:`lino.test_apps.mti`, 
but using OneToOneFields instead of MTI.
Result is that everything gets much easier.
Which is another example to 
confirm that Multi-table inheritance 
"is a bad thing"
(`Two scoops of Django <https://django.2scoops.org/>`_)


.. The following lines are here for running doctest on this document. 
  Sphinx removes them because they are a comment, but doctest executes them.
  
  >>> from django.conf import settings
  >>> settings.SITE.startup()
  >>> nomti = settings.SITE.modules.nomti
  >>> Person = nomti.Person
  >>> Restaurant = nomti.Restaurant
  >>> Bar = nomti.Bar
  >>> Place = nomti.Place


The database models
-------------------

Here is the :file:`models.py` file used for this example.

We have a table of Places, some of them are Restaurants, 
some are Pubs, and some are neither Pub nor Restaurant.


.. literalinclude:: ../../lino/test_apps/nomti/models.py


Populating the database
-----------------------

Here are the **Persons** who act in our story:

>>> anne = Person(name="Anne") ; anne.save()
>>> bert = Person(name="Bert"); bert.save()
>>> claude = Person(name="Claude"); claude.save()
>>> dirk = Person(name="Dirk"); dirk.save()


"Chez Lola" is a **simple Place** owned and managed by Anne, 
it's neither a Restaurant nor a Bar:

>>> place = Place(id=1,name="Chez Lola",ceo=anne)
>>> place.save()
>>> place.owners.add(anne)

You cannot create a **Restaurant** or a **Bar** without first 
creating the Place:

>>> Restaurant().save()
Traceback (most recent call last):
...
IntegrityError: nomti_restaurant.place_id may not be NULL

"Mamma mia" is a Restaurant with a CEO, two owners and two cooks:

>>> place = Place(id=2,name="Mamma mia",ceo=bert)
>>> place.save()
>>> place.owners.add(anne)
>>> place.owners.add(bert)
>>> r = Restaurant(id=1,place=place)
>>> r.save()
>>> r.cooks.add(claude)
>>> r.cooks.add(dirk)

Bert owns a a little Bar named "Foo" which doesn't serve alcohol:

>>> place = Place(id=3,name="Foo",ceo=bert)
>>> place.save()
>>> Bar(id=1,place=place,serves_alcohol=False).save()

Claude and Dirk also work in a place that is both Restaurant and Bar:

>>> place = Place(id=4,name="Chez Claude",ceo=claude)
>>> place.save()
>>> place.owners.add(claude)
>>> r = Restaurant(place=place)
>>> r.save()
>>> r.cooks.add(claude)
>>> r.cooks.add(dirk)
>>> Bar(place=place).save()

Here is our data:

>>> Person.objects.all()
[Person #1 (u'Anne'), Person #2 (u'Bert'), Person #3 (u'Claude'), Person #4 (u'Dirk')]

>>> for obj in Place.objects.all(): print obj.pk, obj
1 Chez Lola (ceo=Anne,owners=Anne)
2 Mamma mia Restaurant (ceo=Bert,owners=Anne,Bert)
3 Foo Bar (ceo=Bert,owners=)
4 Chez Claude Restaurant & Bar (ceo=Claude,owners=Claude)

>>> for obj in Restaurant.objects.all(): print obj.pk, obj
1 Mamma mia (cooks=Claude,Dirk)
2 Chez Claude (cooks=Claude,Dirk)

>>> for obj in Bar.objects.all(): print obj.pk, obj
1 Foo (no alcohol)
2 Chez Claude

Now a user of our application 
discovers that Mamma mia isn't actually a `Restaurant` but a `Bar`.
They would like to "remove it's Restaurant data" (`serves_hot_dogs` and `cooks`)
from the database, but keep the `Place` data (`name`, `ceo` and `owners`).
Especially the primary key and related objects should remain unchanged.

>>> obj = Restaurant.objects.get(pk=1)
>>> place = obj.place
>>> obj.delete()
>>> Bar(place=place).save()

Result:

>>> for obj in Restaurant.objects.all(): print obj.pk, obj
2 Chez Claude (cooks=Claude,Dirk)

>>> for obj in Bar.objects.all(): print obj.pk, obj
1 Foo (no alcohol)
2 Chez Claude
3 Mamma mia

>>> for obj in Place.objects.all(): print obj.pk,obj
1 Chez Lola (ceo=Anne,owners=Anne)
2 Mamma mia Bar (ceo=Bert,owners=Anne,Bert)
3 Foo Bar (ceo=Bert,owners=)
4 Chez Claude Restaurant & Bar (ceo=Claude,owners=Claude)


"""
