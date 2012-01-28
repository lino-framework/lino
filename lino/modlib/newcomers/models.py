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

import os
import sys
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.utils.encoding import force_unicode


from lino import tools
from lino import dd
#~ from lino.utils.babel import default_language
#~ from lino import reports
#~ from lino import layouts
from lino.utils import perms
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino.utils.choosers import chooser
from lino.utils import babel
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method
#~ from lino.modlib.contacts import models as contacts
from lino.modlib.users import models as users


from lino.apps.dsbe.models import Person, AllPersons, only_my_persons, PersonsByCoach1, MyActivePersons

class Broker(models.Model):
    """
    A Broker (Vermittler) is an external institution 
    who suggests newcomers.
    """
    class Meta:
        verbose_name = _("Broker")
        verbose_name_plural = _("Brokers")
        
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Brokers(dd.Table):
    """
    List of Brokers on this site.
    """
    model = Broker
    column_names = 'name *'
    order_by = ["name"]



class Faculty(babel.BabelNamed):
    """
    A Faculty (Fachbereich) is a conceptual (not organizational)
    department of this PCSW. 
    Each Newcomer will be assigned to one and only one Faculty, 
    based on his/her needs.
    
    """
    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")
    body = babel.BabelTextField(_("Body"),blank=True,format='html')
    

class Faculties(dd.Table):
    model = Faculty
    column_names = 'name *'
    order_by = ["name"]

class Competence(mixins.AutoUser,mixins.Sequenced):
    """
    Deserves more documentation.
    """
    class Meta:
        #~ abstract = True
        verbose_name = _("Competence") 
        verbose_name_plural = _("Competences")
        
    faculty = models.ForeignKey(Faculty)
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
class Competences(dd.Table):
    model = Competence
    column_names = 'id *'
    order_by = ["id"]

class CompetencesByUser(Competences):
    master_key = 'user'
    column_names = 'seqno faculty *'
    order_by = ["seqno"]

class CompetencesByFaculty(Competences):
    master_key = 'faculty'
    column_names = 'user *'
    order_by = ["user"]


class MyCompetences(mixins.ByUser,CompetencesByUser):
    pass

    
class Newcomers(AllPersons):
    """
    Persons who have the "Newcomer" checkbox on.
    """
    
    #~ filter = dict(newcomer=True)
    known_values = dict(newcomer=True)
    #~ use_as_default_report = False
    column_names = "name_column broker faculty address_column *"
    
    @classmethod
    def init_label(self):
        return _("Newcomers")
        
class NewClients(AllPersons):
    label = _("New Clients")
    use_as_default_report = False
    
    parameters = dict(
        user = models.ForeignKey(users.User,verbose_name=_("Show agents for newcomer")),
        since= models.DateField(_("Count Newcomers since"),blank=True,default=datetime.date.today),
    )
    
    column_names = "name_column:20 coached_from coached_until national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type coach1 language:10 *"
    
    
    @classmethod
    def get_request_queryset(self,ar):
        """
        We only want the Persons who actually have at least one client.
        We store the corresponding request in the user object 
        under the name `my_persons`.
        """
        #~ qs = Person.objects.all()
        qs = super(NewClients,self).get_request_queryset(ar)
        
        if ar.param_values.user:
            qs = only_my_persons(qs,ar.param_values.user)
            
        if ar.param_values.since:
            qs = qs.filter(coached_from__isnull=False,coached_from__gte=ar.param_values.since) 
            
        return qs
            
    
        
        
class UsersByNewcomer(dd.VirtualTable):
    """
    A list of the users that are susceptible to become responsible for a Newcomer.
    """
    label = _("Users by Newcomer")
    column_names = 'user primary_clients active_clients newcomers'
    parameters = dict(
        person = models.ForeignKey('contacts.Person',verbose_name=_("Show suggested agents for")),
        since= models.DateField(_("Count Newcomers since"),blank=True,default=datetime.date.today),
    )
    
    @chooser()
    def person_choices(cls):
        return Newcomers.request().data_iterator
        
    @classmethod
    def get_data_rows(self,ar):
        """
        We only want the users who actually have at least one client.
        We store the corresponding request in the user object 
        under the name `my_persons`.
        """
        Q = models.Q
        for user in users.User.objects.filter(
            Q(username=ar.get_user().username) | Q(is_spis=True)
          ).order_by('username'):
            if ar.param_values.person:
                r = Competence.objects.filter(user=user,faculty=ar.param_values.person.faculty)
                if r.count():
                    yield user
                
    @dd.virtualfield('contacts.Person.coach1')
    def user(self,obj,ar):
        return obj
        
    @dd.requestfield(_("Primary clients"))
    def primary_clients(self,obj,ar):
        return PersonsByCoach1.request(ar.ui,master_instance=obj)
        
    @dd.requestfield(_("Active clients"))
    def active_clients(self,obj,ar):
        return MyActivePersons.request(ar.ui,subst_user=obj)
        
    @dd.requestfield(_("Newcomers"))
    def newcomers(self,obj,ar):
        return NewClients.request(ar.ui,subst_user=obj,
          param_values=dict(
            person=ar.param_values.person,
            since=ar.param_values.since))
        
        
#~ if settings.LINO.user_model:
dd.inject_field(users.User,
    'is_newcomers',
    models.BooleanField(
        verbose_name=_("is Newcomers user")
    ),"""Whether this user is responsible for dispatching of Newcomers.
    Deserves more documentation.
    """)

dd.inject_field(Person,
    'broker',
    models.ForeignKey(Broker,
        blank=True,null=True),
    """The Broker who sent this Newcomer.
    """)
dd.inject_field(Person,
    'faculty',
    models.ForeignKey(Faculty,
        blank=True,null=True),
    """The Faculty this client has been attributed to.
    """)

class Module(dd.Module):
    pass
  
  
def setup_main_menu(site,ui,user,m):
    if user.is_newcomers:
        m.add_action(Newcomers)
  
def setup_my_menu(site,ui,user,m): 
    if user.is_newcomers:
        #~ m.add_action(MyCompetences)
        m  = m.add_menu("newcomers",_("Newcomers"))
        m.add_action(UsersByNewcomer)
        m.add_action(NewClients)
  
def setup_config_menu(site,ui,user,m): 
    if user.is_newcomers:
        m  = m.add_menu("newcomers",_("Newcomers"))
        m.add_action(Brokers)
        m.add_action(Faculties)
  
def setup_explorer_menu(site,ui,user,m):
    if user.is_newcomers:
        m.add_action(Competences)
  