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

import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.safestring import mark_safe

#from lino.apps.igen import Model
from lino.apps.countries import models as countries 

##
## report definitions
##        
        
from django import forms

from lino.utils import reports
from lino.utils import layouts
from lino.utils import perms

#__app_label__ = "contacts"


class PaymentTerm(models.Model):
    name = models.CharField(max_length=200)
    days = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    #proforma = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
        
    def get_due_date(self,date1):
        assert isinstance(date1,datetime.date), \
          "%s is not a date" % date1
        #~ print type(date1),type(relativedelta(months=self.months,days=self.days))
        d = date1 + relativedelta(months=self.months,days=self.days)
        return d


class PaymentTerms(reports.Report):
    model = PaymentTerm
    order_by = "id"
    can_view = perms.is_staff
    #~ def can_view(self,request):
      #~ return request.user.is_staff




#~ class Contact(models.Model):
    #~ """
    
#~ Company and/or Person contact data, linked with client account and
#~ choosable for invoicing regarding particular order (if wanting other
#~ invoice to than client default contact). If CompanyName field is
#~ filled, contact record will be presented as CompanyName in contacts
#~ listing - otherwise as Person First- and Lastname.
    
#~ # Examples:
#~ >>> p=Contact.objects.create(lastName="Saffre",firstName="Luc")
#~ >>> unicode(p)
#~ u'Luc Saffre'
#~ >>> p=Contact.objects.create(lastName="Saffre", firstName="Luc", title="Mr.")
#~ >>> unicode(p)
#~ u'Luc Saffre'
#~ >>> p=Contact.objects.create(lastName="Saffre", title="Mr.")
#~ >>> unicode(p)
#~ u'Mr. Saffre'
#~ >>> p=Contact.objects.create(firstName="Luc")
#~ >>> unicode(p)
#~ u'Luc'
#~ >>> p=Contact.objects.create(lastName="Saffre",firstName="Luc", companyName="Example & Co")
#~ >>> unicode(p)
#~ u'Example & Co (Luc Saffre)'
    
    #~ """
    
    #~ #name = models.CharField(max_length=200)
    #~ companyName = models.CharField(max_length=200,blank=True)
    #~ nationalId = models.CharField(max_length=200,blank=True)
    #~ vatId = models.CharField(max_length=200,blank=True)
    
    #~ addr1 = models.CharField(max_length=200,blank=True)
    #~ addr2 = models.CharField(max_length=200,blank=True)
    #~ country = models.ForeignKey(countries.Country,blank=True,null=True)
    #~ #city = models.ForeignKey("City",blank=True,null=True)
    #~ city = models.CharField(max_length=200,blank=True)
    #~ zipCode = models.CharField(max_length=10,blank=True)
    #~ region = models.CharField(max_length=200,blank=True)
    #~ language = models.ForeignKey(countries.Language,blank=True,null=True)
    
    #~ email = models.EmailField(blank=True)
    #~ url = models.URLField(blank=True)
    #~ phone = models.CharField(max_length=200,blank=True)
    #~ gsm = models.CharField(max_length=200,blank=True)
    #~ #image = models.ImageField(blank=True,null=True,
    #~ # upload_to=".")
    
    #~ remarks = models.TextField(blank=True)
    #~ ordering = ("companyName","lastName","firstName")
    
    #~ def __unicode__(self):
        #~ if self.title and not self.firstName:
            #~ l = filter(lambda x:x,[self.title,self.lastName])
        #~ else:
            #~ l = filter(lambda x:x,[self.firstName,self.lastName])

        #~ s = " ".join(l)
            
        #~ if self.companyName:
            #~ if len(s) > 0:
                #~ return self.companyName + " (" + s + ")"
            #~ else:
                #~ return self.companyName
        #~ else:
            #~ return s
            
    #~ def as_address(self,linesep="\n<br/>"):
        #~ l = filter(lambda x:x,[self.title,self.firstName,self.lastName])
        #~ s = " ".join(l)
        #~ if self.companyName:
            #~ s=self.companyName+linesep+s
        #~ if self.addr1:
          #~ s += linesep+self.addr1
        #~ if self.addr2:
          #~ s += linesep+self.addr2
        #~ if self.city:
          #~ s += linesep+self.city
        #~ if self.zipCode:
          #~ s += linesep+self.zipCode
          #~ if self.region:
            #~ s += " " + self.region
        #~ elif self.region:
            #~ s += linesep+ self.region
        #~ if self.id == 1:
            #~ foreigner = False
        #~ else:
            #~ foreigner = (self.country != Contact.objects.get(id=1).country)
        #~ if foreigner: # (if self.country != sender's country)
            #~ s += linesep + unicode(self.country)
        #~ return mark_safe(s)
        #~ #as_address.allow_tags=True

