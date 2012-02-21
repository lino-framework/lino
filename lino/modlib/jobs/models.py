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
See also :doc:`/dsbe/models`.

"""
import logging
logger = logging.getLogger(__name__)

import os
import time
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode 

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation





from lino import dd
#~ from lino import layouts
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
from lino.tools import range_filter
from lino.utils.babel import DEFAULT_LANGUAGE, babelattr, babeldict_getitem, language_choices
from lino.utils.htmlgen import UL
#~ from lino.utils.babel import add_babel_field, DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils.choicelists import ChoiceList
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.cal.models import DurationUnit

# not used here, but these modules are required in INSTALLED_APPS, 
# and other code may import them using 
# ``from lino.apps.dsbe.models import Property``

from lino.modlib.properties.models import Property
from lino.modlib.notes.models import NoteType
from lino.modlib.countries.models import Country, City
from lino.modlib.isip.models import ContractBase
from lino.apps.dsbe.models import Company, Companies, CompanyDetail


#~ SCHEDULE_CHOICES = {
    #~ 'de':[ 
        #~ u"5-Tage-Woche",
        #~ u"Montag, Mittwoch, Freitag",
        #~ u"Individuell",
        #~ ],
    #~ 'fr':[ 
        #~ u"5 jours/semaine",
        #~ u"lundi,mercredi,vendredi",
        #~ u"individuel",
        #~ ],
    #~ 'en':[
        #~ u"5 days/week",
        #~ u"Monday, Wednesday, Friday",
        #~ u"Individual",
        #~ ]
#~ }

#~ REGIME_CHOICES = {
    #~ 'de':[ 
        #~ u"20 Stunden/Woche",
        #~ u"35 Stunden/Woche",
        #~ u"38 Stunden/Woche",
        #~ ],
    #~ 'fr':[ 
        #~ u"20 heures/semaine",
        #~ u"35 heures/semaine",
        #~ u"38 heures/semaine",
        #~ ],
    #~ 'en':[
        #~ u"20 hours/week",
        #~ u"35 hours/week",
        #~ u"38 hours/week",
        #~ u"38 hours/week",
        #~ ]
#~ }


class Schedule(babel.BabelNamed):
    """List of choices for `jobs.Contract.schedule` field."""
    class Meta:
        verbose_name = _("Work Schedule")
        verbose_name_plural = _('Work Schedules')
        
class Schedules(dd.Table):
    model = Schedule
    order_by = ['name']

class Regime(babel.BabelNamed):
    """List of choices for `jobs.Contract.regime` field."""
    class Meta:
        verbose_name = _("Work Regime")
        verbose_name_plural = _('Work Regimes')
        
class Regimes(dd.Table):
    model = Regime
    order_by = ['name']




class JobProvider(Company):
    """Stellenanbieter (BISA, BW, ...) 
    """
    class Meta:
        app_label = 'jobs'
        verbose_name = _("Job Provider")
        verbose_name_plural = _('Job Providers')
    

class JobProviderDetail(CompanyDetail):
    """
    This is the same as CompanyDetail, except that we
    
    - remove MTI fields from `remark` panel
    - add a new tab `jobs`
    
    """
    box5 = "remarks" 
    jobs = """
    JobsByProvider
    ContractsByProvider
    """
    main = "general notes jobs"
    
    def setup_handle(self,lh):
        CompanyDetail.setup_handle(self,lh)
        lh.jobs.label = _("Jobs")

      

  


class JobProviders(Companies):
    """
    List of Companies that have `Company.is_jobprovider` activated.
    """
    use_as_default_report = False
    model = JobProvider
    app_label = 'jobs'
    detail_layout = JobProviderDetail()
  


#
# CONTRACT TYPES 
#
class ContractType(mixins.PrintableType,babel.BabelNamed):
    """
    This is the homologue of 
    :class:`lino.modlib.isip.models.ContractType` (see there 
    for general documentation).
    
    They are separated tables because ISIP contracts are in practice
    very different from JOBS contracts, and also their types should 
    not be mixed.
    
    """
  
    _lino_preferred_width = 20 
    
    templates_group = 'jobs/Contract'
    
    class Meta:
        verbose_name = _("Job Contract Type")
        verbose_name_plural = _('Job Contract Types')
        
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


class Sector(babel.BabelNamed):
    """Each Job should have an "Activity Sector"."""
    class Meta:
        verbose_name = _("Job Sector")
        verbose_name_plural = _('Job Sectors')
        
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
class Sectors(dd.Table):
    model = Sector
    order_by = ['name']

class Function(babel.BabelNamed):
    """Each Job may have a Function."""
    class Meta:
        verbose_name = _("Job Function")
        verbose_name_plural = _('Job Functions')
        
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
    sector = models.ForeignKey(Sector)
        #~ related_name="%(app_label)s_%(class)s_set_by_provider",
        #~ verbose_name=_("Job Provider"),
        #~ blank=True,null=True)
class Functions(dd.Table):
    model = Function
    column_names = 'name sector *'
    order_by = ['name']
    
class FunctionsBySector(Functions):
    master_key = 'sector'

#
# JOB CONTRACTS
# 
class Contract(ContractBase):
    """
    A Contract
    
    [NOTE1] I applies_from and duration are set, then the default value 
    for applies_until is computed 26 workdays per month:
    
    - duration `312` -> 12 months 
    - duration `468` -> 18 months 
    - duration `624` -> 24 months 
    
    """
    class Meta:
        verbose_name = _("Job Contract")
        verbose_name_plural = _('Job Contracts')
        
    type = models.ForeignKey("jobs.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        verbose_name=_("Contract Type"),blank=True)
    
    provider = models.ForeignKey(JobProvider,
        related_name="%(app_label)s_%(class)s_set_by_provider",
        #~ verbose_name=_("Employer"),
        blank=True,null=True)
    job = models.ForeignKey("jobs.Job",
        verbose_name=_("Job"),
        blank=True,null=True)
        
    duration = models.IntegerField(_("duration (days)"),
        blank=True,null=True,default=None)
    
    
    #~ regime = models.CharField(_("regime"),max_length=200,blank=True)
    #~ schedule = models.CharField(_("schedule"),max_length=200,blank=True)
    regime = models.ForeignKey(Regime,blank=True,null=True)
    schedule = models.ForeignKey(Schedule,blank=True,null=True)
    hourly_rate = dd.PriceField(_("hourly rate"),blank=True,null=True)
    refund_rate = models.CharField(_("refund rate"),max_length=200,
        blank=True)
    
    reference_person = models.CharField(_("reference person"),max_length=200,
        blank=True)
        
    responsibilities = dd.RichTextField(_("responsibilities"),
        blank=True,null=True,format='html')
    
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
    
    #~ aid_nature = models.CharField(_("aid nature"),max_length=100,blank=True)
    #~ aid_rate = models.CharField(_("aid rate"),max_length=100,blank=True)
    
    @chooser()
    def contact_choices(cls,provider):
        if provider is not None:
            #~ return provider.rolesbyparent.all()
            #~ return provider.rolesbyparent.filter(type__use_in_contracts=True)
            #~ return links.Link.objects.filter(type__use_in_contracts=True,a=provider)
            return contacts.Role.objects.filter(
                type__use_in_contracts=True,company=provider)
        return []
        
    def get_company(self):
        return self.provider
    company = property(get_company)
    """for backwards compatibility. Document templates use a field `company`.
    """

    def get_recipient(self):
        if self.contact:
            return self.contact
        if self.provider:
            return self.provider
        return self.person
    recipient = property(get_recipient)
    
    
    #~ def prepare_printable(self):
        #~ self.company = self.company
    
    
    @chooser(simple_values=True)
    def duration_choices(cls):
        return [ 312, 468, 624 ]
        #~ return [ 0, 25, 50, 100 ]
    
    #~ @chooser(simple_values=True)
    #~ def regime_choices(cls,language):
        #~ return language_choices(language,REGIME_CHOICES)
    
    #~ @chooser(simple_values=True)
    #~ def schedule_choices(cls,language):
        #~ return language_choices(language,SCHEDULE_CHOICES)
    
    @chooser(simple_values=True)
    def refund_rate_choices(cls):
        return [ 
        u"0%",
        u"25%",
        u"50%",
        u"100%",
        ]
    
    
    def disabled_fields(self,request):
        df = []
        if self.job:
            if self.job.provider:
                df.append('provider')
            if self.job.contract_type:
                df.append('type')
        if not self.build_time:
            return df 
        return df + self.PRINTABLE_FIELDS
        
    def unused_get_reminder_html(self,ui,user):
        #~ url = ui.get_detail_url(self,fmt='detail')
        #~ if self.type:
            #~ s = unicode(self.type)
        #~ else:
            #~ s = self._meta.verbose_name
        #~ s += ' #' + unicode(self.pk)
        
        #~ s = ui.href(url,cgi.escape(s))
        s = ui.href_to(self)
        
        more = []
        if self.person:
            more.append(ui.href_to(self.person))
        if self.provider:
            more.append(ui.href_to(self.provider))
        if self.user and self.user != user:
            more.append(cgi.escape(unicode(self.user)))
        if self.reminder_text:
            more.append(cgi.escape(self.reminder_text))
        else:
            more.append(cgi.escape(_('Due date reached')))
        return s + '&nbsp;: ' + (', '.join(more))
        
    #~ def save(self,*args,**kw):
        #~ if self.job_id is not None:
            #~ qs = self.person.candidature_set.filter(contract=self)
            #~ if qs.count() == 0:
                #~ qs = self.person.candidature_set.filter(job=self.job,contract=None)
                #~ if qs.count() == 1: 
                    #~ obj = qs[0]
                    #~ obj.contract = self
                    #~ obj.save()
                    #~ dblogger.info(u'Marked job request %s as satisfied by %s' % (
                      #~ obj,self))
        #~ r = super(Contract,self).save(*args,**kw)
        #~ return r
        
    #~ def data_control(self):
        #~ "Used by :class:`lino.models.DataControlListing`."
        #~ msgs = []
        #~ qs = self.person.candidature_set.filter(contract=self)
        #~ if qs.count() > 1: 
            #~ msgs.append(
              #~ u'There are more than one job request using contract %s : %s' \
              #~ % qs)
        #~ return msgs
        
    def full_clean(self,*args,**kw):
        if self.person_id is not None:
            #~ if not self.user_asd:
                #~ if self.person.user != self.user:
                    #~ self.user_asd = self.person.user
            if self.applies_from:
                if self.person.birth_date:
                    def duration(refdate):
                        if type(refdate) != datetime.date:
                            raise Exception("%r is not a date!" % refdate)
                        delta = refdate - self.person.birth_date.as_date()
                        age = delta.days / 365
                        if age < 36:
                            return 312
                        elif age < 50:
                            return 468
                        else:
                            return 624
                  
                    if self.duration is None:
                        if self.applies_until:
                            self.duration = duration(self.applies_until)
                        else:
                            self.duration = duration(self.applies_from)
                            self.applies_until = self.applies_from + datetime.timedelta(days=self.duration)
                            
                if self.duration and not self.applies_until:
                    #~ self.applies_until = self.applies_from + datetime.timedelta(days=self.duration)
                    self.applies_until = DurationUnit.months.add_duration(
                      self.applies_from,self.duration/26)  # [NOTE1]
              
        #~ if self.job_id is not None:
        if self.job:
            if self.job.provider is not None:
                self.provider = self.job.provider
            if self.job.contract_type is not None:
                self.type = self.job.contract_type
            if self.hourly_rate is None:
                self.hourly_rate = self.job.hourly_rate
            
        if self.provider is not None:
            if self.contact is not None:
                if self.contact.company.pk != self.provider.company_ptr.pk:
                    self.contact = None
                    
        super(Contract,self).full_clean(*args,**kw)
        
    @classmethod
    def site_setup(cls,lino):
        """
        Here's how to override the default verbose_name of a field.
        """
        Contract.user.verbose_name=_("responsible (DSBE)")
        #~ resolve_field('jobs.Contract.user').verbose_name=_("responsible (DSBE)")
        #~ lino.CONTRACT_PRINTABLE_FIELDS = dd.fields_list(cls,
        cls.PRINTABLE_FIELDS = dd.fields_list(cls,
            'person job provider contact type '
            'applies_from applies_until duration '
            'language schedule regime hourly_rate refund_rate '
            'reference_person responsibilities '
            'user user_asd exam_policy '
            'date_decided date_issued ')
        #~ super(Contract,cls).site_setup(lino)

class Contracts(dd.Table):
    model = Contract
    column_names = 'id job applies_from applies_until user type *'
    order_by = ['id']
    active_fields = 'job provider contact'.split()
    
    detail_template = """
    id:8 person:25 user:15 user_asd:15 language:8
    job type provider contact:20     
    applies_from duration applies_until 
    regime:20 schedule:30 hourly_rate:10 refund_rate:10
    date_decided date_issued date_ended ending
    reference_person build_time
    responsibilities cal.TasksByOwner cal.EventsByOwner 
    """
    
    
class ContractsByPerson(Contracts):
    master_key = 'person'
    column_names = 'job applies_from applies_until user type *'

        
class ContractsByProvider(Contracts):
    master_key = 'provider'
    column_names = 'person job applies_from applies_until user type *'

class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from person job user *"
    order_by = ["applies_from"]

class ContractsByJob(Contracts):
    column_names = 'person applies_from applies_until user type *'
    master_key = 'job'

class ContractsByRegime(Contracts):
    master_key = 'regime'
    column_names = 'job applies_from applies_until user type *'

class ContractsBySchedule(Contracts):
    master_key = 'schedule'
    column_names = 'job applies_from applies_until user type *'

class MyContracts(mixins.ByUser,Contracts):
    column_names = "applies_from person job *"
    label = _("My contracts")
    #~ order_by = "reminder_date"
    #~ column_names = "reminder_date person company *"
    order_by = ["applies_from"]
    #~ filter = dict(reminder_date__isnull=False)




class JobType(mixins.Sequenced):
    """
    The list of Job Types is used for statistical analysis, 
    e.g. in :class:``
    """
    
    class Meta:
        verbose_name = _("Job Type")
        verbose_name_plural = _('Job Types')
        
    name = models.CharField(max_length=200,
          blank=True,
          verbose_name=_("Designation"))
          
    remark = models.CharField(max_length=200,
        blank=True,
        verbose_name=_("Remark"))
        
          
    def __unicode__(self):
        return unicode(self.name)
        
  
class SectorFunction(models.Model):
    """
    Abstract base for models that refer to a 
    :class:`Sector` and a :class:`Function`.
    """
    class Meta:
        abstract = True
        
    sector = models.ForeignKey("jobs.Sector",
        blank=True,null=True)
    function = models.ForeignKey("jobs.Function",
        blank=True,null=True)
    
    @chooser()
    def function_choices(cls,sector):
        if sector is not None:
            return sector.function_set.all()
        return Function.objects.all()
        
        
class Offer(SectorFunction):
    "A Job Offer"
    class Meta:
        verbose_name = _("Job Offer")
        verbose_name_plural = _('Job Offers')
        ordering = ['name']
        
    name = models.CharField(max_length=100,
        blank=True,
        verbose_name=_("Name"))
    
    provider = models.ForeignKey(JobProvider,
        blank=True,null=True)
    
    selection_from = models.DateField(_("selection from"),
        blank=True,null=True)
    selection_until = models.DateField(_("selection until"),
        blank=True,null=True)
    start_date = models.DateField(_("start date"),
        blank=True,null=True)
    
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
    def __unicode__(self):
        if self.name:
            return self.name
        return u'%s @ %s' % (self.function,self.provider)
  
class Offers(dd.Table):
    model = Offer
    
    
    
#
# STUDY TYPE
#
class StudyType(babel.BabelNamed):
    #~ text = models.TextField(_("Description"),blank=True,null=True)
    class Meta:
        verbose_name = _("study type")
        verbose_name_plural = _("study types")

class StudyTypes(dd.Table):
    #~ label = _('Study types')
    model = StudyType
    order_by = ["name"]


class HistoryByPerson(dd.Table):
    master_key = 'person'
    order_by = ["started"]
    
    @classmethod
    def create_instance(self,req,**kw):
        obj = super(HistoryByPerson,self).create_instance(req,**kw)
        if obj.person is not None:
            previous_exps = self.model.objects.filter(person=obj.person).order_by('started')
            if previous_exps.count() > 0:
                exp = previous_exps[previous_exps.count()-1]
                if exp.stopped:
                    obj.started = exp.stopped
                else:
                    obj.started = exp.started
        return obj
    


class Study(CountryCity):
    class Meta:
        verbose_name = _("study or education")
        verbose_name_plural = _("Studies & education")
    person = models.ForeignKey(settings.LINO.person_model) #,verbose_name=_("Person"))
    type = models.ForeignKey(StudyType,verbose_name=_("Study type"))
    content = models.CharField(max_length=200,
        blank=True, # null=True,
        verbose_name=_("Study content"))
    #~ content = models.ForeignKey(StudyContent,blank=True,null=True,verbose_name=_("Study content"))
  
    started = dd.MonthField(_("started"),blank=True,null=True)
    stopped = dd.MonthField(_("stopped"),blank=True,null=True)
    #~ started = models.DateField(blank=True,null=True,verbose_name=_("started"))
    #~ stopped = models.DateField(blank=True,null=True,verbose_name=_("stopped"))
    #~ started = dd.MonthField(blank=True,null=True,verbose_name=_("started"))
    #~ stopped = dd.MonthField(blank=True,null=True,verbose_name=_("stopped"))
    success = models.BooleanField(verbose_name=_("Success"),default=False)
    language = models.ForeignKey("countries.Language",
        blank=True,null=True,verbose_name=_("Language"))
    #~ language = dd.LanguageField(blank=True,null=True,verbose_name=_("Language"))
    
    school = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("School"))
    #~ school = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("School"))
    
    remarks = models.TextField(blank=True,null=True,verbose_name=_("Remarks"))
    
    def __unicode__(self):
        return unicode(self.type)

class Studies(dd.Table):
    "General list of Studies (all Persons)"
    model = Study
    order_by = "country city type content".split()

        
class StudiesByCountry(Studies):
    master_key = 'country'
    
class StudiesByCity(Studies):
    master_key = 'city'
    
class StudiesByPerson(HistoryByPerson):
    "List of studies for a known person."
    model = Study
    #~ label = _("Studies & experiences")
    button_label = _("Studies")
    column_names = 'type content started stopped country city success language school remarks *'
    
class Experience(SectorFunction):
    class Meta:
        verbose_name = _("Job Experience")
        verbose_name_plural = _("Job Experiences")
    person = models.ForeignKey(settings.LINO.person_model,verbose_name=_("Person"))
    #~ company = models.ForeignKey("contacts.Company",verbose_name=_("Company"))
    company = models.CharField(max_length=200,verbose_name=_("company"))
    #~ type = models.ForeignKey(JobType,verbose_name=_("job type"))
    title = models.CharField(max_length=200,verbose_name=_("job title"),blank=True)
    country = models.ForeignKey("countries.Country",
        blank=True,null=True,
        verbose_name=_("Country"))
  
    started = dd.MonthField(_("started"),blank=True,null=True)
    stopped = dd.MonthField(_("stopped"),blank=True,null=True)
    
    remarks = models.TextField(blank=True,null=True,verbose_name=_("Remarks"))
    
    def __unicode__(self):
        return unicode(self.title)
  
class Experiences(dd.Table):
    model = Experience
  
class ExperiencesByFunction(Experiences):
    master_key = 'function'
    order_by = ["started"]

    
class ExperiencesByPerson(Experiences,HistoryByPerson):
    "List of job experiences for a known person"
    #~ model = Experience
    column_names = "company started stopped title sector function country remarks"
    
  
    
    

class Job(SectorFunction):
    """
    A place where Clients can work. at some Job Provider
    """
    
    _lino_preferred_width = 20 
    
    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _('Jobs')
        ordering = ['name']
        
    name = models.CharField(max_length=100,
        verbose_name=_("Name"))
    
    type = models.ForeignKey("jobs.JobType",
        blank=True,null=True,
        verbose_name=_("Job Type"))
    
    provider = models.ForeignKey(JobProvider,
        blank=True,null=True)
    
    contract_type = models.ForeignKey(ContractType,blank=True,null=True,
        verbose_name=_("Contract Type"))
    
    hourly_rate = dd.PriceField(_("hourly rate"),blank=True,null=True)
    
    capacity = models.IntegerField(_("capacity"),
        default=1)
        
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
    def __unicode__(self):
        if self.provider:
            return u'%s bei %s' % (self.name,self.provider.name)
        return self.name
  
    def disabled_fields(self,request):
        #~ if self.contract_set.count():
        #~ if self.contract_set.filter(must_build=False).count():
        if self.contract_set.filter(build_time__isnull=False).count():
            return ['contract_type','provider']
        return []
        
        
    #~ @chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().queryset
        
    #~ @classmethod
    #~ def setup_report(model,rpt):
        #~ rpt.add_action(DirectPrintAction('candidates',_("List of candidates"),'courses/candidates.odt'))
        #~ rpt.add_action(DirectPrintAction('participants',_("List of participants"),'courses/participants.odt'))
        
    #~ def get_print_language(self,pm):
        #~ "Used by DirectPrintAction"
        #~ return DEFAULT_LANGUAGE
        
    #~ def participants(self):
        #~ u"""
        #~ Liste von :class:`CourseRequest`-Instanzen, 
        #~ die in diesem Kurs eingetragen sind. 
        #~ """
        #~ return ParticipantsByCourse().request(master_instance=self)
        
    #~ def candidates(self):
        #~ u"""
        #~ Liste von :class:`CourseRequest`-Instanzen, 
        #~ die noch in keinem Kurs eingetragen sind, aber für diesen Kurs in Frage 
        #~ kommen. 
        #~ """
        #~ return CandidatesByCourse().request(master_instance=self)
        
        
