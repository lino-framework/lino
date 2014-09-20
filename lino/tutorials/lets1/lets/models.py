
from django.db import models
from lino import dd, rt


class Place(dd.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Places(dd.Table):
    model = Place


class Provider(dd.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Providers(dd.Table):
    model = Provider

    detail_layout = """
    id name place email
    OffersByProvider
    """


class Customer(dd.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Customers(dd.Table):
    model = Customer

    detail_layout = """
    id name place email
    DemandsByCustomer
    """


class Product(dd.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Products(dd.Table):
    model = Product

    detail_layout = """
    id name
    OffersByProduct DemandsByProduct
    """


class Offer(dd.Model):
    provider = models.ForeignKey(Provider)
    product = models.ForeignKey(Product)
    valid_until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s offered by %s" % (self.product, self.provider)


class Offers(dd.Table):
    model = Offer


class OffersByProvider(Offers):
    master_key = 'provider'


class OffersByProduct(Offers):
    master_key = 'product'


class Demand(dd.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "%s (%s)" % (self.product, self.provider)


class Demands(dd.Table):
    model = Demand


class DemandsByCustomer(Demands):
    master_key = 'customer'


class DemandsByProduct(Demands):
    master_key = 'product'
