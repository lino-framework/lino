# -*- coding: UTF-8 -*-
## Copyright 2008-2011 Luc Saffre
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
#~ from django.contrib.auth import models as auth
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from lino import fields
        
from lino import reports
from lino import actions
from lino import mixins
from lino.utils import mti
from lino.utils import perms
from lino.utils import babel 
#~ from lino.utils.babel import add_babel_field, babelattr

#~ from lino.tools import resolve_app

#~ journals = resolve_app('journals')
#~ journals = models.get_app('journals')
#~ auth = resolve_app('auth')
from lino.modlib.users import models as auth
#~ ledger = models.get_app('ledger')
from lino.modlib.ledger import models as ledger
from lino.modlib.journals import models as journals
from lino.modlib.products import models as products
from lino.modlib.contacts import models as contacts
#~ products = models.get_app('products')
#~ ledger = resolve_app('ledger')
#~ products = resolve_app('products')
#~ contacts = resolve_app('contacts')
#~ from lino.modlib.contacts import models as contacts


class PaymentTerm(babel.BabelNamed):
    """Represents a convention on how an Invoice should be paid. 
    """
    
    class Meta:
        verbose_name = _("Payment Term")
        verbose_name_plural = _("Payment Terms")
        
    id = models.CharField(max_length=10,primary_key=True)
    days = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    #proforma = models.BooleanField(default=False)
    
    def get_due_date(self,date1):
        assert isinstance(date1,datetime.date), \
          "%s is not a date" % date1
        #~ print type(date1),type(relativedelta(months=self.months,days=self.days))
        d = date1 + relativedelta(months=self.months,days=self.days)
        return d


class PaymentTerms(reports.Report):
    model = PaymentTerm
    order_by = ["id"]
    can_view = perms.is_staff
    #~ def can_view(self,request):
      #~ return request.user.is_staff





#~ class Customer(contacts.Contact):
    #~ paymentTerm = models.ForeignKey("PaymentTerm",blank=True,null=True)
    #~ vatExempt = models.BooleanField(default=False)
    #~ itemVat = models.BooleanField(default=False)
    
    #~ @classmethod
    #~ def from_parent(cls,*args,**kw):
        #~ return child_from_parent(cls,*args,**kw)
  
from lino.utils.choicelists import ChoiceList  
class Channel(ChoiceList):
    label = _("Channel")
add = Channel.add_item
add('P',en=u"Paper",de=u"Papier", fr=u"Papier",et="Paber")
add('E',en=u"E-mail",de=u"E-mail", fr=u"courrier électronique",et="e-mail")


class InvoicingMode(mixins.PrintableType,babel.BabelNamed):
    """Represents a method of issuing/sending invoices.
    """
    class Meta:
        verbose_name = _("Invoicing Mode")
        verbose_name_plural = _("Invoicing Modes")
    #~ CHANNEL_CHOICES = (
        #~ ('P', 'Regular Mail'),
        #~ ('E', 'E-Mail'),
    #~ )
    id = models.CharField(max_length=3, primary_key=True)
    journal = journals.JournalRef()
    #journal = models.ForeignKey(journals.Journal)
    #~ name = babel.BabelCharField(max_length=200)
    price = fields.PriceField(blank=True,null=True)
    "Additional fee charged when using this method."
    channel = Channel.field(help_text="""
        Method used to send the invoice.""")
    #~ channel = models.CharField(max_length=1, 
                #~ choices=CHANNEL_CHOICES,help_text="""
    #~ Method used to send the invoice. 
                #~ """)
    advance_days = models.IntegerField(default=0,
                   help_text="""
    Invoices must be sent out X days in advance so that the customer
    has a chance to pay them in time. 
    """)
    
    #~ def __unicode__(self):
        #~ return unicode(babel.babelattr(self,'name'))
        
#~ add_babel_field(InvoicingMode,'name')
        
        
class InvoicingModes(reports.Report):
    model = 'sales.InvoicingMode'
    order_by = ["id"]
    can_view = perms.is_staff
    
    
    
