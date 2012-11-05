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
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
#~ from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
#~ from lino.modlib.uploads import models as uploads
#~ from lino.modlib.cal import models as cal
#~ from lino.modlib.users import models as users
from lino.modlib.contacts.utils import Gender
from lino.modlib.properties.models import HowWell
#~ from lino.utils.choicelists import HowWell, Gender
from lino.utils.choicelists import ChoiceList
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.utils import babel 
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.core.modeltools import obj2str

from lino.modlib.countries.models import CountryCity
#~ from lino.modlib.cal import models as cal
#~ from lino.modlib.contacts.models import Partner

#~ # not used here, but these modules are required in INSTALLED_APPS, 
#~ # and other code may import them using 

#~ from lino.modlib.properties.models import Property
#~ # from lino.modlib.notes.models import NoteType
#~ from lino.modlib.countries.models import Country, City

if settings.LINO.user_model:
    User = dd.resolve_model(settings.LINO.user_model,strict=True)

users = dd.resolve_app('users')
cal = dd.resolve_app('cal')
contacts = dd.resolve_app('contacts')
Company = dd.resolve_model('contacts.Company',strict=True)
Person = dd.resolve_model('contacts.Person',strict=True)



#~ class PresenceStatus(babel.BabelNamed):
    #~ class Meta:
        #~ verbose_name = _("Presence Status")
        #~ verbose_name_plural = _("Presence Statuses")
        
#~ class PresenceStatuses(dd.Table):
    #~ model = PresenceStatus
    
class Content(babel.BabelNamed):
    class Meta:
        verbose_name = _("Course Content")
        verbose_name_plural = _('Course Contents')
    #~ name = models.CharField(max_length=200,
          #~ blank=True,# null=True,
          #~ verbose_name=_("Name"))
    #~ def __unicode__(self):
        #~ return unicode(self.name)
        
class Contents(dd.Table):
    model = Content
    detail_layout = """
    id name
    school.CoursesByContent
    """
    
        
#~ class Room(babel.BabelNamed):
    #~ class Meta:
        #~ verbose_name = _("Classroom")
        #~ verbose_name_plural = _("Classrooms")
        
#~ class Rooms(dd.Table):
    #~ model = Room
        
        
class Teacher(Person):
    class Meta:
        #~ app_label = 'school'
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
    
#~ site.modules.contacts.Persons.add_detail_tab('school.CoursesByTeacher')

class TeacherDetail(contacts.PersonDetail):
    box5 = "remarks" 
    general = dd.Panel(contacts.PersonDetail.main,label = _("General"))
    main = "general cal.EventsByPartner school.CoursesByTeacher"

    #~ def setup_handle(self,lh):
      
        #~ lh.general.label = _("General")
        #~ lh.notes.label = _("Notes")

class Teachers(contacts.Persons):
    model = Teacher
    detail_layout = TeacherDetail()
  

class Pupil(Person):
    class Meta:
        #~ app_label = 'courses'
        verbose_name = _("Pupil")
        verbose_name_plural = _("Pupils")
    
class PupilDetail(contacts.PersonDetail):
    box5 = "remarks" 
    general = dd.Panel(contacts.PersonDetail.main,label = _("General"))
    
    school = dd.Panel("""
    EnrolmentsByPupil 
    # PresencesByPupil
    cal.GuestsByPartner
    """,label = _("School"))
    
    main = "general school"

    #~ def setup_handle(self,lh):
      
        #~ lh.general.label = _("General")
        #~ lh.school.label = _("School")
        #~ lh.notes.label = _("Notes")

class Pupils(contacts.Persons):
    model = Pupil
    detail_layout = PupilDetail()




  
    
#~ class Course(cal.RecurrenceSet,mixins.Printable):
  
class Slot(mixins.Sequenced):
    """
    """
    class Meta:
        verbose_name = _("Timetable Slot") # Zeitnische
        verbose_name_plural = _('Timetable Slots')
        
    name = models.CharField(max_length=200,
          unique=True,
          verbose_name=_("Name"))
    #~ weekday = cal.Weekday.field()
    monday    = models.BooleanField(cal.Weekday.monday.text)
    tuesday   = models.BooleanField(cal.Weekday.tuesday.text)
    wednesday = models.BooleanField(cal.Weekday.wednesday.text)
    thursday  = models.BooleanField(cal.Weekday.thursday.text)
    friday    = models.BooleanField(cal.Weekday.friday.text)
    saturday  = models.BooleanField(cal.Weekday.saturday.text)
    sunday    = models.BooleanField(cal.Weekday.sunday.text)
    start_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start Time"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End Time"))
  
    def __unicode__(self):
        return self.name
        
    def is_available_on(self,date):
        wd = date.isoweekday() # Monday:1, Tuesday:2 ... Sunday:7
        wd = cal.Weekday.get_by_value(str(wd))
        return getattr(self,wd.name)
        
class Slots(dd.Table):
    model = Slot
    detail_layout = """
    name start_time end_time 
    monday tuesday wednesday thursday friday saturday sunday
    school.CoursesBySlot
    """
    

#~ def on_event_generated(self,course,ev):
def setup_course_event(self,course,ev):
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
    
if not hasattr(settings.LINO,'setup_course_event'):
    #~ raise Exception("20120403")
    #~ setattr(site.__class__,'setup_course_event',setup_course_event)
    settings.LINO.__class__.setup_course_event = setup_course_event
    
    
