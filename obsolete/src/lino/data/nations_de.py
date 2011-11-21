#coding: latin1

## Copyright Luc Saffre 2003-2005

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


#from lino.schemas.sprl.tables import Nations

def populate(q):
    s = """
#AC - Ascension Island 
AD - Andorra 
AE - Vereinigte Arabische Emirate 
AF - Afghanistan 
AG - Antigua und Barbuda 
AI - Anguilla 
AL - Albanien 
AM - Armenien 
AN - Niederländische Antillen 
AO - Angola 
AQ - Antarktis 
AR - Argentinien 
AS - Amerikanisch Samoa 
AT - Österreich 
AU - Australien
AW - Aruba 
AZ - Aserbaidschan

BA - Bosnien-Herzegowina
BB - Barbados
BD - Bangladesch
BE - Belgien
BF - Burkina Faso
BG - Bulgarien
BH - Bahrain
BI - Burundi
BJ - Benin
BM - Bermuda
BN - Brunei Darussalam
BO - Bolivien
BR - Brasilien
BS - Bahamas
BT - Bhutan
BV - Bouvet Island
BW - Botswana
BY - Belarus
BZ - Belize


CA - Kanada
CC - Cocos (Keeling) Islands
CD - Demokratische Republik Kongo (früher Zaire)
CF - Zentralafrikanische Republik
CG - Kongo
CH - Schweiz (Confoederatio Helvetica)
CI - Elfenbeinküste
CK - Cook Inseln
CL - Chile
CM - Kamerun
CN - China
CO - Kolumbien
CR - Costa Rica
CS - Tschechoslowakei (ehemalige)
CU - Kuba
CV - Kap Verde
CX - Weihnachtsinseln
CY - Zypern
CZ - Tschechien


DE - Deutschland
DJ - Djibouti
DK - Dänemark
DM - Dominika
DO - Dominikanische Republik
DZ - Algerien


EC - Ecuador
EE - Estland
EG - Ägypten
EH - Westsahara
ER - Eritrea
ES - Spanien
ET - Äthiopien


FI - Finnland
FJ - Fidschi
FK - Falkland-Inseln (Malvinas)
FM - Mikronesien
FO - Färöer
FR - Frankreich
FX - France, Metropolitan


GA - Gabun
GB - Großbritannien (UK)
GD - Grenada
GE - Georgien
GF - Französisch-Guyana
GH - Ghana
GI - Gibraltar
GL - Grönland
GM - Gambia
GN - Guinea
GP - Guadeloupe
GQ - Äquatorialguinea
GR - Griechenland
GS - S. Georgia and S. Sandwich Islands
GT - Guatemala
GU - Guam
GW - Guinea-Bissau
GY - Guyana

HK - Hong Kong
HM - Heard and McDonald Inseln
HN - Honduras
HR - Kroatien (Hrvatska)
HT - Haiti
HU - Ungarn

ID - Indonesien
IE - Irland
IL - Israel
IN - Indien
IO - British Indian Ocean Territory
IQ - Irak
IR - Iran
IS - Island
IT - Italien


JM - Jamaika
JO - Jordanien
JP - Japan


KE - Kenia
KG - Kirgisien
KH - Kambodscha
KI - Kiribati
KM - Komoren
KN - Saint Kitts und Nevis
KP - Nordkorea
KR - Südkorea
KW - Kuwait
KY - Kayman-Inseln
KZ - Kasachstan


LA - Laos
LB - Libanon
LC - Saint Lucia
LI - Liechtenstein
LK - Sri Lanka
LR - Liberia
LS - Lesotho
LT - Litauen
LU - Luxemburg
LV - Lettland
LY - Libyen


MA - Marokko
MC - Monaco
MD - Moldavien
MG - Madagaskar
MH - Marshall Inseln
MK - Ehemalige Jugoslawische Republik Mazedonien Siehe [2b]
ML - Mali
MM - Myanmar
MN - Mongolei
MO - Macao
MP - Northern Mariana Islands
MQ - Martinique
MR - Mauretanien
MS - Montserrat
MT - Malta
MU - Mauritius
MV - Malediven
MW - Malawi
MX - Mexiko
MY - Malaysia
MZ - Mosambik


NA - Namibia
NC - Neukaledonien
NE - Niger
NF - Norfolk Inseln
NG - Nigeria
NI - Nicaragua
NL - Niederlande
NO - Norwegen
NP - Nepal
NR - Nauru
NT - Neutrale Zone
NU - Niue
NZ - Neuseeland (Aotearoa)


OM - Oman


PA - Panama
PE - Peru
PF - Französisch Polynesien
PG - Papua-Neuguinea
PH - Philippinen
PK - Pakistan
PL - Polen
PM - St. Pierre und Miquelon
PN - Pitcairn
PR - Puerto Rico
#PS - Palästina (okkupierte Gebiete)
PT - Portugal
PW - Palau
PY - Paraguay


QA - Katar


RE - Reunion
RO - Rumänien
RU - Russland
RW - Ruanda


SA - Saudi Arabien
SB - Solomon Inseln
SC - Seychellen
SD - Sudan
SE - Schweden
SG - Singapur
SH - St. Helena
SI - Slowenien
SJ - Svalbard und Jan Mayen Islands
SK - Slowakei
SL - Sierra Leone
SM - San Marino
SN - Senegal
SO - Somalia
SR - Surinam
ST - São Tomé und Príncipe
SU - Ehemalige UdSSR
SV - El Salvador
SY - Syrien
SZ - Swasiland


TC - Turks and Caicos Islands
TD - Tschad
TF - French Southern Territories
TG - Togo
TH - Thailand
TJ - Tadschikistan
TK - Tokelau
TM - Turkmenistan
TN - Tunesien
TO - Tonga
TP - Osttimor
TR - Türkei
TT - Trinidad und Tobago
TV - Tuvalu
TW - Taiwan
TZ - Tansania


UA - Ukraine
UG - Uganda
UK - Vereinigtes Königreich
UM - US Minor Outlying Islands
US - Vereinigte Staaten von Amerika
UY - Uruguay
UZ - Usbekistan


VA - Vatikan (Heiliger Stuhl)
VC - Saint Vincent und die Grenadinen
VE - Venezuela
VG - Jungferninseln (British)
VI - Jungferninseln (U.S.)
VN - Vietnam
VU - Vanuatu


WF - Wallis und Futuna
WS - Samoa


YE - Jemen
YT - Mayotte
YU - Serbien und Montenegro (Jugoslawien, wird vermutlich demnächst geändert)


ZA - Südafrika
ZM - Sambia
ZR - Zaire (jetzt CD - Demokratische Republik Kongo)
ZW - Simbabwe

"""
    #NATIONS = sess.query(Nations)
    q.setBabelLangs('de')
    for l in s.splitlines():
        if len(l) and l[0] != '#':
            (id,name) = l.split('-',1)
            id=id.strip().lower()
            n = q.peek(id)
            n.lock()
            n.name = name.strip()
            n.unlock()
            #print __name__, n.name
            
    #sess.commit()
