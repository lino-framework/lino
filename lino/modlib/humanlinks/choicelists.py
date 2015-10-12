# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Choicelists for `lino.modlib.humanlinks`.

"""


from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.translation import string_concat
from lino.modlib.contacts.roles import ContactsStaff

from lino.api import dd


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
    """The global list of human link types.  This is used as choicelist
    for the :attr:`type <lino.modlib.humanlinks.models.Link.type>`
    field of a human link.

    The default list contains the following data:

    .. django2rst::
        
        rt.show(humanlinks.LinkTypes)

    .. attribute:: adoptive_parent

        A person who adopts a child of other parents as his or her own child.

    .. attribute:: stepparent

        Someone that your mother or father marries after the marriage
        to or relationship with your other parent has ended

    .. attribute:: foster_parent

        A man (woman) who looks after or brings up a child or children
        as a father (mother), in place of the natural or adoptive
        father (mother). [`thefreedictionary
        <http://www.thefreedictionary.com/foster+father>`_]

    """
    required_roles = dd.required(ContactsStaff)
    verbose_name = _("Parency type")
    verbose_name_plural = _("Parency types")
    item_class = LinkType

add = LinkTypes.add_item
add('01', 'parent',
    _("Father"), _("Mother"),
    _("Son"), _("Daughter"))

add('02',
    'adoptive_parent',
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
    'stepparent',
    _("Stepfather"), _("Stepmother"),
    _("Stepson"), _("Stepdaughter"))

add('09',
    'foster_parent',
    _("Foster father"), _("Foster mother"),
    _("Foster son"), _("Foster daughter"))

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


