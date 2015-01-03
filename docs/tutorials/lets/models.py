from django.db import models
from lino import dd
from lino.utils import join_elems
from lino.utils.xmlgen.html import E


class Place(dd.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Places(dd.Table):
    model = Place


class Member(dd.Model):
    name = models.CharField(max_length=200)
    place = models.ForeignKey(Place, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Members(dd.Table):
    model = Member

    detail_layout = """
    id name place email
    OffersByMember DemandsByMember
    """


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


class Products(dd.Table):
    model = Product

    detail_layout = """
    id name
    OffersByProduct DemandsByProduct
    """

    column_names = 'name offered_by demanded_by'


class Offer(dd.Model):
    provider = models.ForeignKey(Member)
    product = models.ForeignKey(Product)
    valid_until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s offered by %s" % (self.product, self.provider)


class Offers(dd.Table):
    model = Offer


class OffersByMember(Offers):
    master_key = 'provider'


class OffersByProduct(Offers):
    master_key = 'product'


class Demand(dd.Model):
    customer = models.ForeignKey(Member)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "%s (%s)" % (self.product, self.provider)


class Demands(dd.Table):
    model = Demand


class DemandsByMember(Demands):
    master_key = 'customer'


class DemandsByProduct(Demands):
    master_key = 'product'
