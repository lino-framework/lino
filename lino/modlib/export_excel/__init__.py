# Copyright 2014 Josef Kejzlar, Luc Saffre
# License: BSD (see file COPYING for details)

"""This app installs a button to "export" any table to excel xls format.

To use it, simply add the following line to your
:meth:`ad.Site.get_installed_apps`::

    yield 'lino.modlib.export_excel'

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Export to Excel xls format")

