# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Concepts")

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('concepts.Concepts')


