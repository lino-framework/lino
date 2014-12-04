# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)


"""The :xfile:`models.py` module for the :mod:`lino.modlib.lists` app.

This module defines the tables

- :class:`List`
- :class:`Membership`

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino import dd, mixins


class ListType(mixins.BabelNamed):

    """Represents a possible choice for the `list_type` field of a
    :class:`List`.

    """

    class Meta:
        verbose_name = _("List Type")
        verbose_name_plural = _("List Types")


class ListTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = 'lists.ListType'
    column_names = 'name *'


class List(mixins.BabelNamed, mixins.Referrable):

    class Meta:
        verbose_name = _("Partner List")
        verbose_name_plural = _("Partner Lists")

    list_type = dd.ForeignKey('lists.ListType', blank=True, null=True)
    remarks = models.TextField(_("Remarks"), blank=True)

    print_labels = dd.PrintLabelsAction()


class Lists(dd.Table):
    required = dd.required(user_level='manager')
    model = 'lists.List'
    column_names = 'ref name list_type *'
    order_by = ['ref']

    insert_layout = dd.FormLayout("""
    ref list_type
    name
    remarks
    """, window_size=(60, 12))

    detail_layout = dd.FormLayout("""
    ref list_type id
    name
    remarks
    MembersByList
    """)


class Member(mixins.Sequenced):

    class Meta:
        verbose_name = _("List memberships")
        verbose_name_plural = _("List memberships")

    list = dd.ForeignKey('lists.List')
    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name="list_memberships")
    remark = models.CharField(_("Remark"), max_length=200, blank=True)


class Members(dd.Table):
    required = dd.required(user_level='manager')
    model = 'lists.Member'


class MembersByList(Members):
    master_key = 'list'
    order_by = ['seqno']
    column_names = "seqno partner remark"


class MembersByPartner(Members):
    master_key = 'partner'
    column_names = "list remark"
    order_by = ['list__ref']


MODULE_LABEL = settings.SITE.plugins.contacts.verbose_name


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("contacts", MODULE_LABEL)
    m.add_action('lists.Lists')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("contacts", MODULE_LABEL)
    m.add_action('lists.ListTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("contacts", MODULE_LABEL)
    m.add_action('lists.Members')
