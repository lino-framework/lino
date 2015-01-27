# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.modlib.countries` package
defines models and choicelists for managing geographic places.


.. autosummary::
   :toctree:

    choicelists
    mixins
    models
    utils
    fixtures.few_countries
    fixtures.few_cities
    fixtures.be
    fixtures.ee
    fixtures.eesti


"""

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Places")
    region_label = _("County")

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('countries.Countries')
        m.add_action('countries.Places')

