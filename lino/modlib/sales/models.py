# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)
import datetime
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django.conf import settings
#~ from django.contrib.auth import models as auth
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from lino import dd
        
#~ from lino import reports
from lino.core import actions
from lino import mixins
from lino.utils import mti
from lino.utils import babel 
#~ from lino.utils.babel import add_babel_field, babelattr
#~ from lino.utils.quantities import Duration


#~ journals = resolve_app('journals')
#~ journals = models.get_app('journals')
#~ auth = resolve_app('auth')
#~ from lino.modlib.users import models as auth
contacts = dd.resolve_app('contacts')
ledger = dd.resolve_app('ledger')
vat = dd.resolve_app('vat')
products = dd.resolve_app('products')
#~ from lino.modlib.ledger import models as ledger
#~ from lino.modlib.journals import models as journals
#~ from lino.modlib.products import models as products
#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.vat.models import TradeTypes
#~ products = models.get_app('products')
#~ ledger = resolve_app('ledger')
#~ products = resolve_app('products')
#~ contacts = resolve_app('contacts')
#~ from lino.modlib.contacts import models as contacts
#~ from lino.utils.choicelists import ChoiceList  

#~ class Channel(ChoiceList):
    #~ label = _("Channel")
#~ add = Channel.add_item
#~ add('P',_("Paper"))
#~ add('E',_("E-mail"))

class InvoiceStates(dd.Workflow):
    #~ label = _("State")
    pass
add = InvoiceStates.add_item
add('10',_("Booked"),'booked',help_text=_("Ready to sign"))
add('20',_("Signed"),'signed')
add('30',_("Sent"),'sent')
add('40',_("Paid"),'paid')



class PaymentTerm(babel.BabelNamed):
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
  

class InvoicingMode(mixins.PrintableType,babel.BabelNamed):
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
        #~ return unicode(babel.babelattr(self,'name'))
        
#~ add_babel_field(InvoicingMode,'name')
        
        
class InvoicingModes(dd.Table):
    model = InvoicingMode
    
    
    
class ShippingMode(babel.BabelNamed):
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
        #~ return u"SalesRule %d" % (self.id)
        
#~ def get_sales_rule(doc):
    #~ for r in SalesRule.objects.all().order_by("id"):
        #~ if r.journal is None or r.journal == doc.journal:
            #~ return r
            

class Customer(dd.Model):
    """
    Mixin meant to be applied to contacts.Person and contacts.Company
    """
    class Meta:
        abstract = True

    payment_term = models.ForeignKey(PaymentTerm,
        blank=True,null=True,help_text="""\
The default payment term of sales invoices for this customer.""")
    vat_regime = vat.VatRegimes.field(blank=True,help_text="""\
The default `VAT regime` of sales invoices for this customer.""")
    item_vat = models.BooleanField(default=False,help_text="""\
The default item_vat settings of sales invoices for this customer.""")


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
      mixins.ProjectRelated,
      #~ journals.Sendable,
      #~ journals.Journaled,
      #~ contacts.ContactDocument,
      mixins.TypedPrintable):
    """Common base class for :class:`Order` and :class:`Invoice`.
    
    #~ Subclasses must either add themselves a date field (as does Order) 
    #~ or inherit it from Transaction (as does Invoice)
    """
    class Meta:
        abstract = True
        
    #~ item_class = NotImplementedError
        
    #~ customer = models.ForeignKey("sales.Customer",
        #~ blank=True,null=True,
        #~ related_name="%(app_label)s_%(class)s_by_contact",
        #~ related_name="%(app_label)s_%(class)s_related",
        #~ )
    language = babel.LanguageField(default=babel.DEFAULT_LANGUAGE)
    
    #~ customer = models.ForeignKey(Customer,
        #~ related_name="customer_%(class)s")
    #~ ship_to = models.ForeignKey(Customer,
        #~ blank=True,null=True,
        #~ related_name="shipTo_%(class)s")
    your_ref = models.CharField(max_length=200,blank=True)
    imode = models.ForeignKey(InvoicingMode,blank=True)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    sales_remark = models.CharField("Remark for sales",
      max_length=200,blank=True)
    subject = models.CharField("Subject line",max_length=200,blank=True)
    #~ vat_exempt = models.BooleanField(default=False)
    #~ item_vat = models.BooleanField(default=False)
    #~ total_excl = dd.PriceField(blank=True,null=True)
    #~ total_vat = dd.PriceField(blank=True,null=True)
    intro = models.TextField("Introductive Text",blank=True)
    #~ user = models.ForeignKey(settings.LINO.user_model,blank=True,null=True)
    #status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    discount = models.IntegerField(_("Discount"),blank=True,null=True)
        
    #~ @dd.chooser()
    #~ def partner_choices(self):
        #~ return Customer.objects.order_by('name')
        
    def add_item(self,product=None,qty=None,**kw):
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
        kw['document'] = self
        return self.items.model(**kw)
        #~ cannot use create here because that would try to save() the item
        #~ return self.items.create(**kw)
    
    #~ @dd.virtualfield(dd.PriceField(_("Total incl. VAT")))
    #~ def total_incl(self,ar=None):
        #~ if self.total_excl is None:
            #~ return None
        #~ return self.total_excl + self.total_vat
    
    def update_totals(self):
        logger.info("20121202 sales.update_totals()")
        if self.pk is None:
            return
        total_excl = 0
        total_vat = 0
        for i in self.items.all():
            if i.total_excl is not None:
                total_excl += i.total_excl
            if i.total_vat is not None:
                total_vat += i.total_vat
            #~ if not i.product.vatExempt:
                #~ total_vat += i.total_excl() * 0.18
        self.total_excl = total_excl
        self.total_vat = total_vat
        #~ if self.journal == "ORD":
            #~ print "  done before_save:", self
        

            
    def full_clean(self,*args,**kw):
        if self.imode_id is None:
            self.imode_id = 1 # self.partner
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
        self.update_totals()
      
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



