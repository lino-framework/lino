# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# License: BSD (see file COPYING for details)

from django.conf import settings
from lino.core.dbutils import resolve_model
from lino.utils.instantiator import Instantiator
#from lino import reports


def objects():
    #~ city = Instantiator('countries.City','name country').build
    #~ yield city('Vigala','EE')
    if 'et' in settings.SITE.languages:
        lang = 'et'
    else:
        # if language 'et' is not available, use the default language
        lang = settings.SITE.languages[0]

    organisation = Instantiator(
        "partners.Organisation", country='EE', language=lang).build
    yield organisation(name=u'Minu Firma OÜ')
    yield organisation(name=u'Mets ja Puu OÜ')
    yield organisation(name=u'Kenavälja OÜ')

    person = Instantiator("partners.Person",
                          "first_name last_name", country='EE').build
    yield person(u'Aare', u'Aaresild')
    yield person(u'Ahti', u'Aaspere')
    yield person(u'Peeter', u'Bach')
    yield person(u'Tiina', u'Engelbert')
    yield person(u'Inge', u'Hallik')
    yield person(u'Harri', u'Hunt')
    yield person(u'Ingmar', u'Iliste')
    yield person(u'Jaan', u'Janno')
    yield person(u'Jaan', u'Jõgi')
    yield person(u'Karl', u'Kask')
    yield person(u'Leo', u'Lepamets')
    yield person(u'Madis', u'Mäeorg')
    yield person(u'Natalja', u'Nagel')
    yield person(u'Ott', u'Ojavee')
    yield person(u'Piret', u'Paas')
    yield person(u'Rannes', u'Rannala')
    yield person(u'Silja', u'Sääsk')
    yield person(u'Tõnu', u'Tamm')
    yield person(u'Tiina', u'Türnpuu')
    yield person(u'Urmas', u'Uukivi')
