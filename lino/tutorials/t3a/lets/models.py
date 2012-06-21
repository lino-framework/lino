
from django.db import models
from lino import dd

class Place(dd.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
        
class Provider(dd.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place,blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name

class Customer(dd.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place,blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name

class Product(dd.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Offer(dd.Model):
    provider = models.ForeignKey(Provider)
    product = models.ForeignKey(Product)
    valid_until = models.DateField(blank=True,null=True)
    
    def __unicode__(self):
        return "%s offered by %s" % (self.product,self.provider)

class Demand(dd.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    
    def __unicode__(self):
        return "%s (%s)" % (self.product,self.provider)

class Providers(dd.Table):
    model = Provider
    
class Customers(dd.Table):
    model = Customer

class Products(dd.Table):
    model = Product

class Offers(dd.Table):
    model = Offer

class Places(dd.Table):
    model = Place

class OffersByProvider(Offers):
    master_key = 'provider'
        
class Demands(dd.Table):
    model = Demand

class DemandsByCustomer(Demands):
    master_key = 'customer'

class DemandsByProduct(Demands):
    master_key = 'product'

class OffersByProduct(Offers):
    master_key = 'product'
        
