# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module adds models for Projects, Milestones, Tickets & Co.

A **Project** is something into which somebody (the `partner`) invests
time, energy and money.  The partner can be either external or the
runner of the site.  Projects form a tree: each Project can have a
`parent` (another Project for which it is a sub-project).

A **Ticket** is a concrete question or problem formulated by a
`reporter` (a user).  A Ticket is always related to one and only one
Project.  It may be related to other tickets which may belong to other
projects.

Projects are handled by their *name* while Tickets are handled by
their *number*.

A **Milestone** is a named step of evolution of a Project.  For
software projects we usually call them a "release" and they are named
by a version number.

"""

from django.conf import settings
from django.db import models

from lino import mixins
from lino.api import dd, rt, _, pgettext

from lino.utils.xmlgen.html import E

blogs = dd.resolve_app('blogs')

from lino.modlib.tickets.utils import TicketStates, DependencyTypes
from lino.modlib.cal.mixins import daterange_text
from lino.modlib.users.mixins import UserAuthored


class TimeInvestment(dd.Model):

    class Meta:
        abstract = True

    planned_time = models.TimeField(
        _("Planned time"),
        blank=True, null=True)

    invested_time = models.TimeField(
        _("Invested time"), blank=True, null=True, editable=False)


class ProjectType(mixins.PrintableType, mixins.BabelNamed):

    "Deserves more documentation."

    templates_group = 'tickets/Project'

    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')


class ProjectTypes(dd.Table):
    model = 'tickets.ProjectType'
    column_names = 'name build_method template *'


#~ class Repository(UserAuthored):
    #~ class Meta:
        #~ verbose_name = _("Repository")
        #~ verbose_name_plural = _('Repositories')

    #~ ref = dd.NullCharField(_("Reference"),max_length=40,blank=True,null=True,unique=True)
    #~ srcref_url_template = models.CharField(_("Name"),max_length=200)


class Project(TimeInvestment, mixins.Referrable):
    """A **project** is something on which several users work together.
    """
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _('Projects')

    name = models.CharField(_("Name"), max_length=200)
    parent = models.ForeignKey(
        'self', blank=True, null=True, verbose_name=_("Parent"))
    type = models.ForeignKey('tickets.ProjectType', blank=True, null=True)
    description = dd.RichTextField(_("Description"), blank=True,
                                   format='plain')
    srcref_url_template = models.CharField(blank=True, max_length=200)
    changeset_url_template = models.CharField(blank=True, max_length=200)

    def __unicode__(self):
        return self.ref or self.name


class ProjectDetail(dd.FormLayout):
    main = "general tickets history"

    general = dd.Panel("""
    ref name parent type
    description:30 ProjectsByProject:30
    # cal.EventsByProject
    """, label=_("General"))

    tickets = dd.Panel("""
    TicketsByProject #SessionsByProject
    """, label=_("Tickets"))

    history = dd.Panel("""
    srcref_url_template changeset_url_template
    MilestonesByProject
    """, label=_("Timeline"))


class Projects(dd.Table):
    model = 'tickets.Project'
    detail_layout = ProjectDetail()


class ProjectsByProject(Projects):
    master_key = 'parent'
    label = _("Sub-projects")
    column_names = "ref name *"


# class MyProjects(Projects, ByUser):
#     order_by = ["name"]
#     column_names = 'ref name id *'

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


class Milestone(dd.Model):  # mixins.Referrable):
    """
    """
    class Meta:
        verbose_name = _("Milestone")
        verbose_name_plural = _('Milestones')
        ordering = ['project', 'label']

    project = dd.ForeignKey(
        'tickets.Project',
        related_name='milestones_by_project')
    label = models.CharField(_("Label"), max_length=20)
    expected = models.DateField(_("Expected for"), blank=True, null=True)
    reached = models.DateField(_("Reached"), blank=True, null=True)
    #~ description = dd.RichTextField(_("Description"),blank=True,format='plain')

    #~ def __unicode__(self):
        #~ return self.label

    def __unicode__(self):
        return "{0}:{1}".format(self.project, self.label)


class Milestones(dd.Table):
    model = 'tickets.Milestone'
    detail_layout = """
    project label expected reached id
    TicketsFixed TicketsReported
    """
    insert_layout = """
    project label
    """


class MilestonesByProject(Milestones):
    master_key = 'project'
    column_names = "label expected reached *"


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


class Ticket(UserAuthored, mixins.CreatedModified, TimeInvestment):
    """
    """
    workflow_state_field = 'state'

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')

    project = dd.ForeignKey('tickets.Project', blank=True, null=True)
    summary = models.CharField(
        pgettext("Ticket", "Summary"), max_length=200,
        blank=True,
        help_text=_("Short summary of the problem."))
    description = dd.RichTextField(
        _("Description"), blank=True, format='plain')

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
        settings.SITE.user_model,
        related_name="assigned_tickets",
        blank=True, null=True,
        help_text=_("The user who works on this ticket."))
    #~ state = models.ForeignKey('tickets.TicketState',blank=True,null=True)
    state = TicketStates.field(blank=True)
    closed = models.DateTimeField(_("Closed since"), editable=False, null=True)
    #~ start_date = models.DateField(
        #~ verbose_name=_("Start date"),
        #~ blank=True,null=True)

    def __unicode__(self):
        return u"#%d (%s)" % (self.id, self.summary)

    @dd.chooser()
    def reported_for_choices(cls, project):
        if not project:
            return []
        return project.milestones_by_project.filter(
            reached__isnull=False)

    @dd.chooser()
    def fixed_for_choices(cls, project):
        if not project:
            return []
        return project.milestones_by_project.all()

    @dd.displayfield(_("Overview"))
    def overview(self, ar):
        return ar.obj2html(self)


class TicketEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = TicketEvents.add_item
add('10', _("Opened"), 'opened')
add('20', _("Closed"), 'closed')


class TicketDetail(dd.DetailLayout):
    main = "general time"

    general = dd.Panel("""
    summary assigned_to project reported_for id 
    user created modified state workflow_buttons fixed_for
    description
    ParentsByTicket ChildrenByTicket
    """, label=_("General"))

    time = dd.Panel("""
    planned_time invested_time
    clocking.SessionsByTicket
    """, label=_("Time"))


class Tickets(dd.Table):
    model = 'tickets.Ticket'
    detail_layout = TicketDetail()
    insert_layout = dd.FormLayout("""
    summary
    project
    """, window_size=(50, 'auto'))

    parameters = mixins.ObservedPeriod(
        user=dd.ForeignKey(
            settings.SITE.user_model,
            blank=True, null=True,
            help_text=_("Only rows authored by this user.")),
        assigned_to=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Assigned to"),
            blank=True, null=True,
            help_text=_("Only rows authored by this user.")),
        project=dd.ForeignKey(
            'tickets.Project',
            blank=True, null=True),
        state=TicketStates.field(
            blank=True, help_text=_("Only rows having this state.")),
        observed_event=TicketEvents.field(blank=True))
    params_layout = """user assigned_to project state \
    start_date end_date observed_event"""
    simple_parameters = ('user', 'assigned_to', 'state')

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Tickets, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.project:
            qs = qs.filter(project=pv.project)

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

        if pv.project:
            yield unicode(pv.project)


class UnassignedTickets(Tickets):
    column_names = "summary project user *"


class TicketsByProject(Tickets):
    master_key = 'project'
    column_names = "summary user planned_time invested_time *"
    auto_fit_column_widths = True


class RecentTickets(Tickets):
    label = _("Recent tickets")
    order_by = ["-modified", "id"]
    column_names = 'modified id overview state *'


# class TicketsByPartner(Tickets):
#     master_key = 'partner'
#     column_names = "summary project user *"


class TicketsFixed(Tickets):
    label = _("Tickets Fixed")
    master_key = 'fixed_for'
    column_names = "id summary user *"
    editable = False


class TicketsReported(Tickets):
    label = _("Tickets Reported")
    master_key = 'reported_for'
    column_names = "id summary user *"
    editable = False


class MyOwnedTickets(Tickets):
    order_by = ["-created", "id"]
    column_names = 'created id project summary state *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyOwnedTickets, self).param_defaults(ar, **kw)
        u = ar.get_user()
        if u is not None:
            kw.update(user=u)
        return kw


class MyAssignedTickets(Tickets):
    label = _("Tickets assigned to me")
    order_by = ["-created", "id"]
    column_names = 'created id project summary state *'
    # slave_grid_format = 'summary'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyAssignedTickets, self).param_defaults(ar, **kw)
        u = ar.get_user()
        if u is not None:
            kw.update(assigned_to=u)
        return kw

    @classmethod
    def get_slave_summary(self, obj, ar):
        buttons = []
        # sar = ar.spawn(self, master_instance=ar.get_user())
        u = ar.get_user()
        sar = self.insert_action.request_from(ar, known_values=dict(user=u))
        qs = Ticket.objects.filter(user=u)
        # qs = qs.exclude(state=TicketStates.active)
        for ticket in qs:
            # btn = ar.instance_action_button(
            #     ticket.start_session, label=str(ticket.id))
            sar.known_values.update(ticket=ticket)
            btn = sar.ar2button(None, str(ticket.id))
            buttons.append(btn)

        return E.div(*buttons)


def you_are_busy_messages(ar):
    """Yield :message:`You are busy in XXX` messages for the welcome
page."""

    events = rt.modules.cal.Event.objects.filter(
        user=ar.get_user(), guest__state=GuestStates.busy).distinct()
    if events.count() > 0:
        chunks = [unicode(_("You are busy in "))]
        sep = None
        for evt in events:
            if sep:
                chunks.append(sep)
            ctx = dict(id=evt.id)
            if evt.event_type is None:
                ctx.update(label=unicode(evt))
            else:
                ctx.update(label=evt.event_type.event_label)

            if evt.project is None:
                txt = _("{label} #{id}").format(**ctx)
            else:
                ctx.update(project=unicode(evt.project))
                txt = _("{label} with {project}").format(**ctx)
            chunks.append(ar.obj2html(evt, txt))
            chunks += [
                ' (',
                ar.instance_action_button(evt.close_meeting),
                ')']
            sep = ', '
        chunks.append('. ')
        yield E.span(*chunks)
            

#dd.add_welcome_handler(you_are_busy_messages)


