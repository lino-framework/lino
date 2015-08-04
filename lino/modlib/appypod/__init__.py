# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This plugins installs a button to "print" any table into PDF using
LibreOffice.  This requires :mod:`lino.utils.appy_pod`.

.. autosummary::
   :toctree:

    choicelists
    mixins
    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Appy POD")

