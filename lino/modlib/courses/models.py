# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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

from __future__ import unicode_literals

"""
The :xfile:`models.py` module for the :mod:`lino.modlib.courses` app.
"""


#~ print '20130219 lino.modlib.courses 1'  


import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime
from decimal import Decimal
ZERO = Decimal()
ONE = Decimal(1)

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy

from django.contrib.contenttypes.models import ContentType

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation


#~ from lino import reports
from lino import dd
#~ from lino import layouts
#~ from lino.utils import printable
from lino import mixins
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.core.dbutils import obj2str

from north.dbutils import day_and_month


users = dd.resolve_app('users')
cal = dd.resolve_app('cal')
sales = dd.resolve_app('sales')
contacts = dd.resolve_app('contacts')
#~ Company = dd.resolve_model('contacts.Company',strict=True)
#~ print '20130219 lino.modlib.courses 2'  

"""
Here we must use `resolve_model` with `strict=True`
because we want the concrete model 
and we don't know whether it is overridden
by this application.
"""
Person = dd.resolve_model('contacts.Person',strict=True)
# equivalent alternative :
#~ Person = settings.SITE.modules.contacts.Person

#~ from lino.modlib.contacts.models import Person
#~ print '20130219 lino.modlib.courses 3'  

#~ except ImportError as e:
    #~ import traceback
    #~ traceback.print_exc(e)
    #~ raise Exception("20130607")

#~ class PresenceStatus(dd.BabelNamed):
    #~ class Meta:
        #~ verbose_name = _("Presence Status")
        #~ verbose_name_plural = _("Presence Statuses")
        
#~ class PresenceStatuses(dd.Table):
    #~ model = PresenceStatus
    
class StartEndTime(dd.Model):
    class Meta:
        abstract = True
    start_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start Time"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End Time"))
    
 
class Slot(mixins.Sequenced,StartEndTime):
    """
    """
    class Meta:
        verbose_name = _("Timetable Slot") # Zeitnische
        verbose_name_plural = _('Timetable Slots')
        
    name = models.CharField(max_length=200,
          blank=True,
          verbose_name=_("Name"))
  
    def __unicode__(self):
        return self.name or "%s-%s" % (self.start_time,self.end_time)
        
class Slots(dd.Table):
    model = Slot
    required = dd.required(user_level='manager')
    insert_layout = """
    start_time end_time 
    name
    """
    detail_layout = """
    name start_time end_time 
    courses.CoursesBySlot
    """
    
    
class Topic(dd.BabelNamed,dd.Printable):
    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _('Topics')
        
class Topics(dd.Table):
    model = Topic
    required = dd.required(user_level='manager')
    detail_layout = """
    id name
    courses.LinesByTopic
    courses.CoursesByTopic
    """
    
class Line(dd.BabelNamed):
    class Meta:
        verbose_name = _("Course Line")
        verbose_name_plural = _('Course Lines')
    topic = models.ForeignKey(Topic,blank=True,null=True)
    description = dd.BabelTextField(_("Description"),blank=True)
    
    #~ def __unicode__(self):
        #~ return "%s (%s)" % (dd.BabelNamed.__unicode__(self),self.topic)
          
        
class Lines(dd.Table):
    model = Line
    required = dd.required(user_level='manager')
    detail_layout = """
    id name
    description
    courses.CoursesByLine
    """
    
class LinesByTopic(Lines):
    master_key = "topic"


class TeacherType(dd.BabelNamed,dd.Printable):
    class Meta:
        verbose_name = _("Teacher type")
        verbose_name_plural = _('Teacher types')
        
class TeacherTypes(dd.Table):
    model = TeacherType
    required = dd.required(user_level='manager')
    detail_layout = """
    id name
    courses.TeachersByType
    """



class Teacher(Person):
    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        
    teacher_type = dd.ForeignKey('courses.TeacherType',blank=True,null=True)
    
    def __unicode__(self):
        #~ return self.get_full_name(salutation=False)
        return self.last_name
      
class TeacherDetail(contacts.PersonDetail):
    general = dd.Panel(contacts.PersonDetail.main,label = _("General"))
    box5 = "remarks" 
    main = "general courses.CoursesByTeacher courses.EventsByTeacher cal.GuestsByPartner"

    #~ def setup_handle(self,lh):
      
        #~ lh.general.label = _("General")
        #~ lh.notes.label = _("Notes")

