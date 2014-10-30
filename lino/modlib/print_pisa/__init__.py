# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This app installs a button to "print" any table into PDf using
Pisa.

To use it, simply add the following line to your
:meth:`ad.Site.get_installed_apps`::

    yield 'lino.modlib.print_pisa'

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Print table using Pisa")

