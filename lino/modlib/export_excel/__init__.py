# Copyright 2014-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This plugin installs a button to export any table to excel xls format.

To use it, simply add the following line to your
:meth:`lino.core.site.Site.get_installed_apps`::

    yield 'lino.modlib.export_excel'

"""

from lino import ad, _

class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Export to Excel xls format")
