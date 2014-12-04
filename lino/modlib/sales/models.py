# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"See :mod:`ml.sales`."

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)
import datetime

from decimal import Decimal
HUNDRED = Decimal('100')
ZERO = Decimal(0)

from django.db import models
from django.conf import settings
#~ from django.contrib.auth import models as auth
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from lino import dd, rt

#~ from lino import reports
from lino.core import actions
from lino import mixins
from lino.utils import mti
#~ from lino.utils.quantities import Duration

from lino.modlib.excerpts.mixins import Certifiable

from ..vat.utils import add_vat, remove_vat

#~ journals = resolve_app('journals')
#~ journals = models.get_app('journals')
#~ auth = resolve_app('auth')
#~ from lino.modlib.users import models as auth
partners = dd.resolve_app(settings.SITE.partners_app_label)
#~ accounts = dd.resolve_app('accounts')
ledger = dd.resolve_app('ledger', strict=True)
vat = dd.resolve_app('vat', strict=True)
products = dd.resolve_app('products', strict=True)


vat.TradeTypes.sales.update(
    price_field_name='sales_price',
    price_field_label=_("Sales price"),
    base_account_field_name='sales_account',
    base_account_field_label=_("Sales Base account"),
    vat_account_field_name='sales_vat_account',
    vat_account_field_label=_("Sales VAT account"),
    partner_account_field_name='clients_account',
    partner_account_field_label=_("Clients account"))

vat.TradeTypes.wages.update(
    partner_account_field_name='wages_account',
    partner_account_field_label=_("Wages account"))

vat.TradeTypes.clearings.update(
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


class InvoiceStates(dd.Workflow):
    pass

add = InvoiceStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)
add('30', _("Signed"), 'signed', editable=False)
add('40', _("Sent"), 'sent', editable=False)
add('50', _("Paid"), 'paid', editable=False)


InvoiceStates.registered.add_transition(
    _("Register"), states='draft', icon_name='accept')
InvoiceStates.draft.add_transition(
    _("Deregister"), states="registered", icon_name='pencil')
#~ InvoiceStates.submitted.add_transition(_("Submit"),states="registered")


class ShippingMode(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Shipping Mode")
        verbose_name_plural = _("Shipping Modes")

    price = dd.PriceField(blank=True, null=True)


class ShippingModes(dd.Table):

    model = ShippingMode


class SalesDocument(
        vat.VatDocument,
        ledger.Matchable,
        Certifiable):

    # Subclasses must either add themselves a date field (as does
    # Order) or inherit it from Voucher (as does Invoice)

    auto_compute_totals = True

    class Meta:
        abstract = True

    language = dd.LanguageField()

    # ship_to = models.ForeignKey('contacts.Partner',
        # blank=True,null=True,
        # related_name="ship_to_%(class)s")
    your_ref = models.CharField(
        _("Your reference"), max_length=200, blank=True)
    shipping_mode = models.ForeignKey(ShippingMode, blank=True, null=True)
    subject = models.CharField(_("Subject line"), max_length=200, blank=True)
    intro = models.TextField("Introductive Text", blank=True)
    discount = dd.PercentageField(_("Discount"), blank=True, null=True)

    def get_printable_type(self):
        return self.journal

    def get_print_language(self):
        return self.language

    def get_trade_type(self):
        return vat.TradeTypes.sales

    def add_voucher_item(self, product=None, qty=None, **kw):
        if product is not None:
            if not isinstance(product, products.Product):
                product = products.Product.objects.get(pk=product)
            #~ if qty is None:
                #~ qty = Duration(1)
        kw['product'] = product

        kw['qty'] = qty
        return super(SalesDocument, self).add_voucher_item(**kw)


class SalesDocuments(dd.Table):
    pass


class Invoice(SalesDocument, ledger.Voucher):
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Invoice')
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    due_date = models.DateField(_("Date of payment"), blank=True, null=True)
    order = dd.ForeignKey('orders.Order', blank=True, null=True)
    state = InvoiceStates.field(default=InvoiceStates.draft)
    workflow_state_field = 'state'

    def get_due_date(self):
        return self.due_date or self.date

    def full_clean(self, *args, **kw):
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.date)
        # SalesDocument.before_save(self)
        # ledger.LedgerDocumentMixin.before_save(self)
        super(Invoice, self).full_clean(*args, **kw)

    #~ def before_state_change(self,ar,old,new):
        #~ if new.name == 'registered':
            #~ self.compute_totals()
        #~ elif new.name == 'draft':
            #~ pass
        #~ super(Invoice,self).before_state_change(ar,old,new)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Invoice, cls).get_registrable_fields(site):
            yield f
        yield 'due_date'
        yield 'order'

        # yield 'imode'
        yield 'shipping_mode'
        yield 'discount'

        yield 'date'
        yield 'user'
        #~ yield 'item_vat'


