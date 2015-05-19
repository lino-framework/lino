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

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Q

from lino import mixins
from lino.api import dd, rt, _, pgettext

from lino.utils.xmlgen.html import E

from lino.core.utils import gfk2lookup

blogs = dd.resolve_app('blogs')

from lino.modlib.cal.mixins import daterange_text
from lino.modlib.contacts.mixins import ContactRelated
# from lino.modlib.contenttypes.mixins import Controllable
# from lino.modlib.users.mixins import UserAuthored, ByUser
from lino.utils import join_elems

from .choicelists import TicketEvents, TicketStates, LinkTypes


class TimeInvestment(dd.Model):

    class Meta:
        abstract = True

    closed = models.BooleanField(_("Closed"), default=False)
    private = models.BooleanField(_("Private"), default=False)

    planned_time = models.TimeField(
        _("Planned time"),
        blank=True, null=True)

    invested_time = models.TimeField(
        _("Invested time"), blank=True, null=True, editable=False)


class ProjectType(mixins.BabelNamed):
    """The type of a :class:`Project`."""

    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')


class ProjectTypes(dd.Table):
    model = 'tickets.ProjectType'
    column_names = 'name *'
    detail_layout = """id name
    ProjectsByType
    """

class TicketType(mixins.BabelNamed):
    """The type of a :class:`Ticket`."""

    class Meta:
        verbose_name = _("Ticket type")
        verbose_name_plural = _('Ticket types')


class TicketTypes(dd.Table):
    model = 'tickets.TicketType'
    column_names = 'name *'
    detail_layout = """id name
    TicketsByType
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
#             return "{0} ({1})".format(txt, self.nickname)
#         return txt
#         #     return "#{0} ({1})".format(self.id, self.nickname)
#         # return "#{0}".format(self.id)

class Project(TimeInvestment, mixins.Referrable, ContactRelated):
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
    company #contact_person #contact_role private closed
    description:30 ProjectsByParent:30
    # cal.EventsByProject
    """, label=_("General"))

    tickets = dd.Panel("""
    #SponsorshipsByProject
    TicketsByProject #SessionsByProject
    """, label=_("Tickets"))

    history = dd.Panel("""
    srcref_url_template changeset_url_template
    MilestonesByProject
    """, label=_("Timeline"))


class Projects(dd.Table):
    model = 'tickets.Project'
    detail_layout = ProjectDetail()
    column_names = "ref name parent type *"


class ProjectsByParent(Projects):
    master_key = 'parent'
    label = _("Subprojects")
    column_names = "ref name type *"


class ProjectsByType(Projects):
    master_key = 'type'
    column_names = "ref name *"

# class MyProjects(Projects, ByUser):
#     order_by = ["name"]
#     column_names = 'ref name id *'


class ProjectsByCompany(Projects):
    master_key = 'company'
    column_names = "ref name *"


# class Sponsorship(dd.Model):
#     class Meta:
#         verbose_name = _("Sponsorship")
#         verbose_name_plural = _('Sponsorships')

#     project = dd.ForeignKey('tickets.Project')
#     partner = dd.ForeignKey('contacts.Partner')
#     remark = models.CharField(_("Remark"), max_length=200, blank=True)


# class Sponsorships(dd.Table):
#     model = 'tickets.Sponsorship'


# class SponsorshipsByProject(Sponsorships):
#     master_key = 'project'
#     column_names = "partner remark *"


# class SponsorshipsByPartner(Sponsorships):
#     master_key = 'partner'
#     column_names = "project remark *"


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


class Link(dd.Model):

    class Meta:
        verbose_name = _("Dependency")
        verbose_name_plural = _("Dependencies")

    type = LinkTypes.field(default=LinkTypes.requires)
    parent = dd.ForeignKey(
        'tickets.Ticket',
        verbose_name=_("Parent"),
        related_name='tickets_children')
    child = dd.ForeignKey(
        'tickets.Ticket',
        blank=True, null=True,
        verbose_name=_("Child"),
        related_name='tickets_parents')

    @dd.displayfield(_("Type"))
    def type_as_parent(self, ar):
        # print('20140204 type_as_parent', self.type)
        return self.type.as_parent()

    @dd.displayfield(_("Type"))
    def type_as_child(self, ar):
        # print('20140204 type_as_child', self.type)
        return self.type.as_child()

    def __unicode__(self):
        if self.type is None:
            return super(Link, self).__unicode__()
        return _("%(child)s is %(what)s") % dict(
            child=unicode(self.child),
            what=self.type_of_parent_text())

    def type_of_parent_text(self):
        return _("%(type)s of %(parent)s") % dict(
            parent=self.parent,
            type=self.type.as_child())


