# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
"""
from __future__ import unicode_literals

from lino.api import dd, rt
from lino.utils import i2d
Country = dd.resolve_model("countries.Country")
City = dd.resolve_model("countries.Place")
Type = dd.resolve_model("events.Type")
Event = dd.resolve_model("events.Event")
Stage = dd.resolve_model("events.Stage")
Place = dd.resolve_model("events.Place")
Feature = dd.resolve_model("events.Feature")

from lino.modlib.countries.models import PlaceTypes


def get_city(name):
    flt = rt.lookup_filter('name', name)
    try:
        return City.objects.exclude(
            type__in=[PlaceTypes.county, PlaceTypes.province]).get(flt)
    except City.DoesNotExist:
        raise Exception("No city named %r" % name)


def event(type, date, name, name_nl, name_fr, *features, **kw):
    #~ features = [f.pk for f in features]
    cities = kw.pop('cities', None)
    e = Event(type=type, date=i2d(date), name=name,
              name_nl=name_nl, name_fr=name_fr, **kw)
    e.full_clean()
    e.save()
    if features:
        e.features = features
    if cities:
        for name in cities:
            stage = Stage(event=e, city=get_city(name))
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
    # raeren = City.objects.get(name="Raeren")
    eupen = City.objects.get(name="Eupen")
    # ottignies = City.objects.get(name="Ottignies")
    # ans = City.objects.get(name="Ans")
    bbach = City.objects.get(name="Bütgenbach")
    # bullingen = City.objects.get(name="Büllingen")
    stvith = City.objects.get(name="Sankt Vith")
    # monschau = City.objects.get(name="Montjoie")

    yield City(name="Lontzen", country=BE)
    yield City(name="Dinant", country=BE)
    yield City(name="Erezée", country=BE)

    #~ stvith = City(name="Sankt Vith",name_fr="Saint-Vith",country=BE)
    #~ yield stvith
    #~ monschau = City(name="Monschau",name_fr="Montjoie",country=DE)
    #~ yield monschau

    #~ bullingen = City(name="Büllingen",name_fr="Bullange",country=BE)
    #~ yield bullingen

    #~ bbach = City(name="Bütgenbach",name_fr="Butgenbach",country=BE)
    #~ yield bbach

    irmep = Place(name="IRMEP-Kaserne", name_fr="Caserne IRMEP", city=eupen)
    yield irmep

    domaine = Place(name="Zur Domäne", name_fr="«Zur Domäne»", city=bbach)
    yield domaine

    triangel = Place(name="Triangel", city=stvith)
    yield triangel

    galmei = Place(name="Galmeiplatz (Koul-Gelände)",
                   name_fr="Place Galmei (domaine «Koul»)", city=kelmis)
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
    f4 = Feature(
        name="Radtag der DG",
        name_nl="Fietsdag van de DG",
        name_fr="Journée vélo de la CG")
    yield f4

    # 2013

    yield event(breitensport, 20130324,
                "18\. Bike-Day  IRMEP-RSK Eupen",
                "18\. Bike-Day  IRMEP-RSK Eupen",
                "18e Bike-Day de l'IRMEP-RSK Eupen",
                f1, f2, place=irmep)
    yield event(breitensport, 20130505,
                "24\. Eifel-Biker event",
                "24\. Eifel-Biker event",
                "24e event des Eifel-Bikers",
                f1, f2, place=domaine)
    yield event(breitensport, 20130706,
                "Internationale 3 Länderfahrt",
                "Internationale 3 Länderfahrt",
                "Randonnée internationale des 3 frontières",
                f3, f2, place=triangel)
    yield event(breitensport, 20130901,
                "Radtag der DG",
                "Fietsdag van de DG",
                "Journée vélo de la CG", f3, f2,
                place=galmei, url="http://www.vclc.be")

    yield event(strasse, 20130510,
                "1\. Etappe des Triptyque Ardennais",
                "1\. etappe Triptyque Ardennais",
                "1e étape du Triptyque Ardennais",
                cities=["Raeren", "Büllingen"])

    yield event(strasse, 20130511,
                "2\. Etappe des Triptyque Ardennais",
                "2\. etappe Triptyque Ardennais",
                "2e étape du Triptyque Ardennais",
                cities=["Monschau", "Eupen"])

    yield event(strasse, 20130720,
                "Etappenankunft Tour de la Région Wallonne (TRW)",
                "Aankomst etappe Tour de la Région Wallonne (TRW)",
                "Arrivée d'étape du Tour de la Région Wallonne (TRW)",
                cities=["Ans", "Eupen"])

    yield event(trophy, 20130316, '', '', '', cities=["Ottignies"])
    yield event(trophy, 20130323, '', '', '', cities=["Thieusies"])
    yield event(trophy, 20130427, '', '', '', cities=["Cuesmes"])
    yield event(trophy, 20130505, '', '', '', cities=["Bütgenbach"])
    yield event(trophy, 20130519, '', '', '', cities=["La Reid"])
    yield event(trophy, 20130525, '', '', '', cities=["Eupen"])
    yield event(trophy, 20130706, '', '', '', cities=["Sankt Vith"])
    #~ yield event(trophy,20130713,'','','',cities=["Ouren"])
    yield event(trophy, 20130824, '', '', '', cities=["Blégny"])
    yield event(trophy, 20130901, '', '', '', cities=["Kelmis"],
                url="http://www.vclc.be")
    yield event(trophy, 20130914, '', '', '', cities=["Cerfontaine"])
    yield event(trophy, 20130921, '', '', '', cities=["Burdinne"])

    yield event(mtb, 20130526,
                "Merida Cup – 5\. Lauf",
                "Merida Cup – 5de manche",
                "Merida Cup – 5e manche",
                cities=["Eupen"])
    yield event(mtb, 20130706,
                "UCI 2 MTB Rennen",
                "UCI 2 MTB koers",
                "Course MTB UCI 2",
                cities=["Sankt Vith"])
    #~ yield event(mtb,20130714,
      #~ 'Merida Cup – 6\. Lauf',
      #~ "Merida Cup – 6de manche",
      #~ "Merida Cup – 6e manche",
      #~ cities=["Ouren"])

    yield event(breitensport, 20140323,
                "19\. Bike-Day  IRMEP-RSK Eupen",
                "19\. Bike-Day  IRMEP-RSK Eupen",
                "19e Bike-Day de l'IRMEP-RSK Eupen",
                f1, f2, f4, place=irmep)
    yield event(breitensport, 20140504,
                "25\. Eifel-Biker event",
                "25\. Eifel-Biker event",
                "25e event des Eifel-Bikers",
                f1, f2, f4, place=domaine)
                # url="http://www.eifel-biker.be")
    yield event(breitensport, 20140605,
                "Internationale Dreiländerfahrt",
                "Internationale Drielandentocht",
                "Randonnée internationale des trois frontières",
                f3, f2, f4, place=triangel)
                # url="http://www.rsv.be/dreilanderfahrt-2")
    yield event(breitensport, 20140518,
                "Radtag der DG",
                "Fietsdag van de DG",
                "Journée vélo de la CG", f3, f2,  
                place=galmei, url="")

    yield event(strasse, 20140523,
                "1\. Etappe des Triptyque Ardennais",
                "1\. etappe Triptyque Ardennais",
                "1e étape du Triptyque Ardennais",
                cities=["Kelmis", "Büllingen", "Raeren"])
                # url="http://www.cchawy.be/")

    yield event(strasse, 20140524,
                "2\. Etappe des Triptyque Ardennais",
                "2\. etappe Triptyque Ardennais",
                "2e étape du Triptyque Ardennais",
                cities=["Bütgenbach", "Eupen", "Lontzen"])
                # url="http://www.cchawy.be/")

    yield event(mtb, 20140705,
                "UCI 2 MTB Rennen",
                "UCI 2 MTB koers",
                "Course MTB UCI 2",
                cities=["Sankt Vith"])
    yield event(mtb, 20140907,
                'Wallonia Cup – 6\. Lauf',
                "Wallonia Cup – 6de manche",
                "Wallonia Cup – 6e manche",
                cities=["Eupen"])

    yield event(trophy, 20140315, '', '', '', cities=["Dinant"])
    yield event(trophy, 20140322, '', '', '', cities=["Thieusies"])
    yield event(trophy, 20140426, '', '', '', cities=["Cuesmes"])
    yield event(trophy, 20140518, '', '', '', cities=["Kelmis"])
    yield event(trophy, 20140531, '', '', '', cities=["Erezée"])
    yield event(trophy, 20140608, '', '', '', cities=["La Reid"])
    yield event(trophy, 20140705, '', '', '', cities=["Sankt Vith"])
    yield event(trophy, 20140823, '', '', '', cities=["Blégny"])
    yield event(trophy, 20140906, '', '', '', cities=["Eupen"])
    yield event(trophy, 20140913, '', '', '', cities=["Cerfontaine"])
    yield event(trophy, 20140920, '', '', '', cities=["Burdinne"])
