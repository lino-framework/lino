# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
Part of the :xfile:`models` module for the :mod:`lino.modlib.cal` app.

Defines the :class:`Task` model and its tables.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime
import dateutil

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd

from lino.modlib.cal.models import Component

from lino.modlib.cal.workflows import TaskStates
    

class Task(Component):
    """
    A Task is when a user plans to to something 
    (and optionally wants to get reminded about it).
    """
    #~ workflow_state_field = 'state'
    
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        #~ abstract = True
        
    due_date = models.DateField(
        blank=True,null=True,
        verbose_name=_("Due date"))
    due_time = models.TimeField(
        blank=True,null=True,
        verbose_name=_("Due time"))
    #~ done = models.BooleanField(_("Done"),default=False) # iCal:COMPLETED
    percent = models.IntegerField(_("Duration value"),null=True,blank=True) # iCal:PERCENT
    state = TaskStates.field(default=TaskStates.todo) # iCal:STATUS
    #~ status = models.ForeignKey(TaskStatus,verbose_name=_("Status"),blank=True,null=True) # iCal:STATUS
    
    #~ @dd.action(_("Done"),required=dict(states=['','todo','started']))
    #~ @dd.action(TaskState.todo.text,required=dict(states=['']))
    #~ def mark_todo(self,ar):
        #~ self.state = TaskState.todo
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    
    #~ @dd.action(TaskState.done.text,required=dict(states=['','todo','started']))
    #~ def mark_done(self,ar):
        #~ self.state = TaskState.done
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    
    #~ @dd.action(TaskState.started.text,required=dict(states=['','todo']))
    #~ def mark_started(self,ar):
        #~ self.state = TaskState.started
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    
    #~ @dd.action(TaskState.sleeping.text,required=dict(states=['','todo']))
    #~ def mark_sleeping(self,ar):
        #~ self.state = TaskState.sleeping
        #~ self.save()
        #~ return ar.success_response(refresh=True)
    

    def before_ui_save(self,ar,**kw):
        if self.state == TaskStates.todo:
            self.state = TaskStates.started
        return super(Task,self).before_ui_save(ar,**kw)
        
    #~ def on_user_change(self,request):
        #~ if not self.state:
            #~ self.state = TaskState.todo
        #~ self.user_modified = True
        
    def is_user_modified(self):
        return self.state != TaskStates.todo
        
    @classmethod
    def on_analyze(cls,lino):
        #~ lino.TASK_AUTO_FIELDS = dd.fields_list(cls,
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls,
            '''start_date start_time summary''')
        super(Task,cls).on_analyze(lino)

    #~ def __unicode__(self):
        #~ return "#" + str(self.pk)
        

class Tasks(dd.Table):
    help_text = _("""A calendar task is something you need to do.
    """)
    #~ debug_permissions = True
    model = 'cal.Task'
    required = dd.required(user_groups='office',user_level='manager')
    column_names = 'start_date summary workflow_buttons *'
    order_by = ["-start_date","-start_time"]
    #~ hidden_columns = set('owner_id owner_type'.split())
    
    #~ detail_layout = """
    #~ start_date status due_date user  
    #~ summary 
    #~ created:20 modified:20 owner #owner_type #owner_id
    #~ description #notes.NotesByTask    
    #~ """
    detail_layout = """
    start_date due_date id workflow_buttons 
    summary 
    user project 
    #event_type owner created:20 modified:20   
    description #notes.NotesByTask
    """
    insert_layout = dd.FormLayout("""
    summary
    user project
    """,window_size=(50,'auto'))
    
    
    params_panel_hidden = True
    
    parameters = dd.ObservedPeriod(
        user = dd.ForeignKey(settings.SITE.user_model,
            verbose_name=_("Managed by"),
            blank=True,null=True,
            help_text=_("Only rows managed by this user.")),
        project = dd.ForeignKey(settings.SITE.project_model,
            blank=True,null=True),
        state = TaskStates.field(blank=True,
            help_text=_("Only rows having this state.")),
    )
    
    params_layout = """
    start_date end_date user state project
    """

    @classmethod
    def get_request_queryset(self,ar):
        #~ logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(Tasks,self).get_request_queryset(ar)
            
        if ar.param_values.user:
            qs = qs.filter(user=ar.param_values.user)
            
        if settings.SITE.project_model is not None and ar.param_values.project:
            qs = qs.filter(project=ar.param_values.project)

        if ar.param_values.state:
            qs = qs.filter(state=ar.param_values.state)
            
        if ar.param_values.start_date:
            qs = qs.filter(start_date__gte=ar.param_values.start_date)
        if ar.param_values.end_date:
            qs = qs.filter(start_date__lte=ar.param_values.end_date)
        return qs
        
    @classmethod
    def get_title_tags(self,ar):
        for t in super(Tasks,self).get_title_tags(ar):
            yield t
        if ar.param_values.start_date or ar.param_values.end_date:
            yield unicode(_("Dates %(min)s to %(max)s") % dict(
              min=ar.param_values.start_date or'...',
              max=ar.param_values.end_date or '...'))
              
        if ar.param_values.state:
            yield unicode(ar.param_values.state)
            
        if ar.param_values.user:
            yield unicode(ar.param_values.user)
            
        if settings.SITE.project_model is not None and ar.param_values.project:
            yield unicode(ar.param_values.project)
            

    @classmethod
    def apply_cell_format(self,ar,row,col,recno,td):
        """
        Enhance today by making background color a bit darker.
        """
        if row.start_date == datetime.date.today():
            td.attrib.update(bgcolor="gold")
    
    
    
class TasksByController(Tasks):
    master_key = 'owner'
    required = dd.required(user_groups='office')
    column_names = 'start_date summary workflow_buttons id'
    #~ hidden_columns = set('owner_id owner_type'.split())

if settings.SITE.user_model:    
  
    #~ class RemindersByUser(dd.Table):
    class TasksByUser(Tasks):
        """
        Shows the list of automatically generated tasks for this user.
        """
        #~ model = Task
        #~ label = _("Reminders")
        master_key = 'user'
        required = dd.required(user_groups='office')
        #~ column_names = "start_date summary *"
        #~ order_by = ["start_date"]
        #~ filter = Q(auto_type__isnull=False)
        
    class MyTasks(Tasks):
        label = _("My tasks")
        required = dd.required(user_groups='office')
        #~ required = dict()
        help_text = _("Table of all my tasks.")
        column_names = 'start_date summary workflow_buttons project'
        params_panel_hidden = True
        
        @classmethod
        def param_defaults(self,ar,**kw):
            kw = super(MyTasks,self).param_defaults(ar,**kw)
            kw.update(user=ar.get_user())
            kw.update(state=TaskStates.todo)
            kw.update(start_date=datetime.date.today())
            return kw
            
    
    class unused_MyTasksToDo(MyTasks):
        help_text = _("Table of my tasks marked 'to do'.")
        column_names = 'start_date summary workflow_buttons *'
        label = _("To-do list")
        #~ filter = Q(state__in=(TaskState.blank_item,TaskState.todo,TaskState.started))
        filter = Q(
            start_date__lte=datetime.date.today()+dateutil.relativedelta.relativedelta(days=1),
            state__in=(TaskStates.todo,TaskStates.started))
    
if settings.SITE.project_model:    
  
    class TasksByProject(Tasks):
        required = dd.required(user_groups='office')
        master_key = 'project'
        column_names = 'start_date user summary workflow_buttons *'
    

__all__ = ['Task','Tasks']
#~ __all__ = ['Task','Tasks','MyTasks','TasksByUser','TasksByController','TasksByProject']