#~ class Wish(SectorFunction):
    #~ class Meta:
        #~ verbose_name = _("Job Wish")
        #~ verbose_name_plural = _('Job Wishes')
    #~ person = models.ForeignKey("contacts.Person")
    
#~ class Wishes(dd.Table):
    #~ model = Wish
    
#~ class WishesByPerson(Wishes):
    #~ master_key = 'person'

#~ class WishesBySector(Wishes):
    #~ master_key = 'sector'

#~ class WishesByFunction(Wishes):
    #~ master_key = 'function'


#~ class WishesByOffer(dd.Table):
    #~ """
    #~ Shows the persons that whish this Offer.
    
    #~ It is a slave report without 
    #~ :attr:`master_key <lino.dd.Table.master_key>`,
    #~ which is allowed only because it also overrides
    #~ :meth:`get_request_queryset`
    #~ """
  
    #~ model = Wish
    #~ master = Offer
    #~ label = _("Candidate Job Wishes")
    
    #~ can_add = perms.never
    #~ can_change = perms.never
    
    #~ def get_request_queryset(self,rr):
        #~ """
        #~ Needed because the Offer is not the direct master.
        #~ """
        #~ offer = rr.master_instance
        #~ if offer is None:
            #~ return []
        #~ kw = {}
        #~ qs = self.model.objects.order_by('date_submitted')
        
        #~ if offer.function:
            #~ qs = qs.filter(function=offer.function)
        #~ if offer.sector:
            #~ qs = qs.filter(sector=offer.sector)
            
        #~ return qs

    