class Teachers(contacts.Persons):
    model = Teacher
    #~ detail_layout = TeacherDetail()
  
class TeachersByType(Teachers):
    master_key = 'teacher_type'



class PupilType(dd.BabelNamed,dd.Printable):
    class Meta:
        verbose_name = _("Pupil type")
        verbose_name_plural = _('Pupil types')
        
class PupilTypes(dd.Table):
    model = PupilType
    required = dd.required(user_level='manager')
    detail_layout = """
    id name
    courses.PupilsByType
    """



class Pupil(Person):
    class Meta:
        #~ app_label = 'courses'
        verbose_name = _("Pupil")
        verbose_name_plural = _("Pupils")
        
    pupil_type = dd.ForeignKey('courses.PupilType',blank=True,null=True)
    
class PupilDetail(contacts.PersonDetail):
    main = "general courses.EnrolmentsByPupil"

    general = dd.Panel(contacts.PersonDetail.main,label = _("General"))
    box5 = "remarks" 
    
    #~ pupil = dd.Panel("""
    #~ EnrolmentsByPupil
    #~ """,label = _("Pupil"))
    
    #~ def setup_handle(self,lh):
      
        #~ lh.general.label = _("General")
        #~ lh.courses.label = _("School")
        #~ lh.notes.label = _("Notes")

class Pupils(contacts.Persons):
    model = Pupil
    #~ detail_layout = PupilDetail()

class PupilsByType(Pupils):
    master_key = 'pupil_type'


    
class EventsByTeacher(cal.Events):
    help_text = _("Shows events of courses of this teacher")
    master = Teacher
    column_names = 'when_text:20 project__line room state'
    auto_fit_column_widths = True
    
    @classmethod
    def get_request_queryset(self,ar):
        teacher = ar.master_instance
        if teacher is None: return []
        qs = super(EventsByTeacher,self).get_request_queryset(ar)
        qs = qs.filter(project__in = teacher.course_set.all())
        return qs
  
#~ def on_event_generated(self,course,ev):
def unused_setup_course_event(self,course,ev):
    if not course.slot: 
        return
    if not ev.start_date: 
        #~ raise Exception("20120403 %s" % obj2str(ev))
        return
        
    ev.start_time = course.slot.start_time
    ev.end_time = course.slot.end_time
    
    #~ start_time = datetime.time(16)
    #~ skip = datetime.timedelta(minutes=60)
    #~ if wd in (1,2,4,5):
        #~ pass
    #~ elif wd == 3:
        #~ start_time = datetime.time(13)
    #~ else:
        #~ return
    #~ start_time = datetime.datetime.combine(ev.start_date,start_time)
    #~ start_time = start_time + skip * (course.slot - 1)
    #~ ev.set_datetime('start',start_time)
    #~ ev.set_datetime('end',start_time + skip)

#~ if not hasattr(settings.SITE,'setup_course_event'):
    #~ settings.SITE.__class__.setup_course_event = setup_course_event
    
    
class CourseStates(dd.Workflow):
    required = dd.required(user_level='admin')

add = CourseStates.add_item
add('10', _("Draft"),'draft')
add('20', _("Published"),'published')
add('30', _("Started"),'started')
add('40', _("Ended"),'ended')
add('50', _("Cancelled"),'cancelled')
    
    
    