class ProductDocItem(ledger.VoucherItem, vat.QtyVatItemBase):

    class Meta:
        abstract = True

    product = models.ForeignKey('products.Product', blank=True, null=True)
    #~ title = models.CharField(max_length=200,blank=True)
    description = dd.RichTextField(_("Description"), blank=True, null=True)
    #~ discount = models.IntegerField(_("Discount"),default=0)
    discount = dd.PercentageField(_("Discount"), blank=True, null=True)

    def get_base_account(self, tt):
        if self.product is None:
            return
        return tt.get_product_base_account(self.product)
        #~ return self.voucher.journal.chart.get_account_by_ref(ref)

    #~ def get_vat_class(self,tt):
        #~ name = settings.SITE.get_product_vat_class(tt,self.product)
        #~ return vat.VatClasses.get_by_name(name)

    #~ def full_clean(self,*args,**kw):
        #~ super(ProductDocItem,self).full_clean(*args,**kw)

    def discount_changed(self, ar):
        if not self.product:
            return

        tt = self.voucher.get_trade_type()
        catalog_price = tt.get_catalog_price(self.product)

        if catalog_price is not None:
            #~ assert self.vat_class == self.product.vat_class
            if self.voucher.vat_regime.item_vat:
                rate = self.get_vat_rate()  # rate of this item
            else:
                rate = ZERO
            catalog_rate = settings.SITE.plugins.vat.get_vat_rate(
                tt, self.vat_class, vat.get_default_vat_regime)
            if rate != catalog_rate:
                catalog_price = remove_vat(catalog_price, catalog_rate)
                catalog_price = add_vat(catalog_price, rate)
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

    def before_ui_save(self, ar):
        #~ if self.product:
            #~ if not self.title:
                #~ self.title = self.product.name
            #~ if not self.description:
                #~ self.description = self.product.description
            #~ if self.unit_price is None:
                #~ if self.product.price is not None:
                    #~ self.unit_price = self.product.price * (100 - self.discount) / 100
                    #~ self.unit_price_changed(ar)
        super(ProductDocItem, self).before_ui_save(ar)


#~ class ItemsByDocumentListLayout(layouts.ListLayout):
    #~ title_box = """
    #~ product
    #~ title
    #~ """
    #~ main = "pos:3 title_box description:20x1 discount unit_price qty total"
class ItemsByDocument(dd.Table):
    column_names = "seqno:3 product title description:20x1 discount unit_price qty total_incl *"
    master_key = 'voucher'
    order_by = ["seqno"]


class InvoiceItem(ProductDocItem):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'InvoiceItem')

    voucher = models.ForeignKey('sales.Invoice', related_name='items')


class ItemsByInvoice(ItemsByDocument):
    #~ debug_permissions = 20130128
    model = 'sales.InvoiceItem'
    auto_fit_column_widths = True
    column_names = "seqno:3 product title description:20x1 discount unit_price qty total_incl *"
    hidden_columns = "seqno description total_base total_vat"


