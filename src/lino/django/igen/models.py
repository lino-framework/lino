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

from django.db import models
#from lino.django.tom import models
from django.utils.safestring import mark_safe

from lino.django.utils.validatingmodel import TomModel, ModelValidationError



def linkto(href,text=None):
    if text is None:
        text=href
    return '<a href="%s">%s</a>' % (href,text)
        
class PriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=10,
            max_digits=10,
            decimal_places=2,
            )
        defaults.update(kwargs)
        super(PriceField, self).__init__(*args, **defaults)
        
    def formfield(self, **kwargs):
        fld = super(PriceField, self).formfield(**kwargs)
        # display size is smaller than full size:
        fld.widget.attrs['size'] = "6"
        fld.widget.attrs['style'] = "text-align:right;"
        return fld
        
class MyDateField(models.DateField):
        
    def formfield(self, **kwargs):
        fld = super(MyDateField, self).formfield(**kwargs)
        # display size is smaller than full size:
        fld.widget.attrs['size'] = "8"
        return fld
        
        
        
class QuantityField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=5,
            max_digits=5,
            decimal_places=0,
            )
        defaults.update(kwargs)
        super(QuantityField, self).__init__(*args, **defaults)
        
    def formfield(self, **kwargs):
        fld = super(QuantityField, self).formfield(**kwargs)
        fld.widget.attrs['size'] = "3"
        fld.widget.attrs['style'] = "text-align:right;"
        return fld
        
        
  
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



class PaymentTerm(TomModel):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
        
    def get_due_date(self,date1):
        return date1

class ShippingMode(TomModel):
    name = models.CharField(max_length=200)
    
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
    price = PriceField(blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    def __unicode__(self):
        return self.name
        

class Document(TomModel):
    
    #journal = models.ForeignKey(Journal)
    number = models.AutoField(primary_key=True)
    creation_date = MyDateField() #auto_now_add=True)
    customer = models.ForeignKey(Contact,
      related_name="customer_%(class)s")
    ship_to = models.ForeignKey(Contact,blank=True,null=True,
      related_name="shipTo_%(class)s")
    your_ref = models.CharField(max_length=200,blank=True)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    remarks = models.CharField(max_length=200,blank=True)
    vat_exempt = models.BooleanField(default=False)
    item_vat = models.BooleanField(default=False)
    total_excl = PriceField(default=0)
    total_vat = PriceField(default=0)
    intro = models.TextField("Introductive Text",blank=True)
    
    #~ class Meta:
        #~ abstract = True
        
    def __unicode__(self):
        return "%s # %d" % (self.__class__.__name__,self.number)
        
    def add_item(self,product,qty=None,**kw):
        if product is not None:
            if not isinstance(product,Product):
                product = Product.objects.get(pk=product)
            if qty is None:
                qty = 1
        kw['product'] = product 
        kw['qty'] = qty
        return self.docitem_set.add(DocItem(document=self,**kw))
        
    def total_incl(self):
        return self.total_excl + self.total_vat
    total_incl.field = PriceField()

    def before_save(self):
        total_excl = 0
        total_vat = 0
        for i in self.docitem_set.all():
            total_excl += i.total_excl()
            #~ if not i.product.vatExempt:
                #~ total_vat += i.total_excl() * 0.18
        self.total_excl = total_excl
        self.total_vat = total_vat
        
class Order(Document):
    valid_until = MyDateField("Valid until",blank=True,null=True)
  
class Contract(Document):
    CYCLE_CHOICES = (
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
        ('I', 'Idle'),
    )
    #~ start_date = MyDateField("When to issue next invoice",
      #~ blank=True,null=True,auto_now_add=True)
    cycle = models.CharField(max_length=1, choices=CYCLE_CHOICES)
    
    def get_last_invoice(self):
        invoices = self.invoice_set.order_by('creation_date')
        cnt = invoices.count()
        if cnt == 0:
            return None
        return invoices[cnt-1]
    
    def next_cycle(self,date):
        if self.cycle == "W":
            date += relativedelta(weeks=1)
            #date += datetime.timedelta(7)
        elif self.cycle == "M":
            date += relativedelta(months=1)
            #date += datetime.timedelta(30)
        elif self.cycle == "Q":
            date += relativedelta(months=3)
            #date += datetime.timedelta(91)
        elif self.cycle == "Y":
            date += relativedelta(years=1)
            #date += datetime.timedelta(365)
        return datetime.date(date.year,date.month,date.day)
        
        
    def make_invoice(self,today=None):
        if self.cycle == 'I':
            return
        if today is None:
            today = datetime.date.today()
        last_invoice = self.get_last_invoice()
        if last_invoice is None:
            date = self.creation_date
        else:
            date = self.next_cycle(last_invoice.creation_date)
        #~ print "today", type(today), today
        #~ print "date", type(date), date
        #~ assert isinstance(date,datetime.date)
        #~ assert isinstance(today,datetime.date)
        items = []
        while date <= today:
            items.append(dict(title=str(self) + " " + str(date)+" :"))
            for item in self.docitem_set.all():
                d = {}
                for fn in ('product','title','description',
                    'unitPrice','qty','total'):
                    d[fn] = getattr(item,fn)
                items.append(d)
            date = self.next_cycle(date)
        if len(items) == 0:
            return 
        invoice = Invoice(creation_date=date,contract=self,
            customer=self.customer,
            ship_to=self.ship_to,payment_term=self.payment_term)
        invoice.save()
        for d in items:
            i = DocItem(document=invoice,**d)
            i.save()
        return invoice
            
        
        
    
class Invoice(Document):
    due_date = MyDateField("Payable until",blank=True,null=True)
    contract = models.ForeignKey(Contract,blank=True,null=True)
    
    def before_save(self):
        Document.before_save(self)
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.creation_date)

  

