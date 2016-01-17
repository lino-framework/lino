# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""This plugins installs a build method for generating printable
documents using `django-wkhtmltopdf
<https://github.com/incuna/django-wkhtmltopdf>`__

.. autosummary::
   :toctree:

    choicelists
    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("wkHtmlToPdf")

