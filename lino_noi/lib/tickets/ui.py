# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.


"""Database models for this plugin.

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

"""

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Q

from lino import mixins
from lino.api import dd, rt, _, pgettext

from lino.utils.xmlgen.html import E

from lino_xl.lib.cal.mixins import daterange_text
from lino.modlib.users.mixins import My
from lino.utils import join_elems

from .choicelists import TicketEvents, ProjectEvents, TicketStates, LinkTypes

from .roles import Triager


class ProjectTypes(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    model = 'tickets.ProjectType'
    column_names = 'name *'
    detail_layout = """id name
    ProjectsByType
    """


class TicketTypes(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    model = 'tickets.TicketType'
    column_names = 'name *'
    detail_layout = """id name
    TicketsByType
    """


class ProjectDetail(dd.FormLayout):
    main = "general #tickets history"

    general = dd.Panel("""
    ref name parent type
    company assign_to #contact_person #contact_role private closed
    description ProjectsByParent
    # cal.EventsByProject
    """, label=_("General"))

    # tickets = dd.Panel("""
    # #SponsorshipsByProject
    # TicketsByProject #SessionsByProject
    # """, label=_("Tickets"))

    history = dd.Panel("""
    start_date end_date srcref_url_template changeset_url_template
    #MilestonesByProject
    TicketsByProject
    """, label=_("Timeline"))


class Projects(dd.Table):
    model = 'tickets.Project'
    detail_layout = ProjectDetail()
    column_names = "ref name parent type private *"
    parameters = mixins.ObservedPeriod(
        observed_event=ProjectEvents.field(blank=True),
        interesting_for=dd.ForeignKey(
            'contacts.Partner',
            verbose_name=_("Interesting for"),
            blank=True, null=True,
            help_text=_("Only projects interesting for this partner.")))
    params_layout = """interesting_for start_date end_date observed_event"""

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Projects, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)

        if pv.interesting_for:
            qs = qs.filter(
                Q(tickets_by_project__site__partner=pv.interesting_for) |
                Q(tickets_by_project__site__partner__isnull=True))
            interests = pv.interesting_for.interests_by_partner.values(
                'topic')
            if len(interests) > 0:
                qs = qs.filter(
                    tickets_by_project__topic__in=interests,
                    tickets_by_project__private=False)
        return qs


class AllProjects(Projects):
    required_roles = dd.required(dd.SiteStaff)
    
class ActiveProjects(Projects):
    """Show a list of active projects.

    For an example, see :ref:`noi.specs.projects`.

    """
    label = _("Active projects")
    column_names = 'ref name start_date activity_overview *'
    required_roles = dd.required(dd.SiteStaff)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ActiveProjects, self).param_defaults(ar, **kw)
        kw.update(start_date=dd.demo_date())
        kw.update(end_date=dd.demo_date())
        kw.update(observed_event=ProjectEvents.active)
        return kw

    
class ProjectsByParent(Projects):
    master_key = 'parent'
    label = _("Subprojects")
    column_names = "ref name children_summary *"


class TopLevelProjects(Projects):
    label = _("Projects (tree)")
    required_roles = dd.required(dd.SiteStaff)
    order_by = ["ref"]
    column_names = 'ref name parent children_summary *'
    filter = models.Q(parent__isnull=True)
    variable_row_height = True


class ProjectsByType(Projects):
    master_key = 'type'
    column_names = "ref name *"


class ProjectsByCompany(Projects):
    master_key = 'company'
    column_names = "ref name *"


class Links(dd.Table):
    model = 'tickets.Link'
    required_roles = dd.required(dd.SiteStaff)
    stay_in_grid = True
    detail_layout = dd.FormLayout("""
    parent
    type
    child
    """, window_size=(40, 'auto'))


class LinksByTicket(Links):

    label = _("Dependencies")
    required_roles = dd.required(Triager)
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
        # else:
        #     elems.append(_("No dependencies."))

        # Buttons for creating relationships:

        sar = obj.spawn_triggered.request_from(ar)
        if ar.renderer.is_interactive and sar.get_permission():
            btn = sar.ar2button(obj)
            elems += [E.br(), btn]
        
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


