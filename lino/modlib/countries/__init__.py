# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines models and choicelists for managing geographic places.


.. autosummary::
   :toctree:

    choicelists
    mixins
    models
    utils
    fixtures

See also :mod:`lino.modlib.statbel.countries`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Places")
    needs_plugins = ['lino.modlib.office']

    # settings:

    region_label = _("County")
    """The verbose_name of the region field."""

    country_code = 'BE'
    """The 2-letter ISO code of the country where the site owner is
    located.  This may not be empty, and there must be a country with
    that ISO code in :class:`lino.modlib.countries.models.Country`.

    """

    def on_site_startup(self, site):
        if self.country_code is None:
            raise Exception(
                "countries plugin requires a nonempty `country_code` setting.")

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('countries.Countries')
        m.add_action('countries.Places')

    def get_my_country(self):
        """Return the :class:`Country` instance configured by
:attr:`country_code`."""
        Country = self.site.modules.countries.Country
        try:
            return Country.objects.get(pk=self.country_code)
        except Country.DoesNotExist:
            return

