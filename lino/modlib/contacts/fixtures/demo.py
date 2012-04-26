# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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

from django.conf import settings
from lino.tools import resolve_model
from lino.utils.instantiator import Instantiator
from lino.utils.babel import default_language
from lino.utils.choicelists import Gender
from lino.utils import dblogger
#from lino import reports
#contacts = reports.get_app('contacts')

def objects():
    #~ dblogger.info("Installing contacts demo fixture") # use --verbosity=2
    
    company = Instantiator(settings.LINO.company_model,"name zip_code city:name street street_no",country='EE').build
    yield company(u'Rumma & Ko OÜ','10115','Tallinn',u'Tartu mnt','71')
    
    company = Instantiator(settings.LINO.company_model,"name zip_code city:name street street_no",country='BE').build
    yield company(u'Bäckerei Ausdemwald', '4700', 'Eupen',  u'Vervierser Straße','45')
    yield company(u'Bäckerei Mießen',     '4700', 'Eupen',  u'Gospert','103')
    yield company(u'Bäckerei Schmitz',    '4700', 'Eupen',  u'Aachener Straße','53')
    yield company(u'Garage Mergelsberg',  '4720', 'Kelmis', u'Kasinostraße','13')
    
    company = Instantiator(settings.LINO.company_model,"name zip_code city:name street street_no",country='NL').build
    yield company(u'Donderweer BV','4816 AR','Breda', 'Edisonstraat','12')
    yield company(u'Van Achter NV','4836 LG','Breda', 'Hazeldonk','2')
    
    company = Instantiator(settings.LINO.company_model,"name zip_code city:name street street_no",country='DE').build
    yield company(u'Hans Flott & Co','22453','Hamburg',u'Niendorfer Weg','532')
    yield company(u'Bernd Brechts Bücherladen','80333',u'München',u'Brienner Straße','18')
    yield company(u'Reinhards Baumschule','12487 ',u'Berlin',u'Segelfliegerdamm','123')
    
    company = Instantiator(settings.LINO.company_model,"name zip_code city:name street street_no",country='FR').build
    yield company(u'Moulin Rouge','75018','Paris',u'Boulevard de Clichy','82')
    yield company(u'Auto École Verte','54000 ','Nancy',u'rue de Mon Désert','12')
    
    City = resolve_model('countries.City')
    vigala = City.objects.get(name__exact='Vigala')
    #~ tallinn = City.objects.get(name__exact='Tallinn')
    person = Instantiator(settings.LINO.person_model,"first_name last_name",
                country='EE',street='Uus', street_no='1',
                addr2=u'Vana-Vigala küla',
                city=vigala,zip_code='78003').build
    yield person(u'Luc',  u'Saffre', gender=Gender.male,birth_date='1968-06-01')
    
    eupen = City.objects.get(name__exact='Eupen')
    person = Instantiator(settings.LINO.person_model,"first_name last_name",
                country='BE',city=eupen,zip_code='4700').build
    yield person(u'Andreas',  u'Arens',gender=Gender.male)
    yield person(u'Annette',  u'Arens',gender=Gender.female)
    yield person(u'Hans',     u'Altenberg',gender=Gender.male)
    yield person(u'Alfons',   u'Ausdemwald',gender=Gender.male)
    yield person(u'Laurent',  u'Bastiaensen',gender=Gender.male)
    yield person(u'Charlotte',  u'Collard',gender=Gender.female)
    yield person(u'Ulrike',  u'Charlier',gender=Gender.female)
    yield person(u'Marc',  u'Chantraine',gender=Gender.male)
    yield person(u'Daniel',   u'Dericum',gender=Gender.male)
    yield person(u'Dorothée', u'Demeulenaere',gender=Gender.female)
    yield person(u'Berta',    u'Ernst',gender=Gender.female)
    yield person(u'Bernd',    u'Evertz',gender=Gender.male)
    yield person(u'Eberhart', u'Evers',gender=Gender.male)
    yield person(u'Daniel',   u'Emonts',gender=Gender.male)
    yield person(u'Edgar',    u'Engels',gender=Gender.male)
    yield person(u'Luc',      u'Faymonville',gender=Gender.male)
    yield person(u'Gérard',   u'Gernegroß',gender=Gender.male)
    yield person(u'Werner',   u'Groteclaes',gender=Gender.male)
    yield person(u'Grete',    u'Hilgers',gender=Gender.female)
    yield person(u'Hans',     u'Hilgers',gender=Gender.male)
    yield person(u'Irene',    u'Ingels',gender=Gender.female)
    yield person(u'Jérémy',   u'Jansen',gender=Gender.male)
    yield person(u'Jean-Pierre', u'Jacob',gender=Gender.male)
    yield person(u'Herbert', u'Johnen',gender=Gender.male)
    yield person(u'Johannes', u'Jonas',gender=Gender.male)
    yield person(u'Jan', u'Jousten',gender=Gender.male)
    yield person(u'Karl', u'Kaivers',gender=Gender.male)
    yield person(u'Guido', u'Lambertz',gender=Gender.male)
    yield person(u'Luc', u'Laschet',gender=Gender.male)
    yield person(u'Line', u'Lazarus',gender=Gender.female)
    yield person(u'Josefine', u'Leffin',gender=Gender.female)
    yield person(u'Marc', u'Malmendier',gender=Gender.male)
    yield person(u'Leo', u'Meessen',gender=Gender.male)
    yield person(u'Franz', u'Mießen',gender=Gender.male)
    yield person(u'Marie-Louise', u'Meier',gender=Gender.female)
    
    raeren = City.objects.get(name__exact='Raeren')
    person = Instantiator(settings.LINO.person_model,"first_name last_name",
                country='BE',language=default_language(),city=raeren,zip_code='4730').build
    yield person(u'Erich',    u'Emonts',gender=Gender.male)
    yield person(u'Erwin',    u'Emontspool',gender=Gender.male)
    yield person(u'Erna',     u'Emonts-Gast',gender=Gender.female)
    yield person(u'Alfons',     u'Radermacher',gender=Gender.male)
    yield person(u'Berta',     u'Radermacher',gender=Gender.female)
    yield person(u'Christian',     u'Radermacher',gender=Gender.male)
    yield person(u'Daniela',     u'Radermacher',gender=Gender.female)
    yield person(u'Edgard',     u'Radermacher')
    yield person(u'Fritz',     u'Radermacher')
    yield person(u'Guido',     u'Radermacher')
    yield person(u'Hans',     u'Radermacher')
    yield person(u'Hedi',     u'Radermacher')
    yield person(u'Inge',     u'Radermacher')
    yield person(u'Jean',     u'Radermacher')
    
    # special challenges for alphabetic ordering
    yield person(u'Elio',     u'di Rupo')
    yield person(u'Leonardo', u'da Vinci')
    yield person(u'Herman',   u'van Veen')
    yield person(u'Rein',   u'Õunapuu')
    
    yield person(u'Otto',   u'Östges')
    yield person(u'Erna',   u'Ärgerlich')
    
    
    person = Instantiator(settings.LINO.person_model,country='BE',city=City.objects.get(name__exact=u'Angleur')).build
    yield person(first_name=u'Bernard',last_name=u'Bodard',title='Dr.')
    yield person(first_name=u'Jean',last_name=u'Dupont')
    
    person = Instantiator(settings.LINO.person_model,country='BE',city=City.objects.get(name__exact=u'Oostende')).build
    yield person(first_name=u'Mark',last_name=u'Martelaer')
    yield person(first_name=u'Rik',last_name=u'Radermecker')
    yield person(first_name=u'Marie-Louise',last_name=u'Vandenmeulenbos')
    
    person = Instantiator(settings.LINO.person_model,country='DE').build
    yield person(first_name=u'Emil',last_name=u'Eierschal')
    yield person(first_name=u'Lisa',last_name=u'Lahm')
    yield person(first_name=u'Bernd',last_name=u'Brecht')
    yield person(first_name=u'Karl',last_name=u'Keller')
    
    person = Instantiator(settings.LINO.person_model,country='FR').build
    yield person(first_name=u'Robin',last_name=u'Dubois')
    yield person(first_name=u'Denis',last_name=u'Denon')
    yield person(first_name=u'Jérôme',last_name=u'Jeanémart')
    
    
    s = u"""\
Aachener Straße
Akazienweg
Alter Malmedyer Weg
Am Bahndamm
Am Berg
Am Waisenbüschchen
Auenweg
Auf dem Spitzberg
Auf'm Rain
August-Thonnar-Str.
Bahnhofsgasse
Bahnhofstraße
Bellmerin
Bennetsborn
Bergkapellstraße
Bergstraße
Binsterweg
Brabantstraße
Buchenweg
Edelstraße
Euregiostraße
Favrunpark
Feldstraße
Fränzel
Gewerbestraße
Gospert
Gülcherstraße
Haagenstraße
Haasberg
Haasstraße
Habsburgerweg
Heidberg
Heidgasse
Heidhöhe
Herbesthaler Straße
Hisselsgasse
Hochstraße
Hook
Hostert
Hufengasse
Hugo-Zimmermann-Str.
Hütte
Hütterprivatweg
Im Peschgen
In den Siepen
Industriestraße
Johannesstraße
Judenstraße
Kaperberg
Kaplan-Arnolds-Str.
Karl-Weiß-Str.
Kehrweg
Kirchgasse
Kirchstraße
Klinkeshöfchen
Kügelgasse
Langesthal
Lascheterweg
Limburgerweg
Lindenweg
Lothringerweg
Malmedyer Straße
Maria-Theresia-Straße
Marktplatz
Monschauer Straße
Mühlenweg
Neustraße
Nikolausfeld
Nispert
Noereth
Obere Ibern
Obere Rottergasse
Oestraße
Olengraben
Panorama
Paveestraße
Peter-Becker-Str.
Rosenweg
Rot-Kreuz-Str.
Rotenberg
Rotenbergplatz
Schilsweg
Schlüsselhof
Schnellewindgasse
Schönefeld
Schorberg
Schulstraße
Selterschlag
Simarstraße
Steinroth
Stendrich
Stockbergerweg
Stockem
Theodor-Mooren-Str.
Untere Ibern
Vervierser Straße
Vossengasse
Voulfeld
Werthplatz
Weserstraße
"""
    
    streets_of_eupen = [ line.strip() for line in s.splitlines() if len(line.strip()) > 0 ]
    
    i = 0
    nr = 1
    for p in resolve_model(settings.LINO.person_model).objects.filter(city=eupen):
        p.street = streets_of_eupen[i]
        p.stret_no = str(nr)
        p.save()
        nr += 1
        if i < len(streets_of_eupen) : 
            i += 1
        else:
            i = 0
        
        
