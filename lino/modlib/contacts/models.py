# -*- coding: UTF-8 -*-
## Copyright 2008-2013 Luc Saffre
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

The :xfile:`models.py` module for the :mod:`lino.modlib.contacs` app.

This module defines the tables 

- :class:`Partner` (and their specializations :class:`Person` and :class:`Company`)
- :class:`Role` and :class:`RoleType`

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)


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
#~ from lino import layouts

from lino import dd
#~ from lino import fields

from lino import mixins

from lino.utils import join_words
from lino.utils.choosers import chooser
#~ from lino.models import get_site_config

#~ from lino.modlib.contacts.utils import Genders

#~ from lino.modlib.countries.models import CountryCity
from lino.modlib.countries.models import CountryRegionCity

from lino.modlib.contacts import App



from lino.utils import mti


#~ from lino.modlib.contacts import MODULE_LABEL


PARTNER_NUMBERS_START_AT = 100 # used for generating demo data and tests


class AddressFormatter(object):
    """
    Format used in BE, DE, FR, NL...
    """
    def get_city_lines(me,self):
        if self.city is not None:
            s = join_words(self.zip_code or self.city.zip_code,self.city)
            if s:
                yield s 
            
class EstonianAddressFormatter(AddressFormatter):
    """
    Format used in Estonia.
    Not ready and not tested.
    """
    def get_city_lines(me,self):
        #lines = [self.name,street,self.addr1,self.addr2]
        if self.region: # 
            if self.city:
                join_words(self.zip_code or self.city.zip_code,self.city)
                if self.city_zip_code:
                    yield unicode(self.city)
                    yield unicode(self.city)
            s = join_words(self.zip_code,self.region)
        else: 
            s = join_words(self.zip_code,self.city)
        if s:
            yield s 
            

            
ADDRESS_FORMATTERS = dict()
ADDRESS_FORMATTERS[None] = AddressFormatter()
ADDRESS_FORMATTERS['EE'] = EstonianAddressFormatter()
            
def get_address_formatter(country):
    if country and country.isocode:
        af = ADDRESS_FORMATTERS.get(country.isocode,None)
        if af is not None: 
            return af
    return ADDRESS_FORMATTERS.get(None)
            
            
            




class CompanyType(dd.BabelNamed):
    """
    Represents a possible choice for the  `type`
    field of a :class:`Company`.
    """
    
    class Meta:
        verbose_name = _("company type")
        verbose_name_plural = _("company types")
        
    abbr = dd.BabelCharField(_("Abbreviation"),max_length=30,blank=True)
    
        
class CompanyTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = 'contacts.CompanyType'
    column_names = 'name *'
    #~ label = _("Company types")




