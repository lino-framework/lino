# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""A framework for defining and managing summary tables.
See :doc:`/specs/summaries`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """See :doc:`/dev/plugins`.

    """
    verbose_name = _("Summaries")

    start_year = None
    """The first year for which summaries should be computed."""

    end_year = None
    """The last year for which summaries should be computed."""

    def on_init(self):
        if self.end_year is None:
            self.end_year = self.site.today().year
        if self.start_year is None:
            self.start_year = self.end_year - 2

    # def setup_config_menu(self, site, user_type, m):
    #     g = site.plugins.system
    #     m = m.add_menu(g.app_label, g.verbose_name)
    #     m.add_action('system.SiteConfig', 'check_summaries')

