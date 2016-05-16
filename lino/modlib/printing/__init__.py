# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds printing functionality to your Lino application.
See :doc:`/admin/printing`.


.. autosummary::
   :toctree:

    choicelists
    actions
    utils
    mixins
    models

"""

from lino.api import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Printing")

    # needs_plugins = ['lino_xl.lib.appypod']
    # needs_plugins = ['lino.modlib.plausibility']

