# -*- coding: UTF-8 -*-
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

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
#~ from django.utils.translation import ugettext

from django import forms
from django.utils import translation


import lino
from lino import reports
#~ from lino import layouts
from lino.utils import perms

from lino import fields
from lino import mixins
from lino.utils import join_words
from lino.utils.choosers import chooser
from lino.utils.choicelists import Gender
from lino.utils import babel 
from lino.models import get_site_config

from lino.modlib.countries.models import CountryCity

from lino.modlib.contacts.utils import get_salutation
#~ from lino.modlib.contacts.utils import GENDER_CHOICES, get_salutation
from lino.utils import join_words



from lino.utils import mti

class CompanyType(babel.BabelNamed):
    """
    Represents a possible choice for the  `type`
    field of a :class:`Company`.
    """
    
    class Meta:
        verbose_name = _("company type")
        verbose_name_plural = _("company types")
        
    abbr = babel.BabelCharField(_("Abbreviation"),max_length=30,blank=True)
    
        
class CompanyTypes(reports.Report):
    model = 'contacts.CompanyType'
    column_names = 'name *'
    #~ label = _("Company types")




class Contact(mti.MultiTableBase,CountryCity):
    """
    Base class for anything that has contact information 
    (postal address, email, phone,...).
    
    """
  
    class Meta:
        #~ abstract = True
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
  
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    addr1 = models.CharField(_("Address line before street"),
        max_length=200,blank=True,
        help_text="Address line before street")
    
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
    language = babel.LanguageField()
    
    email = models.EmailField(_('E-Mail'),blank=True) # ,null=True)
    url = models.URLField(_('URL'),blank=True)
    phone = models.CharField(_('Phone'),max_length=200,blank=True)
    gsm = models.CharField(_('GSM'),max_length=200,blank=True)
    fax = models.CharField(_('Fax'),max_length=200,blank=True)
    
    remarks = models.TextField(_("Remarks"),blank=True) # ,null=True)
    
    def save(self,*args,**kw):
        if self.id is None:
            sc = get_site_config()
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        super(Contact,self).save(*args,**kw)
        
    def __unicode__(self):
        return self.name

    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()
        
    def get_full_name(self,*args,**kw):
        """\
Returns a one-line string representing this Contact.
The default returns simply the `name` field, ignoring any parameters, 
but e.g. :class:`Person` overrides this.
        """
        
        #~ try:
            #~ p = getattr(self,'person')
            #~ return p.get_full_name(*args,**kw)
        #~ except ObjectDoesNotExist:
            #~ pass
        return self.name
    full_name = property(get_full_name)
        
        
    def address_location_lines(self):
        #~ lines = []
        #~ lines = [self.name]
        if self.addr1:
            yield self.addr1
        if self.street:
            yield join_words(self.street_prefix, self.street,self.street_no,self.street_box)
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
        if self.country is not None:
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
    

class Contacts(reports.Report):
    model = 'contacts.Contact'
    column_names = "name email * id" 
    order_by = ['name','id']
    #~ column_names = "name * id" 
    
    def get_queryset(self):
        return self.model.objects.select_related('country','city')


class AllContacts(Contacts):
    def init_label(self):
        return _("All %s") % self.model._meta.verbose_name_plural
        
class ContactsByCity(Contacts):
    fk_name = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 name language *"
    
class ContactsByCountry(Contacts):
    fk_name = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()
    
        


#~ def GenderField(**kw):
    #~ options = dict(max_length=1,blank=True,# null=True,
        #~ verbose_name=_("Gender"),choices=Gender.get_choices()) 
    #~ options.update(kw)
    #~ return models.CharField(**options)
        

class Born(models.Model):
    """
    Abstract base class that adds a `birth_date` 
    field and a virtual field "Age".
    """
    class Meta:
        abstract = True
        
    birth_date = fields.IncompleteDateField(
        blank=True,
        verbose_name=_("Birth date"))
        
    #~ birth_date = models.DateField(
        #~ blank=True,null=True,
        #~ verbose_name=_("Birth date"))
    #~ birth_date_circa = models.BooleanField(
        #~ default=False,
        #~ verbose_name=_("not exact"))
        
    def age(self,request,today=None):
        if self.birth_date and self.birth_date.year:
            if today is None:
                today = datetime.date.today()
            try:
                dd = today - self.birth_date.as_date()
            except ValueError:
                pass
            else:
                s = _("%d years") % (dd.days / 365)
                if self.birth_date.is_complete():
                    return s
                return u"±" + s
        return _('unknown')
    age.return_type = fields.DisplayField(_("Age"))
    


