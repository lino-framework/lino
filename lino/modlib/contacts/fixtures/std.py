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

from django.db import models
from django.conf import settings

from django.utils.translation import ugettext as _

from lino.utils.instantiator import Instantiator
from lino.utils.babel import babel_values, DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES


companyType = Instantiator('contacts.CompanyType',"abbr name").build
roletype = Instantiator('contacts.RoleType',"name").build

# thanks to http://belgium.angloinfo.com/countries/belgium/businesses.asp
# see also http://en.wikipedia.org/wiki/Types_of_business_entity

COMPANY_TYPES_FORMAT = 'en nl fr de'
COMPANY_TYPES_TEXT = u"""
Public Limited Company    | NV (Naamloze Vennootschap)   | SA (Société Anonyme) |  AG (Aktiengesellschaft)
Limited Liability Company | BVBA (Besloten Vennootschap met Beperkte Aansprakelijkheid)  | SPRL (Société Privée à Responsabilité Limitée) | PGmbH (Private Gesellschaft mit beschränkter Haft)
One-person Private Limited Company | EBVBA (Eenpersoons Beslotenvennootschap met Beperkte Aansprakelijkheid) | SPRLU (Société d'Une Personne à Responsabilité Limitée) |
Cooperative Company with Limited Liability | CVBA (Cooperatieve Vennootschap met Beperkte Aansprakelijkheid) | SCRL (Société Coopérative à Responsabilité Limitée) | 
Cooperative Company with Unlimited Liability | CVOA (Cooperatieve Vennootschap met Onbeperkte Aansprakelijkheid) | SCRI (Société Coopérative à Responsabilité Illimitée) |
General Partnership | Comm VA (Commanditaire Vennootschap op Aandelen | SNC (Société en Nom Collectif) |
Limited Partnership | Comm V (Gewone Commanditaire Vennootschap) | SCS (Société en Commandite Simple) |
Non-stock Corporation | Maatschap | Société de Droit Commun | Gesellschaft öffentlichen Rechts
Charity/Company established for social purposes | VZW (Vereniging Zonder Winstoogmerk) | ASBL (Association sans But Lucratif) | V.o.G. (Vereinigung ohne Gewinnabsicht)

Cooperative Company | CV (Cooperatieve Vennootschap) | SC (Société Coopérative) | Genossenschaft
Company | Firma | Société | Firma
Public service |  | Service Public | Öffentlicher Dienst
Ministry |  | Ministère | Ministerium
School |  | école | Schule
"""
COMPANY_TYPES = []

def parse(s):
    a = s.split("(",1)
    if len(a) == 2:
        name = a[1].strip()
        if name.endswith(")"):
            return dict(abbr=a[0].strip(),name=name[:-1])
    s = s.strip()
    if not s: return {}
    return dict(name=s)
    
LANGS = {}

for i, lang in enumerate(COMPANY_TYPES_FORMAT.split()):
    if lang in AVAILABLE_LANGUAGES:
    #~ if lang == default_language() or (lang in settings.BABEL_LANGS):
        LANGS[lang] = i
        
#~ print LANGS        

for ln in COMPANY_TYPES_TEXT.splitlines():
    if ln and ln[0] != "#":
        a = ln.split('|')
        if len(a) != 4:
            raise Exception("Line %r has %d fields (expected 4)" % len(a))
        d = dict()
        for lang,i in LANGS.items():
            kw = parse(a[i])
            if lang == DEFAULT_LANGUAGE:
                d.update(kw)
            else:
                for k,v in kw.items():
                    d[k+'_'+lang] = v
        def not_empty(x):
            return x
        #~ print d
        if d.has_key('name'):
            if filter(not_empty, d.values()): # if there's at least one non-empty value
                COMPANY_TYPES.append(d)
        

def objects():

    #~ yield companyType('Firma','Firma')
    #~ yield companyType('asbl','asbl')
    #~ yield companyType('A.S.B.L.','A.S.B.L.')
    #~ yield companyType('sprl','sprl')
    #~ yield companyType('GmbH','GmbH')
    #~ yield companyType('AG','AG')
    #~ yield companyType('S.A.','S.A.')
    #~ yield companyType('S.C.','S.C.')
    #~ yield companyType('V.o.G.','V.o.G.')
    #~ yield companyType('G.o.E.','G.o.E.')
    #~ yield companyType('A.S.B.L.','Association sans but lucratif')
    #~ yield companyType('Maison','Maison')
    #~ yield companyType('Fachklinik','Fachklinik')
    #~ yield companyType("Centre d'Accueil d'Urgence","Centre d'Accueil d'Urgence")
    
    #~ yield companyType(**babel_values('name',
        #~ en=u"Public Limited Company",
        #~ nl=u'NV (Naamloze Vennootschap)',
        #~ fr=u'SA (Société Anonyme)',
        #~ de=u"AG (Aktiengesellschaft)"))
    
    for ct in COMPANY_TYPES:
        yield companyType(**ct)
        
    yield roletype(**babel_values('name',en="Manager",fr=u'Gérant',de=u"Geschäftsführer",et=u"Manager"))
    yield roletype(**babel_values('name',en="Director",fr=u'Directeur',de=u"Direktor",et=u"Direktor"))
    yield roletype(**babel_values('name',en="Secretary",fr=u'Sécrétaire',de=u"Sekretär",et=u"Sekretär"))
    yield roletype(**babel_values('name',en="IT Manager",fr=u'Gérant informatique',de=u"EDV-Manager",et=u"IT manager"))
