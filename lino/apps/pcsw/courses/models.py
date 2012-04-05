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
This module requires a model `courses.CourseProvider` 
to be defined by the application.
"""


import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation


#~ from lino import reports
from lino import dd
#~ from lino import layouts
from lino.utils import perms
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
from lino.modlib.cal import models as cal
from lino.modlib.users import models as users
from lino.utils.choicelists import HowWell, Gender
from lino.utils.choicelists import ChoiceList
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.models import get_site_config
from lino.tools import get_field
from lino.tools import resolve_field
from lino.tools import range_filter
from lino.utils.babel import DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils.babel import language_choices
#~ from lino.utils.babel import add_babel_field, DEFAULT_LANGUAGE, babelattr, babeldict_getitem
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.tools import obj2str

from lino.modlib.countries.models import CountryCity
#~ from lino.modlib.cal.models import DurationUnit, update_auto_task
from lino.modlib.cal.models import DurationUnit, update_reminder
#~ from lino.modlib.contacts.models import Contact
from lino.tools import resolve_model, UnresolvedModel

from lino.apps.pcsw import models as pcsw

#~ # not used here, but these modules are required in INSTALLED_APPS, 
#~ # and other code may import them using 
#~ # ``from lino.apps.pcsw.models import Property``

#~ from lino.modlib.properties.models import Property
#~ # from lino.modlib.notes.models import NoteType
#~ from lino.modlib.countries.models import Country, City

if settings.LINO.user_model:
    User = resolve_model(settings.LINO.user_model,strict=True)


            
#~ Company = resolve_model('contacts.Company')
class CourseProvider(pcsw.Company):
    """
    A CourseProvider is a Company that offers Courses. 
    """
    class Meta:
        #~ app_label = 'courses'
        verbose_name = _("Course provider")
        verbose_name_plural = _("Course providers")
    #~ name = models.CharField(max_length=200,
          #~ verbose_name=_("Name"))
    #~ company = models.ForeignKey("contacts.Company",blank=True,null=True,verbose_name=_("Company"))
    
dd.inject_field(pcsw.Company,
    'is_courseprovider',
    mti.EnableChild(CourseProvider,verbose_name=_("is Course Provider")),
    """Whether this Company is also a Course Provider."""
    )

    
    
class CourseProviderDetail(pcsw.CompanyDetail):
    """
    This is the same as CompanyDetail, except that we
    
    - remove MTI fields
    - add a new tab "Courses"
    
    """
    box5 = "remarks" 
    main = "general notes CourseOffersByProvider"

  

class CourseProviders(pcsw.Companies):
    """
    List of Companies that have `Company.is_courseprovider` activated.
    """
    #~ hide_details = [Contact]
    #~ use_as_default_table = False
    #~ app_label = 'courses'
    #~ label = _("Course providers")
    model = CourseProvider
    detail_layout = CourseProviderDetail()
    #~ known_values = dict(is_courseprovider=True)
    #~ filter = dict(is_courseprovider__exact=True)
    
    #~ def create_instance(self,req,**kw):
        #~ instance = super(CourseProviders,self).create_instance(req,**kw)
        #~ instance.is_courseprovider = True
        #~ return instance
            





#
# COURSE ENDINGS
#
class CourseEnding(models.Model):
    u"""
    Eine Kursbeendigung ist eine *Art und Weise, wie eine Kursanfrage beendet wurde*.
    Später können wir dann Statistiken machen, wieviele Anfragen auf welche Art und 
    Weise beendet wurden.
    """
    class Meta:
        verbose_name = _("Course Ending")
        verbose_name_plural = _('Course Endings')
        
    name = models.CharField(_("designation"),max_length=200)
    
    def __unicode__(self):
        return unicode(self.name)
        
class CourseEndings(dd.Table):
    model = CourseEnding
    column_names = 'name *'
    order_by = ['name']

  
class CourseContent(models.Model):
    u"""
    Ein Kursinhalt (z.B. "Französisch", "Deutsch", "Alphabétisation",...)
    """
    
    class Meta:
        verbose_name = _("Course Content")
        verbose_name_plural = _('Course Contents')
        
    name = models.CharField(max_length=200,
          blank=True,# null=True,
          verbose_name=_("Name"))
    u"""
    Bezeichnung des Kursinhalts (nach Konvention des DSBE).
    """
          
    def __unicode__(self):
        return unicode(self.name)
        
  
class CourseOffer(models.Model):
    """
    """
    class Meta:
        verbose_name = _("Course Offer")
        verbose_name_plural = _('Course Offers')
        
    title = models.CharField(max_length=200,
        verbose_name=_("Name"))
    u"""
    Der Titel des Kurses. Maximal 200 Zeichen.
    """
    
    content = models.ForeignKey("courses.CourseContent",
        verbose_name=_("Course content"))
    """
    Der Inhalt des Kurses (ein :class:`CourseContent`)
    """
    
    provider = models.ForeignKey('courses.CourseProvider')
    #~ provider = models.ForeignKey(CourseProvider,
        #~ verbose_name=_("Course provider"))
    #~ """
    #~ Der Kursanbieter (eine :class:`Company`)
    #~ """
    
    description = dd.RichTextField(_("Description"),blank=True,format='html')
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title,self.provider)
        
    #~ @chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().data_iterator
        
    #~ @classmethod
    #~ def setup_report(model,rpt):
        #~ rpt.add_action(DirectPrintAction('candidates',_("List of candidates"),'candidates'))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return DEFAULT_LANGUAGE
        
        
    