class Order(SalesDocument):
    """
    An Order is when a :class:`Customer` asks us to "deliver" a 
    given set of "products".
    """
    
    #~ date = models.DateField(help_text="""The official date of this document.""")
    
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
    
    cycle = models.CharField(max_length=1, 
            choices=CYCLE_CHOICES)
    start_date = models.DateField(blank=True,null=True,
      help_text="""Beginning of payable period. 
      Set to blank if no bill should be generated""")
    covered_until = models.DateField(blank=True,null=True)
    
    #~ objects = OrderManager()
    
    #~ def get_last_invoice(self):
        #~ invoices = self.invoice_set.order_by('date')
        #~ cnt = invoices.count()
        #~ if cnt == 0:
            #~ return None
        #~ return invoices[cnt-1]
    
        
    def skip_date(self,date):
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
                self.cycle,self))
        return datetime.date(date.year,date.month,date.day)
        
    #~ def before_save(self):
        #~ SalesDocument.before_save(self)
        #~ if self.start_date is None:
            #~ self.start_date = self.date
            
    def full_clean(self,*args,**kw):
        if self.start_date is None:
            self.start_date = self.date
        super(Order,self).full_clean(*args,**kw)
            
    def make_invoice(self,make_until=None,simulate=False,today=None):

        if self.start_date is None:
            return
        if today is None:
            today = datetime.date.today()
            
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
            return # no invoice needed today
            
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
        cover_text = "Period %s to %s" % (cover_from,cover_until)
        #print cover_text
        items = []
        for item in self.items.all():
            d = {}
            for fn in ('product','title','description',
                       'unit_price','qty'):
                d[fn] = getattr(item,fn)
            d['qty'] *= qty
            #d['total'] *= qty
            items.append(d)
        if simulate:
            return True
        #jnl = journals.get_journal(self.imode.journal)
        #~ invoice = self.imode.journal.create_document(
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
            #i = DocItem(document=invoice,**d)
            #i.save()
        invoice.full_clean()
        invoice.save() # save again because totals have been updated
        self.covered_until = cover_until
        self.save()
        return invoice
            
        

class Orders(SalesDocuments):
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
    #~ master_key = 'journal' # see django issue 10808
    #~ column_names = "number:4 date partner:20 imode " \
                  #~ "sales_remark:20 subject:20 total_incl " \
                  #~ "cycle start_date covered_until"
    

class PendingOrdersParams(forms.Form):
    make_until = forms.DateField(label="Make invoices until",
      initial=datetime.date.today()+ONE_DAY,required=False)

class PendingOrders(Orders):
    param_form = PendingOrdersParams
    
    @classmethod
    def get_queryset(self,master_instance,make_until=None):
        assert master_instance is None
        return Order.objects.pending(make_until=make_until)






