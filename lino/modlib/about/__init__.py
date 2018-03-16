# Copyright 2008-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
See :doc:`/specs/about`.

"""

from lino.api import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    def setup_site_menu(self, site, user_type, m):
        m.add_action(site.models.about.About)
        # m.add_action(site.models.about.SiteSearch)
