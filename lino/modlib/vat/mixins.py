# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Model mixins for `lino.modlib.vat`.

.. autosummary::

It defines two database models :class:`VatRule` and
:class:`PaymentTerm`, and a series of mixins which are used in
:mod:`lino.modlib.ledger`, :mod:`lino.modlib.sales` and other apps.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.conf import settings

from lino.api import dd, rt, _

from lino.modlib.ledger.mixins import (
    PartnerRelated, ProjectRelated, VoucherItem)

from .utils import ZERO, ONE
from .choicelists import VatClasses, VatRegimes


def get_default_vat_regime():
    return dd.plugins.vat.default_vat_regime


def get_default_vat_class():
    return dd.plugins.vat.default_vat_class


class VatTotal(dd.Model):
    """Model mixin which defines the fields `total_incl`, `total_base`
    and `total_vat`.  Used for both the document header
    (:class:`VatDocument`) and for each item (:class:`VatItemBase`).

    .. attribute:: total_incl
    
        A :class:`lino.core.fields.PriceField` which stores the total
        amount VAT *included*.

    .. attribute:: total_base

        A :class:`lino.core.fields.PriceField` which stores the total
        amount VAT *excluded*.

    .. attribute:: total_vat

        A :class:`lino.core.fields.PriceField` which stores the amount
        of VAT.

    """
    class Meta:
        abstract = True

    #~ price = dd.PriceField(_("Total"),blank=True,null=True)
    total_incl = dd.PriceField(_("Total incl. VAT"), blank=True, null=True)
    total_base = dd.PriceField(_("Total excl. VAT"), blank=True, null=True)
    total_vat = dd.PriceField(_("VAT"), blank=True, null=True)

    _total_fields = set('total_vat total_base total_incl'.split())
    # For internal use.  This is the list of field names to disable
    # when `auto_compute_totals` is True.

    auto_compute_totals = False
    """Set this to `True` on subclasses who compute their totals
    automatically, i.e. the fields :attr:`total_base`,
    :attr:`total_vat` and :attr:`total_incl` are disabled.  This is
    set to `True` for :class:`lino.modlib.sales.models.SalesDocument`.

    """

    def disabled_fields(self, ar):
        """Disable all three total fields if `auto_compute_totals` is set,
        otherwise disable :attr:`total_vat` if
        :attr:`VatRule.can_edit` is False.

        """
        fields = super(VatTotal, self).disabled_fields(ar)
        if self.auto_compute_totals:
            fields |= self._total_fields
        else:
            rule = self.get_vat_rule()
            if rule is not None and not rule.can_edit:
                fields.add('total_vat')
        return fields

    def reset_totals(self, ar):
        pass

    def get_vat_rule(self):
        """Called when user edits a total field in the document header when
        `auto_compute_totals` is False.

        """
        return None

    def total_base_changed(self, ar):
        """Called when user has edited the `total_base` field.  If total_base
        has been set to blank, then Lino fills it using
        :meth:`reset_totals`. If user has entered a value, compute
        :attr:`total_vat` and :attr:`total_incl` from this value using
        the vat rate. If there is no VatRule, `total_incl` and
        `total_vat` are set to None.

        If there are rounding differences, `total_vat` will get them.

        """
        # logger.info("20150128 total_base_changed %r", self.total_base)
        if self.total_base is None:
            self.reset_totals(ar)
            if self.total_base is None:
                return

        rule = self.get_vat_rule()
        # logger.info("20150128 %r", rule)
        if rule is None:
            self.total_incl = None
            self.total_vat = None
        else:
            self.total_incl = self.total_base * (ONE + rule.rate)
            self.total_vat = self.total_incl - self.total_base

    def total_vat_changed(self, ar):
        """Called when user has edited the `total_vat` field.  If it has been
        set to blank, then Lino fills it using
        :meth:`reset_totals`. If user has entered a value, compute
        :attr:`total_incl`. If there is no VatRule, `total_incl` is
        set to None.

        """
        if self.total_vat is None:
            self.reset_totals(ar)
            if self.total_vat is None:
                return

        if self.total_base is None:
            self.total_base = ZERO
        self.total_incl = self.total_vat + self.total_base

    def total_incl_changed(self, ar):
        """Called when user has edited the `total_incl` field.  If total_incl
        has been set to blank, then Lino fills it using
        :meth:`reset_totals`. If user enters a value, compute
        :attr:`total_base` and :attr:`total_vat` from this value using
        the vat rate. If there is no VatRule, `total_incl` should be
        disabled, so this method will never be called.

        If there are rounding differences, `total_vat` will get them.

        """
        if self.total_incl is None:
            self.reset_totals(ar)
            if self.total_incl is None:
                return
        #~ assert not isinstance(self.total_incl,basestring)
        rule = self.get_vat_rule()
        if rule is None:
            self.total_base = None
            self.total_vat = None
        else:
            self.total_base = self.total_incl / (ONE + rule.rate)
            self.total_vat = self.total_incl - self.total_base