class Invoice(SalesDocument,ledger.Voucher):
  
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
  
    #~ # implements Booked:
    #~ value_date = models.DateField(auto_now=True)
    #~ ledger_remark = models.CharField("Remark for ledger",
      #~ max_length=200,blank=True)
    #~ booked = models.BooleanField(default=False)
    
    #~ item_class = InvoiceItem
    
    due_date = models.DateField(_("Date of payment"),blank=True,null=True)
    order = models.ForeignKey('sales.Order',blank=True,null=True)
    
    state = InvoiceStates.field(blank=True)
    
    workflow_state_field = 'state'
    
    def full_clean(self,*args,**kw):
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.date)
        #SalesDocument.before_save(self)
        #ledger.LedgerDocumentMixin.before_save(self)
        super(Invoice,self).full_clean(*args,**kw)

    #~ def items(self,ar):
        #~ return ar.spawn(ItemsByInvoice,master_instance=self)
        

    #~ def get_wanted_movements(self):
        #~ yield self.create_movement(
          #~ settings.LINO.get_base_account(self),
          #~ self.total_excl)
        #~ if self.total_vat:
            #~ yield self.create_movement(
              #~ settings.LINO.get_vat_account(self),
              #~ self.total_vat)
        #~ yield self.create_movement(
          #~ settings.LINO.site_config.customers_account,
          #~ self.total_excl+self.total_vat)


class ProductDocItem(vat.VatItemBase):
    product = models.ForeignKey('products.Product',blank=True,null=True)
    title = models.CharField(max_length=200,blank=True)
    description = dd.RichTextField(_("Description"),blank=True,null=True)
    discount = models.IntegerField(_("Discount"),default=0)
    
    def get_base_account(self,tt):
        return settings.LINO.get_product_base_account(tt,self.product)
        
    def get_vat_class(self,tt):
        name = settings.LINO.get_product_vat_class(tt,self.product)
        return vat.VatClasses.get_by_name(name)
        
    def full_clean(self,*args,**kw):
        if self.product:
            if not self.title:
                self.title = self.product.name
            if not self.description:
                self.description = self.product.description
            if self.unit_price is None:
                if self.product.price is not None:
                    self.unit_price = self.product.price * (100 - self.discount) / 100
        super(ProductDocItem,self).full_clean(*args,**kw)


class OrderItem(ProductDocItem):
    document = models.ForeignKey(Order,related_name='items') 

class InvoiceItem(ProductDocItem):
    document = models.ForeignKey(Invoice,related_name='items') 


class InvoiceDetail(dd.FormLayout):
    main = "general ledger"
    
    totals = dd.Panel("""
    discount
    total_excl
    total_vat
    total_incl
    state
    # workflow_buttons
    """,label=_("Totals"))
    
    invoice_header = dd.Panel("""
    id date partner language
    order your_ref sales_remark subject 
    imode due_date:20 shipping_mode payment_term  vat_regime item_vat
    user project 
    """,label=_("Header"))
    
    general = dd.Panel("""
    invoice_header:60 totals:20
    ItemsByInvoice
    """,label=_("General"))
    
    ledger = dd.Panel("""
    journal year number narration
    ledger.MovementsByVoucher
    """,label=_("Ledger"))
    
class Invoices(SalesDocuments):
    #~ parameters = dict(pyear=journals.YearRef())
    parameters = dict(
        year=ledger.FiscalYears.field(blank=True),
        journal=ledger.JournalRef(blank=True))
    model = Invoice
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
    
    
    
class InvoicesByJournal(Invoices):
    order_by = ["number"]
    master_key = 'journal' # see django issue 10808
    #master = journals.Journal
    column_names = "number date due_date " \
                  "partner " \
                  "total_incl order subject:10 sales_remark:10 " \
                  "total_excl total_vat user *"
                  #~ "ledger_remark:10 " \

if settings.LINO.project_model:
  
    class InvoicesByProject(Invoices):
        order_by = ['-date']
        master_key = 'project' 
    
class SignAction(actions.Action):
    label = "Sign"
    def run(self,obj,ar):
        ar.confirm(
            "Going to sign %d documents as user %s. Are you sure?" % (
            len(ar.selected_rows),
            ar.get_user()))
        for row in ar.selected_rows:
            row.instance.user = ar.get_user()
            row.instance.save()
        return ar.ui.success_response(refresh=True)

