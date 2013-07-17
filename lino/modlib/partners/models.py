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
This module defines the tables 
- :class:`Partner` (and their specializations :class:`Person` and :class:`Organisation`)
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

#~ from lino.modlib.partners.utils import Genders

#~ from lino.modlib.countries.models import CountryCity
from lino.modlib.countries.models import CountryRegionCity

#~ from lino.modlib.partners.utils import get_salutation
#~ from lino.modlib.partners.utils import GENDER_CHOICES, get_salutation


from lino.utils import mti

from lino.modlib.partners import MODULE_LABEL

if False:

    class PartnerType(dd.Choice):
        
        def __init__(self,cls,value,model_spec,name=None):
            #~ self.model_spec = model_spec
            super(PartnerType,self).__init__(value,model_spec,name)
            def f(model):
                self.model = model
                self.text = model._meta.verbose_name
            dd.do_when_prepared(f,model_spec)
            
            
    class PartnerTypes(dd.ChoiceList):

        @classmethod
        def add_item(cls,value,model,name=None,**kw):
            return cls.add_item_instance(PartnerType(cls,value,model,name,**kw))
            
    PartnerTypes.add_item('P','partners.Person','person')        
    PartnerTypes.add_item('O','partners.Organisation','organisation')


class OrganisationType(dd.BabelNamed):
    """
    Represents a possible choice for the  `type`
    field of an :class:`Organisation`.
    """
    
    class Meta:
        verbose_name = _("Organisation type")
        verbose_name_plural = _("Organisation types")
        
    abbr = dd.BabelCharField(_("Abbreviation"),max_length=30,blank=True)
    
        
class OrganisationTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = 'partners.OrganisationType'
    column_names = 'name *'
    #~ label = _("Organisation types")


class Addressable(CountryRegionCity):
    class Meta:
        abstract = True
        
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
    
    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()
        
    def get_full_name(self,*args,**kw):
        """
        Returns a one-line string representing this Partner.
        The default returns simply the `name` field, ignoring any parameters, 
        but e.g. :class:`PersonMixin` overrides this.
        """
        raise NotImplementedError()
        #~ return self.name
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
            sc = settings.SITE.site_config # get_site_config()
            if not sc.site_partner or self.country != sc.site_partner.country: 
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
        
    @dd.displayfield(_("Address"))
    def address_column(self,request):
        return self.address_location(', ')
    #~ address_column.return_type = dd.DisplayField(_("Address"))
    
    @dd.displayfield(_("Name"))
    def name_column(self,request):
        #~ return join_words(self.last_name.upper(),self.first_name)
        return unicode(self)
    
        

#~ class Contact(mti.MultiTableBase,CountryCity):
class Partner(dd.Model):
    """
    
    A :class:`Partner` is anything that can act as a business partner.
    A Partner has at least a name and usually also one "official" address.
    Predefined subclasses of Partners are
    :class:`Person` for physical persons and
    :class:`Organisation` for companies, organisations and any kind of 
    non-formal Partners.
    
    
    Base class for anything that has contact information 
    (postal address, email, phone,...).
    
    """
    
    """
    preferred width for ForeignKey fields to a Partner
    """
    preferred_foreignkey_width = 20 
    
  
    class Meta:
        abstract = settings.SITE.is_abstract_model('partners.Partner')
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
  
    name = models.CharField(max_length=200,verbose_name=_('Name'))
    
    #~ type = PartnerTypes.field(blank=True)
    
    def save(self,*args,**kw):
        if self.id is None:
            sc = settings.SITE.site_config # get_site_config()
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        #~ logger.info("20120327 Partner.save(%s,%s)",args,kw)
        super(Partner,self).save(*args,**kw)
        
    #~ def typed_partner(self):
        #~ if self.organisation:
            #~ return self.organisation
        #~ return self.person
            
        
    def __unicode__(self):
        return self.name






class Partners(dd.Table):
    required = dd.required(user_level='user')
    model = 'partners.Partner'
    order_by = ['name','id']
    #~ column_names = "name * id" 
    #~ detail_layout = PartnerDetail()
    detail_layout = """
    id name
    organisation person
    """
    insert_layout = dd.FormLayout("""
    name
    organisation person
    """,window_size=(40,'auto'))
    



