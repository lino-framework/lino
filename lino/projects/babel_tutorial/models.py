from builtins import object
from lino.api import dd
from lino import mixins
from django.utils.translation import ugettext_lazy as _


class Categories(dd.ChoiceList):
    verbose_name = _("Category")
    verbose_name_plural = _("Categories")

Categories.add_item("01", _("Hardware"), 'hardware')
Categories.add_item("02", _("Service"), 'service')
Categories.add_item("03", _("Accessories"), 'accessories')
Categories.add_item("04", _("Software"), 'software')


class Product(mixins.BabelNamed):

    price = dd.PriceField(_("Price"), blank=True, null=True)

    category = Categories.field(blank=True, null=True)

    class Meta(object):
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Products(dd.Table):
    model = Product
    sort_order = ['name']
    column_names = "name category price *"
    auto_fit_column_widths = True

    detail_layout = """
    id price category
    name
    """

    insert_layout = dd.FormLayout("""
    name
    category price
    """, window_size=(40, 'auto'))


