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
from django.db.models import Q

from lino import dd
from lino.utils.xmlgen.html import E


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
add('01', 'parent',
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
    'spouse',
    _("Husband"), _("Wife"),
    _("Husband"), _("Wife"))

add('07',
    'partner',
    _("Partner"), _("Partner"),
    _("Partner"), _("Partner"))

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


class Link(dd.Model):

    class Meta:
        verbose_name = _("Personal Link")
        verbose_name_plural = _("Personal Links")

    type = LinkTypes.field(default=LinkTypes.parent)
    parent = dd.ForeignKey(
        dd.apps.humanlinks.human_model,
        verbose_name=_("Parent"),
        related_name='children')
    child = dd.ForeignKey(
        dd.apps.humanlinks.human_model,
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


def pf(obj):
    return obj.get_full_name(nominative=True)


class LinksByHuman(Links):
    label = _("Human Links")
    required = dd.required()
    master = dd.apps.humanlinks.human_model
    column_names = 'parent type_as_parent:10 child'
    slave_grid_format = 'summary'

    @classmethod
    def get_request_queryset(self, ar):
        mi = ar.master_instance  # a Person
        if mi is None:
            return
        Link = dd.modules.humanlinks.Link
        flt = Q(parent=mi) | Q(child=mi)
        return Link.objects.filter(flt).order_by(
            'child__birth_date', 'parent__birth_date')

    @classmethod
    def get_slave_summary(self, obj, ar):
        sar = self.request(master_instance=obj)
        links = []
        for lnk in sar:
            if lnk.child == obj:
                i = (lnk.type.as_child(obj), lnk.parent)
            else:
                i = (lnk.type.as_parent(obj), lnk.child)
            links.append(i)

        def by_age(a, b):
            return cmp(b[1].birth_date.as_date(), a[1].birth_date.as_date())

        links.sort(by_age)

        items = []
        for type, other in links:
            items.append(E.li(
                unicode(type), _(" of "),
                ar.obj2html(other, pf(other)),
                " (%s)" % other.age()
            ))
        elems = []
        if len(items) > 0:
            elems += [_("%s is") % pf(obj)]
            elems.append(E.ul(*items))
        # elems += [
        #     E.br(), ar.instance_action_button(obj.create_household)]
        return E.div(*elems)


def setup_explorer_menu(site, ui, profile, m):
    p = dd.apps.contacts
    m = m.add_menu(p.app_label, p.verbose_name)
    m.add_action(Links)
    m.add_action(LinkTypes)


__all__ = [
    'LinkTypes',
    'Link',
    'Links',
    'LinksByHuman'
    ]

