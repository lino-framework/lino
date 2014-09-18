# Copyright 2010-2011 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines an Upload model.

"""
from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Uploads")

