# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module adds models for Projects, Milestones, Tickets & Co.

A **Project** is something into which somebody (the `partner`) invests
time, energy and money.  The partner can be either external or the
runner of the site.  Projects form a tree: each Project can have a
`parent` (another Project for which it is a sub-project).

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
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.excerpts.mixins import Certifiable
from lino.utils import join_elems

from .choicelists import TicketEvents, TicketStates, LinkTypes
from .roles import Worker


class TimeInvestment(dd.Model):
    """Model mixin for things which represent a time investment.  This
    currently just defines a group of three fields:

    .. attribute:: closed

        Whether this investment is closed, i.e. certain things should
        not change anymore.

    .. attribute:: private

        Whether this investment is private, i.e. should not be
        publicly visible anywhere.
        
        The default value is True.  Tickets on public projects cannot
        be private, but tickets on private projects may be manually
        set to public.

    .. attribute:: planned_time

        The time (in hours) we plan to work on this project or ticket.

    """
    class Meta:
        abstract = True

    closed = models.BooleanField(_("Closed"), default=False)
    private = models.BooleanField(_("Private"), default=True)

    planned_time = models.TimeField(
        _("Planned time"),
        blank=True, null=True)

    # invested_time = models.TimeField(
    #     _("Invested time"), blank=True, null=True, editable=False)


class ProjectType(mixins.BabelNamed):
    """The type of a :class:`Project`."""

    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')


class TicketType(mixins.BabelNamed):
    """The type of a :class:`Ticket`."""

    class Meta:
        verbose_name = _("Ticket type")
        verbose_name_plural = _('Ticket types')


#~ class Repository(UserAuthored):
    #~ class Meta:
        #~ verbose_name = _("Repository")
        #~ verbose_name_plural = _('Repositories')


class Project(TimeInvestment, mixins.Hierarchical, mixins.Referrable,
              ContactRelated):
    """A **project** is something on which several users work together.

    .. attribute:: name

    .. attribute:: parent

    .. attribute:: assign_to

        The user to whom new tickets will be assigned.
        See :attr:`Ticket.assigned_to`.

    """
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _('Projects')

    name = models.CharField(_("Name"), max_length=200)
    # parent = models.ForeignKey(
    #     'self', blank=True, null=True, verbose_name=_("Parent"))
    assign_to = dd.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Assign tickets to"),
        blank=True, null=True,
        help_text=_("The user to whom new tickets will be assigned."))
    type = models.ForeignKey('tickets.ProjectType', blank=True, null=True)
    description = dd.RichTextField(_("Description"), blank=True)
    srcref_url_template = models.CharField(blank=True, max_length=200)
    changeset_url_template = models.CharField(blank=True, max_length=200)
    # root = models.ForeignKey(
    #     'self', blank=True, null=True, verbose_name=_("Root"))

    def __unicode__(self):
        return self.ref or self.name

    # def save(self, *args, **kwargs):
    #     root = self.parent
    #     while root is not None:
    #         if root.parent is None:
    #             break
    #         else:
    #             root = root.parent
    #     self.root = root
    #     super(Project, self).save(*args, **kwargs)


class Site(dd.Model):
    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _('Sites')

    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)
    name = models.CharField(_("Designation"), max_length=200)
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Milestone(Certifiable):  # mixins.Referrable):
    """
    """
    class Meta:
        verbose_name = _("Milestone")
        verbose_name_plural = _('Milestones')

    # project = dd.ForeignKey(
    #     'tickets.Project',
    #     related_name='milestones_by_project')
    site = dd.ForeignKey(
        'tickets.Site',
        related_name='milestones_by_site', blank=True, null=True)
    label = models.CharField(_("Label"), max_length=20, blank=True)
    expected = models.DateField(_("Expected for"), blank=True, null=True)
    reached = models.DateField(_("Reached"), blank=True, null=True)
    description = dd.RichTextField(_("Description"), blank=True)
    changes_since = models.DateField(
        _("Changes since"), blank=True, null=True,
        help_text=_("In printed document include a list of "
                    "other changes since this date"))

    #~ def __unicode__(self):
        #~ return self.label

    def __unicode__(self):
        label = self.label
        if not label:
            if self.reached:
                label = self.reached.isoformat()
            else:
                label = "#{0}".format(self.id)
        return "{0}:{1}".format(self.site, label)


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
    # label = "⚇"  # "\u2687"
    show_in_workflow = False
    show_in_bbar = False

    def __init__(self, label, link_type):
        self.label = label
        self.link_type = link_type
        self.help_text = _(
            "Spawn a new child ticket {0} this one.").format(
            link_type.as_child())
        super(SpawnTicket, self).__init__()

    def run_from_ui(self, ar, **kw):
        p = ar.selected_rows[0]
        c = rt.modules.tickets.Ticket(
            reporter=ar.get_user(),
            summary=_("New ticket {0} #{1}".format(
                self.link_type.as_child(), p.id)))
        for k in ('project', 'private'):
            setattr(c, k, getattr(p, k))
        c.full_clean()
        c.save()
        d = rt.modules.tickets.Link(
            parent=p, child=c,
            type=self.link_type)
        d.full_clean()
        d.save()
        ar.success(
            _("New ticket {0} has been spawned as child of {1}.").format(
                c, p))
        ar.goto_instance(c)


