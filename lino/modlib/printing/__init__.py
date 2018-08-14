# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds printing functionality to a Lino application.
See :doc:`/specs/printing`.

"""

from lino.api import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Printing")

    # needs_plugins = ['lino_xl.lib.appypod']
    # needs_plugins = ['lino.modlib.checkdata']

