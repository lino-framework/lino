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
from django.db import models
#from lino.django.tom import models
from lino.django.tom.validatingmodel import TomModel, ModelValidationError

from django.utils.safestring import mark_safe


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
    firstName = models.CharField(max_length=200,blank=True,null=True)
    lastName = models.CharField(max_length=200,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    
    companyName = models.CharField(max_length=200,blank=True,null=True)
    nationalId = models.CharField(max_length=200,blank=True,null=True)
    vatId = models.CharField(max_length=200,blank=True,null=True)
    
    addr1 = models.CharField(max_length=200,blank=True,null=True)
    addr2 = models.CharField(max_length=200,blank=True,null=True)
    country = models.ForeignKey("Country",blank=True,null=True)
    #city = models.ForeignKey("City",blank=True,null=True)
    city = models.CharField(max_length=200,blank=True,null=True)
    zipCode = models.CharField(max_length=10,blank=True,null=True)
    region = models.CharField(max_length=200,blank=True,null=True)
    
    email = models.EmailField(blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    phone = models.CharField(max_length=200,blank=True,null=True)
    gsm = models.CharField(max_length=200,blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    vatExempt = models.BooleanField(default=False)
    itemVat = models.BooleanField(default=False)
    
    language = models.ForeignKey("Language",blank=True,null=True)
    paymentTerm = models.ForeignKey("PaymentTerm",blank=True,null=True)
    
    remarks = models.TextField(blank=True,null=True)
    
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


class Country(TomModel):
    name = models.CharField(max_length=200)
    isocode = models.CharField(max_length=2,primary_key=True)
    
    class Meta:
        verbose_name_plural = "Countries"
    
    def __unicode__(self):
        return self.name
        
 
    
class Language(TomModel):
    id = models.CharField(max_length=2,primary_key=True)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

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
    description = models.TextField(blank=True,null=True)
    def __unicode__(self):
        return self.name

class Product(TomModel):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
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
    creation_date = MyDateField() # auto_now_add=True)
    customer = models.ForeignKey(Contact,
      related_name="customer_%(class)s")
    ship_to = models.ForeignKey(Contact,blank=True,null=True,
      related_name="shipTo_%(class)s")
    your_ref = models.CharField(max_length=200,blank=True,null=True)
    shipping_mode = models.ForeignKey(ShippingMode,blank=True,null=True)
    payment_term = models.ForeignKey(PaymentTerm,blank=True,null=True)
    remarks = models.CharField(max_length=200,blank=True,null=True)
    vat_exempt = models.BooleanField(default=False)
    item_vat = models.BooleanField(default=False)
    total_excl = PriceField(default=0)
    total_vat = PriceField(default=0)
    intro = models.TextField("Introductive Text",blank=True,null=True)
    
    #~ class Meta:
        #~ abstract = True
        
    def __unicode__(self):
        return "%s # %d" % (self.__class__.__name__,self.number)
        
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
  
class Invoice(Document):
    due_date = MyDateField("Payable until",blank=True,null=True)
    def before_save(self):
        Document.before_save(self)
        if self.due_date is None:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.creation_date)


class DocItem(TomModel):
    document = models.ForeignKey(Document) 
    pos = models.IntegerField("Position")
    
    product = models.ForeignKey(Product)
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
        
from lino.django.tom import reports
from lino.django.utils.layouts import PageLayout 


class ContactPageLayout(PageLayout):
    
    box1 = """
              title:5 firstName:20 lastName:50
              companyName:60 nationalId:15
              """
    box2 = """email:60 
              url:60"""
    box3 = """phone:15 
              gsm:15"""
    box4 = """country region
              city:25 zipCode:25
              addr1:60
              addr2:60
              """
    box5 = """vatId 
                vatExempt 
                itemVat"""
    box6 = """language 
                paymentTerm"""
    box7 = """box5 
              box6
              """
    main = """
            box1
            box2 box3
            box4 box7
            remarks:6x60
            documents
            """



class Contacts(reports.Report):
    page_layout_class = ContactPageLayout
    #detail_reports = "documents"
    #queryset = Contact.objects.order_by("id")
    columnNames = "id:3 companyName firstName lastName title country"
    can_delete = True
    model = Contact
    order_by = "id"

    #~ documents = DocumentsByCustomer
    #~ def documents(self,renderer):
        #~ return DocumentsByCustomer(renderer.instance)

    #~ def documents(self):
        #~ return DocumentsByCustomer(self)
        
    def inlines(self):
        return dict(documents=DocumentsByCustomer())

class Companies(Contacts):
    #queryset=Contact.objects.order_by("companyName")
    columnNames = "companyName country title firstName lastName"
    queryset = Contact.objects.exclude(companyName__exact=None)
    model = Contact
    order_by = "companyName"
    #~ queryset = Contact.objects.exclude(companyName__exact=None)\
      #~ .order_by("companyName")
    

class Persons(Contacts):
    queryset=Contact.objects.filter(companyName__exact=None)
    order_by = "lastName firstName"
    columnNames="title firstName lastName country"
    
class CountryPageLayout(PageLayout):
    main = """
    isocode name
    contacts
    """
class Countries(reports.Report):
    page_layout_class = CountryPageLayout
    queryset = Country.objects.order_by("isocode")
    columnNames = "isocode name"
    
    def inlines(self):
        return dict(contacts = ContactsByCountry())

class Languages(reports.Report):
    queryset=Language.objects.order_by("id")

class PaymentTerms(reports.Report):
    queryset=PaymentTerm.objects.order_by("id")

class ShippingModes(reports.Report):
    queryset=ShippingMode.objects.order_by("id")

class ProductCats(reports.Report):
    queryset=ProductCat.objects.order_by("id")

class ProductPageLayout(PageLayout):
    main = """
        id:5 name:50 cat
        description:6x50
        price vatExempt
    """

class Products(reports.Report):
    page_layout_class = ProductPageLayout
    queryset = Product.objects.order_by("id")
    columnNames = "id:3 name description:1x30 cat vatExempt price:6"
    
    
class DocumentPageLayout(PageLayout):
    box1 = """
      number your_ref creation_date
      customer ship_to
      """
    box2 = """
      shipping_mode payment_term
      vat_exempt item_vat
      """
    box3 = """
      remarks:40
      intro:5x40
      """
    box4 = """
      total_excl 
      total_vat
      total_incl
      """
    main = """
      box1 box2
      box3 box4
      items:5x80
      """
      

class Documents(reports.Report):
    page_layout_class = DocumentPageLayout
    #detail_reports = "items"
    columnNames = "number:4 creation_date:8 customer:20 " \
                  "total_incl total_excl total_vat"

    #items = ItemsByDocument

    #~ def items(self):
        #~ return ItemsByDocument(self)
        
    def inlines(self):
        return dict(items=ItemsByDocument())
        
class Orders(Documents):
    queryset = Order.objects.order_by("number")


class InvoicePageLayout(DocumentPageLayout):
    box1 = """
      number your_ref creation_date
      customer ship_to due_date
      """

class Invoices(Orders):
    queryset = Invoice.objects.order_by("number")
    page_layout_class = InvoicePageLayout

    
class ItemsByDocument(reports.Report):
    columnNames = "pos:3 product title description:1x40 " \
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

class ContactsByCountry(Contacts):
    model = Contact
    master = Country
    order_by = "city addr1"
