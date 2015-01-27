# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino import ad


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu("vat", site.plugins.vat.verbose_name)
        m.add_action('declarations.Declarations')


