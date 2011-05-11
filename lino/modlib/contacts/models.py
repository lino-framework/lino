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
This module deserves more documentation.

It defines tables like `Person` and `Company`

"""

import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django import forms

import lino
from lino import reports
#~ from lino import layouts
from lino.utils import perms

from lino import fields
from lino import mixins
from lino.utils import join_words
from lino.utils.choosers import chooser
from lino.utils.babel import babelattr
from lino.utils import babel 
#~ from lino.mixins.addressable import Addressable, Addressables
from lino.models import get_site_config

from lino.modlib.countries.models import CountryCity


class Addressable(CountryCity):
    """
    Abstract base class for anything that has contact information (postal address, email, phone,...).
    
    """
  
    class Meta:
        abstract = True
  
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    addr1 = models.CharField(_("Address line before street"),
        max_length=200,blank=True,
        help_text="Address line before street")
    
    street = models.CharField(_("Street"),max_length=200,blank=True,
        help_text="Name of street. Without house number.")
    
    street_no = models.CharField(_("No."),max_length=10,blank=True,
        help_text="House number")
    
    street_box = models.CharField(_("Box"),max_length=10,blank=True,
        help_text="Text to print after :attr:`steet_no` on the same line")
    
    addr2 = models.CharField(_("Address line after street"),
        max_length=200,blank=True,
        help_text="Address line to print below street line")
    
    #~ country = models.ForeignKey('countries.Country',
        #~ blank=True,null=True,
        #~ verbose_name=_("Country"),
        #~ help_text="The country where this contact is located.")
    
    #~ city = models.ForeignKey('countries.City',blank=True,null=True,
        #~ verbose_name=_('City'),
        #~ help_text="""
        #~ The city where this contact is located.
        #~ The list of choices for this field is context-sensitive
        #~ and depends on the :attr:`country`.
        #~ """)
    
    #city = models.CharField(max_length=200,blank=True)
    zip_code = models.CharField(_("Zip code"),max_length=10,blank=True)
    region = models.CharField(_("Region"),max_length=200,blank=True)
    #~ language = models.ForeignKey('countries.Language',default=default_language)
    language = fields.LanguageField(default=babel.DEFAULT_LANGUAGE,choices=settings.LANGUAGES)
    
    email = models.EmailField(_('E-Mail'),blank=True,null=True)
    url = models.URLField(_('URL'),blank=True)
    phone = models.CharField(_('Phone'),max_length=200,blank=True)
    gsm = models.CharField(_('GSM'),max_length=200,blank=True)
    fax = models.CharField(_('Fax'),max_length=200,blank=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    remarks = models.TextField(_("Remarks"),blank=True,null=True)
    
    def __unicode__(self):
        return self.name
        
    #~ @chooser()
    #~ def city_choices(cls,country):
        #~ if country is not None:
            #~ return country.city_set.order_by('name')
        #~ return cls.city.field.rel.to.objects.order_by('name')
        
    #~ def create_city_choice(self,text):
        #~ if self.country is not None:
            #~ return self.country.city_set.create(name=text,country=self.country)
        #~ raise Exception("Cannot create city if country is empty")
        

    def address_person_lines(self):
    #~ def recipient_lines(self):
        yield self.name
        
        
    def address_location_lines(self):
        #~ lines = []
        #~ lines = [self.name]
        if self.addr1:
            yield self.addr1
        if self.street:
            yield join_words(self.street,self.street_no,self.street_box)
        if self.addr2:
            yield self.addr2
        #lines = [self.name,street,self.addr1,self.addr2]
        if self.region: # format used in Estonia
            if self.city:
                yield unicode(self.city)
            s = join_words(self.zip_code,self.region)
        else: 
            s = join_words(self.zip_code,self.city)
        if s:
            yield s 
        #~ foreigner = True # False
        #~ if self.id == 1:
            #~ foreigner = False
        #~ else:
            #~ foreigner = (self.country != self.objects.get(pk=1).country)
        sc = get_site_config()
        if not sc.site_company or self.country != sc.site_company.country: 
            # (if self.country != sender's country)
            yield unicode(self.country)
            
        #~ logger.debug('%s : as_address() -> %r',self,lines)
        
    def address_lines(self):
        for ln in self.address_person_lines() : yield ln
        for ln in self.address_location_lines() : yield ln
          
    #~ def address(self,linesep="\n<br/>"):
    def address(self,linesep="\n"):
        """
        The plain text full postal address (person and location). 
        Lines are separated by `linesep`.
        """
        #~ return linesep.join(self.address_lines())
        return linesep.join(list(self.address_person_lines()) + list(self.address_location_lines()))
    address.return_type = models.TextField(_("Address"))
    
    def address_location(self,linesep="\n"):
        """
        The plain text postal address location part. 
        Lines are separated by `linesep`.
        """
        return linesep.join(self.address_location_lines())
    



class Addressables(reports.Report):
    column_names = "name * id" 
    def get_queryset(self):
        return self.model.objects.select_related('country','city')
  


class Person(Addressable):
    """
    Base class for models that represent a physical person. 
    """
    class Meta:
        abstract = True
        #~ app_label = 'contacts'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    first_name = models.CharField(max_length=200,blank=True,
      verbose_name=_('First name'))
    "Space-separated list of all first names."
    
    last_name = models.CharField(max_length=200,blank=True,
      verbose_name=_('Last name'))
    "Last name (family name)."
    
    title = models.CharField(max_length=200,blank=True,
      verbose_name=_('Title'))
    "Text to print as part of the first address line in front of first_name."
        
    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        return u'%s %s' % (self.first_name, self.last_name)
    full_name = property(get_full_name)
    
    def address_person_lines(self):
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
    order_by = "last_name first_name id".split()
    #can_view = perms.is_authenticated

