# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.
"""
Adds an arbitrary selection of a few demo cities.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import MultipleObjectsReturned
from lino.utils import dblogger
from north import dbutils
from lino.core.dbutils import resolve_model
from lino.utils.instantiator import Instantiator
from north.dbutils import babel_values


from lino import dd

def objects():
    #~ dblogger.info("Installing countries few_cities fixture")
    countries = dd.resolve_app('countries')
    #~ City = resolve_model('countries.City')
    City = countries.City
    Country = countries.Country
    CityTypes = countries.CityTypes
    city = Instantiator(City,'name country').build
    def make_city(country_id,name=None,**kw):
        kw.setdefault('type',CityTypes.city)
        #~ kw.update()
        #~ if name:
            #~ kw.update(name=name)
        flt = dbutils.lookup_filter('name',name,country__isocode=country_id,**kw)
        try:
            return City.objects.exclude(type__in=[CityTypes.county,CityTypes.province]).get(flt)
            #~ return City.objects.exclude(type=CityTypes.county).get(
                #~ country__isocode=country_id,name=name)
        except MultipleObjectsReturned:
            #~ qs = City.objects.exclude(type=CityTypes.county).filter(country__isocode=country_id,name=name)
            logger.info("Oops, there are multiple cities for %r", name)
            return qs[0]
        except City.DoesNotExist:
            return city(name,country_id,**kw)
        
    BE = Country.objects.get(pk='BE')
    DE = Country.objects.get(pk='DE')
    FR = Country.objects.get(pk='FR')
    eupen = make_city('BE','Eupen',zip_code='4700')
    yield eupen
    yield make_city('BE','Nispert',type=CityTypes.township,parent=eupen)
    
    reuland = make_city('BE','Burg-Reuland ',zip_code='4790')
    yield make_city('BE','Ouren',type=CityTypes.township,parent=reuland)
    
    yield City(country=BE,zip_code='4720',type=CityTypes.city,
      **babel_values('name',de='Kelmis',fr='La Calamine',en="Kelmis"))
    yield make_city('BE','Kettenis',zip_code='4701',type=CityTypes.village)
    yield make_city('BE','Raeren',zip_code='4730',type=CityTypes.village)
    yield make_city('BE','Angleur',zip_code='4031')
    yield make_city('BE','Ans',zip_code='4430')
    yield make_city('BE','Ottignies',zip_code='1340')
    yield make_city('BE','Thieusies',zip_code='7061')
    yield make_city('BE','Cuesmes',zip_code='7033')
    yield make_city('BE','La Reid',zip_code='4910')
    yield make_city('BE','Blégny ',zip_code='4670')
    yield make_city('BE','Cerfontaine',zip_code='5630')
    yield make_city('BE','Burdinne',zip_code='4210')
    
    
    def be_province(de,fr,nl):
        return City(country=BE,type=CityTypes.province,
            **babel_values('name',de=de,fr=fr,nl=nl,en=fr))
    
    def be_city(zip_code,de,fr,nl,en,**kw):
        kw.update(babel_values('name',de=de,fr=fr,nl=nl,en=en))
        return City(country=BE,zip_code=zip_code,type=CityTypes.city,**kw)
            
    yield be_province("Antwerpen","Anvers","Antwerpen")
    yield be_province("Luxemburg","Luxembourg","Luxemburg")
    yield be_province("Limburg","Limbourg","Limburg")
    yield be_province("Namür","Namur","Namen")
    
    prov = be_province("Lüttich","Liège","Luik")
    yield prov
    yield be_city('4000',"Lüttich","Liège","Luik","Liège",parent=prov)
    yield be_city('4750',"Bütgenbach","Butgenbach","Butgenbach","Butgenbach",parent=prov)
    yield be_city('4760',"Büllingen","Bullange","Büllingen","Büllingen",parent=prov)
    yield be_city('4780',"Sankt Vith","Saint-Vith","Sankt Vith","Sankt Vith",parent=prov)
    yield be_city('4780',"Recht","Recht","Recht","Recht",parent=prov)
    
    yield be_province("Hennegau","Hainaut","Henegouwen")
    yield be_province("Wallonisch-Brabant","Brabant wallon","Waals-Brabant")
    yield be_province("Flämisch-Brabant","Brabant flamant","Vlaams-Brabant")
    yield be_province("Ostflandern","Flandre de l'Est","Oost-Vlaanderen")
    yield be_province("Westflandern","Flandre de l'Ouest","West-Vlaanderen")
    
    yield be_city('1000',"Brüssel","Bruxelles","Brussel","Brussels")
    yield be_city('7000',"Bergen","Mons","Bergen","Mons")
    yield be_city('8400',"Ostende","Ostende","Oostende","Ostende")
    yield be_city('5000',"Namür","Namur","Namen","Namur")
    
    harjumaa = make_city('EE','Harjumaa',type=CityTypes.county)
    yield harjumaa
    parnumaa = make_city('EE','Pärnumaa',type=CityTypes.county)
    yield parnumaa
    raplamaa = make_city('EE','Raplamaa',type=CityTypes.county)
    yield raplamaa
    
    yield make_city('EE','Vigala',type=CityTypes.municipality,parent=raplamaa)
    yield make_city('EE','Rapla',type=CityTypes.town,parent=raplamaa)
    
    yield make_city('EE','Tallinn',type=CityTypes.city,parent=harjumaa)
    yield make_city('EE','Pärnu',type=CityTypes.town,parent=parnumaa)
    yield make_city('EE','Tartu',type=CityTypes.town)
    yield make_city('EE','Narva',type=CityTypes.town)
    yield make_city('EE','Ääsmäe',type=CityTypes.town,parent=harjumaa)

    #~ yield make_city(u'Aachen','DE')
    yield City(country=DE,type=CityTypes.city,
      **babel_values('name',de='Aachen',fr='Aix-la-Chapelle',nl="Aken",en="Aachen"))
    yield City(country=DE,type=CityTypes.city,
      **babel_values('name',de='Köln',fr='Cologne',nl="Keulen",en="Cologne"))
    yield make_city('DE','Berlin')
    yield make_city('DE','Hamburg')
    yield City(country=DE,type=CityTypes.city,
      **babel_values('name',de='München',fr='Munich',en="Munich"))
    yield City(country=DE,type=CityTypes.city,
      **babel_values('name',de='Monschau',fr='Montjoie',en="Monschau"))
    
    yield make_city('NL','Maastricht')
    yield make_city('NL','Amsterdam')
    yield make_city('NL','Den Haag')
    yield make_city('NL','Rotterdam')
    yield make_city('NL','Utrecht')
    yield make_city('NL','Breda')
    
    yield City(country=FR,type=CityTypes.city,
      **babel_values('name',de='Paris',fr='Paris',en="Paris",et="Pariis",nl="Parijs"))
    yield City(country=FR,type=CityTypes.city,
      **babel_values('name',de='Nizza',fr='Nice',en="Nice"))
    yield make_city('FR','Metz')
    yield make_city('FR','Strasbourg')
    yield make_city('FR','Nancy')
    yield make_city('FR','Marseille')
