# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd


class LinkType(dd.Choice):
    def __init__(self, value, text, name,
                 mptext, fptext,
                 mctext, fctext,
                 **kw):
        self.mptext = mptext  # male parent
        self.fptext = fptext
        self.mctext = mctext
        self.fctext = fctext
        super(LinkType, self).__init__(value, text, name, **kw)

    def as_parent(self, human):
        if human is None: return self.text
        return human.mf(self.mptext, self.fptext)

    def as_child(self, human):
        if human is None: return self.text
        return human.mf(self.mctext, self.fctext)

    
class LinkTypes(dd.ChoiceList):
    verbose_name_plural = _("Link type")
    item_class = LinkType

add = LinkTypes.add_item
add('01',
    _("Natural parency"), 'natural',
    _("Father"), _("Mother"),
    _("Son"), _("Daughter"))

add('02',
    _("Adoptive parency"), 'adoptive',
    _("Adoptive father"), _("Adoptive mother"),
    _("Adopted son"), _("Adopted daughter"))


class Link(dd.Sequenced):

    class Meta:
        verbose_name = _("Human Link")
        verbose_name_plural = _("Human Links")

    type = LinkTypes.field(default=LinkTypes.natural)
    parent = dd.ForeignKey(
        dd.apps.humanlinks.human_model,
        verbose_name=_("Parent"),
        related_name='children')
    child = dd.ForeignKey(
        dd.apps.humanlinks.human_model,
        verbose_name=_("Child"),
        related_name='parents')

    @dd.displayfield(_("Type"))
    def type_as_parent(self, ar):
        # print('20140204 type_as_parent', self.type)
        return self.type.as_parent(self.parent)

    # @dd.virtualfield(LinkTypes.field())
    @dd.displayfield(_("Type"))
    def type_as_child(self, ar):
        # print('20140204 type_as_child', self.type)
        return self.type.as_child(self.child)


class Links(dd.Table):
    model = 'humanlinks.Link'
    required = dd.required(user_level='admin')
    insert_layout = dd.FormLayout("""
    type
    parent 
    child
    """, window_size=(40, 'auto'))
    detail_layout = dd.FormLayout("""
    id seqno type
    parent child
    """, window_size=(60, 'auto'))


class ParentsByHuman(Links):
    label = pgettext("(human)", "Parents")
    required = dd.required()
    master_key = 'child'
    column_names = 'type_as_parent:10 parent'
    auto_fit_column_widths = True


class ChildrenByHuman(Links):
    label = pgettext("(human)", "Children")
    required = dd.required()
    master_key = 'parent'
    column_names = 'type_as_child:10 child'
    auto_fit_column_widths = True


def setup_explorer_menu(site, ui, profile, m):
    p = dd.apps.contacts
    m = m.add_menu(p.app_label, p.verbose_name)
    m.add_action(Links)
    m.add_action(LinkTypes)


__all__ = [
    'LinkTypes',
    'Link',
    'Links',
    'ChildrenByHuman',
    'ParentsByHuman']

