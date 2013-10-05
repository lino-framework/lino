# -*- coding: UTF-8 -*-
## Copyright 2008-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""


"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)
import datetime

from decimal import Decimal
HUNDRED = Decimal('100')
ZERO = Decimal(0)

from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django import forms
from django.conf import settings
#~ from django.contrib.auth import models as auth
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from lino import dd
        
#~ from lino import reports
from lino.core import actions
from lino import mixins
from lino.utils import mti
#~ from lino.utils.quantities import Duration

from ..vat.utils import add_vat, remove_vat

#~ journals = resolve_app('journals')
#~ journals = models.get_app('journals')
#~ auth = resolve_app('auth')
#~ from lino.modlib.users import models as auth
partners = dd.resolve_app(settings.SITE.partners_app_label)
#~ accounts = dd.resolve_app('accounts')
ledger = dd.resolve_app('ledger',strict=True)
vat = dd.resolve_app('vat',strict=True)
products = dd.resolve_app('products',strict=True)



vat.TradeTypes.sales.update(
    price_field_name='sales_price',
    price_field_label=_("Sales price"),
    base_account_field_name='sales_account',
    base_account_field_label=_("Sales Base account"),
    vat_account_field_name='sales_vat_account',
    vat_account_field_label=_("Sales VAT account"),
    partner_account_field_name='clients_account',
    partner_account_field_label=_("Clients account"))

dd.inject_field('contacts.Partner','invoicing_address',dd.ForeignKey('contacts.Partner',
        verbose_name=_("Invoicing address"),
        blank=True,null=True))
    


#~ class Channel(ChoiceList):
    #~ label = _("Channel")
#~ add = Channel.add_item
#~ add('P',_("Paper"))
#~ add('E',_("E-mail"))

class InvoiceStates(dd.Workflow):
    """
    This lists the possible values for the workflow of a :class:`Invoice`
    """
add = InvoiceStates.add_item
add('10',_("Draft"),'draft',editable=True)
add('20',_("Registered"),'registered',editable=False) 
add('30',_("Signed"),'signed',editable=False)
add('40',_("Sent"),'sent',editable=False)
add('50',_("Paid"),'paid',editable=False)




class PaymentTerm(dd.BabelNamed):
    """
    A convention on how an Invoice should be paid. 
    """
    
    class Meta:
        verbose_name = _("Payment Term")
        verbose_name_plural = _("Payment Terms")
        
    days = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    end_of_month = models.BooleanField(default=False)
    
    def get_due_date(self,date1):
        assert isinstance(date1,datetime.date), \
          "%s is not a date" % date1
        #~ print type(date1),type(relativedelta(months=self.months,days=self.days))
        d = date1 + relativedelta(months=self.months,days=self.days)
        if self.end_of_month:
            d = date(d.year,d.month+1,1)
            d = relativedelta(d,days=-1)
        return d


class PaymentTerms(dd.Table):
    model = PaymentTerm
    order_by = ["id"]
  

class InvoicingMode(mixins.PrintableType,dd.BabelNamed):
    """Represents a method of issuing/sending invoices.
    """
    class Meta:
        verbose_name = _("Invoicing Mode")
        verbose_name_plural = _("Invoicing Modes")
    #~ id = models.CharField(max_length=3, primary_key=True)
    #~ journal = journals.JournalRef()
    price = dd.PriceField(blank=True,null=True,help_text=_("""\
Additional fee charged when using this invoicing mode."""))
    #~ channel = Channel.field(help_text="""
        #~ Method used to send the invoice.""")
    #~ channel = models.CharField(max_length=1, 
                #~ choices=CHANNEL_CHOICES,help_text="""
    #~ Method used to send the invoice. 
                #~ """)
    advance_days = models.IntegerField(
        default=0,
        help_text="""
How many days in advance invoices should be posted so that the customer
has a chance to pay them in time.""")
    
    #~ def __unicode__(self):
        #~ return unicode(dd.babelattr(self,'name'))
        
#~ add_babel_field(InvoicingMode,'name')
        
        
class InvoicingModes(dd.Table):
    model = InvoicingMode
    
    
    
class ShippingMode(dd.BabelNamed):
    price = dd.PriceField(blank=True,null=True)
    class Meta:
        verbose_name = _("Shipping Mode")
        verbose_name_plural = _("Shipping Modes")
    
        
class ShippingModes(dd.Table):
    """
    Represents a possible method of how the items described in a SalesDocument 
    are to be transferred from us to our customer.
    """
    model = ShippingMode
    #~ order_by = ["id"]
    #~ can_view = perms.is_staff
    #~ def can_view(self,request):
      #~ return request.user.is_staff



