# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Part of the :xfile:`models` module for the :mod:`lino.modlib.cal` app.

Defines the :class:`Task` model and its tables.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins
from lino.modlib.office.roles import OfficeUser, OfficeStaff

from .models import Component

from .workflows import TaskStates


class Task(Component):
    """A Task is when a user plans to to something
    (and optionally wants to get reminded about it).

    .. attribute:: state
     
        The state of this Task. one of :class:`TaskStates`


    """
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        abstract = dd.is_abstract_model(__name__, 'Task')

    due_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Due date"))
    due_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Due time"))
    # ~ done = models.BooleanField(_("Done"),default=False) # iCal:COMPLETED
    # iCal:PERCENT
    percent = models.IntegerField(_("Duration value"), null=True, blank=True)
    state = TaskStates.field(default=TaskStates.todo)  # iCal:STATUS
    # ~ status = models.ForeignKey(TaskStatus,verbose_name=_("Status"),blank=True,null=True) # iCal:STATUS

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

    def before_ui_save(self, ar, **kw):
        if self.state == TaskStates.todo:
            self.state = TaskStates.started
        return super(Task, self).before_ui_save(ar, **kw)

    #~ def on_user_change(self,request):
        #~ if not self.state:
            #~ self.state = TaskState.todo
        #~ self.user_modified = True

    def is_user_modified(self):
        return self.state != TaskStates.todo

    @classmethod
    def on_analyze(cls, lino):
        #~ lino.TASK_AUTO_FIELDS = dd.fields_list(cls,
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(
            cls, """start_date start_time summary""")
        super(Task, cls).on_analyze(lino)

    #~ def __unicode__(self):
        # ~ return "#" + str(self.pk)


class Tasks(dd.Table):
    help_text = _("""A calendar task is something you need to do.""")
    model = 'cal.Task'
    required_roles = dd.required(OfficeStaff)
    column_names = 'start_date summary workflow_buttons *'
    order_by = ["start_date", "start_time"]

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
    """, window_size=(50, 'auto'))

    params_panel_hidden = True

    parameters = mixins.ObservedPeriod(
        user=dd.ForeignKey(settings.SITE.user_model,
                           verbose_name=_("Managed by"),
                           blank=True, null=True,
                           help_text=_("Only rows managed by this user.")),
        project=dd.ForeignKey(settings.SITE.project_model,
                              blank=True, null=True),
        state=TaskStates.field(blank=True,
                               help_text=_("Only rows having this state.")),
    )

    params_layout = """
    start_date end_date user state project
    """

    @classmethod
    def get_request_queryset(self, ar):
        #~ logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(Tasks, self).get_request_queryset(ar)

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
    def get_title_tags(self, ar):
        for t in super(Tasks, self).get_title_tags(ar):
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
    def apply_cell_format(self, ar, row, col, recno, td):
        """
        Enhance today by making background color a bit darker.
        """
        if row.start_date == settings.SITE.today():
            td.attrib.update(bgcolor="gold")


class TasksByController(Tasks):
    master_key = 'owner'
    required_roles = dd.required(OfficeUser)
    column_names = 'start_date summary workflow_buttons id'
    #~ hidden_columns = set('owner_id owner_type'.split())
    auto_fit_column_widths = True

if settings.SITE.user_model:

    class TasksByUser(Tasks):
        """
        Shows the list of automatically generated tasks for this user.
        """
        master_key = 'user'
        required_roles = dd.required(OfficeUser)

    class MyTasks(Tasks):
        """All my tasks.  Only those whose start_date is today or in the
future.  This table is used in
:meth:`lino_welfare.projects.base.Site.get_admin_item`.

        """
        label = _("My tasks")
        required_roles = dd.required(OfficeUser)
        help_text = _("Table of all my tasks.")
        column_names = 'start_date summary workflow_buttons project'
        params_panel_hidden = True

        @classmethod
        def param_defaults(self, ar, **kw):
            kw = super(MyTasks, self).param_defaults(ar, **kw)
            kw.update(user=ar.get_user())
            kw.update(state=TaskStates.todo)
            kw.update(start_date=settings.SITE.today())
            return kw


if settings.SITE.project_model:

    class TasksByProject(Tasks):
        required_roles = dd.required(OfficeUser)
        master_key = 'project'
        column_names = 'start_date user summary workflow_buttons *'

