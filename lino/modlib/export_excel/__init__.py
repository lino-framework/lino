# Copyright 2014-2015 Josef Kejzlar, Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This app installs a button to "export" any table to excel xls format.

To use it, simply add the following line to your
:meth:`lino.core.site.Site.get_installed_apps`::

    yield 'lino.modlib.export_excel'

"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Export to Excel xls format")