class ShippingMode(babel.BabelNamed):
    id = models.CharField(max_length=10, primary_key=True)
    #~ name = babel.BabelCharField(max_length=200)
    price = fields.PriceField(blank=True,null=True)
    
    #~ def __unicode__(self):
        #~ return self.name
        
class ShippingModes(reports.Report):
    """Represents a possible method of how the items described in a SalesDocument 
    are to be transferred from us to our customer.
    """
    class Meta:
        verbose_name = _("Shipping Mode")
        verbose_name_plural = _("Shipping Modes")
    model = ShippingMode
    order_by = ["id"]
    can_view = perms.is_staff
    #~ def can_view(self,request):
      #~ return request.user.is_staff



class SalesRule(models.Model):
    """Represents a group of default values for certain parameters of a SalesDocument.
    """
    class Meta:
        verbose_name = _("Sales Rule")
        verbose_name_plural = _("Sales Rules")
    #journal = models.ForeignKey(journals.Journal,blank=True,null=True)
    journal = journals.JournalRef(blank=True,null=True)
    imode = models.ForeignKey(InvoicingMode,blank=True,null=True)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    
    def __unicode__(self):
        return u"SalesRule %d" % (self.id)
        
def get_sales_rule(doc):
    for r in SalesRule.objects.all().order_by("id"):
        if r.journal is None or r.journal == doc.journal:
            return r
            

class Customer(contacts.Contact):
    """
    A Customer is a Contact that can receive sales invoices.
    """    
    class Meta:
        verbose_name =_("Customer")
        verbose_name_plural =_("Customers")
        
    #~ name = models.CharField(max_length=40)
    #~ company = models.ForeignKey('contacts.Company',blank=True,null=True)
    #~ person = models.ForeignKey('contacts.Person',blank=True,null=True)
    
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    vat_exempt = models.BooleanField(default=False)
    item_vat = models.BooleanField(default=False)
    
    #~ def __unicode__(self):
        #~ if self.name is None:
            #~ return u"Unsaved customer %s" % self.id
        #~ return self.name
        
        
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
    
    
#~ class Customers(reports.Report):
    #~ column_names = "name payment_term vat_exempt item_vat company person"
    #~ can_delete = True
    #~ model = Customer
    #~ order_by = ["name"]