#~ class Contact(mti.MultiTableBase,CountryCity):
class Partner(mti.MultiTableBase,CountryRegionCity,dd.Addressable):
    """
    
    A :class:`Partner` is anything that can act as a business partner.
    A Partner has at least a name and usually also one "official" address.
    Predefined subclasses of Partners are
    :class:`Person` for physical persons and
    :class:`Company` for companies, organisations and any kind of 
    non-formal Partners.
    
    
    Base class for anything that has contact information 
    (postal address, email, phone,...).
    
    """
    
    """
    preferred width for ForeignKey fields to a Partner
    """
    preferred_foreignkey_width = 20 
    
  
    class Meta:
        abstract = settings.SITE.is_abstract_model('contacts.Partner')
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
  
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
    
    #~ zip_code = models.CharField(_("Zip code"),
        #~ max_length=10,blank=True)
    #~ region = models.CharField(_("Region"),
        #~ max_length=200,blank=True)
    language = dd.LanguageField()
    
    email = models.EmailField(_('E-Mail'),blank=True) # ,null=True)
    url = models.URLField(_('URL'),blank=True)
    phone = models.CharField(_('Phone'),max_length=200,blank=True)
    gsm = models.CharField(_('GSM'),max_length=200,blank=True)
    fax = models.CharField(_('Fax'),max_length=200,blank=True)
    
    remarks = models.TextField(_("Remarks"),blank=True) # ,null=True)
    
    is_person = mti.EnableChild(
        "contacts.Person",
        verbose_name=_("is Person"),
        help_text=_("Whether this Partner is a Person."))
        
    is_company = mti.EnableChild(
        "contacts.Company",
        verbose_name=_("is Company"),
        help_text=_("Whether this Partner is a Company."))
        
    print_labels = dd.PrintLabelsAction()
        
    def on_create(self,ar):
        self.language = ar.get_user().language
        super(Partner,self).on_create(ar)
        
    def save(self,*args,**kw):
        if self.id is None:
            sc = settings.SITE.site_config # get_site_config()
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        #~ logger.info("20120327 Partner.save(%s,%s)",args,kw)
        super(Partner,self).save(*args,**kw)
        
    def __unicode__(self):
        return self.name
        
    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()
        
    def get_full_name(self,*args,**kw):
        """\
Returns a one-line string representing this Partner.
The default returns simply the `name` field, ignoring any parameters, 
but e.g. :class:`PersonMixin` overrides this.
        """
        #~ print '20120729 Partner.get_full_name`'
        
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
            yield join_words(
              self.street_prefix, self.street,
              self.street_no,self.street_box)
        if self.addr2:
            yield self.addr2
           
        af = get_address_formatter(self.country)
        for ln in af.get_city_lines(self):
            yield ln
            
        if self.country is not None:
            sc = settings.SITE.site_config # get_site_config()
            #~ print 20130228, sc.site_company_id
            if sc.site_company is None or self.country != sc.site_company.country: 
                # (if self.country != sender's country)
                yield unicode(self.country)
            
        #~ logger.debug('%s : as_address() -> %r',self,lines)
        
    def address_location(self,linesep="\n"):
        """
        The plain text postal address location part. 
        Lines are separated by `linesep`.
        """
        return linesep.join(self.address_location_lines())
        
    @dd.displayfield(_("Address"))
    def address_column(self,request):
        return self.address_location(', ')
    #~ address_column.return_type = dd.DisplayField(_("Address"))
    
    @dd.displayfield(_("Name"))
    def name_column(self,request):
        #~ return join_words(self.last_name.upper(),self.first_name)
        return unicode(self)
    
    def get_partner_instance(self):
        return self # compatibility with lino.modlib.partners

class PartnerDetail(dd.FormLayout):
  
    main = """
    address_box:60 contact_box:30
    bottom_box
    """
    
    address_box = dd.Panel("""
    name_box
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """,label = _("Address"))
    
    contact_box = dd.Panel("""
    info_box
    email:40 
    url
    phone
    gsm fax
    """,label = _("Contact"))

    bottom_box = """
    remarks 
    is_person is_company #is_user
    """
        
    name_box = "name"
    info_box = "id language"
    
    
    #~ def setup_handle(self,dh):
        #~ dh.address_box.label = _("Address")
        #~ dh.contact_box.label = _("Contact")
  
    
    
class Partners(dd.Table):
    required = dd.Required(user_level='user',user_groups='office')
    model = 'contacts.Partner'
    column_names = "name email * id" 
    order_by = ['name','id']
    #~ column_names = "name * id" 
    detail_layout = PartnerDetail()
    insert_layout = dd.FormLayout("""
    name
    language email
    """,window_size=(40,'auto'))
    
    @classmethod
    def get_queryset(self):
        return self.model.objects.select_related('country','city')


#~ class AllPartners(Partners):
  
    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return _("All %s") % self.model._meta.verbose_name_plural
        
class PartnersByCity(Partners):
    master_key = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 name language *"
    
class PartnersByCountry(Partners):
    master_key = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()



  