class PersonsByCountry(Persons):
    fk_name = 'country'
    order_by = 'city street street_no street_box addr2'.split()
    column_names = "city street street_no street_box addr2 name language"
    














class PartnerDocument(models.Model):
    """
    This adds two fields 'person' and 'company' to this model, 
    making it something that refers to a "partner". 
    If company is filled, then person means a contact person for this company.
    Otherwise the "partner" is a private person.
    """
    
    class Meta:
        abstract = True
        
    person = models.ForeignKey("contacts.Person",
        blank=True,null=True,
        verbose_name=_("Person"))
    company = models.ForeignKey("contacts.Company",
        blank=True,null=True,verbose_name=_("Company"))
        
    def get_partner(self):
        if self.company is not None:
            return self.company
        return self.person
        

class ContactDocument(PartnerDocument):
    """
    A document whose recipient is a :class:`Contact`.
    """
  
    class Meta:
        abstract = True
        
    contact = models.ForeignKey("contacts.Contact",
      blank=True,null=True,
      verbose_name=_("represented by"))
    language = fields.LanguageField(default=babel.DEFAULT_LANGUAGE)

    @chooser()
    def contact_choices(cls,company):
        if company is not None:
            return company.contact_set.all()
        return []
        #~ print 'Contract.contact_choices for', company
        #~ choices = company.contact_set.all()
        #~ print 'Contract.contact_choices returns', choices
        #~ return choices

    def get_recipient(self):
        if self.contact:
            return self.contact
        if self.company:
            return self.company
        return self.person
    recipient = property(get_recipient)




class CompanyType(models.Model):
    """
    Represents a possible choice for the :class:`Company`.type
    field.
    Implemented by 
    :ref:`dsbe.contacts.CompanyType`
    :ref:`igen.contacts.CompanyType`
    """
    
    class Meta:
        verbose_name = _("company type")
        verbose_name_plural = _("company types")
        
    name = babel.BabelCharField(_("Designation"),max_length=200)
    abbr = babel.BabelCharField(_("Abbreviation"),max_length=30,blank=True)
    
    def __unicode__(self):
        #~ return self.name
        return babelattr(self,'name')
        
        
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
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
    
    vat_id = models.CharField(_("VAT id"),max_length=200,blank=True)
    """The national VAT identification number.
    """
    
    type = models.ForeignKey('contacts.CompanyType',blank=True,null=True,
      verbose_name=_("Company type"))
    """Pointer to this company's :class:`CompanyType`. 
    """
    
              
class Companies(Addressables):
    #~ label = _("Companies")
    #~ column_names = "name country city id address *"
    model = 'contacts.Company'
    order_by = ["name"]
    
    
    
class CompaniesByCountry(Companies):
    fk_name = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()
    

class ContactType(models.Model):
    """
    Implements the :class:`contacts.ContactType` convention.
    """
    class Meta:
        verbose_name = _("contact type")
        verbose_name_plural = _("contact types")
    #~ id = models.CharField(max_length=10,primary_key=True)
    #~ abbr = models.CharField(max_length=30,verbose_name=_("Abbreviation"))
    name = babel.BabelCharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        #~ return self.name
        return babelattr(self,'name')

#~ add_babel_field(ContactType,'name')

class ContactTypes(reports.Report):
    model = 'contacts.ContactType'


class Contact(models.Model):
    """
    Represents a :class:`Person` having a (more or less known) 
    role in a :class:`Company`.
    """
  
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
            
    def address_lines(self):
        for ln in self.person.address_person_lines():
            yield ln
        if self.company:
            for ln in self.company.address_person_lines():
                yield ln
            for ln in self.company.address_location_lines():
                yield ln
        else:
            for ln in self.person.address_location_lines():
                yield ln

class ContactsByCompany(reports.Report):
    model = 'contacts.Contact'
    fk_name = 'company'
    column_names = 'person type *'

class ContactsByPerson(reports.Report):
    label = _("Contact for")
    model = 'contacts.Contact'
    fk_name = 'person'
    column_names = 'company type *'
    
        

from lino.models import SiteConfig
#~ from lino.tools import resolve_field
    
field = models.ForeignKey("contacts.Company",
        blank=True,null=True,
        verbose_name=_("The company that runs this site"),
        related_name='site_company_sites',
        )
field.__doc__ = """
The Company to be used as sender in documents. Needs more documentation.
"""
SiteConfig.add_to_class('site_company',field)

field = models.IntegerField(
        default=1,
        verbose_name=_("The next automatic id for Person or Company"),
        )
field.__doc__ = """
The next automatic id for Person or Company. Needs more documentation.
"""
SiteConfig.add_to_class('next_partner_id',field)
        