class TicketDetail(dd.DetailLayout):
    main = "general more history_tab"

    general = dd.Panel("""
    general1
    comments.CommentsByRFC:60 clocking.SessionsByTicket:20
    """, label=_("General"))

    history_tab = dd.Panel("""
    changes.ChangesByMaster:50 stars.StarsByController:20
    """, label=_("History"), required_roles=dd.login_required(Triager))

    general1 = """
    summary:40 id:6 reporter:12
    site topic project private
    workflow_buttons assigned_to waiting_for
    """

    more = dd.Panel("""
    more1 DuplicatesByTicket:20
    description:40 upgrade_notes:20 LinksByTicket:20
    """, label=_("More"))

    more1 = """
    #nickname:10 created modified reported_for #fixed_for ticket_type:10
    state duplicate_of planned_time priority
    # standby feedback closed
    """


class Tickets(dd.Table):
    """Global list of all tickets.

    .. attribute:: site

        Select a site if you want to see only tickets for this site.

    .. attribute:: show_private

        Show only (or hide) tickets that are marked private.

    .. attribute:: show_active

        Show only (or hide) tickets which are active (i.e. state is Talk
        or ToDo).

    .. attribute:: show_assigned

        Show only (or hide) tickets which are assigned to somebody.

    .. attribute:: has_project

        Show only (or hide) tickets which have a project assigned.

    .. attribute:: feasable_by

        Show only tickets for which I am competent.

    """
    required_roles = set()  # also for anonymous
    model = 'tickets.Ticket'
    order_by = ["-id"]
    column_names = 'id summary:50 reporter:10 topic faculty ' \
                   'workflow_buttons:30 project:10 *'
    detail_layout = TicketDetail()
    insert_layout = dd.InsertLayout("""
    # reporter #product
    summary
    description
    """, window_size=(70, 20))

    detail_html_template = "tickets/Ticket/detail.html"

    parameters = mixins.ObservedPeriod(
        observed_event=TicketEvents.field(blank=True),
        topic=dd.ForeignKey('topics.Topic', blank=True,),
        site=dd.ForeignKey('tickets.Site', blank=True,),
        reporter=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Reporter"),
            blank=True, null=True,
            help_text=_("Only rows reporter by this user.")),
        assigned_to=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Assigned to"),
            blank=True, null=True,
            help_text=_("Only tickets assigned to this user.")),
        feasable_by=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Feasable by"), blank=True, null=True),
        interesting_for=dd.ForeignKey(
            'contacts.Partner',
            verbose_name=_("Interesting for"),
            blank=True, null=True,
            help_text=_("Only tickets interesting for this partner.")),
        project=dd.ForeignKey(
            'tickets.Project',
            blank=True, null=True),
        state=TicketStates.field(
            blank=True, help_text=_("Only rows having this state.")),
        show_assigned=dd.YesNo.field(_("Assigned"), blank=True),
        show_active=dd.YesNo.field(_("Active"), blank=True),
        has_project=dd.YesNo.field(_("Has project"), blank=True),
        show_private=dd.YesNo.field(_("Private"), blank=True))

    params_layout = """
    reporter assigned_to interesting_for site project state has_project
    show_assigned show_active #show_closed #show_standby show_private \
    start_date end_date observed_event topic feasable_by"""
    # simple_parameters = ('reporter', 'assigned_to', 'state', 'project')

    @classmethod
    def get_simple_parameters(cls):
        s = super(Tickets, cls).get_simple_parameters()
        s |= set(('reporter', 'assigned_to',
                  'state', 'project' ,'topic', 'site'))
        return s

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Tickets, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)

        if pv.feasable_by:
            faculties = set()
            for fac in rt.models.faculties.Faculty.objects.filter(
                competence__user=pv.feasable_by):
                faculties |= set(fac.get_parental_line())
            qs = qs.filter(Q(faculty__in=faculties))
            
        if pv.interesting_for:

            interests = pv.interesting_for.interests_by_partner.values(
                'topic')
            if len(interests) > 0:
                qs = qs.filter(
                    Q(site__partner=pv.interesting_for) |
                    Q(topic__in=interests, private=False))

        # if pv.show_closed == dd.YesNo.no:
        #     qs = qs.filter(closed=False)
        # elif pv.show_closed == dd.YesNo.yes:
        #     qs = qs.filter(closed=True)

        if pv.show_assigned == dd.YesNo.no:
            qs = qs.filter(assigned_to__isnull=True)
        elif pv.show_assigned == dd.YesNo.yes:
            qs = qs.filter(assigned_to__isnull=False)


        active_states = TicketStates.filter(active=True)
        # active_states = (
        #     TicketStates.todo, TicketStates.talk, TicketStates.ready)
        # print 20160810, active_states
        if pv.show_active == dd.YesNo.no:
            qs = qs.exclude(state__in=active_states)
        elif pv.show_assigned == dd.YesNo.yes:
            qs = qs.filter(state__in=active_states)

        if pv.has_project == dd.YesNo.no:
            qs = qs.filter(project__isnull=True)
        elif pv.has_project == dd.YesNo.yes:
            qs = qs.filter(project__isnull=False)

        # if pv.show_standby == dd.YesNo.no:
        #     qs = qs.filter(standby=False)
        # elif pv.show_standby == dd.YesNo.yes:
        #     qs = qs.filter(standby=True)

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

