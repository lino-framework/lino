# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.vat`.

.. autosummary::

It defines two database models :class:`VatRule` and
:class:`PaymentTerm`, and a series of mixins which are used in
:mod:`lino.modlib.ledger`, :mod:`lino.modlib.sales` and other apps.

"""

from __future__ import unicode_literals
from __future__ import print_function

import datetime

from dateutil.relativedelta import relativedelta

from django.db import models
from django.conf import settings
from django.db.models import Q

from lino.mixins.periods import DatePeriod
from lino.mixins import Sequenced
from lino.mixins import BabelNamed
from lino.modlib.system.mixins import PeriodEvents

from lino.api import dd, rt, _

from .utils import remove_vat, ZERO
from .choicelists import VatClasses, VatRegimes, TradeTypes
from .mixins import VatTotal, VatDocument, VatItemBase


class VatRule(Sequenced, DatePeriod):
    """Example data see :mod:`lino.modlib.vat.fixtures.euvatrates`

    .. attribute:: country
    .. attribute:: vat_class
    .. attribute:: vat_regime
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
    # trade_type = TradeTypes.field(blank=True)
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


class VatRules(dd.Table):
    model = 'vat.VatRule'
    column_names = "seqno country vat_class vat_regime \
    start_date end_date rate can_edit *"
    hide_sums = True
    auto_fit_column_widths = True


class PaymentTerm(BabelNamed):
    """A convention on how an invoice should be paid.

    """

    class Meta:
        verbose_name = _("Payment Term")
        verbose_name_plural = _("Payment Terms")

    days = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    end_of_month = models.BooleanField(default=False)

    def get_due_date(self, date1):
        assert isinstance(date1, datetime.date), \
            "%s is not a date" % date1
        d = date1 + relativedelta(months=self.months, days=self.days)
        if self.end_of_month:
            d = datetime.date(d.year, d.month + 1, 1)
            d = relativedelta(d, days=-1)
        return d


class PaymentTerms(dd.Table):
    model = 'vat.PaymentTerm'
    order_by = ["id"]


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
        'vat.PaymentTerm',
        blank=True, null=True,
        help_text=_("The default payment term for "
                    "sales invoices to this customer.")))
