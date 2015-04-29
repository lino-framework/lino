# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino.modlib.orders`.

.. autosummary::

"""

import logging
logger = logging.getLogger(__name__)
import datetime

from decimal import Decimal
HUNDRED = Decimal('100')

from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
#~ from django import forms
from django.conf import settings
#~ from django.contrib.auth import models as auth
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

#~ from lino import reports
from lino.core import actions
from lino import mixins
from lino.utils import mti
#~ from lino.utils.quantities import Duration


contacts = dd.resolve_app('contacts')
accounts = dd.resolve_app('accounts')
ledger = dd.resolve_app('ledger')
vat = dd.resolve_app('vat')
products = dd.resolve_app('products')
sales = dd.resolve_app('sales')


class OrderStates(dd.Workflow):
    pass
add = OrderStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)
add('30', _("Inactive"), 'inactive', editable=False)


@dd.receiver(dd.pre_analyze)
def setup_workflow(sender=None, **kw):
    OrderStates.registered.add_transition(_("Register"), states='draft')
    OrderStates.draft.add_transition(_("Deregister"), states="registered")


class Order(sales.SalesDocument, mixins.ProjectRelated, mixins.Registrable):

    """
    An Order is when a :class:`Customer` asks us to "deliver" a 
    given set of "products".
    """

    #~ date = models.DateField(help_text="""The official date of this voucher.""")

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    #~ item_class = OrderItem

    CYCLE_CHOICES = (
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
    )

    state = OrderStates.field(blank=True)

    cycle = models.CharField(max_length=1,
                             choices=CYCLE_CHOICES)
    start_date = models.DateField(blank=True, null=True,
      help_text="""Beginning of payable period. 
      Set to blank if no bill should be generated""")
    covered_until = models.DateField(blank=True, null=True)

    #~ objects = OrderManager()

    #~ def get_last_invoice(self):
        #~ invoices = self.invoice_set.order_by('date')
        #~ cnt = invoices.count()
        #~ if cnt == 0:
            #~ return None
        #~ return invoices[cnt-1]

    def skip_date(self, date):
        if self.cycle == "W":
            date += relativedelta(weeks=1)
        elif self.cycle == "M":
            date += relativedelta(months=1)
        elif self.cycle == "Q":
            date += relativedelta(months=3)
        elif self.cycle == "Y":
            date += relativedelta(years=1)
        else:
            raise Exception("Invalid cycle value %r in %s" % (
                self.cycle, self))
        return datetime.date(date.year, date.month, date.day)

    #~ def before_save(self):
        #~ SalesDocument.before_save(self)
        #~ if self.start_date is None:
            #~ self.start_date = self.date

    def full_clean(self, *args, **kw):
        if self.start_date is None:
            self.start_date = self.date
        super(Order, self).full_clean(*args, **kw)

    def make_invoice(self, make_until=None, simulate=False, today=None):

        if self.start_date is None:
            return
        if today is None:
            today = settings.SITE.today()

        if make_until is None:
            make_until = today

        # assume that billing occurs once every month
        # and that invoices must be sent out 5 days before they get paid
        # and that covering periods are never increased or decreased to
        # fit into the billing cycle.

        if self.covered_until:
            covered_until = self.covered_until
        else:
            covered_until = self.start_date - ONE_DAY

        if self.payment_term is None:
            r = get_sales_rule(self)
            payment_term = r.payment_term
        else:
            payment_term = self.payment_term

        expect_payment = payment_term.get_due_date(make_until)
        expect_payment += relativedelta(days=self.imode.advance_days)

        if expect_payment < covered_until:
            return  # no invoice needed today

        #last_invoice = self.get_last_invoice()
        cover_from = covered_until + ONE_DAY
        cover_until = self.skip_date(cover_from) - ONE_DAY
        qty = 1
        while cover_until < expect_payment:
            cover_until = self.skip_date(cover_until)
            qty += 1

        #~ print "today", type(today), today
        #~ print "date", type(date), date
        #~ assert isinstance(date,datetime.date)
        #~ assert isinstance(today,datetime.date)
        cover_text = "Period %s to %s" % (cover_from, cover_until)
        # print cover_text
        items = []
        for item in self.items.all():
            d = {}
            for fn in ('product', 'title', 'description',
                       'unit_price', 'qty'):
                d[fn] = getattr(item, fn)
            d['qty'] *= qty
            #d['total'] *= qty
            items.append(d)
        if simulate:
            return True
        #jnl = journals.get_journal(self.imode.journal)
        #~ invoice = self.imode.journal.create_voucher(
        invoice = Invoice(
            date=today,
            order=self,
            partner=self.partner,
            #~ ship_to=self.ship_to,
            imode=self.imode,
            payment_term=self.payment_term,
            shipping_mode=self.shipping_mode,
            subject=cover_text,
            your_ref=unicode(self),
        )

        invoice.full_clean()
        invoice.save()
        for d in items:
            i = invoice.add_item(**d)
            i.full_clean()
            i.save()
            #i = DocItem(voucher=invoice,**d)
            # i.save()
        invoice.full_clean()
        invoice.save()  # save again because totals have been updated
        self.covered_until = cover_until
        self.save()
        return invoice


class Orders(sales.SalesDocuments):
    model = Order
    #~ order_by = ["number"]

    column_names = "partner:20 imode " \
        "sales_remark:20 subject:20 total_incl " \
        "cycle start_date covered_until"

    #~ def inlines(self):
        #~ d = super(Orders,self).inlines()
        #~ d.update(emitted_invoices=InvoicesByOrder())
        #~ return d

#~ class OrdersByJournal(Orders):
    #~ order_by = ["number"]
    # ~ master_key = 'journal' # see django issue 10808
    #~ column_names = "number:4 date partner:20 imode " \
                  #~ "sales_remark:20 subject:20 total_incl " \
                  #~ "cycle start_date covered_until"


#~ class PendingOrdersParams(forms.Form):
    #~ make_until = forms.DateField(label="Make invoices until",
      #~ initial=settings.SITE.today()+ONE_DAY,required=False)

#~ class PendingOrders(Orders):
    #~ param_form = PendingOrdersParams

    #~ @classmethod
    #~ def get_queryset(self,master_instance,make_until=None):
        #~ assert master_instance is None
        #~ return Order.objects.pending(make_until=make_until)


class ProductDocItem(ledger.VoucherItem, vat.QtyVatItemBase):
    product = models.ForeignKey('products.Product', blank=True, null=True)
    #~ title = models.CharField(max_length=200,blank=True)
    description = dd.RichTextField(_("Description"), blank=True, null=True)
    discount = models.IntegerField(_("Discount"), default=0)

    def get_base_account(self, tt):
        ref = tt.get_product_base_account(self.product)
        return self.voucher.journal.chart.get_account_by_ref(ref)

    def product_changed(self, ar):
        if self.product:
            self.title = self.product.name
            self.description = self.product.description
            if self.qty is None:
                self.qty = Decimal("1")
            if self.product.price is not None:
                self.unit_price = self.product.price * \
                    (HUNDRED - self.discount) / HUNDRED
                self.unit_price_changed(ar)


class OrderItem(sales.ProductDocItem):
    voucher = models.ForeignKey(Order, related_name='items')


class OrderDetail(dd.FormLayout):
    totals = dd.Panel("""
    discount
    total_base
    total_vat
    total_incl
    workflow_buttons
    """, label=_("Totals"))

    header = dd.Panel("""
    id date partner language
    order your_ref sales_remark subject 
    imode due_date:20 shipping_mode payment_term  vat_regime #item_vat
    user project 
    """, label=_("Header"))

    main = """
    header:60 totals:20
    ItemsByOrder
    """


class InvoicesByOrder(sales.Invoices):
    master_key = "order"


class ItemsByOrder(sales.ItemsByDocument):
    model = OrderItem


class OrderItemsByProduct(ItemsByOrder):
    master_key = 'product'


#~ class SalesByCustomer(SalesDocuments):
class OrdersByPartner(Orders):
    #~ model = 'sales.Order'
    master_key = 'partner'
    order_by = ["start_date"]
    column_names = "start_date total_incl total_base total_vat *"