#~ class PartnerDetail(dd.FormLayout):
class AddressableDetail(dd.FormLayout):
  
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
    """
        
    name_box = "name"
    info_box = "id language"
    
    
    #~ def setup_handle(self,dh):
        #~ dh.address_box.label = _("Address")
        #~ dh.contact_box.label = _("Contact")
  
    
    
class Addressables(dd.Table):
    required = dd.required(user_level='user')
    column_names = "name email * id" 
    
    @classmethod
    def get_queryset(self):
        return self.model.objects.select_related('country','city')


#~ class AllPartners(Partners):
  
    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return _("All %s") % self.model._meta.verbose_name_plural
        

class ConcretePartner(dd.Model):
    class Meta:
        abstract = True
    
    def get_partner_name(self):
        raise NotImplementedError()
        
    def get_typed_instance(self,model):
        if model is self.__class__: return self
        return self.partner
        #~ if model is Person: return self.
        
    #~ def get_partner_instance(self):
        #~ if self.partner_id is None:
            #~ return None
        #~ return self.partner
        
    def save(self,*args,**kw):
        if self.partner_id is None:
            assert self.id is None
            p = Partner()
            p.save()
            self.id = p.id
            self.partner = p
            f = self._meta.get_field('partner')
            setattr(p,self.__class__.__name__.lower(),self)
        self.partner.name = self.get_partner_name()
        self.partner.save()
        super(ConcretePartner,self).save(*args,**kw)
        

class PersonMixin(mixins.Human):
    """
    Can be used also for Persons that are no Partners
    """
    class Meta:
        abstract = True
        
    title = models.CharField(max_length=200,blank=True,
      verbose_name=_('Title'))
    """Text to print as part of the first address line in front of first_name."""
        
  
class Person(ConcretePartner,Addressable,PersonMixin):
    """
    Mixin for models that represent a physical person. 
    """
    
    class Meta:
        #~ abstract = True
        abstract = settings.SITE.is_abstract_model('partners.Person')
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        
    #~ partner = models.OneToOneField(Partner,blank=True,related_name="person")
    partner = models.OneToOneField(Partner,blank=True)

    def address_person_lines(self,*args,**kw):
        "Deserves more documentation."
        if self.title:
            yield self.title
        yield self.get_full_name(*args,**kw)
        #~ l = filter(lambda x:x,[self.first_name,self.last_name])
        #~ yield  " ".join(l)
        
            
    def get_partner_name(self):
        return join_words(self.last_name,self.first_name)

    def get_full_name(self,*args,**kw):
        """
        Returns a one-line string representing this Partner.
        The default returns simply the `name` field, ignoring any parameters, 
        but e.g. :class:`PersonMixin` overrides this.
        """
        return self.get_partner_name()
        
    full_name = property(get_full_name)




class PersonDetail(AddressableDetail):
  
    #~ main = """
    #~ address_box contact_box
    #~ bottom_box partners.RolesByPerson
    #~ """
    
    name_box = "last_name first_name:15 gender title:10"
    #~ info_box = "id:5 language:10 birth_date:10"
    info_box = "id:5 language:10"

    bottom_box = "remarks partners.ContactsByPerson"
        
    
    #~ def setup_handle(self,dh):
        #~ PartnerDetail.setup_handle(self,dh)
        #~ dh.address_box.label = _("Address")
        #~ dh.contact_box.label = _("Contact")
  


#~ class Persons(dd.Table):
class Persons(Addressables):
    """
    List of all Persons.
    """
    #~ required = dict(user_level='user')
    model = "partners.Person"
    order_by = ["last_name","first_name","id"]
    column_names = "name_column:20 address_column email phone:10 gsm:10 id language:10 *"
    detail_layout = PersonDetail()
    
    insert_layout = dd.FormLayout("""
    title first_name last_name
    gender language
    """,window_size=(60,'auto'))
    


