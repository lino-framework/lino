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

A **Project** is something into which somebody invests time, energy and money.
Projects form a tree: each Project can have a `parent` 
(another Project for which it is a sub-project).

A **Milestone** is a named step of evolution of a Project.
(For software projects we usually call them a "release" and they are named by a version number.)

A **Ticket** is a concrete question or problem formulated 
by a `reporter` (a Partner). 
A Ticket is always related to a given Project.

A **Session** is when a User works during a given lapse of time 
on a given Project and/or Ticket.

All the Sessions related to a given Project represent the time 
invested into that Project.

Projects are handled by their *name* while Tickets are handled by their *number*.

Extreme case of a session: 

- I start to work on an existing ticket #1 at 9:23.
  A customer phones at 10:17 with a question. Created #2.
  That call is interrupted several times (by the customer himself).
  During the first interruption another customer calls, 
  with another problem (ticket #3) which we solve together within 5 minutes.
  During the second interruption (which lasts 7 minutes) I make a coffee break.
  During the third interruption I continue to analyze the customer's problem.
  When ticket #2 is solved, I decided that it's not worth to keep track of each interruption and that the overall session time for this ticket
  can be estimated to 0:40.
  
  ::
  
    Ticket start end    Pause  Duration
    #1     9:23  13:12  0:45
    #2     10:17 11:12  0:12       0:43   
    #3     10:23 10:28         0:05


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

from lino.modlib.tickets.utils import TicketStates

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
        verbose_name = _("Session Type")
        verbose_name_plural = _('Session Types')

class SessionTypes(dd.Table):
    model = SessionType
    column_names = 'name *'


class Project(mixins.UserAuthored,mixins.Printable):
    """
    The `user` ("Autor") of a project is the User who manages that Project.
    """
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _('Projects')
        
    name = models.CharField(_("Name"),max_length=20)
    parent = models.ForeignKey('self',blank=True,null=True,verbose_name=_("Parent"))
    type = models.ForeignKey('tickets.ProjectType',blank=True,null=True)
    #~ partner = models.ForeignKey('contacts.Partner',blank=True,null=True)
    summary = models.CharField(_("Summary"),max_length=200,blank=True)
    #~ description = dd.RichTextField(_("Description"),blank=True,format='plain')
    
    def __unicode__(self):
        return self.name
        
    
class Projects(dd.Table):
    model = 'tickets.Project'
    detail_layout = """
    name summary parent
    type user 
    # description
    MilestonesByProject TicketsByProject ProjectsByProject 
    # cal.EventsByProject
    """

class ProjectsByProject(Projects):
    master_key = 'parent'
    label = _("Sub-projects")
    column_names = "name summary *"

#~ class ProjectsByPartner(Projects):
    #~ master_key = 'partner'
    #~ column_names = "name summary *"
    #~ label = _("Sub-projects")





class Milestone(mixins.ProjectRelated):
    """
    """
    class Meta:
        verbose_name = _("Milestone")
        verbose_name_plural = _('Milestones')
        
    label = models.CharField(_("Label"),max_length=20)
    expected = models.DateField(_("Expected for"),blank=True,null=True)
    reached = models.DateField(_("Reached"),blank=True,null=True)
    
    def __unicode__(self):
        return self.label
        

class Milestones(dd.Table):
    model = Milestone
    detail_layout = """
    project label expected reached id
    TicketsFixed TicketsReported
    """
    insert_layout = dd.FormLayout("""
    project label 
    """,window_size=(40,'auto'))
    
class MilestonesByProject(Milestones):
    master_key = 'project'
    column_names = "label expected reached *"


#~ class TicketState(babel.BabelNamed):
    #~ """
    #~ The state of a ticket (new, open, closed, ...)
    #~ """
    
    #~ class Meta:
        #~ verbose_name = _("Ticket State")
        #~ verbose_name_plural = _('Ticket States')

#~ class TicketStates(dd.Table):
    #~ model = TicketState
    #~ column_names = 'name *'


class Ticket(mixins.AutoUser,mixins.CreatedModified,mixins.ProjectRelated):
    """
    """
    workflow_state_field = 'state'
    
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')
        
    reported = dd.ForeignKey(Milestone,
        related_name='tickets_reported',
        verbose_name='Reported for',
        blank=True,null=True,
        help_text=_("Milestone for which this ticket has been reported."))
    fixed = dd.ForeignKey(Milestone,
        related_name='tickets_fixed',
        verbose_name='Fixed for',
        blank=True,null=True,
        help_text=_("The milestone for which this ticket has been fixed."))
    partner = models.ForeignKey('contacts.Partner',
        blank=True,null=True,
        help_text=_("The partner who reported this ticket."))
    #~ partner = models.ForeignKey('contacts.Partner')
    #~ project = models.ForeignKey('tickets.Project',blank=True,null=True)
    summary = models.CharField(_("Summary"),max_length=200,
        blank=True,
        help_text=_("Short summary of the problem."))
    #~ state = models.ForeignKey('tickets.TicketState',blank=True,null=True)
    state = TicketStates.field()
    description = dd.RichTextField(_("Description"),blank=True,format='plain')
    #~ start_date = models.DateField(
        #~ verbose_name=_("Start date"),
        #~ blank=True,null=True)
    
    def __unicode__(self):
        return u"#%d (%s)" % (self.id,self.summary)
        
    @dd.chooser()
    def reported_choices(cls,project):
        if not project: return []
        return project.tickets_milestone_set_by_project.filter(reached__isnull=False)
        
    @dd.chooser()
    def fixed_choices(cls,project):
        if not project: return []
        return project.tickets_milestone_set_by_project.all()
        

    def allow_state_accepted(self,user):
        if not self.reported:
            return False
        return True
        
    def allow_state_working(self,user):
        if not self.user:
            return False
        return True
        
    def allow_state_fixed(self,user):
        if not self.fixed:
            return False
        return True
        

class Tickets(dd.Table):
    model = Ticket
    detail_layout = """
    partner project reported summary id
    user created modified state workflow_buttons fixed
    description 
    SessionsByTicket EntriesByTicket
    """
    insert_layout = dd.FormLayout("""
    partner 
    project 
    summary 
    """,window_size=(50,'auto'))
    
class UnassignedTickets(Tickets):
    column_names = "summary project partner *"
class TicketsByProject(Tickets):
    master_key = 'project'
    column_names = "summary user partner *"

class TicketsByPartner(Tickets):
    master_key = 'partner'
    column_names = "summary project user *"

class TicketsFixed(Tickets):
    label = _("Tickets Fixed")
    master_key = 'fixed'
    column_names = "summary user partner *"
    editable = False

class TicketsReported(Tickets):
    label = _("Tickets Reported")
    master_key = 'reported'
    column_names = "summary user partner *"
    editable = False

    
    
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
    detail_layout = """
    date start_time end_time break_time project ticket
    user id 
    description
    EntriesBySession
    """
    
class SessionsByTicket(Sessions):
    master_key = 'ticket'
    
if settings.LINO.user_model:
  
    class MySessions(Sessions,mixins.ByUser):
        order_by = ['date','start_time']
        column_names = 'date start_time end_time break_time project ticket description *'
    
    class MySessionsByDate(MySessions):
        #~ master_key = 'date'
        order_by = ['start_time']
        label = _("My sessions by date")
        column_names = 'start_time end_time break_time project ticket description *'
    
        parameters = dict(
          today = models.DateField(_("Date"),
          blank=True,default=datetime.date.today),
        )
        @classmethod
        def get_request_queryset(self,ar):
            qs = super(MySessions,self).get_request_queryset(ar)
            #~ if ar.param_values.date:
            return qs.filter(date=ar.param_values.today)
            #~ return qs
            
        @classmethod
        def create_instance(self,ar,**kw):
            kw.update(date=ar.param_values.today)
            return super(MySessions,self).create_instance(ar,**kw)

    

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
  
    Tickets.detail_layout = Tickets.detail_layout.replace(' EntriesByTicket','')



if settings.LINO.user_model:    
  
    class MyProjects(Projects,mixins.ByUser):
        order_by = ["name"]
        column_names = 'name id summary *'
        
    class MyTickets(Tickets,mixins.ByUser):
        order_by = ["created","id"]
        column_names = 'created id project summary state *'
        

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
        



def setup_main_menu(site,ui,user,m): 
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action(MyProjects)
    m.add_action(MyTickets)
    m.add_action(MySessions)
    m.add_action(MySessionsByDate)
    #~ m.add_action(MySessionsByDate,params=dict(master_instance=datetime.date.today()))

def setup_my_menu(site,ui,user,m): 
    pass
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action(ProjectTypes)
    #~ m.add_action(TicketStates)
    m.add_action(SessionTypes)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action(Projects)
    m.add_action(Tickets)
    m.add_action(Sessions)
    m.add_action(Milestones)
  