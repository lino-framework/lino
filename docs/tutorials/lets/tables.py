from lino import dd


class Places(dd.Table):
    model = 'lets.Place'


class Members(dd.Table):
    model = 'lets.Member'

    detail_layout = """
    id name place email
    OffersByMember DemandsByMember
    """


class Products(dd.Table):
    model = 'lets.Product'

    detail_layout = """
    id name
    OffersByProduct DemandsByProduct
    """

    column_names = 'name offered_by demanded_by'


class Offers(dd.Table):
    model = 'lets.Offer'


class OffersByMember(Offers):
    master_key = 'provider'


class OffersByProduct(Offers):
    master_key = 'product'


class Demands(dd.Table):
    model = 'lets.Demand'


class DemandsByMember(Demands):
    master_key = 'customer'


class DemandsByProduct(Demands):
    master_key = 'product'