class Candidature(SectorFunction):
    """
    """
    class Meta:
        verbose_name = _("Job Candidature")
        verbose_name_plural = _('Job Candidatures')
        
    person = models.ForeignKey(settings.LINO.person_model)
    
    job = models.ForeignKey("jobs.Job",
        blank=True,null=True)
        #~ verbose_name=_("Requested Job"))
    
    #~ date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    date_submitted = models.DateField(_("date submitted"))
    u"Das Datum, an dem die Anfrage erstellt wurde."
    
    #~ contract = models.ForeignKey("jobs.Contract",blank=True,null=True,
        #~ verbose_name=_("Contract found"))
    #~ u"""
    #~ Der Vertrag, durch den diese Anfrage befriedigt wurde 
    #~ (ein Objekt vom Typ :class:`Contract`).
    #~ So lange dieses Feld leer ist, gilt die Anfrage als offen.
    #~ """
        
    remark = models.TextField(
        blank=True,null=True,
        verbose_name=_("Remark"))
        
    def __unicode__(self):
        return force_unicode(_('Candidature by %(person)s') % dict(
            person=self.person.get_full_name(salutation=False)))
            
    #~ @chooser()
    #~ def contract_choices(cls,job,person):
        #~ if person and job:
            #~ return person.contract_set.filter(job=job)
        #~ return []
        
    #~ def clean(self,*args,**kw):
        #~ if self.contract:
            #~ if self.contract.person != self.person:
                #~ raise ValidationError(
                  #~ "Cannot satisfy a Candidature with a Contract on another Person")
        #~ super(Candidature,self).clean(*args,**kw)
    
    def on_create(self,req):
        self.date_submitted = datetime.date.today()
    