#~ class Course(StartEndTime,cal.EventGenerator,cal.RecurrenceSet,mixins.Printable):
class Course(contacts.ContactRelated,cal.EventGenerator,cal.RecurrenceSet,dd.Printable):
    """
    A Course is a group of pupils that regularily 
    meet with a given teacher in a given room.
    """
    
    FILL_EVENT_GUESTS = False
    
    class Meta:
        abstract = settings.SITE.is_abstract_model('courses.Course')
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')
        
    workflow_state_field = 'state'
    
    line = models.ForeignKey('courses.Line')
    teacher = models.ForeignKey(Teacher,blank=True,null=True)
    #~ room = models.ForeignKey(Room,blank=True,null=True)
    room = dd.ForeignKey('cal.Room',blank=True,null=True)
    slot = models.ForeignKey(Slot,blank=True,null=True)
    
    #~ price = dd.PriceField(verbose_name=_("Price"),blank=True,null=True)
    
    state = CourseStates.field(default=CourseStates.draft)
    
    max_places = models.PositiveIntegerField(
        pgettext("in a course","Places"),
        help_text=("Maximal number of participants"),
        blank=True,null=True)
        
    #~ slot = models.PositiveSmallIntegerField(_("Time slot"),
        #~ blank=True,null=True)
        
        
    tariff = dd.ForeignKey('products.Product',
        blank=True,null=True,
        verbose_name=_("Tariff"),
        related_name='courses_by_tariff')
        
        
    
    def __unicode__(self):
        return u"%s (%s %s)" % (self.line,dd.dtos(self.start_date),self.room)
          
    def update_cal_rset(self):
        return self
        
    def update_cal_from(self):
        if self.state in (CourseStates.draft,CourseStates.cancelled): 
            return None
        if self.start_date is None:
            return None
        # if every is per_weekday, actual start may be later than self.start_date
        return self.get_next_date(self.start_date+datetime.timedelta(days=-1))
        
    def update_cal_until(self):
        return self.end_date
        
    def update_cal_calendar(self):
        return self.calendar
        
    def update_cal_subject(self,i):
        return "%s %s" % (dd.babelattr(self.calendar,'event_label'),i)
        #~ return _("Lesson %d") % i
        
    @dd.displayfield(_("Info"))
    def info(self,ar):
        return ar.obj2html(self)
        
    @dd.displayfield(_("Events"))
    def events_text(self,ar=None):
        return ', '.join([day_and_month(e.start_date)
            for e in self.cal_event_set_by_project.order_by('start_date')])
        
    @dd.requestfield(_("Requested"))
    def requested(self,ar):
        #~ return ar.spawn(EnrolmentsByCourse,master_instance=self,param_values=dict(state=EnrolmentStates.requested))
        return EnrolmentsByCourse.request(self,param_values=dict(state=EnrolmentStates.requested))
        
    @dd.requestfield(_("Confirmed"))
    def confirmed(self,ar):
        return EnrolmentsByCourse.request(self,param_values=dict(state=EnrolmentStates.confirmed))
        
    @dd.requestfield(_("Enrolments"))
    def enrolments(self,ar):
        return EnrolmentsByCourse.request(self)
        
"""
customize fields coming from mixins to override their inherited default verbose_names
"""
dd.update_field(Course,'contact_person',verbose_name = _("Contact person"))
dd.update_field(Course,'company',verbose_name = _("Organizer"))
          
          
@dd.receiver(dd.pre_save, sender=cal.Event,dispatch_uid="setup_event_from_course")
def setup_event_from_course(sender=None,instance=None,**kw):
    #~ logger.info("20130528 setup_event_from_course")
    if settings.SITE.loading_from_dump: return
    event = instance
    if event.is_user_modified(): return
    if event.is_fixed_state(): return
    if not isinstance(event.owner,Course): return
    course = event.owner
    event.project = course
    #~ settings.SITE.setup_course_event(course,event)
    
    event.room = course.room
    if course.slot: 
        event.start_time = course.slot.start_time
        event.end_time = course.slot.end_time
    else:
        event.start_time = course.start_time
        event.end_time = course.end_time
    
       
if Course.FILL_EVENT_GUESTS:
    
    @dd.receiver(dd.post_save, sender=cal.Event,dispatch_uid="fill_event_guests_from_course")
    def fill_event_guests_from_course(sender=None,instance=None,**kw):
        #~ logger.info("20130528 fill_event_guests_from_course")
        if settings.SITE.loading_from_dump: return
        event = instance
        if event.is_user_modified(): return
        if event.is_fixed_state(): return
        if not isinstance(event.owner,Course): return
        course = event.owner
        if event.guest_set.count() > 0: return
        for e in course.enrolment_set.all():
            cal.Guest(partner=e.pupil,event=event).save()
    
  

