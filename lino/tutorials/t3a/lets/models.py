from django.db import models
from lino import reports

class Place(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
        
class Provider(models.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place,blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place,blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    #~ provider = models.ForeignKey(Provider)
    
    def __unicode__(self):
        return self.name

class Offer(models.Model):
    provider = models.ForeignKey(Provider)
    product = models.ForeignKey(Product)
    valid_until = models.DateField(blank=True,null=True)
    
    def __unicode__(self):
        return "%s offered by %s" % (self.product,self.provider)

class Demand(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    
    def __unicode__(self):
        return "%s (%s)" % (self.product,self.provider)

class Providers(reports.Report):
    model = Provider
    
class Customers(reports.Report):
    model = Customer

class Products(reports.Report):
    model = Product

class Offers(reports.Report):
    model = Offer

class Places(reports.Report):
    model = Place

class OffersByProvider(Offers):
    fk_name = 'provider'
        
class Demands(reports.Report):
    model = Demand

class DemandsByCustomer(Demands):
    fk_name = 'customer'

class DemandsByProduct(Demands):
    fk_name = 'product'

class OffersByProduct(Offers):
    fk_name = 'product'
        