class DocItem(TomModel):
    document = models.ForeignKey(Document) 
    pos = models.IntegerField("Position")
    
    product = models.ForeignKey(Product,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
    unitPrice = PriceField(blank=True,null=True) 
    qty = QuantityField(blank=True,null=True)
    total = PriceField(blank=True,null=True)
    
    #~ class Meta:
        #~ abstract = True
        
    def total_excl(self):
        if self.unitPrice:
            qty = self.qty or 1
            return self.unitPrice * qty
        elif self.total:
            return self.total
        return 0
        
    def before_save(self):
        #print "before_save()", self
        if self.pos is None:
            self.pos = self.document.docitem_set.count() + 1
        if self.product:
            if not self.title:
                self.title = self.product.name
            if not self.description:
                self.description = self.product.description
            if not self.unitPrice:
                self.unitPrice = self.product.price
        self.document.save()
    before_save.alters_data = True
        



##
## report definitions
##        
        
from lino.django.utils import reports
from lino.django.utils.layouts import PageLayout 

from lino.django.utils.models import Country, Languages






class ContactPageLayout(PageLayout):
    
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
        return dict(documents=DocumentsByCustomer())


class Contacts(reports.Report):
    page_layouts = (ContactPageLayout, ContactDocumentsLayout)
    columnNames = "id:3 companyName firstName lastName title country"
    can_delete = True
    model = Contact
    order_by = "id"
    


        
class Companies(Contacts):
    #queryset=Contact.objects.order_by("companyName")
    columnNames = "companyName country title firstName lastName"
    queryset = Contact.objects.exclude(companyName__exact=None)
    order_by = "companyName"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    

class Persons(Contacts):
    queryset=Contact.objects.filter(companyName__exact=None)
    order_by = "lastName firstName"
    columnNames = "title firstName lastName country"
    
class PaymentTerms(reports.Report):
    model = PaymentTerm
    order_by = "id"
    def can_view(self,request):
      return request.user.is_staff

class ShippingModes(reports.Report):
    model = ShippingMode
    order_by = "id"
    def can_view(self,request):
      return request.user.is_staff

class ProductCats(reports.Report):
    queryset=ProductCat.objects.order_by("id")

class ProductPageLayout(PageLayout):
    main = """
        id:5 name:50 cat
        description:50x6
        price vatExempt
    """

class Products(reports.Report):
    page_layouts = (ProductPageLayout,)
    queryset = Product.objects.order_by("id")
    columnNames = "id:3 name description:30x1 cat vatExempt price:6"
    
    
class DocumentPageLayout(PageLayout):
    box1 = """
      number your_ref creation_date
      customer ship_to
      """
    box2 = """
      shipping_mode 
      payment_term
      vat_exempt item_vat
      """
    box3 = """
      remarks:40
      intro:40x5
      """
    box4 = """
      total_excl
      total_vat
      total_incl
      """
    main = """
      box1 box2 box4
      box3 
      items:80x5
      """
      
    #~ def items(self):
        #~ return ItemsByDocument()
      
    def inlines(self):
        return dict(items=ItemsByDocument())

class Documents(reports.Report):
    page_layouts = (DocumentPageLayout,)
    #detail_reports = "items"
    columnNames = "number:4 creation_date customer:20 " \
                  "total_incl total_excl total_vat"

        
class Orders(Documents):
    queryset = Order.objects.order_by("number")
    
    
class ContractPageLayout(DocumentPageLayout):
    label = "Emitted invoices"
    main = "emitted_invoices"
    def inlines(self):
        return dict(emitted_invoices=InvoicesByContract())
   

class Contracts(Documents):
    queryset = Contract.objects.order_by("number")
    page_layouts = Documents.page_layouts + (ContractPageLayout,)


class InvoicePageLayout(DocumentPageLayout):
    box2 = """
      shipping_mode
      payment_term
      vat_exempt item_vat
      contract
      """

class Invoices(Orders):
    queryset = Invoice.objects.order_by("number")
    page_layouts = (InvoicePageLayout,)

class InvoicesByContract(Orders):
    model = Invoice
    master = Contract
    fk_name = "contract"
    order_by = "number"

    
class ItemsByDocument(reports.Report):
    columnNames = "pos:3 product title description:30x1 " \
                  "unitPrice qty total"
    model = DocItem
    master = Document
    order_by = "pos"
    
    
    #~ def __init__(self,doc,**kw):
        #~ self.doc = doc
        #~ reports.Report.__init__(self,**kw)
        
    #~ def get_queryset(self,document):
        #~ return document.docitem_set.order_by("pos")
#Documents.items = ItemsByDocument()

class DocumentsByCustomer(Documents):
    #detail_reports = "items"
    columnNames = "number:4 creation_date:8 " \
                  "total_incl total_excl total_vat"
    model = Document
    master = Contact
    fk_name = 'customer'
    order_by = "creation_date"

    #~ def __init__(self,customer,**kw):
        #~ self.customer = customer
        #~ reports.Report.__init__(self,**kw)
        
    #~ def get_queryset(self):
        #~ return Document.objects.filter(customer=self.customer).order_by("creation_date")

    def get_title(self,renderer):
        return unicode(renderer.master_instance) + " : documents by customer"




class CountryPageLayout(PageLayout):
    main = """
    isocode name
    contacts
    """
    #~ def contacts(self):
        #~ return ContactsByCountry()
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


def lino_setup(lino):
    m = lino.add_menu("contacts","~Contacts")
    m.add_action(Contacts())
    m.add_action(Companies())
    m.add_action(Persons())
    m = lino.add_menu("prods","~Products")
    m.add_action(Products())
    m.add_action(ProductCats())
    m = lino.add_menu("docs","~Documents")
    m.add_action(Orders())
    m.add_action(Contracts())
    m.add_action(Invoices())
    m = lino.add_menu("config","~Configuration")
    m.add_action(ShippingModes())
    m.add_action(PaymentTerms())
    m.add_action(Languages())
    m.add_action(Countries())


