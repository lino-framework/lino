## Copyright 2009 Luc Saffre
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

from django import forms
from django.db import models
from django.utils.translation import ugettext as _

import lino
from lino import reports
from lino import forms
from lino import layouts
from lino import actions
from lino.utils import perms


class Permissions(reports.Report):
    model = auth.Permission
    order_by = 'content_type__app_label codename'
  
class Users(reports.Report):
    model = auth.User
    order_by = "username"
    display_field = 'username'
    columnNames = 'username first_name last_name is_active id is_superuser is_staff last_login'

class Groups(reports.Report):
    model = auth.Group
    order_by = "name"
    display_field = 'name'

class Sessions(reports.Report):
    model = sessions.Session
    display_field = 'session_key'


class ContentTypes(reports.Report):
    model = contenttypes.ContentType


class PasswordResetOK(actions.Action):
    label = _("Request Password Reset")
    def run(self,context):
        context.error('not implemented')

class PasswordResetLayout(layouts.FormLayout):
    #form = PasswordResetForm
    #width = 50
    
    intro = layouts.StaticText("""
    Please fill in your e-mail adress.
    We will then send you a mail with a new temporary password.
    """)
    
    main = """
    intro
    email:50
    ok cancel
    """
    
class PasswordReset(forms.Form):
    layout = PasswordResetLayout
    title = _("Request Password Reset")
    #email = models.EmailField(verbose_name=_("E-mail"), max_length=75)
    email = forms.Input(fieldLabel=_("E-mail"),maxLength=75)
    ok = PasswordResetOK()
    
    
from django.contrib.auth import login, authenticate, logout

class LoginOK(actions.OK):
  
    label = _("Login")
    
    def run(self,context):
      
        username = context.request.POST.get('username')
        password = context.request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise actions.ValidationError(
                _("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not user.is_active:
                raise actions.ValidationError(_("This account is inactive."))
            login(context.request, user)
            #lino.log.info("User %s logged in.",user)
            context.refresh_menu()
            context.done("Welcome, %s!" % user)
        

class LoginLayout(layouts.FormLayout):
    main = """
    text
    username
    password
    cancel ok
    """
    text = layouts.StaticText("Please enter your username and password to authentificate.")
    


class Login(forms.Form):
    layout = LoginLayout
    #username = models.CharField(verbose_name=_("Username"), max_length=75)    
    #password = models.CharField(verbose_name=_("Password"), max_length=75)
    username = forms.Input(fieldLabel=_("Username"),maxLength=75)
    password = forms.Input(fieldLabel=_("Password"),maxLength=75,inputType='password')
    ok = LoginOK()
  

    def before(self,context):
        if not context.request.session.test_cookie_worked():
           raise actions.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))
        

class Logout(actions.Command): #actions.OK):
  
    label = _("Log out")
    
    def run(self,context):
        user = context.get_user()
        context.confirm(_("%s, are you sure you want to log out?") % user)
        logout(context.request)
        context.refresh_menu()
        context.done("Goodbye, %s!" % user)

    


def add_auth_menu(lino):
    m = lino.add_menu("auth",_("~Authentificate"))
    m.add_action('system.Login',can_view=perms.is_anonymous)
    m.add_action('system.Logout',can_view=perms.is_authenticated)
    m.add_action('system.PasswordReset',can_view=perms.is_authenticated)