class Candidatures(dd.Table):
    model = Candidature
    order_by = ['date_submitted']
    column_names = 'date_submitted job:25 * id'

class CandidaturesByPerson(Candidatures):
    master_key = 'person'

class CandidaturesBySector(Candidatures):
    master_key = 'sector'

class CandidaturesByFunction(Candidatures):
    master_key = 'function'

class CandidaturesByJob(Candidatures):
    master_key = 'job'
    column_names = 'date_submitted person:25 * id'
  
    @classmethod
    def create_instance(self,req,**kw):
        obj = super(CandidaturesByJob,self).create_instance(req,**kw)
        if obj.job is not None:
            obj.type = obj.job.type
        return obj
    



class SectorFunctionByOffer(dd.Table):
    """
    Shows the Candidatures or Experiences for this Offer.
    
    It is a slave report without 
    :attr:`master_key <lino.dd.Table.master_key>`,
    which is allowed only because it overrides
    :meth:`get_request_queryset`.
    """
    can_add = perms.never
    can_change = perms.never
    master = Offer
    
    @classmethod
    def get_request_queryset(self,rr):
        """
        Needed because the Offer is not the direct master.
        """
        offer = rr.master_instance
        if offer is None:
            return []
        kw = {}
        qs = self.model.objects.order_by('date_submitted')
        
        if offer.function:
            qs = qs.filter(function=offer.function)
        if offer.sector:
            qs = qs.filter(sector=offer.sector)
            
        #~ required_id_sets = []
        
        #~ if offer.function:
            #~ q = JobRequest.objects.filter(function=offer.function)
            #~ required_id_sets.append(set(q.values_list('person__id',flat=True)))
        #~ if offer.sector:
            #~ q = JobRequest.objects.filter(sector=offer.sector)
            #~ required_id_sets.append(set(q.values_list('person__id',flat=True)))

        #~ if required_id_sets:
            #~ s = set(required_id_sets[0])
            #~ for i in required_id_sets[1:]:
                #~ s.intersection_update(i)
                #~ # keep only elements found in both s and i.
            #~ qs = qs.filter(id__in=s)
              
        return qs
  

