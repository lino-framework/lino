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
from lino.utils import choicelists
from lino.utils.choosers import chooser
from lino import mixins
from lino.core import actions

#~ from lino.mixins import PersonMixin
#~ from lino.modlib.contacts.models import Contact
#~ from lino.modlib.contacts import models as contacts

#~ contacts = dd.resolve_app('contacts')

from lino.core.perms import UserLevels, UserProfiles

if settings.LINO.user_model != 'users.User':
    raise Exception("""\
You are using lino.modlib.users in your INSTALLED_APPS, 
but settings.LINO.user_model is %r (should be 'users.User').
""" % settings.LINO.user_model)

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
    
    authenticated = True
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['last_name','first_name']

    username = models.CharField(_('Username'), max_length=30, 
        unique=True, 
        help_text=_("""
        Required. Must be unique. 
        """))
        
    profile = UserProfiles.field()
    
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)
    
    remarks = models.TextField(_("Remarks"),blank=True) # ,null=True)
    
    language = babel.LanguageField()
    
    if settings.LINO.is_installed('contacts'):
      
        partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
        
    else:
      
        partner = dd.DummyField()
    

    def __unicode__(self):
        return self.get_full_name()
        

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


    if settings.LINO.is_installed('contacts'):
        def get_person(self):
            if self.partner:
                return self.partner.get_mti_child('person')
    else:
        def get_person(self):
            return None
    
    person = property(get_person)

    def get_row_permission(self,user,state,action):
        """
        Only system managers may edit other users.
        See also :meth:`User.disabled_fields`.
        """
        #~ print 20120621, self, user, state, action
        if action.readonly: return True
        if user.profile.level >= UserLevels.admin: return True
        #~ print 20120621, user.profile.level, 'is not', UserLevels.admin
        if user.profile.level >= UserLevels.user: 
            if user == self: return True
        return super(User,self).get_row_permission(user,state,action)
        #~ return False
        
    def disabled_fields(self,ar):
        """
        Only System admins may change the profile of users.
        See also :meth:`Users.get_row_permission`.
        """
        #~ if ar.get_user().is_superuser: 
        #~ if request.user.is_superuser: 
        if ar.get_user().profile.level < UserLevels.admin:
            l = ['profile']
        else:
            l = []
        #~ if self.profile:
            #~ l += settings.LINO.user_profile_fields
        return l
        
    def save(self,*args,**kw):
        p = self.person
        if p is not None:
            for n in ('first_name','last_name','email'):
                if not getattr(self,n):
                    setattr(self,n,getattr(p,n))
        super(User,self).save(*args,**kw)
        
    def get_received_mandates(self):
        #~ return [ [u.id,_("as %s")%u] for u in self.__class__.objects.all()]
        return [ [u.id,unicode(u)] for u in self.__class__.objects.all()]
        #~ return self.__class__.objects.all()


class UserDetail(dd.FormLayout):
  
    box1 = """
    username id profile 
    first_name last_name partner
    email language 
    created modified
    """

    main = """
    box1
    remarks AuthoritiesByUser
    """
    
class UserInsert(dd.FormLayout):
  
    window_size = (60,'auto')
    
    main = """
    username email 
    first_name last_name
    partner
    language profile     
    """
    
 
class Users(dd.Table):
    """
    Shows the list of all users on this site.
    """
    #~ debug_actions  = True
    required = dict(user_level='manager')
    model = User
    #~ order_by = "last_name first_name".split()
    order_by = ["username"]
    #~ column_names = 'username first_name last_name is_active is_staff is_expert is_superuser *'
    column_names = 'username profile first_name last_name *'
    detail_layout = UserDetail()
    insert_layout = UserInsert()

    #~ @classmethod
    #~ def get_row_permission(cls,action,user,obj):
        #~ """
        #~ Only system managers may edit other users.
        #~ See also :meth:`User.disabled_fields`.
        #~ """
        #~ if not super(Users,cls).get_row_permission(action,user,obj):
            #~ return False
        #~ if user.level >= UserLevel.manager: return True
        #~ if action.readonly: return True
        #~ if user is not None and user == obj: return True
        #~ return False
          
class MySettings(Users):
    use_as_default_table = False 
    default_action = actions.ShowDetailAction()
    hide_top_toolbar = True
    #~ model = User
    #~ detail_layout = Users.detail_layout
    #~ detail_layout = UserDetail()
    required = dict()
    
    


class Authority(mixins.UserAuthored):
    """
    An Authority is when a User gives another User the right to "represent him"
   
    :user: points to the user who gives the right of representation. author of this Authority
    :authorized: points to the user who gets the right to represent the author
    
    """
    
    class Meta:
        verbose_name = _("Authority")
        verbose_name_plural = _("Authorities")
        
    #~ quick_search_fields = ('user__username','user__first_name','user__last_name')
    
    authorized = models.ForeignKey(settings.LINO.user_model,
        help_text=_("""\
The user who gets authority to act in your name."""))



    @dd.chooser()
    def authorized_choices(cls,user):
        return settings.LINO.user_model.objects.exclude(
            profile=dd.UserProfiles.blank_item).exclude(id=user.id)
              #~ .exclude(level__gte=UserLevels.admin)
    
        
class Authorities(dd.Table):
    required = dict(user_level='manager')
    model = Authority


class AuthoritiesByUser(Authorities):
    required = dict()
    master_key = 'user'
    label = _("Authorities given")

class AuthoritiesByAuthorized(Authorities):
    required = dict()
    master_key = 'authorized'
    label = _("Authorities taken")