class SalesRule(dd.Model):
    """
    A group of default values for certain parameters of a SalesDocument.
    """
    class Meta:
        verbose_name = _("Sales Rule")
        verbose_name_plural = _("Sales Rules")
    #journal = models.ForeignKey(journals.Journal,blank=True,null=True)
    #~ journal = journals.JournalRef(blank=True,null=True)
    imode = models.ForeignKey(InvoicingMode,blank=True,null=True)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    
    #~ def __unicode__(self):
        #~ return "SalesRule %d" % (self.id)
        
#~ def get_sales_rule(doc):
    #~ for r in SalesRule.objects.all().order_by("id"):
        #~ if r.journal is None or r.journal == doc.journal:
            #~ return r
            

#~ class Customer(dd.Model):
    #~ """
    #~ Mixin meant to be applied to contacts.Person, 
    #~ contacts.Company and/or contacts.Partner
    #~ """
    #~ class Meta:
        #~ abstract = True

    #~ payment_term = models.ForeignKey(PaymentTerm,
        #~ blank=True,null=True,help_text="""\
#~ The default payment term of sales invoices for this customer.""")
    #~ vat_regime = vat.VatRegimes.field(blank=True,help_text="""\
#~ The default `VAT regime` of sales invoices for this customer.""")
    #~ item_vat = models.BooleanField(default=False,help_text="""\
#~ The default item_vat settings of sales invoices for this customer.""")


#~ class Customer(contacts.Partner):
    #~ """
    #~ A Customer is a :class:`contacts.Partner` 
    #~ that can receive sales invoices.
    #~ """    
    #~ class Meta:
        #~ verbose_name =_("Customer")
        #~ verbose_name_plural =_("Customers")
        
    #~ # name = models.CharField(max_length=40)
    #~ # company = models.ForeignKey('contacts.Company',blank=True,null=True)
    #~ # person = models.ForeignKey('contacts.Person',blank=True,null=True)
    
    #~ payment_term = models.ForeignKey(PaymentTerm,
        #~ blank=True,null=True,help_text="""\
#~ The default payment term of sales invoices for this customer.""")
    #~ vat_regime = vat.VatRegimes.field(blank=True,help_text="""\
#~ The default `VAT regime` of sales invoices for this customer.""")
    #~ item_vat = models.BooleanField(default=False,help_text="""\
#~ The default item_vat settings of sales invoices for this customer.""")
    
        
    #~ def full_clean(self,*args,**kw):
        #~ if self.company_id is not None:
            #~ self.name = self.company.name
        #~ elif self.person_id is not None:
            #~ l = filter(lambda x:x,[self.person.last_name,self.person.first_name,self.person.title])
            #~ self.name = " ".join(l)
        #~ super(Customer,self).full_clean(*args,**kw)
        
    #~ def as_address(self,*args,**kw):
        #~ recipient = self.company or self.person
        #~ return recipient.as_address(self,*args,**kw)
    
    
#~ class Customers(dd.Table):
    #~ column_names = "name payment_term vat_exempt item_vat company person"
    #~ can_delete = True
    #~ model = Customer
    #~ order_by = ["name"]