class AllTickets(Tickets):
    required_roles = dd.login_required(dd.SiteStaff)

class DuplicatesByTicket(Tickets):
    """Shows the tickets which are marked as duplicates of this
    (i.e. whose `duplicate_of` field points to this ticket.

    """
    label = _("Duplicates")
    master_key = 'duplicate_of'
    column_names = "id summary *"


class SuggestedTickets(Tickets):
    required_roles = dd.login_required()
    label = _("Where I can help")
    column_names = 'overview:50 reporter:10 topic faculty ' \
                   'workflow_buttons:30 *'
    params_panel_hidden = True
    params_layout = """
    reporter feasable_by site project state
    show_assigned show_active topic"""
    
    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(SuggestedTickets, self).param_defaults(ar, **kw)
        kw.update(show_assigned=dd.YesNo.no)
        kw.update(show_active=dd.YesNo.yes)
        kw.update(feasable_by=ar.get_user())
        return kw


    


class UnassignedTickets(Tickets):
    column_names = "summary project reporter *"
    label = _("Unassigned Tickets")
    required_roles = dd.login_required(Triager)

    @classmethod
    def get_queryset(self, ar):
        return self.model.objects.filter(assigned_to=None)


class TicketsByProject(Tickets):
    master_key = 'project'
    required_roles = dd.login_required(Triager)
    column_names = ("overview:50 topic:10 reporter:10 state "
                    "planned_time *")


class TicketsByType(Tickets):
    master_key = 'ticket_type'
    column_names = "summary state  *"


class TicketsByTopic(Tickets):
    master_key = 'topic'
    column_names = "summary state  *"


class PublicTickets(Tickets):
    label = _("Public tickets")
    order_by = ["-priority", "-id"]
    column_names = 'overview:50 state:10 ticket_type:10 project:10 topic:10 priority:3 *'
    filter = models.Q(assigned_to=None)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(PublicTickets, self).param_defaults(ar, **kw)
        kw.update(show_assigned=dd.YesNo.no)
        kw.update(show_private=dd.YesNo.no)
        kw.update(show_active=dd.YesNo.yes)
        # kw.update(show_closed=dd.YesNo.no)
        # kw.update(state=TicketStates.todo)
        return kw


class TicketsToTriage(Tickets):
    """List of tickets that need to be triaged.  Currently this is
    equivalent to those having their state set to :attr:`new
    <lino_noi.lib.tickets.choicelists.TicketStates.new>`.

    """
    required_roles = dd.login_required(Triager)
    label = _("Tickets to triage")
    button_label = _("Triage")
    order_by = ["-id"]
    column_names = 'overview:50 topic:10 reporter:10 project:10 ' \
                   'assigned_to:10 ticket_type:10 workflow_buttons:40 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(TicketsToTriage, self).param_defaults(ar, **kw)
        kw.update(state=TicketStates.new)
        return kw

    welcome_message_when_count = 0


class TicketsToTalk(Tickets):
    label = _("Tickets to talk")
    required_roles = dd.login_required(Triager)
    order_by = ["-priority", "-deadline", "-id"]
    # order_by = ["-id"]
    column_names = "overview:50  priority #deadline waiting_for " \
                   "workflow_buttons:40 *"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(TicketsToTalk, self).param_defaults(ar, **kw)
        kw.update(state=TicketStates.talk)
        return kw


