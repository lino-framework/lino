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

from __future__ import unicode_literals
import re


abbrRE = re.compile("^(.*)\s*\((.*)\)\s*",re.DOTALL)



from lino.utils import babel

from lino import dd
Concept = dd.resolve_model('concepts.Concept')


"""
============================================ ================================================== =================================================
en                                           de                                                 fr
============================================ ================================================== =================================================
NR (National Register)                       NR (Nationalregister)                              RN (Régistre National)
PCSW (Public Centre for Social Welfare)      ÖSHZ (Öffentliches Sozialhilfezentrum)             CPAS (Centre Public d'Action Sociale)
SPIS (Social Integration Service)            DSBE (Dienst für Sozial-Berufliche Eingliederung)  SISP (Service d'insertion socio-professionnelle)
ISIP (Individual social integration project) VSE (Vertrag zur Sozialen Eingliederung)           PIIS (Projet Individualisé d'Intégration Sociale)
SSIN (Social Security Identification Number) INSS (Identifizierungsnummer der Sozialsicherheit) NISS (N° d'Identification de la Sécurité Sociale)
============================================ ================================================== =================================================
"""

def C(en,de,fr='',nl='',**kw):
    texts = dict(en=en,de=de,fr=fr,nl=nl)
    name = dict()
    abbr = dict()
    for lang in 'en','de','fr','nl':
        t = texts.get(lang)
        if t:
            mo = abbrRE.match(t)
            if mo:
                abbr[lang] = mo.group(1).strip()
                name[lang] = mo.group(2).strip()
                #~ kw['abbr_'+lang] = mo.group(1).strip()
                #~ kw['name_'+lang] = mo.group(2).strip()
            else:
                name[lang] = t
                #~ kw['name_'+lang] = t
    kw = babel.babel_values('name',**name)
    kw.update(babel.babel_values('abbr',**abbr))
    return Concept(**kw)
    
def objects():
    yield C("NR (National Register)",
      "NR (Nationalregister)",
      "RN (Registre National)",
      "RR (Rijksregister)")
    yield C("PCSW (Public Centre for Social Welfare)",
      "ÖSHZ (Öffentliches Sozialhilfezentrum)",
      "CPAS (Centre Public d'Action Sociale)",
      "OCMW (Openbaar Centrum voor Maatschappelijk Welzijn)")
    yield C("SPIS (Social Integration Service)",
      "DSBE (Dienst für Sozial-Berufliche Eingliederung)",
      "SISP (Service d'insertion socio-professionnelle)",
      "DSPI (Dienst Socio-Professionele Inschakeling)")
    yield C("ISIP (Individual social integration project)",
      "VSE (Vertrag zur Sozialen Eingliederung)",
      "PIIS (Projet Individualisé d'Intégration Sociale)")
    yield C("SSIN (Social Security Identification Number)",
      "INSS (Identifizierungsnummer der Sozialsicherheit)",
      "NISS (N° d'Identification de la Sécurité Sociale)")
    yield C("Debts consulting",
      "Schuldnerberatung",
      "Médiation de dettes",
      "Schuldbemiddeling ")
    yield C("Social Service",
      "Sozialdienst",
      "Service Social",
      "Sociale dienst")
    