class SalesDocument(
      #~ mixins.UserAuthored,
      vat.VatDocument,
      ledger.Matchable,
      #~ journals.Sendable,
      #~ journals.Journaled,
      #~ contacts.ContactDocument,
      mixins.TypedPrintable):
    """Common base class for `orders.Order` and :class:`Invoice`.
    
    #~ Subclasses must either add themselves a date field (as does Order) 
    #~ or inherit it from Voucher (as does Invoice)
    """
    
    auto_compute_totals = True
    
    class Meta:
        abstract = True
        
    #~ item_class = NotImplementedError
        
    #~ customer = models.ForeignKey("sales.Customer",
        #~ blank=True,null=True,
        #~ related_name="%(app_label)s_%(class)s_by_contact",
        #~ related_name="%(app_label)s_%(class)s_related",
        #~ )
    language = dd.LanguageField()
    
    #~ customer = models.ForeignKey(Customer,
        #~ related_name="customer_%(class)s")
    #~ ship_to = models.ForeignKey(Customer,
        #~ blank=True,null=True,
        #~ related_name="shipTo_%(class)s")
    your_ref = models.CharField(_("Your reference"),max_length=200,blank=True)
    imode = models.ForeignKey(InvoicingMode,blank=True,null=True)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    #~ sales_remark = models.CharField("Remark for sales",
      #~ max_length=200,blank=True)
    subject = models.CharField(_("Subject line"),max_length=200,blank=True)
    #~ vat_exempt = models.BooleanField(default=False)
    #~ item_vat = models.BooleanField(default=False)
    #~ total_base = dd.PriceField(blank=True,null=True)
    #~ total_vat = dd.PriceField(blank=True,null=True)
    intro = models.TextField("Introductive Text",blank=True)
    #~ user = models.ForeignKey(settings.SITE.user_model,blank=True,null=True)
    #status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    #~ discount = models.IntegerField(_("Discount"),blank=True,null=True)
    discount = dd.PercentageField(_("Discount"),blank=True,null=True)
    
    
    def get_printable_type(self):
        return self.journal

    def get_print_language(self):
        return self.language
        
    #~ @dd.chooser()
    #~ def partner_choices(self):
        #~ return Customer.objects.order_by('name')
        
    def get_trade_type(self):
        return vat.TradeTypes.sales
        
    def add_voucher_item(self,product=None,qty=None,**kw):
        if product is not None:
            if not isinstance(product,products.Product):
                product = products.Product.objects.get(pk=product)
            #~ if qty is None:
                #~ qty = Duration(1)
        kw['product'] = product 
        
        #~ unit_price = kw.get('unit_price',None)
        #~ if type(unit_price) == float:
            #~ kw['unit_price'] = "%.2f" % unit_price
        kw['qty'] = qty
        #print self,kw
        return super(SalesDocument,self).add_voucher_item(**kw)
        
    #~ @dd.virtualfield(dd.PriceField(_("Total incl. VAT")))
    #~ def total_incl(self,ar=None):
        #~ if self.total_base is None:
            #~ return None
        #~ return self.total_base + self.total_vat
    
    def unused_compute_totals(self):
        #~ logger.info("20121202 sales.compute_totals()")
        if self.pk is None:
            return
        total_base = 0
        total_vat = 0
        for i in self.items.all():
            if i.total_base is not None:
                total_base += i.total_base
            if i.total_vat is not None:
                total_vat += i.total_vat
            #~ if not i.product.vatExempt:
                #~ total_vat += i.total_base() * 0.18
        self.total_base = total_base
        self.total_vat = total_vat
        #~ if self.journal == "ORD":
            #~ print "  done before_save:", self
        

            
    def full_clean(self,*args,**kw):
        """
        """
        if self.imode is None:
            #~ self.imode_id = 1 # self.partner
            #~ self.imode_id = self.partner.imode
            self.imode = self.partner.imode
        super(SalesDocument,self).full_clean(*args,**kw)
        #~ r = get_sales_rule(self)
        #~ if r is None:
            #~ raise ValidationError("No sales rule for %s",self)
        #~ if self.imode is None:
            #~ self.imode = r.imode
        #~ if self.shipping_mode is None:
            #~ self.shipping_mode = r.shipping_mode
        #~ if self.shipping_mode is None:
            #~ self.shipping_mode = r.shipping_mode
      
#~ SALES_PRINTABLE_FIELDS = dd.fields_list(SalesDocument,
  #~ 'customer imode payment_term '
  #~ 'date your_ref subject '
  #~ 'language vat_exempt item_vat ')

class SalesDocuments(dd.Table):
    pass
    #~ model = SalesDocument
    #~ page_layouts = (DocumentPageLayout,)
    #actions = reports.Report.actions + [ PrintAction ]
    
    #~ def inlines(self):
        #~ return dict(items=ItemsByDocument())


        


#~ class Invoice(SalesDocument,ledger.Voucher,mixins.Registrable):
class Invoice(SalesDocument,ledger.Voucher):
    """
    An invoice usually used for selling something.
    """
    class Meta:
        abstract = settings.SITE.is_abstract_model('sales.Invoice')
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
    due_date = models.DateField(_("Date of payment"),blank=True,null=True)
    order = dd.ForeignKey('orders.Order',blank=True,null=True)
    
    state = InvoiceStates.field(default=InvoiceStates.draft)
    
    workflow_state_field = 'state'
    
    #~ _registrable_fields = set('date author partner vat_regime payment_term due_date'.split())
    
    def get_due_date(self):
        return self.due_date or self.date
        
    def full_clean(self,*args,**kw):
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.date)
        #SalesDocument.before_save(self)
        #ledger.LedgerDocumentMixin.before_save(self)
        super(Invoice,self).full_clean(*args,**kw)
        
        
    @classmethod
    def get_registrable_fields(cls,site):
        for f in super(Invoice,cls).get_registrable_fields(site): yield f
        yield 'due_date'
        yield 'order'
        
        yield 'payment_term'
        yield 'imode'
        yield 'shipping_mode'
        yield 'discount'
        
        yield 'date'
        yield 'user'
        yield 'partner'
        yield 'vat_regime'
        #~ yield 'item_vat'



