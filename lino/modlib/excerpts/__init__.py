# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""See :mod:`ml.excerpts`.

.. autosummary::
   :toctree:

   models
   mixins
   choicelists
   fixtures.std

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Excerpts")

    needs_plugins = ['lino.modlib.outbox']

    def setup_main_menu(self, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('excerpts.MyExcerpts')

    def setup_config_menu(self, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('excerpts.ExcerptTypes')

    def setup_explorer_menu(self, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('excerpts.Excerpts')