class SalesDocument(
      mixins.AutoUser,
      journals.Sendable,
      journals.Journaled,
      #~ contacts.ContactDocument,
      mixins.TypedPrintable):
    """Common base class for :class:`Order` and :class:`Invoice`.
    """
    class Meta:
        abstract = True
        
    #~ item_class = NotImplementedError
        
    customer = models.ForeignKey("sales.Customer",
        #~ blank=True,null=True,
        #~ related_name="%(app_label)s_%(class)s_by_contact",
        #~ related_name="%(app_label)s_%(class)s_related",
        )
    language = fields.LanguageField(default=babel.DEFAULT_LANGUAGE)
    
    creation_date = models.DateField(blank=True,auto_now_add=True)
    #~ customer = models.ForeignKey(Customer,
        #~ related_name="customer_%(class)s")
    #~ ship_to = models.ForeignKey(Customer,
        #~ blank=True,null=True,
        #~ related_name="shipTo_%(class)s")
    your_ref = models.CharField(max_length=200,blank=True)
    imode = models.ForeignKey(InvoicingMode)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    sales_remark = models.CharField("Remark for sales",
      max_length=200,blank=True)
    subject = models.CharField("Subject line",max_length=200,blank=True)
    vat_exempt = models.BooleanField(default=False)
    item_vat = models.BooleanField(default=False)
    total_excl = fields.PriceField(default=0)
    total_vat = fields.PriceField(default=0)
    intro = models.TextField("Introductive Text",blank=True)
    #~ user = models.ForeignKey(settings.LINO.user_model,blank=True,null=True)
    #status = models.CharField(max_length=1, choices=STATUS_CHOICES)
        
    def can_send(self):
        "only signed documents can be sent"
        return self.user is not None
        
    def get_printable_type(self):
        return self.imode
        
    def disabled_fields(self,request):
        if self.must_build:
            return []
        return SALES_PRINTABLE_FIELDS
        
    #~ def save(self, *args, **kwargs):
        #~ self.before_save()
        #~ super(SalesDocument,self).save(*args,**kwargs)
                    
        
    def add_item(self,product=None,qty=None,**kw):
        if product is not None:
            if not isinstance(product,products.Product):
                product = products.Product.objects.get(pk=product)
            if qty is None:
                qty = 1
        kw['product'] = product 
        unit_price = kw.get('unit_price',None)
        if type(unit_price) == float:
            kw['unit_price'] = "%.2f" % unit_price
        kw['qty'] = qty
        #print self,kw
        kw['document'] = self
        return self.items.model(**kw)
        #~ cannot use create here because that would try to save() the item
        #~ return self.items.create(**kw)
        
    def total_incl(self,request=None):
        return self.total_excl + self.total_vat
    total_incl.return_type = fields.PriceField()
    
    def update_total(self):
        if self.pk is None:
            return
        total_excl = 0
        total_vat = 0
        for i in self.items.all():
            if i.total is not None:
                total_excl += i.total
            #~ if not i.product.vatExempt:
                #~ total_vat += i.total_excl() * 0.18
        self.total_excl = total_excl
        self.total_vat = total_vat
        #~ if self.journal == "ORD":
            #~ print "  done before_save:", self
        

            
    def full_clean(self,*args,**kw):
        #~ logger.info("SalesDocument.full_clean")
        super(SalesDocument,self).full_clean(*args,**kw)
        r = get_sales_rule(self)
        if r is None:
            raise ValidationError("No sales rule for %s",self)
            #~ raise journals.DocumentError("No sales rule for %s",self)
        if self.imode is None:
            self.imode = r.imode
        if self.shipping_mode is None:
            self.shipping_mode = r.shipping_mode
        if self.shipping_mode is None:
            self.shipping_mode = r.shipping_mode
        self.update_total()
      
SALES_PRINTABLE_FIELDS = reports.fields_list(SalesDocument,
  'customer imode payment_term '
  'creation_date your_ref subject '
  'language vat_exempt item_vat ')

class OrderManager(models.Manager):
  
    def pending(self,make_until=None):
        l = []
        for o in self.all():
            if o.make_invoice(make_until=make_until,simulate=True):
                l.append(o)
        return l
        


class Order(SalesDocument):
    """
    An Order is when a :class:`Customer` asks us to "deliver" a 
    given set of "products".
    """
    
    #~ item_class = OrderItem
  
    CYCLE_CHOICES = (
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
    )
    
    cycle = models.CharField(max_length=1, 
            choices=CYCLE_CHOICES)
    start_date = fields.MyDateField(blank=True,null=True,
      help_text="""Beginning of payable period. 
      Set to blank if no bill should be generated""")
    covered_until = fields.MyDateField(blank=True,null=True)
    
    objects = OrderManager()
    
    #~ def get_last_invoice(self):
        #~ invoices = self.invoice_set.order_by('creation_date')
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
            #~ self.start_date = self.creation_date
            
    def full_clean(self,*args,**kw):
        if self.start_date is None:
            self.start_date = self.creation_date
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
        invoice = self.imode.journal.create_document(
            creation_date=today,
            order=self,
            customer=self.customer,
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
            
        
    
class Invoice(ledger.Booked,SalesDocument):
  
    #~ # implements Booked:
    #~ value_date = models.DateField(auto_now=True)
    #~ ledger_remark = models.CharField("Remark for ledger",
      #~ max_length=200,blank=True)
    #~ booked = models.BooleanField(default=False)
    
    #~ item_class = InvoiceItem
    
    due_date = models.DateField("Payable until",blank=True,null=True)
    order = models.ForeignKey('sales.Order',blank=True,null=True)
    
    def full_clean(self,*args,**kw):
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.creation_date)
        #SalesDocument.before_save(self)
        #ledger.LedgerDocumentMixin.before_save(self)
        super(Invoice,self).full_clean(*args,**kw)


    def collect_bookings(self):
        jnl = self.get_journal()
        yield self.create_booking(
          account=ledger.get_account('sales_base'),
          debit=self.total_excl)
        yield self.create_booking(
          account=ledger.get_account('sales_vat'),
          debit=self.total_vat)
        yield self.create_booking(
          account=ledger.Account.objects.get(pk=jnl.account_id),
          credit=self.total_excl+self.total_vat)