class DocumentsToSign(Invoices):
    use_as_default_table = False
    filter = dict(user__isnull=True)
    #~ can_add = perms.never
    column_names = "number:4 order date " \
                  "partner:10 imode " \
                  "subject:10 total_incl total_excl total_vat "
    #~ actions = Invoices.actions + [ SignAction() ]
    
    #~ def get_row_actions(self,renderer):
        #~ l = super(Invoices,self).get_row_actions(renderer)
        
        #~ def sign(renderer):
            #~ for row in renderer.selected_rows():
                #~ row.instance.user = renderer.request.user
                #~ row.instance.save()
            #~ renderer.must_refresh()
            
        #~ l.append( ('sign', sign) )
        #~ return l 


  
class InvoicesByOrder(SalesDocuments):
    model = Invoice
    master_key = "order"
    order_by = ["number"]
    column_names = "number date your_ref total_excl *"

    
#~ class ItemsByDocumentListLayout(layouts.ListLayout):
    #~ title_box = """
    #~ product
    #~ title
    #~ """
    #~ main = "pos:3 title_box description:20x1 discount unit_price qty total"

class ItemsByDocument(dd.Table):
    column_names = "seqno:3 product title description:20x1 discount unit_price qty total_incl *"
    master_key = 'document'
    order_by = ["seqno"]
    

class ItemsByOrder(ItemsByDocument):
    model = OrderItem

class ItemsByInvoice(ItemsByDocument):
    model = InvoiceItem
    

class OrderItemsByProduct(ItemsByOrder):
    master_key = 'product'

class InvoiceItemsByProduct(ItemsByInvoice):
    master_key = 'product'

    


#~ class DocumentsByPartnerDetail(layouts.PageLayout):
    #~ label = "Sales"
    #~ main = """
            #~ company person
            #~ DocumentsByPartner
            #~ """
#~ contacts.Partners.register_page_layout(DocumentsByPartnerDetail)
            

#~ class SalesByCustomer(SalesDocuments):
class OrdersByPartner(Orders):
    #~ model = 'sales.Order'
    master_key = 'partner'
    order_by = ["start_date"]
    column_names = "start_date total_incl total_excl total_vat *"
    

class InvoicesByPartner(Invoices):
    #~ model = 'sales.Invoice'
    order_by = ["date"]
    master_key = 'partner'
    column_names = "date total_incl total_excl total_vat *"
    

#~ class SalesByPerson(SalesDocuments):
    #~ column_names = "journal:4 number:4 date:8 " \
                   #~ "total_incl total_excl total_vat *"
    #~ order_by = ["date"]
    #~ master_key = 'person'

        


#~ journals.register_doctype(Order,OrdersByJournal)
#~ ledger.register_voucher_type(Invoice,InvoicesByJournal)
ledger.VoucherTypes.add_item(Invoice,InvoicesByJournal)


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
        


def customize_contacts():

    dd.inject_field('contacts.Partner',
        'is_customer',
        mti.EnableChild('sales.Customer',verbose_name=_("is Customer")),
        """Whether this Partner is also a Customer."""
        )


MODULE_LABEL = _("Sales")

def site_setup(site):
    if site.is_installed('products'):
        site.modules.products.Products.add_detail_tab("sales",
            "sales.OrderItemsByProduct\nsales.InvoiceItemsByProduct",
            label=MODULE_LABEL)
    #~ if site.is_installed('tickets'):
        #~ site.modules.tickets.Projects.add_detail_tab("sales","sales.InvoicesByProject")
    #~ site.modules.lino.SiteConfigs.add_detail_tab("sales","""
    #~ #sales_base_account
    #~ #sales_vat_account
    #~ customers_account
    #~ """,label=_("Sales"))


def setup_main_menu(site,ui,profile,m): 
    #~ m = m.add_menu("sales",MODULE_LABEL)
    m = m.add_menu(vat.TradeTypes.sales.name,vat.TradeTypes.sales.text)
    m.add_action(Orders)
    
    for jnl in ledger.Journal.objects.all():
        if jnl.trade_type == vat.TradeTypes.sales:
            m.add_action(jnl.voucher_type.table_class,
                label=unicode(jnl),
                params=dict(master_instance=jnl))
    
    #~ m.add_action(Invoices)
    #~ m.add_action(DocumentsToSign)
    #~ m.add_action(PendingOrders)

def setup_my_menu(site,ui,profile,m): 
    pass
  
def setup_config_menu(site,ui,profile,m): 
    m = m.add_menu("sales",MODULE_LABEL)
    m.add_action(InvoicingModes)
    m.add_action(ShippingModes)
    m.add_action(PaymentTerms)
    
def setup_explorer_menu(site,ui,profile,m):
    pass
  
customize_contacts()
#~ customize_siteconfig()

  