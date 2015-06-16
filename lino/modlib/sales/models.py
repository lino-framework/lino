# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.sales`.

"""

from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.core import actions
from lino import mixins

from lino.modlib.excerpts.mixins import Certifiable

from lino.modlib.vat.utils import add_vat, remove_vat, HUNDRED
from lino.modlib.vat.mixins import QtyVatItemBase, VatDocument
from lino.modlib.vat.mixins import get_default_vat_regime
from lino.modlib.ledger.mixins import Matchable, SequencedVoucherItem
from lino.modlib.ledger.models import Voucher
from lino.modlib.ledger.choicelists import TradeTypes
from lino.modlib.ledger.choicelists import VoucherTypes
from lino.modlib.ledger.ui import PartnerVouchers, ByJournal

# ledger = dd.resolve_app('ledger', strict=True)


TradeTypes.sales.update(
    price_field_name='sales_price',
    price_field_label=_("Sales price"),
    base_account_field_name='sales_account',
    base_account_field_label=_("Sales Base account"),
    vat_account_field_name='sales_vat_account',
    vat_account_field_label=_("Sales VAT account"),
    partner_account_field_name='clients_account',
    partner_account_field_label=_("Clients account"))

TradeTypes.wages.update(
    partner_account_field_name='wages_account',
    partner_account_field_label=_("Wages account"))

TradeTypes.clearings.update(
    partner_account_field_name='clearings_account',
    partner_account_field_label=_("Clearings account"))

dd.inject_field(
    'contacts.Partner',
    'invoice_recipient',
    dd.ForeignKey('contacts.Partner',
                  verbose_name=_("Invoicing address"),
                  blank=True, null=True))

#~ class Channel(ChoiceList):
    #~ label = _("Channel")
#~ add = Channel.add_item
#~ add('P',_("Paper"))
#~ add('E',_("E-mail"))


# class InvoiceStates(dd.Workflow):
#     """List of the possible values for the state of an :class:`Invoice`.

#     """
#     pass

# add = InvoiceStates.add_item
# add('10', _("Draft"), 'draft', editable=True)
# add('20', _("Registered"), 'registered', editable=False)
# add('30', _("Signed"), 'signed', editable=False)
# add('40', _("Sent"), 'sent', editable=False)
# add('50', _("Paid"), 'paid', editable=False)


# @dd.receiver(dd.pre_analyze)
# def sales_workflow(sender=None, **kw):
#     InvoiceStates.registered.add_transition(
#         _("Register"), states='draft', icon_name='accept')
#     InvoiceStates.draft.add_transition(
#         _("Deregister"), states="registered", icon_name='pencil')
#     #~ InvoiceStates.submitted.add_transition(_("Submit"),states="registered")


class ShippingMode(mixins.BabelNamed):
    """
    Represents a possible method of how the items described in a
    :class:`SalesDocument` are to be transferred from us to our customer.

    .. attribute:: price

    """
    class Meta:
        verbose_name = _("Shipping Mode")
        verbose_name_plural = _("Shipping Modes")

    price = dd.PriceField(blank=True, null=True)


class ShippingModes(dd.Table):

    model = 'sales.ShippingMode'


class SalesDocument(VatDocument, Certifiable):
    """Common base class for `orders.Order` and :class:`VatProductInvoice`.

    Subclasses must either add themselves a `date` field (as does
    Order) or inherit it from Voucher (as does VatProductInvoice)

    """

    auto_compute_totals = True

    class Meta:
        abstract = True

    language = dd.LanguageField()

    # ship_to = models.ForeignKey('contacts.Partner',
        # blank=True,null=True,
        # related_name="ship_to_%(class)s")
    # your_ref = models.CharField(
    #     _("Your reference"), max_length=200, blank=True)
    shipping_mode = models.ForeignKey(ShippingMode, blank=True, null=True)
    subject = models.CharField(_("Subject line"), max_length=200, blank=True)
    intro = models.TextField("Introductive Text", blank=True)
    discount = dd.PercentageField(_("Discount"), blank=True, null=True)

    def get_printable_type(self):
        return self.journal

    def get_print_language(self):
        return self.language

    def get_trade_type(self):
        return TradeTypes.sales

    def add_voucher_item(self, product=None, qty=None, **kw):
        Product = rt.modules.products.Product
        if product is not None:
            if not isinstance(product, Product):
                product = Product.objects.get(pk=product)
            #~ if qty is None:
                #~ qty = Duration(1)
        kw['product'] = product

        kw['qty'] = qty
        return super(SalesDocument, self).add_voucher_item(**kw)


