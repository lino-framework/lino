# Copyright 2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This plugins installs a build method for generating printable
documents using `django-wkhtmltopdf
<https://pypi.python.org/pypi/django-wkhtmltopdf>`__

This plugin is deprecated. We recommend to use either
:mod:`lino.modlib.weasyprint` or :mod:`lino_xl.lib.appypod` for
producing `.pdf` documents.

Note that `django-wkhtmltopdf` is not installed automatically.  So
before you to print something using this method, you need to run::

   $ pip install django-wkhtmltopdf



.. autosummary::
   :toctree:

    choicelists
    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("wkHtmlToPdf")

