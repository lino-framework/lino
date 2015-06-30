# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds a user group "Office" and serves as menu hook for several
other modules.

.. autosummary::

  roles

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Office")

    # def on_site_startup(self, site):
    #     from lino.modlib.users.utils import add_user_group
    #     add_user_group(self.app_label, self.verbose_name)

