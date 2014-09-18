# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This module is for managing a reception desk and a waiting queue: 
register clients into a waiting queue 
as they present themselves at a reception desk (Empfangsschalter),
and unregister them when they leave again.

User documentation see :ref:`welfare.reception`.

"""
from lino import ad

from django.utils.translation import ugettext_lazy as _
#~ def _(s): return s


class Plugin(ad.Plugin):
    verbose_name = _("Reception")
    depends = ['cal']
