## Copyright 2008-2009 Luc Saffre
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
>>> luc = contacts.Contact(firstName="Luc",lastName="Saffre")
>>> luc.save()
>>> luc
<Contact: Luc Saffre>

>>> c = Customer.from_parent(luc)
>>> c.save()
>>> c
<Customer: Luc Saffre>

"""

import datetime
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

# __app_label__ = "sales"


from django.db import models
from django.contrib.auth import models as auth

from lino.utils.ticket7623 import child_from_parent

from lino.modlib import fields

        
from django import forms

from lino import reports
from lino import layouts
from lino import actions
from lino.utils import perms

#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.journals import models as journals
#~ from lino.modlib.ledger import models as ledger
#~ from lino.modlib.products import models as products

contacts = reports.get_app('contacts')
journals = reports.get_app('journals')
ledger = reports.get_app('ledger')
products = reports.get_app('products')



class PaymentTerm(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=200)
    days = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    #proforma = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
        
    def get_due_date(self,date1):
        assert isinstance(date1,datetime.date), \
          "%s is not a date" % date1
        #~ print type(date1),type(relativedelta(months=self.months,days=self.days))
        d = date1 + relativedelta(months=self.months,days=self.days)
        return d


class PaymentTerms(reports.Report):
    model = PaymentTerm
    order_by = "id"
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
  


class InvoicingMode(models.Model):
    CHANNEL_CHOICES = (
        ('P', 'Regular Mail'),
        ('E', 'E-Mail'),
    )
    id = models.CharField(max_length=3, primary_key=True)
    journal = journals.JournalRef()
    #journal = models.ForeignKey(journals.Journal)
    name = models.CharField(max_length=200)
    price = fields.PriceField(blank=True,null=True)
    channel = models.CharField(max_length=1, 
                choices=CHANNEL_CHOICES,help_text="""
    Method used to send the invoice. 
                """)
    advance_days = models.IntegerField(default=0,
                   help_text="""
    Invoices must be sent out X days in advance so that the customer
    has a chance to pay them in time. 
    """)
    
    def __unicode__(self):
        return self.name
        
class InvoicingModes(reports.Report):
    model = InvoicingMode
    order_by = "id"
    can_view = perms.is_staff
    
    
    
class ShippingMode(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    price = fields.PriceField(blank=True,null=True)
    
    def __unicode__(self):
        return self.name
        
class ShippingModes(reports.Report):
    model = ShippingMode
    order_by = "id"
    can_view = perms.is_staff
    #~ def can_view(self,request):
      #~ return request.user.is_staff



class SalesRule(models.Model):
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
            
            
class Partner(contacts.Partner):
    class Meta:
        app_label = 'contacts'
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    vat_exempt = models.BooleanField(default=False)
    item_vat = models.BooleanField(default=False)
    

class PartnerPageLayout(layouts.PageLayout):
    main = """
           company person
           payment_term 
           vat_exempt item_vat
           """
    
class Partners(reports.Report):
    page_layouts = (PartnerPageLayout,)
    columnNames = "name payment_term vat_exempt item_vat company person"
    can_delete = True
    model = Partner
    order_by = "name"
    #can_view = perms.is_authenticated


class SalesDocument(journals.AbstractDocument):
    
    creation_date = fields.MyDateField() #auto_now_add=True)
    customer = models.ForeignKey('contacts.Partner',
        related_name="customer_%(class)s")
    ship_to = models.ForeignKey('contacts.Partner',
        blank=True,null=True,
        related_name="shipTo_%(class)s")
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
    user = models.ForeignKey(auth.User,blank=True,null=True)
    #status = models.CharField(max_length=1, choices=STATUS_CHOICES)
        
    def can_send(self):
        "only signed documents can be sent"
        return self.user is not None
        
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
        return self.docitem_set.create(**kw)
        
    def total_incl(self):
        return self.total_excl + self.total_vat
    total_incl.return_type = fields.PriceField()
    
    def update_total(self):
        total_excl = 0
        total_vat = 0
        for i in self.docitem_set.all():
            if i.total is not None:
                total_excl += i.total
            #~ if not i.product.vatExempt:
                #~ total_vat += i.total_excl() * 0.18
        self.total_excl = total_excl
        self.total_vat = total_vat
        #~ if self.journal == "ORD":
            #~ print "  done before_save:", self
        

    def before_save(self):
        #~ if self.journal == "ORD":
            #~ print "before_save:", self
        journals.AbstractDocument.before_save(self)
        r = get_sales_rule(self)
        if r is None:
            raise journals.DocumentError("No sales rule for %s",self)
        if self.imode is None:
            self.imode = r.imode
        if self.shipping_mode is None:
            self.shipping_mode = r.shipping_mode
        if self.shipping_mode is None:
            self.shipping_mode = r.shipping_mode
        self.update_total()
      
        
class OrderManager(models.Manager):
  
    def pending(self,make_until=None):
        l = []
        for o in self.all():
            if o.make_invoice(make_until=make_until,simulate=True):
                l.append(o)
        return l
        


class Order(SalesDocument):
  
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
        
    def before_save(self):
        SalesDocument.before_save(self)
        if self.start_date is None:
            self.start_date = self.creation_date
            
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
            
        expect_payment = self.payment_term.get_due_date(make_until)
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
        for item in self.docitem_set.all():
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
            ship_to=self.ship_to,
            imode=self.imode,
            payment_term=self.payment_term,
            shipping_mode=self.shipping_mode,
            subject=cover_text,
            your_ref=unicode(self),
            )
            
        #invoice.save()
        for d in items:
            invoice.add_item(**d).save()
            #i = DocItem(document=invoice,**d)
            #i.save()
        invoice.save() # save again because totals have been updated
        self.covered_until = cover_until
        self.save()
        return invoice
            
        
    
class Invoice(ledger.LedgerDocument,SalesDocument):
    due_date = fields.MyDateField("Payable until",blank=True,null=True)
    order = models.ForeignKey(Order,blank=True,null=True)
    
    def before_save(self):
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.creation_date)
        #SalesDocument.before_save(self)
        #ledger.LedgerDocumentMixin.before_save(self)
        super(Invoice,self).before_save()


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
    document = models.ForeignKey(SalesDocument) 
    pos = models.IntegerField("Position")
    
    product = models.ForeignKey(products.Product,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True)
    description = models.TextField(blank=True,null=True)
    
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
        
    def save(self, *args, **kwargs):
        self.before_save()
        super(DocItem,self).save(*args,**kwargs)
                    
    def before_save(self):
        #print "before_save()", self
        if self.pos is None:
            self.pos = self.document.docitem_set.count() + 1
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
        self.document.update_total()
    before_save.alters_data = True

    def __unicode__(self):
        return "%s object" % self.__class__.__name__
        #~ if self.document is None:
            #~ return models.Model.__unicode__(self)
        #~ return u"DocItem %s.%d" % (self.document,self.pos)



    
class DocumentPageLayout(layouts.PageLayout):
    box1 = """
      journal number your_ref 
      creation_date 
      customer 
      ship_to
      """
    box2 = """
      imode
      shipping_mode 
      payment_term
      user sent_time
      """
    box3 = """
      subject 
      sales_remark:80
      intro:80x5
      """
    box4 = """
      vat_exempt 
      item_vat
      total_excl
      total_vat
      total_incl
      """
    box5 = ''
    
    main = """
      box1 box2 box4
      box3 box5
      sales_ItemsByDocument:100x15
      """
      
        
class OrderPageLayout(DocumentPageLayout):
    box5 = """
      cycle:20
      start_date
      covered_until
      """
        
        
class InvoicePageLayout(DocumentPageLayout):
    box5 = """
      order
      """

class EmittedInvoicesPageLayout(OrderPageLayout):
    label = "Emitted invoices"
    main = """
    journal number:4 creation_date customer:20 start_date
    sales_InvoicesByOrder
    """


class SalesDocuments(reports.Report):
    model = SalesDocument
    page_layouts = (DocumentPageLayout,)
    #actions = reports.Report.actions + [ PrintAction ]
    
    #~ def inlines(self):
        #~ return dict(items=ItemsByDocument())


class Orders(SalesDocuments):
    model = Order
    order_by = "number"
    page_layouts = (OrderPageLayout,EmittedInvoicesPageLayout,)
    can_view = perms.is_authenticated
    
    #~ def inlines(self):
        #~ d = super(Orders,self).inlines()
        #~ d.update(emitted_invoices=InvoicesByOrder())
        #~ return d
    
class OrdersByJournal(Orders):
    order_by = "number"
    #master = journals.Journal
    fk_name = 'journal' # see django issue 10808
    columnNames = "number:4 creation_date customer:20 imode " \
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
    order_by = "id"
    page_layouts = (InvoicePageLayout,)
    can_view = perms.is_staff
    
class InvoicesByJournal(Invoices):
    order_by = "number"
    fk_name = 'journal' # see django issue 10808
    #master = journals.Journal
    columnNames = "number:4 creation_date due_date " \
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
    filter = dict(user__exact=None)
    can_add = perms.never
    columnNames = "number:4 order creation_date " \
                  "customer:10 imode " \
                  "subject:10 total_incl total_excl total_vat "
    actions = Invoices.actions + [ SignAction() ]
    
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
    #master = Order
    fk_name = "order"
    order_by = "number"
    columnNames = "number creation_date your_ref total_excl total_vat shipping_mode payment_term due_date subject sales_remark vat_exempt item_vat "

    
#~ class ItemsByDocumentRowLayout(layouts.RowLayout):
    #~ title_box = """
    #~ product
    #~ title
    #~ """
    #~ main = "pos:3 title_box description:20x1 discount unit_price qty total"

class ItemsByDocument(reports.Report):
    columnNames = "pos:3 product title description:20x1 discount unit_price qty total"
    #row_layout_class = ItemsByDocumentRowLayout
    model = DocItem
    #master = SalesDocument
    fk_name = 'document'
    order_by = "pos"
    



#~ class DocumentsByPartnerDetail(layouts.PageLayout):
    #~ label = "Sales"
    #~ main = """
            #~ company person
            #~ DocumentsByPartner
            #~ """
#~ contacts.Partners.register_page_layout(DocumentsByPartnerDetail)
            

class DocumentsByPartner(SalesDocuments):
    columnNames = "journal:4 number:4 creation_date:8 " \
                  "total_incl total_excl total_vat"
    #master = 'contacts.Partner'
    fk_name = 'customer'
    order_by = "creation_date"

    def get_title(self,renderer):
        return "Documents by customer"
        #return unicode(renderer.master_instance) + " : documents by customer"
        


#~ class Customers(contacts.Contacts):
    #~ model = Customer
    #~ page_layouts = (PartnerPageLayout,DocumentsByCustomerTabLayout)
    
        
journals.register_doctype(Order,OrdersByJournal)
journals.register_doctype(Invoice,InvoicesByJournal)
