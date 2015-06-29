# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Database models for `lino.modlib.humanlinks`.

.. autosummary::

"""


from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.translation import string_concat
from django.db.models import Q
from lino.modlib.contacts.roles import ContactsUser, ContactsStaff

from lino.api import dd, rt
from lino.utils.xmlgen.html import E

config = dd.apps.humanlinks


class LinkType(dd.Choice):

    symmetric = False

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
    required_roles = dd.required(ContactsStaff)
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
    _("Husband"), _("Wife"), symmetric=True)

add('06',
    'friend',
    pgettext("male", "Friend"), pgettext("female", "Friend"),
    pgettext("male", "Friend"), pgettext("female", "Friend"),
    symmetric=True)

add('07',
    'partner',
    pgettext("male", "Partner"), pgettext("female", "Partner"),
    pgettext("male", "Partner"), pgettext("female", "Partner"),
    symmetric=True)

add('08',
    'step',
    _("Stepfather"), _("Stepmother"),
    _("Stepson"), _("Stepdaughter"))

add('10',
    'sibling',
    pgettext("male", "Brother"), pgettext("female", "Sister"),
    pgettext("male", "Brother"), pgettext("female", "Sister"),
    symmetric=True)

add('11',
    'cousin',
    pgettext("male", "Cousin"), pgettext("female", "Cousin"),
    pgettext("male", "Cousin"), pgettext("female", "Cousin"),
    symmetric=True)

add('12',
    'uncle',
    _("Uncle"), _("Aunt"),
    _("Nephew"), _("Niece"))

add('80',
    'relative',
    pgettext("male", "Relative"), pgettext("female", "Relative"),
    pgettext("male", "Relative"), pgettext("female", "Relative"),
    symmetric=True)

add('90',
    'other',
    pgettext("male", "Other"), pgettext("female", "Other"),
    pgettext("male", "Other"), pgettext("female", "Other"),
    symmetric=True)


addable_link_types = (
    LinkTypes.parent, LinkTypes.adoptive,
    LinkTypes.spouse,
    LinkTypes.partner,
    LinkTypes.step,
    LinkTypes.sibling,
    LinkTypes.cousin,
    LinkTypes.uncle,
    LinkTypes.relative, LinkTypes.other)


class Link(dd.Model):

    class Meta:
        verbose_name = _("Personal Link")
        verbose_name_plural = _("Personal Links")

    type = LinkTypes.field(default=LinkTypes.parent)
    parent = dd.ForeignKey(
        config.person_model,
        verbose_name=_("Parent"),
        related_name='humanlinks_children')
    child = dd.ForeignKey(
        config.person_model,
        blank=True, null=True,
        verbose_name=_("Child"),
        related_name='humanlinks_parents')

    @dd.displayfield(_("Type"))
    def type_as_parent(self, ar):
        # print('20140204 type_as_parent', self.type)
        return self.type.as_parent(self.parent)

    @dd.displayfield(_("Type"))
    def type_as_child(self, ar):
        # print('20140204 type_as_child', self.type)
        return self.type.as_child(self.child)

    def __unicode__(self):
        if self.type is None:
            return super(Link, self).__unicode__()
        return _("%(child)s is %(what)s") % dict(
            child=unicode(self.child),
            what=self.type_of_parent_text())

    def type_of_parent_text(self):
        return _("%(type)s of %(parent)s") % dict(
            parent=self.parent,
            type=self.type.as_child(self.child))

    @classmethod
    def check_autocreate(cls, parent, child):
        if parent is None or child is None:
            return False
        if parent == child:
            return False
            # raise ValidationError("Parent and Child must differ")
        t = (LinkTypes.parent, LinkTypes.adoptive)
        qs = cls.objects.filter(parent=parent, child=child, type__in=t)
        if qs.count() == 0:
            obj = cls(parent=parent, child=child, type=LinkTypes.parent)
            obj.full_clean()
            obj.save()
            # dd.logger.info("20141018 autocreated %s", obj)
            return True
        return False


class Links(dd.Table):
    model = 'humanlinks.Link'
    required_roles = dd.required(ContactsStaff)
    stay_in_grid = True
    detail_layout = dd.FormLayout("""
    parent
    child
    type
    """, window_size=(40, 'auto'))


class LinksByHuman(Links):
    """Show all links for which this human is either parent or child."""
    label = _("Human Links")
    required_roles = dd.required(ContactsUser)
    master = config.person_model
    column_names = 'parent type_as_parent:10 child'
    slave_grid_format = 'summary'

    @classmethod
    def get_request_queryset(self, ar):
        mi = ar.master_instance  # a Person
        if mi is None:
            return
        Link = rt.modules.humanlinks.Link
        flt = Q(parent=mi) | Q(child=mi)
        return Link.objects.filter(flt).order_by(
            'child__birth_date', 'parent__birth_date')

    @classmethod
    def get_slave_summary(self, obj, ar):
        """The :meth:`summary view <lino.core.actors.Actor.get_slave_summary>`
        for :class:`LinksByHuman`.

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
                    i = (lnk.type.as_child(obj), lnk.parent)
                else:
                    i = (lnk.type.as_parent(obj), lnk.child)
                links.append(i)

        def by_age(a, b):
            return cmp(b[1].birth_date.as_date(), a[1].birth_date.as_date())

        try:
            links.sort(by_age)
        # except AttributeError:
        except (AttributeError, ValueError):
            # AttributeError: 'str' object has no attribute 'as_date'
            # possible when empty birth_date
            # ValueError: day is out of range for month
            pass

        items = []
        for type, other in links:
            items.append(E.li(
                unicode(type), _(" of "),
                obj.format_family_member(ar, other),
                " (%s)" % other.age()
            ))
        elems = []
        if len(items) > 0:
            elems += [_("%s is") % obj.first_name]
            elems.append(E.ul(*items))
        else:
            elems.append(_("No relationships."))

        # Buttons for creating relationships:
        sar = self.insert_action.request_from(ar)
        if sar.get_permission():
            actions = []
            for lt in addable_link_types:
                sar.known_values.update(type=lt, parent=obj)
                sar.known_values.pop('child', None)
                #sar = ar.spawn(self, known_values=dict(type=lt, parent=obj))
                btn = sar.ar2button(None, lt.as_parent(obj), icon_name=None)
                actions.append(btn)
                if not lt.symmetric:
                    actions.append('/')
                    sar.known_values.update(type=lt, child=obj)
                    sar.known_values.pop('parent', None)
                    btn = sar.ar2button(None, lt.as_child(obj), icon_name=None)
                    actions.append(btn)
                actions.append(' ')

            if len(actions) > 0:
                elems += [E.br(), _("Create relationship as ")] + actions
        return E.div(*elems)


# __all__ = [
#     'LinkTypes',
#     'Link',
#     'Links',
#     'LinksByHuman'
#     ]

