Luc's Django pitfall collection
===============================


Defining IntegerField as explicit primary_key field
---------------------------------------------------

Don't define an IntegerField as explicit primary_key field, otherwise you'll get unexpected behaviour (testcase `20100519 <http://code.google.com/p/lino/source/browse/src/lino/test_apps/20100519/models.py>`_).

Consider the following Model definitions::

  class Person(models.Model):  
      name = models.CharField(max_length=200)
      def __unicode__(self):
          return self.name

  class AutoPerson(models.Model):  
      id = models.AutoField(primary_key=True)
      # otherwise same as Person

  class IntegerPerson(models.Model):  
      id = models.IntegerField(primary_key=True)
      # otherwise same as Person

  class CharPerson(models.Model):  
      id = models.CharField(primary_key=True,max_length=10)
      # otherwise same as Person

Here is the problem:

  >>> p = IntegerPerson(name="Luc")
  >>> p.save()
  >>> p.save()
  >>> IntegerPerson.objects.all()
  [<IntegerPerson: Luc>, <IntegerPerson: Luc>]

Oops! The second `save()` has created a second instance! That's not normal!

That's not normal because there's nothing wrong with saving your object a second time, it works for all the other cases I tried: 

  >>> p = AutoPerson(name="Luc")
  >>> p.save()
  >>> p.save()
  >>> AutoPerson.objects.all()
  [<AutoPerson: Luc>]

  >>> p = Person(name="Luc")
  >>> p.save()
  >>> p.save()
  >>> Person.objects.all()
  [<Person: Luc>]

  >>> p = CharPerson(name="Luc")
  >>> p.save()
  >>> p.save()
  >>> CharPerson.objects.all()
  [<CharPerson: Luc>]



Keeping empty fixtures
----------------------

Never define an empty fixture (i.e. one that returns no objects).
Django then thinks "If the fixture we loaded contains 0 objects, assume that an error 
was encountered during fixture loading." and afterwards may behave strangely.

Creating an empty fixture when using :mod:`lino.utils.dpyserializer` is easy. 
Just create a file :xfile:`initial_data.dpy` in the :xfile:`fixtures` 
subdir of one of your :setting:`INSTALLED_APPS` with this contents::

    def objects():
        return [] 

Then you run::

  manage.py loaddata demo
  
and `loaddata` says a warning:: 

  No fixture data found for 'initial_data'. (File format may be invalid.)

The strange behaviour is that 
Django does a rollback of the `initial_data` fixtures of all your installed apps,
but then continues to loaddata the `demo` fixtures.

