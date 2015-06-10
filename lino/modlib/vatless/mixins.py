# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for `lino.modlib.vatless`.


"""


from lino.api import dd


class PartnerDetailMixin(dd.DetailLayout):
    """Defines a panel :attr:`ledger`, to be added as a tab panel to your
    layout's `main` element.

    .. attribute:: ledger

        Shows the tables `vatless.VouchersByPartner` and
        `ledger.MovementsByPartner`.

    """
    if dd.is_installed('ledger'):
        ledger = dd.Panel("""
        vatless.VouchersByPartner
        ledger.MovementsByPartner
        """, label=dd.plugins.ledger.verbose_name)
    else:
        ledger = dd.DummyPanel()
