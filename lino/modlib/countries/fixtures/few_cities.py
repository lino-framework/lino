# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Adds an arbitrary selection of a few demo cities.
"""

from __future__ import unicode_literals

import logging
from lino.modlib.countries.choicelists import PlaceType

logger = logging.getLogger(__name__)

from django.core.exceptions import MultipleObjectsReturned
from lino.utils import dblogger
from lino.core.utils import resolve_model
from lino.utils.instantiator import Instantiator
from lino import AFTER17

from lino.api import dd, rt


def objects():
    #~ dblogger.info("Installing countries few_cities fixture")
    countries = dd.resolve_app('countries')
    #~ Place = resolve_model('countries.Place')
    Place = countries.Place
    Country = countries.Country
    PlaceTypes = countries.PlaceTypes
    city = Instantiator(Place, 'name country').build

    def make_city(country_id, name=None, **kw):
        if False:  # AFTER17:
            kw.setdefault('type', PlaceTypes.city.pk)
            if kw.get('type',False) and isinstance(kw.get('type',False),PlaceType):
                kw['type'] = kw['type'].pk
        else:
            kw.setdefault('type', PlaceTypes.city)
        flt = rt.lookup_filter(
            'name', name, country__isocode=country_id, **kw)
        try:
            return Place.objects.get(flt)
            # return Place.objects.exclude(type__in=[
            #     PlaceTypes.county, PlaceTypes.province]).get(flt)
        except MultipleObjectsReturned:
            #~ qs = Place.objects.exclude(type=PlaceTypes.county).filter(country__isocode=country_id,name=name)
            raise Exception("Oops, there are multiple cities for %r", name)
        except Place.DoesNotExist:
            obj = city(name, country_id, **kw)
            obj.full_clean()
            obj.save()
            return obj

    BE = Country.objects.get(pk='BE')
    DE = Country.objects.get(pk='DE')
    FR = Country.objects.get(pk='FR')
    eupen = make_city('BE', 'Eupen', zip_code='4700')
    yield eupen
    yield make_city('BE', 'Nispert', type=PlaceTypes.township, parent=eupen)

    reuland = make_city('BE', 'Burg-Reuland ', zip_code='4790')
    yield make_city('BE', 'Ouren', type=PlaceTypes.township, parent=reuland)

    yield Place(country=BE, zip_code='4720', type=PlaceTypes.city,
                **dd.babel_values('name', de='Kelmis', fr='La Calamine',
                                  en="Kelmis", et="Kelmis"))
    yield make_city('BE', 'Kettenis', zip_code='4701', type=PlaceTypes.village)
    yield make_city('BE', 'Raeren', zip_code='4730', type=PlaceTypes.village)
    yield make_city('BE', 'Angleur', zip_code='4031')
    yield make_city('BE', 'Ans', zip_code='4430')
    yield make_city('BE', 'Ottignies', zip_code='1340')
    yield make_city('BE', 'Thieusies', zip_code='7061')
    yield make_city('BE', 'Cuesmes', zip_code='7033')
    yield make_city('BE', 'La Reid', zip_code='4910')
    yield make_city('BE', 'Blégny ', zip_code='4670')
    yield make_city('BE', 'Trembleur ', zip_code='4670')
    yield make_city('BE', 'Mortier ', zip_code='4670')
    yield make_city('BE', 'Cerfontaine', zip_code='5630')
    yield make_city('BE', 'Burdinne', zip_code='4210')

    def be_province(de, fr, nl):
        if False:  # AFTER17:
            p = Place(
                country=BE, type=PlaceTypes.province.pk,
                **dd.babel_values('name', de=de, fr=fr, nl=nl, en=fr, et=fr))
        else:
            p = Place(
            country=BE, type=PlaceTypes.province,
            **dd.babel_values('name', de=de, fr=fr, nl=nl, en=fr, et=fr))
        return p

    def be_city(zip_code, de=None, fr=None, nl=None, en=None, **kw):
        kw.update(dd.babel_values('name', de=de, fr=fr, nl=nl, en=en, et=en))
        if False:  # AFTER17:
            kw.setdefault('type', PlaceTypes.city.pk)
            if kw.get('type',False) and isinstance(kw.get('type',False),PlaceType):
                kw['type'] = kw['type'].pk
        else:
            kw.setdefault('type', PlaceTypes.city)
        return Place(country=BE, zip_code=zip_code, **kw)

    yield be_province("Antwerpen", "Anvers", "Antwerpen")
    yield be_province("Luxemburg", "Luxembourg", "Luxemburg")
    yield be_province("Namür", "Namur", "Namen")

    prov = be_province("Limburg", "Limbourg", "Limburg")
    yield prov
    yield make_city('BE', 'Aalst-bij-Sint-Truiden', zip_code='3800', parent=prov, type=PlaceTypes.village)

    prov = be_province("Lüttich", "Liège", "Luik")
    yield prov
    yield be_city('4000', "Lüttich", "Liège", "Luik", "Liège", parent=prov)
    yield be_city('4750', "Bütgenbach", "Butgenbach", "Butgenbach", "Butgenbach", parent=prov)
    yield be_city('4760', "Büllingen", "Bullange", "Büllingen", "Büllingen", parent=prov)
    yield be_city('4780', "Sankt Vith", "Saint-Vith", "Sankt Vith", "Sankt Vith", parent=prov)
    yield be_city('4780', "Recht", "Recht", "Recht", "Recht", parent=prov)
    yield be_city('4837', "Baelen", "Baelen", "Baelen", "Baelen", parent=prov)

    yield be_province("Hennegau", "Hainaut", "Henegouwen")
    yield be_province("Wallonisch-Brabant", "Brabant wallon", "Waals-Brabant")
    yield be_province("Flämisch-Brabant", "Brabant flamant", "Vlaams-Brabant")

    prov = be_province("Ostflandern", "Flandre de l'Est", "Oost-Vlaanderen")
    yield prov

    aalst = be_city('9300', "Aalst", "Alost", "Aalst", "Aalst", parent=prov)
    yield aalst
    yield be_city('9308', name="Gijzegem",
                  parent=aalst, type=PlaceTypes.village)
    yield be_city('9310', name="Baardegem ",
                  parent=aalst, type=PlaceTypes.village)
    yield be_city('9320', name="Erembodegem",
                  parent=aalst, type=PlaceTypes.village)
    yield be_city('9310', name="Herdersem", parent=aalst,
                  type=PlaceTypes.village)
    yield be_city('9308', name="Hofstade", parent=aalst,
                  type=PlaceTypes.village)
    yield be_city('9310', name="Meldert",
                  parent=aalst, type=PlaceTypes.village)
    yield be_city('9320', name="Nieuwerkerken",
                  parent=aalst, type=PlaceTypes.village)
    yield be_city('9310', name="Moorsel",
                  parent=aalst, type=PlaceTypes.village)

    yield be_province("Westflandern", "Flandre de l'Ouest", "West-Vlaanderen")

    yield be_city('1000', "Brüssel", "Bruxelles", "Brussel", "Brussels")
    yield be_city('7000', "Bergen", "Mons", "Bergen", "Mons")
    yield be_city('8400', "Ostende", "Ostende", "Oostende", "Ostende")
    yield be_city('5000', "Namür", "Namur", "Namen", "Namur")

    harjumaa = make_city('EE', 'Harju', type=PlaceTypes.county)
    yield harjumaa
    parnumaa = make_city('EE', 'Pärnu', type=PlaceTypes.county)
    yield parnumaa
    raplamaa = make_city('EE', 'Rapla', type=PlaceTypes.county)
    yield raplamaa

    yield make_city('EE', 'Vigala', type=PlaceTypes.municipality,
                    parent=raplamaa)
    yield make_city('EE', 'Rapla', type=PlaceTypes.town, parent=raplamaa)

    tallinn = make_city('EE', 'Tallinn', type=PlaceTypes.town, parent=harjumaa)
    yield tallinn
    yield make_city('EE', 'Kesklinn',
                    type=PlaceTypes.township, parent=tallinn)
    yield make_city('EE', 'Põhja-Tallinn',
                    type=PlaceTypes.township, parent=tallinn)

    yield make_city('EE', 'Pärnu', type=PlaceTypes.town, parent=parnumaa)
    yield make_city('EE', 'Tartu', type=PlaceTypes.town)
    yield make_city('EE', 'Narva', type=PlaceTypes.town)
    yield make_city('EE', 'Ääsmäe', type=PlaceTypes.town, parent=harjumaa)

    #~ yield make_city(u'Aachen','DE')
    yield Place(country=DE, type=PlaceTypes.city,
                **dd.babel_values('name', de='Aachen',
                               fr='Aix-la-Chapelle', nl="Aken",
                               en="Aachen", et="Aachen"))
    yield Place(country=DE, type=PlaceTypes.city,
                **dd.babel_values('name', de='Köln',
                               fr='Cologne', nl="Keulen",
                               en="Cologne", et="Köln"))
    yield make_city('DE', 'Berlin')
    yield make_city('DE', 'Hamburg')
    yield Place(country=DE, type=PlaceTypes.city,
                **dd.babel_values('name', de='München',
                               fr='Munich', en="Munich", et="München"))
    yield Place(country=DE, type=PlaceTypes.city,
                **dd.babel_values('name', de='Monschau',
                               fr='Montjoie', en="Monschau", et="Monschau"))

    yield make_city('NL', 'Maastricht')
    yield make_city('NL', 'Amsterdam')
    yield make_city('NL', 'Den Haag')
    yield make_city('NL', 'Rotterdam')
    yield make_city('NL', 'Utrecht')
    yield make_city('NL', 'Breda')

    yield Place(country=FR, type=PlaceTypes.city,
                **dd.babel_values('name', de='Paris', fr='Paris',
                               en="Paris", et="Pariis", nl="Parijs"))
    yield Place(country=FR, type=PlaceTypes.city,
                **dd.babel_values('name', de='Nizza',
                               fr='Nice', en="Nice", et="Nizza"))
    yield make_city('FR', 'Metz')
    yield make_city('FR', 'Strasbourg')
    yield make_city('FR', 'Nancy')
    yield make_city('FR', 'Marseille')
