# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Choicelists for `lino.modlib.countries`.

.. autosummary::

"""
from __future__ import unicode_literals
from builtins import object


from lino.api import dd, rt
from django.utils.translation import ugettext_lazy as _


class PlaceType(dd.Choice):

    def find(self, name):
        M = rt.modules.countries.Place
        try:
            return M.objects.get(type=self, name=name)
        except M.DoesNotExist:
            raise Exception("No %s named %s" % (self, name))


class PlaceTypes(dd.ChoiceList):
    """
    A choicelist of possible place types.

    .. django2rst::

            rt.show(countries.PlaceTypes)


    Sources used:

    - http://en.wikipedia.org/wiki/List_of_subnational_entities

    """
    verbose_name = _("Place Type")
    item_class = PlaceType

add = PlaceTypes.add_item
# ~ add('10', pgettext_lazy(u'countries','State'))             # de:Bundesland
add('10', _('Member State'))      # de:Bundesland
add('11', _('Division'))
add('12', _('Region'))
add('13', _('Community'))            # fr:Communauté de: Gemeinschaft
add('14', _('Territory'))
# ~ add('15', _('City-state'))        # et:Linnriik  de:Stadtstaat  fr:Cité-État

add('20', _('County'), 'county')      # et:maakond   de:Regierungsbezirk
add('21', _('Province'), 'province')
add('22', _('Shire'))
add('23', _('Subregion'))
add('24', _('Department'))
add('25', _('Arrondissement'))
add('26', _('Prefecture'))
add('27', _('District'), 'district')
add('28', _('Sector'))                      # de:Kreis

add('50', _('City'), 'city')              # et:suurlinn  de:Stadt
add('51', _('Town'), 'town')              # et:linn      de:Kleinstadt
add('52', _('Municipality'), 'municipality')  # et:vald de:Gemeinde fr:Commune
add('54', _('Parish'), 'parish')           # de:Pfarre fr:Paroisse
add('55', _('Township'), 'township')       # de:Stadtteil fr:?, et: linnaosa
add('56', _('Quarter'), 'quarter')           # de:Viertel fr:Quartier

add('61', _('Borough'), 'borough')           # et:alev
add('62', _('Small borough'), 'smallborough')     # et:alevik

add('70', _('Village'), 'village')           # et:küla


class CountryDriver(object):

    def __init__(self, region_types, city_types):
        self.region_types = [PlaceTypes.get_by_value(v)
                             for v in region_types.split()]
        self.city_types = [PlaceTypes.get_by_value(v)
                           for v in city_types.split()]

    def is_region(self, p):
        return p and p.type and p.type in self.region_types


class CountryDrivers(object):
    BE = CountryDriver('21', '50 70')
    EE = CountryDriver('20', '50 51 52 55 61 62 70')
    DE = CountryDriver('10', '50 51 52 70')
    FR = CountryDriver('24', '50 51 52 70')