class PersonMixin(mixins.Human):
    """
    Can be used also for Persons that are no Partners
    """
    class Meta:
        abstract = True
        
    title = models.CharField(max_length=200,blank=True,
        verbose_name=_('Title'),
        help_text=_("Text to print before first_name as part of the first address line."))
    
        
  
class Person(PersonMixin,Partner):
    """
    Mixin for models that represent a physical person. 
    
    See :ref:`lino.tutorial.human`.

    """
    class Meta:
        #~ abstract = True
        abstract = settings.SITE.is_abstract_model('contacts.Person')
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        ordering = ['last_name','first_name']

    def address_person_lines(self,*args,**kw):
        "Deserves more documentation."
        if self.title:
            yield self.title
        yield self.get_full_name(*args,**kw)
        #~ l = filter(lambda x:x,[self.first_name,self.last_name])
        #~ yield  " ".join(l)
        
    def full_clean(self,*args,**kw):
    #~ def save(self,*args,**kw):
        """
        Set the `name` field of this person. 
        This field is visible in the Partner's detail but not 
        in the Person's detail and serves for sorting 
        when selecting a Partner. 
        It also serves for quick search on Persons.
        """
        self.name = join_words(self.last_name,self.first_name)
        super(Person,self).full_clean(*args,**kw)





class PersonDetail(PartnerDetail):
  
    #~ main = """
    #~ address_box contact_box
    #~ bottom_box contacts.RolesByPerson
    #~ """
    
    name_box = "last_name first_name:15 gender title:10"
    #~ info_box = "id:5 language:10 birth_date:10"
    info_box = "id:5 language:10"

    bottom_box = "remarks contacts.RolesByPerson"
        
    
    #~ def setup_handle(self,dh):
        #~ PartnerDetail.setup_handle(self,dh)
        #~ dh.address_box.label = _("Address")
        #~ dh.contact_box.label = _("Contact")
  


#~ class Persons(dd.Table):
class Persons(Partners):
    """
    List of all Persons.
    """
    #~ required = dict(user_level='user')
    model = "contacts.Person"
    order_by = ["last_name","first_name","id"]
    column_names = "name_column:20 address_column email phone:10 gsm:10 id language:10 *"
    detail_layout = PersonDetail()
    
    insert_layout = dd.FormLayout("""
    title first_name last_name
    gender language
    """,window_size=(60,'auto'))
    


#~ class CompanyMixin(dd.Model):
class Company(Partner):
    """
    Abstract base class for a company.
    See also :doc:`/tickets/14`.
    """
    class Meta:
        abstract = settings.SITE.is_abstract_model('contacts.Company')
        #~ abstract = True
        app_label = 'contacts'
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
    
    prefix = models.CharField(max_length=200,blank=True) 
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
        #~ print '20120729 Company.get_full_name`'
        if self.type:
            return join_words(self.type.abbr,self.name)
        return self.name
    full_name = property(get_full_name)
    
    #~ @classmethod
    #~ def site_setup(cls,lino):
        #~ raise Exception('20110810')

class CompanyDetail(PartnerDetail):
  
    bottom_box = """
    type vat_id:12
    remarks contacts.RolesByCompany
    """

    name_box = "prefix name"
    #~ name_box = """prefix name type:20"""
    #~ info_box = "id:5 language:10 vat_id:12"



class Companies(Partners):
    model = "contacts.Company"
    order_by = ["name"]
    detail_layout = CompanyDetail()
    insert_layout = dd.FormLayout("""
    name 
    language:20 email:40
    type id
    """,window_size=(60,'auto'))
    
#~ class List(Partner):
    #~ pass

#~ class Lists(Partners):
    #~ model = List
    #~ order_by = ["name"]
    #~ detail_layout = """
    #~ id name
    #~ language email
    #~ MembersByList
    #~ """
    #~ insert_layout = dd.FormLayout("""
    #~ name 
    #~ language email
    #~ """,window_size=(40,'auto'))