class VatDocument(PartnerRelated, ProjectRelated, VatTotal):
    """Abstract base class for invoices, offers and other vouchers.

    .. attribute:: refresh_after_item_edit

        The total fields of an invoice are currently not automatically
        updated each time an item is modified.  Users must click the
        Save or the Register button to see the invoices totals.

        One idea is to have
        :meth:`lino.modlib.vat.models.VatItemBase.after_ui_save`
        insert a `refresh_all=True` (into the response to the PUT or
        POST coming from Lino.GridPanel.on_afteredit).
        
        This has the disadvantage that the cell cursor moves to the
        upper left corner after each cell edit.  We can see how this
        feels by setting :attr:`refresh_after_item_edit` to `True`.

    .. attribute:: vat_regime

        The VAT regime to be used in this document.  A pointer to
        :class:`VatRegimes`.

    """

    auto_compute_totals = True

    refresh_after_item_edit = False

    class Meta:
        abstract = True

    vat_regime = VatRegimes.field()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(VatDocument, cls).get_registrable_fields(site):
            yield f
        yield 'vat_regime'

    if False:
        # this didn't work as expected because __init__() is called
        # also when an existing instance is being retrieved from database
        def __init__(self, *args, **kw):
            super(VatDocument, self).__init__(*args, **kw)
            self.item_vat = settings.SITE.get_item_vat(self)

    def compute_totals(self):
        if self.pk is None:
            return
        base = Decimal()
        vat = Decimal()
        for i in self.items.all():
            if i.total_base is not None:
                base += i.total_base
                vat += i.total_vat
        self.total_base = base
        self.total_vat = vat
        self.total_incl = vat + base

    def get_sums_dict(self):
        sums_dict = dict()

        def book(account, amount):
            if account in sums_dict:
                sums_dict[account] += amount
            else:
                sums_dict[account] = amount
        #~ if self.journal.type == JournalTypes.purchases:
        tt = self.get_trade_type()
        vat_account = tt.get_vat_account()
        if vat_account is None:
            raise Exception("No VAT account for %s." % tt)
        for i in self.items.order_by('seqno'):
            if i.total_base:
                b = i.get_base_account(tt)
                if b is None:
                    raise Exception(
                        "No base account for %s (total_base is %r)" % (
                            i, i.total_base))
                book(b, i.total_base)
            if i.total_vat:
                book(vat_account, i.total_vat)
        return sums_dict

    def get_wanted_movements(self):
        sums_dict = self.get_sums_dict()
        #~ logger.info("20120901 get_wanted_movements %s",sums_dict)
        sum = Decimal()
        for a, m in sums_dict.items():
            if m:
                yield self.create_movement(a, None, not self.journal.dc, m)
                sum += m

        a = self.get_trade_type().get_partner_account()
        if a is not None:
            yield self.create_movement(
                a, None, self.journal.dc, sum, partner=self.partner,
                match=self.match)

    def fill_defaults(self):
        if not self.payment_term:
            self.payment_term = self.partner.payment_term
        if not self.vat_regime:
            self.vat_regime = self.partner.vat_regime
            if not self.vat_regime:
                self.vat_regime = get_default_vat_regime()

    def full_clean(self, *args, **kw):
        self.fill_defaults()
        self.compute_totals()
        super(VatDocument, self).full_clean(*args, **kw)

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.compute_totals()
        elif new.name == 'draft':
            pass
        super(VatDocument, self).before_state_change(ar, old, new)


