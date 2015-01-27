# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This app installs a button to "print" any table into PDf using
LibreOffice.  This requires :mod:`lino.utils.appy_pod`.

To use it, simply add the following line to your
:setting:`get_installed_apps`::

    yield 'lino.modlib.appypod'

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Appy POD")

