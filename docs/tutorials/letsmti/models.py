from django.db import models

from lino import dd
from lino.utils import join_elems
from lino.utils import mti
from lino.utils.xmlgen.html import E


class Place(dd.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Member(dd.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True)

    is_customer = mti.EnableChild('Customer',
                                  verbose_name="is a customer")
    is_supplier = mti.EnableChild('Supplier',
                                  verbose_name="is a supplier")

    def __unicode__(self):
        return self.name


class Customer(Member):
    customer_remark = models.CharField(max_length=200, blank=True)

    
class Supplier(Member):

    supplier_remark = models.CharField(max_length=200, blank=True)
    

class Product(dd.Model):
    name = models.CharField(max_length=200)

    suppliers = models.ManyToManyField(
        'Supplier', through='Offer',
        related_name='offered_products')
    customers = models.ManyToManyField(
        'Customer', through='Demand',
        related_name='wanted_products')

    def __unicode__(self):
        return self.name

    @dd.displayfield("Offered by")
    def offered_by(self, ar):
        items = [ar.obj2html(o) for o in self.suppliers.all()]
        items = join_elems(items, sep=', ')
        return E.p(*items)

    @dd.displayfield("Wanted by")
    def demanded_by(self, ar):
        items = [ar.obj2html(o) for o in self.customers.all()]
        items = join_elems(items, sep=', ')
        return E.p(*items)


class Offer(dd.Model):
    supplier = models.ForeignKey(Supplier)
    product = models.ForeignKey(Product)
    valid_until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s offered by %s" % (self.product, self.supplier)


class Demand(dd.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "%s (%s)" % (self.product, self.supplier)


# We must import it so that it gets loaded together with the models.
from .tables import *

