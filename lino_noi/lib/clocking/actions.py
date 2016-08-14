# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""Defines actions for this plugin."""


from django.db import models
from django.utils import timezone

from lino.api import dd, rt, _

from lino.mixins.periods import Monthly
from lino.modlib.printing.mixins import DirectPrintAction
from lino.core.roles import SiteUser
from .roles import Worker


class EndSession(dd.Action):
    """To close a session means to stop working on that ticket for this time.

    """
    label = u"◉"  # FISHEYE (U+25C9)
    # label = u"↘"  # u"\u2198"
    # label = _("End session")
    help_text = _("End this session.")
    # icon_name = 'emoticon_smile'
    show_in_workflow = True
    show_in_bbar = False
    readonly = False

    def get_action_permission(self, ar, obj, state):
        if obj.end_time:
            return False
        return super(EndSession, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):

        def ok(ar2):
            now = timezone.now()
            for obj in ar.selected_rows:
                obj.set_datetime('end', now)
                # obj.end_date = dd.today()
                # obj.end_time = now.time()
                obj.save()
                obj.ticket.touch()
                obj.ticket.save()
                ar2.set_response(refresh=True)

        if True:
            ok(ar)
        else:
            msg = _("Close {0} sessions.").format(len(ar.selected_rows))
            ar.confirm(ok, msg, _("Are you sure?"))


class EndTicketSession(dd.Action):
    # label = _("End session")
    # label = u"\u231a\u2198"
    # label = u"↘"  # u"\u2198"
    label = u"◉"  # FISHEYE (U+25C9)
    help_text = _("End the active session on this ticket.")
    show_in_workflow = True
    show_in_bbar = False
    required_roles = dd.required(Worker)
    readonly = False
    
    def get_action_permission(self, ar, obj, state):
        # u = ar.get_user()
        # if not u.profile.has_required_roles([SiteUser]):
        #     # avoid query with AnonymousUser
        #     return False
        if not super(EndTicketSession, self).get_action_permission(
                ar, obj, state):
            return False
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=ar.get_user(), ticket=obj, end_time__isnull=True)
        if qs.count() == 0:
            return False
        return True

    def run_from_ui(self, ar, **kw):
        Session = rt.modules.clocking.Session
        ses = Session.objects.get(
            user=ar.get_user(), ticket=ar.selected_rows[0],
            end_time__isnull=True)
        ses.set_datetime('end', timezone.now())
        ses.full_clean()
        ses.save()
        ar.set_response(refresh=True)


class StartTicketSession(dd.Action):
    # label = _("Start session")
    # label = u"\u262d"
    # label = u"\u2692"
    # label = u"\u2690"
    # label = u"\u2328"
    # label = u"\u231a\u2197"
    # label = u"↗"  # \u2197
    label = u"▶"  # BLACK RIGHT-POINTING TRIANGLE (U+25B6)
    help_text = _("Start a session on this ticket.")
    # icon_name = 'emoticon_smile'
    show_in_workflow = True
    show_in_bbar = False
    readonly = False
    required_roles = dd.required(Worker)

    def get_action_permission(self, ar, obj, state):
        if obj.standby or obj.closed:
            return False
        u = ar.get_user()
        # if not u.profile.has_required_roles([SiteUser]):
            # avoid query with AnonymousUser
            # return False
        Session = rt.modules.clocking.Session
        qs = Session.objects.filter(
            user=u, ticket=obj, end_time__isnull=True)
        if qs.count():
            return False
        return super(StartTicketSession, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar, **kw):
        me = ar.get_user()
        obj = ar.selected_rows[0]

        ses = rt.modules.clocking.Session(ticket=obj, user=me)
        ses.full_clean()
        ses.save()
        ar.set_response(refresh=True)


if dd.is_installed('clocking'):  # Sphinx autodoc
    dd.inject_action(
        dd.plugins.clocking.ticket_model,
        start_session=StartTicketSession())
    dd.inject_action(
        dd.plugins.clocking.ticket_model,
        end_session=EndTicketSession())


class PrintActivityReport(DirectPrintAction):
    """Print an activity report.

    Not yet used. This is meant to be used as a list action on
    Session, but Lino does not yet support list actions with a
    parameter window.

    """
    select_rows = False
    # combo_group = "creacert"
    label = _("Activity report")
    tplname = "activity_report"
    build_method = "weasy2html"
    icon_name = None
    parameters = Monthly(
        show_remarks=models.BooleanField(
            _("Show remarks"), default=False),
        show_states=models.BooleanField(
            _("Show states"), default=True))
    params_layout = """
    start_date
    end_date
    show_remarks
    show_states
    """
    keep_user_values = True
    # default_format = 'json'
    # http_method = 'POST'
