from django.db import models
from lino import dd
from lino.utils import join_elems
from lino.utils.xmlgen.html import E

# We must import it so that it gets loaded together with the models.
from .tables import *


class Place(dd.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Member(dd.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Product(dd.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    @dd.displayfield("Offered by")
    def offered_by(self, ar):
        items = [ar.obj2html(o.provider)
                 for o in OffersByProduct.request(self)]
        items = join_elems(items, sep=', ')
        return E.p(*items)

    @dd.displayfield("Wanted by")
    def demanded_by(self, ar):
        items = [ar.obj2html(o.customer)
                 for o in DemandsByProduct.request(self)]
        items = join_elems(items, sep=', ')
        return E.p(*items)


class Offer(dd.Model):
    provider = models.ForeignKey(Member)
    product = models.ForeignKey(Product)
    valid_until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s offered by %s" % (self.product, self.provider)


class Demand(dd.Model):
    customer = models.ForeignKey(Member)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "%s (%s)" % (self.product, self.provider)