class VatItemBase(VoucherItem, VatTotal):
    """Model mixin for items of a :class:`VatTotal`.

    Abstract Base class for
    :class:`lino.modlib.ledger.models.InvoiceItem`, i.e. the lines of
    invoices *without* unit prices and quantities.

    Subclasses must define a field called "voucher" which must be a
    ForeignKey with related_name="items" to the "owning document",
    which in turn must be a subclass of :class:`VatDocument`).

    .. attribute:: vat_class

        The VAT class to be applied for this item. A pointer to
        :class:`VatClasses`.

    """

    class Meta:
        abstract = True

    vat_class = VatClasses.field(blank=True, default=get_default_vat_class)

    def get_vat_class(self, tt):
        return dd.plugins.vat.get_vat_class(tt, self)

    def vat_class_changed(self, ar):
        #~ logger.info("20121204 vat_class_changed")
        if self.voucher.vat_regime.item_vat:
            self.total_incl_changed(ar)
        else:
            self.total_base_changed(ar)

    def get_base_account(self, tt):
        raise NotImplementedError

    def get_vat_rule(self):
        if self.vat_class is None:
            tt = self.voucher.get_trade_type()
            self.vat_class = self.get_vat_class(tt)
        rule = rt.modules.vat.VatRule.get_vat_rule(
            self.voucher.vat_regime, self.vat_class,
            self.voucher.partner.country or
            dd.plugins.countries.get_my_country(),
            self.voucher.date)
        return rule

    #~ def save(self,*args,**kw):
        #~ super(VatItemBase,self).save(*args,**kw)
        #~ self.voucher.full_clean()
        #~ self.voucher.save()

    def set_amount(self, ar, amount):
        self.voucher.fill_defaults()
        # rule = self.get_vat_rule()
        # if rule is None:
        #     rate = ZERO
        # else:
        #     rate = rule.rate
        if self.voucher.vat_regime.item_vat:  # unit_price_includes_vat
            self.total_incl = amount
            self.total_incl_changed(ar)
        else:
            self.total_base = amount
            self.total_base_changed(ar)

    def reset_totals(self, ar):
        """
        """
        if not self.voucher.auto_compute_totals:
            total = Decimal()
            for item in self.voucher.items.exclude(id=self.id):
                total += item.total_incl
            #~ if total != self.voucher.total_incl:
            self.total_incl = self.voucher.total_incl - total
            self.total_incl_changed(ar)

        super(VatItemBase, self).reset_totals(ar)

    def before_ui_save(self, ar):
        if self.total_incl is None:
            self.reset_totals(ar)
        super(VatItemBase, self).before_ui_save(ar)

    def after_ui_save(self, ar, cw):
        """
        After editing a grid cell automatically show new invoice totals.
        See :srcref:`docs/tickets/68`
        """
        kw = super(VatItemBase, self).after_ui_save(ar, cw)
        if self.voucher.refresh_after_item_edit:
            ar.set_response(refresh_all=True)
            self.voucher.compute_totals()
            self.voucher.full_clean()
            self.voucher.save()
        return kw


class QtyVatItemBase(VatItemBase):
    """Model mixin for items of a :class:`VatTotal`, adds `unit_price` and
`qty`.

    Abstract Base class for :class:`lino.modlib.sales.InvoiceItem` and
    :class:`lino.modlib.sales.OrderItem`, i.e. the lines of invoices
    *with* unit prices and quantities.

    """

    class Meta:
        abstract = True

    unit_price = dd.PriceField(_("Unit price"), blank=True, null=True)
    qty = dd.QuantityField(_("Quantity"), blank=True, null=True)

    def unit_price_changed(self, ar):
        self.reset_totals(ar)

    def qty_changed(self, ar):
        self.reset_totals(ar)

    def reset_totals(self, ar):
        super(QtyVatItemBase, self).reset_totals(ar)
        #~ if not self.voucher.auto_compute_totals:
            #~ if self.qty:
                #~ if self.voucher.item_vat:
                    #~ self.unit_price = self.total_incl / self.qty
                #~ else:
                    #~ self.unit_price = self.total_base / self.qty

        if self.unit_price is not None and self.qty is not None:
            self.set_amount(ar, self.unit_price * self.qty)