class Course(cal.EventGenerator,cal.RecurrenceSet,mixins.Printable):
    """
    A Course is a group of pupils that regularily 
    meet with a given teacher in a given place.
    """
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')
        
    content = models.ForeignKey(Content)
    teacher = models.ForeignKey(Teacher)
    #~ place = models.ForeignKey(Place,verbose_name=_("Place"),null=True,blank=True) # iCal:LOCATION
    #~ room = models.ForeignKey(Room,blank=True,null=True)
    place = models.ForeignKey(cal.Place,blank=True,null=True)
    slot = models.ForeignKey(Slot,blank=True,null=True)
    #~ slot = models.PositiveSmallIntegerField(_("Time slot"),
        #~ blank=True,null=True)
    
    def __unicode__(self):
        return u"%s (%s)" % (self.content,self.teacher)
          
    def update_cal_rset(self):
        return self
        
    def update_cal_from(self):
        return self.start_date
        
    def update_cal_until(self):
        return self.end_date
        
    def update_cal_subject(self,i):
        return _("Lesson %d") % (i + 1)
        
          
    def update_owned_instance(self,owned):
        #~ if self.course is not None:
        if isinstance(owned,cal.Event):
            owned.project = self
            settings.LINO.setup_course_event(self,owned)
            if owned.guest_set.count() == 0:
            #~ if ev.presence_set.count() == 0:
                for e in self.enrolment_set.all():
                    cal.Guest(partner=e.pupil,event=owned).save()
                    #~ Presence(pupil=e.pupil,event=ev).save()
        super(Course,self).update_owned_instance(owned)
        
  

class CourseDetail(dd.FormLayout):
    #~ start = "start_date start_time"
    #~ end = "end_date end_time"
    #~ freq = "every every_unit"
    #~ start end freq
    main = """
    id:8 user teacher content place 
    summary
    start_date end_date slot every every_unit
    description
    #remark
    #rrule
    school.EnrolmentsByCourse cal.EventsByController
    """
    
    #~ def setup_handle(self,dh):
        #~ dh.start.label = _("Start")
        #~ dh.end.label = _("End")
        #~ dh.freq.label = _("Frequency")
  
class Courses(dd.Table):
    model = Course
    #~ order_by = ['date','start_time']
    detail_layout = CourseDetail() 
    column_names = "content teacher place slot summary *"

class CoursesByTeacher(Courses):
    master_key = "teacher"

class CoursesByContent(Courses):
    master_key = "content"

class CoursesBySlot(Courses):
    master_key = "slot"

class Enrolment(dd.Model):
  
    class Meta:
        verbose_name = _("Enrolment")
        verbose_name_plural = _('Enrolments')

    #~ teacher = models.ForeignKey(Teacher)
    course = models.ForeignKey(Course)
    pupil = models.ForeignKey(Pupil)

class Enrolments(dd.Table):
    model = Enrolment

class EnrolmentsByPupil(Enrolments):
    master_key = "pupil"

class EnrolmentsByCourse(Enrolments):
    master_key = "course"





#~ class Lesson(models.Model,mixins.Printable):
#~ class Event(cal.EventBase):
    #~ class Meta:
        #~ app_label = 'cal'
        #~ verbose_name = _("Lesson")
        #~ verbose_name_plural = _('Lessons')
        
    #~ def __unicode__(self):
        #~ return u"%s %s (%s)" % (
          #~ babel.dtos(self.start_date),
          #~ self.start_time,
          #~ self.user)
  


#~ class Events(dd.Table):
    #~ model = Event
    #~ order_by = ['start_date','start_time']
    #~ detail_layout = EventDetail()

#~ class EventsByTeacher(Events):
    #~ master_key = "user"

#~ class EventsByCourse(Events):
    #~ master_key = "course"


#~ class Presence(dd.Model):
  
    #~ class Meta:
        #~ verbose_name = _("Presence")
        #~ verbose_name_plural = _('Presences')

    #~ # teacher = models.ForeignKey(Teacher)
    #~ event = models.ForeignKey(cal.Event)
    #~ pupil = models.ForeignKey(Pupil)
    #~ absent = models.BooleanField(_("Absent"))
    #~ excused = models.BooleanField(_("Excused"))
    #~ remark = models.CharField(_("Remark"),max_length=200,blank=True)
    #~ # status = models.ForeignKey(PresenceStatus,null=True,blank=True)
    
    #~ def save(self,*args,**kw):
        #~ if self.excused and not self.absent:
            #~ self.absent = True
        #~ super(Presence,self).save(*args,**kw)
        
    #~ def absent_changed(self,rr):
        #~ if not self.absent:
            #~ self.excused = False

#~ class Presences(dd.Table):
    #~ model = Presence
    #~ order_by = ['event__start_date','event__start_time']

#~ class PresencesByPupil(Presences):
    #~ master_key = "pupil"

#~ class PresencesByEvent(Presences):
    #~ master_key = "event"
    



from lino.models import SiteConfig

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


    
def setup_main_menu(site,ui,user,main):
    m = main.get_item("contacts")
    m.add_action(Teachers)
    m.add_action(Pupils)
    m = main.add_menu("school",_("School"))
    m.add_action(Courses)
    m.add_action(Teachers)
    m.add_action(Pupils)
  
def unused_setup_master_menu(site,ui,user,m): 
    #~ m = m.add_menu("school",_("School"))
    m.add_action(Teachers)
    m.add_action(Pupils)
    #~ m.add_action(CourseOffers)
    #~ m.add_action(Courses)
            

def setup_my_menu(site,ui,user,m): pass
  
def setup_config_menu(site,ui,user,m):
    m = m.add_menu("school",_("School"))
    #~ m.add_action(Rooms)
    m.add_action(Contents)
    m.add_action(Slots)
    #~ m.add_action(PresenceStatuses)
  
def setup_explorer_menu(site,ui,user,m):
    m = m.add_menu("school",_("School"))
    #~ m.add_action(Presences)
    #~ m.add_action(Events)
    m.add_action(Enrolments)
  