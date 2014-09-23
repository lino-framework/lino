# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"See :mod:`ml.countries`."

from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Places")
    region_label = _("County")
