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
        verbose_name = _("Job Provider")
        verbose_name_plural = _('Job Providers')
    

class JobProviders(Companies):
    """
    List of Companies that have `Company.is_jobprovider` activated.
    """
    use_as_default_report = False
    #~ label = _("Job Providers")
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
        verbose_name=_("Job Provider"),
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
            qs = self.person.jobrequest_set.filter(contract=self)
            if qs.count() == 0:
                qs = self.person.jobrequest_set.filter(job=self.job,contract=None)
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
        qs = self.person.jobrequest_set.filter(contract=self)
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
                if self.contact.parent != self.provider.company_ptr:
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
    A work place at some job provider
    """
    
    class Meta:
        verbose_name = _("Job Type")
        verbose_name_plural = _('Job Types')
        
    name = models.CharField(max_length=200,
          blank=True,
          verbose_name=_("Designation"))
          
    def __unicode__(self):
        return unicode(self.name)
        
  
class Job(models.Model):
    """
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
        blank=True,null=True,
        verbose_name=_("Job Provider"))
    
    contract_type = models.ForeignKey(ContractType,blank=True,null=True,
        verbose_name=_("Contract Type"))
    
    hourly_rate = fields.PriceField(_("hourly rate"),blank=True,null=True)
    
    capacity = models.IntegerField(_("capacity"),
        default=1)
        
    remark = models.CharField(max_length=200,
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
        
        
class JobRequest(models.Model):
    class Meta:
        verbose_name = _("Job Requests")
        verbose_name_plural = _('Job Requests')
        
    person = models.ForeignKey("contacts.Person",
        verbose_name=_("Person"))
    
    job = models.ForeignKey("jobs.Job",
        verbose_name=_("Requested Job"))
    
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
                  "Cannot satisfy a JobRequest with a Contract on another  Person")
        super(JobRequest,self).clean(*args,**kw)
    
        
class Jobs(reports.Report):
    model = Job
    #~ order_by = ['start_date']
    column_names = 'name provider * id'

class JobTypes(reports.Report):
    model = JobType
    order_by = ['name']

class JobsByProvider(Jobs):
    fk_name = 'provider'

class JobsByType(Jobs):
    fk_name = 'type'

class JobRequests(reports.Report):
    model = JobRequest
    order_by = ['date_submitted']

class JobRequestsByPerson(JobRequests):
    fk_name = 'person'
    column_names = '* id'

class RequestsByJob(JobRequests):
    fk_name = 'job'
  
    def create_instance(self,req,**kw):
        obj = super(RequestsByJob,self).create_instance(req,**kw)
        if obj.job is not None:
            obj.type = obj.job.type
        return obj
    

COLS = 8

class ContractsSituation(mixins.Listing):
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
            for job in jobtype.job_set.all():
                actives = []
                candidates = []
                for ct in job.contract_set.all():
                    if ct.applies_from:
                        until = ct.date_ended or ct.applies_until
                        if not until or (ct.applies_from <= today and until >= today):
                            actives.append(ct)
                for req in job.jobrequest_set.all():
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
        mti.EnableChild('jobs.JobProvider',verbose_name=_("is Job Provider")),
        """Whether this Company is also a Job Provider."""
        )


def setup_main_menu(site,ui,user,m): 
    m.add_action('jobs.JobProviders')

def setup_my_menu(site,ui,user,m): 
    m.add_action('jobs.MyContracts')
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("jobs",_("~Jobs"))
    m.add_action('jobs.Jobs')
    m.add_action('jobs.ContractTypes')
    m.add_action('jobs.JobTypes')
            
    
    
  
def setup_explorer_menu(site,ui,user,m):
    m.add_action('jobs.Contracts')
