## Copyright 2008-2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Defines models 
:class:`Language`,
:class:`Country` and
:class:`City`.

"""


import datetime
from django.db import models
from django.conf import settings

from lino import reports
#~ from lino import layouts
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from lino.utils.choosers import chooser
#~ from lino.utils.babel import add_babel_field, babelattr
from lino.utils import babel 
from lino.utils import dblogger


#~ class Language(models.Model):
class Language(babel.BabelNamed):
    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
    id = models.CharField(max_length=3,primary_key=True)
    #~ name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    #~ name = models.CharField(max_length=200,verbose_name=_("Designation"))
    iso2 = models.CharField(max_length=2,blank=True) # ,null=True)
    
    #~ def __unicode__(self):
        #~ return babel.babelattr(self,'name')

#~ add_babel_field(Language,'name')

class Languages(reports.Report):
    model = Language




class Country(babel.BabelNamed):
    """
    Implements the :class:`countries.Country` convention.
    """
    
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        
    isocode = models.CharField(max_length=4,primary_key=True)
    #~ name = models.CharField(max_length=200)
    #~ name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    short_code = models.CharField(max_length=4,blank=True)
    iso3 = models.CharField(max_length=3,blank=True)
    
    #~ def __unicode__(self):
        #~ return babel.babelattr(self,'name')

#~ add_babel_field(Country,'name')
        
class Countries(reports.Report):
    """
    Shows the global list of countries.
    """
    #~ label = _("Countries")
    model = 'countries.Country'
    order_by = ["name","isocode"]
    column_names = "name isocode *"
    
    
FREQUENT_COUNTRIES = ['BE','NL','DE', 'FR', 'LU']


class City(models.Model):
    """
    Implements the :class:`countries.City` convention.
    """
    name = models.CharField(max_length=200)
    country = models.ForeignKey('countries.Country')
    zip_code = models.CharField(max_length=8,blank=True)
    
    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        if not settings.LINO.allow_duplicate_cities:
            unique_together = ('country','name','zip_code')
    
    def __unicode__(self):
        return self.name
        
class Cities(reports.Report):
    #~ label = _("Cities")
    model = 'countries.City'
    order_by = "country name".split()
    column_names = "country name zip_code *"
    
class CitiesByCountry(Cities):
    column_names = "name zip_code country *"
    fk_name = 'country'



class CountryCity(models.Model):
    """
    Adds two fields `country` and `city` and defines 
    a context-sensitive chooser for city as well as a 
    `create_city_choice` method.
    """
    class Meta:
        abstract = True
        
    country = models.ForeignKey("countries.Country",blank=True,null=True,
        verbose_name=_("Country"))
    city = models.ForeignKey('countries.City',blank=True,null=True,
        verbose_name=_('City'))
        
    @chooser()
    def city_choices(cls,country):
        if country is not None:
            return country.city_set.order_by('name')
        return cls.city.field.rel.to.objects.order_by('name')
        
    def create_city_choice(self,text):
        """Called when an unknown city name was given. 
        Try to auto-create it.
        """
        if self.country is not None:
            #~ return self.country.city_set.create(name=text)
            #~ except IntegrityError:
            qs = self.country.city_set.filter(name__iexact=text)
            if qs.count() == 0:
                return self.country.city_set.create(name=text,country=self.country)
            raise ValidationError("Refused to auto-create city %r in %s because same name exists.",(text,self.country))
        #~ dblogger.warning("Cannot auto-create city %r if country is empty",text)
        raise ValidationError("Cannot auto-create city %r if country is empty",text)
  
    def full_clean(self,*args,**kw):
        if self.city is not None and self.country != self.city.country:
            self.country = self.city.country
        super(CountryCity,self).full_clean(*args,**kw)
