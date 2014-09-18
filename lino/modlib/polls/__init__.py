# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
A polls app for Lino. This is the main app for :ref:`polly`.

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Polls")
