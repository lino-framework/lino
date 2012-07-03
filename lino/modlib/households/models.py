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
from django.utils.translation import string_concat
#~ from django.utils.translation import ugettext

from django import forms
from django.utils import translation


import lino

from lino import dd

from lino import mixins
from lino.utils import join_words
from lino.utils.choosers import chooser
from lino.utils.choicelists import Gender
from lino.utils import babel

from lino.utils import mti
from lino.modlib.contacts import models as contacts
from lino.apps.pcsw import models as pcsw

class Type(babel.BabelNamed):
    """
    Type of a household.
    http://www.belgium.be/fr/famille/couple/cohabitation/
    """
    class Meta:
        verbose_name = _("Household Type")
        verbose_name_plural = _("Household Types")

class Types(dd.Table):
    model = Type
    detail_template = """
    name 
    HouseholdsByType
    """


#~ pcsw = dd.resolve_app('pcsw')
#~ Partner = dd.resolve_model('contacts.Partner')
class Household(pcsw.CpasPartner,contacts.Partner):
    """
    A Household is a Partner that represents several Persons living together.
    list of :class:`members <Member>`.
    """
    class Meta:
        verbose_name = _("Household")
        verbose_name_plural = _("Households")
    
    prefix = models.CharField(max_length=200,blank=True) 
    type = models.ForeignKey(Type,blank=True,null=True)
    #~ father = models.ForeignKey(settings.LINO.person_model,
        #~ related_name='father_for',blank=True,null=True,
        #~ verbose_name=_("Father"))
    #~ mother = models.ForeignKey(settings.LINO.person_model,
        #~ related_name='mother_for',blank=True,null=True,
        #~ verbose_name=_("Mother"))
        
    #~ dummy = models.CharField(max_length=1,blank=True) 
    # workaround for https://code.djangoproject.com/ticket/13864
        
    def full_clean(self,*args,**kw):
        if not self.name or self.name == '-':
            l = []
            for m in self.member_set.all():
                if m.role.name_giving:
                    l.append(m.person.last_name)
            #~ if self.father:
                #~ l.append(self.father.last_name)
            #~ if self.mother:
                #~ l.append(self.mother.last_name)
            if len(l):
                self.name = '-'.join(l)
            else:
                self.name = "-"
        super(Household,self).full_clean(*args,**kw)
        
    #~ @chooser()
    #~ def father_choices(cls):
        # Person = dd.resolve_model('contacts.Person')
        #~ Person = settings.LINO.person_model
        #~ return Person.objects.filter(gender=Gender.male)
        
    #~ @chooser()
    #~ def mother_choices(cls):
        # Person = dd.resolve_model('contacts.Person')
        #~ Person = settings.LINO.person_model
        #~ return Person.objects.filter(gender=Gender.female)
        
        
        
    #~ def get_full_name(self,**salutation_options):
    def get_full_name(self,salutation=True,**salutation_options):
        """Deserves more documentation."""
        #~ if self.prefix:
        return join_words(self.prefix,self.name)
        #~ return join_words(_("Household"),self.name)
    full_name = property(get_full_name)
    
    def __unicode__(self):
        return unicode(self.get_full_name())
        #~ return self.name


class HouseholdDetail(dd.FormLayout):
  
    box3 = """
    country region
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    activity bank_account1:12 bank_account2:12
    """

    box4 = """
    email:40 
    url
    phone
    gsm
    """

    address_box = "box3 box4"

    bottom_box = "remarks MembersByHousehold"

    intro_box = """
    type name language:10 id 
    """

    main = """
    intro_box
    address_box
    bottom_box
    """
    


              
class Households(pcsw.Partners):
    model = Household
    order_by = ["name"]
    detail_layout = HouseholdDetail()
    
    @classmethod
    def do_setup(self):
        super(Households,self).do_setup()
        self.imported_fields = dd.fields_list(self.model,
          '''name remarks region zip_code city country 
          street_prefix street street_no street_box 
          addr2
          language 
          phone fax email url
          is_person is_company
          bank_account1 bank_account2 activity 
          is_active newcomer is_deprecated 
          ''')
    
    
