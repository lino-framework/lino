# -*- coding: UTF-8 -*-
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

"""
This module adds models for Projects, Tickets and Sessions.

Projects are handled by their *name* while Tickets are handled by their *number*.
Projects are long-term while Tickets are short-term.

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
from lino.utils import babel
#~ from lino.modlib.cal import models as cal

blogs = dd.resolve_app('blogs')


class ProjectType(mixins.PrintableType,babel.BabelNamed):
    "Deserves more documentation."
  
    templates_group = 'tickets/Project'
    
    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')

class ProjectTypes(dd.Table):
    model = ProjectType
    column_names = 'name build_method template *'


class SessionType(babel.BabelNamed):
    "Deserves more documentation."
  
    class Meta:
        verbose_name = _("SessionType")
        verbose_name_plural = _('Session Types')

class SessionTypes(dd.Table):
    model = SessionType
    column_names = 'name *'


class Project(mixins.AutoUser,mixins.Printable):
    """
    """
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _('Projects')
        
    parent = models.ForeignKey('self',blank=True,null=True)
    type = models.ForeignKey('tickets.ProjectType',blank=True,null=True)
    name = models.CharField(_("Name"),max_length=20)
    summary = models.CharField(_("Summary"),max_length=200,blank=True)
    description = dd.RichTextField(_("Description"),blank=True,format='plain')
    
    def __unicode__(self):
        return self.name
        
    
class Projects(dd.Table):
    model = 'tickets.Project'
    detail_template = """
    name summary type user 
    description
    TicketsByProject ProjectsByProject
    # cal.EventsByProject
    """

class ProjectsByProject(Projects):
    master_key = 'parent'
    label = _("Sub-projects")


class TicketState(babel.BabelNamed):
    """
    The state of a ticket (new, open, closed, ...)
    """
    
    class Meta:
        verbose_name = _("Ticket State")
        verbose_name_plural = _('Ticket States')

class TicketStates(dd.Table):
    model = TicketState
    column_names = 'name *'



class Ticket(mixins.AutoUser,mixins.CreatedModified,mixins.ProjectRelated):
    """
    """
    
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')
        
    #~ project = models.ForeignKey('tickets.Project',blank=True,null=True)
    summary = models.CharField(_("Summary"),max_length=200,blank=True)
    state = models.ForeignKey('tickets.TicketState',blank=True,null=True)
    description = dd.RichTextField(_("Description"),blank=True,format='plain')
    #~ start_date = models.DateField(
        #~ verbose_name=_("Start date"),
        #~ blank=True,null=True)
    
    def __unicode__(self):
        return u"#%d (%s)" % (self.id,self.summary)


class Tickets(dd.Table):
    model = Ticket
    detail_template = """
    project summary user created modified
    description
    SessionsByTicket EntriesByTicket
    """
    
class TicketsByProject(Tickets):
    master_key = 'project'

#~ class EventsByTicket(cal.Events):
    #~ master_key = 'ticket'
    
    
class Session(mixins.AutoUser,mixins.ProjectRelated):
    """
    A Session is when a user works on a project or ticket. This just keeps track 
    """
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _('Sessions')

    #~ project = models.ForeignKey('tickets.Project',blank=True,null=True)
    ticket = models.ForeignKey('tickets.Ticket',blank=True,null=True)
    description = dd.RichTextField(_("Description"),blank=True,format='plain')
    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Start time"))
    end_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("End Time"))
    break_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Break Time"))
    
    
class Sessions(dd.Table):
    model = Session
    column_names = 'date start_time end_time break_time description user *'
    order_by = ['date','start_time']
    detail_template = """
    date start_time end_time break_time project ticket
    user id 
    description
    EntriesBySession
    """
    
class SessionsByTicket(Sessions):
    master_key = 'ticket'

if blogs:
  
    dd.inject_field('blogs.Entry',
        'ticket',
        models.ForeignKey("tickets.Ticket",
            blank=True,null=True,
            # verbose_name=_("Local job office"),
            # related_name='job_office_sites'
            help_text="""The Ticket attributed to this Entry."""))

    class EntriesByTicket(blogs.Entries):
        master_key = 'ticket'
    
    class EntriesBySession(EntriesByTicket):
        """
        The Blog Entries linked to *the Ticket of* a Session.
        
        Blog Entries are not directly linked to a Session, but in the 
        Detail of a Session we want to display a table of related blog 
        entries.
        """
        @classmethod
        def get_filter_kw(self,master_instance,**kw):
            if master_instance is not None:
                master_instance = master_instance.ticket
            return super(EntriesBySession,self).get_filter_kw(master_instance,**kw)
        
    
else:
  
    Tickets.detail_template = Tickets.detail_template.replace(' EntriesByTicket','')



if settings.LINO.user_model:    
  
    class MyProjects(Projects,mixins.ByUser):
        order_by = ["name"]
        column_names = 'name id summary *'
        
    class MyTickets(Tickets,mixins.ByUser):
        order_by = ["created","id"]
        column_names = 'created id project summary state *'
        
    class MySessions(Sessions,mixins.ByUser):
        order_by = ['date','start_time']
        column_names = 'date start_time end_time break_time project ticket description *'
    
    class MySessionsByDate(MySessions):
        master_key = 'date'
        order_by = ['start_time']
        label = _("My sessions by date")
        column_names = 'start_time end_time break_time project ticket description *'
    
        parameters = dict(
          date = models.DateField(_("Date"),
          blank=True,default=datetime.date.today),
        )
        @classmethod
        def get_request_queryset(self,ar):
            qs = super(MySessions,self).get_request_queryset(ar)
            #~ if ar.param_values.date:
            return qs.filter(date=ar.param_values.date)
            #~ return qs
            
        @classmethod
        def create_instance(self,ar,**kw):
            kw.update(date=ar.param_values.date)
            return super(MySessions,self).create_instance(ar,**kw)


#~ if dd.is_installed('cal'):

    #~ dd.inject_field(cal.Event,
        #~ 'ticket',
        #~ models.ForeignKey("tickets.Ticket",
            #~ blank=True,null=True,
            #~ # verbose_name=_("Local job office"),
            #~ # related_name='job_office_sites'
            #~ ),
        #~ """The Ticket attributed to this event.
        #~ """)
        



def setup_main_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action(MyProjects)
    m.add_action(MyTickets)
    m.add_action(MySessions)
    m.add_action(MySessionsByDate)
    #~ m.add_action(MySessionsByDate,params=dict(master_instance=datetime.date.today()))
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action(ProjectTypes)
    m.add_action(TicketStates)
    m.add_action(SessionTypes)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action(Projects)
    m.add_action(Tickets)
    m.add_action(Sessions)
  