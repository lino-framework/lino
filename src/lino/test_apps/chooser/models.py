"""

Module lino.utils.choosers
--------------------------

You instantiate a Chooser by specifying a model and a fieldname. 
The fieldname must be the name of a field that has been defined in your model.
A Chooser for a field FOO on a model will look whether the model defines a class method FOO_choices().

Preparation
===========

Create some countries and some cities:
  
  >>> be = Country(name='Belgium')
  >>> be.save()
  >>> fr = Country(name='France')
  >>> fr.save()
  >>> brussels = City(country=be,name='Brussels')
  >>> brussels.save()
  >>> eupen = City(country=be,name='Eupen')
  >>> eupen.save()
  >>> paris = City(country=fr,name='Paris')
  >>> paris.save()
  >>> lyon = City(country=fr,name='Lyon')
  >>> lyon.save()
  
(Intermezzo to test `obj2str()`:)

  >>> print obj2str(be)
  Country(id=1,name='Belgium')
  >>> print obj2str(paris)
  City(id=3,name='Paris',country=<Country: France>)
  
The `choosers` needs initialization:

  >>> choosers.discover()  
  
Situation 1 
===========

A Contact has ForeignKey fields to Country and City. 
In an entry form for a Contact you want only the cities of that country when selecting a city.

How to use a Chooser on a ForeignKey:

  >>> city = choosers.get_for_field(get_field(Contact,'city'))
  >>> [unicode(o) for o in city.get_choices(country=be)]
  [u'Brussels', u'Eupen']
  
  >>> [unicode(o) for o in city.get_choices(country=fr)]
  [u'Lyon', u'Paris']
  >>> [unicode(o) for o in city.get_choices()]
  [u'Brussels', u'Eupen', u'Lyon', u'Paris']
  
There is no method `country_choices`, so `Contact.country` has no Chooser:
  
  >>> print choosers.get_for_field(get_field(Contact,'country'))
  None

  
Situation 2
===========

How to use a Chooser on a field with choices:

  >>> food = choosers.get_for_field(get_field(Contact,'food'))
  
  >>> [unicode(o) for o in food.get_choices()]
  [u'Potato', u'Vegetable', u'Meat', u'Fish']
  
  >>> [unicode(o) for o in food.get_choices(year_in_school='FR')]
  [u'Potato']

  >>> [unicode(o) for o in food.get_choices(year_in_school='SR')]
  [u'Potato', u'Vegetable', u'Meat', u'Fish']


Special cases
=============

Note that `Chooser.get_choices()` ignores any unused keyword arguments:
  
  >>> [unicode(o) for o in city.get_choices(country=be,foo=1,bar=True,baz='7')]
  [u'Brussels', u'Eupen']

  
  

"""

from django.db import models
from lino import reports
from lino.utils import choosers
from lino.modlib.tools import obj2str, get_field

YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
)

MENU = [
  # name reserved_for
  ('Potato', None),
  ('Vegetable', 'SO JR SR GR'),
  ('Meat', 'JR SR GR'),
  ('Fish', 'SR GR'),
]

   
class Country(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country)
    def __unicode__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City)
    year_in_school = models.CharField(max_length=2,choices=YEAR_IN_SCHOOL_CHOICES)
    food = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name
        
    @classmethod
    def city_choices(cls,country):
        if country is not None:
            return country.city_set.order_by('name')
        return cls.city.field.rel.to.objects.order_by('name')
        
    @classmethod
    def food_choices(cls,year_in_school):
        food = []
        for name, reserved_for in MENU:
            if (year_in_school is None) or (reserved_for is None) or year_in_school in reserved_for:
                food.append(name)
        return food

class Contacts(reports.Report):
    model = Contact
    
    