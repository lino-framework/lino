## Copyright 2008-2009 Luc Saffre.
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

from django.db import models
from django.utils.safestring import mark_safe

#from lino.apps.igen import Model
from lino.apps.countries import models as countries 

#__app_label__ = "contacts"


class Contact(models.Model):
    """
    
Company and/or Person contact data, linked with client account and
choosable for invoicing regarding particular order (if wanting other
invoice to than client default contact). If CompanyName field is
filled, contact record will be presented as CompanyName in contacts
listing - otherwise as Person First- and Lastname.
    
# Examples:
>>> p=Contact.objects.create(lastName="Saffre",firstName="Luc")
>>> unicode(p)
u'Luc Saffre'
>>> p=Contact.objects.create(lastName="Saffre", firstName="Luc", title="Mr.")
>>> unicode(p)
u'Luc Saffre'
>>> p=Contact.objects.create(lastName="Saffre", title="Mr.")
>>> unicode(p)
u'Mr. Saffre'
>>> p=Contact.objects.create(firstName="Luc")
>>> unicode(p)
u'Luc'
>>> p=Contact.objects.create(lastName="Saffre",firstName="Luc", companyName="Example & Co")
>>> unicode(p)
u'Example & Co (Luc Saffre)'
    
    """
    #name = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200,blank=True)
    lastName = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)
    
    companyName = models.CharField(max_length=200,blank=True)
    nationalId = models.CharField(max_length=200,blank=True)
    vatId = models.CharField(max_length=200,blank=True)
    
    addr1 = models.CharField(max_length=200,blank=True)
    addr2 = models.CharField(max_length=200,blank=True)
    country = models.ForeignKey(countries.Country,blank=True,null=True)
    #city = models.ForeignKey("City",blank=True,null=True)
    city = models.CharField(max_length=200,blank=True)
    zipCode = models.CharField(max_length=10,blank=True)
    region = models.CharField(max_length=200,blank=True)
    language = models.ForeignKey(countries.Language,blank=True,null=True)
    
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=200,blank=True)
    gsm = models.CharField(max_length=200,blank=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    remarks = models.TextField(blank=True)
    ordering = ("companyName","lastName","firstName")
    
    def __unicode__(self):
        if self.title and not self.firstName:
            l = filter(lambda x:x,[self.title,self.lastName])
        else:
            l = filter(lambda x:x,[self.firstName,self.lastName])

        s = " ".join(l)
            
        if self.companyName:
            if len(s) > 0:
                return self.companyName + " (" + s + ")"
            else:
                return self.companyName
        else:
            return s
            
    def as_address(self,linesep="\n<br/>"):
        l = filter(lambda x:x,[self.title,self.firstName,self.lastName])
        s = " ".join(l)
        if self.companyName:
            s=self.companyName+linesep+s
        if self.addr1:
          s += linesep+self.addr1
        if self.addr2:
          s += linesep+self.addr2
        if self.city:
          s += linesep+self.city
        if self.zipCode:
          s += linesep+self.zipCode
          if self.region:
            s += " " + self.region
        elif self.region:
            s += linesep+ self.region
        if self.id == 1:
            foreigner = False
        else:
            foreigner = (self.country != Contact.objects.get(id=1).country)
        if foreigner: # (if self.country != sender's country)
            s += linesep + unicode(self.country)
        return mark_safe(s)
        #as_address.allow_tags=True


##
## report definitions
##        
        
from django import forms

from lino.utils import reports
from lino.utils import layouts
from lino.utils import perms

#from lino.plugins.countries import Languages

class ContactPageLayout(layouts.PageLayout):
    #frame = False
    
    box1 = """
              title:10 firstName:15 lastName
              companyName nationalId:12 id
              """
    box2 = """email:40 
              url"""
    box3 = """phone
              gsm"""
    box4 = """country region
              city zipCode:10
              addr1:40
              addr2
              """
    box7 = """vatId:15
              language
              """
    main = """
            box1
            box2 box3
            box4 box7
            remarks:60x6
            """
            
    #~ def documents(self):
        #~ return DocumentsByCustomer()
            
class Contacts(reports.Report):
    page_layouts = (ContactPageLayout,)
    columnNames = "id:3 companyName firstName lastName title country"
    can_delete = True
    model = Contact
    order_by = "id"
    #can_view = perms.is_authenticated

        
class Companies(Contacts):
    #queryset=Contact.objects.order_by("companyName")
    columnNames = "companyName country title firstName lastName"
    exclude = dict(companyName__exact='')
    order_by = "companyName"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    

class Persons(Contacts):
    filter = dict(companyName__exact='')
    order_by = "lastName firstName"
    columnNames = "title firstName lastName country id"
    


class ContactsByCountry(Contacts):
    model = Contact
    master = countries.Country
    order_by = "city addr1"
    
class CountryAndContactsPage(layouts.PageLayout):
    label = "Contacts by Country"
    main = """
    isocode name
    ContactsByCountry
    """
    
    
    #~ def slaves(self):
        #~ return dict(contacts = ContactsByCountry)


class Countries(countries.Countries):
    page_layouts = (layouts.PageLayout,CountryAndContactsPage)
    
  

