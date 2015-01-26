from django.db.models import Q
from lino import dd


class Places(dd.Table):
    model = 'lets.Place'


class Members(dd.Table):
    model = 'lets.Member'

    # column_names = "name email place DemandsByMember OffersByMember"
    column_names = "name email place offered_products wanted_products"

    detail_layout = """
    id name place email
    OffersByMember DemandsByMember
    """


class Products(dd.Table):
    model = 'lets.Product'
    order_by = ['name']

    detail_layout = """
    id name
    OffersByProduct DemandsByProduct
    """

    column_names = 'id name providers customers'


class ActiveProducts(Products):
    
    label = "Active products"
    column_names = 'name offered_by wanted_by'

    @classmethod
    def get_request_queryset(cls, ar):
        # add filter condition to the queryset so that only active
        # products are shown, i.e. for which there is at least one
        # offer or one demand.
        qs = super(ActiveProducts, cls).get_request_queryset(ar)
        qs = qs.filter(Q(offer__isnull=False) | Q(demand__isnull=False))
        qs = qs.distinct()
        return qs


class Offers(dd.Table):
    model = 'lets.Offer'


class OffersByMember(Offers):
    master_key = 'provider'

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        return [ar.obj2html(obj.product)]


class OffersByProduct(Offers):
    master_key = 'product'

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        return [ar.obj2html(obj.provider)]


class Demands(dd.Table):
    model = 'lets.Demand'


class DemandsByMember(Demands):
    master_key = 'customer'

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        return [ar.obj2html(obj.product)]


class DemandsByProduct(Demands):
    master_key = 'product'

    @classmethod
    def summary_row(cls, ar, obj, **kw):
        return [ar.obj2html(obj.customer)]
