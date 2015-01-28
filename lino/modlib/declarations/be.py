# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Belgian VAT declaration fields.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal

from django.db import models
from django.conf import settings

from lino.api import dd, rt
from lino import mixins
#~ from lino.core.utils import full_model_name
#~ from lino.utils.choicelists import ChoiceList
#contacts = reports.get_app('contacts')
#~ from lino.modlib.journals import models as journals
#~ journals = reports.get_app('journals')
#from lino.modlib.contacts import models as contacts
#from lino.modlib.journals import models as journals
from django.utils.translation import ugettext_lazy as _
#~ from lino.modlib.accounts.utils import AccountTypes


class DeclarationField(dd.Choice):

    def amount_for_field(fld, dcl, mvt, jnl):
        tt = jnl.trade_type
        if not tt:
            return
        if not fld.name.startswith(tt.name):
            return
        #~ if tt.name == 'sales':
        if fld.name.endswith("_base"):
            return mvt.amount
        if fld.name.endswith("_vat"):
            return mvt.amount
        #~ if fld.value == '80':
            #~ if item.vat_class == VatClasses.
            #~ if item.get_base_account().type == AccountTypes.invest
            #~ return item.total_base


class PurchaseBaseField(dd.Choice):

    def __init__(self, selector, *args, **kw):
        self.selector = selector
        super(PurchaseBaseField, self).__init__(*args, **kw)

    def amount_for_field(fld, dcl, mvt, jnl):
        return None


class DeclarationFields(dd.ChoiceList):

    item_class = DeclarationField

    fields_layout = dd.Panel("""
    sales_base sales_vat
    purchases_base purchases_vat
    purchases_investments purchases_ware purchases_services
    """)

add = DeclarationFields.add_item
add("00", _("Sales base"), "sales_base")
add("10", _("Sales VAT"), "sales_vat")
add("20", _("Purchases base"), "purchases_base")
add("30", _("Purchases VAT"), "purchases_vat")

add = DeclarationFields.add_item_instance
add(PurchaseBaseField("80", "80", _("Investments"), 'purchases_investments'))
add(PurchaseBaseField("81", "81", _("Ware"), 'purchases_ware'))
add(PurchaseBaseField("82", "82", _("Services"), 'purchases_services'))
