## Copyright 2008-2009 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import datetime
import dateutil

from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
#from lino.django.tom import models
from django.utils.safestring import mark_safe

from lino.django.utils.validatingmodel import TomModel, ModelValidationError
from lino.django.utils import render

#from lino.django.utils.journals import Journal
#from lino.django.journals import models as journals
from lino.django.plugins import fields, journals

from django.contrib.auth.models import User

def linkto(href,text=None):
    if text is None:
        text=href
    return '<a href="%s">%s</a>' % (href,text)
        
  
class Contact(TomModel):
    """
    
Company and/or Person contact data, linked with client account and
choosable for invoicing regarding particular order (if wanting other
invoice to than client default contact). If CompanyName field is
filled, contact record will be presented as CompanyName in contacts
listing - otherwise as Person First- and Lastname.
    
# Examples:
>>> p=Contact.objects.create(lastName="Saffre",firstName="Luc")
>>> unicode(p)
u'Luc Saffre'
>>> p=Contact.objects.create(lastName="Saffre", firstName="Luc", title="Mr.")
>>> unicode(p)
u'Luc Saffre'
>>> p=Contact.objects.create(lastName="Saffre", title="Mr.")
>>> unicode(p)
u'Mr. Saffre'
>>> p=Contact.objects.create(firstName="Luc")
>>> unicode(p)
u'Luc'
>>> p=Contact.objects.create(lastName="Saffre",firstName="Luc", companyName="Example & Co")
>>> unicode(p)
u'Example & Co (Luc Saffre)'
    
    """
    #name = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200,blank=True)
    lastName = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=200,blank=True)
    
    companyName = models.CharField(max_length=200,blank=True)
    nationalId = models.CharField(max_length=200,blank=True)
    vatId = models.CharField(max_length=200,blank=True)
    
    addr1 = models.CharField(max_length=200,blank=True)
    addr2 = models.CharField(max_length=200,blank=True)
    country = models.ForeignKey("utils.Country",blank=True,null=True)
    #city = models.ForeignKey("City",blank=True,null=True)
    city = models.CharField(max_length=200,blank=True)
    zipCode = models.CharField(max_length=10,blank=True)
    region = models.CharField(max_length=200,blank=True)
    
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    phone = models.CharField(max_length=200,blank=True)
    gsm = models.CharField(max_length=200,blank=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    vatExempt = models.BooleanField(default=False)
    itemVat = models.BooleanField(default=False)
    
    language = models.ForeignKey("utils.Language",blank=True,null=True)
    paymentTerm = models.ForeignKey("PaymentTerm",blank=True,null=True)
    
    remarks = models.TextField(blank=True)
    
    ordering=("companyName","lastName","firstName")
    
    def __unicode__(self):
        if self.title and not self.firstName:
            l=filter(lambda x:x,[self.title,self.lastName])
        else:
            l=filter(lambda x:x,[self.firstName,self.lastName])
            
        s=" ".join(l)
            
        if self.companyName:
            if len(s) > 0:
                return self.companyName+" ("+s+")"
            else:
                return self.companyName
        else:
            return s
            
    def as_address(self,linesep="\n<br/>"):
        l=filter(lambda x:x,[self.title,self.firstName,self.lastName])
        s=" ".join(l)
        if self.companyName:
            s=self.companyName+linesep+s
        if self.addr1:
          s += linesep+self.addr1
        if self.addr2:
          s += linesep+self.addr2
        if self.city:
          s += linesep+self.city
        if self.zipCode:
          s += linesep+self.zipCode
          if self.region:
            s += " " + self.region
        elif self.region:
            s += linesep+ self.region
        if self.id == 1:
            foreigner=False
        else:
            foreigner=(self.country != Contact.objects.get(id=1).country)
        if foreigner: # (if self.country != sender's country)
            s += linesep + unicode(self.country)
        return s
    as_address.allow_tags=True


class InvoicingMode(models.Model):
    CHANNEL_CHOICES = (
        ('P', 'Regular Mail'),
        ('E', 'E-Mail'),
    )
    id = models.CharField(max_length=3, primary_key=True)
    journal = models.ForeignKey(journals.Journal)
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
        
    
    
class PaymentTerm(TomModel):
    name = models.CharField(max_length=200)
    days = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    #proforma = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
        
    def get_due_date(self,date1):
        d = date1 + relativedelta(months=self.months,days=self.days)
        return d


class ShippingMode(TomModel):
    name = models.CharField(max_length=200)
    price = fields.PriceField(blank=True,null=True)
    
    def __unicode__(self):
        return self.name
        
        

class ProductCat(TomModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.name

class Product(TomModel):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cat = models.ForeignKey("ProductCat",verbose_name="Category")
    vatExempt = models.BooleanField(default=False)
    price = fields.PriceField(blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    def __unicode__(self):
        return self.name

class SalesRule(models.Model):
    journal = models.ForeignKey(journals.Journal,blank=True,null=True)
    imode = models.ForeignKey(InvoicingMode,blank=True,null=True)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    
def get_sales_rule(doc):
    for r in SalesRule.objects.all().order_by("id"):
        if r.journal is None or r.journal == doc.journal:
            return r

class SalesDocument(journals.AbstractDocument):
    
    creation_date = fields.MyDateField() #auto_now_add=True)
    customer = models.ForeignKey(Contact,
      related_name="customer_%(class)s")
    ship_to = models.ForeignKey(Contact,blank=True,null=True,
      related_name="shipTo_%(class)s")
    your_ref = models.CharField(max_length=200,blank=True)
    imode = models.ForeignKey(InvoicingMode)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    remark = models.CharField("Remark for internal use",
      max_length=200,blank=True)
    subject = models.CharField("Subject line",max_length=200,blank=True)
    vat_exempt = models.BooleanField(default=False)
    item_vat = models.BooleanField(default=False)
    total_excl = fields.PriceField(default=0)
    total_vat = fields.PriceField(default=0)
    intro = models.TextField("Introductive Text",blank=True)
    user = models.ForeignKey(User,blank=True,null=True)
    sent_date = fields.MyDateField(blank=True,null=True)
    #status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    #~ class Meta:
        #~ abstract = True
        
    def add_item(self,product=None,qty=None,**kw):
        if product is not None:
            if not isinstance(product,Product):
                product = Product.objects.get(pk=product)
            if qty is None:
                qty = 1
        kw['product'] = product 
        kw['qty'] = qty
        return self.docitem_set.create(**kw)
        
    def total_incl(self):
        return self.total_excl + self.total_vat
    total_incl.field = fields.PriceField()

    def before_save(self):
      
        r = get_document_rule(self)
        if r is None:
            raise journals.DocumentError("no document rule")
        if self.imode is None:
            self.imode = r.imode
        if self.shipping_mode is None:
            self.shipping_mode = r.shipping_mode
        if self.shipping_mode is None:
            self.shipping_mode = r.shipping_mode
      
        total_excl = 0
        total_vat = 0
        for i in self.docitem_set.all():
            if i.total is not None:
                total_excl += i.total
            #~ if not i.product.vatExempt:
                #~ total_vat += i.total_excl() * 0.18
        self.total_excl = total_excl
        self.total_vat = total_vat
        
    def send(self,simulate=True):
        result = render.print_instance(self,model=self.get_model(),as_pdf=True)
        #print result
        fn = "%s%d.pdf" % (self.journal.id,self.id)
        file(fn,"w").write(result)
        if not simulate:
            self.sent_date = datetime.date.today()
            self.save()
        
        
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
                       'unitPrice','qty'):
                d[fn] = getattr(item,fn)
            d['qty'] *= qty
            #d['total'] *= qty
            items.append(d)
        if simulate:
            return True
        invoice = self.imode.journal.create_document(
            creation_date=today,order=self,
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
            
journals.register_doctype(Order)        
        
    
class Invoice(SalesDocument):
    due_date = fields.MyDateField("Payable until",blank=True,null=True)
    order = models.ForeignKey(Order,blank=True,null=True)
    #can_send = models.BooleanField(default=False)
    
    
    def before_save(self):
        Document.before_save(self)
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.creation_date)



class DocItem(TomModel):
    document = models.ForeignKey(SalesDocument) 
    pos = models.IntegerField("Position")
    
    product = models.ForeignKey(Product,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True)
    description = models.TextField(blank=True,null=True)
    
    discount = models.IntegerField("Discount %",default=0)
    unitPrice = fields.PriceField(blank=True,null=True) 
    qty = fields.QuantityField(blank=True,null=True)
    total = fields.PriceField(blank=True,null=True)
    
    #~ def total_excl(self):
        #~ if self.unitPrice is not None:
            #~ qty = self.qty or 1
            #~ return self.unitPrice * qty
        #~ elif self.total is not None:
            #~ return self.total
        #~ return 0
        
    def before_save(self):
        #print "before_save()", self
        if self.pos is None:
            self.pos = self.document.docitem_set.count() + 1
        if self.product:
            if not self.title:
                self.title = self.product.name
            if not self.description:
                self.description = self.product.description
            if self.unitPrice is None:
                if self.product.price is not None:
                    self.unitPrice = self.product.price * (100 - self.discount) / 100
        if self.unitPrice is not None and self.qty is not None:
            self.total = self.unitPrice * self.qty
        self.document.save() # update total in document
    before_save.alters_data = True

journals.register_doctype(Invoice)



##
## report definitions
##        
        
from django import forms

from lino.django.utils import reports
from lino.django.utils import layouts
from lino.django.utils import perms

from lino.django.utils.models import Country, Languages

class ContactPageLayout(layouts.PageLayout):
    
    box1 = """
              title:10 firstName:15 lastName
              companyName nationalId:12
              """
    box2 = """email:30 
              url:30"""
    box3 = """phone:15 
              gsm:15"""
    box4 = """country region
              city zipCode:10
              addr1:30
              addr2:30
              """
    box7 = """vatId
              vatExempt itemVat 
              language
              paymentTerm"""
    #~ box7 = """box5 
              #~ box6
              #~ """
    main = """
            box1
            box2 box3
            box4 box7
            remarks:45x6
            """
            
    #~ def documents(self):
        #~ return DocumentsByCustomer()
            

class ContactDocumentsLayout(ContactPageLayout):
    label = "Documents"
    main = """
            box1
            documents
            """
    def inlines(self):
        return dict(documents=DocumentsByContact())


class Contacts(reports.Report):
    page_layouts = (ContactPageLayout, ContactDocumentsLayout)
    columnNames = "id:3 companyName firstName lastName title country"
    can_delete = True
    model = Contact
    order_by = "id"
    #can_view = perms.is_authenticated

        
class Companies(Contacts):
    #queryset=Contact.objects.order_by("companyName")
    columnNames = "companyName country title firstName lastName"
    exclude = dict(companyName__exact='')
    order_by = "companyName"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    

class Persons(Contacts):
    filter = dict(companyName__exact='')
    order_by = "lastName firstName"
    columnNames = "title firstName lastName country"
    
class PaymentTerms(reports.Report):
    model = PaymentTerm
    order_by = "id"
    can_view = perms.is_staff
    #~ def can_view(self,request):
      #~ return request.user.is_staff

class ShippingModes(reports.Report):
    model = ShippingMode
    order_by = "id"
    can_view = perms.is_staff
    #~ def can_view(self,request):
      #~ return request.user.is_staff

class InvoicingModes(reports.Report):
    model = InvoicingMode
    order_by = "id"
    can_view = perms.is_staff

class ProductCats(reports.Report):
    model = ProductCat
    order_by = "id"
    can_view = perms.is_staff

class ProductPageLayout(layouts.PageLayout):
    main = """
    id:5 name:50 cat
    description:50x6
    price vatExempt
    """

class Products(reports.Report):
    page_layouts = (ProductPageLayout,)
    model = Product
    order_by = "id"
    columnNames = "id:3 name description:30x1 cat vatExempt price:6"
    
    
class DocumentPageLayout(layouts.PageLayout):
    box1 = """
      number your_ref creation_date 
      user sent_date
      customer 
      ship_to
      """
    box2 = """
      imode
      shipping_mode 
      payment_term
      vat_exempt item_vat
      """
    box3 = """
      subject:40
      remark:40
      intro:40x5
      """
    box4 = """
      total_excl
      total_vat
      total_incl
      """
    box5 = ''
    
    main = """
      box1 box2 box4
      box3 box5
      items:60x5
      """
      
    def inlines(self):
        return dict(items=ItemsByDocument())
        
class OrderPageLayout(DocumentPageLayout):
    box5 = """
      cycle
      start_date
      covered_until
      """
        
        
class InvoicePageLayout(DocumentPageLayout):
    box5 = """
      order
      """

class EmittedInvoicesPageLayout(DocumentPageLayout):
    label = "Emitted invoices"
    main = """
    number:4 creation_date customer:20 start_date
    emitted_invoices
    """
    def inlines(self):
        return dict(emitted_invoices=InvoicesByOrder())
   

class Orders(reports.Report):
    model = Order
    order_by = "number"
    page_layouts = (OrderPageLayout,EmittedInvoicesPageLayout,)
    columnNames = "number:4 creation_date customer:20 imode " \
                  "remark:20 subject:20 total_incl " \
                  "cycle start_date covered_until"
    can_view = perms.is_authenticated
    
    

class PendingOrdersParams(forms.Form):
    make_until = forms.DateField(label="Make invoices until",
      initial=datetime.date.today()+ONE_DAY,required=False)

class PendingOrders(Orders):
    param_form = PendingOrdersParams
    def get_queryset(self,master_instance,make_until=None):
        assert master_instance is None
        return Order.objects.pending(make_until=make_until)
    
class Invoices(reports.Report):
    model = Invoice
    order_by = "number"
    page_layouts = (InvoicePageLayout,)
    columnNames = "number:4 creation_date due_date " \
                  "customer:10 " \
                  "total_incl order subject:10 remark:10 " \
                  "total_excl total_vat user "
    can_view = perms.is_staff

class DocumentsToSign(Invoices):
    filter = dict(user__exact=None)
    can_add = perms.never
    columnNames = "number:4 order creation_date " \
                  "customer:10 imode " \
                  "subject:10 total_incl total_excl total_vat "
                  
    def get_row_actions(self,renderer):
        l = super(Invoices,self).get_row_actions(renderer)
        
        def sign(renderer):
            for row in renderer.selected_rows():
                row.instance.user = renderer.request.user
                row.instance.save()
            renderer.must_refresh()
            
        l.append( ('sign', sign) )
        return l 
        
    
  
class InvoicesByOrder(reports.Report):
    model = Invoice
    master = Order
    fk_name = "order"
    order_by = "number"
    columnNames = "number creation_date your_ref total_excl total_vat shipping_mode payment_term due_date subject remark vat_exempt item_vat "

    
class ItemsByDocumentRowLayout(layouts.RowLayout):
    title_box = """
    product
    title
    """
    main = "pos:3 title_box description:20x1 discount unitPrice qty total"

class ItemsByDocument(reports.Report):
    #~ columnNames = "pos:3 product title description:30x1 " \
                  #~ "unitPrice qty total"
    row_layout_class = ItemsByDocumentRowLayout
    model = DocItem
    master = SalesDocument
    order_by = "pos"
    
    

class DocumentsByContact(reports.Report):
    page_layouts = (DocumentPageLayout,)
    columnNames = "number:4 creation_date:8 " \
                  "total_incl total_excl total_vat"
    model = SalesDocument
    master = Contact
    fk_name = 'customer'
    order_by = "creation_date"

    def get_title(self,renderer):
        return unicode(renderer.master_instance) + " : documents by customer"




class CountryPageLayout(layouts.PageLayout):
    main = """
    isocode name
    contacts
    """

    def inlines(self):
        return dict(contacts = ContactsByCountry())

        
class Countries(reports.Report):
    #page_layout_class = CountryPageLayout
    model = Country
    order_by = "isocode"
    
    page_layouts = (CountryPageLayout,)
    
    
class ContactsByCountry(Contacts):
    model = Contact
    master = Country
    order_by = "city addr1"
    
        
class MakeInvoicesDialog(layouts.Dialog):
    # not yet working
    class form_class(forms.Form):
        today = forms.DateField(label="Generate invoices on")
        order = forms.ModelChoiceField(
            label="(only for this single order:)",
            queryset=Order.objects.all())
    
    intro = layouts.StaticText("""
    <p>This is the first example of a <em>Dialog</em>.</p>
    """)
    
    layout = """
    intro
    today
    order
    simulate ok cancel help
    """
    
    def execute(self,simulate=False):
        orders_seen = 0
        invoices_made = 0
        if self.order is not None: # all orders
            orders = Order.objects.all()
        else:
            orders = ( self.order, )
        for ct in orders:
            orders_seen += 1
            if ct.make_invoice(self.make_until,simulate):
                invoices_made += 1
        if simulate:
            msg = "%d orders would make %d invoices."
        else:
            msg = "%d orders made %d new invoices."
        self.message(msg,orders_seen, invoices_made)
        
    def ok(self):
        return self.execute(simulate=False)
        
    def simulate(self):
        return self.execute(simulate=True)
            
        


def lino_setup(lino):
    pass
    #~ m = lino.add_menu("contacts","~Contacts")
    #~ m.add_action(Companies())
    #~ m.add_action(Persons())
    #~ m.add_action(Contacts(),label="All")
    #~ m = lino.add_menu("prods","~Products")
    #~ m.add_action(Products())
    #~ m.add_action(ProductCats())
    #~ m = lino.add_menu("docs","~Documents",
      #~ can_view=perms.is_authenticated)
    #~ m.add_action(Orders())
    #~ m.add_action(Invoices())
    #~ m.add_action(DocumentsToSign())
    #~ m.add_action(PendingOrders())
    
    m = lino.add_menu("admin","~Administration",
      can_view=perms.is_staff)
    m.add_action(MakeInvoicesDialog())
    
    #~ m = lino.add_menu("config","~Configuration",
      #~ can_view=perms.is_staff)
    #~ m.add_action(InvoicingModes())
    #~ m.add_action(ShippingModes())
    #~ m.add_action(PaymentTerms())
    #~ m.add_action(Languages())
    #~ m.add_action(Countries())