# class ContactType(dd.BabelNamed):
class RoleType(dd.BabelNamed):
    """
    TODO: rename "RoleType" to "Function" or "ContactType".
    
    RoleType,name is used at "in seiner Eigenschaft als ..." 
    in document templates for contracts.    
    """
    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")


class RoleTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = RoleType


#~ class Contact(dd.Model):
class Role(dd.Model,dd.Addressable):
    """
    
    A Contact (historical model name :class:`Role`) 
    is a :class:`Person` 
    that has a given  role (:class:`ContactType`) 
    in a given :class:`Company`. 
    
    TODO: rename "Role" to "Contact".
    """
  
    class Meta:
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")
        
    type = models.ForeignKey('contacts.RoleType',
      blank=True,null=True,
      verbose_name=_("Contact Role"))
    person = models.ForeignKey("contacts.Person",related_name='rolesbyperson')
    company = models.ForeignKey("contacts.Company",related_name='rolesbycompany')
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
        return u"%s (%s)" % (self.person, self.type)
            
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
    def address_person_lines(self):
        #~ yield self.name
        if self.company:
            for ln in self.company.address_person_lines():
                yield ln
        for ln in self.person.address_person_lines():
            yield ln
        
    def address_location_lines(self):
        if self.company:
            return self.company.address_location_lines()
        else:
            return self.person.address_location_lines()

#~ class ContactsByCompany(dd.Table):
    #~ model = 'contacts.RoleOccurence'
    #~ master_key = 'company'
    #~ column_names = 'person type *'

#~ class ContactsByPerson(dd.Table):
    #~ label = _("Contact for")
    #~ model = 'contacts.RoleOccurence'
    #~ master_key = 'person'
    #~ column_names = 'company type *'
    
