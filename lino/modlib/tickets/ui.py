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

from lino.modlib.cal.mixins import daterange_text
from lino.modlib.users.mixins import My
from lino.utils import join_elems

from .choicelists import TicketEvents, ProjectEvents, TicketStates, LinkTypes


class ProjectTypes(dd.Table):
    model = 'tickets.ProjectType'
    column_names = 'name *'
    detail_layout = """id name
    ProjectsByType
    """


class TicketTypes(dd.Table):
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
    description:30
    ProjectsByParent:30 TicketsByProject
    # cal.EventsByProject
    """, label=_("General"))

    # tickets = dd.Panel("""
    # #SponsorshipsByProject
    # TicketsByProject #SessionsByProject
    # """, label=_("Tickets"))

    history = dd.Panel("""
    srcref_url_template changeset_url_template
    MilestonesByProject
    """, label=_("Timeline"))


class Projects(dd.Table):
    model = 'tickets.Project'
    detail_layout = ProjectDetail()
    column_names = "ref name parent type *"
    parameters = mixins.ObservedPeriod(
        observed_event=ProjectEvents.field(blank=True),
        interesting_for=dd.ForeignKey(
            'tickets.Site',
            verbose_name=_("Interesting for"),
            blank=True, null=True,
            help_text=_("Only project interesting for this site.")))
    params_layout = """interesting_for start_date end_date observed_event"""

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Projects, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)

        if pv.interesting_for:
            qs = qs.filter(
                Q(tickets_by_project__site=pv.interesting_for) |
                Q(tickets_by_project__site__isnull=True))
            interests = pv.interesting_for.interests_by_site.values(
                'product')
            if len(interests) > 0:
                qs = qs.filter(tickets_by_project__product__in=interests)
        return qs


