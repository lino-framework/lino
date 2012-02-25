# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
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

#~ import logging
#~ logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from lino.tools import resolve_model
from lino.utils.instantiator import Instantiator
from lino.utils.babel import default_language
from lino.utils.babel import babel_values
from lino.utils.choicelists import Gender
from lino.utils import dblogger
from lino.utils import Cycler

from lino.sandbox.contacts import models as contacts

print 20120225, 'settings.FIXTURE_DIRS is', settings.FIXTURE_DIRS

dblogger.info("Imported contacts demo fixture")

COUNT = 0

#~ addresstype= Instantiator('contacts.AddressType',"name").build
role = Instantiator('contacts.Role',"name").build
#~ person = Instantiator('contacts.Person',"first_name last_name").build
#~ company = Instantiator('contacts.Company',"name").build
#~ contact = Instantiator('contacts.Contact').build

Company = contacts.Company
Person = contacts.Person
User = contacts.User
City = resolve_model('countries.City')

if not settings.LINO.abstract_address:
    Address = contacts.Address
    address = Instantiator(Address,"country zip_code city:name street street_no").build


def company(name,country_id,zip_code,city,street,street_no):
    if settings.LINO.abstract_address:
        city = City.objects.get(name=city)
        yield Company(name=name,country_id=country_id,zip_code=zip_code,
          city=city,street=street,street_no=street_no)
    else:
        addr = address(country_id,zip_code,city,street,street_no)
        yield addr
        com = Company(name=name,address=addr)
        yield com

def person(first_name,last_name,country_id=None,zip_code='',city=None,**kw):
    if settings.LINO.abstract_address:
        if city is not None:
            city = City.objects.get(name=city)
        yield Person(first_name=first_name,last_name=last_name,
          country_id=country_id,zip_code=zip_code,city=city)
    else:
        addr = address(country_id,zip_code,city)
        yield addr
        yield Person(first_name=first_name,last_name=last_name,address=addr)
    
    
def contact(company,person,**kw):
    return contacts.Contact(person=person,company=company,**kw)
        

