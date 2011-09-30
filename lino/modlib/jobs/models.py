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
See also :doc:`/dsbe/models`.

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

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation





from lino import reports
#~ from lino import layouts
from lino.utils import perms
from lino.utils import dblogger
#~ from lino.utils import printable
from lino import mixins
from lino import actions
from lino import fields
from lino.modlib.contacts import models as contacts
#~ from lino.modlib.contacts.models import SEX_CHOICES
from lino.modlib.notes import models as notes
from lino.modlib.links import models as links
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
from lino.mixins.printable import DirectPrintAction
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.cal.models import DurationUnit, update_auto_task

# not used here, but these modules are required in INSTALLED_APPS, 
# and other code may import them using 
# ``from lino.apps.dsbe.models import Property``

from lino.modlib.properties.models import Property
from lino.modlib.notes.models import NoteType
from lino.modlib.countries.models import Country, City
from lino.modlib.isip.models import ContractBase
from lino.apps.dsbe.models import Company, Companies


SCHEDULE_CHOICES = {
    'de':[ 
        u"5-Tage-Woche",
        u"Montag, Mittwoch, Freitag",
        u"Individuell",
        ],
    'fr':[ 
        u"5 jours/semaine",
        u"lundi,mercredi,vendredi",
        u"individuel",
        ],
    'en':[
        u"5 days/week",
        u"Monday, Wednesday, Friday",
        u"Individual",
        ]
}

REGIME_CHOICES = {
    'de':[ 
        u"20 Stunden/Woche",
        u"35 Stunden/Woche",
        u"38 Stunden/Woche",
        ],
    'fr':[ 
        u"20 heures/semaine",
        u"35 heures/semaine",
        u"38 heures/semaine",
        ],
    'en':[
        u"20 hours/week",
        u"35 hours/week",
        u"38 hours/week",
        u"38 hours/week",
        ]
}





class JobProvider(Company):
    """Stellenanbieter (BISA, BW, ...) 
    """
    class Meta:
        app_label = 'jobs'
        verbose_name = _("Employer")
        verbose_name_plural = _('Employers')
    

class JobProviders(Companies):
    """
    List of Companies that have `Company.is_jobprovider` activated.
    """
    use_as_default_report = False
    model = JobProvider
    app_label = 'jobs'
  


#
# CONTRACT TYPES 
#
class ContractType(mixins.PrintableType,babel.BabelNamed):
  
    templates_group = 'jobs/Contract'
    
    class Meta:
        verbose_name = _("Job Contract Type")
        verbose_name_plural = _('Job Contract Types')
        
    ref = models.CharField(_("reference"),max_length=20,blank=True)

class ContractTypes(reports.Report):
    model = ContractType
    column_names = 'name ref build_method template *'


class Sector(babel.BabelNamed):
    """Each Job should have an "Activity Sector"."""
    class Meta:
        verbose_name = _("Job Sector")
        verbose_name_plural = _('Job Sectors')
        
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
class Sectors(reports.Report):
    model = Sector

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
class Functions(reports.Report):
    model = Function
    
class FunctionsBySector(Functions):
    fk_name = 'sector'

