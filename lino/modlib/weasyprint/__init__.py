# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""This plugins installs two build methods for generating
:doc:`printable documents </admin/printing>`.

Both methods have the same input template, whose ending must be
:xfile:`.weasy.html`.

Both methods then render the input template through Jinja with the
standard context variables (defined by :meth:`get_printable_context
<lino.core.model.Model.get_printable_context>`.

The base build method :class:`WeasyBuildMethod
<lino.modlib.weasyprint.choicelists.WeasyBuildMethod>` then returns
this HTML output "as is", the other method runs `weasyprint
<http://weasyprint.readthedocs.io>`__ over the HTML file to convert it
to a :file:`.pdf` file.

In order to use this functionality, you must (1) add it to your
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

