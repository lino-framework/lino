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

#countries = models.get_app('countries')

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
        l = filter(lambda x:x,[self.addr1,self.addr2])
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
    
    
class Company(Contact):    
    vat_id = models.CharField(max_length=200,blank=True)
    
    def as_address(self,linesep="\n<br/>"):
        s = Contact.as_address(self,linesep)
        return self.name + linesep + s
    
    
class Person(Contact):    
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)
    
    def as_address(self,linesep="\n<br/>"):
        s = Contact.as_address(self,linesep)
        l = filter(lambda x:x,[self.title,self.first_name,self.last_name])
        return " ".join(l) + linesep + s

##
## report definitions
##        
        
from django import forms

from lino.utils import reports
from lino.utils import layouts
from lino.utils import perms

countries = models.get_app('countries')

class ContactPageLayout(layouts.PageLayout):
    
    box2 = """email:40 
              url"""
    box3 = """phone
              gsm"""
    box4 = """country region
              city zip_code:10
              addr1:40
              addr2
              """
    box7 = """national_id:15
              language id
              """
    main = """
            box1
            box2 box3
            box4 box7
            remarks:60x6
            """
            
    #~ def documents(self):
        #~ return DocumentsByCustomer()

class PersonPageLayout(ContactPageLayout):
    box1 = """
              last_name first_name:15 title:10 
              """
class CompanyPageLayout(ContactPageLayout):
    box1 = """
              name vat_id:12
              """
              
class ProjectsByPersonPage(layouts.PageLayout):
    main = """
    id title first_name last_name
    ProjectsByPerson
    """

class ProjectsByCompanyPage(layouts.PageLayout):
    main = """
    id name vat_id
    ProjectsByCompany
    """

            
class Persons(reports.Report):
    label = "Personen"
    page_layouts = (PersonPageLayout,ProjectsByPersonPage)
    columnNames = "first_name last_name title country id"
    can_delete = True
    model = Person
    order_by = "name"
    #can_view = perms.is_authenticated

        
class Companies(reports.Report):
    label = "Firmen und Organisationen"
    page_layouts = (CompanyPageLayout,ProjectsByCompanyPage)
    columnNames = "name country id"
    model = Company
    order_by = "name"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    


class PersonsByCountry(reports.Report):
    model = Person # Contact
    master = countries.Country
    order_by = "city addr1"
    columnNames = "city addr1 name"
    
class CompaniesByCountry(PersonsByCountry):
    model = Company
    
class PersonsByCountryPage(layouts.PageLayout):
    label = "Personen pro Land"
    main = """
    isocode name
    PersonsByCountry
    """

class CompaniesByCountryPage(layouts.PageLayout):
    label = "Firmen pro Land"
    main = """
    isocode name
    CompaniesByCountry
    """
    
class Countries(countries.Countries):
    page_layouts = (
      layouts.PageLayout,
      PersonsByCountryPage,
      CompaniesByCountryPage)
    
  