class SalesDocuments(PartnerVouchers):
    pass


class VatProductInvoice(SalesDocument, Voucher, Matchable):
    """A sales invoice is a legal document which describes that something
    (the invoice items) has been sold to a given partner. The partner
    can be either a private person or an organization.

    Inherits from :class:`lino.modlib.ledger.models.Voucher`.

    """
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'VatProductInvoice')
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    order = dd.ForeignKey('orders.Order', blank=True, null=True)
    # state = InvoiceStates.field(default=InvoiceStates.draft)
    # workflow_state_field = 'state'

    def full_clean(self, *args, **kw):
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.date)
        # SalesDocument.before_save(self)
        # ledger.LedgerDocumentMixin.before_save(self)
        super(VatProductInvoice, self).full_clean(*args, **kw)

    #~ def before_state_change(self,ar,old,new):
        #~ if new.name == 'registered':
            #~ self.compute_totals()
        #~ elif new.name == 'draft':
            #~ pass
        #~ super(VatProductInvoice,self).before_state_change(ar,old,new)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(VatProductInvoice, cls).get_registrable_fields(site):
            yield f
        yield 'due_date'
        yield 'order'

        # yield 'imode'
        yield 'shipping_mode'
        yield 'discount'

        yield 'date'
        yield 'user'
        #~ yield 'item_vat'


class InvoiceDetail(dd.FormLayout):
    main = "general more ledger"

    totals = dd.Panel("""
    # discount
    total_base
    total_vat
    total_incl
    workflow_buttons
    """, label=_("Totals"))

    invoice_header = dd.Panel("""
    date partner vat_regime
    order subject your_ref
    payment_term due_date:20
    shipping_mode
    """, label=_("Header"))  # sales_remark

    general = dd.Panel("""
    invoice_header:60 totals:20
    ItemsByInvoice
    """, label=_("General"))

    more = dd.Panel("""
    id user language #project #item_vat
    intro
    """, label=_("More"))

    ledger = dd.Panel("""
    journal year number narration
    ledger.MovementsByVoucher
    """, label=_("Ledger"))


class Invoices(SalesDocuments):
    model = 'sales.VatProductInvoice'
    order_by = ["-id"]
    column_names = "id date partner total_incl user *"
    detail_layout = InvoiceDetail()
    insert_layout = dd.FormLayout("""
    partner date
    subject
    """, window_size=(40, 'auto'))
    # parameters = dict(
    #     state=VoucherStates.field(blank=True),
    #     **SalesDocuments.parameters)

    # start_at_bottom = True

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     qs = super(Invoices, cls).get_request_queryset(ar)
    #     pv = ar.param_values
    #     if pv.state:
    #         qs = qs.filter(state=pv.state)
    #     return qs


class InvoicesByJournal(Invoices, ByJournal):
    """Shows all invoices of a given journal (whose `voucher_type` must be
    :class:`VatProductInvoice`)

    """
    params_panel_hidden = True
    params_layout = "partner year state"
    column_names = "number date due_date " \
        "partner " \
        "total_incl order subject:10 " \
        "total_base total_vat user *"
                  #~ "ledger_remark:10 " \


class ProductDocItem(QtyVatItemBase):

    class Meta:
        abstract = True

    product = models.ForeignKey('products.Product', blank=True, null=True)
    description = dd.RichTextField(_("Description"), blank=True, null=True)
    discount = dd.PercentageField(_("Discount"), blank=True, null=True)

    def get_base_account(self, tt):
        if self.product is None:
            return
        return tt.get_product_base_account(self.product)
        #~ return self.voucher.journal.chart.get_account_by_ref(ref)

    def discount_changed(self, ar):
        if not self.product:
            return

        tt = self.voucher.get_trade_type()
        catalog_price = tt.get_catalog_price(self.product)

        if catalog_price is None:
            return
        #~ assert self.vat_class == self.product.vat_class
        rule = self.get_vat_rule()
        if rule is None:
            return
        cat_rule = rt.modules.vat.VatRule.get_vat_rule(
            get_default_vat_regime, self.get_vat_class(tt),
            dd.plugins.countries.get_my_country(),
            dd.today())
        if cat_rule is None:
            return
        if rule.rate != cat_rule.rate:
            catalog_price = remove_vat(catalog_price, cat_rule.rate)
            catalog_price = add_vat(catalog_price, cat_rule.rate)

        if self.discount is None:
            self.unit_price = catalog_price
        else:
            self.unit_price = catalog_price * \
                (HUNDRED - self.discount) / HUNDRED
        self.unit_price_changed(ar)

    def product_changed(self, ar):
        if self.product:
            self.title = self.product.name
            self.description = self.product.description
            if self.qty is None:
                self.qty = Decimal("1")
            self.discount_changed(ar)


