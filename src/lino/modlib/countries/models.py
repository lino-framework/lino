## Copyright 2008-2010 Luc Saffre
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


import datetime
from django.db import models
from lino import reports
from django.utils.translation import ugettext as _


class Country(models.Model):
    name = models.CharField(max_length=200)
    isocode = models.CharField(max_length=4,primary_key=True)
    short_code = models.CharField(max_length=4)
    
    class Meta:
        verbose_name_plural = _("Countries")
    
    def __unicode__(self):
        return self.name
        
class Countries(reports.Report):
    model = 'countries.Country'
    order_by = "isocode"
    column_names = "isocode name short_code"
    
FREQUENT_COUNTRIES = ['BE','NL','DE', 'FR', 'LU']


class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey('countries.Country')
    zip_code = models.CharField(max_length=8,blank=True)
    
    class Meta:
        verbose_name_plural = _("Cities")
        unique_together = ('country','zip_code') # not supported in sqlite?
    
    def __unicode__(self):
        return self.name
        
class Cities(reports.Report):
    model = 'countries.City'
    order_by = "country name"
    column_names = "country name zip_code"
    



class Language(models.Model):
    id = models.CharField(max_length=2,primary_key=True)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Languages(reports.Report):
    model = 'countries.Language'
    order_by = "id"

