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
from lino.utils.instantiator import Instantiator
#~ from north.dbutils import default_language
#~ from lino.modlib.contacts.utils import Gender
from lino import mixins
from lino.utils import dblogger
from lino import dd
#from lino import reports

#~ contacts = reports.get_app('contacts')
#~ Gender = contacts.Gender

def objects():
    #~ dblogger.info("Installing contacts demo fixture") # use --verbosity=2
    #~ print settings.SITE.languages
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='EE').build
    yield company('Rumma & Ko OÜ','10115','Tallinn','Tartu mnt','71')
    #~ Company = resolve_model('contacts.Company')
    #~ obj = Company(name='Rumma & Ko OÜ',zip_code='10115',street='Tartu mnt',street_no='71')
    #~ print obj2str(obj)
    #~ yield obj
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='BE').build
    yield company('Bäckerei Ausdemwald', '4700', 'Eupen',  'Vervierser Straße','45')
    yield company('Bäckerei Mießen',     '4700', 'Eupen',  'Gospert','103')
    yield company('Bäckerei Schmitz',    '4700', 'Eupen',  'Aachener Straße','53')
    yield company('Garage Mergelsberg',  '4720', 'Kelmis', 'Kasinostraße','13')
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='NL').build
    yield company('Donderweer BV','4816 AR','Breda', 'Edisonstraat','12')
    yield company('Van Achter NV','4836 LG','Breda', 'Hazeldonk','2')
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='DE').build
    yield company('Hans Flott & Co','22453','Hamburg','Niendorfer Weg','532')
    if 'de' in settings.SITE.languages:
        munich = 'München'
    else:
        munich = 'Munich'
    yield company('Bernd Brechts Bücherladen','80333',munich,'Brienner Straße','18')
    yield company('Reinhards Baumschule','12487 ','Berlin','Segelfliegerdamm','123')
    
    company = Instantiator('contacts.Company',"name zip_code city:name street street_no",country='FR').build
    yield company('Moulin Rouge','75018','Paris','Boulevard de Clichy','82')
    yield company('Auto École Verte','54000 ','Nancy','rue de Mon Désert','12')
    
    City = dd.resolve_model('countries.City')
    
    #~ vigala = City.objects.get(name__exact='Vigala')
    #~ person = Instantiator("contacts.Person","first_name last_name",
                #~ country='EE',street='Uus', street_no='1',
                #~ addr2='Vana-Vigala küla',
                #~ city=vigala,zip_code='78003').build
    #~ yield person('Luc',  'Saffre', gender=mixins.Genders.male)
    
    eupen = City.objects.get(name__exact='Eupen')
    person = Instantiator("contacts.Person","first_name last_name",
                country='BE',city=eupen,zip_code='4700').build
    yield person('Andreas',  'Arens',gender=mixins.Genders.male)
    yield person('Annette',  'Arens',gender=mixins.Genders.female)
    yield person('Hans',     'Altenberg',gender=mixins.Genders.male)
    yield person('Alfons',   'Ausdemwald',gender=mixins.Genders.male)
    yield person('Laurent',  'Bastiaensen',gender=mixins.Genders.male)
    yield person('Charlotte', 'Collard',gender=mixins.Genders.female)
    yield person('Ulrike',   'Charlier',gender=mixins.Genders.female)
    yield person('Marc',  'Chantraine',gender=mixins.Genders.male)
    yield person('Daniel',   'Dericum',gender=mixins.Genders.male)
    yield person('Dorothée', 'Demeulenaere',gender=mixins.Genders.female)
    yield person('Dorothée', 'Dobbelstein-Demeulenaere',gender=mixins.Genders.female)
    yield person('Dorothée', 'Dobbelstein',gender=mixins.Genders.female)
    yield person('Berta',    'Ernst',gender=mixins.Genders.female)
    yield person('Bernd',    'Evertz',gender=mixins.Genders.male)
    yield person('Eberhart', 'Evers',gender=mixins.Genders.male)
    yield person('Daniel',   'Emonts',gender=mixins.Genders.male)
    yield person('Edgar',    'Engels',gender=mixins.Genders.male)
    yield person('Luc',      'Faymonville',gender=mixins.Genders.male)
    yield person('Germaine', 'Gernegroß',gender=mixins.Genders.female)
    yield person('Gregory',  'Groteclaes',gender=mixins.Genders.male)
    yield person('Hildegard','Hilgers',gender=mixins.Genders.female)
    yield person('Henri',    'Hilgers',gender=mixins.Genders.male)
    yield person('Irene',    'Ingels',gender=mixins.Genders.female)
    yield person('Jérémy',   'Jansen',gender=mixins.Genders.male)
    yield person('Jacqueline', 'Jacobs',gender=mixins.Genders.female)
    yield person('Johann', 'Johnen',gender=mixins.Genders.male)
    yield person('Josef', 'Jonas',gender=mixins.Genders.male)
    yield person('Jan',   'Jousten',gender=mixins.Genders.male)
    yield person('Karl',  'Kaivers',gender=mixins.Genders.male)
    yield person('Guido', 'Lambertz',gender=mixins.Genders.male)
    yield person('Laura', 'Laschet',gender=mixins.Genders.female)
    yield person('Line', 'Lazarus',gender=mixins.Genders.female)
    yield person('Josefine', 'Leffin',gender=mixins.Genders.female)
    yield person('Marc', 'Malmendier',gender=mixins.Genders.male)
    yield person('Melissa', 'Meessen',gender=mixins.Genders.female)
    yield person('Michael', 'Mießen',gender=mixins.Genders.male)
    yield person('Marie-Louise', 'Meier',gender=mixins.Genders.female)
    
    raeren = City.objects.get(name__exact='Raeren')
    person = Instantiator("contacts.Person","first_name last_name",
                country='BE',language=settings.SITE.DEFAULT_LANGUAGE.django_code,
                city=raeren,zip_code='4730').build
    yield person('Erich',    'Emonts',gender=mixins.Genders.male)
    yield person('Erwin',    'Emontspool',gender=mixins.Genders.male)
    yield person('Erna',     'Emonts-Gast',gender=mixins.Genders.female)
    yield person('Alfons',     'Radermacher',gender=mixins.Genders.male)
    yield person('Berta',     'Radermacher',gender=mixins.Genders.female)
    yield person('Christian',     'Radermacher',gender=mixins.Genders.male)
    yield person('Daniela',     'Radermacher',gender=mixins.Genders.female)
    yield person('Edgard',     'Radermacher',gender=mixins.Genders.male)
    yield person('Fritz',     'Radermacher',gender=mixins.Genders.male)
    yield person('Guido',     'Radermacher',gender=mixins.Genders.male)
    yield person('Hans',     'Radermacher',gender=mixins.Genders.male)
    yield person('Hedi',     'Radermacher',gender=mixins.Genders.female)
    yield person('Inge',     'Radermacher',gender=mixins.Genders.female)
    yield person('Jean',     'Radermacher',gender=mixins.Genders.male)
    
    # special challenges for alphabetic ordering
    yield person('Didier',     'di Rupo',gender=mixins.Genders.male)
    yield person('David', 'da Vinci',gender=mixins.Genders.male)
    yield person('Vincent',   'van Veen',gender=mixins.Genders.male)
    yield person('Rein',   'Õunapuu',gender=mixins.Genders.male)
    
    yield person('Otto',   'Östges',gender=mixins.Genders.male)
    yield person('Erna',   'Ärgerlich',gender=mixins.Genders.female)
    
    
    person = Instantiator("contacts.Person",country='BE',city=City.objects.get(name__exact='Angleur')).build
    yield person(first_name='Bernard',last_name='Bodard',title='Dr.')
    yield person(first_name='Jean',last_name='Dupont')
    
    #~ person = Instantiator("contacts.Person",country='BE',city=City.objects.get(name__exact='Oostende')).build
    person = Instantiator("contacts.Person",country='NL',city=City.objects.get(name__exact='Amsterdam')).build
    yield person(first_name='Mark',last_name='Martelaer',gender=mixins.Genders.male)
    yield person(first_name='Rik',last_name='Radermecker',gender=mixins.Genders.male)
    yield person(first_name='Marie-Louise',last_name='Vandenmeulenbos',gender=mixins.Genders.female)
    
    person = Instantiator("contacts.Person",country='DE').build
    yield person(first_name='Emil',last_name='Eierschal',gender=mixins.Genders.male)
    yield person(first_name='Lisa',last_name='Lahm',gender=mixins.Genders.female)
    yield person(first_name='Bernd',last_name='Brecht',gender=mixins.Genders.male)
    yield person(first_name='Karl',last_name='Keller',gender=mixins.Genders.male)
    
    person = Instantiator("contacts.Person",country='FR').build
    yield person(first_name='Robin',last_name='Dubois',gender=mixins.Genders.male)
    yield person(first_name='Denis',last_name='Denon',gender=mixins.Genders.male)
    yield person(first_name='Jérôme',last_name='Jeanémart',gender=mixins.Genders.male)
    
    
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
    for p in dd.resolve_model("contacts.Person").objects.filter(city=eupen):
        p.street = streets_of_eupen[i]
        p.stret_no = str(nr)
        p.save()
        nr += 1
        if i < len(streets_of_eupen) : 
            i += 1
        else:
            i = 0
        
        
