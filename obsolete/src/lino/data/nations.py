#coding: latin1

## Copyright Luc Saffre 2004. This file is part of the Lino project.

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

"""
ISO country codes from
http://www.bcpl.net/~jspath/isocodes.html

"""

import csv
import os
#from lino.adamo.datatypes import DataVeto
from lino import adamo

#factbookDir = r'l:\doc\factbook'

factbookDir = os.path.dirname(__file__)

def populate(q):

    s = """\
ad     Andorra, Principality of
ae     United Arab Emirates
af     Afghanistan, Islamic State of
ag     Antigua and Barbuda
ai     Anguilla
al     Albania
am     Armenia
an     Netherlands Antilles
ao     Angola
aq     Antarctica
ar     Argentina
as     American Samoa
at     Austria
au     Australia
aw     Aruba
az     Azerbaidjan
ba     Bosnia-Herzegovina
bb     Barbados
bd     Bangladesh
be     Belgium
bf     Burkina Faso
bg     Bulgaria
bh     Bahrain
bi     Burundi
bj     Benin
bm     Bermuda
bn     Brunei Darussalam
bo     Bolivia
br     Brazil
bs     Bahamas
bt     Bhutan
bv     Bouvet Island
bw     Botswana
by     Belarus
bz     Belize
ca     Canada
cc     Cocos (Keeling) Islands
cf     Central African Republic
cd     Congo, The Democratic Republic of the
cg     Congo
ch     Switzerland
ci     Ivory Coast (Cote D'Ivoire)
ck     Cook Islands
cl     Chile
cm     Cameroon
cn     China
co     Colombia
cr     Costa Rica
cs     Former Czechoslovakia
cu     Cuba
cv     Cape Verde
cx     Christmas Island
cy     Cyprus
cz     Czech Republic
de     Germany
dj     Djibouti
dk     Denmark
dm     Dominica
do     Dominican Republic
dz     Algeria
ec     Ecuador
ee     Estonia
eg     Egypt
eh     Western Sahara
er     Eritrea
es     Spain
et     Ethiopia
fi     Finland
fj     Fiji
fk     Falkland Islands
fm     Micronesia
fo     Faroe Islands
fr     France
fx     France (European Territory)
ga     Gabon
gb     Great Britain
gd     Grenada
ge     Georgia
gf     French Guyana
gh     Ghana
gi     Gibraltar
gl     Greenland
gm     Gambia
gn     Guinea
gp     Guadeloupe (French)
gq     Equatorial Guinea
gr     Greece
gs     S. Georgia & S. Sandwich Isls.
gt     Guatemala
gu     Guam (USA)
gw     Guinea Bissau
gy     Guyana
hk     Hong Kong
hm     Heard and McDonald Islands
hn     Honduras
hr     Croatia
ht     Haiti
hu     Hungary
id     Indonesia
ie     Ireland
il     Israel
in     India
io     British Indian Ocean Territory
iq     Iraq
ir     Iran
is     Iceland
it     Italy
jm     Jamaica
jo     Jordan
jp     Japan
ke     Kenya
kg     Kyrgyz Republic (Kyrgyzstan)
kh     Cambodia, Kingdom of
ki     Kiribati
km     Comoros
kn     Saint Kitts & Nevis Anguilla
kp     North Korea
kr     South Korea
kw     Kuwait
ky     Cayman Islands
kz     Kazakhstan
la     Laos
lb     Lebanon
lc     Saint Lucia
li     Liechtenstein
lk     Sri Lanka
lr     Liberia
ls     Lesotho
lt     Lithuania
lu     Luxembourg
lv     Latvia
ly     Libya
ma     Morocco
mc     Monaco
md     Moldavia
mg     Madagascar
mh     Marshall Islands
mk     Macedonia
ml     Mali
mm     Myanmar
mn     Mongolia
mo     Macau
mp     Northern Mariana Islands
mq     Martinique (French)
mr     Mauritania
ms     Montserrat
mt     Malta
mu     Mauritius
mv     Maldives
mw     Malawi
mx     Mexico
my     Malaysia
mz     Mozambique
na     Namibia
nc     New Caledonia (French)
ne     Niger
nf     Norfolk Island
ng     Nigeria
ni     Nicaragua
nl     Netherlands
no     Norway
np     Nepal
nr     Nauru
nt     Neutral Zone
nu     Niue
nz     New Zealand
om     Oman
pa     Panama
pe     Peru
pf     Polynesia (French)
pg     Papua New Guinea
ph     Philippines
pk     Pakistan
pl     Poland
pm     Saint Pierre and Miquelon
pn     Pitcairn Island
pr     Puerto Rico
pt     Portugal
pw     Palau
py     Paraguay
qa     Qatar
re     Reunion (French)
ro     Romania
ru     Russian Federation
rw     Rwanda
sa     Saudi Arabia
sb     Solomon Islands
sc     Seychelles
sd     Sudan
se     Sweden
sg     Singapore
sh     Saint Helena
si     Slovenia
sj     Svalbard and Jan Mayen Islands
sk     Slovak Republic
sl     Sierra Leone
sm     San Marino
sn     Senegal
so     Somalia
sr     Suriname
st     Saint Tome (Sao Tome) and Principe
su     Former USSR
sv     El Salvador
sy     Syria
sz     Swaziland
tc     Turks and Caicos Islands
td     Chad
tf     French Southern Territories
tg     Togo
th     Thailand
tj     Tadjikistan
tk     Tokelau
tm     Turkmenistan
tn     Tunisia
to     Tonga
tp     East Timor
tr     Turkey
tt     Trinidad and Tobago
tv     Tuvalu
tw     Taiwan
tz     Tanzania
ua     Ukraine
ug     Uganda
uk     United Kingdom
um     USA Minor Outlying Islands
us     United States
uy     Uruguay
uz     Uzbekistan
va     Holy See (Vatican City State)
vc     Saint Vincent & Grenadines
ve     Venezuela
vg     Virgin Islands (British)
vi     Virgin Islands (USA)
vn     Vietnam
vu     Vanuatu
wf     Wallis and Futuna Islands
ws     Samoa
ye     Yemen
yt     Mayotte
yu     Yugoslavia
za     South Africa
zm     Zambia
zr     Zaire
zw     Zimbabwe
"""
    
    q.setBabelLangs('en')
    #from lino.schemas.sprl.tables import Nations
    #q = sess.query(Nations)
    for l in s.splitlines():
        (id,name) = l.split(None,1)
        row = q.appendRow(id=id.strip(),
                          name=name.strip())
        
    #q.commit()
    #print q._session.getBabelLangs()
