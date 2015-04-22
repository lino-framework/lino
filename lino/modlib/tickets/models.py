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

import datetime

from django.conf import settings
from django.db import models
from django.db.models import Q

from lino import mixins
from lino.api import dd, rt, _, pgettext

from lino.utils.xmlgen.html import E

blogs = dd.resolve_app('blogs')

from .utils import TicketStates, DependencyTypes
from lino.modlib.cal.mixins import daterange_text


class TimeInvestment(dd.Model):

    class Meta:
        abstract = True

    planned_time = models.TimeField(
        _("Planned time"),
        blank=True, null=True)

    invested_time = models.TimeField(
        _("Invested time"), blank=True, null=True, editable=False)


class ProjectType(mixins.BabelNamed):
    """The type of a :class:`Project`."""

    # templates_group = 'tickets/Project'

    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')


class ProjectTypes(dd.Table):
    model = 'tickets.ProjectType'
    column_names = 'name *'
    # column_names = 'name build_method template *'
    detail_layout = """id name
    ProjectsByType
    """


#~ class Repository(UserAuthored):
    #~ class Meta:
        #~ verbose_name = _("Repository")
        #~ verbose_name_plural = _('Repositories')

    #~ ref = dd.NullCharField(_("Reference"),max_length=40,blank=True,null=True,unique=True)
    #~ srcref_url_template = models.CharField(_("Name"),max_length=200)

# class Nicknamed(dd.Model):
#     class Meta:
#         abstract = True

#     def __unicode__(self):
#         txt = super(Nicknamed, self).__unicode__()
#         if self.nickname:
#             return u"{0} ({1})".format(txt, self.nickname)
#         return txt
#         #     return u"#{0} ({1})".format(self.id, self.nickname)
#         # return u"#{0}".format(self.id)

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
    description = dd.RichTextField(_("Description"), blank=True)
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
    SponsorshipsByProject
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
    column_names = "ref name type *"


class ProjectsByType(Projects):
    master_key = 'type'
    column_names = "ref name *"

# class MyProjects(Projects, ByUser):
#     order_by = ["name"]
#     column_names = 'ref name id *'

# class ProjectsByPartner(Projects):
#     master_key = 'partner'
#     column_names = "ref name *"


class Sponsorship(dd.Model):
    class Meta:
        verbose_name = _("Sponsorship")
        verbose_name_plural = _('Sponsorships')

    project = dd.ForeignKey('tickets.Project')
    partner = dd.ForeignKey('contacts.Partner')
    remark = models.CharField(_("Remark"), max_length=200, blank=True)


class Sponsorships(dd.Table):
    model = 'tickets.Sponsorship'


class SponsorshipsByProject(Sponsorships):
    master_key = 'project'
    column_names = "partner remark *"


class SponsorshipsByPartner(Sponsorships):
    master_key = 'partner'
    column_names = "project remark *"


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
        return u"{0}:{1}".format(self.project, self.label)


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
    label = _("Children")
    master_key = 'parent'
    column_names = "dependency_type child *"


class ParentsByTicket(Dependencies):
    label = _("Parents")
    master_key = 'child'
    column_names = "dependency_type parent *"


class CloseTicket(dd.Action):
    """
    """
    label = _("Close ticket")
    help_text = _("Mark this ticket as closed.")
    show_in_workflow = True
    show_in_bbar = False

    def get_action_permission(self, ar, obj, state):
        if obj.closed:
            return False
        return super(CloseTicket,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):

        def ok(ar2):
            now = datetime.datetime.now()
            for obj in ar.selected_rows:
                obj.closed = now
                obj.save()
                ar2.set_response(refresh=True)

        if True:
            ok(ar)
        else:
            msg = _("Close {0} tickets.").format(len(ar.selected_rows))
            ar.confirm(ok, msg, _("Are you sure?"))


class Ticket(mixins.CreatedModified, TimeInvestment):
    """
    """
    workflow_state_field = 'state'

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')

    project = dd.ForeignKey('tickets.Project', blank=True, null=True)
    nickname = models.CharField(_("Nickname"), max_length=50, blank=True)
    summary = models.CharField(
        pgettext("Ticket", "Summary"), max_length=200,
        blank=True,
        help_text=_("Short summary of the problem."))
    description = dd.RichTextField(_("Description"), blank=True)

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
        verbose_name=_("Assigned to"),
        related_name="assigned_tickets",
        blank=True, null=True,
        help_text=_("The user who works on this ticket."))
    reporter = dd.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Reporter"),
        related_name="reported_tickets",
        help_text=_("The user who reported this ticket."))
    #~ state = models.ForeignKey('tickets.TicketState',blank=True,null=True)
    state = TicketStates.field(default=TicketStates.new)
    closed = models.DateTimeField(_("Closed since"), editable=False, null=True)
    #~ start_date = models.DateField(
        #~ verbose_name=_("Start date"),
        #~ blank=True,null=True)

    close_tickert = CloseTicket()

    def on_create(self, ar):
        if self.reporter_id is None:
            u = ar.get_user()
            if u is not None:
                self.reporter = u
        super(Ticket, self).on_create(ar)

    def __unicode__(self):
        if self.nickname:
            return u"#{0} ({1})".format(self.id, self.nickname)
        return u"#{0}".format(self.id)
        # return u"#%d (%s)" % (self.id, self.summary)

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
        return E.span(ar.obj2html(self), ' ', self.summary)