class TicketsToDo(Tickets):
    """Shows a list of tickets "to do". This means attributed to me and
    state "confirmed".

    """
    label = _("Tickets to do")
    required_roles = dd.login_required()
    order_by = ["-priority", "-deadline", "-id"]
    column_names = 'overview:50 priority deadline waiting_for ' \
                   'workflow_buttons:40 *'
    params_layout = """
    reporter site project state 
    start_date end_date observed_event topic feasable_by"""

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(TicketsToDo, self).param_defaults(ar, **kw)
        kw.update(state=TicketStates.todo)
        kw.update(assigned_to=ar.get_user())
        return kw


class ActiveTickets(Tickets):
    """Active tickets are those which are neither closed nor in standby
    mode.

    """
    label = _("Active tickets")
    required_roles = dd.login_required(Triager)
    order_by = ["-id"]
    # order_by = ["-modified", "id"]
    column_names = 'overview:50 topic:10 reporter:10 project:10 ' \
                   'assigned_to:10 ticket_type:10 workflow_buttons:40 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ActiveTickets, self).param_defaults(ar, **kw)
        kw.update(show_active=dd.YesNo.yes)
        # kw.update(show_closed=dd.YesNo.no)
        # kw.update(show_standby=dd.YesNo.no)
        return kw


class MyTickets(My, Tickets):
    """Show the tickets reported by me."""
    required_roles = dd.login_required()
    order_by = ["-id"]
    column_names = 'overview:50 faculty topic ' \
                   'workflow_buttons:40 *'
    params_layout = """
    reporter site project state 
    start_date end_date observed_event topic feasable_by"""


# class InterestingTickets(ActiveTickets):
#     label = _("Interesting tickets")

#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super(InterestingTickets, self).param_defaults(ar, **kw)
#         # kw.update(interesting_for=ar.get_user())
#         return kw


# class TicketsByPartner(Tickets):
#     master_key = 'partner'
#     column_names = "summary project user *"


class TicketsFixed(Tickets):
    label = _("Fixed tickets")
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


class Sites(dd.Table):
    # required_roles = set()  # also for anonymous
    model = 'tickets.Site'
    column_names = "name partner remark id *"
    order_by = ['name']
    detail_html_template = "tickets/Site/detail.html"

    insert_layout = """
    name
    remark
    """

    detail_layout = """
    id name partner #responsible_user
    remark
    TicketsBySite
    """

class AllSites(Sites):
    required_roles = dd.required(dd.SiteStaff)

class SitesByPartner(Sites):
    master_key = 'partner'
    column_names = "name remark *"


class TicketsBySite(Tickets):
    label = _("Known problems")
    master_key = 'site'

    @classmethod
    def param_defaults(self, ar, **kw):
        mi = ar.master_instance
        kw = super(TicketsBySite, self).param_defaults(ar, **kw)
        kw.update(interesting_for=mi.partner)
        kw.update(end_date=dd.today())
        kw.update(observed_event=TicketEvents.todo)
        return kw


# class MyKnownProblems(Tickets):
#     """For users whose `user_site` is set, show the known problems on
#     their site.

#     """
#     required_roles = dd.login_required()
#     label = _("My known problems")
#     abstract = not dd.is_installed('contacts')

#     # @classmethod
#     # def get_master_instance(self, ar, model, pk):
#     #     u = ar.get_user()
#     #     return u.user_site
        
#     @classmethod
#     def get_request_queryset(self, ar):
#         u = ar.get_user()
#         # print "20150910", u.user_site
#         if not u.user_site:
#             ar.no_data_text = _("Only for users whose `user_site` is set.")
#             return self.model.objects.none()
#         return super(MyKnownProblems, self).get_request_queryset(ar)

#     @classmethod
#     def param_defaults(self, ar, **kw):
#         u = ar.get_user()
#         kw = super(MyKnownProblems, self).param_defaults(ar, **kw)
#         if u.user_site:
#             kw.update(interesting_for=u.user_site.partner)
#         kw.update(end_date=dd.demo_date())
#         kw.update(observed_event=TicketEvents.todo)
#         return kw

#     @classmethod
#     def get_welcome_messages(cls, ar, **kw):
#         sar = ar.spawn(cls)
#         count = sar.get_total_count()
#         if count > 0:
#             msg = _("There are {0} known problems for {1}.")
#             msg = msg.format(count, ar.get_user().user_site)
#             yield ar.href_to_request(sar, msg)