class ProductDocItem(ledger.VoucherItem,vat.QtyVatItemBase):
    
    class Meta:
        abstract = True
        
    product = models.ForeignKey('products.Product',blank=True,null=True)
    #~ title = models.CharField(max_length=200,blank=True)
    description = dd.RichTextField(_("Description"),blank=True,null=True)
    #~ discount = models.IntegerField(_("Discount"),default=0)
    discount = dd.PercentageField(_("Discount"),blank=True,null=True)
    

    
    def get_base_account(self,tt):
        return tt.get_product_base_account(self.product)
        #~ return self.voucher.journal.chart.get_account_by_ref(ref)
        
    #~ def get_vat_class(self,tt):
        #~ name = settings.SITE.get_product_vat_class(tt,self.product)
        #~ return vat.VatClasses.get_by_name(name)
        
    #~ def full_clean(self,*args,**kw):
        #~ super(ProductDocItem,self).full_clean(*args,**kw)

    def discount_changed(self,ar):
        if not self.product:
            return

        tt = self.voucher.get_trade_type()
        catalog_price = tt.get_catalog_price(self.product)
            
        if catalog_price is not None:
            #~ assert self.vat_class == self.product.vat_class
            if self.voucher.vat_regime.item_vat:
                rate = self.get_vat_rate() # rate of this item
            else:
                rate = ZERO
            catalog_rate = settings.SITE.get_vat_rate(tt,
                self.vat_class,vat.get_default_vat_regime)
            if rate != catalog_rate:
                catalog_price = remove_vat(catalog_price,catalog_rate)
                catalog_price = add_vat(catalog_price,rate)
            if self.discount is None:
                self.unit_price = catalog_price
            else:
                self.unit_price = catalog_price * (HUNDRED - self.discount) / HUNDRED                    
            self.unit_price_changed(ar)
                
    def product_changed(self,ar):
        if self.product:
            self.title = self.product.name
            self.description = self.product.description
            if self.qty is None:
                self.qty = Decimal("1")
            self.discount_changed(ar)
        
    def before_ui_save(self,ar):
        #~ if self.product:
            #~ if not self.title:
                #~ self.title = self.product.name
            #~ if not self.description:
                #~ self.description = self.product.description
            #~ if self.unit_price is None:
                #~ if self.product.price is not None:
                    #~ self.unit_price = self.product.price * (100 - self.discount) / 100
                    #~ self.unit_price_changed(ar)
        super(ProductDocItem,self).before_ui_save(ar)
      


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
        abstract = settings.SITE.is_abstract_model('sales.InvoiceItem')
        
    voucher = models.ForeignKey('sales.Invoice',related_name='items') 