#
# JOB CONTRACTS
# 
class Contract(ContractBase):
    """
    A Contract
    """
    class Meta:
        verbose_name = _("Job Contract")
        verbose_name_plural = _('Job Contracts')
        
    type = models.ForeignKey("jobs.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        verbose_name=_("Contract Type"),blank=True)
    
    provider = models.ForeignKey(JobProvider,
        related_name="%(app_label)s_%(class)s_set_by_provider",
        verbose_name=_("Employer"),
        blank=True,null=True)
    job = models.ForeignKey("jobs.Job",
        verbose_name=_("Job"),
        blank=True,null=True)
        
    duration = models.IntegerField(_("duration (days)"),
        blank=True,null=True,default=None)
    
    
    regime = models.CharField(_("regime"),max_length=200,blank=True)
    schedule = models.CharField(_("schedule"),max_length=200,blank=True)
    hourly_rate = fields.PriceField(_("hourly rate"),blank=True,null=True)
    refund_rate = models.CharField(_("refund rate"),max_length=200,
        blank=True)
    
    reference_person = models.CharField(_("reference person"),max_length=200,
        blank=True)
        
    responsibilities = fields.RichTextField(_("responsibilities"),
        blank=True,null=True,format='html')
    
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
    
    #~ aid_nature = models.CharField(_("aid nature"),max_length=100,blank=True)
    #~ aid_rate = models.CharField(_("aid rate"),max_length=100,blank=True)
    
    @chooser()
    def contact_choices(cls,provider):
        if provider is not None:
            return provider.rolesbyparent.all()
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
    
    @chooser(simple_values=True)
    def regime_choices(cls,language):
        return language_choices(language,REGIME_CHOICES)
    
    @chooser(simple_values=True)
    def schedule_choices(cls,language):
        return language_choices(language,SCHEDULE_CHOICES)
    
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
        if self.must_build:
            return df
        #~ return df + settings.LINO.CONTRACT_PRINTABLE_FIELDS
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
        
    def save(self,*args,**kw):
        #~ self.before_save()
        if self.job_id is not None:
            qs = self.person.candidature_set.filter(contract=self)
            if qs.count() == 0:
                qs = self.person.candidature_set.filter(job=self.job,contract=None)
                if qs.count() == 1: 
                    obj = qs[0]
                    obj.contract = self
                    obj.save()
                    dblogger.info(u'Marked job request %s as satisfied by %s' % (
                      obj,self))
        r = super(Contract,self).save(*args,**kw)
        return r
        
    def data_control(self):
        "Used by :class:`lino.models.DataControlListing`."
        msgs = []
        qs = self.person.candidature_set.filter(contract=self)
        if qs.count() > 1: 
            msgs.append(
              u'There are more than one job request using contract %s : %s' \
              % qs)
        return msgs
        
    def full_clean(self,*args,**kw):
        if self.person_id is not None:
            #~ if not self.user_asd:
                #~ if self.person.user != self.user:
                    #~ self.user_asd = self.person.user
            if self.person.birth_date and self.applies_from:
                def duration(refdate):
                    if type(refdate) != datetime.date:
                        raise Exception("%r is not a date!" % refdate)
                    delta = refdate - self.person.birth_date
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
                if self.contact.parent.pk != self.provider.company_ptr.pk:
                    self.contact = None
                    
        super(Contract,self).full_clean(*args,**kw)
        
    @classmethod
    def site_setup(cls,lino):
        """
        Here's how to override the default verbose_name of a field.
        """
        Contract.user.verbose_name=_("responsible (DSBE)")
        #~ resolve_field('jobs.Contract.user').verbose_name=_("responsible (DSBE)")
        #~ lino.CONTRACT_PRINTABLE_FIELDS = reports.fields_list(cls,
        cls.PRINTABLE_FIELDS = reports.fields_list(cls,
            'person job provider contact type '
            'applies_from applies_until duration '
            'language schedule regime hourly_rate refund_rate '
            'reference_person responsibilities '
            'user user_asd exam_policy '
            'date_decided date_issued ')
        #~ super(Contract,cls).site_setup(lino)

class Contracts(reports.Report):
    model = Contract
    column_names = 'id job applies_from applies_until user type *'
    order_by = ['id']
    active_fields = 'job provider contact'.split()
    
class ContractsByPerson(Contracts):
    fk_name = 'person'
    column_names = 'job applies_from applies_until user type *'

        
class ContractsByProvider(Contracts):
    fk_name = 'provider'
    column_names = 'person job applies_from applies_until user type *'

class ContractsByType(Contracts):
    fk_name = 'type'
    column_names = "applies_from person job user *"
    order_by = ["applies_from"]

class ContractsByJob(Contracts):
    column_names = 'person applies_from applies_until user type *'
    fk_name = 'job'

class MyContracts(mixins.ByUser,Contracts):
    column_names = "applies_from person job *"
    label = _("My contracts")
    #~ order_by = "reminder_date"
    #~ column_names = "reminder_date person company *"
    order_by = ["applies_from"]
    #~ filter = dict(reminder_date__isnull=False)




class JobType(mixins.Sequenced):
    """
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
  
class Offers(reports.Report):
    model = Offer
    
    
    
#
# STUDY TYPE
#
class StudyType(babel.BabelNamed):
    #~ text = models.TextField(_("Description"),blank=True,null=True)
    class Meta:
        verbose_name = _("study type")
        verbose_name_plural = _("study types")

class StudyTypes(reports.Report):
    #~ label = _('Study types')
    model = StudyType
    order_by = ["name"]


class HistoryByPerson(reports.Report):
    fk_name = 'person'
    order_by = ["started"]
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
    person = models.ForeignKey("contacts.Person") #,verbose_name=_("Person"))
    type = models.ForeignKey(StudyType,verbose_name=_("Study type"))
    content = models.CharField(max_length=200,
        blank=True, # null=True,
        verbose_name=_("Study content"))
    #~ content = models.ForeignKey(StudyContent,blank=True,null=True,verbose_name=_("Study content"))
  
    started = fields.MonthField(_("started"),blank=True,null=True)
    stopped = fields.MonthField(_("stopped"),blank=True,null=True)
    #~ started = models.DateField(blank=True,null=True,verbose_name=_("started"))
    #~ stopped = models.DateField(blank=True,null=True,verbose_name=_("stopped"))
    #~ started = fields.MonthField(blank=True,null=True,verbose_name=_("started"))
    #~ stopped = fields.MonthField(blank=True,null=True,verbose_name=_("stopped"))
    success = models.BooleanField(verbose_name=_("Success"),default=False)
    language = models.ForeignKey("countries.Language",
        blank=True,null=True,verbose_name=_("Language"))
    #~ language = fields.LanguageField(blank=True,null=True,verbose_name=_("Language"))
    
    school = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("School"))
    #~ school = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("School"))
    
    remarks = models.TextField(blank=True,null=True,verbose_name=_("Remarks"))
    
    def __unicode__(self):
        return unicode(self.type)
  
        
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
    person = models.ForeignKey("contacts.Person",verbose_name=_("Person"))
    #~ company = models.ForeignKey("contacts.Company",verbose_name=_("Company"))
    company = models.CharField(max_length=200,verbose_name=_("company"))
    #~ type = models.ForeignKey(JobType,verbose_name=_("job type"))
    title = models.CharField(max_length=200,verbose_name=_("job title"),blank=True)
    country = models.ForeignKey("countries.Country",
        blank=True,null=True,
        verbose_name=_("Country"))
  
    started = fields.MonthField(_("started"),blank=True,null=True)
    stopped = fields.MonthField(_("stopped"),blank=True,null=True)
    
    remarks = models.TextField(blank=True,null=True,verbose_name=_("Remarks"))
    
    def __unicode__(self):
        return unicode(self.title)
  
class Experiences(reports.Report):
    model = Experience
  
class ExperiencesByFunction(Experiences):
    fk_name = 'function'
    order_by = ["started"]

    
class ExperiencesByPerson(Experiences,HistoryByPerson):
    "List of job experiences for a known person"
    model = Experience
    
  
    
    

#~ class Job(SectorFunction):
class Job(models.Model):
    """
    A work place at some employer
    """
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
    
    hourly_rate = fields.PriceField(_("hourly rate"),blank=True,null=True)
    
    capacity = models.IntegerField(_("capacity"),
        default=1)
        
    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))
        
    def __unicode__(self):
        return self.name
        #~ return u'%s @ %s' % (self.name,self.provider)
  
    def disabled_fields(self,request):
        #~ if self.contract_set.count():
        if self.contract_set.filter(must_build=False).count():
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
        
        
class Wish(SectorFunction):
    class Meta:
        verbose_name = _("Job Wish")
        verbose_name_plural = _('Job Wishes')
    person = models.ForeignKey("contacts.Person")
    
class Wishes(reports.Report):
    model = Wish
    
class WishesByPerson(Wishes):
    fk_name = 'person'

class WishesBySector(Wishes):
    fk_name = 'sector'

class WishesByFunction(Wishes):
    fk_name = 'function'


class WishesByOffer(reports.Report):
    """
    Shows the persons that whish this Offer.
    
    It is a slave report without 
    :attr:`fk_name <lino.reports.Report.fk_name>`,
    which is allowed only because it also overrides
    :meth:`get_request_queryset`
    """
  
    model = Wish
    master = Offer
    label = _("Candidate Job Wishes")
    
    can_add = perms.never
    can_change = perms.never
    
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

    

class Candidature(models.Model):
    class Meta:
        verbose_name = _("Job Candidature")
        verbose_name_plural = _('Job Candidatures')
        
    person = models.ForeignKey("contacts.Person")
    
    job = models.ForeignKey("jobs.Job",
        blank=True,null=True)
        #~ verbose_name=_("Requested Job"))
    
    date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    u"Das Datum, an dem die Anfrage erstellt wurde."
    
    contract = models.ForeignKey("jobs.Contract",blank=True,null=True,
        verbose_name=_("Contract found"))
    u"""
    Der Vertrag, durch den diese Anfrage befriedigt wurde 
    (ein Objekt vom Typ :class:`Contract`).
    So lange dieses Feld leer ist, gilt die Anfrage als offen.
    """
        
    remark = models.TextField(
        blank=True,null=True,
        verbose_name=_("Remark"))
        
    def __unicode__(self):
        return force_unicode(_('%(job)s request by %(person)s') % dict(
            job=self.job.name,
            person=self.person.get_full_name(salutation=False)))
            
    @chooser()
    def contract_choices(cls,job,person):
        if person and job:
            return person.contract_set.filter(job=job)
        return []
        
    def clean(self,*args,**kw):
        if self.contract:
            if self.contract.person != self.person:
                raise ValidationError(
                  "Cannot satisfy a Candidature with a Contract on another Person")
        super(Candidature,self).clean(*args,**kw)
    



class Jobs(reports.Report):
    model = Job
    #~ order_by = ['start_date']
    column_names = 'name provider * id'

class JobTypes(reports.Report):
    model = JobType
    order_by = ['name']

class JobsByProvider(Jobs):
    fk_name = 'provider'

#~ class JobsByFunction(Jobs):
    #~ fk_name = 'function'

#~ class JobsBySector(Jobs):
    #~ fk_name = 'sector'

class JobsByType(Jobs):
    fk_name = 'type'

class Candidatures(reports.Report):
    model = Candidature
    order_by = ['date_submitted']
    column_names = '* id'

class CandidaturesByPerson(Candidatures):
    fk_name = 'person'

class CandidaturesByJob(Candidatures):
    fk_name = 'job'
  
    def create_instance(self,req,**kw):
        obj = super(RequestsByJob,self).create_instance(req,**kw)
        if obj.job is not None:
            obj.type = obj.job.type
        return obj
    

COLS = 8

class new_ContractsSituation(mixins.Listing):
    class Meta:
        verbose_name = _("Contracts Situation") 
        
    contract_type = models.ForeignKey(ContractType,blank=True,null=True)
    job_type = models.ForeignKey(JobType,blank=True,null=True)
    
    def body(self):
        today = self.date or datetime.date.today()
        html = ''
        rows = []
          
        for jobtype in JobType.objects.all():
            providers = [] # (obj, jobs)
            #~ for job in jobtype.job_set.all():
            for job in jobtype.job_set.order_by('provider'):
                actives = []
                candidates = []
                for ct in job.contract_set.all():
                    if ct.applies_from:
                        until = ct.date_ended or ct.applies_until
                        if not until or (ct.applies_from <= today and until >= today):
                            actives.append(ct)
                for req in job.candidature_set.all():
                    if not req.contract:
                        candidates.append(req)
                if candidates + actives:
                    s = "<p>"
                    s += "<b>%s (%s)</b>" % (
                      cgi.escape(unicode(job)),job.capacity)
                    if job.remark:
                        s += " <i>%s</i>" % cgi.escape(job.remark)
                    s += "</p>"
                    s += UL([u'%s bis %s' % (
                      ct.person.last_name.upper(),
                      babel.dtos(ct.applies_until)
                    ) for ct in actives])
                    #~ s += "<li>"
                    #~ for ct in actives:
                        #~ s += '<li>%s</li>' % cgi.escape(unicode(ct.person))
                    #~ s += "</li>"
                    if candidates:
                        s += "<p>%s:</p>" % cgi.escape(_("Candidates"))
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
        return html

class ContractsSituation(mixins.Listing):
    template_name = 'Listing-Landscape.odt'
    class Meta:
        verbose_name = _("Contracts Situation") 
        
    contract_type = models.ForeignKey(ContractType,blank=True,null=True)
    job_type = models.ForeignKey(JobType,blank=True,null=True)
    
    def body(self):
        today = self.date or datetime.date.today()
        html = ''
        rows = []
          
        for jobtype in JobType.objects.all():
            cells = []
            #~ for job in jobtype.job_set.all():
            for job in jobtype.job_set.order_by('provider'):
                actives = []
                candidates = []
                for ct in job.contract_set.all():
                    if ct.applies_from:
                        until = ct.date_ended or ct.applies_until
                        if not until or (ct.applies_from <= today and until >= today):
                            actives.append(ct)
                for req in job.candidature_set.all():
                    if not req.contract:
                        candidates.append(req)
                if candidates + actives:
                    s = "<p>"
                    s += "<b>%s (%s)</b>" % (
                      cgi.escape(unicode(job)),job.capacity)
                    if job.remark:
                        s += " <i>%s</i>" % cgi.escape(job.remark)
                    s += "</p>"
                    s += UL([u'%s bis %s' % (
                      ct.person.last_name.upper(),
                      babel.dtos(ct.applies_until)
                    ) for ct in actives])
                    #~ s += "<li>"
                    #~ for ct in actives:
                        #~ s += '<li>%s</li>' % cgi.escape(unicode(ct.person))
                    #~ s += "</li>"
                    if candidates:
                        s += "<p>%s:</p>" % cgi.escape(_("Candidates"))
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
        return html


if reports.is_installed('contacts') and reports.is_installed('jobs'):
  
    reports.inject_field(Company,
        'is_jobprovider',
        mti.EnableChild('jobs.JobProvider',verbose_name=_("is Employer")),
        """Whether this Company is also an Employer."""
        )


def setup_main_menu(site,ui,user,m): 
    m.add_action('jobs.JobProviders')
    m.add_action('jobs.Offers')

def setup_my_menu(site,ui,user,m): 
    m.add_action('jobs.MyContracts')
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("jobs",_("~Jobs"))
    m.add_action('jobs.Jobs')
    m.add_action('jobs.ContractTypes')
    m.add_action('jobs.JobTypes')
    m.add_action('jobs.Sectors')
    m.add_action('jobs.Functions')
    m.add_action('jobs.StudyTypes')
            
    
    
  
def setup_explorer_menu(site,ui,user,m):
    m.add_action('jobs.Contracts')
    m.add_action('jobs.Candidatures')
    m.add_action('jobs.Wishes')