class CandidaturesByOffer(SectorFunctionByOffer):
    model = Candidature
    label = _("Candidates")
    
class ExperiencesByOffer(SectorFunctionByOffer):
    model = Experience
    label = _("Candidates")
    


class Jobs(dd.Table):
    model = Job
    #~ order_by = ['start_date']
    column_names = 'name provider * id'
    
    detail_template = """
    name provider contract_type type id 
    sector function capacity hourly_rate 
    remark CandidaturesByJob
    ContractsByJob
    """

    

class JobTypes(dd.Table):
    model = JobType
    order_by = ['name']
    detail_template = """
    id name 
    JobsByType
    """

class JobsByProvider(Jobs):
    master_key = 'provider'

#~ class JobsByFunction(Jobs):
    #~ master_key = 'function'

#~ class JobsBySector(Jobs):
    #~ master_key = 'sector'

class JobsByType(Jobs):
    master_key = 'type'

class ContractsByType(Contracts):
    master_key = 'type'
    
    
  
if True: # settings.LINO.user_model:
  
    from lino.tools import resolve_model, UnresolvedModel
    USER_MODEL = resolve_model(settings.LINO.user_model)
    
    class ContractsSearch(Contracts):
        """
        Shows the job contracts owned by this user.
        """
        label = _("Job Contracts Search")
        
        use_as_default_report = False
        
        parameters = dict(
          user = models.ForeignKey(USER_MODEL,blank=True),
          #~ user = models.ForeignKey(settings.LINO.user_model,blank=True),
          type = models.ForeignKey(ContractType,blank=True,verbose_name=_("Only contracts of type")),
          show_past = models.BooleanField(_("past contracts"),default=True),
          show_active = models.BooleanField(_("active contracts"),default=True),
          show_coming = models.BooleanField(_("coming contracts"),default=True),
          today = models.DateField(_("on"),blank=True,default=datetime.date.today),
        )
        params_template = """type show_past show_active show_coming today user"""
        #~ params_panel_hidden = False
        
        #~ master_key = 'user'
        #~ group_by = ['type']
        group_by = ['person__group']
        column_names = 'id applies_from applies_until job person person__city person__national_id person__gender user type *'
        
        @classmethod
        def get_request_queryset(cls,rr):
            #~ logger.info("20120114 param_values = %r",rr.param_values)
            qs = super(ContractsSearch,cls).get_request_queryset(rr)
            #~ user = rr.param_values.get('user',None)
            if rr.param_values.user:
                qs = qs.filter(user=rr.param_values.user)
            if rr.param_values.type:
                qs = qs.filter(type=rr.param_values.type)
            today = rr.param_values.today
            #~ today = rr.param_values.get('today',None) or datetime.date.today()
            #~ show_active = rr.param_values.get('show_active',True)
            if today:
                if not rr.param_values.show_active:
                    flt = range_filter(today,'applies_from','applies_until')
                    #~ logger.info("20120114 flt = %r",flt)
                    qs = qs.exclude(flt)
                #~ show_past = rr.param_values.get('show_past',True)
                if not rr.param_values.show_past:
                    qs = qs.exclude(applies_until__isnull=False,applies_until__lt=today)
                #~ show_coming = rr.param_values.get('show_coming',True)
                if not rr.param_values.show_coming:
                    qs = qs.exclude(applies_from__isnull=False,applies_from__gt=today)
            return qs
            
        def on_group_break(self,group):
            if group == 0:
                yield self.total_line(0)
            else:
                yield self.total_line(group)
                
        def total_line(self,group):
            return 
    


