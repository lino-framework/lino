# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Orders")

    def setup_main_menu(config, site, profile, m):
        m = m.add_menu(vat.TradeTypes.sales.name, vat.TradeTypes.sales.text)
        m.add_action(Orders)

    def setup_config_menu(config, site, profile, m):
        m = m.add_menu("sales", MODULE_LABEL)
        m.add_action(InvoicingModes)
        m.add_action(ShippingModes)
        m.add_action(PaymentTerms)

        
