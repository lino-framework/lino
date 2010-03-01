"""

Create some data:
  
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
  
Now:

  >>> city = Contact._meta.get_field('city')
  >>> rpt = Contacts()
  >>> [unicode(o) for o in rpt.get_field_choices(city,{'country':be})]
  [u'Brussels', u'Eupen']
  >>> [unicode(o) for o in rpt.get_field_choices(city,{'country':fr})]
  [u'Lyon', u'Paris']
  >>> [unicode(o) for o in rpt.get_field_choices(city,{'country':None})]
  [u'Brussels', u'Eupen', u'Lyon', u'Paris']

"""

from django.db import models
from lino import reports
   
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
    def __unicode__(self):
        return self.name
        
    @classmethod
    def city_choices(cls,country):
        if country is not None:
            return country.city_set.order_by('name')
        return City.objects.order_by('name')

class Contacts(reports.Report):
    model = Contact
    
    