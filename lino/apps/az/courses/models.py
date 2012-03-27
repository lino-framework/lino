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
from lino.utils import perms
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
from lino.modlib.contacts import models as contacts
from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
#~ from lino.modlib.uploads import models as uploads
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
from lino.modlib.contacts.models import Partner
from lino.tools import resolve_model, UnresolvedModel

#~ # not used here, but these modules are required in INSTALLED_APPS, 
#~ # and other code may import them using 
#~ # ``from lino.apps.dsbe.models import Property``

#~ from lino.modlib.properties.models import Property
#~ # from lino.modlib.notes.models import NoteType
#~ from lino.modlib.countries.models import Country, City

if settings.LINO.user_model:
    User = resolve_model(settings.LINO.user_model,strict=True)

#~ Company = resolve_model('contacts.Company',strict=True)
Person = resolve_model('contacts.Person',strict=True)



class PresenceStatus(babel.BabelNamed):
    class Meta:
        verbose_name = _("Presence Status")
        verbose_name_plural = _("Presence Statuses")
        
class PresenceStatuses(dd.Table):
    model = PresenceStatus
        
        
class Teacher(Person):
    class Meta:
        app_label = 'courses'
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
    
class TeacherDetail(contacts.PersonDetail):
    box5 = "remarks" 
    general = contacts.PersonDetail.main
    main = "general LessonsByTeacher"

    def setup_handle(self,lh):
      
        lh.general.label = _("General")
        #~ lh.notes.label = _("Notes")

class Teachers(contacts.Persons):
    model = Teacher
    detail_layout = TeacherDetail()
  

class Pupil(Person):
    class Meta:
        app_label = 'courses'
        verbose_name = _("Pupil")
        verbose_name_plural = _("Pupils")
    
class PupilDetail(contacts.PersonDetail):
    box5 = "remarks" 
    general = contacts.PersonDetail.main
    main = "general PresencesByPupil"

    def setup_handle(self,lh):
      
        lh.general.label = _("General")
        #~ lh.notes.label = _("Notes")

class Pupils(contacts.Persons):
    model = Pupil
    detail_layout = PupilDetail()
  




class Content(models.Model):
    
    class Meta:
        verbose_name = _("Course Content")
        verbose_name_plural = _('Course Contents')
        
    name = models.CharField(max_length=200,
          blank=True,# null=True,
          verbose_name=_("Name"))
          
    def __unicode__(self):
        return unicode(self.name)
        
  
    
class Lesson(models.Model,mixins.Printable):
    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _('Lessons')
        
        
    teacher = models.ForeignKey(Teacher)
    
    date = models.DateField(_("date"))
    start_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start time"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End time"))
  
    remark = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("Remark"))
        
    def __unicode__(self):
        return u"%s %s-%s (%s)" % (
          babel.dtos(self.start_date),
          self.start_time,
          self.end_time,
          self.teacher)
  

class Lessons(dd.Table):
    model = Lesson
    order_by = ['date start_time']
    detail_template = """
    id:8 teacher start_time end_time 
    remark
    courses.PresencesByLesson
    """

class Presence(models.Model):
  
    class Meta:
        verbose_name = _("Presence")
        verbose_name_plural = _('Presences')

    #~ teacher = models.ForeignKey(Teacher)
    lesson = models.ForeignKey(Lesson)
    pupil = models.ForeignKey(Pupil)
    status = models.ForeignKey(PresenceStatus)




class Presences(dd.Table):
    model = Presence
    #~ order_by = ['date start_time']

class PresencesByPupil(Presences):
    master_key = "pupil"

class PresencesByLesson(Presences):
    master_key = "lesson"
    
class LessonsByTeacher(Lessons):
    master_key = "teacher"




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

    
def setup_main_menu(site,ui,user,m): 
    m = m.add_menu("courses",_("Courses"))
    m.add_action(Teachers)
    m.add_action(Pupils)
    #~ m.add_action(CourseOffers)
    #~ m.add_action(Courses)
            

def setup_my_menu(site,ui,user,m): pass
  
def setup_config_menu(site,ui,user,m):
    m = m.add_menu("courses",_("Courses"))
    m.add_action(PresenceStatuses)
  
def setup_explorer_menu(site,ui,user,m):
    m = m.add_menu("courses",_("Courses"))
    m.add_action(Presences)
    m.add_action(Lessons)
  