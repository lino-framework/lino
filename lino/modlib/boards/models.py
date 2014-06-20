# Copyright 2008-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from lino import dd
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Board(dd.BabelNamed, dd.DatePeriod):

    class Meta:
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")


dd.update_field(Board, 'start_date', verbose_name=_("Works since"))
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


class BoardDecision(dd.Model):

    class Meta:
        abstract = True

    decided_date = models.DateField(
        verbose_name=_('Decided'), default=dd.today)
    board = models.ForeignKey('boards.Board', blank=True, null=True)

    @dd.chooser()
    def board_choices(self, decided_date):
        M = dd.resolve_model('boards.Board')
        qs = M.objects.all()
        if decided_date:
            qs = dd.PeriodEvents.active.add_filter(qs, decided_date)
        return qs


menu_host = dd.apps.contacts


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
    m.add_action('boards.Boards')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
    m.add_action('boards.Members')

