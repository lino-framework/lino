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

    verbose_name = _("Places")
    region_label = _("County")
