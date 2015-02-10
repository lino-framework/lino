# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. autosummary::
   :toctree:

    models


"""

from lino.api import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    def setup_site_menu(config, site, profile, m):
        m.add_action(site.modules.about.About)
        if site.use_experimental_features:
            m.add_action(site.modules.about.Models)
            m.add_action(site.modules.about.Inspector)
            m.add_action(site.modules.about.SourceFiles)
            m.add_action(site.modules.about.DetailLayouts)
            m.add_action(site.modules.about.WindowActions)
            m.add_action(site.modules.about.FormPanels)
