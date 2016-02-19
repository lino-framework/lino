# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""This plugin installs a series of build methods for generating
printable documents using LibreOffice.

These build methods require a running LibreOffice server (see
:ref:`admin.oood`).  Compared to the built-in :class:`PisaBuildMethod
<lino.modlib.printing.choicelists.PisaBuildMethod>`.  This has the
disadvantage of requiring more effort to get started, but it has
several advantages:

- Can be used to produce editable files (`.rtf` or `.odt`) from the
  same `.odt` template.
- Features like automatic hyphenation, sophisticated fonts and layouts
  are beyond the scope of pisa.
- Templates are `.odt` files (not `.html`), meaning that end-users
  dare to edit them more easily.

This plugin also adds a generic button to "print" *any* table into PDF
using LibreOffice.

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

