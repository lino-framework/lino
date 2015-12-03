from django.db.models import Q
from lino.api import dd


class Places(dd.Table):
    model = 'Place'


class Members(dd.Table):
    model = 'Member'
    column_names = "id name place email *"

    detail_layout = """
    id name place email mti_navigator
    """


class Customers(dd.Table):
    model = 'Customer'

    column_names = "id name place email customer_remark *"
    detail_layout = """
    id name place email mti_navigator
    customer_remark
    DemandsByCustomer
    """


class Suppliers(dd.Table):
    model = 'Supplier'

    column_names = "id name place email supplier_remark *"
    detail_layout = """
    id name place email mti_navigator
    supplier_remark
    OffersBySupplier
    """


class Products(dd.Table):
    model = 'Product'
    order_by = ['name']

    detail_layout = """
    id name
    OffersByProduct DemandsByProduct
    """

    column_names = 'id name'


class ActiveProducts(Products):
    
    label = "Active products"
    column_names = 'name offered_by demanded_by'

    @classmethod
    def get_request_queryset(cls, ar):
        # add filter condition to the queryset so that only "active"
        # products are shown, i.e. for which there is at least one
        # offer or one demand.
        qs = super(ActiveProducts, cls).get_request_queryset(ar)
        qs = qs.filter(Q(offer__isnull=False) | Q(demand__isnull=False))
        qs = qs.distinct()
        return qs


class Offers(dd.Table):
    model = 'Offer'
    column_names = "id supplier__name supplier__place " \
                   "supplier__email supplier__supplier_remark *"


class OffersBySupplier(Offers):
    master_key = 'supplier'


class OffersByProduct(Offers):
    master_key = 'product'


class Demands(dd.Table):
    model = 'Demand'


class DemandsByCustomer(Demands):
    master_key = 'customer'


class DemandsByProduct(Demands):
    master_key = 'product'