class Links(dd.Table):
    model = 'tickets.Link'
    required = dd.required(user_level='admin')
    stay_in_grid = True
    detail_layout = dd.FormLayout("""
    parent
    child
    type
    """, window_size=(40, 'auto'))


class LinksByTicket(Links):

    label = _("Dependencies")
    required = dd.required()
    master = 'tickets.Ticket'
    column_names = 'parent type_as_parent:10 child'
    slave_grid_format = 'summary'

    @classmethod
    def get_request_queryset(self, ar):
        mi = ar.master_instance  # a Person
        if mi is None:
            return
        Link = rt.modules.tickets.Link
        flt = Q(parent=mi) | Q(child=mi)
        return Link.objects.filter(flt).order_by(
            'child__modified', 'parent__modified')

    @classmethod
    def get_slave_summary(self, obj, ar):
        """The :meth:`summary view <lino.core.actors.Actor.get_slave_summary>`
        for :class:`LinksByTicket`.

        """
        # if obj.pk is None:
        #     return ''
        #     raise Exception("20150218")
        sar = self.request_from(ar, master_instance=obj)
        links = []
        for lnk in sar:
            if lnk.parent is None or lnk.child is None:
                pass
            else:
                if lnk.child_id == obj.id:
                    i = (lnk.type.as_child(), lnk.parent)
                else:
                    i = (lnk.type.as_parent(), lnk.child)
                links.append(i)

        def by_age(a, b):
            return cmp(b[1].modified, a[1].modified)

        try:
            links.sort(by_age)
        # except AttributeError:
        except (AttributeError, ValueError):
            # AttributeError: 'str' object has no attribute 'as_date'
            # possible when empty birth_date
            # ValueError: day is out of range for month
            pass

        tbt = dict()  # tickets by lnktype
        for lnktype, other in links:
            lst = tbt.setdefault(lnktype, [])
            txt = "#%d" % other.id
            lst.append(ar.obj2html(other, txt, title=other.summary))

        items = []
        for lnktype, lst in tbt.items():
            items.append(E.li(unicode(lnktype), ": ", *join_elems(lst, ', ')))
        elems = []
        if len(items) > 0:
            # elems += join_elems(items)
            # elems.append(l(*items))
            elems.append(E.ul(*items))
        else:
            elems.append(_("No dependencies."))

        # Buttons for creating relationships:
        sar = self.insert_action.request_from(ar)
        if ar.renderer.is_interactive and sar.get_permission():
            actions = []
            for lt in LinkTypes.objects():
                actions.append(E.br())
                sar.known_values.update(type=lt, parent=obj)
                sar.known_values.pop('child', None)
                btn = sar.ar2button(None, lt.as_parent(), icon_name=None)
                if not lt.symmetric:
                    # actions.append('/')
                    sar.known_values.update(type=lt, child=obj)
                    sar.known_values.pop('parent', None)
                    btn2 = sar.ar2button(None, lt.as_child(), icon_name=None)
                    # actions.append(btn)
                    btn = E.span(btn, '/', btn2)
                actions.append(btn)
                # actions.append(' ')
            # actions = join_elems(actions, E.br)

            if len(actions) > 0:
                elems += [E.br(), _("Create dependency as ")] + actions
        return E.div(*elems)



# class Dependency(dd.Model):
#     class Meta:
#         verbose_name = _("Dependency")
#         verbose_name_plural = _('Dependencies')

#     parent = dd.ForeignKey('tickets.Ticket', related_name="children")
#     child = dd.ForeignKey('tickets.Ticket', related_name="parents")
#     dependency_type = DependencyTypes.field()


# class Dependencies(dd.Table):
#     model = 'tickets.Dependency'


