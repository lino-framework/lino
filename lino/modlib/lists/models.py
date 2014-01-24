# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.


"""The :xfile:`models.py` module for the :mod:`lino.modlib.lists` app.

This module defines the tables

- :class:`List`
- :class:`Membership`

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

from lino.modlib.contacts.models import ContactRelated
# contacts = dd.resolve_app('contacts')


class ListType(dd.BabelNamed):

    """Represents a possible choice for the `type` field of a
    :class:`List`.

    """

    class Meta:
        verbose_name = _("List Type")
        verbose_name_plural = _("List Types")


class ListTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = 'lists.ListType'
    column_names = 'name *'


class List(dd.BabelNamed, dd.Referrable):

    class Meta:
        verbose_name = _("Partner List")
        verbose_name_plural = _("Partner Lists")

    type = dd.ForeignKey('lists.ListType')
    remarks = models.TextField(_("Remarks"), blank=True)

    print_labels = dd.PrintLabelsAction()


class Lists(dd.Table):
    required = dd.required(user_level='manager')
    model = 'lists.List'
    column_names = 'name *'
    order_by = ['ref']

    insert_layout = dd.FormLayout("""
    ref type
    name
    remarks
    """, window_size=(60, 12))

    detail_layout = dd.FormLayout("""
    ref type id
    name
    remarks
    MembersByList
    """)


class Member(ContactRelated, dd.Sequenced):

    class Meta:
        verbose_name = _("List Member")
        verbose_name_plural = _("List Members")

    list = dd.ForeignKey('lists.List')
    remark = models.CharField(_("Remark"), max_length=200, blank=True)


dd.update_field(Member, 'contact_person', verbose_name=_("Person"))
dd.update_field(Member, 'contact_role', verbose_name=_("Role"))


class Members(dd.Table):
    required = dd.required(user_level='manager')
    model = 'lists.Member'


class MembersByList(Members):
    master_key = 'list'
    order_by = ['seqno']
    column_names = "seqno company contact_person contact_role remark"


class MembersByPerson(Members):
    master_key = 'contact_person'
    column_names = "list company contact_role remark"
    label = _("Memberships")


class MembersByCompany(Members):
    master_key = 'company'
    column_names = "list contact_person contact_role remark"
    label = _("Memberships")


MODULE_LABEL = dd.apps.contacts.verbose_name


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("contacts", MODULE_LABEL)
    m.add_action('lists.Lists')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("contacts", MODULE_LABEL)
    m.add_action('lists.ListTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("contacts", MODULE_LABEL)
    m.add_action('lists.Members')

