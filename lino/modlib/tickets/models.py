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
This module adds models for Projects, Tickets and Comments.

"""
import cgi
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino import fields
from lino import reports
from lino.utils import babel
#~ from lino.modlib.cal import models as cal


class ProjectType(mixins.PrintableType,babel.BabelNamed):
    "Deserves more documentation."
  
    templates_group = 'tickets/Project'
    
    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')

class ProjectTypes(reports.Report):
    model = ProjectType
    column_names = 'name build_method template *'


    
class Project(mixins.AutoUser,mixins.Printable):
    """
    """
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _('Projects')
        
    type = models.ForeignKey('tickets.ProjectType',blank=True,null=True)
    name = models.CharField(_("Name"),max_length=20)
    summary = models.CharField(_("Summary"),max_length=200,blank=True)
    description = fields.RichTextField(_("Description"),blank=True,format='plain')
    
    def __unicode__(self):
        return self.name
        
    
class Projects(reports.Report):
    model = 'tickets.Project'



class TicketState(babel.BabelNamed):
    """
    The state of a ticket (new, open, closed, ...)
    """
    
    class Meta:
        verbose_name = _("Ticket State")
        verbose_name_plural = _('Ticket States')

class TicketStates(reports.Report):
    model = TicketState
    column_names = 'name *'



class Ticket(mixins.AutoUser,mixins.ProjectRelated,mixins.CreatedModified):
    """
    """
    
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')
        
    #~ project = models.ForeignKey('tickets.Project',blank=True,null=True)
    summary = models.CharField(_("Summary"),max_length=200,blank=True)
    state = models.ForeignKey('tickets.TicketState',blank=True,null=True)
    description = fields.RichTextField(_("Description"),blank=True,format='plain')
    #~ start_date = models.DateField(
        #~ verbose_name=_("Start date"),
        #~ blank=True,null=True)
    
    def __unicode__(self):
        return u"#%d (%s)" % (self.id,self.summary)


class Tickets(reports.Report):
    model = 'tickets.Ticket'

class TicketsByProject(Tickets):
    fk_name = 'project'

#~ class EventsByTicket(cal.Events):
    #~ fk_name = 'ticket'
    
    
class Comment(mixins.AutoUser,mixins.CreatedModified):
  
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _('Comments')

    ticket = models.ForeignKey('tickets.Ticket')
    description = fields.RichTextField(_("Description"),blank=True,format='plain')
    
class Comments(reports.Report):
    model = Comment
    column_names = 'created description user *'
    
class CommentsByTicket(Comments):
    fk_name = 'ticket'

if settings.LINO.user_model:    
    class MyProjects(mixins.ByUser):
        model = 'tickets.Project'
        order_by = ["name"]
        column_names = 'name id summary *'
        
    class MyTickets(mixins.ByUser):
        model = 'tickets.Ticket'
        order_by = ["created","id"]
        column_names = 'created id project summary state *'
        
    class MyComments(mixins.ByUser):
        model = 'tickets.Comment'
        order_by = ["-modified"]
        column_names = 'modified description *'
    

#~ if reports.is_installed('cal'):

    #~ reports.inject_field(cal.Event,
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
    m.add_action('tickets.MyProjects')
    m.add_action('tickets.MyTickets')
    m.add_action('tickets.MyComments')
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action('tickets.ProjectTypes')
    m.add_action('tickets.TicketStates')
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("tickets",_("Tickets"))
    m.add_action('tickets.Projects')
    m.add_action('tickets.Tickets')
    m.add_action('tickets.Comments')
  