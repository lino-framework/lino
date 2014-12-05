# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is Luc's personal collection of Belgian vocabulary.  It is
not complete enough to be of real benefit, but publicly available at
http://belref.lino-framework.org/

"""

from __future__ import unicode_literals
import re


abbrRE = re.compile("^(.*)\s*\((.*)\)\s*", re.DOTALL)


from lino import dd

Concept = dd.resolve_model('concepts.Concept')
Link = dd.resolve_model('concepts.Link')

from lino.modlib.concepts.models import LinkTypes


def C(en, de, fr='', nl='', jargon=None, obsoletes=None, **kw):
    texts = dict(en=en, de=de, fr=fr, nl=nl)
    name = dict()
    abbr = dict()
    for lang in 'en', 'de', 'fr', 'nl':
        t = texts.get(lang)
        if t:
            mo = abbrRE.match(t)
            if mo:
                abbr[lang] = mo.group(1).strip()
                name[lang] = mo.group(2).strip()
            else:
                name[lang] = t
    kw.update(dd.babel_values('name', **name))
    kw.update(dd.babel_values('abbr', **abbr))
    obj = Concept(**kw)
    yield obj
    if obsoletes is not None:
        if isinstance(obsoletes, dd.Model):
            obsoletes = [obsoletes]
        for obsoleted in obsoletes:
            yield Link(parent=obsoleted, child=obj, type=LinkTypes.obsoletes)

    if jargon is not None:
        if isinstance(jargon, dd.Model):
            jargon = [jargon]
        for domain in jargon:
            yield Link(parent=domain, child=obj, type=LinkTypes.jargon)


def objects():
    nsi = C(
        "NSI (National Statistics Institute)",
        "NIS (Nationales Institut für Statistik)",
        "INS (Institut National de Statistique)",
        "NIS (Nationaal Instituut voor Statistiek)")
    yield nsi
    yield C(
        "Statistics Belgium",
        "GDSWI (Generaldirektion Statistik und Wirtschaftsinformation)",
        "DGSIE (Direction générale Statistique et Information économique)",
        "ADSEI (Algemene Directie Statistiek en Economische Informatie)",
        obsoletes=nsi)
    yield C(
        "NR (National Register)",
        "NR (Nationalregister)",
        "RN (Registre National)",
        "RR (Rijksregister)")
    cpas = C(
        "PCSW (Public Centre for Social Welfare)",
        "ÖSHZ (Öffentliches Sozialhilfezentrum)",
        "CPAS (Centre Public d'Action Sociale)",
        "OCMW (Openbaar Centrum voor Maatschappelijk Welzijn)",
        is_jargon_domain=True)
    yield cpas
    yield C(
        "SPIS (Social Integration Service)",
        "DSBE (Dienst für Sozial-Berufliche Eingliederung)",
        "SISP (Service d'insertion socio-professionnelle)",
        "DSPI (Dienst Socio-Professionele Inschakeling)",
        jargon=cpas)
    yield C(
        "ISIP (Individual social integration project)",
        "VSE (Vertrag zur Sozialen Eingliederung)",
        "PIIS (Projet Individualisé d'Intégration Sociale)",
        jargon=cpas)
    yield C(
        "SSIN (Social Security Identification Number)",
        "INSS (Identifizierungsnummer der Sozialsicherheit)",
        "NISS (N° d'Identification de la Sécurité Sociale)",
        jargon=cpas)
    yield C(
        "Debts consulting",
        "Schuldnerberatung",
        "Médiation de dettes",
        "Schuldbemiddeling ")
    yield C(
        "Social Service",
        "Sozialdienst",
        "Service Social",
        "Sociale dienst")
    yield C(
        "LEA (Local Employment Agency)",
        "LBA (Lokale Beschäftigungsagentur)",
        "ALE (Agence locale pour l'emploi)",
        "PWA (Plaatselijk werkgelegenheidsagentschap)")
    yield C(
        "NEO (National Employment Office)",
        "LfA (Landesamt für Arbeitsbeschaffung)",
        "ONEM (Office national de l'emploi)",
        "RVA (Rijksdienst voor Arbeidsvoorziening)")
    yield C(
        "Head of household",
        "Haushaltsvorstand",
        "Chef de ménage",
        "Haushaltsvorstand")