class DocItem(models.Model):
    "Base class for InvoiceItem and OrderItem"
    class Meta:
        abstract = True
        unique_together  = ('document','pos')
    
    pos = models.IntegerField("Position")
    
    product = models.ForeignKey(products.Product,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True)
    description = fields.RichTextField(_("Description"),blank=True,null=True)
    
    discount = models.IntegerField("Discount %",default=0)
    unit_price = fields.PriceField(blank=True,null=True) 
    qty = fields.QuantityField(blank=True,null=True)
    total = fields.PriceField(blank=True,null=True)
    
    #~ def total_excl(self):
        #~ if self.unitPrice is not None:
            #~ qty = self.qty or 1
            #~ return self.unitPrice * qty
        #~ elif self.total is not None:
            #~ return self.total
        #~ return 0
        
    #~ def save(self, *args, **kwargs):
        #~ self.before_save()
        #~ super(DocItem,self).save(*args,**kwargs)
                    
    def full_clean(self,*args,**kw):
        #print "before_save()", self
        if self.document.pk is not None:
            if self.pos is None:
                self.pos = self.document.items.count() + 1
            if self.product:
                if not self.title:
                    self.title = self.product.name
                if not self.description:
                    self.description = self.product.description
                if self.unit_price is None:
                    if self.product.price is not None:
                        self.unit_price = self.product.price * (100 - self.discount) / 100
            if self.unit_price is not None and self.qty is not None:
                self.total = self.unit_price * self.qty
            #self.document.save() # update total in document
            #~ self.document.update_total()
        super(DocItem,self).full_clean(*args,**kw)
    #~ before_save.alters_data = True

    def __unicode__(self):
        return "%s object" % self.__class__.__name__
        #~ if self.document is None:
            #~ return models.Model.__unicode__(self)
        #~ return u"DocItem %s.%d" % (self.document,self.pos)


class OrderItem(DocItem):
    #~ class Meta:
        #~ abstract = True
    document = models.ForeignKey('sales.Order',related_name='items') 

class InvoiceItem(DocItem):
    #~ class Meta:
        #~ abstract = True
    document = models.ForeignKey('sales.Invoice',related_name='items') 

    

class SalesDocuments(reports.Report):
    pass
    #~ model = SalesDocument
    #~ page_layouts = (DocumentPageLayout,)
    #actions = reports.Report.actions + [ PrintAction ]
    
    #~ def inlines(self):
        #~ return dict(items=ItemsByDocument())


class Orders(SalesDocuments):
    model = Order
    order_by = ["number"]
    can_view = perms.is_authenticated
    
    #~ def inlines(self):
        #~ d = super(Orders,self).inlines()
        #~ d.update(emitted_invoices=InvoicesByOrder())
        #~ return d
    
class OrdersByJournal(Orders):
    order_by = ["number"]
    #master = journals.Journal
    fk_name = 'journal' # see django issue 10808
    column_names = "number:4 creation_date customer:20 imode " \
                  "sales_remark:20 subject:20 total_incl " \
                  "cycle start_date covered_until"
    

class PendingOrdersParams(forms.Form):
    make_until = forms.DateField(label="Make invoices until",
      initial=datetime.date.today()+ONE_DAY,required=False)

class PendingOrders(Orders):
    param_form = PendingOrdersParams
    def get_queryset(self,master_instance,make_until=None):
        assert master_instance is None
        return Order.objects.pending(make_until=make_until)

    
class Invoices(SalesDocuments):
    model = Invoice
    order_by = ["id"]
    can_view = perms.is_staff
    
class InvoicesByJournal(Invoices):
    order_by = ["number"]
    fk_name = 'journal' # see django issue 10808
    #master = journals.Journal
    column_names = "number:4 creation_date due_date " \
                  "customer:10 " \
                  "total_incl order subject:10 sales_remark:10 " \
                  "ledger_remark:10 " \
                  "total_excl total_vat user "

