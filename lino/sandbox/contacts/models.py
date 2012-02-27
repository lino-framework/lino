# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
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

"""
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd
#~ from lino.utils.mti import EnableChild
from lino.modlib.countries.models import CountryCity
from lino.utils import babel 
from lino.models import get_site_config
from lino.utils.choicelists import Gender
from lino.utils import join_words




#~ class AddressType(babel.BabelNamed):
    #~ class Meta:
        #~ verbose_name = _("Address Type")
        #~ verbose_name_plural = _("Address Types")
   
#~ class AddressTypes(dd.Table):
    #~ model = AddressType
    #~ column_names = 'name *'
    
    
class Role(babel.BabelNamed):
    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
class Roles(dd.Table):
    model = Role
    column_names = 'name *'


class Address(CountryCity):
  
    class Meta:
        abstract = settings.LINO.abstract_address
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
  
    addr1 = models.CharField(_("Address line before street"),
        max_length=200,blank=True)
    
    street_prefix = models.CharField(_("Street prefix"),max_length=200,blank=True,
        help_text="Text to print before name of street, but to ignore for sorting.")
    
    street = models.CharField(_("Street"),max_length=200,blank=True,
        help_text="Name of street. Without house number.")
    
    street_no = models.CharField(_("No."),max_length=10,blank=True,
        help_text="House number")
    
    street_box = models.CharField(_("Box"),max_length=10,blank=True,
        help_text="Text to print after :attr:`steet_no` on the same line")
    
    addr2 = models.CharField(_("Address line after street"),
        max_length=200,blank=True,
        help_text="Address line to print below street line")
    
    zip_code = models.CharField(_("Zip code"),
        max_length=10,blank=True)
    region = models.CharField(_("Region"),
        max_length=200,blank=True)
    
    def __unicode__(self):
        return self.address_location(', ')

    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()
        
    def get_full_name(self,*args,**kw):
        return self.name
    full_name = property(get_full_name)
        
        
    def address_location_lines(self):
        if self.addr1:
            yield self.addr1
        if self.street:
            yield join_words(
              self.street_prefix, self.street,
              self.street_no,self.street_box)
        if self.addr2:
            yield self.addr2
        if self.region: # format used in Estonia
            if self.city:
                yield unicode(self.city)
            s = join_words(self.zip_code,self.region)
        else: 
            s = join_words(self.zip_code,self.city)
        if s:
            yield s 
        if self.country is not None:
            sc = get_site_config()
            if not sc.site_company or self.country != sc.site_company.address.country: 
                yield unicode(self.country)
            
        
    def address_lines(self):
        for ln in self.address_person_lines() : yield ln
        for ln in self.address_location_lines() : yield ln
          
    def postal_address(self,linesep="\n"):
        """
        The plain text full postal address (person and location). 
        Lines are separated by `linesep`.
        """
        return linesep.join(list(self.address_person_lines()) + list(self.address_location_lines()))
    postal_address.return_type = models.TextField(_("Address"))
    
    def address_location(self,linesep="\n"):
        """
        The plain text postal address location part. 
        Lines are separated by `linesep`.
        """
        return linesep.join(self.address_location_lines())
        
class AddressDetail(dd.DetailLayout):
    address = """
    country region city zip_code
    addr1
    street_prefix street street_no street_box
    addr2
    """
    
if settings.LINO.abstract_address:
  
    AddressableMixin = Address
    
else:  
  
    class AddressableMixin(models.Model):
        class Meta:
            abstract = True
        address = models.ForeignKey(Address,null=True,blank=True)
        
    class Addresses(dd.Table):
        model = Address
        detail_layout = AddressDetail(main="address")
    
    


class Person(AddressableMixin):
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        
    title = models.CharField(_('Title'),max_length=200,blank=True,
        help_text="""
        Text to print as part of the first address line in front of first_name.
        """)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = Gender.field()
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
        
        
    
class PersonDetail(AddressDetail):
    main = """
    title first_name last_name gender
    address
    ContactsByPerson
    """
    
  
class Persons(dd.Table):
    model = Person
    column_names = 'last_name first_name *'
    detail_layout = PersonDetail()


class Company(AddressableMixin):  
    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        
    name = models.CharField(max_length=50)
        
    def __unicode__(self):
        return self.name
        
class CompanyDetail(AddressDetail):
    main = """
    name
    address
    ContactsByCompany
    """
    
class Companies(dd.Table):
    model = Company
    column_names = 'name *'
    detail_layout = CompanyDetail()




class Contact(models.Model):  
    class Meta:
        #~ abstract = True
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        
    person = models.ForeignKey(Person,null=True,blank=True)
    company = models.ForeignKey(Company,null=True,blank=True)
    role = models.ForeignKey(Role,null=True,blank=True)
    
    language = babel.LanguageField()
    
    #~ address = models.ForeignKey(Address,null=True,blank=True)
    #~ address_type = models.ForeignKey(AddressType,blank=True,null=True)
    
    email = models.EmailField(_('E-Mail'),blank=True) # ,null=True)
    url = models.URLField(_('URL'),blank=True)
    phone = models.CharField(_('Phone'),max_length=200,blank=True)
    gsm = models.CharField(_('GSM'),max_length=200,blank=True)
    fax = models.CharField(_('Fax'),max_length=200,blank=True)
    
    def send_mail(self, subject, message, from_email=None):
        "Sends an e-mail to this User."
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email])
        

    
class Contacts(dd.Table):
    model = Contact
    #~ column_names = '*'
    detail_template = """
    person company role
    email url
    phone gsm fax
    """

class ContactsByPerson(Contacts):
    master_key = 'person'
    column_names = "email url phone gsm fax company role *"
    
class ContactsByCompany(Contacts):
    master_key = 'company'
    column_names = "email url phone gsm fax person role *"


#~ class User(Person):
class User(Contact):
  
    _lino_preferred_width = 15 
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    username = models.CharField(_('username'), max_length=30, 
        unique=True, 
        help_text=_("""
        Required. 30 characters or fewer. 
        Letters, numbers and @/./+/-/_ characters
        """))
    is_staff = models.BooleanField(_('is staff'), default=False, 
        help_text=_("""
        Designates whether the user can log into this admin site.
        """))
    is_expert = models.BooleanField(_('is expert'), default=False, 
        help_text=_("""
        Designates whether this user has access to functions that require expert rights.
        """))
    is_active = models.BooleanField(_('is active'), default=True, 
        help_text=_("""
        Designates whether this user should be treated as active. 
        Unselect this instead of deleting accounts.
        """))
    is_superuser = models.BooleanField(_('is superuser'), 
        default=False, 
        help_text=_("""
        Designates that this user has all permissions without 
        explicitly assigning them.
        """))
    last_login = models.DateTimeField(_('last login'), default=datetime.datetime.now)
    date_joined = models.DateTimeField(_('date joined'), default=datetime.datetime.now)

    def __unicode__(self):
        return self.username

    def full_clean(self,*args,**kw):
        if not self.username and self.person:
            self.username = self.person.first_name.lower()
        super(User,self).full_clean(*args,**kw)
        

class Users(Contacts):
    model = User
    column_names = 'username person company is_superuser is_staff *'

    
if settings.LINO.is_installed('contacts'):
    """
    Don't inject fields if contacts is just being imported from some other module.
    """
  
    from lino.models import SiteConfig

    dd.inject_field(SiteConfig,
        'site_company',
        models.ForeignKey(Company,
            blank=True,null=True,
            verbose_name=_("The company that runs this site"),
            related_name='site_company_sites',
            ),
        """The Company to be used as sender in documents.""")
        
    
        
        
NAME = "contacts"
LABEL = _("Contacts")

def setup_main_menu(site,ui,user,m):
    m.add_action(Companies)
    m.add_action(Persons)
    #~ m.add_action(Contacts)
    

def setup_my_menu(site,ui,user,m): 
    pass
  
def setup_config_menu(site,ui,user,m): 
    #~ m = m.add_menu(NAME,LABEL)
    #~ m.add_action(AddressTypes)
    m.add_action(Roles)
    m.add_action(site.modules.countries.Countries)
    m.add_action(site.modules.countries.Cities)
            
  
def setup_explorer_menu(site,ui,user,m):
    #~ m = m.add_menu(NAME,LABEL)
    m.add_action(Contacts)
    if not settings.LINO.abstract_address:
        m.add_action(Addresses)
  