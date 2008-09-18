## Copyright 2008 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import datetime
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200,blank=True)
    birthdate = models.DateField('birth date',blank=True)
    title = models.CharField(max_length=200,blank=True)
    home = models.ForeignKey("Contact",blank=True,related_name="home")
    
    def __unicode__(self):
        s=self.name
        if self.firstname:
          s=self.firstname+" "+s
        return s

    def age(self,date=None):
        if date is None:
            date=datetime.date.today()
        age=date-self.birthdate
        return age.days() / 365
    age.short_description = 'Approximative age'


class Organisation(models.Model):
    name = models.CharField(max_length=200)
    siege = models.ForeignKey("Contact",blank=True,related_name="siege")
    #~ poll = models.ForeignKey(Poll)
    #~ choice = models.CharField(max_length=200)
    #~ votes = models.IntegerField()
    
    def __unicode__(self):
        return self.name
        
        
class Contact(models.Model):
    name = models.CharField(max_length=200)
    organisation = models.ForeignKey(Organisation)
    person = models.ForeignKey(Person)
    country = models.ForeignKey("Country",blank=True)
    city = models.ForeignKey("City",blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    addr2 = models.CharField(max_length=200,blank=True)
    
    def __unicode__(self):
        s=self.name
        if self.organisation:
          s += "\n%u" % self.organisation
        if self.person:
          s += "\n%u" % self.person
        if self.addr1:
          s += "\n%u" % self.addr1
        if self.addr2:
          s += "\n%u" % self.addr2
        if self.zipcode and self.city:
          s += "\n%u %s" % (self.zipcode,self.city)
        if self.country:
          s += "\n%u" % self.country
        return s
    
    
class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey("Country")
    def __unicode__(self):
        return self.name
 
class Country(models.Model):
    name = models.CharField(max_length=200)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3,blank=True) 
    def __unicode__(self):
        return self.name
 