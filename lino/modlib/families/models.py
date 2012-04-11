# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
#~ from django.utils.translation import ugettext

from django import forms
from django.utils import translation


import lino

from lino import dd

from lino import mixins
from lino.utils import join_words
from lino.utils.choosers import chooser
from lino.utils import babel
from lino.models import get_site_config

from lino.utils import mti
from lino.modlib.contacts import models as contacts



class Family(contacts.Partner):
    """
    """
    class Meta:
        verbose_name = _("Family")
        verbose_name_plural = _("Families")
    
    dummy = models.CharField(max_length=1,blank=True) 
    # workaround for https://code.djangoproject.com/ticket/13864
        
    #~ def get_full_name(self,**salutation_options):
    def get_full_name(self,salutation=True,**salutation_options):
        """Deserves more documentation."""
        return join_words(_("Family"),self.name)
    full_name = property(get_full_name)
    
    def __unicode__(self):
        return unicode(join_words(_("Family"),self.name))
        #~ return self.name


class FamilyDetail(dd.DetailLayout):
  
    box3 = """
    country region
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    """

    box4 = """
    email:40 
    url
    phone
    gsm
    """

    address_box = "box3 box4"

    bottom_box = "remarks MembersByFamily"

    intro_box = """
    name id language 
    """

    main = """
    intro_box
    address_box
    bottom_box
    """
    


              
class Families(contacts.Partners):
    model = Family
    order_by = ["name"]
    detail_layout = FamilyDetail()
    
    
    



# class ContactType(babel.BabelNamed):
class Role(babel.BabelNamed):
    """
    Deserves more documentation.
    """
    class Meta:
        verbose_name = _("Family Role")
        verbose_name_plural = _("Family Roles")


class Roles(dd.Table):
    model = Role


class Member(models.Model):
    """
    The role of a given :class:`Person` in a given :class:`Family`.
    """
  
    class Meta:
        verbose_name = _("Family Member")
        verbose_name_plural = _("Family Members")
        
    role = models.ForeignKey(Role,
      blank=True,null=True,
      )
    #~ partner = models.ForeignKey(contacts.Partner,
        #~ related_name='membersbypartner')
    family = models.ForeignKey(Family,
        related_name='membersbyfamily')
    person = models.ForeignKey(settings.LINO.person_model,
        related_name='membersbyperson')
    #~ type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))

    def __unicode__(self):
        if self.person_id is None:
            return super(Member,self).__unicode__()
        if self.type is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.type)

    def address_lines(self):
        for ln in self.person.address_person_lines():
            yield ln
        if self.family:
            for ln in self.family.address_person_lines():
                yield ln
            for ln in self.family.address_location_lines():
                yield ln
        else:
            for ln in self.address_location_lines():
                yield ln

class Members(dd.Table):
    model = Member
    
class MembersByFamily(Members):
    label = _("Family Members")
    master_key = 'family'
    column_names = 'person role *'

class MembersByPerson(Members):
    label = _("Member of")
    master_key = 'person'
    column_names = 'family role *'
    
    
    

if settings.LINO.is_installed('family'):
    #~ Don't inject fields if contacts is just being imported from some other module.
  
    from lino.models import SiteConfig

    dd.inject_field(contacts.Partner,
        'is_family',
        #~ mti.EnableChild('contacts.Person',verbose_name=_("is Person")),
        mti.EnableChild(Family,verbose_name=_("is Family")),
        """Whether this Partner is a Family."""
        )




def setup_main_menu(site,ui,user,m): pass
    
def setup_master_menu(site,ui,user,m): 
    m.add_action(Families)

def setup_my_menu(site,ui,user,m): 
    pass
    
def setup_config_menu(site,ui,user,m): 
    m = m.add_menu("families",_("Families"))
    m.add_action(Roles)
  
def setup_explorer_menu(site,ui,user,m):
    m = m.add_menu("families",_("Families"))
    m.add_action(Members)
  