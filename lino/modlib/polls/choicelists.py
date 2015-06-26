# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for `lino.modlib.polls`, including the
:class:`PollsUser`.

"""
from lino.api import _
from lino.modlib.users.choicelists import SiteUser


class PollsUser(SiteUser):
    verbose_name = _("Polls user")


