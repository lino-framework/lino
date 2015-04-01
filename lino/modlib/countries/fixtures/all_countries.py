# coding: utf-8
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This fixture adds all known countries of the world to your
database.

Unlike the official `ISO 3133 <http://www.iso.org/iso/country_codes>`_
it features more languages, and it creates also codes for countries
that no longer exist.  It is not official at all. See also
:doc:`/topics/gpdn`.

The `countries.xml` is an unmodified copy of
http://users.pandora.be/bosteels/countries.xml

TODO: Estonian names. Maybe from
https://et.wikipedia.org/wiki/ISO_maakoodide_loend

`TABLE2` contains 4-letter codes for countries that no longer exist.
This is mostly based on <http://www.davros.org/misc/iso3166.html>,
but one country (DEDE) was added.

The :mod:`lino.modlib.statbel.countries.fixtures.inscodes` fixture,
extends this data by attaching Belgian INS codes to these countries.

"""

from __future__ import print_function

import os
from xml.dom import minidom
import logging
logger = logging.getLogger('lino')

from django.conf import settings

from lino.api import dd


TABLE2 = """
BQAQ 	ATB 	000 British Antarctic Territory
BUMM 	BUR 	104 Burma, Socialist Republic of the Union of
BYAA 	BYS 	112 Byelorussian SSR Soviet Socialist Republic
CTKI 	CTE 	128 Canton & Enderbury Islands
CSHH 	CSK 	200 Czechoslovakia, Czechoslovak Socialist Republic
DYBJ 	DHY 	204 Dahomey
NQAQ 	ATN 	216 Dronning Maud Land
TPTL 	TMP 	626 East Timor (was Portuguese Timor)
AIDJ 	AFI 	262 French Afars and Issas
FQHH 	ATF 	000 French Southern and Antarctic Territories \
(now split between AQ and TF)
DEDE 	??? 	??? German Federal Republic
DDDE 	DDR 	278 German Democratic Republic
GEHH 	GEL 	296 Gilbert & Ellice Islands (now split into Kiribati and Tuvalu)
JTUM 	JTN 	396 Johnston Island
MIUM 	MID 	488 Midway Islands
NTHH 	NTZ 	536 Neutral Zone (formerly between Saudi Arabia & Iraq)
NHVU 	NHB 	548 New Hebrides
PCHH 	PCI 	582 Pacific Islands (trust territory) \
(divided into FM, MH, MP, and PW)
PZPA 	PCZ 	000 Panama Canal Zone
SKIN 	SKM 	000 Sikkim
RHZW 	RHO 	716 Southern Rhodesia
PUUM 	PUS 	849 US Miscellaneous Pacific Islands
SUHH 	SUN 	810 USSR, Union of Soviet Socialist Republics
HVBF 	HVO 	854 Upper Volta, Republic of
VDVN 	VDR 	000 Viet-Nam, Democratic Republic of
WKUM 	WAK 	872 Wake Island
YDYE 	YMD 	720 Yemen, Democratic, People's Democratic Republic of
YUCS 	YUG 	891 Yugoslavia, Federal Republic of
ZRCD 	ZAR 	180 Zaire, Republic of
"""

#~ unused = """
#~ FX 	  FXX 	249 France, Metropolitan
#~ EH  	ESH 	732 Spanish Sahara (now Western Sahara)
#~ YU  	YUG 	890 Yugoslavia, Socialist Federal Republic of
#~ """

COUNTRIES = {}


def objects():

    n = 0
    Country = settings.SITE.modules.countries.Country
    """
    
    """
    fn = os.path.join(os.path.dirname(__file__), 'countries.xml')
    logger.debug("Reading %s", fn)
    dom = minidom.parse(fn)
    #~ print dom.documentElement.__class__
    #~ print dom.documentElement
    for coun in dom.documentElement.getElementsByTagName('coun:country'):
        names = {}
        for name in coun.getElementsByTagName('coun:name'):
            assert len(name.childNodes) == 1
            #~ print [n.data for n in ]
            #~ print name.firstChild.data
            names[str(name.attributes['lang'].value)] = name.firstChild.data

        kw = dd.babel_values('name', **names)
        iso2 = coun.getElementsByTagName('coun:alpha2')[0].childNodes[0].data
        if Country.objects.filter(pk=iso2).count() > 0:
            logger.debug("ISO code %r already exists %s", iso2, coun)
            continue
        kw.update(
            isocode=iso2,
            iso3=coun.getElementsByTagName(
                'coun:alpha3')[0].childNodes[0].data,
        )

        if not 'name' in kw:
            kw['name'] = names['en']
        if kw['name']:
            #~ kw.update(iso3=iso3)
            n += 1
            yield Country(**kw)
        else:
            logger.warning(
                "%r : no name for default site language %s",
                coun, settings.SITE.DEFAULT_LANGUAGE.django_code)

    for ln in TABLE2.splitlines():
        ln = ln.strip()
        if ln:
            code1, code2, code3, name = ln.split(None, 3)
            n += 1
            yield Country(isocode=code1, name=name)

    logger.info("Installed %d countries", n)

