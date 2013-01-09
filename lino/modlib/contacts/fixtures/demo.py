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
Deserves documentation
"""

from __future__ import unicode_literals


from django.conf import settings
from lino.core.modeltools import resolve_model, obj2str
from lino.utils.instantiator import Instantiator
from lino.utils.babel import default_language
#~ from lino.modlib.contacts.utils import Gender
from lino import mixins
from lino.utils import dblogger
#~ from lino import dd
#from lino import reports

#~ contacts = reports.get_app('contacts')
#~ Gender = contacts.Gender

def objects():
    #~ dblogger.info("Installing contacts demo fixture") # use --verbosity=2
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='EE').build
    yield company('Rumma & Ko OÜ','10115','Tallinn','Tartu mnt','71')
    #~ Company = resolve_model('contacts.Company')
    #~ obj = Company(name=u'Rumma & Ko OÜ',zip_code='10115',street=u'Tartu mnt',street_no='71')
    #~ print obj2str(obj)
    #~ yield obj
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='BE').build
    yield company('Bäckerei Ausdemwald', '4700', 'Eupen',  u'Vervierser Straße','45')
    yield company('Bäckerei Mießen',     '4700', 'Eupen',  u'Gospert','103')
    yield company('Bäckerei Schmitz',    '4700', 'Eupen',  u'Aachener Straße','53')
    yield company('Garage Mergelsberg',  '4720', 'Kelmis', u'Kasinostraße','13')
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='NL').build
    yield company(u'Donderweer BV','4816 AR','Breda', 'Edisonstraat','12')
    yield company(u'Van Achter NV','4836 LG','Breda', 'Hazeldonk','2')
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='DE').build
    yield company('Hans Flott & Co','22453','Hamburg','Niendorfer Weg','532')
    yield company('Bernd Brechts Bücherladen','80333','München','Brienner Straße','18')
    yield company('Reinhards Baumschule','12487 ','Berlin','Segelfliegerdamm','123')
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='FR').build
    yield company(u'Moulin Rouge','75018','Paris',u'Boulevard de Clichy','82')
    yield company(u'Auto École Verte','54000 ','Nancy',u'rue de Mon Désert','12')
    
    City = resolve_model('countries.City')
    vigala = City.objects.get(name__exact='Vigala')
    #~ tallinn = City.objects.get(name__exact='Tallinn')
    person = Instantiator(settings.LINO.person_model,"first_name last_name",
                country='EE',street='Uus', street_no='1',
                addr2=u'Vana-Vigala küla',
                city=vigala,zip_code='78003').build
    #~ yield person(u'Luc',  u'Saffre', gender=Gender.male,birth_date='1968-06-01')
    yield person(u'Luc',  u'Saffre', gender=mixins.Genders.male)
    
    eupen = City.objects.get(name__exact='Eupen')
    person = Instantiator(settings.LINO.person_model,"first_name last_name",
                country='BE',city=eupen,zip_code='4700').build
    yield person(u'Andreas',  u'Arens',gender=mixins.Genders.male)
    yield person(u'Annette',  u'Arens',gender=mixins.Genders.female)
    yield person(u'Hans',     u'Altenberg',gender=mixins.Genders.male)
    yield person(u'Alfons',   u'Ausdemwald',gender=mixins.Genders.male)
    yield person(u'Laurent',  u'Bastiaensen',gender=mixins.Genders.male)
    yield person(u'Charlotte', u'Collard',gender=mixins.Genders.female)
    yield person(u'Ulrike',   u'Charlier',gender=mixins.Genders.female)
    yield person(u'Marc',  u'Chantraine',gender=mixins.Genders.male)
    yield person(u'Daniel',   u'Dericum',gender=mixins.Genders.male)
    yield person(u'Dorothée', u'Demeulenaere',gender=mixins.Genders.female)
    yield person(u'Berta',    u'Ernst',gender=mixins.Genders.female)
    yield person(u'Bernd',    u'Evertz',gender=mixins.Genders.male)
    yield person(u'Eberhart', u'Evers',gender=mixins.Genders.male)
    yield person(u'Daniel',   u'Emonts',gender=mixins.Genders.male)
    yield person(u'Edgar',    u'Engels',gender=mixins.Genders.male)
    yield person(u'Luc',      u'Faymonville',gender=mixins.Genders.male)
    yield person(u'Germaine', u'Gernegroß',gender=mixins.Genders.female)
    yield person(u'Gregory',  u'Groteclaes',gender=mixins.Genders.male)
    yield person(u'Hildegard',u'Hilgers',gender=mixins.Genders.female)
    yield person(u'Henri',    u'Hilgers',gender=mixins.Genders.male)
    yield person(u'Irene',    u'Ingels',gender=mixins.Genders.female)
    yield person(u'Jérémy',   u'Jansen',gender=mixins.Genders.male)
    yield person(u'Jacqueline', u'Jacobs',gender=mixins.Genders.female)
    yield person(u'Johann', u'Johnen',gender=mixins.Genders.male)
    yield person(u'Josef', u'Jonas',gender=mixins.Genders.male)
    yield person(u'Jan',   u'Jousten',gender=mixins.Genders.male)
    yield person(u'Karl',  u'Kaivers',gender=mixins.Genders.male)
    yield person(u'Guido', u'Lambertz',gender=mixins.Genders.male)
    yield person(u'Laura', u'Laschet',gender=mixins.Genders.female)
    yield person(u'Line', u'Lazarus',gender=mixins.Genders.female)
    yield person(u'Josefine', u'Leffin',gender=mixins.Genders.female)
    yield person(u'Marc', u'Malmendier',gender=mixins.Genders.male)
    yield person(u'Melissa', u'Meessen',gender=mixins.Genders.female)
    yield person(u'Michael', u'Mießen',gender=mixins.Genders.male)
    yield person(u'Marie-Louise', u'Meier',gender=mixins.Genders.female)
    
    raeren = City.objects.get(name__exact='Raeren')
    person = Instantiator(settings.LINO.person_model,"first_name last_name",
                country='BE',language=default_language(),
                city=raeren,zip_code='4730').build
    yield person(u'Erich',    u'Emonts',gender=mixins.Genders.male)
    yield person(u'Erwin',    u'Emontspool',gender=mixins.Genders.male)
    yield person(u'Erna',     u'Emonts-Gast',gender=mixins.Genders.female)
    yield person(u'Alfons',     u'Radermacher',gender=mixins.Genders.male)
    yield person(u'Berta',     u'Radermacher',gender=mixins.Genders.female)
    yield person(u'Christian',     u'Radermacher',gender=mixins.Genders.male)
    yield person(u'Daniela',     u'Radermacher',gender=mixins.Genders.female)
    yield person(u'Edgard',     u'Radermacher',gender=mixins.Genders.male)
    yield person(u'Fritz',     u'Radermacher',gender=mixins.Genders.male)
    yield person(u'Guido',     u'Radermacher',gender=mixins.Genders.male)
    yield person(u'Hans',     u'Radermacher',gender=mixins.Genders.male)
    yield person(u'Hedi',     u'Radermacher',gender=mixins.Genders.female)
    yield person(u'Inge',     u'Radermacher',gender=mixins.Genders.female)
    yield person(u'Jean',     u'Radermacher',gender=mixins.Genders.male)
    
    # special challenges for alphabetic ordering
    yield person(u'Didier',     u'di Rupo',gender=mixins.Genders.male)
    yield person(u'David', u'da Vinci',gender=mixins.Genders.male)
    yield person(u'Vincent',   u'van Veen',gender=mixins.Genders.male)
    yield person(u'Rein',   u'Õunapuu',gender=mixins.Genders.male)
    
    yield person(u'Otto',   u'Östges',gender=mixins.Genders.male)
    yield person(u'Erna',   u'Ärgerlich',gender=mixins.Genders.female)
    
    
    person = Instantiator(settings.LINO.person_model,country='BE',city=City.objects.get(name__exact=u'Angleur')).build
    yield person(first_name=u'Bernard',last_name=u'Bodard',title='Dr.')
    yield person(first_name=u'Jean',last_name=u'Dupont')
    
    #~ person = Instantiator(settings.LINO.person_model,country='BE',city=City.objects.get(name__exact=u'Oostende')).build
    person = Instantiator(settings.LINO.person_model,country='NL',city=City.objects.get(name__exact='Amsterdam')).build
    yield person(first_name=u'Mark',last_name=u'Martelaer',gender=mixins.Genders.male)
    yield person(first_name=u'Rik',last_name=u'Radermecker',gender=mixins.Genders.male)
    yield person(first_name=u'Marie-Louise',last_name=u'Vandenmeulenbos',gender=mixins.Genders.female)
    
    person = Instantiator(settings.LINO.person_model,country='DE').build
    yield person(first_name=u'Emil',last_name=u'Eierschal',gender=mixins.Genders.male)
    yield person(first_name=u'Lisa',last_name=u'Lahm',gender=mixins.Genders.female)
    yield person(first_name=u'Bernd',last_name=u'Brecht',gender=mixins.Genders.male)
    yield person(first_name=u'Karl',last_name=u'Keller',gender=mixins.Genders.male)
    
    person = Instantiator(settings.LINO.person_model,country='FR').build
    yield person(first_name=u'Robin',last_name=u'Dubois',gender=mixins.Genders.male)
    yield person(first_name=u'Denis',last_name=u'Denon',gender=mixins.Genders.male)
    yield person(first_name=u'Jérôme',last_name=u'Jeanémart',gender=mixins.Genders.male)
    
    
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
        
        