class Roles(dd.Table):
    required = dd.required(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = 'contacts.Role'   
    
class RolesByCompany(Roles):
    required = dd.required()
    auto_fit_column_widths = True
    #~ required_user_level = None
    label = _("Contact persons")
    master_key = 'company'
    column_names = 'person type *'
    hidden_columns = 'id'

class RolesByPerson(Roles):
    required = dd.required()
    #~ required_user_level = None
    label = _("Contact for")
    master_key = 'person'
    column_names = 'company type *'
    auto_fit_column_widths = True
    hidden_columns = 'id'
    
    
    
class PartnerDocument(dd.Model):
    """
    Adds two fields 'partner' and 'person' to this model, 
    making it something that refers to a "partner". 
    `person` means a "contact person" for the partner.
    
    """
    
    class Meta:
        abstract = True
        
    company = models.ForeignKey("contacts.Company",
        blank=True,null=True)
        
    person = models.ForeignKey("contacts.Person",blank=True,null=True)
        
    def get_partner(self):
        if self.company is not None:
            return self.company
        return self.person
        
    def get_mailable_recipients(self):
        for p in self.company, self.person:
            if p is not None and p.email:
                #~ yield "%s <%s>" % (p, p.email)
                yield ('to', p)
                #~ yield ('to', unicode(p), p.email)
        
    def get_postable_recipients(self):
        for p in self.company, self.person:
            if p is not None:
                yield p
        
        
    def summary_row(self,ar,**kw):
        """
        A :meth:`lino.core.model.Model.summary_row` 
        method for partner documents.
        """
        href_to = ar.obj2html
        #~ href_to = ui.ext_renderer.href_to
        s = [href_to(self)]
        #~ if self.person and not dd.has_fk(rr,'person'):
        if self.person:
            if self.company:
                s += [" (", href_to(self.person), 
                    "/",href_to(self.company),")"]
            else:
                s += [" (",href_to(self.person), ")"]
        elif self.company:
            s += [" (", href_to(self.company),")"]
        return s
            
    def update_owned_instance(self,other):
        #~ print '20120627 PartnerDocument.update_owned_instance'
        if isinstance(other,mixins.ProjectRelated):
            if isinstance(self.person,Person):
                other.project = self.person
            elif isinstance(self.company,Person):
                other.project = self.company
        other.person = self.person
        other.company = self.company
        super(PartnerDocument,self).update_owned_instance(other)
        



class OldCompanyContact(dd.Model):
    """
    Abstract class which adds two fields `company` and `contact`.
    """
    class Meta:
        abstract = True
        
    company = models.ForeignKey("contacts.Company",
        related_name="%(app_label)s_%(class)s_set_by_company",
        verbose_name=_("Company"),
        blank=True,null=True)
        
    contact = models.ForeignKey("contacts.Role",
      related_name="%(app_label)s_%(class)s_set_by_contact",
      blank=True,null=True,
      verbose_name=_("represented by"))
      
    @chooser()
    def contact_choices(cls,company):
        if company is not None:
            return cls.contact_choices_queryset(company)
        return []
        
    @classmethod
    def contact_choices_queryset(cls,company):
        return Role.objects.filter(company=company)

    def full_clean(self,*args,**kw):
        if self.company:
            if self.contact is None \
              or self.contact.company is None \
              or self.contact.company.pk != self.company.pk:
                qs = self.contact_choices_queryset(self.company)
                #~ qs = self.company.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact = None
        super(CompanyContact,self).full_clean(*args,**kw)


class ContactRelated(dd.Model):
    """
    Abstract class for things that relate to a company represented by a person as a given role.
    
    .. local_fields:: lino.modlib.contacts.models.ContactRelated
    
        Adds 3 fields `company`, `contact_person` and `contact_role`.
        
    """
    
    class Meta:
        abstract = True
        
    company = models.ForeignKey("contacts.Company",
        related_name="%(app_label)s_%(class)s_set_by_company",
        verbose_name=_("Company"),
        blank=True,null=True)
        
    contact_person = models.ForeignKey("contacts.Person",
      related_name="%(app_label)s_%(class)s_set_by_contact_person",
      blank=True,null=True,
      verbose_name=_("represented by"))
      
    contact_role = models.ForeignKey("contacts.RoleType",
      related_name="%(app_label)s_%(class)s_set_by_contact_role",
      blank=True,null=True,
      verbose_name=_("represented as"))
      
    @chooser()
    def contact_person_choices(cls,company):
        """
        chooser method for the `contact_person` field.
        """
        if company is not None:
            return cls.contact_person_choices_queryset(company)
        return settings.SITE.modules.contacts.Person.objects.order_by('last_name','first_name')
        
        
    def get_contact(self):
        if self.contact_person is not None:
            if self.company is not None:
                roles = Role.objects.filter(company=self.company,person=self.contact_person)
                #~ print '20120929 get_contact', roles
                if roles.count() == 1:
                    return roles[0]
        
    def get_recipient(self):
        contact = self.get_contact()
        if contact is not None: 
            return contact
        if self.contact_person is not None:
            if self.company is not None:
                return Role(company=self.company,person=self.contact_person)
            return self.contact_person
        return self.company
        
    recipient = property(get_recipient)
    
    def get_partner(self):
        return self.company or self.contact_person
    partner = property(get_partner)
    """(read-only property) 
    The "legal partner", 
    i.e. usually the :class:`Company` instance pointed to by 
    the `company` field,
    except when that field is empty, in which case `partner` 
    contains the :class:`Person` pointed to by the 
    `contact_person` field.
    If both fields are empty, then `partner` contains `None`.
    """

    def contact_person_changed(self,ar):
        #~ print '20120929 contact_person_changed'
        if self.company and not self.contact_person_id:
            roles = Role.objects.filter(company=self.company)
            if roles.count() == 1:
                self.contact_person = roles[0].person
                self.contact_role = roles[0].type
            return 
      
    @classmethod
    def contact_person_choices_queryset(cls,company):
        """
        Return a queryset of candidate Person objects allowed 
        in `contact_person` for a given `company`.
        """
        return settings.SITE.modules.contacts.Person.objects.filter(rolesbyperson__company=company).distinct()

    def full_clean(self,*args,**kw):
        if not settings.SITE.loading_from_dump:
            if self.company is not None and self.contact_person is None:
                qs = self.contact_person_choices_queryset(self.company)
                #~ qs = self.company.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact_person = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact_person = None
            contact = self.get_contact()
            if contact is not None:
                self.contact_role = contact.type
                #~ print '20120929b', contact.type
        super(ContactRelated,self).full_clean(*args,**kw)


    


#~ if settings.SITE.is_installed('contacts'):
  
    #~ """
    #~ Don't inject fields if contacts is just being imported from some other module.
    #~ """
    
#~ dd.inject_field(settings.SITE.user_model,
    #~ 'partner',
    #~ models.ForeignKey(Partner,
        #~ blank=True,null=True,
        #~ verbose_name=_("Partner")))



#~ if settings.SITE.is_installed('contacts'):
  
    #~ from lino.models import SiteConfig


dd.inject_field('system.SiteConfig',
    'next_partner_id',
    models.IntegerField(default=PARTNER_NUMBERS_START_AT, #
        verbose_name=_("Next partner id"),
        help_text=_("The next automatic id for any new partner.")))
    
dd.inject_field('system.SiteConfig',
    'site_company',
    models.ForeignKey("contacts.Company",
        blank=True,null=True,
        verbose_name=_("The company that runs this site"),
        related_name='site_company_sites',
        help_text=_("The Company to be used as sender in documents.")))
    

#~ dd.inject_field(Partner,
    #~ 'is_person',
    #~ mti.EnableChild(
        #~ settings.SITE.person_model,
        #~ verbose_name=_("is Person"),
        #~ help_text=_("Whether this Partner is a Person.")))
#~ dd.inject_field(Partner,
    #~ 'is_company',
    #~ mti.EnableChild(
        #~ "contacts.Company",
        #~ verbose_name=_("is Company"),
        #~ help_text=_("Whether this Partner is a Company.")))



def site_setup(site):

    site.modules.countries.Cities.set_detail_layout("""
    name country 
    type parent zip_code id 
    CitiesByCity
    contacts.PartnersByCity
    """)
    
@dd.receiver(dd.pre_analyze)
def company_model_alias(sender,**kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisation = sender.modules.contacts.Company  

@dd.receiver(dd.post_analyze)
def company_tables_alias(sender,**kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisations = sender.modules.contacts.Companies


def setup_main_menu(site,ui,profile,m):
    m = m.add_menu("contacts",App.verbose_name)
    #~ actors = (Persons,Companies,Partners)
    #~ for m in (Person,Company,Partner):
        #~ if m._meta.abstract: 
            #~ return 
    """
    We use the string representations and not the classes because 
    other installed applications may want to override these tables.
    """
    #~ for a in (Persons,Companies,Partners):
    for a in ('contacts.Persons','contacts.Companies','contacts.Partners'):
        m.add_action(a)

def setup_master_menu(site,ui,profile,m): 
    pass
    
def setup_config_menu(site,ui,profile,m):
    config_contacts = m.add_menu("contacts",App.verbose_name)
    config_contacts.add_action(CompanyTypes)
    config_contacts.add_action(RoleTypes)
    #~ config_contacts.add_action(site.modules.countries.Countries)
    #~ config_contacts.add_action(site.modules.countries.Cities)
    #~ config_contacts.add_action(site.modules.countries.Languages)
            
    #~ m  = m.add_menu("contacts",_("~Contacts"))
    #~ m.add_action('contacts.RoleTypes')
  
def setup_explorer_menu(site,ui,profile,m):
    m = m.add_menu("contacts",App.verbose_name)
    m.add_action(site.modules.contacts.Roles)
    #~ m.add_action(site.modules.countries.Cities)
  
#~ def setup_quicklinks(site,ui,user,m):
    #~ m.add_action(Person.detail_action)
        
  
def PartnerField(**kw):
    return models.ForeignKey(Partner,**kw)
    
