# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds a series of fictive persons and companies.
"""

from __future__ import unicode_literals
from builtins import str


from django.conf import settings
from lino.utils.instantiator import Instantiator
from lino.utils import Cycler
from lino.api import dd, rt

from lino.utils.demonames.bel import streets_of_eupen
STREETS = Cycler(streets_of_eupen())


def objects():

    if settings.SITE.get_language_info('de'):
        munich = 'München'
    else:
        munich = 'Munich'  # en, fr

    if settings.SITE.get_language_info('fr'):
        kelmis = 'La Calamine'
    else:
        kelmis = 'Kelmis'  # en, de

    company = Instantiator(
        'contacts.Company',
        "name zip_code city:name street street_no",
        country='EE').build
    yield company('Rumma & Ko OÜ', '10115', 'Tallinn', 'Tartu mnt', '71')

    company = Instantiator(
        'contacts.Company', "name zip_code city:name street street_no",
        country='BE').build
    yield company('Bäckerei Ausdemwald', '4700', 'Eupen',
                  'Vervierser Straße', '45')
    yield company('Bäckerei Mießen',     '4700', 'Eupen',
                  'Gospert', '103')
    yield company('Bäckerei Schmitz',    '4700', 'Eupen',
                  'Aachener Straße', '53')
    yield company('Garage Mergelsberg',  '4720', kelmis,
                  'Kasinostraße', '13')

    company = Instantiator(
        'contacts.Company',
        "name zip_code city:name street street_no", country='NL').build
    yield company('Donderweer BV', '4816 AR', 'Breda', 'Edisonstraat', '12')
    yield company('Van Achter NV', '4836 LG', 'Breda', 'Hazeldonk', '2')

    company = Instantiator(
        'contacts.Company',
        "name zip_code city:name street street_no", country='DE').build
    yield company('Hans Flott & Co', '22453', 'Hamburg',
                  'Niendorfer Weg', '532')
    yield company('Bernd Brechts Bücherladen', '80333',
                  munich, 'Brienner Straße', '18')
    yield company('Reinhards Baumschule', '12487 ',
                  'Berlin', 'Segelfliegerdamm', '123')

    company = Instantiator(
        'contacts.Company',
        "name zip_code city:name street street_no", country='FR').build
    yield company('Moulin Rouge', '75018', 'Paris',
                  'Boulevard de Clichy', '82')
    yield company('Auto École Verte', '54000 ', 'Nancy',
                  'rue de Mon Désert', '12')

    Place = dd.resolve_model('countries.Place')

    eupen = Place.objects.get(name__exact='Eupen')
    person = Instantiator("contacts.Person", "first_name last_name",
                          country='BE', city=eupen, zip_code='4700').build
    yield person('Andreas',  'Arens', gender=dd.Genders.male)
    yield person('Annette',  'Arens', gender=dd.Genders.female)
    yield person('Hans',     'Altenberg', gender=dd.Genders.male)
    yield person('Alfons',   'Ausdemwald', gender=dd.Genders.male)
    yield person('Laurent',  'Bastiaensen', gender=dd.Genders.male)
    yield person('Charlotte', 'Collard', gender=dd.Genders.female)
    yield person('Ulrike',   'Charlier', gender=dd.Genders.female)
    yield person('Marc',  'Chantraine', gender=dd.Genders.male)
    yield person('Daniel',   'Dericum', gender=dd.Genders.male)
    yield person('Dorothée', 'Demeulenaere', gender=dd.Genders.female)
    yield person('Dorothée', 'Dobbelstein-Demeulenaere',
                 gender=dd.Genders.female)
    yield person('Dorothée', 'Dobbelstein', gender=dd.Genders.female)
    yield person('Berta',    'Ernst', gender=dd.Genders.female)
    yield person('Bernd',    'Evertz', gender=dd.Genders.male)
    yield person('Eberhart', 'Evers', gender=dd.Genders.male)
    yield person('Daniel',   'Emonts', gender=dd.Genders.male)
    yield person('Edgar',    'Engels', gender=dd.Genders.male)
    yield person('Luc',      'Faymonville', gender=dd.Genders.male)
    yield person('Germaine', 'Gernegroß', gender=dd.Genders.female)
    yield person('Gregory',  'Groteclaes', gender=dd.Genders.male)
    yield person('Hildegard', 'Hilgers', gender=dd.Genders.female)
    yield person('Henri',    'Hilgers', gender=dd.Genders.male)
    yield person('Irene',    'Ingels', gender=dd.Genders.female)
    yield person('Jérémy',   'Jansen', gender=dd.Genders.male)
    yield person('Jacqueline', 'Jacobs', gender=dd.Genders.female)
    yield person('Johann', 'Johnen', gender=dd.Genders.male)
    yield person('Josef', 'Jonas', gender=dd.Genders.male)
    yield person('Jan',   'Jousten', gender=dd.Genders.male)
    yield person('Karl',  'Kaivers', gender=dd.Genders.male)
    yield person('Guido', 'Lambertz', gender=dd.Genders.male)
    yield person('Laura', 'Laschet', gender=dd.Genders.female)
    yield person('Line', 'Lazarus', gender=dd.Genders.female)
    yield person('Josefine', 'Leffin', gender=dd.Genders.female)
    yield person('Marc', 'Malmendier', gender=dd.Genders.male)
    yield person('Melissa', 'Meessen', gender=dd.Genders.female)
    yield person('Michael', 'Mießen', gender=dd.Genders.male)
    yield person('Marie-Louise', 'Meier', gender=dd.Genders.female)

    raeren = Place.objects.get(name__exact='Raeren')
    person = Instantiator(
        "contacts.Person", "first_name last_name",
        country='BE', language=settings.SITE.DEFAULT_LANGUAGE.django_code,
        city=raeren, zip_code='4730').build
    yield person('Erich',    'Emonts', gender=dd.Genders.male)
    yield person('Erwin',    'Emontspool', gender=dd.Genders.male)
    yield person('Erna',     'Emonts-Gast', gender=dd.Genders.female)
    yield person('Alfons',     'Radermacher', gender=dd.Genders.male)
    yield person('Berta',     'Radermacher', gender=dd.Genders.female)
    yield person('Christian',     'Radermacher', gender=dd.Genders.male)
    yield person('Daniela',     'Radermacher', gender=dd.Genders.female)
    yield person('Edgard',     'Radermacher', gender=dd.Genders.male)
    yield person('Fritz',     'Radermacher', gender=dd.Genders.male)
    yield person('Guido',     'Radermacher', gender=dd.Genders.male)
    yield person('Hans',     'Radermacher', gender=dd.Genders.male)
    yield person('Hedi',     'Radermacher', gender=dd.Genders.female)
    yield person('Inge',     'Radermacher', gender=dd.Genders.female)
    yield person('Jean',     'Radermacher', gender=dd.Genders.male)

    # special challenges for alphabetic ordering
    yield person('Didier',  'di Rupo', gender=dd.Genders.male)
    yield person('David',   'da Vinci', gender=dd.Genders.male)
    yield person('Vincent', 'van Veen', gender=dd.Genders.male)
    yield person('Õie',     'Õunapuu', gender=dd.Genders.female)
    yield person('Otto',   'Östges', gender=dd.Genders.male)
    yield person('Erna',   'Ärgerlich', gender=dd.Genders.female)

    person = Instantiator("contacts.Person", country='BE',
                          city=Place.objects.get(name__exact='Angleur')).build
    yield person(first_name='Bernard', last_name='Bodard', title='Dr.')
    yield person(first_name='Jean', last_name='Dupont')

    person = Instantiator("contacts.Person", country='NL',
                          city=Place.objects.get(
                              name__exact='Amsterdam')).build
    yield person(first_name='Mark', last_name='Martelaer',
                 gender=dd.Genders.male)
    yield person(first_name='Rik', last_name='Radermecker',
                 gender=dd.Genders.male)
    yield person(first_name='Marie-Louise', last_name='Vandenmeulenbos',
                 gender=dd.Genders.female)

    person = Instantiator("contacts.Person", country='DE').build
    yield person(first_name='Emil', last_name='Eierschal',
                 gender=dd.Genders.male)
    yield person(first_name='Lisa', last_name='Lahm',
                 gender=dd.Genders.female)
    yield person(first_name='Bernd', last_name='Brecht',
                 gender=dd.Genders.male)
    yield person(first_name='Karl', last_name='Keller',
                 gender=dd.Genders.male)

    person = Instantiator("contacts.Person", country='FR').build
    yield person(first_name='Robin', last_name='Dubois',
                 gender=dd.Genders.male)
    yield person(first_name='Denis', last_name='Denon',
                 gender=dd.Genders.male)
    yield person(first_name='Jérôme', last_name='Jeanémart',
                 gender=dd.Genders.male)

    nr = 1
    for p in rt.modules.contacts.Person.objects.filter(city=eupen):
        p.street = STREETS.pop()
        p.stret_no = str(nr)
        p.save()
        nr += 1
