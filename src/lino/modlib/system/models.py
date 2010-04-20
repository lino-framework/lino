## Copyright 2009-2010 Luc Saffre
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

from django.contrib.auth import models as auth
from django.contrib.sessions import models as sessions
from django.contrib.contenttypes import models as contenttypes

#~ from django import forms
from django.db import models
from django.utils.translation import ugettext as _

import lino
from lino import reports
from lino import forms
from lino import layouts
from lino import actions
#~ from lino import commands
from lino.utils import perms


class Permissions(reports.Report):
    model = auth.Permission
    order_by = 'content_type__app_label codename'
  
class Users(reports.Report):
    model = auth.User
    order_by = "username"
    display_field = 'username'
    column_names = 'username first_name last_name is_active id is_superuser is_staff last_login'

class Groups(reports.Report):
    model = auth.Group
    order_by = "name"
    display_field = 'name'

class Sessions(reports.Report):
    model = sessions.Session
    display_field = 'session_key'


class ContentTypes(reports.Report):
    model = contenttypes.ContentType



def add_auth_menu(lino):
    if False:
        m = lino.add_menu("auth",_("~Authentificate"))
        m.add_action('system.Login',can_view=perms.is_anonymous)
        m.add_action('system.Logout',can_view=perms.is_authenticated)
        m.add_action('system.PasswordReset',can_view=perms.is_authenticated)
