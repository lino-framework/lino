# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt


def objects():
    ListType = rt.modules.lists.ListType
    List = rt.modules.lists.List

    mailing = ListType(**dd.str2kw('name', _("Mailing list")))
    yield mailing

    discuss = ListType(**dd.str2kw('name', _("Discussion group")))
    yield discuss

    flags = ListType(**dd.str2kw('name', _("Flags")))
    yield flags

    yield List(list_type=mailing, **dd.str2kw('name', _("Announcements")))
    yield List(list_type=mailing, **dd.str2kw('name', _("Weekly newsletter")))

    yield List(list_type=discuss, **dd.str2kw('name', _("General discussion")))
    yield List(list_type=discuss, **dd.str2kw('name', _("Beginners forum")))
    yield List(list_type=discuss, **dd.str2kw('name', _("Developers forum")))

    yield List(list_type=flags,
               **dd.str2kw('name', _("PyCon 2014")))
    yield List(list_type=flags,
               **dd.str2kw('name', _("Free Software Day 2014")))
    yield List(list_type=flags, **dd.str2kw('name', _("Schools")))