##     print "1: ",\
##           q._session.db._supportedLangs
##     print "2: ", \
##           q._clist._context.getBabelLangs()
##     print "3: ", \
##           q._clist.getAtoms()

    belgique = q.peek('be')
    assert belgique.name == 'Belgium', repr(belgique.name)
    
    # set Nations.area per country:
    f = file(os.path.join(factbookDir,'2147rank.txt'))
    #f = file(os.path.join(factbookDir,'rankorder','2147rank.txt'))
    for l in f.readlines():
        a = l.split('\t')
        if len(a) == 1:
            pass
        else:
            (rank,country,area,date) = a
            if len(area) > 0:
                area = area.replace(',','')
                country = country.strip()
                n = q.findone(name=country)
                if n is not None:
                    n.lock()
                    n.area = int(area)
                    n.unlock()
                    
    # set Nations.population per country:
    f = file(os.path.join(factbookDir,'2119rank.txt'))
    for l in f.readlines():
        a = l.split('\t')
        if len(a) == 1:
            pass
        else:
            (rank,country,population,date) = a
            if len(area) > 0:
                population = population.replace(',','')
                country = country.strip()
                n = q.findone(name=country)
                if n is not None:
                    n.lock()
                    n.population = int(population)
                    n.unlock()


    if False:
        f = file(os.path.join(factbookDir,'world.csv'),'rb')
        r = csv.reader(f)
        r.next()
        for line in r:
            name = line[0]
            capital = line[1]
            #curr = line[3]
            isocode = line[4]
            dialcode = line[6]
            population = line[7].replace(',','')
            try:
                population = int(population)
            except ValueError:
                population = None
            if len(line) > 8:
                x = line[8].replace(',','')
                x = x.split()
                if len(x) > 0:
                    x = x[0]
                    try:
                        area = int(x)
                    except ValueError:
                        area = None
                else:
                    area = None

            print ( name , capital, ccy_code, dialcode,
                    population, area  )
                    
    
