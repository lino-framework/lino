"""
Django pitfall : Defining IntegerField as explicit primary_key field
--------------------------------------------------------------------

If you define an IntegerField as explicit primary_key field, you'll get unexpected bahaviour:

  >>> p = IntegerPerson(name="Luc")
  >>> p.save() 
  >>> p.save() 
  >>> IntegerPerson.objects.all()
  [<IntegerPerson: Luc>, <IntegerPerson: Luc>]

Oops! The second `save()` has created a second instance!
That's not normal. 
There's nothing wrong with saving your object a second time, here are some examples:

  >>> p = AutoPerson(name="Luc")
  >>> p.save() 
  >>> p.save() 
  >>> AutoPerson.objects.all()
  [<AutoPerson: Luc>]
  
Implicit primary key:  

  >>> p = Person(name="Luc")
  >>> p.save() 
  >>> p.save() 
  >>> Person.objects.all()
  [<Person: Luc>]

CharField as primary key:

>>> p = CharPerson(name="Luc")
>>> p.save() 
>>> p.save() 
>>> CharPerson.objects.all()
[<CharPerson: Luc>]

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

    
class Person(models.Model):  
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class AutoPerson(models.Model):  
    id = models.AutoField(primary_key=True,verbose_name=_("ID"))
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class IntegerPerson(models.Model):  
    id = models.IntegerField(primary_key=True,verbose_name=_("ID"))
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class CharPerson(models.Model):  
    id = models.CharField(primary_key=True,verbose_name=_("ID"),max_length=10)
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