class Organisation(ConcretePartner,Addressable):
    """
    Abstract base class for a Organisation.
    See also :doc:`/tickets/14`.
    """
    class Meta:
        abstract = settings.SITE.is_abstract_model('partners.Organisation')
        #~ abstract = True
        #~ app_label = 'partners'
        verbose_name = _("Organisation")
        verbose_name_plural = _("Organisations")
        
    partner = models.OneToOneField(Partner,blank=True)
    #~ partner = models.OneToOneField(Partner,blank=True,related_name="organisation")
    
    name = models.CharField(max_length=200,verbose_name=_('Name'))

    
    prefix = models.CharField(max_length=200,blank=True)
    vat_id = models.CharField(_("VAT id"),max_length=200,blank=True)
    """The national VAT identification number.
    """
    
    type = models.ForeignKey('partners.OrganisationType',blank=True,null=True,
      verbose_name=_("Organisation type"))
    """Pointer to this organisation's :class:`OrganisationType`. 
    """
    
    def get_partner_name(self):
        return self.name
    
    #~ def get_full_name(self,**salutation_options):
    def get_full_name(self,salutation=True,**salutation_options):
        """Deserves more documentation."""
        #~ print '20120729 Organisation.get_full_name`'
        if self.type:
            return join_words(self.type.abbr,self.name)
        return self.name
    full_name = property(get_full_name)
    
    #~ @classmethod
    #~ def site_setup(cls,lino):
        #~ raise Exception('20110810')


class OrganisationDetail(AddressableDetail):
  
    bottom_box = """
    type vat_id:12
    remarks partners.ContactsByOrganisation
    """

    #~ name_box = """prefix name type:20"""
    #~ info_box = "id:5 language:10 vat_id:12"



class Organisations(Addressables):
    model = "partners.Organisation"
    order_by = ["name"]
    detail_layout = OrganisationDetail()
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




class PersonsByCity(Persons):
    master_key = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 last_name first_name language *"
    
class PersonsByCountry(Persons):
    master_key = 'country'
    column_names = "city street street_no last_name first_name language *"
    order_by = "city street street_no".split()


class OrganisationsByCity(Organisations):
    master_key = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 name language *"
    
class OrganisationsByCountry(Organisations):
    master_key = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()




class Role(dd.BabelNamed):
    """
    
    Role.name is used at "in seiner Eigenschaft als ..." 
    in document templates for contracts.    
    """
    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


class Roles(dd.Table):
    required = dd.required(user_level='manager')
    model = Role


class Contact(dd.Model):
    """
    
    A Contact is a :class:`Person` 
    that has a given (:class:`Role`) 
    in a given :class:`Organisation`. 
    
    TODO: rename "Role" to "Contact".
    """
  
    class Meta:
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")
        
    role = models.ForeignKey('partners.Contact',blank=True,null=True)
    person = models.ForeignKey("partners.Person",related_name='contactsbyperson')
    organisation = models.ForeignKey("partners.Organisation",related_name='contactsbyorganisation')
    #~ type = models.ForeignKey('partners.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))

    #~ def __unicode__(self):
        #~ if self.person_id is None:
            #~ return super(Contact,self).__unicode__()
        #~ if self.type is None:
            #~ return unicode(self.person)
        #~ return u"%s (%s)" % (self.person, self.type)
    def __unicode__(self):
        if self.person_id is None:
            return super(Contact,self).__unicode__()
        if self.role is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.role)
            
    def address_lines(self):
        for ln in self.person.address_person_lines():
            yield ln
        if self.organisation:
            for ln in self.organisation.address_person_lines():
                yield ln
            for ln in self.organisation.address_location_lines():
                yield ln
        else:
            for ln in self.person.address_location_lines():
                yield ln

    
