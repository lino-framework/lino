# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds VAT rates (:mod:`lino.modlib.vat.models.VatRate`) for some
European countries.

"""

from lino.utils.instantiator import Instantiator
# from lino import rt
# from lino.modlib.vat.models import VatRegimes, VatClasses


def objects():
    rate = Instantiator(
        'vat.VatRate', 'vat_class country trade_type vat_regime rate')
    yield rate('exempt', None, None, None, 0)
    yield rate('reduced', 'BE', 'purchases', None, '0.07')
    yield rate('reduced', 'BE', 'sales', None, '0.07')
    yield rate('normal', 'BE', 'sales', None, '0.21')
    yield rate('reduced', 'EE', 'sales', None, '0.09')
    yield rate('normal', 'EE', 'sales', None, '0.20')

