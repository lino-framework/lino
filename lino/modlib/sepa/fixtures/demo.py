# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds some commonly known partners and their bank accounts.
"""

from __future__ import unicode_literals

from lino.utils.instantiator import Instantiator
from lino.api import rt

Company = Instantiator('contacts.Company', 'name url').build
Account = Instantiator('sepa.Account', 'partner bic iban remark').build


class Adder(object):
    
    def __init__(self):
        self.current_partner = None
        
    def add_company(self, name, url, **kw):
        obj = Company(name=name, url=url, **kw)
        self.current_partner = obj
        return obj
    
    def add_account(self, bic, iban, remark=''):
        iban = iban.replace(' ', '')
        return Account(self.current_partner, bic, iban, remark)


def objects():

    adder = Adder()
    C = adder.add_company
    A = adder.add_account
        
    yield C('AS Express Post', 'http://www.expresspost.ee/',
            country="EE")
    yield A('HABAEE2X', 'EE872200221012067904')

    yield C('AS Matsalu Veevärk', 'http://www.matsaluvv.ee',
            country="EE")
    yield A('HABAEE2X', 'EE732200221045112758')

    yield C('Eesti Energia AS', "http://www.energia.ee",
            country="EE")
    yield A('HABAEE2X', 'EE232200001180005555', "Eraklilendile")
    yield A('HABAEE2X', 'EE322200221112223334', "Ärikliendile")
    yield A('EEUHEE2X', 'EE081010002059413005')
    yield A('FOREEE2X', 'EE70 3300 3320 9900 0006')
    yield A('NDEAEE2X', 'EE43 17000 1700 0115 797')
    
    yield C('IIZI kindlustusmaakler AS', "http://www.iizi.ee",
            country="EE")
    yield A('HABAEE2X', 'EE382200221013987931')

    yield C('Maksu- ja tolliamet', "http://www.emta.ee",
            country="EE")
    yield A('HABAEE2X', 'EE522200221013264447')

    tallinn = rt.modules.countries.Place.objects.get(name="Tallinn")
    yield C('Ragn-Sells AS', "http://www.ragnsells.ee", country="EE",
            street="Suur-Sõjamäe", street_no=50, street_box="a",
            zip_code="11415",
            city=tallinn)
    yield A('HABAEE2X', 'EE202200221001178338')
    yield A('', 'EE781010220002715011 ')
    yield A('', 'EE321700017000231134')

    yield C('Electrabel Customer Solutions',
            "https://www.electrabel.be",
            country="BE",
            zip_code="1000",
            # city="Bruxelles",
            vat_id='BE 0476 306 127',
            street="Boulevard Simón Bolívar",
            street_no=34)
            # 1000 Bruxelles
    yield A('BPOTBEB1', 'BE46 0003 2544 8336')
    yield A('BPOTBEB1', 'BE81 0003 2587 3924')

    yield C('Ethias s.a.',
            "http://www.ethias.be",
            vat_id="BE 0404.484.654",
            street="Rue des Croisiers",
            street_no=24,
            country="BE",
            zip_code="4000")
    yield A('ETHIBEBB', 'BE79827081803833')
