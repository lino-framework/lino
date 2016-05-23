# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""This plugins installs a build method for generating printable
documents using `weasyprint
<http://weasyprint.readthedocs.io>`__.

In order to use this, you must (1) add it to your
:meth:`get_installed_apps` and (2) run ``pip install weasyprint`` in
your Python environment.



.. autosummary::
   :toctree:

    choicelists
    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("WeasyPrint")

