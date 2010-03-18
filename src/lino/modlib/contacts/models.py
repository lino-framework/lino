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
from django.utils.translation import ugettext as _

#from lino.modlib.countries import models as countries
#countries = reports.get_app('countries')

from django import forms

import lino
from lino import reports
from lino import layouts
from lino.utils import perms

from lino.modlib.contacts.utils import join_words
from lino.modlib.documents.utils import Printable

class Contact(models.Model,Printable):
  
    class Meta:
        abstract = True
        
    name = models.CharField(max_length=200)
    national_id = models.CharField(max_length=200,blank=True)
    street = models.CharField(_("Street"),max_length=200,blank=True)
    street_no = models.CharField(_("No."),max_length=10,blank=True)
    street_box = models.CharField(_("Box"),max_length=10,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    #addr2 = models.CharField(max_length=200,blank=True)
    country = models.ForeignKey('countries.Country',blank=True,null=True)
    city = models.ForeignKey('countries.City',blank=True,null=True)
    #city = models.CharField(max_length=200,blank=True)
    zip_code = models.CharField(max_length=10,blank=True)
    region = models.CharField(max_length=200,blank=True)
    language = models.ForeignKey('countries.Language',blank=True,null=True)
    
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
        lino.log.debug('%s : as_address() -> %r',self,lines)
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
        
class Contacts(reports.Report):
    pass
  
class ContactDetail(layouts.DetailLayout):
    box1 = "name"
    box2 = """national_id:15
              language
              """
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
    bottom_box = "remarks:60x6"
    main = """intro_box
              address_box
              bottom_box
              """
              
    #collapsible_elements = dict(bottom_box=_("Bottom"),address_box=_("Address"))
       
 

class Person(Contact):    
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)
    nationality = models.ForeignKey('countries.Country',
        blank=True,null=True,
        related_name='by_nationality')
        
    class Meta:
        abstract = True
        app_label = 'contacts'
    
    def save(self,*args,**kw):
        self.before_save()
        r = super(Person,self).save(*args,**kw)
        return r
        
    def before_save(self):
        if not self.name:
            l = filter(lambda x:x,[self.last_name,self.first_name,self.title])
            self.name = " ".join(l)

class PersonDetail(ContactDetail):
    layout_model = 'contacts.Person'
    box1 = "last_name first_name:15 title:10"
    box2 = """national_id:15 id
              nationality language
              """

class Persons(Contacts):
    model = "contacts.Person"
    label = _("Persons")
    column_names = "first_name last_name title country id name"
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



class Company(Contact):
    class Meta:
        abstract = True
        app_label = 'contacts'
    
    vat_id = models.CharField(max_length=200,blank=True)
    
    #~ def as_address(self,linesep="\n<br/>"):
        #~ s = Contact.as_address(self,linesep)
        #~ return self.name + linesep + s

class CompanyDetail(ContactDetail):
    layout_model = 'contacts.Company'
    box1 = """name 
    vat_id:12"""
              
class Companies(Contacts):
    label = _("Companies")
    column_names = "name country city id address"
    model = 'contacts.Company'
    order_by = "name"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    
class CompaniesByCountry(Companies):
    fk_name = 'country'
    column_names = "city addr1 name country language"
    order_by = "city addr1"
    
#~ class PersonsByCountryPage(layouts.DetailLayout):
    #~ label = "Persons by Country"
    #~ main = """
    #~ isocode name
    #~ PersonsByCountry
    #~ """
#~ countries.Countries.register_page_layout(PersonsByCountryPage)

#~ class CompaniesByCountryPage(layouts.DetailLayout):
    #~ label = "Companies by Country"
    #~ main = """
    #~ isocode name
    #~ CompaniesByCountry
    #~ """
#~ countries.Countries.register_page_layout(CompaniesByCountryPage)

        



            
#~ class Contacts(reports.Report):
    #~ column_names = "id:3 companyName firstName lastName title country"
    #~ can_delete = True
    #~ model = Contact
    #~ order_by = "id"
    #~ #can_view = perms.is_authenticated

        
#~ class Companies(Contacts):
    #~ #queryset=Contact.objects.order_by("companyName")
    #~ column_names = "companyName country title firstName lastName"
    #~ exclude = dict(companyName__exact='')
    #~ order_by = "companyName"
    

#~ class Persons(Contacts):
    #~ filter = dict(companyName__exact='')
    #~ order_by = "lastName firstName"
    #~ column_names = "title firstName lastName country id"
    


#~ class ContactsByCountry(Contacts):
    #~ model = "contacts.Partner"
    #~ master = "countries.Country"
    #~ order_by = "city addr1"
    
#~ class CountryAndPartnersPage(layouts.DetailLayout):
    #~ label = "Contacts by Country"
    #~ main = """
    #~ isocode name
    #~ ContactsByCountry
    #~ """
    

    
  