class Person(models.Model):
    """
    Base class for models that represent a physical person. 
    """
    class Meta:
        abstract = True
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
        
    #~ gender = GenderField()
    gender = Gender.field()
        
    def get_salutation(self,**salutation_options):
        return get_salutation(
            #~ translation.get_language(),
            self.gender,**salutation_options)
    
        
    def get_full_name(self,salutation=True,**salutation_options):
        """Returns a one-line string composed of salutation, first_name and last_name.
        
The optional keyword argument `salutation` can be set to `False` 
to suppress salutations. 
See :func:`lino.apps.dsbe.tests.dsbe_tests.test04` 
and
:func:`lino.modlib.contacts.tests.test01` 
for some examples.

Optional `salutation_options` see :func:`get_salutation`.
        """
        #~ return '%s %s' % (self.first_name, self.last_name.upper())
        words = []
        if salutation:
            words.append(self.get_salutation(**salutation_options))
        words += [self.first_name, self.last_name.upper()]
        return join_words(*words)
    full_name = property(get_full_name)
    #~ full_name.return_type = models.CharField(max_length=200,verbose_name=_('Full name'))
    
    def address_person_lines(self,*args,**kw):
        "Deserves more documentation."
        if self.title:
            yield self.title
        yield self.get_full_name(*args,**kw)
        #~ l = filter(lambda x:x,[self.first_name,self.last_name])
        #~ yield  " ".join(l)
        
    def full_clean(self,*args,**kw):
        l = filter(lambda x:x,[self.last_name,self.first_name])
        self.name = " ".join(l)
        super(Person,self).full_clean(*args,**kw)


class Persons(reports.Report):
    model = 'contacts.Person'
    order_by = "last_name first_name id".split()
    #~ app_label = 'contacts'
    


class CompanyMixin(models.Model):
#~ class Company(Contact):
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
    
    #~ def get_full_name(self,**salutation_options):
    def get_full_name(self,salutation=True,**salutation_options):
        """Deserves more documentation."""
        if self.type:
            return join_words(self.type.abbr,self.name)
        return self.name
    full_name = property(get_full_name)
    
    #~ @classmethod
    #~ def site_setup(cls,lino):
        #~ raise Exception('20110810')


              
#~ class Companies(Contacts):
    #~ model = 'contacts.Company'
    #~ order_by = ["name"]
    
    
    



# class ContactType(babel.BabelNamed):
class RoleType(babel.BabelNamed):
    """
    Deserves more documentation.
    """
    class Meta:
        verbose_name = _("Role Type")
        verbose_name_plural = _("Role Types")


class RoleTypes(reports.Report):
    model = 'contacts.RoleType'


#~ class Contact(models.Model):
#~ class RoleOccurence(models.Model):
class Role(models.Model):
#~ class unused_Role(object):
    """
    The role of a given :class:`Person` in a given :class:`Company`.
    """
  
    class Meta:
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")
        
    #~ parent = models.ForeignKey('contacts.Contact',
        #~ verbose_name=_("Parent Contact"),
        #~ related_name='rolesbyparent')
    #~ child = models.ForeignKey('contacts.Contact',
        #~ verbose_name=_("Child Contact"),
        #~ related_name='rolesbychild')
    type = models.ForeignKey('contacts.RoleType',
      blank=True,null=True,
      verbose_name=_("Contact Role"))
    person = models.ForeignKey('contacts.Person',related_name='rolesbyperson')
    company = models.ForeignKey('contacts.Company',related_name='rolesbycompany')
    #~ type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))

    #~ def __unicode__(self):
        #~ if self.person_id is None:
            #~ return super(Contact,self).__unicode__()
        #~ if self.type is None:
            #~ return unicode(self.person)
        #~ return u"%s (%s)" % (self.person, self.type)
    def __unicode__(self):
        if self.person_id is None:
            return super(Role,self).__unicode__()
        if self.type is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.company, self.type)
            
    #~ def address_lines(self):
        #~ for ln in self.person.address_person_lines():
            #~ yield ln
        #~ if self.company:
            #~ for ln in self.company.address_person_lines():
                #~ yield ln
            #~ for ln in self.company.address_location_lines():
                #~ yield ln
        #~ else:
            #~ for ln in self.person.address_location_lines():
                #~ yield ln
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