class Course(models.Model,mixins.Printable):
    u"""
    Ein konkreter Kurs, der an einem bestimmten Datum beginnt.
    Für jeden Kurs muss ein entsprechendes Angebot existieren, 
    das u.A. den :class:`Kursinhalt <CourseContent>` 
    und :class:`Kursanbieter <CourseProvider>` 
    detailliert. Also selbst für einen einmalig stattfindenden 
    Kurs muss ein Angebot erstellt werden.
    """
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')
        
        
    offer = models.ForeignKey("courses.CourseOffer")
    
    title = models.CharField(max_length=200,
        blank=True,
        verbose_name=_("Name"))
        
    start_date = models.DateField(_("start date"))
    
    #~ content = models.ForeignKey("courses.CourseContent",verbose_name=_("Course content"))
  
    remark = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung über diesen konkreten Kurs. Maximal 200 Zeichen.
    """
        
    def __unicode__(self):
        #~ s = u"%s %s (%s)" % (self._meta.verbose_name,self.pk,babel.dtos(self.start_date))
        s = babel.dtos(self.start_date)
        if self.title:
            s += " " + self.title
        if self.offer:
            s += " " + unicode(self.offer)
        return s
  
    @classmethod
    def setup_report(model,rpt):
        rpt.add_action(DirectPrintAction(rpt,'candidates',_("List of candidates"),'candidates'))
        rpt.add_action(DirectPrintAction(rpt,'participants',_("List of participants"),'participants'))
        
    def get_print_language(self,pm):
        "Used by DirectPrintAction"
        return DEFAULT_LANGUAGE
        
    def participants(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen, 
        die in diesem Kurs eingetragen sind. 
        """
        return ParticipantsByCourse.request(master_instance=self).data_iterator
        
    def candidates(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen, 
        die noch in keinem Kurs eingetragen sind, aber für diesen Kurs in Frage 
        kommen. 
        """
        return CandidatesByCourse.request(master_instance=self).data_iterator
        
        
class CourseRequest(models.Model):
    """
    A Course Request is created when a certain Person expresses her 
    wish to participate in a Course with a certain CourseContent.
    """
    class Meta:
        verbose_name = _("Course Requests")
        verbose_name_plural = _('Course Requests')
        
    #~ person = models.ForeignKey("contacts.Person",
    person = models.ForeignKey(settings.LINO.person_model,
        verbose_name=_("Person"),
        help_text=u"Die Person, die die Anfrage macht.")
    
    offer = models.ForeignKey("courses.CourseOffer",blank=True,null=True)
    
    content = models.ForeignKey("courses.CourseContent",
        verbose_name=_("Course content"),
        help_text=u"Der gewünschte Kursinhalt (ein Objekt vom Typ :class:`CourseConent`.)")
    
    #~ date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    date_submitted = models.DateField(_("date submitted"),
        help_text=u"Das Datum, an dem die Anfrage erstellt wurde.")
    
    urgent = models.BooleanField(_("Needed for job search"),
        default=False,
        help_text=u"Ankreuzen, wenn der Kurs für die Arbeitssuche benötigt wird.")
    
    #~ """Empty means 'any provider'
    #~ """
    #~ provider = models.ForeignKey(CourseProvider,blank=True,null=True,
        #~ verbose_name=_("Course provider"))
        
    #~ @chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().queryset
        
    course = models.ForeignKey("courses.Course",blank=True,null=True,
        verbose_name=_("Course found"))
    u"""
    Der Kurs, durch den diese Anfrage befriedigt wurde.
    So lange dieses Feld leer ist, gilt die Anfrage als offen.
    """
        
    #~ """
    #~ The person's feedback about how satisfied she was.
    #~ """
    #~ satisfied = StrengthField(verbose_name=_("Satisfied"),blank=True,null=True)
    
    #~ remark = models.CharField(max_length=200,
    remark = models.TextField(
        blank=True,null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung zu dieser konkreten Kursanfrage oder -teilnahme.
    """
        
    date_ended = models.DateField(blank=True,null=True,verbose_name=_("date ended"))
    u"""
    Datum der effektives Beendigung dieser Kursteilname.
    """
    
    ending = models.ForeignKey("courses.CourseEnding",blank=True,null=True,
        verbose_name=_("Ending"))
    u"""
    Die Art der Beendigung 
    (ein Objekt vom Typ :class:`CourseEnding`.)
    Das wird benutzt für spätere Statistiken.
    """
    
    def save(self,*args,**kw):
        if self.offer and self.offer.content:
            self.content = self.offer.content
        super(CourseRequest,self).save(*args,**kw)
        
    @chooser()
    def offer_choices(cls,content):
        if content:
            return CourseOffer.objects.filter(content=content)
        return CourseOffer.objects.all()
        
    
    def on_create(self,req):
        self.date_submitted = datetime.date.today()
    
        
class Courses(dd.Table):
    model = Course
    order_by = ['start_date']
    detail_template = """
    id:8 start_date offer title 
    remark
    courses.ParticipantsByCourse
    courses.CandidatesByCourse
    """
    
class CoursesByOffer(Courses):
    master_key = 'offer'
    column_names = 'start_date * id'

class CourseContents(dd.Table):
    model = CourseContent
    order_by = ['name']

class CourseOffers(dd.Table):
    model = CourseOffer
    detail_template = """
    id:8 title content provider
    description
    CoursesByOffer
    """
    
class CourseOffersByProvider(CourseOffers):
    master_key = 'provider'

class CourseRequests(dd.Table):
    model = CourseRequest
    
    detail_template = """
    date_submitted person content offer urgent 
    course date_ended ending id:8 
    remark  uploads.UploadsByOwner
    """
    
    order_by = ['date_submitted']
    active_fields = ['offer']

class CourseRequestsByPerson(CourseRequests):
    master_key = 'person'
    column_names = 'date_submitted:10 content:15 offer:15 course:20 * id'

class RequestsByCourse(CourseRequests):
    master_key = 'course'
  
    @classmethod
    def create_instance(self,req,**kw):
        obj = super(RequestsByCourse,self).create_instance(req,**kw)
        if obj.course is not None:
            obj.content = obj.course.offer.content
        return obj
    
class RegisterCandidate(dd.RowAction):
    """
    Register the given :class:`Candidate` for the given :class:`Course`.
    This action is available on a row of :class:`CandidatesByCourse`.
    """
    label = _("Register")
    name = "register"
    def run(self,rr,elem):
        elem.course = rr.master_instance
        elem.save()
        return rr.ui.success_response(refresh_all=True,
          message=_("%(person)s has been registered to %(course)s") % dict(
              person=elem.person,course=elem.course))

class UnregisterCandidate(dd.RowAction):
    """
    Unregister the given :class:`Candidate` for the given :class:`Course`.
    This action is available on a row of :class:`ParticipantsByCourse`.
    """
    label = _("Unregister")
    name = "unregister"
    def run(self,rr,elem):
        course = elem.course
        elem.course = None
        elem.save()
        return rr.ui.success_response(refresh_all=True,
          message=_("%(person)s has been unregistered from %(course)s") % dict(person=elem.person,course=course))

class ParticipantsByCourse(RequestsByCourse):
    """
    List of participating :class:`Candidates <Candidate>` for the given :class:`Course`.
    """
    label = _("Participants")
    column_names = 'person remark date_ended ending'
    
    @classmethod
    def setup_actions(self):
        self.add_action(UnregisterCandidate())

class CandidatesByCourse(RequestsByCourse):
    """
    List of :class:`Candidates <Candidate>` for the given :class:`Course`
    which are not registiered.
    """
    label = _("Candidates")
    column_names = 'person remark content date_submitted'
    #~ can_add = perms.never
    
    @classmethod
    def setup_actions(self):
        self.add_action(RegisterCandidate())
    
    @classmethod
    def get_request_queryset(self,rr):
        if rr.master_instance is None:
            return []
        return self.model.objects.filter(course__isnull=True,
            content__exact=rr.master_instance.offer.content)
    
    @classmethod
    def create_instance(self,req,**kw):
        """Manually clear the `course` field.
        """
        obj = super(CandidatesByCourse,self).create_instance(req,**kw)
        obj.course = None
        return obj

