# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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
Tool for language teachers.
Deserves more documentation.
"""
import cgi
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino import dd
#~ from lino.core import reports
from lino.core import actions
from lino.utils import perms
from lino.utils import babel
from lino.utils import dblogger
from lino.tools import resolve_model

from lino.utils.babel import dtosl


def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("cal",_("~Calendar"))
    m.add_action('cal.MyTasks')
    #~ m.add_action('cal.MyEventsToday')
    m.add_action('cal.MyEvents')
    if settings.LINO.use_extensible:
        m.add_action('cal.Panel')
    #~ m.add_action_(actions.Calendar())
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("cal",_("~Calendar"))
    m.add_action('cal.Places')
    m.add_action('cal.Priorities')
    m.add_action('cal.AccessClasses')
    m.add_action('cal.EventStatuses')
    m.add_action('cal.TaskStatuses')
    m.add_action('cal.EventTypes')
    m.add_action('cal.GuestRoles')
    m.add_action('cal.GuestStatuses')
    m.add_action('cal.Calendars')
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("cal",_("~Calendar"))
    m.add_action('cal.Events')
    m.add_action('cal.Tasks')
    m.add_action('cal.Guests')
    m.add_action('cal.RecurrenceSets')
  