# dd.update_field(Ticket, 'user', verbose_name=_("Reporter"))


class TicketEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = TicketEvents.add_item
add('10', _("Opened"), 'opened')
add('20', _("Closed"), 'closed')


class TicketDetail(dd.DetailLayout):
    main = "general time"

    general = dd.Panel("""
    summary:40 nickname:20 id
    project state workflow_buttons
    description
    clocking.SessionsByTicket
    """, label=_("General"))

    time = dd.Panel("""
    reporter reported_for fixed_for created modified closed
    planned_time invested_time assigned_to
    ParentsByTicket ChildrenByTicket
    """, label=_("Planning"))


class Tickets(dd.Table):
    required = dd.Required(auth=True)
    model = 'tickets.Ticket'
    auto_fit_column_widths = True
    detail_layout = TicketDetail()
    insert_layout = dd.FormLayout("""
    summary
    nickname project
    """, window_size=(60, 'auto'))

    parameters = mixins.ObservedPeriod(
        reporter=dd.ForeignKey(
            settings.SITE.user_model,
            blank=True, null=True,
            help_text=_("Only rows reporter by this user.")),
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
        active=dd.YesNo.field(
            blank=True,
            help_text=_("Only tickets which are not closed.")),
        observed_event=TicketEvents.field(blank=True))
    params_layout = """reporter assigned_to project state active \
    start_date end_date observed_event"""
    simple_parameters = ('reporter', 'assigned_to', 'state')

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
        # elif pv.observed_event == TicketEvents.active:
        #     qs = qs.filter(closed__isnull=True)

        if pv.active == dd.YesNo.yes:
            qs = qs.filter(closed__isnull=True)
        elif pv.active == dd.YesNo.no:
            qs = qs.exclude(closed__isnull=False)

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
    column_names = "summary project reporter *"


class TicketsByProject(Tickets):
    master_key = 'project'
    column_names = "summary reporter planned_time invested_time *"


class RecentTickets(Tickets):
    label = _("Recent tickets")
    order_by = ["-modified", "id"]
    column_names = 'overview reporter project state workflow_buttons:20 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(RecentTickets, self).param_defaults(ar, **kw)
        kw.update(active=dd.YesNo.yes)
        return kw


# class TicketsByPartner(Tickets):
#     master_key = 'partner'
#     column_names = "summary project user *"


class TicketsFixed(Tickets):
    label = _("Tickets Fixed")
    master_key = 'fixed_for'
    column_names = "id summary reporter *"
    editable = False


class TicketsReported(Tickets):
    label = _("Reported tickets")
    master_key = 'reported_for'
    column_names = "id summary reporter *"
    editable = False


class TicketsByReporter(Tickets):
    label = _("Reported tickets ")
    master_key = 'reporter'
    column_names = "id summary:60 workflow_buttons:20 *"


class MyOwnedTickets(Tickets):
    order_by = ["-created", "id"]
    column_names = 'created id project summary state *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyOwnedTickets, self).param_defaults(ar, **kw)
        u = ar.get_user()
        if u is not None:
            kw.update(reporter=u)
        return kw


class MyTickets(Tickets):
    label = _("My tickets")
    order_by = ["-created", "id"]
    column_names = 'created id project summary state *'
    # slave_grid_format = 'summary'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyTickets, self).param_defaults(ar, **kw)
        u = ar.get_user()
        if u is not None:
            kw.update(assigned_to=u)
        kw.update(state=TicketStates.active)
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        count = sar.get_total_count()
        if count > 0:
            txt = _("There are %d tickets for you.") % count
            yield ar.href_to_request(sar, txt)

    @classmethod
    def get_slave_summary(self, obj, ar):
        buttons = []
        # sar = ar.spawn(self, master_instance=ar.get_user())
        u = ar.get_user()
        sar = self.insert_action.request_from(
            ar, known_values=dict(reporter=u))
        qs = Ticket.objects.filter(reporter=u)
        # qs = qs.exclude(state=TicketStates.active)
        for ticket in qs:
            # btn = ar.instance_action_button(
            #     ticket.start_session, label=str(ticket.id))
            sar.known_values.update(ticket=ticket)
            btn = sar.ar2button(None, str(ticket.id))
            buttons.append(btn)

        return E.div(*buttons)
