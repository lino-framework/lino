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
from lino.django.tom.layout import VBOX, HBOX

from django.utils.safestring import mark_safe


def linkto(href,text=None):
    if text is None:
        text=href
    return '<a href="%s">%s</a>' % (href,text)
        
class PriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        kwargs['max_digits'] = 10
        kwargs['decimal_places'] = 2
        super(PriceField, self).__init__(*args, **kwargs)
        
class QuantityField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        kwargs['max_digits'] = 5
        kwargs['decimal_places'] = 2
        super(QuantityField, self).__init__(*args, **kwargs)
        
        
#~ class SizedCharField(models.CharField):

    #~ def __init__(self, size=None, *args, **kwargs):
        #~ self.size = size
        #~ super(SizedCharField, self).__init__(*args, **kwargs)
        
    #~ def formfield(self, *args, **kwargs):
        #~ formfield = super(SizedCharField, self).formfield(*args, **kwargs)
        #~ formfield.widget.attrs['size'] = str(self.size)
        #~ return formfield

          

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

    def page_layout(self):
        return VBOX(
            VBOX("""
              title:5 firstName:20 lastName:50
              companyName:60 nationalId:15
              """),
            HBOX(
              VBOX("email:60 url:60"),
              VBOX("phone:15 gsm:15"),
              label="Contact"
            ),
            HBOX(
              VBOX("""
                  country region
                  city:25 zipCode:25
                  addr1:60
                  addr2:60
                  """),
              VBOX(
                VBOX("vatId vatExempt itemVat"),
                VBOX("language paymentTerm"),
                label="Options",
              ),
            ),
            VBOX("remarks:6x60"),
        )
    

class Country(TomModel):
    name = models.CharField(max_length=200)
    isocode = models.CharField(max_length=2,primary_key=True)
    
    class Meta:
        verbose_name_plural = "Countries"

    
    def __unicode__(self):
        return self.name
        
    def contacts(self):
        return ContactsByCountry(self)
        #~ return ", ".join([unicode(c) for c in self.contact_set.all()])
        #~ return mark_safe(", ".join([linkto(c.get_url_path(),unicode(c)) 
          #~ for c in self.contact_set.all()]))
    #~ #contacts.allow_tags=True
    #~ contacts.short_description='List of Contacts here'
        
#~ class Region(models.Model):
    #~ name = models.CharField(max_length=200)
    #~ country = models.ForeignKey("Country")
    
    #~ def __unicode__(self):
        #~ return self.name
        
    
#~ class City(models.Model):
    #~ name = models.CharField(max_length=200)
    #~ country = models.ForeignKey("Country")
    #~ region = models.ForeignKey(Region)
    
    #~ def __unicode__(self):
        #~ return self.name
        
    #~ @allow_tags=True
    #~ @short_description = 'List of Contacts here'
    #~ def contacts(self):
        #~ return ", ".join([linkto(c,displayName(c)) 
          #~ for c in self.contact_set.all()])
 
    
class Language(TomModel):
    id = models.CharField(max_length=2,primary_key=True)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class PaymentTerm(TomModel):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

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
    def page_layout(self):
        return VBOX("""
        id:5 name:50 cat
        description:6x50
        price vatExempt
        """)

#~ class Journal(models.Model):
    #~ name = models.CharField(max_length=200)
    #~ def __unicode__(self):
        #~ return self.name

class Document(TomModel):
    #journal = models.ForeignKey(Journal)
    number = models.AutoField(primary_key=True)
    creation_date = models.DateField(auto_now_add=True)
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
    total_excl = PriceField(blank=True,null=True)
    total_vat = PriceField(blank=True,null=True)
    intro = models.TextField("Introductive Text",blank=True,null=True)
    
    class Meta:
        abstract = True
        
    def total_incl(self):
        return self.total_excl + self.total_vat

class Order(Document):
    valid_until = models.DateField("Valid until",blank=True,null=True)

class Invoice(Document):
    due_date = models.DateField("Payable until",blank=True,null=True)
    
    def page_layout(self):
        return VBOX(
          HBOX("""
            number your_ref creation_date         
            customer:40 ship_to:40
            ""","""
            shipping_mode payment_term
            vat_exempt item_vat
            """,
          ),
          HBOX("""
            remarks:40
            intro:5x40
            ""","""
            total_excl 
            total_vat
            #total_incl
            """),
          "items"
          )
            
    def items(self):
        return ItemsByInvoice(self)

class DocumentItem(TomModel):
    pos = models.IntegerField("Position")
    
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
    unitPrice = PriceField(blank=True,null=True) 
    qty = QuantityField(blank=True,null=True)
    total = PriceField(blank=True,null=True)
    
    class Meta:
        abstract = True
    
class OrderItem(DocumentItem):
    order = models.ForeignKey(Order) #,related_name="items")
        
class InvoiceItem(DocumentItem):
    invoice = models.ForeignKey(Invoice) #,related_name="items")
        
        
               

#
# report definitions
#        
        
from lino.django.tom import reports

class Contacts(reports.Report):
    queryset=Contact.objects.order_by("id")
    columnNames="id companyName firstName lastName title country"
    can_delete=True

class Companies(reports.Report):
    #queryset=Contact.objects.order_by("companyName")
    columnNames="companyName country title firstName lastName"
    queryset=Contact.objects.exclude(companyName__exact=None)\
      .order_by("companyName")

class Persons(reports.Report):
    queryset=Contact.objects.filter(companyName__exact=None)\
      .order_by("lastName","firstName")
    columnNames="title firstName lastName country"
    
class ContactsByCountry(reports.Report):
    
    def __init__(self,country,**kw):
        self.country=country
        reports.Report.__init__(self,**kw)
        
    def get_queryset(self):
        return self.country.contact_set.order_by("city","addr1")
    

class Countries(reports.Report):
    queryset=Country.objects.order_by("isocode")
    columnNames="isocode name contacts"
    #columnWidths="3 30"
    

class Languages(reports.Report):
    queryset=Language.objects.order_by("id")

class PaymentTerms(reports.Report):
    queryset=PaymentTerm.objects.order_by("id")

class ShippingModes(reports.Report):
    queryset=ShippingMode.objects.order_by("id")

class ProductCats(reports.Report):
    queryset=ProductCat.objects.order_by("id")

class Products(reports.Report):
    queryset=Product.objects.order_by("id")

class Orders(reports.Report):
    queryset=Order.objects.order_by("number")

class Invoices(reports.Report):
    queryset=Invoice.objects.order_by("number")
    columnNames="number items due_date customer total_excl total_vat"

class ItemsByInvoice(reports.Report):
    
    def __init__(self,invoice,**kw):
        self.invoice=invoice
        reports.Report.__init__(self,**kw)
        
    def get_queryset(self):
        return self.invoice.invoiceitem_set.order_by("pos")
        #return InvoiceItem.objects.filter(invoice=self.invoice).order_by("pos")
    #queryset=property(get_queryset)
