# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"See :mod:`ml.outbox`."

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Outbox")

    needs_plugins = ['lino.modlib.uploads']
