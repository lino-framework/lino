# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module is for managing a reception desk and a waiting queue:
register clients into a waiting queue as they present themselves at a
reception desk (Empfangsschalter), and unregister them when they leave
again.

It depends on :mod:`lino.modlib.cal`. It does not add any model, but
adds some workflow states, actions and tables.


Extended by :mod:`lino_welfare.modlib.reception`.

"""
from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Reception")
    depends = ['cal']