class HouseholdsByType(Households):
    #~ label = _("Households")
    master_key = 'type'
    #~ column_names = 'person role *'

    
    



class Role(babel.BabelNamed):
    """
    The role of a :class:`Member` in a :class:`Household`.
    """
    class Meta:
        verbose_name = _("Household Role")
        verbose_name_plural = _("Household Roles")

    name_giving = models.BooleanField(_("name-giving"),
      default=False,
      help_text="""\
When the `name` field of a Household is empty, 
its value is computed by joining the `Last Name` 
of all name-giving members with a dash ("-").
      """)
      
    #~ header = babel.BabelCharField(_("Header"),
        #~ max_length=50,blank=True,
        #~ help_text="""\
#~ Default header when a member with this Role is being automatically 
#~ inserted as Actor of a Budget.
    #~ """)
    #~ male = dd.BabelCharField(max_length=200,
        #~ verbose_name=string_concat(_("Designation"),' ',Gender.male.text))
    #~ female = dd.BabelCharField(max_length=200,
        #~ verbose_name=string_concat(_("Designation"),' ',Gender.female.text))
    

class Roles(dd.Table):
    model = Role
    detail_template = """
    name name_giving
    #male
    #female
    MembersByRole
    """


class Member(dd.Model):
    """
    The role of a given :class:`Person` in a given :class:`Household`.
    """
  
    class Meta:
        verbose_name = _("Household Member")
        verbose_name_plural = _("Household Members")
        
    role = models.ForeignKey(Role,blank=True,null=True,help_text="""\
The Role of this Person in this Household.
List of choices is configured in `Configure --> Households --> Roles`.
""")
      #~ 
      #~ )
    #~ partner = models.ForeignKey(contacts.Partner,
        #~ related_name='membersbypartner')
    household = models.ForeignKey(Household)
    person = models.ForeignKey(settings.LINO.person_model,
      related_name='membersbyperson')
    start_date = models.DateField(_("From"),blank=True,null=True)
    end_date = models.DateField(_("Until"),blank=True,null=True)
    #~ type = models.ForeignKey('contacts.ContactType',blank=True,null=True,
      #~ verbose_name=_("contact type"))

    def __unicode__(self):
        if self.person_id is None:
            return super(Member,self).__unicode__()
        if self.role is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.role)

    def address_lines(self):
        for ln in self.person.address_person_lines():
            yield ln
        if self.household:
            for ln in self.household.address_person_lines():
                yield ln
            for ln in self.household.address_location_lines():
                yield ln
        else:
            for ln in self.address_location_lines():
                yield ln

class Members(dd.Table):
    model = Member
    order_by = ['start_date', 'end_date']
    
class MembersByHousehold(Members):
    label = _("Household Members")
    master_key = 'household'
    column_names = 'person role start_date end_date *'

class MembersByPerson(Members):
    label = _("Member of")
    master_key = 'person'
    column_names = 'household role start_date end_date *'

class MembersByRole(Members):
    master_key = 'role'
    column_names = 'person household start_date end_date *'
    
    
    

if settings.LINO.is_installed('households'):
    #~ Don't inject fields if this is just being imported from some other module.
  
    from lino.models import SiteConfig

    dd.inject_field(contacts.Partner,
        'is_household',
        #~ mti.EnableChild('contacts.Person',verbose_name=_("is Person")),
        mti.EnableChild(Household,verbose_name=_("is Household")),
        """Whether this Partner is a Household."""
        )




def setup_main_menu(site,ui,user,m): pass
    
def setup_master_menu(site,ui,user,m): 
    m.add_action(Households)

def setup_my_menu(site,ui,user,m): 
    pass
    
def setup_config_menu(site,ui,user,m): 
    m = m.add_menu("households",_("Households"))
    m.add_action(Roles)
    m.add_action(Types)
  
def setup_explorer_menu(site,ui,user,m):
    m = m.add_menu("households",_("Households"))
    m.add_action(Members)
  