# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.vat`.

.. autosummary::

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from lino.modlib.accounts.utils import DEBIT, CREDIT

from lino.api import dd, rt, _


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
    verbose_name = _("VAT Regime")
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


class TradeType(dd.Choice):
    """
    Base class for the choices of :class:`TradeTypes`.

    """
    price_field_name = None
    price_field_label = None
    partner_account_field_name = None
    partner_account_field_label = None
    base_account_field_name = None
    base_account_field_label = None
    vat_account_field_name = None
    vat_account_field_label = None
    dc = DEBIT

    def get_base_account(self):
        """Return the :class:`lino.modlib.accounts.models.Account` into which
        the **base amount** of any operation should be booked.

        """
        if self.base_account_field_name is None:
            return None
            # raise Exception("%s has no base_account_field_name!" % self)
        return getattr(settings.SITE.site_config,
                       self.base_account_field_name)

    def get_vat_account(self):
        """Return the :class:`ml.accounts.Account` into which the **VAT
        amount** of any operation should be booked.

        """
        if self.vat_account_field_name is None:
            return None
            # raise Exception("%s has no vat_account_field_name!" % self)
        return getattr(settings.SITE.site_config, self.vat_account_field_name)

    def get_partner_account(self):
        """Return the :class:`ml.accounts.Account` into which the **total
      amount** of any operation (base + VAT) should be booked.

        """
        if self.partner_account_field_name is None:
            return None
        return getattr(
            settings.SITE.site_config, self.partner_account_field_name)

    def get_product_base_account(self, product):
        """Return the :class:`ml.accounts.Account` into which the **base
        amount** of any operation should be booked.

        """
        if self.base_account_field_name is None:
            raise Exception("%s has no base_account_field_name" % self)
        return getattr(product, self.base_account_field_name) or \
            getattr(settings.SITE.site_config, self.base_account_field_name)

    def get_catalog_price(self, product):
        """Return the catalog price of the given product for operations with
this trade type.

        """
        return getattr(product, self.price_field_name)


class TradeTypes(dd.ChoiceList):
    """The **trade type** is one of the basic properties of every
    accountable operation where are partner is involved.  Typical
    trade types are "Sales", "Purchases" and "Wages".

    """

    verbose_name = _("Trade Type")
    item_class = TradeType
    help_text = _("The type of trade: usually either `sales` or `purchases`.")

TradeTypes.add_item('S', _("Sales"), 'sales', dc=CREDIT)
TradeTypes.add_item('P', _("Purchases"), 'purchases', dc=DEBIT)
TradeTypes.add_item('W', _("Wages"), 'wages', dc=DEBIT)
TradeTypes.add_item('C', _("Clearings"), 'clearings', dc=DEBIT)

# Note that :mod:`lino.modlib.sales.models` and/or
# :mod:`lino.modlib.ledger.models` (if installed) will modify
# `TradeTypes.sales` at module level so that the following
# `inject_vat_fields` will inject the required fields to
# system.SiteConfig and products.Product (if these are installed).


@dd.receiver(dd.pre_analyze)
def inject_vat_fields(sender, **kw):
    for tt in TradeTypes.items():
        if tt.partner_account_field_name is not None:
            dd.inject_field(
                'system.SiteConfig',
                tt.partner_account_field_name,
                dd.ForeignKey(
                    'accounts.Account',
                    verbose_name=tt.partner_account_field_label,
                    related_name='configs_by_' + tt.partner_account_field_name,
                    blank=True, null=True))
        if tt.vat_account_field_name is not None:
            dd.inject_field('system.SiteConfig', tt.vat_account_field_name,
                            dd.ForeignKey(
                                'accounts.Account',
                                verbose_name=tt.vat_account_field_label,
                                related_name='configs_by_' +
                                tt.vat_account_field_name,
                                blank=True, null=True))
        if tt.base_account_field_name is not None:
            dd.inject_field('system.SiteConfig', tt.base_account_field_name,
                            dd.ForeignKey(
                                'accounts.Account',
                                verbose_name=tt.base_account_field_label,
                                related_name='configs_by_' +
                                tt.base_account_field_name,
                                blank=True, null=True))
            dd.inject_field('products.Product', tt.base_account_field_name,
                            dd.ForeignKey(
                                'accounts.Account',
                                verbose_name=tt.base_account_field_label,
                                related_name='products_by_' +
                                tt.base_account_field_name,
                                blank=True, null=True))
        if tt.price_field_name is not None:
            dd.inject_field('products.Product', tt.price_field_name,
                            dd.PriceField(verbose_name=tt.price_field_label,
                                          blank=True, null=True))


