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
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django import forms

import lino
from lino import reports
from lino import layouts
from lino.utils import perms
#~ from lino.utils import mixins

from lino.modlib import fields
from lino.modlib.contacts.utils import join_words

def default_language():
    from django.conf import settings
    return settings.LANGUAGE_CODE[:2]
    
    
#~ def name_default(obj):
    #~ l = filter(lambda x:x,[obj.last_name,obj.first_name,obj.title])
    #~ return " ".join(l)
        
#~ Contact.name.default = name_default

    

#~ class ContactMixin:
#~ class Contact(models.Model,mixins.Printable):
class Contact(models.Model):
  
    class Meta:
        abstract = True
  
    name = models.CharField(max_length=200)
    street = models.CharField(_("Street"),max_length=200,blank=True)
    street_no = models.CharField(_("No."),max_length=10,blank=True)
    street_box = models.CharField(_("Box"),max_length=10,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    #addr2 = models.CharField(max_length=200,blank=True)
    country = models.ForeignKey('countries.Country',blank=True,null=True,verbose_name=_("Country"))
    city = models.ForeignKey('countries.City',blank=True,null=True)
    #city = models.CharField(max_length=200,blank=True)
    zip_code = models.CharField(max_length=10,blank=True)
    region = models.CharField(max_length=200,blank=True)
    #~ language = models.ForeignKey('countries.Language',default=default_language)
    language = fields.LanguageField(default=default_language)
    
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=200,blank=True)
    gsm = models.CharField(max_length=200,blank=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    remarks = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return self.name
        
    def address(self):
        return self.as_address(', ')
        
    def as_address(self,linesep="\n<br/>"):
        lines = [self.name]
        if self.street:
            lines.append(join_words(self.street,self.street_no,self.street_box))
        if self.addr1:
            lines.append(self.addr1)
        #lines = [self.name,street,self.addr1,self.addr2]
        if self.region: # format used in Estonia
            if self.city:
                lines.append(unicode(self.city))
            s = join_words(self.zip_code,self.region)
        else: 
            s = join_words(self.zip_code,self.city)
        if s:
            lines.append(s)
        foreigner = True # False
        #~ if self.id == 1:
            #~ foreigner = False
        #~ else:
            #~ foreigner = (self.country != self.objects.get(pk=1).country)
        if foreigner and self.country: # (if self.country != sender's country)
            lines.append(unicode(self.country))
        #~ lino.log.debug('%s : as_address() -> %r',self,lines)
        return mark_safe(linesep.join(lines))
        
    @classmethod
    def city_choices(cls,country):
        #print "city_choices", repr(recipient)
        #recipient = self.objects.get(pk=pk)
        if country is not None:
        #if recipient and recipient.country:
            return country.city_set.order_by('name')
        return cls.city.field.rel.to.objects.order_by('name')
        #return countries.City.oiesByCountry().get_queryset(master_instance=recipient.country)
        #return dict(country__in=(recipient.country,))
        
    def on_create(self,request):
        print "lino.modlib.contacts.Contacts.on_create()"
        #~ instance.language = 
        
class Contacts(reports.Report):
    pass
  
class ContactDetail(layouts.DetailLayout):
    box1 = "name"
    box2 = """id language"""
    box3 = """country region
              city zip_code:10
              street:25 street_no street_box
              addr1:40
              """
    box4 = """email:40 
              url
              phone
              gsm
              """
    intro_box = "box1 box2"
    address_box = "box3 box4"
    bottom_box = "remarks"
    main = """intro_box
              address_box
              bottom_box
              """
              
    #collapsible_elements = dict(bottom_box=_("Bottom"),address_box=_("Address"))
       
 

#~ class PersonMixin(ContactMixin):
class Person(Contact):
    class Meta:
        abstract = True
        app_label = 'contacts'

    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)
        
    
    def save(self,*args,**kw):
        self.before_save()
        r = super(Person,self).save(*args,**kw)
        return r
        
    def before_save(self):
        #~ if not self.name:
        l = filter(lambda x:x,[self.last_name,self.first_name,self.title])
        self.name = " ".join(l)

class PersonDetail(ContactDetail):
    datalink = 'contacts.Person'
    box1 = "last_name first_name:15 title:10"

class Persons(Contacts):
    model = "contacts.Person"
    label = _("Persons")
    column_names = "first_name last_name title country id name *"
    can_delete = True
    order_by = "last_name first_name id"
    #can_view = perms.is_authenticated
    

class PersonsByCountry(Persons):
    fk_name = 'country'
    order_by = "city addr1"
    column_names = "city addr1 name nationality language"

class PersonsByNationality(Persons):
    fk_name = 'nationality'
    order_by = "city addr1"
    column_names = "city addr1 name country language"


class CompanyType(models.Model):
    #~ id = models.CharField(max_length=10,primary_key=True)
    abbr = models.CharField(max_length=10,verbose_name=_("Abbreviation"))
    name = models.CharField(max_length=200,verbose_name=_("Designation"))
    def __unicode__(self):
        return self.name
        
class CompanyTypes(reports.Report):
    model = 'contacts.CompanyType'
    label = _("Company types")
        
  
class Company(Contact):
    class Meta:
        abstract = True
        app_label = 'contacts'
#~ class CompanyMixin:
    
    vat_id = models.CharField(max_length=200,blank=True)
    type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,verbose_name=_("Company type"))
    
    #~ def as_address(self,linesep="\n<br/>"):
        #~ s = Contact.as_address(self,linesep)
        #~ return self.name + linesep + s

class CompanyDetail(ContactDetail):
    datalink = 'contacts.Company'
    box1 = """name 
    vat_id:12"""
              
class Companies(Contacts):
    label = _("Companies")
    column_names = "name country city id address *"
    model = 'contacts.Company'
    order_by = "name"
    
class CompaniesByCountry(Companies):
    fk_name = 'country'
    column_names = "city addr1 name country language"
    order_by = "city addr1"
    

