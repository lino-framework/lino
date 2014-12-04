# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from lino import dd, mixins
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Board(mixins.BabelNamed, mixins.DatePeriod):

    class Meta:
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")

    def full_clean(self, *args, **kw):
        if not self.start_date:
            self.start_date = dd.today()
        super(Board, self).full_clean(*args, **kw)


dd.update_field(
    Board, 'start_date',
    verbose_name=_("Works since"),
    null=False)
dd.update_field(Board, 'end_date', verbose_name=_("Worked until"))


class Boards(dd.Table):
    model = 'boards.Board'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name *'
    order_by = ["name"]

    insert_layout = """
    name
    """

    detail_layout = """
    id name
    boards.MembersByBoard
    """


class Member(dd.Model):

    class Meta:
        verbose_name = _("Board member")
        verbose_name_plural = _("Board members")

    board = dd.ForeignKey('boards.Board')
    person = dd.ForeignKey("contacts.Person")
    role = dd.ForeignKey(
        "contacts.RoleType", blank=True, null=True)


class Members(dd.Table):
    model = 'boards.Member'
    required = dd.required(user_level='admin', user_groups='office')


class MembersByBoard(Members):
    master_key = 'board'
    column_names = "role person"
    order_by = ["role"]


class BoardDecision(mixins.UserAuthored):
    # base class for aids.Confirmation
    class Meta:
        abstract = True

    decision_date = models.DateField(
        verbose_name=_('Decided'), blank=True, null=True)
    board = models.ForeignKey('boards.Board', blank=True, null=True)

    @dd.chooser()
    def board_choices(self, decision_date):
        M = dd.resolve_model('boards.Board')
        qs = M.objects.all()
        if decision_date:
            qs = dd.PeriodEvents.active.add_filter(qs, decision_date)
        return qs


menu_host = dd.apps.contacts


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
    m.add_action('boards.Boards')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
    m.add_action('boards.Members')