COLS = 8

#~ class JobsOverviewDetail(dd.DetailLayout):
    #~ main = "body"

class JobsOverview(dd.EmptyTable):
    label = _("Contracts Situation") 
    #~ detail_layout = JobsOverviewDetail()
    detail_template = "body"
    
    parameters = dict(
      date = models.DateField(default=datetime.date.today),
      contract_type = models.ForeignKey(ContractType,blank=True,null=True),
      job_type = models.ForeignKey(JobType,blank=True,null=True),
      )
    params_panel_hidden = True

    @dd.displayfield(_("Body"))
    def body(cls,self,ar):
        #~ logger.info("20120221 3 body(%s)",req)
        #~ logger.info("Waiting 5 seconds...")
        #~ time.sleep(5)
        today = self.date or datetime.date.today()
        html = ''
        rows = []
          
        if ar.param_values.job_type:
            jobtypes = [ar.param_values.job_type]
        else:
            jobtypes = JobType.objects.all()
        for jobtype in jobtypes:
            cells = []
            #~ for job in jobtype.job_set.all():
            for job in jobtype.job_set.order_by('provider'):
                actives = []
                candidates = []
                qs = job.contract_set.all()
                if ar.param_values.contract_type:
                    qs = qs.filter(type=ar.param_values.contract_type)
                for ct in qs:
                    if ct.applies_from:
                        until = ct.date_ended or ct.applies_until
                        if not until or (ct.applies_from <= today and until >= today):
                            actives.append(ct)
                for req in job.candidature_set.all():
                    #~ if not req.contract:
                    candidates.append(req)
                if candidates + actives:
                    s = "<p>"
                    s += "<b>%s (%s)</b>" % (
                      cgi.escape(unicode(job)),job.capacity)
                    if job.remark:
                        s += " <i>%s</i>" % cgi.escape(job.remark)
                    s += "</p>"
                    s += UL(['%s bis %s' % (
                      ct.person.last_name.upper(),
                      babel.dtos(ct.applies_until)
                    ) for ct in actives])
                    #~ s += "<li>"
                    #~ for ct in actives:
                        #~ s += '<li>%s</li>' % cgi.escape(unicode(ct.person))
                    #~ s += "</li>"
                    if candidates:
                        s += "<p>%s:</p>" % cgi.escape(unicode(_("Candidates")))
                        s += UL([i.person for i in candidates])
                        #~ for ct in candidates:
                            #~ s += '<br>' + cgi.escape(unicode(ct.person))
                    cells.append(s)
            if cells:
                html += '<h1>%s</h1>' % cgi.escape(unicode(jobtype))
                #~ head = ''.join(['<col width="30" />' for c in cells])
                #~ head = '<colgroup>%s</colgroup>' % head
                s = ''.join(['<td valign="top">%s</td>' % c for c in cells])
                s = '<tr>%s</tr>' % s
                #~ s = head + s
                html += '<table border="1" width="100%%">%s</table>' % s
        html = '<div class="htmlText">%s</div>' % html
        #~ logger.info(html[46:58])
        #~ html = str(html)
        #~ assert type(html) == type('')
        return html


    

if True: # dd.is_installed('contacts') and dd.is_installed('jobs'):
  
    dd.inject_field(Company,
        'is_jobprovider',
        mti.EnableChild('jobs.JobProvider',verbose_name=_("is Job Provider")),
        """Whether this Company is also a Job Provider."""
        )


def setup_main_menu(site,ui,user,m): 
    if user.is_spis:
        m = m.add_menu("jobs",_("Jobs"))
        m.add_action(JobProviders)
        m.add_action(Jobs)
        m.add_action(Offers)
        m.add_action(ContractsSearch)

def setup_my_menu(site,ui,user,m): 
    if user.is_spis:
        m.add_action(MyContracts)
  
def setup_config_menu(site,ui,user,m): 
    if user.is_spis:
        m  = m.add_menu("jobs",_("~Jobs"))
        m.add_action(ContractTypes)
        m.add_action(JobTypes)
        m.add_action(Sectors)
        m.add_action(Functions)
        m.add_action(StudyTypes)
        m.add_action(Schedules)
        m.add_action(Regimes)
            
    
    
  
def setup_explorer_menu(site,ui,user,m):
    if user.is_spis:
        m.add_action(Contracts)
        m.add_action(Candidatures)
        m.add_action(Studies)
