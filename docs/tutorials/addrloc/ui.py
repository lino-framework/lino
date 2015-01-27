from lino.api import dd


class Companies(dd.Table):
    model = 'Company'
    column_names = 'name address_column *'
    detail_layout = dd.DetailLayout("""
    id name
    addr1
    street_prefix street street_no street_box
    addr2""", window_size=(50, 'auto'))