class CourseDetail(dd.FormLayout):
    #~ start = "start_date start_time"
    #~ end = "end_date end_time"
    #~ freq = "every every_unit"
    #~ start end freq
    main = "general courses.EnrolmentsByCourse"
    general = dd.Panel("""
    line teacher start_date start_time room #slot state id:8
    max_places max_events end_date end_time every_unit every 
    monday tuesday wednesday thursday friday saturday sunday
    company contact_person user calendar 
    cal.EventsByController
    """,label=_("General"))
    
    #~ def setup_handle(self,dh):
        #~ dh.start.label = _("Start")
        #~ dh.end.label = _("End")
        #~ dh.freq.label = _("Frequency")
  
class Courses(dd.Table):
    model = 'courses.Course'
    #~ order_by = ['date','start_time']
    detail_layout = CourseDetail() 
    column_names = "info line teacher room slot *"
    order_by = ['start_date']
    
    parameters = dd.ObservedPeriod(
        line = models.ForeignKey('courses.Line',blank=True,null=True),
        topic = models.ForeignKey('courses.Topic',blank=True,null=True),
        company = models.ForeignKey('contacts.Company',blank=True,null=True),
        teacher = models.ForeignKey('courses.Teacher',blank=True,null=True),
        state = CourseStates.field(blank=True),
        )
    params_layout = """topic line company teacher state"""
    
    simple_param_fields = 'topic line teacher company state'.split()
    
    @classmethod
    def get_request_queryset(self,ar):
        qs = super(Courses,self).get_request_queryset(ar)
        if isinstance(qs,list): return qs
        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                qs = qs.filter(**{n:v})
                #~ print 20130530, qs.query
        
        #~ if ar.param_values.teacher is not None: 
            #~ qs = qs.filter(teacher=ar.param_values.teacher)
            #~ 
        #~ if ar.param_values.line is not None: 
            #~ qs = qs.filter(line=ar.param_values.line)
            #~ 
        #~ if ar.param_values.state is not None:
            #~ qs = qs.filter(state=ar.param_values.state)
            
        return qs
        
    @classmethod
    def get_title_tags(self,ar):
        for t in super(Courses,self).get_title_tags(ar):
            yield t
            
        for n in self.simple_param_fields:
            v = ar.param_values.get(n)
            if v:
                yield unicode(v)
                
    

class CoursesByTeacher(Courses):
    master_key = "teacher"
    column_names = "start_date start_time end_time line room *"

class CoursesByLine(Courses):
    master_key = "line"
    column_names = "start_date start_time end_time weekdays_text where_text times_text teacher room"

class CoursesByTopic(Courses):
    master = Topic
    order_by = ['start_date']
    column_names = "start_date:8 line:20 room:10 weekdays_text:10 times_text:10"
    
    @classmethod
    def get_request_queryset(self,ar):
        topic = ar.master_instance
        if topic is None: return []
        return settings.SITE.modules.courses.Course.objects.filter(line__topic=topic)
        

class CoursesBySlot(Courses):
    master_key = "slot"

class CoursesByCompany(Courses):
    master_key = "company"
    
    
class ActiveCourses(Courses):
    
    label = _("Active courses")
    #~ column_names = 'info requested confirmed teacher company room'
    column_names = 'info enrolments #price max_places teacher company room'
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(ActiveCourses,self).param_defaults(ar,**kw)
        kw.update(state=CourseStates.started)
        return kw

    
    
class EnrolmentStates(dd.Workflow):
    verbose_name_plural = _("Enrolment states")
    required = dd.required(user_level='admin')
    invoiceable = models.BooleanField(_("invoiceable"),default=True)

add = EnrolmentStates.add_item
add('10', _("Requested"),'requested',invoiceable=False)
add('20', _("Confirmed"),'confirmed',invoiceable=True)
add('30', _("Cancelled"),'cancelled',invoiceable=False)
add('40', _("Certified"),'certified',invoiceable=True)
#~ add('40', _("Started"),'started')
#~ add('50', _("Success"),'success')
#~ add('60', _("Award"),'award')
#~ add('90', _("Abandoned"),'abandoned')
    