class SignAction(actions.Action):
    label = "Sign"
    def run(self,context):
        context.confirm(
            "Going to sign %d documents as user %s. Are you sure?" % (
            len(context.selected_rows),
            context.request.user))
        for row in context.selected_rows:
            row.instance.user = context.request.user
            row.instance.save()
        context.refresh()

class DocumentsToSign(Invoices):
    use_as_default_report = False
    filter = dict(user__isnull=True)
    can_add = perms.never
    column_names = "number:4 order creation_date " \
                  "customer:10 imode " \
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
    fk_name = "order"
    order_by = ["number"]
    column_names = "number creation_date your_ref total_excl *"

    
#~ class ItemsByDocumentListLayout(layouts.ListLayout):
    #~ title_box = """
    #~ product
    #~ title
    #~ """
    #~ main = "pos:3 title_box description:20x1 discount unit_price qty total"

class ItemsByDocument(reports.Report):
    column_names = "pos:3 product title description:20x1 discount unit_price qty total"
    #list_layout_class = ItemsByDocumentListLayout
    #master = SalesDocument
    fk_name = 'document'
    order_by = ["pos"]
    

class ItemsByOrder(ItemsByDocument):
    model = 'sales.OrderItem'

class ItemsByInvoice(ItemsByDocument):
    model = 'sales.InvoiceItem'


#~ class DocumentsByPartnerDetail(layouts.PageLayout):
    #~ label = "Sales"
    #~ main = """
            #~ company person
            #~ DocumentsByPartner
            #~ """
#~ contacts.Partners.register_page_layout(DocumentsByPartnerDetail)
            

class SalesByCustomer(SalesDocuments):
    column_names = "journal:4 number:4 creation_date:8 " \
                   "total_incl total_excl total_vat *"
    order_by = ["creation_date"]
    fk_name = 'customer'
    
class OrdersByCustomer(SalesByCustomer):
    model = 'sales.Order'

class InvoicesByCustomer(SalesByCustomer):
    model = 'sales.Invoice'

#~ class SalesByPerson(SalesDocuments):
    #~ column_names = "journal:4 number:4 creation_date:8 " \
                   #~ "total_incl total_excl total_vat *"
    #~ order_by = ["creation_date"]
    #~ fk_name = 'person'

        


journals.register_doctype(Order,OrdersByJournal)
journals.register_doctype(Invoice,InvoicesByJournal)

from lino.modlib.contacts.models import Contact

reports.inject_field(Contact,
    'is_customer',
    mti.EnableChild('sales.Customer',verbose_name=_("is Customer")),
    """Whether this Contactis also a Customer."""
    )



#~ reports.inject_field(
    #~ Contact,'payment_term',
    #~ models.ForeignKey(PaymentTerm,
        #~ blank=True,null=True,
        #~ verbose_name=_("payment term")),
    #~ """The default PaymentTerm for sales invoices to this Contact.
    #~ """)
#~ reports.inject_field(
    #~ Contact, 'vat_exempt',
    #~ models.BooleanField(default=False,
        #~ verbose_name=_("VAT exempt")),
    #~ """The default value for vat_exempt for sales invoices to this Contact.
    #~ """)
#~ reports.inject_field(
    #~ Contact, 'item_vat',
    #~ models.BooleanField(default=False,
        #~ verbose_name=_("item_vat")),
    #~ """The default value for item_vat for sales invoices to this Contact.
    #~ """)


def setup_main_menu(site,ui,user,m): 
    m.add_action('sales.Orders')
    m.add_action('sales.Invoices')
    m.add_action('sales.DocumentsToSign')
    m.add_action('sales.PendingOrders')

def setup_my_menu(site,ui,user,m): 
    pass
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("cal",_("~Sales"))
    m.add_action('sales.InvoicingModes')
    m.add_action('sales.ShippingModes')
    m.add_action('sales.PaymentTerms')
    
def setup_explorer_menu(site,ui,user,m):
    pass
  