class ProjectsByParent(Projects):
    master_key = 'parent'
    label = _("Subprojects")
    column_names = "ref name *"


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
    child
    type
    """, window_size=(40, 'auto'))


class LinksByTicket(Links):

    label = _("Dependencies")
    required_roles = dd.required()
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


class TicketDetail(dd.DetailLayout):
    main = "general planning"

    general = dd.Panel("""
    general1 LinksByTicket
    description:30 clocking.SessionsByTicket:40
    """, label=_("General"))
    
    general1 = """
    summary:40 id ticket_type:10
    reporter project product site
    workflow_buttons:20 feedback standby closed private
    """

    planning = dd.Panel("""
    nickname:10 created modified reported_for fixed_for
    state priority assigned_to duplicate_of planned_time
    DuplicatesByTicket  #ChildrenByTicket
    """, label=_("Planning"))


class Tickets(dd.Table):
    model = 'tickets.Ticket'
    order_by = ["-id"]
    column_names = 'id summary:50 feedback standby closed ' \
                   'workflow_buttons:30 reporter:10 project:10 *'
    auto_fit_column_widths = True
    detail_layout = TicketDetail()
    insert_layout = """
    reporter product
    summary
    """

    parameters = mixins.ObservedPeriod(
        observed_event=TicketEvents.field(blank=True),
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
        interesting_for=dd.ForeignKey(
            'tickets.Site',
            verbose_name=_("Interesting for"),
            blank=True, null=True,
            help_text=_("Only tickets interesting for this site.")),
        project=dd.ForeignKey(
            'tickets.Project',
            blank=True, null=True),
        state=TicketStates.field(
            blank=True, help_text=_("Only rows having this state.")),
        show_assigned=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets which are assigned to somebody.")),
        show_closed=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets which are closed.")),
        has_project=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets with project assigned.")),
        show_standby=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets which are in standby mode.")),
        show_private=dd.YesNo.field(
            blank=True,
            help_text=_("Show tickets which are private.")))
    params_layout = """
    reporter assigned_to interesting_for project state has_project
    show_assigned show_closed show_standby show_private \
    start_date end_date observed_event"""
    simple_parameters = ('reporter', 'assigned_to', 'state', 'project')

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Tickets, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)

        if pv.interesting_for:
            qs = qs.filter(Q(site=pv.interesting_for) | Q(site__isnull=True))
            interests = pv.interesting_for.interests_by_site.values(
                'product')
            if len(interests) > 0:
                qs = qs.filter(product__in=interests)

        if pv.show_closed == dd.YesNo.no:
            qs = qs.filter(closed=False)
        elif pv.show_closed == dd.YesNo.yes:
            qs = qs.filter(closed=True)

        if pv.show_assigned == dd.YesNo.no:
            qs = qs.filter(assigned_to__isnull=True)
        elif pv.show_assigned == dd.YesNo.yes:
            qs = qs.filter(assigned_to__isnull=False)

        if pv.has_project == dd.YesNo.no:
            qs = qs.filter(project__isnull=True)
        elif pv.has_project == dd.YesNo.yes:
            qs = qs.filter(project__isnull=False)

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
    column_names = "overview:50 product:10 reporter:10 state closed standby *"
    auto_fit_column_widths = True


class TicketsByType(Tickets):
    master_key = 'ticket_type'
    column_names = "summary state closed  *"
    auto_fit_column_widths = True


class TicketsByProduct(Tickets):
    master_key = 'product'
    column_names = "summary state closed  *"
    auto_fit_column_widths = True


class PublicTickets(Tickets):
    roles_required = set([])
    label = _("Public tickets")
    order_by = ["-priority", "-id"]
    column_names = 'overview:50 workflow_buttons:30 project:10 *'
    filter = models.Q(assigned_to=None)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(PublicTickets, self).param_defaults(ar, **kw)
        kw.update(show_assigned=dd.YesNo.no)
        kw.update(show_private=dd.YesNo.no)
        kw.update(show_closed=dd.YesNo.no)
        return kw


class TicketsToTriage(Tickets):
    label = _("Tickets to triage")
    button_label = _("Triage")
    order_by = ["-id"]
    column_names = 'overview:50 product:10 reporter:10 project:10 ' \
                   'assigned_to:10 ticket_type:10 workflow_buttons:40 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(TicketsToTriage, self).param_defaults(ar, **kw)
        kw.update(state=TicketStates.new)
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        count = sar.get_total_count()
        if count > 0:
            msg = _("{0} new tickets.")
            msg = msg.format(count)
            yield ar.href_to_request(sar, msg)


class TicketsToTalk(Tickets):
    label = _("Tickets to talk")
    button_label = _("Talk")
    order_by = ["-id"]
    column_names = "overview:50 planned_time priority reporter:10 " \
                   "workflow_buttons:40 *"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(TicketsToTalk, self).param_defaults(ar, **kw)
        kw.update(state=TicketStates.talk)
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        count = sar.get_total_count()
        if count > 0:
            msg = _("{0} tickets to talk.")
            msg = msg.format(count)
            yield ar.href_to_request(sar, msg)


class TicketsToDo(Tickets):
    label = _("Tickets to do")
    button_label = _("To do")
    order_by = ["priority", "-deadline", "-id"]
    column_names = 'overview:50 priority deadline ' \
                   'assigned_to:10 workflow_buttons:40 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(TicketsToDo, self).param_defaults(ar, **kw)
        kw.update(state=TicketStates.todo)
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        count = sar.get_total_count()
        if count > 0:
            msg = _("{0} tickets to do.")
            msg = msg.format(count)
            yield ar.href_to_request(sar, msg)

    
class ActiveTickets(Tickets):
    help_text = _("Active tickets are those which are neither "
                  "closed nor in standby mode.")
    label = _("Active tickets")
    order_by = ["-id"]
    # order_by = ["-modified", "id"]
    column_names = 'overview:50 product:10 reporter:10 project:10 ' \
                   'assigned_to:10 ticket_type:10 workflow_buttons:40 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ActiveTickets, self).param_defaults(ar, **kw)
        kw.update(show_closed=dd.YesNo.no)
        kw.update(show_standby=dd.YesNo.no)
        return kw


class InterestingTickets(ActiveTickets):
    label = _("Interesting tickets")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(InterestingTickets, self).param_defaults(ar, **kw)
        # kw.update(interesting_for=ar.get_user())
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


class Sites(dd.Table):
    model = 'tickets.Site'
    column_names = "name partner remark id *"
    order_by = ['name']
    auto_fit_column_widths = True

    insert_layout = """
    name
    remark
    """

    detail_layout = """
    id name partner
    remark
    InterestsBySite TicketsBySite
    """


class SitesByPartner(Sites):
    master_key = 'partner'
    column_names = "name remark *"


class Interests(dd.Table):
    model = 'tickets.Interest'
    column_names = "site product *"
    auto_fit_column_widths = True


# class MyInterests(My, Interests):
#     order_by = ["product__ref"]
#     column_names = 'product__ref product *'


class InterestsBySite(Interests):
    master_key = 'site'
    order_by = ["product"]
    column_names = 'product *'


class InterestsByProduct(Interests):
    master_key = 'product'
    order_by = ["site"]
    column_names = 'site *'


class TicketsBySite(Tickets):
    master_key = 'site'