class Enrolment(dd.UserAuthored,dd.Printable,sales.Invoiceable):
    
    workflow_state_field = 'state'
  
    class Meta:
        verbose_name = _("Enrolment")
        verbose_name_plural = _('Enrolments')
        unique_together = ('course','pupil')

    #~ teacher = models.ForeignKey(Teacher)
    course = dd.ForeignKey('courses.Course')
    pupil = dd.ForeignKey(Pupil)
    request_date = models.DateField(_("Date of request"),default=datetime.date.today)
    state = EnrolmentStates.field(default=EnrolmentStates.requested)
    amount = dd.PriceField(_("Amount"),blank=True)
    remark = models.CharField(max_length=200,
          blank=True,
          verbose_name=_("Remark"))
  
    def save(self,*args,**kw):
        if self.amount is None:
            self.compute_amount()
        super(Enrolment,self).save(*args,**kw)

    #~ def before_ui_save(self,ar):
        #~ if self.amount is None:
            #~ self.compute_amount()
        #~ super(Enrolment,self).before_ui_save(ar)
        
    def get_print_templates(self,bm,action):
        #~ if self.state:
        return [self.state.name + bm.template_ext]
        #~ return super(Enrolment,self).get_print_templates(bm,action)
        
    def __unicode__(self):
        return "%s / %s" % (self.course,self.pupil)
        
    invoiceable_date_field = 'request_date'
    #~ invoiceable_partner_field = 'pupil'
    
    @classmethod
    def get_partner_filter(cls,partner):
        """
        Return a dict of filter...
        """
        #~ kw.update(pupil=partner)
        q1 = models.Q(pupil__invoicing_address__isnull=True,pupil=partner)
        q2 = models.Q(pupil__invoicing_address=partner)
        return models.Q(q1 | q2,invoice__isnull=True)
    
    
    def pupil_changed(self,ar):
        self.compute_amount()
        
    def compute_amount(self):
        #~ if self.course is None: 
            #~ return 
        if self.course.tariff is None:
            self.amount = ZERO
        self.amount = self.course.tariff.sales_price
            
    def get_invoiceable_amount(self): 
        return self.amount
        
    def get_invoiceable_product(self): 
        #~ if self.course is not None: 
        if self.state.invoiceable: 
            return self.course.tariff
            
    def get_invoiceable_title(self): 
        #~ if self.course is not None: 
        return self.course

    def get_invoiceable_qty(self): 
        return ONE
    

class Enrolments(dd.Table):
    #~ debug_permissions=20130531
    required = dd.required(user_level='manager')
    model = Enrolment
    parameters = dd.ObservedPeriod(
        author = dd.ForeignKey(settings.SITE.user_model,blank=True,null=True),
        state = EnrolmentStates.field(blank=True,null=True),
        course_state = CourseStates.field(_("Course state"),blank=True,null=True),
        participants_only = models.BooleanField(_("Participants only"),
            help_text=_("Hide cancelled enrolments. Ignored if you specify an explicit enrolment state."),
            default=True),
        )
    params_layout = """start_date end_date author state course_state participants_only"""
    order_by = ['request_date']
    column_names = 'request_date course pupil workflow_buttons user *'
    hidden_columns = 'id state'
    insert_layout = """
    request_date user
    course pupil
    remark
    """
    detail_layout = """
    request_date user
    course pupil 
    remark amount workflow_buttons
    sales.InvoicingsByInvoiceable
    """
        
    @classmethod
    def get_request_queryset(self,ar):
        qs = super(Enrolments,self).get_request_queryset(ar)
        if isinstance(qs,list): return qs
        if ar.param_values.author is not None:
            qs = qs.filter(user=ar.param_values.author)
            
        if ar.param_values.state:
            qs = qs.filter(state=ar.param_values.state)
        else:
            if ar.param_values.participants_only:
                qs = qs.exclude(state=EnrolmentStates.cancelled)
            
        if ar.param_values.course_state:
            qs = qs.filter(course__state=ar.param_values.course_state)
            
            
        if ar.param_values.start_date is None or ar.param_values.end_date is None:
            period = None
        else:
            period = (ar.param_values.start_date, ar.param_values.end_date)
        if period is not None:
            qs = qs.filter(dd.inrange_filter('request_date',period))
                
        return qs
        
    @classmethod
    def get_title_tags(self,ar):
        for t in super(Enrolments,self).get_title_tags(ar):
            yield t
            
        if ar.param_values.state:
            yield unicode(ar.param_values.state)
        elif not ar.param_values.participants_only:
            yield unicode(_("Also ")) + unicode(EnrolmentStates.cancelled.text)
        if ar.param_values.course_state:
            yield unicode(settings.SITE.modules.courses.Course._meta.verbose_name) + ' ' + unicode(ar.param_values.course_state)
        if ar.param_values.author:
            yield unicode(ar.param_values.author)
        

