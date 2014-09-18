# Copyright 2008-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Import filters
"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Import filters")
