#coding: utf-8

"""

This is originally based on 
http://www.davros.org/misc/iso3166.html

See also http://www.iso.org/iso/country_codes.htm

"""

import os
from xml.dom import minidom
#~ import logging
#~ logger = logging.getLogger('lino')

from lino.utils import ucsv
from lino.utils import dblogger as logger
from lino.utils.babel import babel_values, DEFAULT_LANGUAGE
from lino.modlib.countries.models import Country

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
FQHH 	ATF 	000 French Southern and Antarctic Territories (now split between AQ and TF)
DDDE 	DDR 	278 German Democratic Republic
GEHH 	GEL 	296 Gilbert & Ellice Islands (now split into Kiribati and Tuvalu)
JTUM 	JTN 	396 Johnston Island
MIUM 	MID 	488 Midway Islands
NTHH 	NTZ 	536 Neutral Zone (formerly between Saudi Arabia & Iraq)
NHVU 	NHB 	548 New Hebrides
PCHH 	PCI 	582 Pacific Islands (trust territory) (divided into FM, MH, MP, and PW)
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
    """
    http://users.pandora.be/bosteels/countries.xml
    """
    fn = os.path.join(os.path.dirname(__file__),'countries.xml')
    dom = minidom.parse(fn)
    #~ print dom.documentElement.__class__
    #~ print dom.documentElement
    for coun in dom.documentElement.getElementsByTagName('coun:country'):
        #~ print coun.toxml()
        #~ print c.attributes['coun:alpha2']
        names = {}
        for name in coun.getElementsByTagName('coun:name'):
            assert len(name.childNodes) == 1
            #~ print [n.data for n in ]
            #~ print name.firstChild.data
            names[str(name.attributes['lang'].value)] = name.firstChild.data
            
        kw = babel_values('name',**names)
        kw.update(
          isocode = coun.getElementsByTagName('coun:alpha2')[0].childNodes[0].data,
          iso3 = coun.getElementsByTagName('coun:alpha3')[0].childNodes[0].data,
          )
        
        if kw['name']:
            #~ kw.update(iso3=iso3)
            n += 1
            yield Country(**kw)
        else:
            logger.debug("%r : no name for default babel language %s",
                code,DEFAULT_LANGUAGE)
            
    for ln in TABLE2.splitlines():
        ln = ln.strip()
        if ln:
            code1, code2, code3, name = ln.split(None,3)
            n += 1
            yield Country(isocode=code1,name=name)
            
            
    #~ logger.info("Installed %d countries",n)
