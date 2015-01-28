# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds VAT rules (:mod:`lino.modlib.vat.models.VatRule`) for some
European countries.

"""

# from lino.utils.instantiator import Instantiator
from lino.api import rt


def objects():
    Country = rt.modules.countries.Country
    # VatRule = rt.modules.vat.VatRule
    vat = rt.modules.vat

    def rule(vat_class, country_id, vat_regime, rate):
        if country_id is None:
            country = None
        else:
            try:
                country = Country.objects.get(pk=country_id)
            except Country.DoesNotExist:
                raise Exception("No country {0}".format(country_id))
        return vat.VatRule(
            country=country,
            vat_class=vat.VatClasses.get_by_name(vat_class),
            # trade_type=vat.TradeTypes.get_by_name(trade_type),
            vat_regime=vat.VatRegimes.get_by_name(vat_regime),
            rate=rate)
    # rule = Instantiator(
    #     'vat.VatRule', 'vat_class country trade_type vat_regime rate')
    yield rule('exempt', None, None, 0)
    yield rule('reduced', 'BE', None, '0.07')
    yield rule('normal', 'BE', None, '0.21')
    yield rule('normal', 'EE', None, '0.20')
    yield rule('reduced', 'EE', None, '0.09')
    yield rule('normal', 'NL', None, '0.21')
    yield rule('reduced', 'NL', None, '0.06')
    yield rule('normal', 'DE', None, '0.19')
    yield rule('reduced', 'DE', None, '0.07')
    yield rule('normal', 'FR', None, '0.20')
    yield rule('reduced', 'FR', None, '0.10')
    # in FR there are more VAT classes, we currently don't support them
    # yield rule('reduced', 'FR', None, None, '0.055')
    # yield rule('reduced', 'FR', None, None, '0.021')

