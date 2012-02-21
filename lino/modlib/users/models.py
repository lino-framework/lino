## Copyright 2011-2012 Luc Saffre
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


import datetime
#~ import logging
#~ logger = logging.getLogger(__name__)

#~ from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from lino import dd
from lino.utils import mti

#~ from lino.mixins import PersonMixin
#~ from lino.modlib.contacts.models import Contact
from lino.modlib.contacts import models as contacts


class User(contacts.Contact,contacts.PersonMixin):
    """
    Represents a User of this site.
    
    This version of the Users table is used on Lino sites with
    :doc:`/topics/http_auth`. 
    
    Only username is required. Other fields are optional.
    
    There is no password field since Lino is not responsible for authentication.
    New users are automatically created in this table when 
    Lino gets a first request with a username that doesn't yet exist.
    It is up to the local system administrator to manually fill then 
    fields like first_name, last_name, email, access rights for the new user.    
    """
    
    _lino_preferred_width = 15 
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    username = models.CharField(_('username'), max_length=30, 
        unique=True, 
        help_text=_("""
        Required. 30 characters or fewer. 
        Letters, numbers and @/./+/-/_ characters
        """))
    #~ first_name = models.CharField(_('first name'), max_length=30, blank=True)
    #~ last_name = models.CharField(_('last name'), max_length=30, blank=True)
    #~ email = models.EmailField(_('e-mail address'), blank=True)
    is_staff = models.BooleanField(_('is staff'), default=False, 
        help_text=_("""
        Designates whether the user can log into this admin site.
        """))
    is_expert = models.BooleanField(_('is expert'), default=False, 
        help_text=_("""
        Designates whether this user has access to functions that require expert rights.
        """))
    is_active = models.BooleanField(_('is active'), default=True, 
        help_text=_("""
        Designates whether this user should be treated as active. 
        Unselect this instead of deleting accounts.
        """))
    is_superuser = models.BooleanField(_('is superuser'), 
        default=False, 
        help_text=_("""
        Designates that this user has all permissions without 
        explicitly assigning them.
        """))
    last_login = models.DateTimeField(_('last login'), default=datetime.datetime.now)
    date_joined = models.DateTimeField(_('date joined'), default=datetime.datetime.now)

    def __unicode__(self):
        return self.username

    def get_full_name(self,salutation=True,**salutation_options):
        "Returns the first_name plus the last_name, with a space in between."
        full_name = u'%s %s' % (self.first_name, self.last_name)
        if not full_name:
            full_name = self.username
        return full_name.strip()


    def email_user(self, subject, message, from_email=None):
        "Sends an e-mail to this User."
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email])

    def full_clean(self,*args,**kw):
        """
        Almost like PersonMixin.full_clean, but 
        takes username if first_name and last_name are empty.
        """
        l = filter(lambda x:x,[self.last_name,self.first_name])
        self.name = " ".join(l)
        if not self.name:
            self.name = self.username
        models.Model.full_clean(self,*args,**kw)
        
    #~ def disable_editing(self,ar):
        #~ if ar.get_user().is_superuser: return False
        #~ if ar.get_user() == self: return False
        #~ return True
        
    def disabled_fields(self,request):
        #~ if ar.get_user().is_superuser: 
        if request.user.is_superuser: 
            return []
        return ['is_superuser','is_active']
        

class Users(dd.Table):
    """Shows the list of users on this site.
    """
    model = User
    #~ order_by = "last_name first_name".split()
    order_by = ["username"]
    column_names = 'username first_name last_name is_active is_staff is_expert is_superuser *'

    @classmethod
    def get_permission(cls,action,user,obj):
        if user.is_superuser: return True
        if action.readonly: return True
        if user is not None and user == obj: return True
        return False
          
  
if settings.LINO.is_installed('contacts'):
    """
    Cannot install modlib.users without installing modlib.contacts.
    But Sphinx's autodoc
    """

    dd.inject_field(contacts.Contact,
        'is_user',
        mti.EnableChild('users.User',verbose_name=_("is User")),
        """Whether this Contact is also a User."""
        )

