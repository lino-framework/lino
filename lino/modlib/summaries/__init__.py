# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Installs a framework for defining summary tables using the
:class:`Summary <lino.modlib.summaries.mixins.Summary>` model mixin
and the :manage:`checksummaries` command.

.. autosummary::
   :toctree:

    mixins
    management.commands.checksummaries

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

    def setup_config_menu(self, site, profile, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('system.SiteConfig', 'check_summaries')

