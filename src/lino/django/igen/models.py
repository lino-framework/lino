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
from lino.django.tom.validatingmodel import ValidatingModel, ModelValidationError


def linkto(obj,text=None):
    if text is None:
        text=unicode(obj)
    s='<a href="/admin/igen/%s/%d' % (obj.__class__.__name__,obj.id)
    s+='">'+text+"</a>"
    return s
        
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
        

class Contact(ValidatingModel):
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
u'Mr. Luc Saffre'
>>> p=Contact.objects.create(lastName="Saffre", title="Mr.")
>>> unicode(p)
u'Mr. Saffre'
>>> p=Contact.objects.create(firstName="Luc")
>>> unicode(p)
u'Luc'
>>> p=Contact.objects.create(lastName="Saffre",firstName="Luc", companyName="Example & Co")
>>> unicode(p)
u'Example & Co (Luc Saffre)'
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
        l=filter(lambda x:x,[self.title,self.firstName,self.lastName])
        s=" ".join(l)
        if self.companyName:
            if len(s) > 0:
                return self.companyName+" ("+s+")"
            else:
                return self.companyName
        else:
            return s
            
    def asAddress(self,linesep="\n<br/>"):
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
    asAddress.allow_tags=True


class Country(models.Model):
    name = models.CharField(max_length=200)
    isocode = models.CharField(max_length=2,primary_key=True)
    
    class Meta:
        verbose_name_plural = "Countries"

    
    def __unicode__(self):
        return self.name
        
    def contacts(self):
        return ", ".join([linkto(c,displayName(c)) 
          for c in self.contact_set.all()])
    contacts.allow_tags=True
    contacts.short_description='List of Contacts here'
        
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
 
    
class Language(models.Model):
    id = models.CharField(max_length=2,primary_key=True)
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class PaymentTerm(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class ShippingMode(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class ProductCat(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    cat = models.ForeignKey("ProductCat")
    vatExempt = models.BooleanField(default=False)
    price = PriceField(blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")

#~ class Journal(models.Model):
    #~ name = models.CharField(max_length=200)
    #~ def __unicode__(self):
        #~ return self.name

class Document(models.Model):
    #journal = models.ForeignKey(Journal)
    number = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Contact,
      related_name="customer_%(class)s")
    shipTo = models.ForeignKey(Contact,blank=True,null=True,
      related_name="shipTo_%(class)s")
    yourRef = models.CharField(max_length=200,blank=True,null=True)
    shippingMode = models.ForeignKey(ShippingMode,blank=True,null=True)
    paymentTerm = models.ForeignKey(PaymentTerm,blank=True,null=True)
    remarks = models.CharField(max_length=200,blank=True,null=True)
    vatExempt = models.BooleanField(default=False)
    itemVat = models.BooleanField(default=False)
    totalExcl = PriceField(blank=True,null=True)
    totalVat = PriceField(blank=True,null=True)
    intro = models.TextField("Introductive Text",blank=True,null=True)
    
    class Meta:
        abstract = True

class Order(Document):
    validUntil = models.DateField("Valid until",blank=True,null=True)

class Invoice(Document):
    dueDate = models.DateField("Payable until",blank=True,null=True)

class DocumentItem(models.Model):
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
    order = models.ForeignKey(Order,related_name="items")
        
class InvoiceItem(DocumentItem):
    invoice = models.ForeignKey(Invoice,related_name="items")
        
        
