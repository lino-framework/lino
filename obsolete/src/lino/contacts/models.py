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
    """
    A person
    
    # A person of whom I know only the firstname
    >>> p1=Person.objects.create(name="Eikki")
    
    # Another person 
    >>> p2=Person.objects.create(name="Saffre",firstname="Luc")
    
    >>> unicode(p2)
    u'Luc Saffre'
    
    """
    name = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200,blank=True)
    birthdate = models.DateField('birth date',blank=True,null=True)
    title = models.CharField(max_length=200,blank=True)
    home = models.ForeignKey("Contact",
                             blank=True,null=True,
                             related_name="home")
    
    def __unicode__(self):
        s=self.name
        if self.firstname:
          s=self.firstname+" "+s
        return s

    def age(self,date=None):
        if self.birthdate is None:
            return None
        if date is None:
            date=datetime.date.today()
        age=date-self.birthdate
        return age.days() / 365
    age.short_description = 'Approximative age'
    
    def contacts(self):
        def label(c):
            if c.organisation is not None:
                return unicode(c.organisation)
            if c.place is not None:
                return unicode(c.place)
            return unicode(c)
        return ", ".join([linkto(c,label(c)) 
          for c in self.contact_set.all()])
    contacts.allow_tags=True


class Organisation(models.Model):
    name = models.CharField(max_length=200)
    siege = models.ForeignKey("Contact",blank=True,null=True,
      related_name="siege")
    #~ poll = models.ForeignKey(Poll)
    #~ choice = models.CharField(max_length=200)
    #~ votes = models.IntegerField()
    
    def __unicode__(self):
        return self.name
        
        

    
class Country(models.Model):
    name = models.CharField(max_length=200)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3,blank=True,null=True) 
    def __unicode__(self):
        return self.name
        
        
def linkto(obj,text=None):
    if text is None:
        text=unicode(obj)
    s='<a href="/admin/contacts/%s/%d' % (obj.__class__.__name__,obj.id)
    s+='">'+text+"</a>"
    return s
        
class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country)
    def __unicode__(self):
        return self.name
    def contacts(self):
        l=[]
        for p in self.place_set.all():
            for c in p.contact_set.all():
                if c.person is not None:
                    l.append(c.person)
        return ", ".join([linkto(x) for x in l])
    contacts.allow_tags=True
 
class Place(models.Model):
    name = models.CharField(max_length=200)
    addr1 = models.CharField(max_length=200,blank=True,null=True)
    addr2 = models.CharField(max_length=200,blank=True,null=True)
    country = models.ForeignKey(Country,blank=True,null=True)
    city = models.ForeignKey(City,blank=True,null=True)
    zipcode = models.CharField(max_length=10,blank=True,null=True)
    
    def __unicode__(self):
        if self.name:
            s=self.name
        else:
            s=''
        if self.addr1:
          s += "\n%s" % self.addr1
        if self.addr2:
          s += "\n%s" % self.addr2
        if self.zipcode and self.city:
          s += "\n%s %s" % (self.zipcode,self.city)
        if self.country:
          s += "\n%s" % self.country
        return s

 
class Contact(models.Model):
    name = models.CharField(max_length=200)
    organisation = models.ForeignKey(Organisation,blank=True,null=True)
    person = models.ForeignKey(Person,blank=True,null=True)
    place = models.ForeignKey(Place,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    def __unicode__(self):
        s=self.name
        if self.organisation:
          s += "\n%s" % self.organisation
        if self.person:
          s += "\n%s" % self.person
        if self.place:
          s += "\n%s" % self.place
        if self.email:
          s += "\n%s" % self.email
        return s