class ItemsByInvoice(ItemsByDocument):
    #~ debug_permissions = 20130128
    model = 'sales.InvoiceItem'
    auto_fit_column_widths = True
    column_names = "seqno:3 product title description:20x1 discount unit_price qty total_incl total_base total_vat"
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
    """,label=_("Totals"))
    
    invoice_header = dd.Panel("""
    date partner vat_regime 
    order subject your_ref 
    payment_term due_date:20 
    imode shipping_mode     
    """,label=_("Header")) # sales_remark 
    
    general = dd.Panel("""
    invoice_header:60 totals:20
    ItemsByInvoice
    """,label=_("General"))
    
    more = dd.Panel("""
    id user language #project #item_vat
    intro
    """,label=_("More"))
    
    ledger = dd.Panel("""
    journal year number narration
    ledger.MovementsByVoucher
    """,label=_("Ledger"))
    
class Invoices(SalesDocuments):
    #~ parameters = dict(pyear=journals.YearRef())
    parameters = dict(
        year=ledger.FiscalYears.field(blank=True),
        journal=ledger.JournalRef(blank=True))
    model = 'sales.Invoice'
    order_by = ["id"]
    column_names = "id date partner total_incl user *" 
    detail_layout = InvoiceDetail()
    insert_layout = dd.FormLayout("""
    partner date 
    subject
    """,window_size=(40,'auto'))
    
    @classmethod
    def get_request_queryset(cls,ar):
        qs = super(Invoices,cls).get_request_queryset(ar)
        #~ print 20120825, ar
        if ar.param_values.year:
            qs = qs.filter(year=ar.param_values.year)
        if ar.param_values.journal:
            qs = qs.filter(journal=ar.param_values.journal)
        return qs
    
    @classmethod
    def param_defaults(cls,ar,**kw):
        kw = super(Invoices,cls).param_defaults(ar,**kw)
        kw.update(year=ledger.FiscalYears.from_date(datetime.date.today()))
        return kw
        

    
class InvoicesByJournal(Invoices):
    order_by = ["number"]
    master_key = 'journal' # see django issue 10808
    params_panel_hidden = True
    #master = journals.Journal
    column_names = "number date due_date " \
                  "partner " \
                  "total_incl order subject:10 " \
                  "total_base total_vat user *"
                  #~ "ledger_remark:10 " \
                  
    @classmethod
    def get_title_base(self,ar):
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
    def run_from_ui(self,ar):
        obj = ar.selected_rows[0]
        def ok():
            for row in ar.selected_rows:
                row.instance.user = ar.get_user()
                row.instance.save()
            return ar.ui.success(refresh=True)
        return ar.prompt(
            "Going to sign %d documents as user %s. Are you sure?" % (
            len(ar.selected_rows),
            ar.get_user()),ok)

class DocumentsToSign(Invoices):
    use_as_default_table = False
    filter = dict(user__isnull=True)
    #~ can_add = perms.never
    column_names = "number:4 order date " \
                  "partner:10 imode " \
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
def add_voucher_type(sender,**kw):
    ledger.VoucherTypes.add_item('sales.Invoice',InvoicesByJournal)


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
        


def customize_partners():

    #~ for ms in 'contacts.Partner', 'contacts.Person', 'contacts.Company':
    partner_model = settings.SITE.partners_app_label + '.Partner'
    dd.inject_field(partner_model,
        'payment_term',
        models.ForeignKey(PaymentTerm,
            blank=True,null=True,
            help_text=_("The default payment term for sales invoices to this customer.")))
        
    dd.inject_field(partner_model,
        'vat_regime',
        vat.VatRegimes.field(
            blank=True,
            help_text=_("The default VAT regime for sales to this customer.")))
            
    #~ dd.inject_field(partner_model,
        #~ 'item_vat',
        #~ models.BooleanField(
            #~ default=False,
            #~ help_text=_("The default item VAT setting for sales to this customer.")))
        #~ 
    dd.inject_field(partner_model,
        'imode',
        models.ForeignKey(InvoicingMode,blank=True,null=True))
        
        



MODULE_LABEL = _("Sales")

def site_setup(site):
    if site.is_installed('products'):
        site.modules.products.Products.add_detail_tab("sales",
            """
            sales.InvoiceItemsByProduct
            """,
            label=MODULE_LABEL)
    #~ for t in (site.modules.partners.Partners,
              #~ site.modules.partners.Persons,
              #~ site.modules.partners.Organisations):
    for m in dd.models_by_base(site.modules.contacts.Partner):
        t = m.get_default_table()
        if not hasattr(t.detail_layout,'sales'):
            t.add_detail_tab("sales", """
            invoicing_address vat_regime imode payment_term 
            sales.InvoicesByPartner
            """,
            label=MODULE_LABEL)
    #~ site.modules.contacts.Partners.add_detail_tab("sales",
    #~ if site.is_installed('tickets'):
        #~ site.modules.tickets.Projects.add_detail_tab("sales","sales.InvoicesByProject")
    #~ site.modules.lino.SiteConfigs.add_detail_tab("sales","""
    #~ #sales_base_account
    #~ #sales_vat_account
    #~ customers_account
    #~ """,label=_("Sales"))


#~ def setup_main_menu(site,ui,profile,m): 
    #~ m = m.add_menu(vat.TradeTypes.sales.name,vat.TradeTypes.sales.text)
    
    #~ for jnl in ledger.Journal.objects.all():
        #~ if jnl.trade_type == vat.TradeTypes.sales:
            #~ m.add_action(jnl.voucher_type.table_class,
                #~ label=unicode(jnl),
                #~ params=dict(master_instance=jnl))
    
    #~ m.add_action(Invoices)
    #~ m.add_action(DocumentsToSign)

def setup_config_menu(site,ui,profile,m): 
    m = m.add_menu("sales",MODULE_LABEL)
    m.add_action(InvoicingModes)
    m.add_action(ShippingModes)
    m.add_action(PaymentTerms)
    
def setup_explorer_menu(site,ui,profile,m):
    pass
  
customize_partners()
#~ customize_siteconfig()

  
