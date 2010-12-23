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
from lino.utils.babel import add_babel_field, default_language, babelattr
from lino.mixins.addressable import Addressable, Addressables

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
        
    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        return u'%s %s' % (self.first_name, self.last_name)
    
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
    order_by = "last_name first_name id".split()
    #can_view = perms.is_authenticated

class PersonsByCountry(Persons):
    fk_name = 'country'
    order_by = 'city street street_no street_box addr2'.split()
    column_names = "city street street_no street_box addr2 name language"
    

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
        #~ return self.name
        return babelattr(self,'name')
        
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
    
    vat_id = models.CharField(_("VAT id"),max_length=200,blank=True)
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
    name = models.CharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        #~ return self.name
        return babelattr(self,'name')

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
    
        