# class ChildrenByTicket(Dependencies):
#     label = _("Children")
#     master_key = 'parent'
#     column_names = "dependency_type child *"


# class ParentsByTicket(Dependencies):
#     label = _("Parents")
#     master_key = 'child'
#     column_names = "dependency_type parent *"



# class CloseTicket(dd.Action):
#     #label = _("Close ticket")
#     label = "\u2611"
#     help_text = _("Mark this ticket as closed.")
#     show_in_workflow = True
#     show_in_bbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is not None or obj.closed is not None:
#             return False
#         return super(CloseTicket, self).get_action_permission(ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         now = datetime.datetime.now()
#         for obj in ar.selected_rows:
#             obj.closed = now
#             obj.save()
#             ar.set_response(refresh=True)


# class StandbyTicket(dd.Action):
#     #label = _("Standby mode")
#     label = "\u2a37"
#     label = "\u2609"
#     help_text = _("Put this ticket into standby mode.")
#     show_in_workflow = True
#     show_in_bbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is not None or obj.closed is not None:
#             return False
#         return super(StandbyTicket, self).get_action_permission(
#             ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         now = datetime.datetime.now()
#         for obj in ar.selected_rows:
#             obj.standby = now
#             obj.save()
#             ar.set_response(refresh=True)


# class ActivateTicket(dd.Action):
#     # label = _("Activate")
#     label = "☀"  # "\u2600"
#     help_text = _("Reactivate this ticket from standby mode or closed state.")
#     show_in_workflow = True
#     show_in_bbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is None and obj.closed is None:
#             return False
#         return super(ActivateTicket, self).get_action_permission(
#             ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         for obj in ar.selected_rows:
#             obj.standby = False
#             obj.closed = False
#             obj.save()
#             ar.set_response(refresh=True)


class SpawnTicket(dd.Action):
    # label = _("Spawn new ticket")
    # label = "\u2611" "☑"
    label = "⚇"  # "\u2687"
    help_text = _("Spawn a new child ticket from this one.")
    show_in_workflow = True
    show_in_bbar = False

    def run_from_ui(self, ar, **kw):
        p = ar.selected_rows[0]
        c = rt.modules.tickets.Ticket(reporter=ar.get_user())
        for k in ('project', 'private'):
            setattr(c, k, getattr(p, k))
        c.full_clean()
        c.save()
        d = rt.modules.tickets.Link(
            parent=p, child=c,
            type=LinkTypes.requires)
        d.full_clean()
        d.save()
        ar.success(
            _("New ticket {0} has been spawned as child of {1}.").format(
                c, p))
        ar.goto_instance(c)


class Ticket(mixins.CreatedModified, TimeInvestment):
    """
    """
    workflow_state_field = 'state'

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')

    project = dd.ForeignKey('tickets.Project', blank=True, null=True)
    product = dd.ForeignKey('products.Product', blank=True, null=True)
    nickname = models.CharField(_("Nickname"), max_length=50, blank=True)
    summary = models.CharField(
        pgettext("Ticket", "Summary"), max_length=200,
        blank=True,
        help_text=_("Short summary of the problem."))
    description = dd.RichTextField(_("Description"), blank=True)
    ticket_type = dd.ForeignKey('tickets.TicketType', blank=True, null=True)
    duplicate_of = models.ForeignKey(
        'self', blank=True, null=True, verbose_name=_("Duplicate of"))

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
    # closed = models.DateTimeField(
    #     _("Closed since"), editable=False, null=True)
    # standby = models.DateTimeField(
    #     _("Standby since"), editable=False, null=True)
    feedback = models.BooleanField(
        _("Feedback"), default=False,
        help_text=_("Ticket is waiting for feedback from somebody else."))
    standby = models.BooleanField(_("Standby"), default=False)

    #~ start_date = models.DateField(
        #~ verbose_name=_("Start date"),
        #~ blank=True,null=True)

    # close_ticket = CloseTicket()
    # set_standby = StandbyTicket()
    # activate_ticket = ActivateTicket()
    spawn_ticket = SpawnTicket()

    def on_create(self, ar):
        if self.reporter_id is None:
            u = ar.get_user()
            if u is not None:
                self.reporter = u
        super(Ticket, self).on_create(ar)

    # def get_choices_text(self, request, actor, field):
    #     return "{0} ({1})".format(self, self.summary)

    def __unicode__(self):
        if self.nickname:
            return "#{0} ({1})".format(self.id, self.nickname)
        return "#{0} ({1})".format(self.id, self.summary)

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
        # return ar.obj2html(self, "#{0}".self.id)
        return ar.obj2html(self)
        # return E.span(ar.obj2html(self), ' ', self.summary)