class ItemsByDocument(dd.Table):
    column_names = "seqno:3 product title description:20x1 discount unit_price qty total_incl *"
    master_key = 'voucher'
    order_by = ["seqno"]


class InvoiceItem(ProductDocItem, SequencedVoucherItem):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'InvoiceItem')

    voucher = models.ForeignKey('sales.VatProductInvoice', related_name='items')
    title = models.CharField(_("Description"), max_length=200, blank=True)


class ItemsByInvoice(ItemsByDocument):
    #~ debug_permissions = 20130128
    model = 'sales.InvoiceItem'
    auto_fit_column_widths = True
    column_names = "seqno:3 product title description:20x1 \
    discount unit_price qty total_incl *"
    hidden_columns = "seqno description total_base total_vat"


class ItemsByInvoicePrint(ItemsByInvoice):
    column_names = "title:40 unit_price:10 qty:5 total_incl:10"


class InvoiceItemsByProduct(ItemsByInvoice):
    master_key = 'product'
    column_names = "voucher voucher__partner qty title \
description:20x1 discount unit_price total_incl total_base total_vat"
    editable = False
    #~ auto_fit_column_widths = True


class SignAction(actions.Action):
    label = "Sign"

    def run_from_ui(self, ar):

        def ok(ar):
            for row in ar.selected_rows:
                row.instance.user = ar.get_user()
                row.instance.save()
            ar.success(refresh=True)

        ar.confirm(
            ok, _("Going to sign %d documents as user %s. Are you sure?") % (
                len(ar.selected_rows),
                ar.get_user()))


class DocumentsToSign(Invoices):
    use_as_default_table = False
    filter = dict(user__isnull=True)
    #~ can_add = perms.never
    column_names = "number:4 order date " \
        "partner:10 " \
        "subject:10 total_incl total_base total_vat "
    #~ actions = Invoices.actions + [ SignAction() ]


class InvoicesByPartner(Invoices):
    #~ model = 'sales.VatProductInvoice'
    order_by = ["-date", '-id']
    master_key = 'partner'
    column_names = "date total_incl total_base total_vat *"


#~ class SalesByPerson(SalesDocuments):
    #~ column_names = "journal:4 number:4 date:8 " \
                   #~ "total_incl total_base total_vat *"
    #~ order_by = ["date"]
    #~ master_key = 'person'


@dd.receiver(dd.pre_analyze)
def add_voucher_type(sender, **kw):
    VoucherTypes.add_item('sales.VatProductInvoice', InvoicesByJournal)


#~ def customize_siteconfig():
    #~ """
    #~ Injects application-specific fields to :class:`SiteConfig <lino.models.SiteConfig>`.
    #~ """

    #~ from lino.models import SiteConfig
    #~ dd.inject_field(SiteConfig,
        #~ 'sales_base_account',
        #~ models.ForeignKey('accounts.Account',
            #~ blank=True,null=True,
            #~ verbose_name=_("Account for base amounts in sales invoices"),
            #~ related_name='sales_base_account'))
    #~ dd.inject_field(SiteConfig,
        #~ 'sales_vat_account',
        #~ models.ForeignKey('accounts.Account',
            #~ blank=True,null=True,
            #~ verbose_name=_("Account for VAT in sales invoices"),
            #~ related_name='sales_vat_account'))
    #~ dd.inject_field(SiteConfig,
        #~ 'customers_account',
        #~ models.ForeignKey('accounts.Account',
            #~ blank=True,null=True,
            #~ verbose_name=_("The account which represents the debts of our customers"),
            #~ related_name='customers_account'))


class ProductDetailMixin(dd.DetailLayout):
    sales = dd.Panel("""
    sales.InvoiceItemsByProduct
    """, label=dd.plugins.sales.verbose_name)
    

class PartnerDetailMixin(dd.DetailLayout):
    sales = dd.Panel("""
    invoice_recipient vat_regime payment_term
    sales.InvoicesByPartner
    """, label=dd.plugins.sales.verbose_name)