#~ class ContactsByCompany(reports.Report):
    #~ model = 'contacts.RoleOccurence'
    #~ fk_name = 'company'
    #~ column_names = 'person type *'

#~ class ContactsByPerson(reports.Report):
    #~ label = _("Contact for")
    #~ model = 'contacts.RoleOccurence'
    #~ fk_name = 'person'
    #~ column_names = 'company type *'
    
class Roles(reports.Report):
    model = 'contacts.Role'   
    
class RolesByCompany(Roles):
    label = _("Contact persons")
    fk_name = 'company'
    column_names = 'person type *'

class RolesByPerson(Roles):
    label = _("Contact for")
    fk_name = 'person'
    column_names = 'company type *'
    
    
    
class PartnerDocument(models.Model):
    """
    Maybe deprecated. 
    This adds two fields 'person' and 'company' to this model, 
    making it something that refers to a "partner". 
    If `company` is empty, the "partner" is a private person.
    If `company` is filled, then `person` means a "contact person" 
    for this company.
    
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
        
    def get_mailable_contacts(self):
        for p in self.company, self.person:
            if p is not None and p.email:
                #~ yield "%s <%s>" % (p, p.email)
                yield ('to', p)
                #~ yield ('to', unicode(p), p.email)
        
        
    #~ def summary_row(self,ui,rr,**kw):
        #~ if self.person:
            #~ if self.company:
                #~ # s += ": " + ui.href_to(self.person) + " / " + ui.href_to(self.company)
                #~ return ui.href_to(self.company) + ' ' + ugettext("attn:") + ' ' + ui.href_to(self.person)
            #~ else:
                #~ return ui.href_to(self.person)
        #~ elif self.company:
            #~ return ui.href_to(self.company)
            
    def summary_row(self,ui,rr,**kw):
        s = ui.href_to(self)
        if self.person and not reports.has_fk(rr,'person'):
            if self.company:
                s += " (" + ui.href_to(self.person) + "/" + ui.href_to(self.company) + ")"
            else:
                s += " (" + ui.href_to(self.person) + ")"
        elif self.company:
            s += " (" + ui.href_to(self.company) + ")"
        return s
            
    def update_owned_instance(self,task):
        task.person = self.person
        task.company = self.company
        
class ContactDocument(models.Model):
    """
    A document whose recipient is a :class:`Contact`.
    """
  
    class Meta:
        abstract = True
        
    contact = models.ForeignKey("contacts.Contact",
        #~ blank=True,null=True,
        related_name="%(app_label)s_%(class)s_by_contact",
        #~ related_name="%(app_label)s_%(class)s_related",
        verbose_name=_("Contact"))
    language = babel.LanguageField(default=babel.DEFAULT_LANGUAGE)

    def get_mailable_contacts(self):
        yield ('to',self.contact)

    def get_recipient(self):
        return self.contact
    recipient = property(get_recipient)



    


if reports.is_installed('contacts'):
  
    from lino.models import SiteConfig

    reports.inject_field(SiteConfig,
        'next_partner_id',
        models.IntegerField(default=100, # first 100 for users from demo fixtures.
            verbose_name=_("The next automatic id for Person or Company")
        ),"""The next automatic id for Person or Company. 
        Deserves more documentation.
        """)
        
    reports.inject_field(SiteConfig,
        'site_company',
        models.ForeignKey("contacts.Company",
            blank=True,null=True,
            verbose_name=_("The company that runs this site"),
            related_name='site_company_sites',
            ),
        """The Company to be used as sender in documents.""")
        

    reports.inject_field(Contact,
        'is_person',
        mti.EnableChild('contacts.Person',verbose_name=_("is Person")),
        """Whether this Contact is also a Person."""
        )
    reports.inject_field(Contact,
        'is_company',
        mti.EnableChild('contacts.Company',verbose_name=_("is Company")),
        """Whether this Contact is also a Company."""
        )




def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    pass
  
def setup_config_menu(site,ui,user,m): 
    pass
    #~ m  = m.add_menu("contacts",_("~Contacts"))
    #~ m.add_action('contacts.RoleTypes')
  
def setup_explorer_menu(site,ui,user,m):
    pass
  