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


#~ import datetime
#~ import logging
#~ logger = logging.getLogger(__name__)

#~ from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from lino import dd
from lino.utils import babel
from lino.utils import mti
from lino.utils.choicelists import UserLevel
from lino.utils.choosers import chooser
from lino import mixins

#~ from lino.mixins import PersonMixin
#~ from lino.modlib.contacts.models import Contact
#~ from lino.modlib.contacts import models as contacts

#~ contacts = dd.resolve_app('contacts')

#~ class User(contacts.Partner,contacts.PersonMixin):
#~ class User(models.Model):
class User(mixins.CreatedModified):
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

    username = models.CharField(_('Username'), max_length=30, 
        unique=True, 
        help_text=_("""
        Required. Must be unique. 
        """))
    
    profile = models.CharField(_('Same profile as'), 
        max_length=30, blank=True,
        help_text=_("""
        The user profile. Leave empty for "profile-giving" users, that is: 
        users who have their own combination of group memberships and 
        userlevels.
        """))
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)
    
    remarks = models.TextField(_("Remarks"),blank=True) # ,null=True)
    
    
    level = UserLevel.field()
    
    language = babel.LanguageField()
    
    #~ is_active = models.BooleanField(_('is active'), default=True, 
        #~ help_text=_("""
        #~ Designates whether this user should be treated as active. 
        #~ Unselect this instead of deleting accounts.
        #~ """))
    #~ is_staff = models.BooleanField(_('is staff'), default=False, 
        #~ help_text=_("""
        #~ Designates whether the user can log into this admin site.
        #~ """))
    #~ is_expert = models.BooleanField(_('is expert'), default=False, 
        #~ help_text=_("""
        #~ Designates whether this user has access to functions that require expert rights.
        #~ """))
    #~ is_superuser = models.BooleanField(_('is superuser'), 
        #~ default=False, 
        #~ help_text=_("""
        #~ Designates that this user has all permissions without 
        #~ explicitly assigning them.
        #~ """))
    #~ last_login = models.DateTimeField(_('last login'), default=datetime.datetime.now)
    #~ date_joined = models.DateTimeField(_('date joined'), default=datetime.datetime.now)
    
    if settings.LINO.is_installed('contacts'):
        partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    

    def __unicode__(self):
        #~ return self.username
        return self.get_full_name()
        
    #~ def get_profile(self):
        #~ return self.profile or self.username
        
    @chooser(simple_values=True)
    def profile_choices(self,username):
        qs = User.objects.filter(profile='').exclude(
          username=username).order_by('username')
        #~ print 20120516, qs
        return [u.username for u in qs]
        

    def get_full_name(self):
        "Returns the first_name plus the last_name, with a space in between."
        full_name = u'%s %s' % (self.first_name, self.last_name)
        if not full_name:
            full_name = self.username
        return full_name.strip()
        
    @dd.displayfield(_("Name"))
    def name_column(self,request):
        #~ return join_words(self.last_name.upper(),self.first_name)
        return unicode(self)
        


    #~ def email_user(self, subject, message, from_email=None):
        #~ "Sends an e-mail to this User."
        #~ from django.core.mail import send_mail
        #~ send_mail(subject, message, from_email, [self.email])
    
    if settings.LINO.is_installed('contacts'):
        def get_person(self):
            if self.partner:
                return self.partner.get_mti_child('person')
    else:
        def get_person(self):
            return None
    
    person = property(get_person)

    def save(self,*args,**kw):
        if self.profile == self.username:
            self.profile = ''
        if self.profile:
            u = self.__class__.objects.get(username=self.profile)
            for k in settings.LINO.user_profile_fields:
                setattr(self,k,getattr(u,k))
        super(User,self).save(*args,**kw)
        if not self.profile:
            for u in self.__class__.objects.filter(profile=self.username):
                for k in settings.LINO.user_profile_fields:
                    setattr(u,k,getattr(self,k))
                    u.save()
                
        
    #~ def full_clean(self,*args,**kw):
        #~ """
        #~ Almost like PersonMixin.full_clean, but 
        #~ takes username if first_name and last_name are empty.
        #~ """
        #~ l = filter(lambda x:x,[self.last_name,self.first_name])
        #~ self.name = " ".join(l)
        #~ if not self.name:
            #~ self.name = self.username
        #~ models.Model.full_clean(self,*args,**kw)
        
    #~ def disable_editing(self,ar):
        #~ if ar.get_user().is_superuser: return False
        #~ if ar.get_user() == self: return False
        #~ return True
        
    def disabled_fields(self,request):
        """
        Only System admins may change the profile of users.
        See also :meth:`Users.get_row_permission`.
        """
        #~ if ar.get_user().is_superuser: 
        #~ if request.user.is_superuser: 
        if self.level <= UserLevel.manager:
            l = ['profile']
        else:
            l = []
        if self.profile:
            l += settings.LINO.user_profile_fields
        return l
        #~ if request.user.level >= UserLevel.expert: 
            #~ if self.profile:
                #~ return settings.LINO.user_profile_fields
            #~ else:
                #~ return []
        #~ return ['is_superuser','is_active','is_staff','is_expert']
        #~ return ['level','profile']
        


#~ class UserDetail(dd.DetailLayout):
  
    #~ box2 = """
    #~ username profile 
    #~ level
    #~ """
    
    #~ box3 = """
    #~ country region
    #~ city zip_code:10
    #~ street_prefix street:25 street_no street_box
    #~ addr2:40
    #~ """

    #~ box4 = """
    #~ email:40 
    #~ url
    #~ phone
    #~ gsm
    #~ """

    #~ box1 = """
    #~ first_name last_name language id
    #~ box3:40 box4:30 
    #~ date_joined last_login 
    #~ """
    #~ general = """
    #~ box1:50 box2:20
    #~ remarks 
    #~ """
    
    #~ main = "general"

class UserDetail(dd.DetailLayout):
  
    box1 = """
    username id profile 
    first_name last_name partner
    email language 
    created modified
    """

    box2 = """
    level
    """
    #~ general = """
    #~ box1:50 box2:20
    #~ remarks 
    #~ """
    
    #~ main = "general"
  
    main = """
    box1:50 box2:20
    remarks 
    """
    
if not settings.LINO.is_installed('contacts'):
    UserDetail.box1.replace('partner','')
 

class Users(dd.Table):
    """Shows the list of users on this site.
    """
    model = User
    #~ order_by = "last_name first_name".split()
    order_by = ["username"]
    #~ column_names = 'username first_name last_name is_active is_staff is_expert is_superuser *'
    column_names = 'username profile first_name last_name level *'
    detail_layout = UserDetail()

    @classmethod
    def get_row_permission(cls,action,user,obj):
        """
        Only system managers may edit other users.
        See also :meth:`User.disabled_fields`.
        """
        if not super(Users,cls).get_row_permission(action,user,obj):
            return False
        #~ if user.is_superuser: return True
        if user.level >= UserLevel.manager: return True
        if action.readonly: return True
        if user is not None and user == obj: return True
        return False
          
  
#~ if settings.LINO.is_installed('contacts'):
    #~ """
    #~ Cannot install modlib.users without installing modlib.contacts.
    #~ But Sphinx's autodoc
    #~ """

    #~ dd.inject_field(contacts.Partner,
        #~ 'is_user',
        #~ mti.EnableChild('users.User',verbose_name=_("is User")),
        #~ """Whether this Partner is also a User."""
        #~ )