class Ticket(mixins.CreatedModified, TimeInvestment):
    """A **Ticket** is a concrete question or problem formulated by a
    :attr:`reporter` (a user).
    
    A Ticket is always related to one and only one Project.  It may be
    related to other tickets which may belong to other projects.


    .. attribute:: reporter

        The user who is reported this ticket.

    .. attribute:: assigned_to

        The user who is working on this ticket.

        If this field is empty and :attr:`project` is not empty, then
        default value is taken from :attr:`Project.assign_to`.

    .. attribute:: waiting_for

        An unformatted one-line text which describes what this ticket
        is waiting for.

    """
    workflow_state_field = 'state'

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')

    project = dd.ForeignKey(
        'tickets.Project', blank=True, null=True,
        related_name="tickets_by_project")
    site = dd.ForeignKey('tickets.Site', blank=True, null=True)
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
    fixed_for = dd.ForeignKey(  # no longer used since 20150814
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
    state = TicketStates.field(default=TicketStates.new)
    waiting_for = models.CharField(
        _("Waiting for"), max_length=200,
        blank=True,
        help_text=_("What to do next."))

    deadline = models.DateField(
        verbose_name=_("Deadline"),
        blank=True, null=True)

    priority = models.SmallIntegerField(
        _("Priority"), default=0,
        help_text=_("Value between 0 and 100."))

    # deprecated fields:
    feedback = models.BooleanField(
        _("Feedback"), default=False,
        help_text=_("Ticket is waiting for feedback from somebody else."))
    standby = models.BooleanField(_("Standby"), default=False)

    spawn_triggered = SpawnTicket(
        _("Spawn triggered ticket"),
        LinkTypes.triggers)
    # spawn_triggered = SpawnTicket("⚇", LinkTypes.triggers)  # "\u2687"
    # spawn_ticket = SpawnTicket("", LinkTypes.requires)  # "\u2687"

    def on_create(self, ar):
        # print "20150523a on_create", self.reporter_id
        # print "20150523a on_create", self.reporter_id
        me = ar.get_user()
        if me is not None:
            if self.reporter_id is None:
                self.reporter = me
            if self.assigned_to_id is None:
                if me.profile.has_required_roles([Worker]):
                    self.assigned_to = me
        super(Ticket, self).on_create(ar)

    def full_clean(self):
        """If :attr:`project` is not set and if the ticket has a
        :attr:`reporter`, use that reporter's :attr:`current_project`
        as default value.

        """
        # print "20150523b on_create", self.reporter
        super(Ticket, self).full_clean()
        me = self.reporter
        if False:
            if me and not self.project and me.current_project:
                self.project = me.current_project
        if self.project:
            if not self.assigned_to and self.project.assign_to:
                self.assigned_to = self.project.assign_to
            if not self.project.private:
                self.private = False

    def disabled_fields(self, ar):
        rv = super(Ticket, self).disabled_fields(ar)
        if self.project and not self.project.private:
            rv.add('private')
        return rv

    # def get_choices_text(self, request, actor, field):
    #     return "{0} ({1})".format(self, self.summary)

    def __unicode__(self):
        if self.nickname:
            return "#{0} ({1})".format(self.id, self.nickname)
        return "#{0} ({1})".format(self.id, self.summary)

    @dd.chooser()
    def reported_for_choices(cls, site):
        if not site:
            return []
        # return site.milestones_by_site.filter(reached__isnull=False)
        return site.milestones_by_site.all()

    @dd.chooser()
    def fixed_for_choices(cls, site):
        if not site:
            return []
        return site.milestones_by_site.all()

    @dd.displayfield(_("Overview"))
    def overview(self, ar):
        # return ar.obj2html(self, "#{0}".self.id)
        return ar.obj2html(self)
        # return E.span(ar.obj2html(self), ' ', self.summary)

# dd.update_field(Ticket, 'user', verbose_name=_("Reporter"))


class Interest(dd.Model):
    """An **interest** is the fact that a given site is interested in the
    tickets related to a given product.

    """
    class Meta:
        verbose_name = _("Interest")
        verbose_name_plural = _('Interests')

    product = dd.ForeignKey(
        'products.Product',
        related_name='interests_by_product')

    site = dd.ForeignKey(
        'tickets.Site',
        related_name='interests_by_site')

# dd.update_field(Interest, 'user', verbose_name=_("User"))


class Deployment(dd.Model):
    """A **deployment** is the fact that a given ticket is being fixed (or
    installed or activated) by a given milestone (to a given site).

    Deployments are visible to the user either by ticket or by milestone.

    """
    class Meta:
        verbose_name = _("Deployment")
        verbose_name_plural = _('Deployments')

    ticket = dd.ForeignKey('tickets.Ticket')
    milestone = dd.ForeignKey('tickets.Milestone')
    remark = dd.RichTextField(_("Remark"), blank=True, format="plain")

    @dd.chooser()
    def milestone_choices(cls, ticket):
        if not ticket:
            return []
        if ticket.site:
            return ticket.site.milestones_by_site.all()
        return rt.modules.tickets.Milestone.objects.order_by('label')


if False:  # removed current_project field because it caused circular
           # dependency (and was not useful)
    dd.inject_field(
        'users.User', 'current_project',
        dd.ForeignKey(
            'tickets.Project', verbose_name=_("Current project"),
            blank=True, null=True, related_name="users_by_project"))

from .ui import *
