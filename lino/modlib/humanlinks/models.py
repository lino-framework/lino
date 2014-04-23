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
from django.utils.translation import string_concat
from django.conf import settings

from lino import dd


class LinkType(dd.Choice):

    def __init__(self, value, name,
                 mptext, fptext,
                 mctext, fctext,
                 **kw):
        self.mptext = mptext  # male parent
        self.fptext = fptext
        self.mctext = mctext
        self.fctext = fctext
        # text = string_concat(
        #     mptext, ' (', fptext, ') / ', mctext, ' (', fctext, ')')
        text = string_concat(mctext, ' (', fctext, ')')
        # text = "%s (%s) / %s (%s)" % (mptext, fptext, mctext, fctext)
        super(LinkType, self).__init__(value, text, name, **kw)

    def as_parent(self, human):
        if human is None:
            return self.text
        return human.mf(self.mptext, self.fptext)

    def as_child(self, human):
        if human is None:
            return self.text
        return human.mf(self.mctext, self.fctext)


class LinkTypes(dd.ChoiceList):
    required = dd.required(user_level='admin')
    verbose_name = _("Parency type")
    verbose_name_plural = _("Parency types")
    item_class = LinkType

add = LinkTypes.add_item
add('01', 'natural',
    _("Father"), _("Mother"),
    _("Son"), _("Daughter"))

add('02',
    'adoptive',
    _("Adoptive father"), _("Adoptive mother"),
    _("Adopted son"), _("Adopted daughter"))

add('03',
    'grandparent',
    _("Grandfather"), _("Grandmother"),
    _("Grandson"), _("Granddaughter"))

add('05',
    'partner',
    _("Husband"), _("Wife"),
    _("Husband"), _("Wife"))

add('06',
    'friend',
    _("Friend"), _("Friend"),
    _("Friend"), _("Friend"))

add('80',
    'relative',
    _("Relative"), _("Relative"),
    _("Relative"), _("Relative"))

add('90',
    'other',
    _("Other"), _("Other"),
    _("Other"), _("Other"))


# class Link(dd.Sequenced):
class Link(dd.Human, dd.Born):

    class Meta:
        verbose_name = _("Dependent Person")
        verbose_name_plural = _("Dependent Persons")

    type = LinkTypes.field(default=LinkTypes.natural)
    parent = dd.ForeignKey(
        settings.SITE.plugins.humanlinks.human_model,
        verbose_name=_("Parent"),
        related_name='children')
    child = dd.ForeignKey(
        settings.SITE.plugins.humanlinks.human_model,
        blank=True, null=True,
        #verbose_name=_("Child"),
        related_name='parents')

    @dd.displayfield(_("Type"))
    def type_as_parent(self, ar):
        # print('20140204 type_as_parent', self.type)
        return self.type.as_parent(self.parent)

    @dd.displayfield(_("Type"))
    def type_as_child(self, ar):
        # print('20140204 type_as_child', self.type)
        return self.type.as_child(self.child)

    # @dd.displayfield(_("Birth date"))
    # def birth_date(self, ar):
    #     return self.child.birth_date

    def full_clean(self):
        """Copy data fields from child"""
        obj = self.child
        if obj is not None:
            for k in ('first_name', 'last_name', 'gender', 'birth_date'):
                setattr(self, k, getattr(obj, k))


class Links(dd.Table):
    model = 'humanlinks.Link'
    required = dd.required(user_level='admin')
    # insert_layout = dd.FormLayout("""
    # type
    # parent
    # child
    # first_name last_name gender birth_date
    # """, window_size=(40, 'auto'))
    # detail_layout = dd.FormLayout("""
    # parent
    # child first_name last_name gender birth_date
    # type:20  id:6
    # """, window_size=(60, 'auto'))


class ParentsByHuman(Links):
    label = pgettext("(human)", "Parents")
    required = dd.required()
    master_key = 'child'
    column_names = 'type_as_parent:10 parent'
    auto_fit_column_widths = True
    # insert_layout = dd.FormLayout("""
    # parent
    # type
    # """, window_size=(40, 'auto'))


class ChildrenByHuman(Links):
    # label = pgettext("(human)", "Children")
    label = _("Dependent persons")
    required = dd.required()
    master_key = 'parent'
    column_names = 'type child first_name last_name gender birth_date age'
    #column_names = 'type_as_child:10 child child__birth_date child__age'
    auto_fit_column_widths = True
    # insert_layout = dd.FormLayout("""
    # child
    # first_name last_name
    # gender birth_date
    # type
    # """, window_size=(40, 'auto'))


def setup_explorer_menu(site, ui, profile, m):
    p = settings.SITE.plugins.contacts
    m = m.add_menu(p.app_label, p.verbose_name)
    m.add_action(Links)
    m.add_action(LinkTypes)


__all__ = [
    'LinkTypes',
    'Link',
    'Links',
    'ChildrenByHuman',
    'ParentsByHuman']

