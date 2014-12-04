# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module adds models for Projects, Milestones, Tickets and Sessions.

A **Project** is something into which somebody invests time, energy and money.
Projects form a tree: each Project can have a `parent` 
(another Project for which it is a sub-project).

A **Milestone** is a named step of evolution of a Project.
For software projects we usually call them a "release" and they are 
named by a version number.

A **Ticket** is a concrete question or problem formulated 
by a `reporter` (a user). 
A Ticket is always related to one and only one Project.
It may be related to other tickets which may belong to other projects.

A **Session** is when an employee (a User) 
works during a given lapse of time on a given Ticket.

All the Sessions related to a given Project represent the time 
invested into that Project.

Projects are handled by their *name* while Tickets are handled by their *number*.

Extreme case of a session:

- I start to work on an existing ticket #1 at 9:23.  A customer phones
  at 10:17 with a question. Created #2.  That call is interrupted
  several times (by the customer himself).  During the first
  interruption another customer calls, with another problem (ticket
  #3) which we solve together within 5 minutes.  During the second
  interruption of #2 (which lasts 7 minutes) I make a coffee break.

  During the third interruption I continue to analyze the customer's
  problem.  When ticket #2 is solved, I decided that it's not worth to
  keep track of each interruption and that the overall session time
  for this ticket can be estimated to 0:40.

  ::

    Ticket start end    Pause  Duration
    #1     9:23  13:12  0:45
    #2     10:17 11:12  0:12       0:43   
    #3     10:23 10:28             0:05

"""
import cgi
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from lino import mixins
from lino import dd, rt
#~ from lino.modlib.cal import models as cal

blogs = dd.resolve_app('blogs')

from lino.modlib.tickets.utils import TicketStates, DependencyTypes
from lino.modlib.cal.mixins import daterange_text


class ProjectType(mixins.PrintableType, mixins.BabelNamed):

    "Deserves more documentation."

    templates_group = 'tickets/Project'

    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')


class ProjectTypes(dd.Table):
    model = ProjectType
    column_names = 'name build_method template *'


class SessionType(mixins.BabelNamed):

    "Deserves more documentation."

    class Meta:
        verbose_name = _("Session Type")
        verbose_name_plural = _('Session Types')


class SessionTypes(dd.Table):
    model = SessionType
    column_names = 'name *'

#~ class Repository(mixins.UserAuthored):
    #~ class Meta:
        #~ verbose_name = _("Repository")
        #~ verbose_name_plural = _('Repositories')

    #~ ref = dd.NullCharField(_("Reference"),max_length=40,blank=True,null=True,unique=True)
    #~ srcref_url_template = models.CharField(_("Name"),max_length=200)


class Project(mixins.UserAuthored, mixins.Printable, mixins.Referrable):

    """
    The `user` ("Autor") of a project is the User who manages that Project.
    """
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _('Projects')

    #~ ref = dd.NullCharField(_("Reference"),max_length=40,blank=True,null=True,unique=True)
    name = models.CharField(_("Name"), max_length=200)
    parent = models.ForeignKey(
        'self', blank=True, null=True, verbose_name=_("Parent"))
    type = models.ForeignKey('tickets.ProjectType', blank=True, null=True)
    #~ summary = models.CharField(_("Summary"),max_length=200,blank=True)
    #~ description = dd.RichTextField(_("Description"),blank=True,format='plain')
    description = dd.RichTextField(_("Description"), blank=True,
                                   format='plain')
    srcref_url_template = models.CharField(blank=True, max_length=200)
    changeset_url_template = models.CharField(blank=True, max_length=200)

    def __unicode__(self):
        return self.name


class ProjectDetail(dd.FormLayout):
    main = "general tickets"

    general = dd.Panel("""
    ref name parent
    type user
    description ProjectsByProject
    # cal.EventsByProject
    """, label=_("General"))

    tickets = dd.Panel("""
    TicketsByProject #SessionsByProject
    """, label=_("Tickets"))

    history = dd.Panel("""
    srcref_url_template changeset_url_template
    MilestonesByProject
    """, label=_("Tickets"))


class Projects(dd.Table):
    model = 'tickets.Project'
    detail_layout = ProjectDetail()


class ProjectsByProject(Projects):
    master_key = 'parent'
    label = _("Sub-projects")
    column_names = "ref name *"


# class ProjectsByPartner(Projects):
#     master_key = 'partner'
#     column_names = "ref name *"


class Vote(dd.Model):
    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _('Votes')

    ticket = dd.ForeignKey('tickets.Ticket')
    partner = dd.ForeignKey('contacts.Partner')
    remark = models.CharField(_("Remark"), max_length=200, blank=True)


class Votes(dd.Table):
    model = 'tickets.Vote'


class VotesByTicket(Votes):
    master_key = 'ticket'
    column_names = "partner remark *"


class VotesByPartner(Votes):
    master_key = 'partner'
    column_names = "ticket remark *"


class Milestone(mixins.Referrable):

    """
    """
    class Meta:
        verbose_name = _("Milestone")
        verbose_name_plural = _('Milestones')

    project = dd.ForeignKey('tickets.Project', blank=True, null=True)
    #~ label = models.CharField(_("Label"),max_length=20)
    expected = models.DateField(_("Expected for"), blank=True, null=True)
    reached = models.DateField(_("Reached"), blank=True, null=True)
    #~ description = dd.RichTextField(_("Description"),blank=True,format='plain')

    #~ def __unicode__(self):
        #~ return self.label


class Milestones(dd.Table):
    model = Milestone
    detail_layout = """
    project ref expected reached id
    TicketsFixed TicketsReported
    """
    insert_layout = dd.FormLayout("""
    project ref
    """, window_size=(40, 'auto'))


class MilestonesByProject(Milestones):
    master_key = 'project'
    column_names = "ref expected reached *"


class Ticket(mixins.AutoUser, mixins.CreatedModified):

    """
    """
    workflow_state_field = 'state'

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')

    reported_for = dd.ForeignKey(
        'tickets.Milestone',
        related_name='tickets_reported',
        verbose_name='Reported for',
        blank=True, null=True,
        help_text=_("Milestone for which this ticket has been reported."))
    fixed_for = dd.ForeignKey(
        'tickets.Milestone',
        related_name='tickets_fixed',
        verbose_name='Fixed for',
        blank=True, null=True,
        help_text=_("The milestone for which this ticket has been fixed."))
    assigned_to = dd.ForeignKey(
        'users.User',
        blank=True, null=True,
        help_text=_("The user who works on this ticket."))
    project = models.ForeignKey('tickets.Project', blank=True, null=True)
    summary = models.CharField(_("Summary"), max_length=200,
                               blank=True,
                               help_text=_("Short summary of the problem."))
    #~ state = models.ForeignKey('tickets.TicketState',blank=True,null=True)
    state = TicketStates.field(blank=True)
    closed = models.DateTimeField(_("Closed since"), editable=False, null=True)
    description = dd.RichTextField(_("Description"), blank=True,
                                   format='plain')
    #~ start_date = models.DateField(
        #~ verbose_name=_("Start date"),
        #~ blank=True,null=True)

    @dd.virtualfield(models.TimeField(_("Time")))
    def time(self, ar):
        return self.sessions_time

    def __unicode__(self):
        return u"#%d (%s)" % (self.id, self.summary)

    @dd.chooser()
    def reported_for_choices(cls, project):
        if not project:
            return []
        return project.tickets_milestone_set_by_project.filter(
            reached__isnull=False)

    @dd.chooser()
    def fixed_for_choices(cls, project):
        if not project:
            return []
        return project.tickets_milestone_set_by_project.all()


class TicketEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = TicketEvents.add_item
add('10', _("Opened"), 'opened')
add('20', _("Closed"), 'closed')


class Tickets(dd.Table):
    model = 'tickets.Ticket'
    detail_layout = """
    summary assigned_to project reported_for id
    user created modified state workflow_buttons fixed_for
    description
    ParentsByTicket ChildrenByTicket
    SessionsByTicket #EntriesByTicket
    """
    insert_layout = dd.FormLayout("""
    summary
    project
    """, window_size=(50, 'auto'))

    parameters = dd.ObservedPeriod(
        user=dd.ForeignKey(settings.SITE.user_model,
                           blank=True, null=True,
                           help_text=_("Only rows authored by this user.")),
        project=dd.ForeignKey(
            settings.SITE.project_model,
            blank=True, null=True),
        state=TicketStates.field(
            blank=True, help_text=_("Only rows having this state.")),
        observed_event=TicketEvents.field(blank=True))
    params_layout = """user project state \
    start_date end_date observed_event"""

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Tickets, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.user:
            qs = qs.filter(user=pv.user)

        if settings.SITE.project_model is not None and pv.project:
            qs = qs.filter(project=pv.project)

        if pv.state:
            qs = qs.filter(state=pv.state)

        if pv.observed_event == TicketEvents.opened:
            if pv.start_date:
                qs = qs.filter(created__gte=pv.start_date)
            if pv.end_date:
                qs = qs.filter(created__lte=pv.end_date)
        elif pv.observed_event == TicketEvents.closed:
            if pv.start_date:
                qs = qs.filter(closed__gte=pv.start_date)
            if pv.end_date:
                qs = qs.filter(closed__lte=pv.end_date)

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Tickets, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.start_date or pv.end_date:
            yield daterange_text(
                pv.start_date,
                pv.end_date)

        if pv.state:
            yield unicode(pv.state)

        if pv.user:
            yield unicode(pv.user)

        if settings.SITE.project_model is not None and pv.project:
            yield unicode(pv.project)

        if pv.observed_event:
            yield unicode(self.parameters['observed_event'].verbose_name) \
                + ' ' + unicode(pv.observed_event)


class UnassignedTickets(Tickets):
    column_names = "summary project user *"


class TicketsByProject(Tickets):
    master_key = 'project'
    column_names = "summary user time *"
    # parameters = dict(
    #     today=models.DateField(_("Date"), blank=True)
    # )

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(TicketsByProject, self).get_request_queryset(ar)
        #~ if ar.param_values.today is not None:
        return qs.annotate(sessions_time=models.Sum('sessions__time'))


class RecentTickets(Tickets):
    label = _("Recent tickets")
    order_by = ["-modified", "id"]
    column_names = 'modified id project summary state *'


# class TicketsByPartner(Tickets):
#     master_key = 'partner'
#     column_names = "summary project user *"


class TicketsFixed(Tickets):
    label = _("Tickets Fixed")
    master_key = 'fixed_for'
    column_names = "summary user *"
    editable = False


class TicketsReported(Tickets):
    label = _("Tickets Reported")
    master_key = 'reported_for'
    column_names = "summary user *"
    editable = False


class Dependency(dd.Model):
    class Meta:
        verbose_name = _("Dependency")
        verbose_name_plural = _('Dependencies')

    parent = dd.ForeignKey('tickets.Ticket', related_name="children")
    child = dd.ForeignKey('tickets.Ticket', related_name="parents")
    dependency_type = DependencyTypes.field()


class Dependencies(dd.Table):
    model = 'tickets.Dependency'


class ChildrenByTicket(Dependencies):
    master_key = 'parent'
    column_names = "dependency_type child *"


class ParentsByTicket(Dependencies):
    master_key = 'child'
    column_names = "dependency_type parent *"


class Session(mixins.AutoUser):

    """
    A Session is when a user works on a given ticket.
    """
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _('Sessions')

    # partner = models.ForeignKey(
    #     'contacts.Partner',
    #     blank=True, null=True,
    #     help_text=_("The partner to be invoiced for this session."))
    # project = models.ForeignKey('tickets.Project',blank=True,null=True)
    ticket = models.ForeignKey('tickets.Ticket',
                               blank=True, null=True,
                               related_name='sessions')
    summary = models.CharField(_("Summary"), max_length=200,
                               blank=True,
                               help_text=_("Short summary of the session."))
    description = dd.RichTextField(_("Description"), blank=True,
                                   format='plain')
    date = models.DateField(verbose_name=_("Date"), blank=True)
    start_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Start time"))
    end_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("End Time"))
    break_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Break Time"))
    time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Time"))
    is_private = models.BooleanField(
        verbose_name=_("is private"), default=False)

    def __unicode__(self):
        if self.start_time and self.end_time:
            return u"%s %s-%s" % (
                self.date.strftime(settings.SITE.date_format_strftime),
                self.start_time.strftime(settings.SITE.time_format_strftime),
                self.end_time.strftime(settings.SITE.time_format_strftime))
        return "%s # %s" % (self._meta.verbose_name, self.pk)

    def save(self, *args, **kwargs):
        if self.date is None and not settings.SITE.loading_from_dump:
            self.date = settings.SITE.today()
        super(Session, self).save(*args, **kwargs)


class Sessions(dd.Table):
    model = Session
    column_names = 'date start_time end_time break_time summary user *'
    order_by = ['date', 'start_time']
    detail_layout = """
    date start_time end_time break_time ticket
    user id
    description
    # EntriesBySession
    """
    stay_in_grid = True


class SessionsByTicket(Sessions):
    master_key = 'ticket'


# class SessionsByProject(Sessions):
#     master_key = 'project'

if settings.SITE.user_model:

    class MySessions(Sessions, mixins.ByUser):
        order_by = ['date', 'start_time']
        column_names = 'date start_time end_time break_time ticket summary *'

    class MySessionsByDate(MySessions):
        #~ master_key = 'date'
        order_by = ['start_time']
        label = _("My sessions by date")
        column_names = 'start_time end_time break_time ticket summary *'

        parameters = dict(
            today=models.DateField(_("Date"),
                                   blank=True, default=settings.SITE.today),
        )

        @classmethod
        def get_request_queryset(self, ar):
            qs = super(MySessions, self).get_request_queryset(ar)
            #~ if ar.param_values.date:
            return qs.filter(date=ar.param_values.today)
            #~ return qs

        @classmethod
        def create_instance(self, ar, **kw):
            kw.update(date=ar.param_values.today)
            return super(MySessions, self).create_instance(ar, **kw)


if blogs:

    dd.inject_field(
        'blogs.Entry',
        'ticket',
        models.ForeignKey(
            "tickets.Ticket",
            blank=True, null=True,
            # verbose_name=_("Local job office"),
            # related_name='job_office_sites'
            help_text="""The Ticket attributed to this Entry."""))

    class EntriesByTicket(blogs.Entries):
        master_key = 'ticket'

    class EntriesBySession(blogs.Entries):

        """The Blog Entries linked to *the Ticket of* a Session.
        
        Blog Entries are not directly linked to a Session, but in the
        Detail of a Session we want to display a table of related blog
        entries.

        """
        master = 'tickets.Session'

        @classmethod
        def get_request_queryset(self, ar):
            if ar.master_instance is not None:
                if ar.master_instance.ticket is not None:
                    qs = blogs.Entries.get_request_queryset(self, ar)
                    return qs.filter(ticket=ar.master_instance.ticket)
            return []

        # @classmethod
        # def get_filter_kw(self, ar, **kw):
        #     if ar.master_instance is not None:
        #         if ar.master_instance.ticket is not None:
        #             kw.update(ticket=ar.master_instance.ticket)
        #             return kw
        #     # otherwise return None


else:

    Tickets.detail_layout = Tickets.detail_layout.replace(
        ' EntriesByTicket', '')


if settings.SITE.user_model:

    class MyProjects(Projects, mixins.ByUser):
        order_by = ["name"]
        column_names = 'ref name id *'

    class MyTickets(Tickets, mixins.ByUser):
        order_by = ["-created", "id"]
        column_names = 'created id project summary state *'

    # class MyOpenTickets(Tickets, mixins.ByUser):
    #     order_by = ["-created", "id"]
    #     column_names = 'created id project summary state *'
    #     filter = models.Q(closed__isnull=True)


#~ if dd.is_installed('cal'):

    #~ dd.inject_field(cal.Event,
        #~ 'ticket',
        #~ models.ForeignKey("tickets.Ticket",
            #~ blank=True,null=True,
            # ~ # verbose_name=_("Local job office"),
            # ~ # related_name='job_office_sites'
            #~ ),
        #~ """The Ticket attributed to this event.
        #~ """)


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("tickets", _("Tickets"))
    m.add_action(MyProjects)
    # m.add_action(MyOpenTickets)
    m.add_action(MyTickets)
    m.add_action(MySessions)
    m.add_action(MySessionsByDate)


def setup_my_menu(site, ui, profile, m):
    pass


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("tickets", _("Tickets"))
    m.add_action(ProjectTypes)
    #~ m.add_action(TicketStates)
    m.add_action(SessionTypes)


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("tickets", _("Tickets"))
    m.add_action(Projects)
    m.add_action(Tickets)
    m.add_action(Sessions)
    m.add_action('tickets.Milestones')
    m.add_action('tickets.Dependencies')
    m.add_action('tickets.Votes')