class ConfirmAllEnrolments(dd.Action):
    label = _("Confirm all")
    select_rows = False
    http_method = 'POST'
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        assert obj is None
        def ok():
            for obj in ar:
                obj.state = EnrolmentStates.confirmed
                obj.save()
                kw.update(refresh_all=True)
            return kw
        msg = _("This will confirm all %d enrolments in this list.") % ar.get_total_count()
        return ar.confirm(ok, msg, _("Are you sure?"))
    


class PendingRequestedEnrolments(Enrolments):
    
    label = _("Pending requested enrolments")
    auto_fit_column_widths = True
    params_panel_hidden = True
    column_names = 'request_date course pupil remark user amount workflow_buttons'
    hidden_columns = 'id state'
    
    confirm_all = ConfirmAllEnrolments()
    
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(PendingRequestedEnrolments,self).param_defaults(ar,**kw)
        kw.update(state=EnrolmentStates.requested)
        return kw
        
class PendingConfirmedEnrolments(Enrolments):
    label = _("Pending confirmed enrolments")
    auto_fit_column_widths = True
    params_panel_hidden = True
    
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(PendingConfirmedEnrolments,self).param_defaults(ar,**kw)
        kw.update(state=EnrolmentStates.confirmed)
        kw.update(course_state=CourseStates.ended)
        return kw
        
    
class EnrolmentsByPupil(Enrolments):
    params_panel_hidden = True
    required = dd.required()
    master_key = "pupil"
    column_names = 'request_date course user workflow_buttons *'

class EnrolmentsByCourse(Enrolments):
    params_panel_hidden = True
    required = dd.required()
    master_key = "course"
    column_names = 'request_date pupil workflow_buttons user *'
    auto_fit_column_widths = True









def get_todo_tables(ar):
    yield (PendingRequestedEnrolments, None) 
    yield (PendingConfirmedEnrolments, None) 




dd.inject_field(Person,
    'is_teacher',
    mti.EnableChild(Teacher,verbose_name=_("is a teacher")),
    """Whether this Person is also a Teacher."""
    )
dd.inject_field(Person,
    'is_pupil',
    mti.EnableChild(Pupil,verbose_name=_("is a pupil")),
    """Whether this Person is also a Pupil."""
    )

MODULE_LABEL = _("School")
    
def setup_main_menu(site,ui,profile,main):
    m = main.get_item("contacts")
    m.add_action(Teachers)
    m.add_action(Pupils)
    m = main.add_menu("courses",MODULE_LABEL)
    m.add_action(Courses)
    #~ m.add_action(Teachers)
    #~ m.add_action(Pupils)
    m.add_action(PendingRequestedEnrolments)
    m.add_action(PendingConfirmedEnrolments)
  
def unused_setup_master_menu(site,ui,profile,m): 
    #~ m = m.add_menu("courses",_("School"))
    m.add_action(Teachers)
    m.add_action(Pupils)
    #~ m.add_action(CourseOffers)
    #~ m.add_action(Courses)


def setup_config_menu(site,ui,profile,m):
    m = m.add_menu("courses",MODULE_LABEL)
    #~ m.add_action(Rooms)
    m.add_action(TeacherTypes)
    m.add_action(PupilTypes)
    m.add_action(Topics)
    m.add_action(Lines)
    m.add_action(Slots)
    #~ m.add_action(PresenceStatuses)
  
def setup_explorer_menu(site,ui,profile,m):
    m = m.add_menu("courses",MODULE_LABEL)
    #~ m.add_action(Presences)
    #~ m.add_action(Events)
    m.add_action(Enrolments)
    m.add_action(EnrolmentStates)
  
  
#~ print '20130219 lino.modlib.courses ok'  