class Contacts(dd.Table):
    required = dd.required(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = 'partners.Contact'
    
class ContactsByOrganisation(Contacts):
    required = dd.required()
    auto_fit_column_widths = True
    #~ required_user_level = None
    label = _("Contact persons")
    master_key = 'organisation'
    column_names = 'person role *'
    hidden_columns = 'id'

class ContactsByPerson(Contacts):
    required = dd.required()
    #~ required_user_level = None
    label = _("Contact for")
    master_key = 'person'
    column_names = 'organisation role *'
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
        
    organisation = models.ForeignKey("partners.Organisation",
        blank=True,null=True)
        
    person = models.ForeignKey("partners.Person",blank=True,null=True)
        
    def get_partner(self):
        if self.organisation is not None:
            return self.organisation
        return self.person
        
    def get_mailable_recipients(self):
        for p in self.organisation, self.person:
            if p is not None and p.email:
                #~ yield "%s <%s>" % (p, p.email)
                yield ('to', p)
                #~ yield ('to', unicode(p), p.email)
        
    def get_postable_recipients(self):
        for p in self.organisation, self.person:
            if p is not None:
                yield p
        
        
    #~ def summary_row(self,ui,rr,**kw):
        #~ if self.person:
            #~ if self.organisation:
                #~ # s += ": " + ui.href_to(self.person) + " / " + ui.href_to(self.organisation)
                #~ return ui.href_to(self.organisation) + ' ' + ugettext("attn:") + ' ' + ui.href_to(self.person)
            #~ else:
                #~ return ui.href_to(self.person)
        #~ elif self.organisation:
            #~ return ui.href_to(self.organisation)
            
    #~ def summary_row(self,ui,rr,**kw):
    def summary_row(self,ar,**kw):
        """
        A :meth:`lino.code.model.Model.summary_row` method for PartnerDocument.
        """
        href_to = ar.href_to
        #~ href_to = ui.ext_renderer.href_to
        s = href_to(self)
        #~ if self.person and not dd.has_fk(rr,'person'):
        if self.person:
            if self.organisation:
                s += " (" + href_to(self.person) \
                    + "/" + href_to(self.organisation) + ")"
            else:
                s += " (" + href_to(self.person) + ")"
        elif self.organisation:
            s += " (" + href_to(self.organisation) + ")"
        return s
            
    def update_owned_instance(self,other):
        #~ print '20120627 PartnerDocument.update_owned_instance'
        if isinstance(other,mixins.ProjectRelated):
            if isinstance(self.person,Person):
                other.project = self.person
            elif isinstance(self.organisation,Person):
                other.project = self.organisation
        other.person = self.person
        other.organisation = self.organisation
        super(PartnerDocument,self).update_owned_instance(other)
        



class OldOrganisationContact(dd.Model):
    """
    Abstract class which adds two fields `organisation` and `contact`.
    """
    class Meta:
        abstract = True
        
    organisation = models.ForeignKey("partners.Organisation",
        related_name="%(app_label)s_%(class)s_set_by_organisation",
        verbose_name=_("Organisation"),
        blank=True,null=True)
        
    contact = models.ForeignKey("partners.Role",
      related_name="%(app_label)s_%(class)s_set_by_contact",
      blank=True,null=True,
      verbose_name=_("represented by"))
      
    @chooser()
    def contact_choices(cls,organisation):
        if organisation is not None:
            return cls.contact_choices_queryset(organisation)
        return []
        
    @classmethod
    def contact_choices_queryset(cls,organisation):
        return Role.objects.filter(organisation=organisation)

    def full_clean(self,*args,**kw):
        if self.organisation:
            if self.contact is None \
              or self.contact.organisation is None \
              or self.contact.organisation.pk != self.organisation.pk:
                qs = self.contact_choices_queryset(self.organisation)
                #~ qs = self.organisation.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact = None
        super(OrganisationContact,self).full_clean(*args,**kw)


#~ class ContactRelated(dd.Model):
class PartnerRelated(dd.Model):
    """
    Abstract class for things that relate to a organisation represented by a person as a given role.
    Adds 3 fields `organisation`, `contact_person` and `contact_role`.
    """
    class Meta:
        abstract = True
        
    organisation = models.ForeignKey("partners.Organisation",
        related_name="%(app_label)s_%(class)s_set_by_organisation",
        verbose_name=_("Organisation"),
        blank=True,null=True)
        
    contact_person = models.ForeignKey("partners.Person",
      related_name="%(app_label)s_%(class)s_set_by_contact_person",
      blank=True,null=True,
      verbose_name=_("represented by"))
      
    contact_role = models.ForeignKey("partners.RoleType",
      related_name="%(app_label)s_%(class)s_set_by_contact_role",
      blank=True,null=True,
      verbose_name=_("represented as"))
      
    @chooser()
    def contact_person_choices(cls,organisation):
        if organisation is not None:
            return cls.contact_person_choices_queryset(organisation)
        return []
        
    def get_contact(self):
        roles = Role.objects.filter(organisation=self.organisation,person=self.contact_person)
        #~ print '20120929 get_contact', roles
        if roles.count() == 1:
            return roles[0]
        
    def contact_person_changed(self,ar):
        #~ print '20120929 contact_person_changed'
        if self.organisation and not self.contact_person_id:
            roles = Role.objects.filter(organisation=self.organisation)
            if roles.count() == 1:
                self.contact_person = roles[0].person
                self.contact_role = roles[0].type
            return 
      
    @classmethod
    def contact_person_choices_queryset(cls,organisation):
    #~ def contact_choices_queryset(cls,organisation):
        return Person.objects.filter(contactsbyperson__organisation=organisation).distinct()

    def full_clean(self,*args,**kw):
        if not settings.SITE.loading_from_dump:
            if self.organisation and self.contact_person is None:
                qs = self.contact_person_choices_queryset(self.organisation)
                #~ qs = self.organisation.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact_person = qs[0]
                else:
                    #~ print "20120227 clear contact!"
                    self.contact = None
            contact = self.get_contact()
            if contact is not None:
                self.contact_role = contact.type
                #~ print '20120929b', contact.type
        super(ContactRelated,self).full_clean(*args,**kw)


    


if settings.SITE.is_installed('partners'):
  
    dd.inject_field('system.SiteConfig',
        'next_partner_id',
        models.IntegerField(default=100, # first 100 for users from demo fixtures.
            verbose_name=_("The next automatic id for Person or Organisation")
        ),"""The next automatic id for Person or Organisation. 
        Deserves more documentation.
        """)
        
    dd.inject_field('system.SiteConfig',
        'site_partner',
        models.ForeignKey("partners.Organisation",
            blank=True,null=True,
            verbose_name=_("The partner that runs this site"),
            related_name='site_partner_sites',
            help_text=_("The partner to be used as sender in documents.")))



def site_setup(site):
    site.modules.countries.Cities.set_detail_layout("""
    name country 
    type parent zip_code id 
    CitiesByCity
    partners.PersonsByCity partners.OrganisationsByCity
    """)
    


def setup_main_menu(site,ui,profile,m):
    m = m.add_menu("partners",MODULE_LABEL)
    #~ actors = (Persons,Companies,Partners)
    #~ for m in (Person,Organisation,Partner):
        #~ if m._meta.abstract: 
            #~ return 
    """
    We use the string representations and not the classes because 
    other installed applications may want to override these tables.
    """
    #~ for a in (Persons,Companies,Partners):
    for a in ('partners.Persons','partners.Organisations','partners.Partners'):
        m.add_action(a)

def setup_my_menu(site,ui,profile,m): 
    pass
  
def setup_master_menu(site,ui,profile,m): 
    pass
    
def setup_config_menu(site,ui,profile,m): 
    config_partners = m.add_menu("partners",MODULE_LABEL)
    config_partners.add_action(OrganisationTypes)
    config_partners.add_action(Roles)
    #~ config_partners.add_action(site.modules.countries.Countries)
    #~ config_partners.add_action(site.modules.countries.Cities)
    #~ config_partners.add_action(site.modules.countries.Languages)
            
    #~ m  = m.add_menu("partners",_("~Contacts"))
    #~ m.add_action('partners.RoleTypes')
  
def setup_explorer_menu(site,ui,profile,m):
    m = m.add_menu("partners",MODULE_LABEL)
    m.add_action(site.modules.partners.Contacts)
    #~ m.add_action(site.modules.countries.Cities)
  
#~ def setup_quicklinks(site,ui,user,m):
    #~ m.add_action(Person.detail_action)
        
  
  
def PartnerField(**kw):
    #~ return dd.FieldsGroup(
        #~ partner_type=PartnerTypes.field(),
        #~ partner=models.ForeignKey(ConcretePartner,**kw))
    return models.ForeignKey(Partner,**kw)
    