class ItemsByInvoicePrint(ItemsByInvoice):
    column_names = "title:40 unit_price:10 qty:5 total_incl:10"


class InvoiceItemsByProduct(ItemsByInvoice):
    master_key = 'product'
    column_names = "voucher voucher__partner qty title description:20x1 discount unit_price total_incl total_base total_vat"
    editable = False
    #~ auto_fit_column_widths = True


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
    #~ parameters = dict(pyear=journals.YearRef())
    parameters = dict(
        year=ledger.FiscalYears.field(blank=True),
        state=InvoiceStates.field(blank=True),
        journal=ledger.JournalRef(blank=True))
    model = 'sales.Invoice'
    order_by = ["id"]
    column_names = "id date partner total_incl user *"
    detail_layout = InvoiceDetail()
    insert_layout = dd.FormLayout("""
    partner date
    subject
    """, window_size=(40, 'auto'))
    start_at_bottom = True

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Invoices, cls).get_request_queryset(ar)
        if not isinstance(qs, list):
            pv = ar.param_values
            #~ print 20120825, ar
            if pv.year:
                qs = qs.filter(year=pv.year)
            if pv.journal:
                qs = qs.filter(journal=pv.journal)
        return qs

    @classmethod
    def unused_param_defaults(cls, ar, **kw):
        kw = super(Invoices, cls).param_defaults(ar, **kw)
        kw.update(year=ledger.FiscalYears.from_date(settings.SITE.today()))
        return kw


class InvoicesByJournal(Invoices):
    order_by = ["number"]
    master_key = 'journal'  # see django issue 10808
    params_panel_hidden = True
    start_at_bottom = True
    #master = journals.Journal
    column_names = "number date due_date " \
        "partner " \
        "total_incl order subject:10 " \
        "total_base total_vat user *"
                  #~ "ledger_remark:10 " \

    @classmethod
    def get_title_base(self, ar):
        """
        Without this override we would have a title like "Invoices of journal <Invoices>"
        """
        return unicode(ar.master_instance)


#~ if settings.SITE.project_model:
  #~
    #~ class InvoicesByProject(Invoices):
        #~ order_by = ['-date']
        #~ master_key = 'project'

class SignAction(actions.Action):
    label = "Sign"

    def run_from_ui(self, ar):
        obj = ar.selected_rows[0]

        def ok(ar):
            for row in ar.selected_rows:
                row.instance.user = ar.get_user()
                row.instance.save()
            ar.success(refresh=True)

        ar.confirm(ok,
                   _("Going to sign %d documents as user %s. Are you sure?") % (
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
    #~ model = 'sales.Invoice'
    order_by = ["date"]
    master_key = 'partner'
    column_names = "date total_incl total_base total_vat *"


#~ class SalesByPerson(SalesDocuments):
    #~ column_names = "journal:4 number:4 date:8 " \
                   #~ "total_incl total_base total_vat *"
    #~ order_by = ["date"]
    #~ master_key = 'person'


@dd.receiver(dd.pre_analyze)
def add_voucher_type(sender, **kw):
    ledger.VoucherTypes.add_item('sales.Invoice', InvoicesByJournal)


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


MODULE_LABEL = settings.SITE.plugins.sales.verbose_name  # _("Sales")


def site_setup(site):
    if site.is_installed('products'):
        site.modules.products.Products.add_detail_tab(
            "sales",
            """
            sales.InvoiceItemsByProduct
            """,
            label=MODULE_LABEL)


class PartnerDetailMixin(dd.Panel):
    sales = dd.Panel(
        """
        invoice_recipient vat_regime payment_term
        sales.InvoicesByPartner
        """,
        label=MODULE_LABEL)


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("sales", MODULE_LABEL)
    # m.add_action(InvoicingModes)
    m.add_action(ShippingModes)


def setup_explorer_menu(site, ui, profile, m):
    pass

