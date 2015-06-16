# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.vat`.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.conf import settings
from django.db.models import Q

from lino.mixins.periods import DatePeriod
from lino.mixins import Sequenced
from lino.modlib.system.mixins import PeriodEvents

from lino.api import dd, rt, _

from lino.utils.xmlgen.html import E

from .utils import ZERO
from .choicelists import VatClasses, VatRegimes
from .mixins import VatDocument, VatItemBase

from lino.modlib.ledger.ui import PartnerVouchers, ByJournal
from lino.modlib.ledger.models import Voucher
from lino.modlib.ledger.mixins import Matchable, AccountInvoiceItem
from lino.modlib.ledger.choicelists import VoucherTypes
from lino.modlib.ledger.choicelists import TradeTypes


TradeTypes.purchases.update(
    base_account_field_name='purchases_account',
    base_account_field_label=_("Purchases Base account"),
    vat_account_field_name='purchases_vat_account',
    vat_account_field_label=_("Purchases VAT account"),
    partner_account_field_name='suppliers_account',
    partner_account_field_label=_("Suppliers account"))


class VatRule(Sequenced, DatePeriod):
    """A rule which defines how VAT is to be handled for a given invoice
    item.

    Example data see :mod:`lino.modlib.vat.fixtures.euvatrates`.

    Database fields:

    .. attribute:: country
    .. attribute:: vat_class

    .. attribute:: vat_regime

        The regime for which this rule applies. Pointer to
        :class:`VatRegimes <lino.modlib.vat.choicelists.VatRegimes>`.
    
    .. attribute:: rate
    
        The VAT rate to be applied. Note that a VAT rate of 20 percent is
        stored as `0.20` (not `20`).

    .. attribute:: can_edit

        Whether the VAT amount can be modified by the user. This applies
        only for documents with :attr:`VatTotal.auto_compute_totals` set
        to `False`.

    """
    class Meta:
        verbose_name = _("VAT rule")
        verbose_name_plural = _("VAT rules")

    country = dd.ForeignKey('countries.Country', blank=True, null=True)
    vat_class = VatClasses.field(blank=True)
    vat_regime = VatRegimes.field(blank=True)
    rate = models.DecimalField(default=ZERO, decimal_places=4, max_digits=7)
    can_edit = models.BooleanField(_("Editable amount"), default=True)

    @classmethod
    def get_vat_rule(cls, vat_regime, vat_class, country, date):
        """Return the one and only VatRule object to be applied for the given
criteria.

        """
        qs = cls.objects.order_by('seqno')
        qs = qs.filter(Q(country__isnull=True) | Q(country=country))
        if vat_class is not None:
            qs = qs.filter(Q(vat_class='') | Q(vat_class=vat_class))
        if vat_regime is not None:
            qs = qs.filter(
                Q(vat_regime='') | Q(vat_regime=vat_regime))
        qs = PeriodEvents.active.add_filter(qs, date)
        if qs.count() == 1:
            return qs[0]
        rt.show(VatRules)
        msg = _("Found {num} VAT rules for %{context}!)").format(
            num=qs.count(), context=dict(
                vat_regime=vat_regime, vat_class=vat_class,
                country=country.isocode, date=dd.fds(date)))
        # msg += " (SQL query was {0})".format(qs.query)
        dd.logger.info(msg)
        # raise Warning(msg)
        return None

    def __unicode__(self):
        kw = dict(
            vat_regime=self.vat_regime,
            vat_class=self.vat_class,
            rate=self.rate,
            country=self.country, seqno=self.seqno)
        return "{country} {vat_class} {rate}".format(**kw)


class VatAccountInvoice(VatDocument, Voucher, Matchable):
    """An invoice for which the user enters just the bare accounts and
    amounts (not products, quantities, discounts).

    An account invoice does not usually produce a printable
    document. This model is typically used to store incoming purchase
    invoices, but exceptions in both directions are possible: (1)
    purchase invoices can be stored using `purchases.Invoice` if stock
    management is important, or (2) outgoing sales invoice can have
    been created using some external tool and are entered into Lino
    just for the general ledger.

    """
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    # state = InvoiceStates.field(default=InvoiceStates.draft)


class InvoiceItem(AccountInvoiceItem, VatItemBase):
    """An item of an account invoice.  Inherits from
    :class:`AccountInvoiceItem
    <lino.modlib.ledger.mixins.AccountInvoiceItem>` and
    :class:`VatItemBase <lino.modlib.vat.models.VatItemBase>`.

    """
    voucher = dd.ForeignKey('vat.VatAccountInvoice', related_name='items')
    title = models.CharField(_("Description"), max_length=200, blank=True)


if False:
    """Install a post_init signal listener for each concrete subclass of
    VatDocument.  The following trick worked...  but best is to store
    it in VatRegime, not per voucher.

    """

    def set_default_item_vat(sender, instance=None, **kwargs):
        instance.item_vat = settings.SITE.get_item_vat(instance)
        #~ print("20130902 set_default_item_vat", instance)

    @dd.receiver(dd.post_analyze)
    def on_post_analyze(sender, **kw):
        for m in rt.models_by_base(VatDocument):
            dd.post_init.connect(set_default_item_vat, sender=m)
            #~ print('20130902 on_post_analyze installed receiver for',m)


dd.inject_field(
    'contacts.Partner',
    'vat_regime',
    VatRegimes.field(
        blank=True,
        help_text=_("The default VAT regime for \
        sales and purchases of this partner.")))

dd.inject_field(
    'contacts.Company',
    'vat_id',
    models.CharField(_("VAT id"), max_length=200, blank=True))

dd.inject_field(
    'contacts.Partner',
    'payment_term',
    models.ForeignKey(
        'ledger.PaymentTerm',
        blank=True, null=True,
        help_text=_("The default payment term for "
                    "sales invoices to this customer.")))

from .ui import *
