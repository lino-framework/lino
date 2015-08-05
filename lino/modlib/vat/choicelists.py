# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.vat`.

.. autosummary::

"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import dd, _


class VatClasses(dd.ChoiceList):
    """
    A VAT class is a direct or indirect property of a trade object
    (e.g. a Product) which determines the VAT *rate* to be used.  It
    does not contain the actual rate because this still varies
    depending on your country, the time and type of the operation, and
    possibly other factors.

    Typical content is as follows (but applications may redefine or
    extend this list in :meth:`lino.core.site.Site.setup_choicelists`):

    .. django2rst:: rt.show("vat.VatRegimes")

    """
    verbose_name = _("VAT Class")
    verbose_name_plural = _("VAT Classes")

add = VatClasses.add_item
add('0', _("Exempt"), 'exempt')    # post stamps, ...
add('1', _("Reduced"), 'reduced')  # food, books,...
add('2', _("Normal"), 'normal')    # everything else


class VatRegime(dd.Choice):
    "Base class for choices of :class:`VatRegimes`."

    item_vat = True
    "Whether unit prices are VAT included or not."


class VatRegimes(dd.ChoiceList):
    """
    The VAT regime is a classification of the way how VAT is being
    handled, e.g. whether and how it is to be paid.

    Typical content is as follows (but applications may redefine or
    extend this list in :meth:`lino.core.site.Site.setup_choicelists`):

    .. django2rst:: rt.show("vat.VatClasses")

    """
    verbose_name = _("VAT regime")
    verbose_name_plural = _("VAT regimes")
    item_class = VatRegime
    help_text = _(
        "Determines how the VAT is being handled, \
        i.e. whether and how it is to be paid.")

add = VatRegimes.add_item
add('10', _("Private person"), 'private')
add('20', _("Subject to VAT"), 'subject')
add('25', _("Co-contractor"), 'cocontractor')
add('30', _("Intra-community"), 'intracom')
add('40', _("Outside EU"), 'outside')
add('50', _("Exempt"), 'exempt', item_vat=False)

