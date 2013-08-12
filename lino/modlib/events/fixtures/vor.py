# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
"""
from __future__ import unicode_literals

from lino import dd
from lino.utils import i2d
from north import dbutils
Country = dd.resolve_model("countries.Country")
City = dd.resolve_model("countries.City")
Type = dd.resolve_model("events.Type")
Event = dd.resolve_model("events.Event")
Stage = dd.resolve_model("events.Stage")
Place = dd.resolve_model("events.Place")
Feature = dd.resolve_model("events.Feature")

from lino.modlib.countries.models import CityTypes

def get_city(name):
    flt = dbutils.lookup_filter('name',name)
    try:
        return City.objects.exclude(
            type__in=[CityTypes.county,CityTypes.province]).get(flt)
    except City.DoesNotExist:
        raise Exception("No city named %r" % name)
    
def event(type,date,name,name_nl,name_fr,*features,**kw):
    #~ features = [f.pk for f in features]
    cities = kw.pop('cities',None)
    e = Event(type=type,date=i2d(date),name=name,name_nl=name_nl,name_fr=name_fr,**kw)
    e.full_clean()
    e.save()
    if features:
        e.features=features
    if cities:
        for name in cities:
            stage = Stage(event=e,city=get_city(name))
            stage.full_clean()
            stage.save()
        #~ e.cities = [get_city(n) for n in cities]
    return e
    
def objects():
    BE = Country.objects.get(pk='BE')
    DE = Country.objects.get(pk='DE')
    #~ u = User(username='root')
    #~ yield u
    
    breitensport = Type(
        name="Breitensport",
        name_nl="Sport voor allen",
        name_fr="Sport pour tous")
    yield breitensport
    
    strasse = Type(
      name="Radrennen Straße",
      name_nl="Koersen op de weg",
      name_fr="Courses sur route")
    yield strasse
    
    mtb = Type(
      name="MTB Rennen ≥ 15-jährige",
      name_nl="MTB koersen ≥ 15 jaarige",
      name_fr="Courses Mountain Bike pour ≥ 15 ans")
    yield mtb
    
    trophy = Type(
        name="Mountainbike Rennsport -- Kids Trophy O2 Biker/V.O.R.-Lotto",
        name_nl="Mountainbike koersen -- Kids Trophy O2 Biker/V.O.R.-Lotto",
        name_fr="Courses Mountain Bike -- Kids Trophy O2 Biker/V.O.R.-Lotto",
        events_column_names="when:40 where:40"
        )
    yield trophy
    
    kelmis = City.objects.get(name="Kelmis")
    raeren = City.objects.get(name="Raeren")
    eupen = City.objects.get(name="Eupen")
    ottignies = City.objects.get(name="Ottignies")
    #~ ans = City.objects.get(name="Ans")
    bbach = City.objects.get(name="Bütgenbach")
    bullingen = City.objects.get(name="Büllingen")
    stvith = City.objects.get(name="Sankt Vith")
    #~ monschau = City.objects.get(name="Montjoie")
    
    #~ stvith = City(name="Sankt Vith",name_fr="Saint-Vith",country=BE)
    #~ yield stvith
    #~ monschau = City(name="Monschau",name_fr="Montjoie",country=DE)
    #~ yield monschau
    
    #~ bullingen = City(name="Büllingen",name_fr="Bullange",country=BE)
    #~ yield bullingen
    
    #~ bbach = City(name="Bütgenbach",name_fr="Butgenbach",country=BE)
    #~ yield bbach
    
    
    
    irmep = Place(name="IRMEP-Kaserne",name_fr="Caserne IRMEP",city=eupen)
    yield irmep
    
    domaine = Place(name="Zur Domäne",name_fr="«Zur Domäne»",city=bbach)
    yield domaine
    
    triangel = Place(name="Triangel",city=stvith)
    yield triangel
    
    galmei = Place(name="Galmeiplatz (Koul-Gelände)",
        name_fr="Place Galmei (domaine «Koul»)",city=kelmis)
    yield galmei
    
    
    f1 = Feature(name="Mountain-Bike-Ausfahrt",
        name_nl="Mountain Bike tocht",
        name_fr="Sortie Mountain Bike")
    yield f1
    f2 = Feature(name="Volksradfahren",
        name_nl="Recreatiev fietsen",
        name_fr="Cyclisme récréatif")
    yield f2
    f3 = Feature(
        name="Straße- und Mountain Bike Touren",
        name_nl="Straße- und Mountain Bike Touren",
        name_fr="Randonnées route et Mountain Bike")
    yield f3
    
    
    yield event(breitensport,20130324,
      "18\. Bike-Day  IRMEP-RSK Eupen",
      "18\. Bike-Day  IRMEP-RSK Eupen",
      "18e Bike-Day de l'IRMEP-RSK Eupen",
      f1,f2,place=irmep)
    yield event(breitensport,20130505,
      "24\. Eifel-Biker event",
      "24\. Eifel-Biker event",
      "24e event des Eifel-Bikers",
      f1,f2,place=domaine)
    yield event(breitensport,20130706,
      "Internationale 3 Länderfahrt", 
      "Internationale 3 Länderfahrt", 
      "Randonnée internationale des 3 frontières", 
      f3,f2,place=triangel)
    yield event(breitensport,20130901,
      "Radtag der DG",
      "Fietsdag van de DG",
      "Journée vélo de la CG", f3,f2,
      place=galmei,url="http://www.vclc.be")
      
      
      
    yield event(strasse,20130510,
      "1\. Etappe des Triptyque Ardennais",
      "1\. etappe Triptyque Ardennais",
      "1e étape du Triptyque Ardennais",
      cities=["Raeren","Büllingen"])
      
    yield event(strasse,20130511,
      "2\. Etappe des Triptyque Ardennais",
      "2\. etappe Triptyque Ardennais",
      "2e étape du Triptyque Ardennais",
      cities=["Monschau","Eupen"])
      
    yield event(strasse,20130720,
      "Etappenankunft Tour de la Région Wallonne (TRW)",
      "Aankomst etappe Tour de la Région Wallonne (TRW)",
      "Arrivée d'étape du Tour de la Région Wallonne (TRW)",
      cities=["Ans","Eupen"])
      
      
    yield event(trophy,20130316,'','','',cities=["Ottignies"])
    yield event(trophy,20130323,'','','',cities=["Thieusies"])
    yield event(trophy,20130427,'','','',cities=["Cuesmes"])
    yield event(trophy,20130505,'','','',cities=["Bütgenbach"])
    yield event(trophy,20130519,'','','',cities=["La Reid"])
    yield event(trophy,20130525,'','','',cities=["Eupen"])
    yield event(trophy,20130706,'','','',cities=["Sankt Vith"])
    #~ yield event(trophy,20130713,'','','',cities=["Ouren"])
    yield event(trophy,20130824,'','','',cities=["Blégny"])
    yield event(trophy,20130901,'','','',cities=["Kelmis"],url="http://www.vclc.be")
    yield event(trophy,20130914,'','','',cities=["Cerfontaine"])
    yield event(trophy,20130921,'','','',cities=["Burdinne"])
    
    yield event(mtb,20130526,
      "Merida Cup – 5\. Lauf",
      "Merida Cup – 5de manche",
      "Merida Cup – 5e manche",
      cities=["Eupen"])
    yield event(mtb,20130706,
      "UCI 2 MTB Rennen",
      "UCI 2 MTB koers",
      "Course MTB UCI 2",
      cities=["Sankt Vith"])
    #~ yield event(mtb,20130714,
      #~ 'Merida Cup – 6\. Lauf',
      #~ "Merida Cup – 6de manche",
      #~ "Merida Cup – 6e manche",
      #~ cities=["Ouren"])
      
      