def objects():
    global COUNT
    COUNT += 1
    dblogger.info("Started contacts demo fixture %d",COUNT)
    
    #~ yield addresstype(**babel_values('name',en="Default",fr=u'Gérant',de=u"Geschäftsführer",et=u"Manager"))
    
    yield role(**babel_values('name',en="Manager",fr=u'Gérant',de=u"Geschäftsführer",et=u"Manager"))
    yield role(**babel_values('name',en="Director",fr=u'Directeur',de=u"Direktor",et=u"Direktor"))
    yield role(**babel_values('name',en="Secretary",fr=u'Sécrétaire',de=u"Sekretär",et=u"Sekretär"))
    yield role(**babel_values('name',en="IT Manager",fr=u'Gérant informatique',de=u"EDV-Manager",et=u"IT manager"))
    
    
    yield company(u"Rumma & Ko OÜ", 'EE','10115','Tallinn',u'Tartu mnt','71')
    
    yield company(u'Bäckerei Ausdemwald', 'BE', '4700', 'Eupen',  u'Vervierser Straße','45')
    yield company(u'Bäckerei Mießen',     'BE', '4700', 'Eupen',  u'Gospert','103')
    yield company(u'Bäckerei Schmitz',    'BE', '4700', 'Eupen',  u'Aachener Straße','53')
    yield company(u'Garage Mergelsberg',  'BE', '4720', 'Kelmis', u'Kasinostraße','13')
    
    yield company(u'Donderweer BV',       'NL', '4816 AR','Breda', 'Edisonstraat','12')
    yield company(u'Van Achter NV',       'NL', '4836 LG','Breda', 'Hazeldonk','2')
    
    yield company(u'Hans Flott & Co',     'DE', '22453','Hamburg',u'Niendorfer Weg','532')
    yield company(u'Bernd Brechts Bücherladen','DE', '80333',u'München',u'Brienner Straße','18')
    yield company(u'Reinhards Baumschule','DE', '12487 ',u'Berlin',u'Segelfliegerdamm','123')
    
    yield company(u'Moulin Rouge',  'FR', '75018','Paris',u'Boulevard de Clichy','82')
    yield company(u'Auto École Verte','FR', '54000 ','Nancy',u'rue de Mon Désert','12')
    
    
    
    #~ yield person(u'Luc',  u'Saffre', gender=Gender.male)
    
    yield person(u'Andreas',  u'Arens', 'BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Annette',  u'Arens','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Hans',     u'Altenberg','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Alfons',   u'Ausdemwald','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Laurent',  u'Bastiaensen','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Charlotte',  u'Collard','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Ulrike',  u'Charlier','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Marc',  u'Chantraine','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Daniel',   u'Dericum','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Dorothée', u'Demeulenaere','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Berta',    u'Ernst','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Bernd',    u'Evertz','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Eberhart', u'Evers','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Daniel',   u'Emonts','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Edgar',    u'Engels','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Luc',      u'Faymonville','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Gérard',   u'Gernegroß','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Werner',   u'Groteclaes','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Grete',    u'Hilgers','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Hans',     u'Hilgers','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Irene',    u'Ingels','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Jérémy',   u'Jansen','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Jean-Pierre', u'Jacob','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Herbert', u'Johnen','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Johannes', u'Jonas','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Jan', u'Jousten','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Karl', u'Kaivers','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Guido', u'Lambertz','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Luc', u'Laschet','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Line', u'Lazarus','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Josefine', u'Leffin','BE','4700','Eupen',  gender=Gender.female)
    yield person(u'Marc', u'Malmendier','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Leo', u'Meessen','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Franz', u'Mießen','BE','4700','Eupen',  gender=Gender.male)
    yield person(u'Marie-Louise', u'Meier','BE','4700','Eupen',  gender=Gender.female)
    
    yield person(u'Erich',     u'Emonts',     'BE','4730','Raeren', gender=Gender.male)
    yield person(u'Erwin',     u'Emontspool', 'BE','4730','Raeren', gender=Gender.male)
    yield person(u'Erna',      u'Emonts-Gast', 'BE','4730','Raeren', gender=Gender.female)
    yield person(u'Alfons',    u'Radermacher','BE','4730','Raeren', gender=Gender.male)
    yield person(u'Berta',     u'Radermacher','BE','4730','Raeren', gender=Gender.female)
    yield person(u'Christian', u'Radermacher','BE','4730','Raeren', gender=Gender.male)
    yield person(u'Daniela',   u'Radermacher','BE','4730','Raeren', gender=Gender.female)
    yield person(u'Edgard',    u'Radermacher','BE','4730','Raeren', gender=Gender.male)
    yield person(u'Fritz',     u'Radermacher','BE','4730','Raeren', gender=Gender.male)
    yield person(u'Guido',     u'Radermacher','BE','4730','Raeren', gender=Gender.male)
    yield person(u'Hans',      u'Radermacher','BE','4730','Raeren', gender=Gender.male)
    yield person(u'Hedi',      u'Radermacher','BE','4730','Raeren', gender=Gender.female)
    yield person(u'Inge',      u'Radermacher','BE','4730','Raeren', gender=Gender.female)
    yield person(u'Jean',      u'Radermacher','BE','4730','Raeren', gender=Gender.male)
    
    # special challenges for alphabetic ordering
    yield person(u'Elio',     u'di Rupo')
    yield person(u'Leonardo', u'da Vinci')
    yield person(u'Herman',   u'van Veen')
    yield person(u'Rein',   u'Õunapuu')
    yield person(u'Otto',   u'Östges')
    yield person(u'Erna',   u'Ärgerlich')
    
    
    yield person(u'Bernard',u'Bodard',title='Dr.')
    yield person(u'Jean',u'Dupont')
    
    yield person(u'Mark',u'Martelaer')
    yield person(u'Rik',u'Radermecker')
    yield person(u'Marie-Louise',u'Vandenmeulenbos')
    
    yield person(u'Emil',u'Eierschal')
    yield person(u'Lisa',u'Lahm')
    yield person(u'Bernd',u'Brecht')
    yield person(u'Karl',u'Keller')
    
    yield person(u'Robin',u'Dubois')
    yield person(u'Denis',u'Denon')
    yield person(u'Jérôme',u'Jeanémart')
    
    
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
    
    if settings.LINO.abstract_address:
    
        nr = 1
        #~ CITIES = Cycler(City.objects.all())
        eupen = City.objects.get(name="Eupen")
        STREETS = Cycler(streets_of_eupen)
        for p in Person.objects.filter(city=eupen):
            p.street = STREETS.pop()
            p.street_no = str(nr)
            p.save()
            nr += 1
    else:
        nr = 1
        for street in streets_of_eupen:
            for i in range(3):
                yield address('BE','4700','Eupen',street,str(nr))
                nr += 1
            
            
        ADDRESSES = Cycler(Address.objects.all())
        for p in Person.objects.all():
            p.address = ADDRESSES.pop()
            p.save()
      
        
    PERSONS = Cycler(contacts.Person.objects.all())
    COMPANIES = Cycler(contacts.Company.objects.all())
    ROLES = Cycler(contacts.Role.objects.all())
    for i in range(100):
        com = COMPANIES.pop()
        yield contact(com,PERSONS.pop(),role=ROLES.pop())
        yield contact(com,PERSONS.pop(),role=ROLES.pop())
        
    rumma = contacts.Company.objects.get(name=u"Rumma & Ko OÜ")
    def user(first_name,last_name,**kw):
        p = Person(first_name=first_name,last_name=last_name)
        p.save()
        return User(person=p,company=rumma,**kw)
    
    yield user("Alice","Imedemaal",is_superuser=True)
    yield user("Bert","Sesamestreet")
    yield user("Charles","Braun")
    dblogger.info("Done contacts demo fixture")