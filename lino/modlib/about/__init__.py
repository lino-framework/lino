# Copyright 2008-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. autosummary::
   :toctree:

    models


"""

from lino.api import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    def setup_site_menu(self, site, user_type, m):
        m.add_action(site.models.about.About)
        # m.add_action(site.models.about.SiteSearch)
        if site.use_experimental_features:
            m.add_action(site.models.about.Models)
            m.add_action(site.models.about.Inspector)
            m.add_action(site.models.about.SourceFiles)
            # m.add_action(site.models.about.DetailLayouts)
            # m.add_action(site.models.about.WindowActions)
            # m.add_action(site.models.about.FormPanels)
