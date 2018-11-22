# Copyright 2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Serves as menu hook for several other modules.

.. autosummary::
   :toctree:

    roles

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Office")
