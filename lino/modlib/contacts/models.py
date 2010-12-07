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
#~ from lino import layouts
from lino.utils import perms

from lino import fields
from lino.modlib.contacts.utils import join_words
from lino.utils.babel import add_babel_field, default_language, babelattr


    
#~ def name_default(obj):
    #~ l = filter(lambda x:x,[obj.last_name,obj.first_name,obj.title])
    #~ return " ".join(l)
        
#~ Contact.name.default = name_default

    

#~ class ContactMixin:
class Addressable(models.Model):
    """
    Implements the :class:`contacts.Contact` convention.
    """
  
    class Meta:
        abstract = True
  
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    street = models.CharField(_("Street"),max_length=200,blank=True)
    street_no = models.CharField(_("No."),max_length=10,blank=True)
    street_box = models.CharField(_("Box"),max_length=10,blank=True)
    addr1 = models.CharField(max_length=200,blank=True)
    #addr2 = models.CharField(max_length=200,blank=True)
    
    country = models.ForeignKey('countries.Country',blank=True,null=True,
      verbose_name=_("Country"))
    "See :meth:`contacts.Contact.country`"
    
    city = models.ForeignKey('countries.City',blank=True,null=True,
        verbose_name=_('City'))
    "See :meth:`contacts.Contact.city`"
    
    #city = models.CharField(max_length=200,blank=True)
    zip_code = models.CharField(_("Zip code"),max_length=10,blank=True)
    region = models.CharField(_("Region"),max_length=200,blank=True)
    #~ language = models.ForeignKey('countries.Language',default=default_language)
    language = fields.LanguageField(default=default_language)
    
    email = models.EmailField(_('E-Mail'),blank=True,null=True)
    url = models.URLField(blank=True,verbose_name=_('URL'))
    phone = models.CharField(max_length=200,blank=True,verbose_name=_('Phone'))
    gsm = models.CharField(max_length=200,blank=True,verbose_name=_('GSM'))
    fax = models.CharField(max_length=200,blank=True,verbose_name=_('Fax'))
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    remarks = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return self.name
        
    def recipient_lines(self):
        yield self.name
        
    def address(self,linesep="\n<br/>"):
        "Implements :meth:`contacts.Contact.address`"
        return linesep.join(self.address_lines()) # ', ')
    address.return_type = models.TextField(_("Address"))
    
        
    def address_lines(self,linesep="\n<br/>"):
        #~ lines = []
        #~ lines = [self.name]
        if self.addr1:
            yield self.addr1
        if self.street:
            yield join_words(self.street,self.street_no,self.street_box)
        #lines = [self.name,street,self.addr1,self.addr2]
        if self.region: # format used in Estonia
            if self.city:
                yield unicode(self.city)
            s = join_words(self.zip_code,self.region)
        else: 
            s = join_words(self.zip_code,self.city)
        if s:
            yield s 
        foreigner = True # False
        #~ if self.id == 1:
            #~ foreigner = False
        #~ else:
            #~ foreigner = (self.country != self.objects.get(pk=1).country)
        if foreigner and self.country: # (if self.country != sender's country)
            yield unicode(self.country)
        #~ logger.debug('%s : as_address() -> %r',self,lines)
        #~ return mark_safe(linesep.join(lines))
        
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
        pass
        #~ print "lino.modlib.contacts.Contacts.on_create()"
        #~ instance.language = 
        
class Addressables(reports.Report):
    column_names = "name * id" 
    def get_queryset(self):
        return self.model.objects.select_related('country','city')
  

