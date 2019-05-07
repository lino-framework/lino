# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Provides a menu hook for several other plugins.

See :doc:`/specs/office`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Office")