# dd.update_field(Ticket, 'user', verbose_name=_("Reporter"))


class TicketDetail(dd.DetailLayout):
    main = "general planning"

    general = dd.Panel("""
    general1 LinksByTicket
    description:30 clocking.SessionsByTicket:40
    """, label=_("General"))
    
    general1 = """
    summary:40 id ticket_type:10
    reporter project product reported_for
    workflow_buttons:20 feedback standby closed private
    """

    planning = dd.Panel("""
    nickname:10 fixed_for created modified
    state assigned_to duplicate_of planned_time invested_time
    DuplicatesByTicket  #ChildrenByTicket
    """, label=_("Planning"))


class Tickets(dd.Table):
    required = dd.Required(auth=True)
    model = 'tickets.Ticket'
    order_by = ["id"]
    column_names = 'id summary:50 feedback standby closed workflow_buttons:30 reporter:10 project:10 *'
    auto_fit_column_widths = True
    detail_layout = TicketDetail()
    insert_layout = dd.FormLayout("""
    reporter project
    summary
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
        show_closed=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets which are closed.")),
        show_standby=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets which are in standby mode.")),
        show_private=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets which are private.")),
        observed_event=TicketEvents.field(blank=True))
    params_layout = """
    reporter assigned_to project state
    show_closed show_standby show_private start_date end_date observed_event"""
    simple_parameters = ('reporter', 'assigned_to', 'state', 'project')

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Tickets, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)

        if pv.show_closed == dd.YesNo.no:
            qs = qs.filter(closed=False)
        elif pv.show_closed == dd.YesNo.yes:
            qs = qs.filter(closed=True)

        if pv.show_standby == dd.YesNo.no:
            qs = qs.filter(standby=False)
        elif pv.show_standby == dd.YesNo.yes:
            qs = qs.filter(standby=True)

        if pv.show_private == dd.YesNo.no:
            qs = qs.filter(private=False, project__private=False)
        elif pv.show_private == dd.YesNo.yes:
            qs = qs.filter(Q(private=True) | Q(project__private=True))
        # print 20150512, qs.query
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


class DuplicatesByTicket(Tickets):
    label = _("Duplicates")
    master_key = 'duplicate_of'
    column_names = "id summary project reporter *"


class UnassignedTickets(Tickets):
    column_names = "summary project reporter *"


class TicketsByProject(Tickets):
    master_key = 'project'
    column_names = "summary ticket_type reported_for fixed_for state closed invested_time *"
    auto_fit_column_widths = True


class TicketsByType(Tickets):
    master_key = 'ticket_type'
    column_names = "summary state closed invested_time *"
    auto_fit_column_widths = True


class TicketsByProduct(Tickets):
    master_key = 'product'
    column_names = "summary state closed invested_time *"
    auto_fit_column_widths = True


class PublicTickets(Tickets):
    label = _("Public tickets")
    order_by = ["-modified", "id"]
    column_names = 'overview:50 workflow_buttons:30 reporter:10 project:10 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(PublicTickets, self).param_defaults(ar, **kw)
        kw.update(show_closed=dd.YesNo.no)
        # kw.update(show_standby=dd.YesNo.no)
        kw.update(show_private=dd.YesNo.no)
        return kw


class ActiveTickets(Tickets):
    help_text = _("Active tickets are those which are neither "
                  "closed nor in standby mode.")
    label = _("Active tickets")
    order_by = ["-modified", "id"]
    column_names = 'overview:50 workflow_buttons:40 \
    reporter:10 ticket_type:10 project:10 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ActiveTickets, self).param_defaults(ar, **kw)
        kw.update(show_closed=dd.YesNo.no)
        kw.update(show_standby=dd.YesNo.no)
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