class Person(Addressable):
    """
    Implements the :class:`contacts.Person` convention.
    """
    class Meta:
        abstract = True
        app_label = 'contacts'
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    first_name = models.CharField(max_length=200,blank=True,
      verbose_name=_('First name'))
    last_name = models.CharField(max_length=200,blank=True,
      verbose_name=_('Last name'))
    title = models.CharField(max_length=200,blank=True,
      verbose_name=_('Title'))
        
    
    #~ def save(self,*args,**kw):
        #~ self.before_save()
        #~ r = super(Person,self).save(*args,**kw)
        #~ return r
        
    def recipient_lines(self):
        if self.title:
            yield self.title
        l = filter(lambda x:x,[self.first_name,self.last_name])
        yield  " ".join(l)
        
    def full_clean(self,*args,**kw):
    #~ def before_save(self):
        #~ if not self.name:
        #~ l = filter(lambda x:x,[self.last_name,self.first_name,self.title])
        l = filter(lambda x:x,[self.last_name,self.first_name])
        self.name = " ".join(l)
        super(Person,self).full_clean(*args,**kw)

#~ class PersonDetail(ContactDetail):
    #~ datalink = 'contacts.Person'
    #~ box1 = "last_name first_name:15 title:10"

class Persons(Addressables):
    model = "contacts.Person"
    #~ label = _("Persons")
    #~ column_names = "first_name last_name title country id name *"
    can_delete = True
    order_by = "last_name first_name id"
    #can_view = perms.is_authenticated

class PersonsByCountry(Persons):
    fk_name = 'country'
    order_by = "city addr1"
    column_names = "city addr1 name language"
    

class CompanyType(models.Model):
    """
    Implements the :class:`contacts.CompanyType` convention.
    """
    class Meta:
        verbose_name = _("company type")
        verbose_name_plural = _("company types")
    name = models.CharField(_("Designation"),max_length=200)
    abbr = models.CharField(_("Abbreviation"),max_length=30,blank=True)
    
    def __unicode__(self):
        return self.name
        
add_babel_field(CompanyType,'abbr')
add_babel_field(CompanyType,'name')
        
class CompanyTypes(reports.Report):
    model = 'contacts.CompanyType'
    column_names = 'name *'
    #~ label = _("Company types")
        

class Company(Addressable):
    """
    Implements the :class:`contacts.Company` convention.
    See also :doc:`/tickets/14`.
    """
    class Meta:
        abstract = True
        app_label = 'contacts'
    
    vat_id = models.CharField(max_length=200,blank=True)
    type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,
      verbose_name=_("Company type"))
    """Pointer to this company's :class:`CompanyType`. 
    """
    
              
class Companies(Addressables):
    #~ label = _("Companies")
    #~ column_names = "name country city id address *"
    model = 'contacts.Company'
    order_by = "name"
    
    
    
class CompaniesByCountry(Companies):
    fk_name = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no"
    

class ContactType(models.Model):
    """
    Implements the :class:`contacts.ContactType` convention.
    """
    class Meta:
        verbose_name = _("contact type")
        verbose_name_plural = _("contact types")
    #~ id = models.CharField(max_length=10,primary_key=True)
    #~ abbr = models.CharField(max_length=30,verbose_name=_("Abbreviation"))
    name = models.CharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        return self.name

add_babel_field(ContactType,'name')

class ContactTypes(reports.Report):
    model = 'contacts.ContactType'


class Contact(models.Model):
  
    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")
        
    person = models.ForeignKey('contacts.Person',verbose_name=_("person"))
    company = models.ForeignKey('contacts.Company',blank=True,null=True,
      verbose_name=_("company"))
    type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      verbose_name=_("contact type"))

    def __unicode__(self):
        if self.person_id is None:
            return super(Contact,self).__unicode__()
        if self.type is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.type)
        #~ return unicode(self.person)
        #~ if self.company_id is not None:
            #~ if self.person_id is not None:
                #~ return u"%s (%s)" % (self.company, self.person)
            #~ return unicode(self.company)

class ContactsByCompany(reports.Report):
    model = 'contacts.Contact'
    fk_name = 'company'
    column_names = 'person type *'

class ContactsByPerson(reports.Report):
    label = _("Contact for")
    model = 'contacts.Contact'
    fk_name = 'person'
    column_names = 'company type *'
    
        