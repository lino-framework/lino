# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Add comments to any model instance.

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Comments")
