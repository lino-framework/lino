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
ISIP (Individualized Social Integration 
Projects, fr. "PIIS", german "VSE")
are contracts between a PCSW and a Person.

"""

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode 


from lino import dd
from lino.utils import perms
from lino.utils import dblogger
#~ from lino.utils import printable
from lino import mixins
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
from lino.utils.choicelists import HowWell
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.models import get_site_config
from lino.tools import get_field
from lino.tools import resolve_field
from lino.utils.babel import DEFAULT_LANGUAGE, babelattr, babeldict_getitem, language_choices
from lino.utils.htmlgen import UL
#~ from lino.utils.babel import add_babel_field, DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils.choicelists import ChoiceList
from lino.utils import mti
from lino.utils import overlap, overlap2, encompass
from lino.mixins.printable import DirectPrintAction
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str, models_by_abc

from lino.modlib.countries.models import CountryCity
from lino.modlib.cal.models import DurationUnit, update_auto_task, update_auto_event

# not used here, but these modules are required in INSTALLED_APPS, 
# and other code may import them using 
# ``from lino.apps.dsbe.models import Property``

from lino.modlib.properties.models import Property
from lino.modlib.notes.models import NoteType
from lino.modlib.countries.models import Country, City
from lino.apps.dsbe.models import Company, Companies


#
# CONTRACT TYPES 
#
class ContractType(mixins.PrintableType,babel.BabelNamed):
  
    """
    The contract type determines the print template to be used. 
    Print templates may use the `ref` field to conditionally 
    hide or show certain parts.
    `exam_policy` is the default value for new Contracts.
    """
    
    _lino_preferred_width = 20 
    
    templates_group = 'isip/Contract'
    
    class Meta:
        verbose_name = _("ISIP Type")
        verbose_name_plural = _('ISIP Types')
        
    ref = models.CharField(_("Reference"),max_length=20,blank=True)
    exam_policy = models.ForeignKey("isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True,null=True)
        

class ContractTypes(dd.Table):
    model = ContractType
    column_names = 'name ref build_method template *'
    detail_template = """
    id name 
    ref build_method template
    ContractsByType
    """



#
# EXAMINATION POLICIES
#
class ExamPolicy(babel.BabelNamed):
    """
    Examination policy. 
    This also decides about automatic tasks to be created.
    """
    every = models.IntegerField(_("Evaluation every X months"),
        default=0)
    every_unit = DurationUnit.field(_("Duration unit"),
        default=DurationUnit.months,
        blank=True) # iCal:DURATION
    class Meta:
        verbose_name = _("Examination Policy")
        verbose_name_plural = _('Examination Policies')
        

class ExamPolicies(dd.Table):
    model = ExamPolicy
    column_names = 'name *'

#
# CONTRACT ENDINGS
#
class ContractEnding(models.Model):
    class Meta:
        verbose_name = _("Contract Ending")
        verbose_name_plural = _('Contract Endings')
        
    name = models.CharField(_("designation"),max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)
        
class ContractEndings(dd.Table):
    model = ContractEnding
    column_names = 'name *'
    order_by = ['name']


#~ def contract_contact_choices(company):
    #~ return links.Link.objects.filter(
        #~ type__use_in_contracts=True,
        #~ a_id=company.pk)

def contract_contact_choices(company):
    return contacts.Role.objects.filter(
        type__use_in_contracts=True,
        company__id=company.pk)



class ContractBase(mixins.DiffingMixin,mixins.TypedPrintable,mixins.AutoUser):
    """Abstract base class for 
    :class:`lino.modlib.jobs.models.Contract`
    and
    :class:`lino.modlib.isip.models.Contract`
    """
    
    TASKTYPE_CONTRACT_APPLIES_UNTIL = 1
    
    class Meta:
        abstract = True
  
    person = models.ForeignKey(settings.LINO.person_model,
        related_name="%(app_label)s_%(class)s_set_by_person",
        verbose_name=_("Person"))
        
    #~ contact = models.ForeignKey("links.Link",
      #~ related_name="%(app_label)s_%(class)s_set_by_contact",
      #~ blank=True,null=True,
      #~ verbose_name=_("represented by"))
    contact = models.ForeignKey("contacts.Role",
      related_name="%(app_label)s_%(class)s_set_by_contact",
      blank=True,null=True,
      verbose_name=_("represented by"))
    #~ contact = models.ForeignKey("contacts.Contact",
      #~ blank=True,null=True,
      #~ verbose_name=_("represented by"))
    language = babel.LanguageField()
    
    applies_from = models.DateField(_("applies from"),blank=True,null=True)
    applies_until = models.DateField(_("applies until"),blank=True,null=True)
    date_decided = models.DateField(blank=True,null=True,verbose_name=_("date decided"))
    date_issued = models.DateField(blank=True,null=True,verbose_name=_("date issued"))
    
    user_asd = models.ForeignKey("users.User",
        verbose_name=_("responsible (ASD)"),
        related_name="%(app_label)s_%(class)s_set_by_user_asd",
        #~ related_name='contracts_asd',
        blank=True,null=True) 
    
    exam_policy = models.ForeignKey("isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True,null=True)
        
    ending = models.ForeignKey("isip.ContractEnding",
        related_name="%(app_label)s_%(class)s_set",
        blank=True,null=True,
        verbose_name=_("Ending"))
    date_ended = models.DateField(blank=True,null=True,verbose_name=_("date ended"))
    
    #~ def summary_row(self,ui,rr,**kw):
    def summary_row(self,ui,**kw):
        s = ui.href_to(self)
        #~ s += " (" + ui.href_to(self.person) + ")"
        #~ s += " (" + ui.href_to(self.person) + "/" + ui.href_to(self.provider) + ")"
        return s
            
    def __unicode__(self):
        #~ return u'%s # %s' % (self._meta.verbose_name,self.pk)
        #~ return u'%s#%s (%s)' % (self.job.name,self.pk,
            #~ self.person.get_full_name(salutation=False))
        return u'%s#%s (%s)' % (self._meta.verbose_name,self.pk,
            self.person.get_full_name(salutation=False))
    
    #~ def __unicode__(self):
        #~ msg = _("Contract # %s")
        #~ # msg = _("Contract # %(pk)d (%(person)s/%(company)s)")
        #~ # return msg % dict(pk=self.pk, person=self.person, company=self.company)
        #~ return msg % self.pk
        
        
    def dsbe_person(self):
        """Used in document templates."""
        if self.person_id is not None:
            if self.person.coach2_id is not None:
                return self.person.coach2_id
            return self.person.coach1 or self.user
            
        #~ try:
            #~ return self.person.coaching_set.get(type__name__exact='DSBE').coach        
        #~ except Exception,e:
            #~ return self.person.user or self.user
            
    def person_changed(self,request):
        if self.person_id is not None:
            if self.person.coach1_id is None or self.person.coach1_id == self.user_id:
                self.user_asd = None
            else:
                self.user_asd = self.person.coach1
                
    def on_create(self,request):
        super(ContractBase,self).on_create(request)
        self.person_changed(request)
      
    def full_clean(self,*args,**kw):
        if self.type_id and self.type.exam_policy_id:
            if not self.exam_policy_id:
                self.exam_policy_id = self.type.exam_policy_id
        if self.company:
            if self.contact is None or self.contact.company != self.company:
                qs = contract_contact_choices(self.company)
                #~ qs = self.company.rolesbyparent.all()
                if qs.count() == 1:
                    self.contact = qs[0]
                #~ else:
                    #~ print "20120227 clear contact!"
                    #~ self.contact = None
        # severe test is ready but not yet activated :
        if False and self.person_id is not None:
            msg = OverlappingContractsTest(self.person).check(self)
            if msg:
                raise ValidationError(msg)
            
        super(ContractBase,self).full_clean(*args,**kw)
        

    def update_owned_instance(self,comp):
        #~ mixins.Reminder.update_owned_task(self,task)
        #~ contacts.PartnerDocument.update_owned_task(self,task)
        comp.project = self.person
        #~ task.company = self.company
        
    def after_update_owned_instance(self,comp):
        if comp.user_modified:
            self.update_reminders()
        
        
    def save(self,*args,**kw):
        super(ContractBase,self).save(*args,**kw)
        self.update_reminders()
        
    def update_reminders(self):
        """
        Generate automatic calendar events owned by this contract.
        
        [NOTE1] if one event has been manually rescheduled, all following events
        adapt to the new rythm.
        
        """
        MAX_AUTO_EVENTS = 36
        if self.user:
            if self.applies_from and self.exam_policy_id \
                and self.exam_policy.every > 0 \
                and self.exam_policy.every_unit:
                date = self.applies_from
            else:
                date = None
            until = self.date_ended or self.applies_until
            if not until:
                date = None
            for i in range(MAX_AUTO_EVENTS):
                if date:
                    date = self.exam_policy.every_unit.add_duration(date,self.exam_policy.every)
                    #~ date = DurationUnit.months.add_duration(
                            #~ date,self.exam_policy.every)
                    if until and date > until:
                        date = None
                subject = _("Evaluation %d") % (i + 1)
                e = update_auto_event(
                  i + 1,
                  self.user,
                  date,subject,self)
                if e: # [NOTE1]
                    date = e.start_date
                        
            if self.applies_until:
                date = DurationUnit.months.add_duration(self.applies_until,-1)
            else:
                date = None
            update_auto_task(
              self.TASKTYPE_CONTRACT_APPLIES_UNTIL,
              self.user,
              date,
              _("Contract ends in a month"),
              self)
              #~ alarm_value=1,alarm_unit=DurationUnit.months)
              
    #~ def overlaps_with(self,b):
        #~ if b == self: 
            #~ return False
        #~ a1 = self.applies_from
        #~ a2 = self.date_ended or self.applies_until
        #~ b1 = b.applies_from
        #~ b2 = b.date_ended or b.applies_until
        #~ return overlap(a1,a2,b1,b2)
        
    def active_period(self):
        return (self.applies_from, self.date_ended or self.applies_until)
        
        
    #~ def data_control(self):
        #~ msgs = []
        #~ for model in models_by_abc(ContractBase):
            #~ for con in model.objects.filter(person=self.person):
                #~ if self.overlaps_with(con):
                    #~ msgs.append(_("Dates overlap with %s") % con)
        #~ return msgs
          

class OverlappingContractsTest:
    """
    Volatile object used to test for overlapping contracts.
    """
    def __init__(self,person):
        """
        Test whether this person has overlapping contracts.
        """
        from lino.modlib.isip.models import ContractBase
        self.person = person
        self.actives = []
        for model in models_by_abc(ContractBase):
            for con1 in model.objects.filter(person=person):
                p1 = con1.active_period()
                if p1:
                    self.actives.append((p1,con1))
        
    def check(self,con1):
        ap = con1.active_period()
        if ap:
            if not encompass((self.person.coached_from,self.person.coached_until),ap):
                return _("Date range lies outside of coached period")
            for (p2,con2) in self.actives:
                if con1 != con2 and overlap2(ap,p2):
                    return _("Date range overlaps with %(ctype)s #%(id)s") % dict(
                      ctype=con2.__class__._meta.verbose_name,
                      id=con2.pk
                    )
        return None
        
    def check_all(self):
        messages = []
        for (p1,con1) in self.actives:
            msg = self.check(con1)
            if msg:
                messages.append(
                  _("%(ctype)s #%(id)s : %(msg)s") % dict(
                    msg=msg,
                    ctype=con1.__class__._meta.verbose_name,
                    id=con1.pk))
        return messages
        

            
    
class Contract(ContractBase):
    """
    ISIP = Individual Social Integration Project (VSE)
    """
    class Meta:
        verbose_name = _("ISIP")
        verbose_name_plural = _("ISIPs")
        
    type = models.ForeignKey("isip.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        verbose_name=_("Contract Type"),blank=True)
    
    company = models.ForeignKey(settings.LINO.company_model,
        verbose_name=_("Company"),
        blank=True,null=True)
        
    stages = dd.RichTextField(_("stages"),
        blank=True,null=True,format='html')
    goals = dd.RichTextField(_("goals"),
        blank=True,null=True,format='html')
    duties_asd = dd.RichTextField(_("duties ASD"),
        blank=True,null=True,format='html')
    duties_dsbe = dd.RichTextField(_("duties DSBE"),
        blank=True,null=True,format='html')
    duties_company = dd.RichTextField(_("duties company"),
        blank=True,null=True,format='html')
    duties_person = dd.RichTextField(_("duties person"),
        blank=True,null=True,format='html')
    
    @classmethod
    def site_setup(cls,lino):
        """
        Here's how to override the default verbose_name of a field.
        """
        #~ resolve_field('dsbe.Contract.user').verbose_name=_("responsible (DSBE)")
        Contract.user.verbose_name=_("responsible (DSBE)")
        #~ lino.CONTRACT_PRINTABLE_FIELDS = dd.fields_list(cls,
        cls.PRINTABLE_FIELDS = dd.fields_list(cls,
            'person company contact type '
            'applies_from applies_until '
            'language '
            'stages goals duties_dsbe duties_company '
            'duties_asd duties_person '
            'user user_asd exam_policy '
            'date_decided date_issued ')
        #~ super(Contract,cls).site_setup(lino)
        
    @chooser()
    def contact_choices(cls,company):
        if company is not None:
            #~ return company.rolesbyparent.all()
            #~ return company.rolesbyparent.filter(type__use_in_contracts=True)
            #~ return links.Link.objects.filter(type__use_in_contracts=True,a=company)
            return contract_contact_choices(company)
        return []

    def get_recipient(self):
        if self.contact:
            return self.contact
        if self.company:
            return self.company
        return self.person
    recipient = property(get_recipient)
        
    def disabled_fields(self,request):
        #~ if self.must_build:
        if not self.build_time:
            return []
        #~ return df + settings.LINO.CONTRACT_PRINTABLE_FIELDS
        return self.PRINTABLE_FIELDS


class ContractDetail(dd.DetailLayout):    
    general = """
    id:8 person:25 user:15 user_asd:15 language:8
    type company contact:20     
    applies_from applies_until exam_policy
    
    date_decided date_issued 
    date_ended ending
    cal.TasksByOwner cal.EventsByOwner
    """
    
    isip = """
    stages        goals
    duties_asd    duties_dsbe
    duties_company duties_person
    """
    
    main = "general isip"
    
    def setup_handle(self,dh):
        dh.general.label = _("General")
        dh.isip.label = _("ISIP")


class Contracts(dd.Table):
    model = Contract
    column_names = 'id applies_from applies_until user type *'
    order_by = ['id']
    #~ active_fields = ('company','contact')
    active_fields = ['company']
    detail_layout = ContractDetail()
    
class ContractsByPerson(Contracts):
    master_key = 'person'
    column_names = 'applies_from applies_until user type *'

        
class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from person user *"
    order_by = ["applies_from"]

class MyContracts(Contracts,mixins.ByUser):
    column_names = "applies_from person *"
    #~ label = _("My ISIP contracts")
    #~ label = _("My PIIS contracts")
    #~ order_by = "reminder_date"
    #~ column_names = "reminder_date person company *"
    order_by = ["applies_from"]
    #~ filter = dict(reminder_date__isnull=False)




def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    if user.is_spis:
        m.add_action(MyContracts)
  
def setup_config_menu(site,ui,user,m): 
    if user.is_spis:
        m  = m.add_menu("isip",_("ISIPs"))
        m.add_action(ContractTypes)
        m.add_action(ContractEndings)
        m.add_action(ExamPolicies)
  
def setup_explorer_menu(site,ui,user,m):
    if user.is_spis:
        m.add_action(Contracts)