class Contact(models.Model):
  
    class Meta:
        abstract = True
        
    name = models.CharField(max_length=200)
    national_id = models.CharField(max_length=200,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    addr2 = models.CharField(max_length=200,blank=True)
    country = models.ForeignKey('countries.Country',blank=True,null=True)
    #city = models.ForeignKey("City",blank=True,null=True)
    city = models.CharField(max_length=200,blank=True)
    zip_code = models.CharField(max_length=10,blank=True)
    region = models.CharField(max_length=200,blank=True)
    language = models.ForeignKey('countries.Language',blank=True,null=True)
    
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=200,blank=True)
    gsm = models.CharField(max_length=200,blank=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    remarks = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
        
    def as_address(self,linesep="\n<br/>"):
        l = filter(lambda x:x,[self.name,self.addr1,self.addr2])
        s = linesep.join(l)
        if self.city:
          s += linesep+self.city
        if self.zipCode:
          s += linesep+self.zipCode
          if self.region:
            s += " " + self.region
        elif self.region:
            s += linesep + self.region
        if self.id == 1:
            foreigner = False
        else:
            foreigner = (self.country != Contact.objects.get(id=1).country)
        if foreigner: # (if self.country != sender's country)
            s += linesep + unicode(self.country)
        return mark_safe(s)
    
class ContactPageLayout(layouts.PageLayout):
    #frame = False
    
    box3 = """country region
              city zip_code:10
              addr1:40
              addr2
              """
    box4 = """email:40 
              url
              phone
              gsm
              """
    box7 = """national_id:15
              language
              """
    main = """box1 box7
              box3 box4
              remarks:60x6
              """
       
 

class Person(Contact):    
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)
    nationality = models.ForeignKey('countries.Country',
        blank=True,null=True,
        related_name='by_nationality')
    
    def save(self,*args,**kw):
        self.before_save()
        r = super(Contact,self).save(*args,**kw)
        return r
        
    def before_save(self):
        if True: # not self.name:
            l = filter(lambda x:x,[self.title,self.first_name,self.last_name])
            self.name = " ".join(l)

class PersonPageLayout(ContactPageLayout):
    box1 = "last_name first_name:15 title:10"
    box7 = """national_id:15
              nationality
              language
              """

class Persons(reports.Report):
    #label = "Personen"
    page_layouts = (PersonPageLayout,)
    columnNames = "first_name last_name title country id name"
    can_delete = True
    model = Person
    order_by = "last_name first_name id"
    #can_view = perms.is_authenticated

class PersonsByCountry(reports.Report):
    model = Person # Contact
    master = countries.Country
    fk_name = 'country'
    order_by = "city addr1"
    columnNames = "city addr1 name nationality language"

class PersonsByNationality(reports.Report):
    model = Person # Contact
    master = countries.Country
    fk_name = 'nationality'
    order_by = "city addr1"
    columnNames = "city addr1 name country language"



class Company(Contact):
    vat_id = models.CharField(max_length=200,blank=True)
    
    def as_address(self,linesep="\n<br/>"):
        s = Contact.as_address(self,linesep)
        return self.name + linesep + s

class CompanyPageLayout(ContactPageLayout):
    box1 = "name vat_id:12"
              
class Companies(reports.Report):
    #label = "Companies"
    page_layouts = (CompanyPageLayout,)
    columnNames = "name country id"
    model = Company
    order_by = "name"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    
class CompaniesByCountry(reports.Report):
    model = Company
    master = countries.Country
    columnNames = "city addr1 name country language"
    order_by = "city addr1"
    
class PersonsByCountryPage(layouts.PageLayout):
    label = "Persons by Country"
    main = """
    isocode name
    PersonsByCountry
    """
countries.Countries.register_page_layout(PersonsByCountryPage)

class CompaniesByCountryPage(layouts.PageLayout):
    label = "Companies by Country"
    main = """
    isocode name
    CompaniesByCountry
    """
countries.Countries.register_page_layout(CompaniesByCountryPage)

        
class Partner(models.Model):
    name = models.CharField("Searchname",max_length=30)
    company = models.ForeignKey(Company,blank=True,null=True)
    person = models.ForeignKey(Person,blank=True,null=True)
    payment_term = models.ForeignKey("PaymentTerm",blank=True,null=True)
    vat_exempt = models.BooleanField(default=False)
    item_vat = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.company:
            return unicode(self.company)
        return unicode(self.person)

class PartnerPageLayout(layouts.PageLayout):
    main = """
           company person
           payment_term 
           vat_exempt item_vat
           """
    
class Partners(reports.Report):
    page_layouts = (PartnerPageLayout,)
    columnNames = "company person payment_term vat_exempt item_vat"
    can_delete = True
    model = Partner
    order_by = "id"
    #can_view = perms.is_authenticated




            
#~ class Contacts(reports.Report):
    #~ page_layouts = (ContactPageLayout,)
    #~ columnNames = "id:3 companyName firstName lastName title country"
    #~ can_delete = True
    #~ model = Contact
    #~ order_by = "id"
    #~ #can_view = perms.is_authenticated

        
#~ class Companies(Contacts):
    #~ #queryset=Contact.objects.order_by("companyName")
    #~ columnNames = "companyName country title firstName lastName"
    #~ exclude = dict(companyName__exact='')
    #~ order_by = "companyName"
    

#~ class Persons(Contacts):
    #~ filter = dict(companyName__exact='')
    #~ order_by = "lastName firstName"
    #~ columnNames = "title firstName lastName country id"
    


#~ class ContactsByCountry(Contacts):
    #~ model = Contact
    #~ master = countries.Country
    #~ order_by = "city addr1"
    
#~ class CountryAndContactsPage(layouts.PageLayout):
    #~ label = "Contacts by Country"
    #~ main = """
    #~ isocode name
    #~ ContactsByCountry
    #~ """
    
    


#~ class Countries(countries.Countries):
    #~ page_layouts = (layouts.PageLayout,CountryAndContactsPage)
    
  

