# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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

import os
import codecs
#~ import logging
#~ logger = logging.getLogger('lino')
from lino.utils import dblogger as logger

from lino.utils.babel import babel_values, DEFAULT_LANGUAGE
from lino.modlib.countries.models import Language


LANGUAGES = {}

"""
http://www.sil.org/iso639-3/iso-639-3_20100707.tab
http://www.sil.org/iso639-3/download.asp
"""
fn = os.path.join(os.path.dirname(__file__),'iso-639-3_20100707.tab')
n = 0
#~ for ln in file(fn).readlines():
for ln in codecs.open(fn,encoding="UTF-8").readlines():
    n += 1
    if ln:
      rec = ln.split('\t')
      if len(rec) != 8:
          logger.warning("Ignored line %d (len(rec) is %d)",n,len(rec))
      elif len(rec[0]) != 3:
          logger.warning("Ignored line %d",n)
      else:
          language_type = rec[5]
          if language_type == 'L':
              ref_name = rec[6]
              if ref_name:
                  code = rec[0]
                  if len(rec[1]) == 3:
                      code = rec[1]
                  LANGUAGES[code] = dict(en=ref_name,iso2=rec[3])
          else:
              logger.debug("Ignored line %d : language type is %r",n,language_type)


"""
German language names
ISO 639-2/B
http://www.d-nb.de/standardisierung/pdf/sprachencodes_dt.pdf
"""

german = u'''
Abchasisch abk
Aceh-Sprache ace
Acholi-Sprache ach
Adangme-Sprache ada
Adygisch ady
Ägyptisch egy
Afrihili afh
Afrikaans afr
Ainu-Sprache ain
Akan-Sprache aka
Akkadisch akk
Albanisch alb
Aleutisch ale
Algonkin-Sprachen (Andere) alg
Altäthiopisch gez
Altaisch alt
Altaische Sprachen (Andere) tut
Altenglisch ang
Altfranzösisch fro
Althochdeutsch goh
Altirisch sga
Alt-Newārī nwc
Altnorwegisch non
Altokzitanisch pro
Altpersisch peo
Amharisch amh
Anga-Sprache anp
Apachen-Sprachen apa
Arabisch ara
Aragonesisch arg
Aramäisch arc
Arapaho-Sprache arp
Arauka-Sprachen arn
Arawak-Sprachen arw
Armenisch arm
Aromunisch rup
Aserbeidschanisch aze
Assamesisch asm
Asturisch ast
Athapaskische Sprachen (Andere) ath
Australische Sprachen aus
Austronesische Sprachen (Andere) map
Avestisch ave
Awadhī awa
Awarisch ava
Aymará-Sprache aym
Bahasa Indonesia ind
Balinesisch ban
Baltische Sprachen (Andere) bat
Bambara-Sprache bam
Bamileke-Sprachen bai

Banda-Sprachen <Ubangi-Sprachen> bad
Bantusprachen (Andere) bnt
Basaa-Sprache bas
Baschkirisch bak
Baskisch baq
Batak-Sprache btk
Beach-la-mar bis
Bedauye bej
Belutschisch bal
Bemba-Sprache bem
Bengali ben
Berbersprachen (Andere) ber
Bhojpurī bho
Bihari (Andere) bih
Bikol-Sprache bik
Bilin-Sprache byn
Birmanisch bur
Blackfoot-Sprache bla
Bliss-Symbol zbl
Bokmål nob
Bosnisch bos
Braj-Bhakha bra
Bretonisch bre
Bugi-Sprache bug
Bulgarisch bul
Burjatisch bua
Caddo-Sprachen cad
Cebuano ceb
Chamorro-Sprache cha
Cham-Sprachen cmc
Cherokee-Sprache chr
Cheyenne-Sprache chy
Chibcha-Sprachen chb
Chinesisch chi
Chinook-Jargon chn
Chipewyan-Sprache chp
Choctaw-Sprache cho
Cree-Sprache cre
Dänisch dan
Dajakisch day
Dakota-Sprache dak
Danakil-Sprache aar
Darginisch dar
Delaware-Sprache del
Deutsch ger
Dinka-Sprache din
Dogrī doi
Dogrib-Sprache dgr
Drawidische Sprachen (Andere) dra
Duala-Sprachen dua


Dyula-Sprache dyu
Dzongkha dzo
Edo-Sprache bin
Efik efi
Einzelne andere Sprachen mis
Ekajuk eka
Elamisch elx
Elliceanisch tvl
Englisch eng
Erza-Mordwinisch myv
Esperanto epo
Estnisch est
Ewe-Sprache ewe
Ewondo ewo
Färöisch fao
Fante-Sprache fat
Fidschi-Sprache fij
Finnisch fin
Finnougrische Sprachen (Andere) fiu
Fon-Sprache fon
Französisch fre
Friesisch fry
Friulisch fur
Ful ful
Gälisch-Schottisch gla
Galicisch glg
Galla-Sprache orm
Ganda-Sprache lug
Ga-Sprache gaa
Gayo-Sprache gay
Gbaya-Sprache gba
Georgisch geo
Germanische Sprachen (Andere) gem
Gilbertesisch gil
Gondi-Sprache gon
Gorontalesisch gor
Gotisch got
Grebo-Sprache grb
Griechisch grc
Grönländisch kal
Guaraní-Sprache grn
Gujarātī-Sprache guj
Haida-Sprache hai
Haïtien (Haiti-Kreolisch) hat
Hamitosemitische Sprachen (Andere) afa
Haussa-Sprache hau
Hawaiisch haw
Hebräisch heb

Herero-Sprache her
Hethitisch hit
Hiligaynon-Sprache hil
Himachali him
Hindi hin
Hiri-Motu hmo
Hupa-Sprache hup
Iban-Sprache iba
Ibo-Sprache ibo
Ido ido
Ijo-Sprache ijo
Ilokano-Sprache ilo
Inarisaamisch smn
Indianersprachen, Nordamerika (Andere) nai
Indianersprachen, Südamerika (Andere) sai
Indianersprachen, Zentralamerika (Andere) cai
Indoarische Sprachen (Andere) inc
Indogermanische Sprachen (Andere) ine
Inguschisch inh
Interlingua ina
Interlingue ile
Inuktitut iku
Inupik ipk
Iranische Sprachen (Andere) ira
Irisch gle
Irokesische Sprachen iro
Isländisch ice
Italienisch ita
Jakutisch sah
Japanisch jpn
Javanisch jav
Jiddisch yid
Judenspanisch lad
Jüdisch-Arabisch jrb
Jüdisch-Persisch jpr
Kabardinisch kbd
Kabylisch kab
Kachin-Sprache kac
Kalmückisch xal
Kamba-Sprache kam
Kambodschanisch khm
Kannada kan
Kanuri-Sprache kau
Karakalpakisch kaa
Karatschaiisch-Balkarisch krc
Karelisch krl
Karenisch kar
Karibische Sprachen car
Kasachisch kaz

Kaschmiri kas
Kaschubisch csb
Katalanisch cat
Kaukasische Sprachen (Andere) cau
Kawi kaw
Kein linguistischer Inhalt zxx
Keltische Sprachen (Andere) cel
Khasi-Sprache kha
Khoisan-Sprachen (Andere) khi
Khotta mag
Kikuyu-Sprache kik
Kimbundu-Sprache kmb
Kirchenslawisch chu
Kirgisisch kir
Klingonisch tlh
Komi-Sprache kom
Kongo-Sprache kon
Konkani kok
Koptisch cop
Koreanisch kor
Kornisch cor
Korsisch cos
Kosraeanisch kos
Kpelle-Sprache kpe
Kreolische Sprachen; Pidginsprachen (Andere) crp
Kreolisch-Englisch (Andere) cpe
Kreolisch-Französisch (Andere) cpf
Kreolisch-Portugiesisch (Andere) cpp
Krimtatarisch crh
Kroatisch hrv
Kru-Sprachen (Andere) kro
Kumükisch kum
Kunstsprachen (Andere) art
Kurdisch kur
Kuschitische Sprachen (Andere) cus
Kutchin-Sprache gwi
Kutenai-Sprache kut
Kwanyama-Sprache kua
Kymrisch wel
Lahndā lah
Lalo-Sprache iii
Lamba-Sprache <Bantusprache> lam
Laotisch lao
Latein lat
Lesgisch lez
Lettisch lav
Limburgisch lim
Lingala lin
Litauisch lit

Luiseño-Sprache lui
Lulesaamisch smj
Lulua-Sprache lua
Lunda-Sprache lun
Luo-Sprache luo
Lushai-Sprache lus
Luxemburgisch ltz
Maduresisch mad
Maithili mai
Makassarisch mak
Makedonisch mac
Malagassi-Sprache mlg
Malaiisch may
Malayalam mal
Maledivisch div
Malinke-Sprache man
Maltesisch mlt
Mandaresisch mdr
Mandschurisch mnc
Manobo-Sprachen mno
Manx glv
Maori-Sprache mao
Marathi mar
Marschallesisch mah
Mārwārī mwr
Massai-Sprache mas
Maya-Sprachen myn
Mbundu-Sprache umb
Mehrere Sprachen mul
Meithei-Sprache mni
Mende-Sprache men
Miao-Sprachen hmn
Micmac-Sprache mic
Minangkabau-Sprache min
Mirandesisch mwl
Mittelenglisch enm
Mittelfranzösisch frm
Mittelhochdeutsch gmh
Mittelirisch mga
Mittelniederländisch dum
Mittelpersisch pal
Mohawk-Sprache moh
Mokscha-Sprache mdf
Mongolisch mon
Mongo-Sprache lol
Mon-Khmer-Sprachen (Andere) mkh
Mossi-Sprache mos
Mundasprachen (Andere) mun
Muskogisch mus
Nahuatl nah

Nauruanisch nau
Navajo-Sprache nav
Ndebele-Sprache <Simbabwe> nde
Ndebele-Sprache <Transvaal> nbl
Ndonga ndo
Neapel / Mundart nap
Nepali nep
Neugriechisch gre
Neumelanesisch tpi
Neuostaramäisch syr
Newārī new
Nias-Sprache nia
Nicht zu entscheiden und
Niederdeutsch nds
Niederländisch dut
Niedersorbisch dsb
Nigerkordofanische Sprachen (Andere) nic
Nilosaharanische Sprachen (Andere) ssa
Niue-Sprache niu
N'Ko nqo
Nkole-Sprache nyn
Nogaisch nog
Nordfriesisch frr
Nordsaamisch sme
Norwegisch nor
Nubische Sprachen nub
Nyamwezi-Sprache nym
Nyanja-Sprache nya
Nynorsk nno
Nyoro-Sprache nyo
Nzima-Sprache nzi
Obersorbisch hsb
Ojibwa-Sprache oji
Okzitanisch oci
Oraon-Sprache kru
Oriya-Sprache ori
Osage-Sprache osa
Osmanisch ota
Ossetisch oss
Osterinsel-Sprache rap
Ostfriesisch frs
Otomangue-Sprachen oto
Palau-Sprache pau
Pāli pli
Pampanggan-Sprache pam
Pandschabi-Sprache pan
Pangasinan-Sprache pag
Pangwe-Sprache fan
Papiamento pap
Papuasprachen (Andere) paa

Paschtu pus
Pedi-Sprache nso
Persisch per
Philippinisch-Austronesisch (Andere) phi
Phönikisch phn
Pilipino fil
Polnisch pol
Ponapeanisch pon
Portugiesisch por
Prākrit pra
Quechua-Sprache que
Rätoromanisch roh
Rājasthānī raj
Rarotonganisch rar
Romani <Sprache> rom
Romanische Sprachen (Andere) roa
Rotse-Sprache loz
Rumänisch rum
Rundi-Sprache run
Russisch rus
Rwanda-Sprache kin
Saamisch smi
Sakisch kho
Salish-Sprache sal
Samaritanisch sam
Samoanisch smo
Sandawe-Sprache sad
Sango-Sprache sag
Sanskrit san
Santālī sat
Sardisch srd
Sasak sas
Schan-Sprache shn
Schona-Sprache sna
Schottisch sco
Schwedisch swe
Schweizerdeutsch gsw
Selkupisch sel
Semitische Sprachen (Andere) sem
Serbisch srp
Serer-Sprache srr
Sidamo-Sprache sid
Sindhi-Sprache snd
Singhalesisch sin
Sinotibetische Sprachen (Andere) sit
Sioux-Sprachen (Andere) sio
Sizilianisch scn
Skoltsaamisch sms


Slave-Sprache den
Slawische Sprachen (Andere) sla
Slowakisch slo
Slowenisch slv
Sogdisch sog
Somali som
Songhai-Sprache son
Soninke-Sprache snk
Sorbisch (Andere) wen
Spanisch spa
Sranantongo srn
Südsaamisch sma
Süd-Sotho-Sprache sot
Sukuma-Sprache suk
Sumerisch sux
Sundanesisch sun
Susu sus
Swahili swa
Swasi-Sprache ssw
Syrisch syc
Tadschikisch tgk
Tagalog tgl
Tahitisch tah
Tamašeq tmh
Tamil tam
Tatarisch tat
Telugu-Sprache tel
Temne-Sprache tem
Tereno-Sprache ter
Tetum-Sprache tet
Thailändisch tha
Thaisprachen (Andere) tai
Tibetisch tib
Tigre-Sprache tig
Tigrinja-Sprache tir
Tiv-Sprache tiv
Tlingit-Sprache tli
Tokelauanisch tkl
Tonga <Bantusprache, Sambia> tog
Tongaisch ton
Trukesisch chk
Tschagataisch chg
Tschechisch cze
Tscheremissisch chm
Tschetschenisch che
Tschuwaschisch chv
Tsimshian-Sprache tsi
Tsonga-Sprache tso
Tswana-Sprache tsn
Türkisch tur
Tumbuka-Sprache tum


Tupi-Sprache tup
Turkmenisch tuk
Tuwinisch tyv
Twi-Sprache twi
Udmurtisch udm
Ugaritisch uga
Uigurisch uig
Ukrainisch ukr
Ungarisch hun
Urdu urd
Usbekisch uzb
Vai-Sprache vai
Venda-Sprache ven
Vietnamesisch vie
Volapük vol
Wakash-Sprachen wak
Walamo-Sprache wal
Wallonisch wln
Waray war
Washo-Sprache was
Weißrussisch bel
Wolof-Sprache wol
Wotisch vot
Xhosa-Sprache xho
Yao-Sprache <Bantusprache> yao
Yapesisch yap
Yoruba-Sprache yor
Ypik-Sprachen ypk
Zande-Sprachen znd
Zapotekisch zap
Zazaki zza
Zeichensprachen sgn
Zenaga zen
Zhuang zha
Zulu-Sprache zul
Zuñi-Sprache zun
'''


# copied from http://fr.wikipedia.org/wiki/Liste_des_codes_ISO_639-1
french = u"""
aa	aar	aar	Afar	Afaraf	Afar	
ab	abk	abk	Abkhaze	Аҧсуа	Abkhazian	
ae	ave	ave	Avestique	Avesta	Avestan	
af	afr	afr	Afrikaans	Afrikaans	Afrikaans	
ak	aka	aka + 2	Akan	Akan	Akan	
am	amh	amh	Amharique	አማርኛ	Amharic	
an	arg	arg	Aragonais	Aragonés	Aragonese	
ar	ara	ara + 30	Arabe	 العربية	Arabic	L'arabe standard est arb en ISO 639-3
as	asm	asm	Assamais	অসমীয়া	Assamese	
av	ava	ava	Avar	авар мацӀ ; магӀарул мацӀ	Avaric	
ay	aym	aym + 2	Aymara	Aymar aru	Aymara	
az	aze	aze + 2	Azéri	Azərbaycan dili	Azerbaijani	
ba	bak	bak	Bachkir	башҡорт теле	Bashkir	
be	bel	bel	Biélorusse	Беларуская	Belarusian	
bg	bul	bul	Bulgare	български език	Bulgarian	
bh	bih	--	Bihari	भोजपुरी	Bihari	Code de langue collective pour le bhojpuri, le magahi et le maithili
bi	bis	bis	Bichelamar	Bislama	Bislama	
bm	bam	bam	Bambara	Bamanankan	Bambara	
bn	ben	ben	Bengalî	বাংলা	Bengali	
bo	tib/bod	bod	Tibétain	བོད་ཡིག	Tibetan	
br	bre	bre	Breton	Brezhoneg	Breton	
bs	bos	bos	Bosnien	Bosanski jezik	Bosnian	
ca	cat	cat	Catalan	Català	Catalan	
ce	che	che	Tchétchène	нохчийн мотт	Chechen	
ch	cha	cha	Chamorro	Chamoru	Chamorro	
co	cos	cos	Corse	Corsu ; lingua corsa	Corsian	
cr	cre	cre + 6	Cri	ᓀᐦᐃᔭᐍᐏᐣ	Cree	
cs	cze/ces	ces	Tchèque	Česky ; čeština	Czech	
cu	chu	chu	Vieux slave	Словѣньскъ	Church Slavic	
cv	chv	chv	Tchouvache	чӑваш чӗлхи	Chuvash	
cy	wel/cym	cym	Gallois	Cymraeg	Welsh	
da	dan	dan	Danois	Dansk	Danish	
de	ger/deu	deu	Allemand	Deutsch	German	
dv	div	div	Divehi	 ދިވެހި	Divehi	
dz	dzo	dzo	Dzongkha	རྫོང་ཁ	Dzongkha	
ee	ewe	ewe	Ewe	Ɛʋɛgbɛ	Ewe	
el	gre/ell	ell	Grec moderne	Ελληνικά	Greek	
en	eng	eng	Anglais	English	English	
eo	epo	epo	Espéranto	Esperanto	Esperanto	
es	spa	spa	Espagnol	Español; castellano	Spanish	
et	est	est	Estonien	Eesti keel	Estonian	
eu	baq/eus	eus	Basque	Euskara	Basque	
fa	per/fas	fas + 2	Persan	 فارسی	Persian	
ff	ful	ful + 9	Peul	Fulfulde	Fulah	
fi	fin	fin	Finnois	Suomen kieli	Finnish	
fj	fij	fij	Fidjien	Vosa Vakaviti	Fijian	
fo	fao	fao	Féringien	Føroyskt	Faroese	
fr	fre/fra	fra	Français	Français ; langue française	French	
fy	fry	fry + 3	Frison	Frysk	Western Frisian	
ga	gle	gle	Irlandais	Gaeilge	Irish	
gd	gla	gla	Écossais	Gàidhlig	Scottish Gaelic	
gl	glg	glg	Galicien	Galego	Galician	
gn	grn	grn + 5	Guarani	Avañe'ẽ	Guarani	
gu	guj	guj	Gujarâtî	ગુજરાતી	Gujarati	
gv	glv	glv	Mannois	Ghaelg	Manx	
ha	hau	hau	Haoussa	 هَوُسَ	Hausa	
he	heb	heb	Hébreu	 עברית	Hebrew	
hi	hin	hin	Hindî	हिन्दी ; हिंदी	Hindi	
ho	hmo	hmo	Hiri motu	Hiri Motu	Hiri Motu	
hr	scr/hrv	hrv	Croate	Hrvatski	Croatian	
ht	hat	hat	Créole haïtien	Kreyòl ayisyen	Haitian	
hu	hun	hun	Hongrois	Magyar	Hungarian	
hy	arm/hye	hye	Arménien	Հայերեն	Armenian	
hz	her	her	Herero	Otjiherero	Herero	
ia	ina	ina	Interlingua	Interlingua	Interlingua	
id	ind	ind	Indonésien	Bahasa Indonesia	Indonesian	
ie	ile	ile	Occidental	Interlingue	Interlingue	
ig	ibo	ibo	Igbo	Igbo	Igbo	
ii	iii	iii	Yi	ꆇꉙ	Sichuan Yi	
ik	ipk	ipk + 2	Inupiaq	Iñupiaq ; Iñupiatun	Inupiaq	
io	ido	ido	Ido	Ido	Ido	
is	ice/isl	isl	Islandais	Íslenska	Icelandic	
it	ita	ita	Italien	Italiano	Italian	
iu	iku	iku + 2	Inuktitut	ᐃᓄᒃᑎᑐᑦ	Inuktitut	
ja	jpn	jpn	Japonais	日本語 (にほんご)	Japanese	
jv	jav	jav	Javanais	Basa Jawa	Javanese	
ka	geo/kat	kat	Géorgien	ქართული	Georgian	
kg	kon	kon + 3	Kikongo	KiKongo	Kongo	
ki	kik	kik	Kikuyu	Gĩkũyũ	Kikuyu	
kj	kua	kua	Kuanyama	Kuanyama	Kwanyama	
kk	kaz	kaz	Kazakh	Қазақ тілі	Kazakh	
kl	kal	kal	Kalaallisut	Kalaallisut ; kalaallit oqaasii	Kalaallisut	
km	khm	khm	Khmer	ភាសាខ្មែរ	Khmer	
kn	kan	kan	Kannara	ಕನ್ನಡ	Kannada	
ko	kor	kor	Coréen	한국어 (韓國語) ; 조선말 (朝鮮語)	Korean	
kr	kau	kau + 3	Kanouri	Kanuri	Kanuri	
ks	kas	kas	Kashmiri	कश्मीरी ; كشميري	Kashmiri	
ku	kur	kur + 3	Kurde	Kurdî ; كوردی	Kurdish	
kv	kom	kom + 2	Komi	коми кыв	Komi	
kw	cor	cor	Cornique	Kernewek	Cornish	
ky	kir	kir	Kirghiz	кыргыз тили	Kirghiz	
la	lat	lat	Latin	Latine ; lingua latina	Latin	
lb	ltz	ltz	Luxembourgeois	Lëtzebuergesch	Luxembourgish	
lg	lug	lug	Ganda	Luganda	Ganda	
li	lim	lim	Limbourgeois	Limburgs	Limburgish	
ln	lin	lin	Lingala	Lingála	Lingala	
lo	lao	lao	Lao	ພາສາລາວ	Lao	
lt	lit	lit	Lituanien	Lietuvių kalba	Lithuanian	
lu	lub	lub	Tchiluba	cilubà	Luba-Katanga	
lv	lav	lav	Letton	Latviešu valoda	Latvian	
mg	mlg	mlg + 10	Malgache	Fiteny malagasy	Malagasy	
mh	mah	mah	Marshallais	Kajin M̧ajeļ	Marshallese	
mi	mao/mri	mri	Māori de Nouvelle-Zélande	Te reo Māori	Māori	
mk	mac/mkd	mkd	Macédonien	македонски јазик	Macedonian	
ml	mal	mal	Malayalam	മലയാളം	Malayalam	
mn	mon	mon + 2	Mongol	Монгол	Mongolian	
mo	mol	mol	Moldave	лимба молдовеняскэ	Moldavian	
mr	mar	mar	Marâthî	मराठी	Marathi	
ms	may/msa	msa + 13	Malais	Bahasa Melayu ; بهاس ملايو	Malay	
mt	mlt	mlt	Maltais	Malti	Maltese	
my	bur/mya	mya	Birman	ဗမာစာ	Burmese	
na	nau	nau	Nauruan	Ekakairũ Naoero	Nauru	
nb	nob	nob	Norvégien Bokmål	Norsk bokmål	Norwegian Bokmål	
nd	nde	nde	Ndébélé du Nord	isiNdebele	North Ndebele	
ne	nep	nep	Népalais	नेपाली	Nepali	
ng	ndo	ndo	Ndonga	Owambo	Ndonga	
nl	dut/nld	nld	Néerlandais	Nederlands	Dutch	
nn	nno	nno	Norvégien Nynorsk	Norsk nynorsk	Norwegian Nynorsk	
no	nor	nor + 2	Norvégien	Norsk	Norwegian	
nr	nbl	nbl	Ndébélé du Sud	Ndébélé	South Ndebele	
nv	nav	nav	Navajo	Diné bizaad ; Dinékʼehǰí	Navajo	
ny	nya	nya	Chichewa	ChiCheŵa ; chinyanja	Chichewa	
oc	oci	oci + 5	Occitan	Occitan	Occitan	
oj	oji	oji + 7	Ojibwé	ᐊᓂᔑᓈᐯᒧᐎᓐ	Ojibwa	
om	orm	orm + 4	Oromo	Afaan Oromoo	Oromo	
or	ori	ori	Oriya	ଓଡ଼ିଆ	Oriya	
os	oss	oss	Ossète	Ирон æвзаг	Ossetian	
pa	pan	pan	Panjâbî	ਪੰਜਾਬੀ ; پنجابی	Panjabi	
pi	pli	pli	Pâli	पािऴ	Pāli
pl	pol	pol	Polonais	Polski	Polish	
ps	pus	pus + 3	Pachto	 پښتو	Pashto	
pt	por	por	Portugais	Português	Portuguese	
qu	que	que + 44	Quechua	Runa Simi ; Kichwa	Quechua	
rm	roh	roh	Romanche	Rumantsch grischun	Raeto-Romance	
rn	run	run	Kirundi	kiRundi	Kirundi	
ro	rum/ron	ron	Roumain	Română	Romanian	
ru	rus	rus	Russe	русский язык	Russian	
rw	kin	kin	Kinyarwanda	Kinyarwanda	Kinyarwanda	
sa	san	san	Sanskrit	संस्कृतम्	Sanskrit	
sc	srd	srd + 4	Sarde	sardu	Sardinian	
sd	snd	snd	Sindhi	सिन्धी ; سنڌي، سندھی	Sindhi	
se	sme	sme	Same du Nord	Davvisámegiella	Northern Sami	
sg	sag	sag	Sango	Yângâ tî sängö	Sango	
si	sin	sin	Cingalais	සිංහල	Sinhalese	
sk	slo/slk	slk	Slovaque	Slovenčina	Slovak	
sl	slv	slv	Slovène	Slovenščina	Slovene	
sm	smo	smo	Samoan	Gagana fa'a Samoa	Samoan	
sn	sna	sna	Shona	chiShona	Shona	
so	som	som	Somali	Soomaaliga ; af Soomaali	Somali	
sq	alb/sqi	sqi + 4	Albanais	Shqip	Albanian	
sr	scc/srp	srp	Serbe	српски језик	Serbian	
ss	ssw	ssw	Siswati	SiSwati	Swati	
st	sot	sot	Sotho du Sud	seSotho	Sotho	
su	sun	sun	Soundanais	Basa Sunda	Sundanese	
sv	swe	swe	Suédois	Svenska	Swedish	
sw	swa	swa + 2	Swahili	Kiswahili	Swahili	
ta	tam	tam	Tamoul	தமிழ்	Tamil	
te	tel	tel	Télougou	తెలుగు	Telugu	
tg	tgk	tgk	Tadjik	тоҷикӣ ; toğikī ; تاجیکی	Tajik	
th	tha	tha	Thaï	ไทย	Thai	
ti	tir	tir	Tigrinya	ትግርኛ	Tigrinya	
tk	tuk	tuk	Turkmène	Türkmen ; Түркмен	Turkmen	
tl	tgl	tgl	Tagalog	Tagalog	Tagalog	
tn	tsn	tsn	Tswana	seTswana	Tswana	
to	ton	ton	Tongien	faka Tonga	Tonga	
tr	tur	tur	Turc	Türkçe	Turkish	
ts	tso	tso	Tsonga	xiTsonga	Tsonga	
tt	tat	tat	Tatar	татарча ; tatarça ; تاتارچا	Tatar	
tw	twi	twi	Twi	Twi	Twi	
ty	tah	tah	Tahitien	Reo Mā`ohi	Tahitian	
ug	uig	uig	Ouïghour	Uyƣurqə ; ئۇيغۇرچ	Uighur	
uk	ukr	ukr	Ukrainien	українська мова	Ukrainian	
ur	urd	urd	Ourdou	 اردو	Urdu	
uz	uzb	uzb + 2	Ouzbek	O'zbek ; Ўзбек ; أۇزبېك	Uzbek	
ve	ven	ven	Venda	tshiVenḓa	Venda	
vi	vie	vie	Vietnamien	Tiếng Việt	Vietnamese	
vo	vol	vol	Volapük	Volapük	Volapük	
wa	wln	wln	Wallon	Walon	Walloon	
wo	wol	wol	Wolof	Wollof	Wolof	
xh	xho	xho	Xhosa	isiXhosa	Xhosa	
yi	yid	yid + 2	Yiddish	 ייִדיש	Yiddish	
yo	yor	yor	Yoruba	Yorùbá	Yoruba	
za	zha	zha + 2	Zhuang	Saɯ cueŋƅ ; Saw cuengh	Zhuang	
zh	chi/zho	zho + 13	Chinois	中文, 汉语, 漢語	Chinese	
zu	zul	zul	Zoulou	isiZulu	Zulu
"""



n = 0
for ln in german.splitlines():
    n += 1
    if ln:
        ln = ln.strip()
        if not ln[-4:-3].isspace():
            logger.warning("german %d: syntax",n)
        else:
            code = ln[-3:]
            name = ln[:-4]
            d = LANGUAGES.get(code,None)
            if d is None:
                pass
                #~ logger.warning("%r in german but not english",code)
                #~ d = dict(en=name)
                #~ LANGUAGES[code] = d
            else:
                d.update(de=name)
                
n = 0
for ln in french.splitlines():
    n += 1
    if ln:
        ln = ln.strip()
        rec = ln.split('\t')
        if len(rec) < 6:
            logger.warning("Ignored french:%d:%s (len(rec) is %d)",n,ln,len(rec))
        code = rec[1]
        if len(code) == 7:
            if code[3:4] == '/':
                code = code[:3]
            else:
                code = None
        if code:
            name = rec[3]
            d = LANGUAGES.get(code,None)
            if d is not None:
                d.update(fr=name)

def objects():
    n = 0
    for code,kw in LANGUAGES.items():
        iso2 = kw['iso2']
        kw = babel_values('name',**kw)
        if kw['name']:
            n += 1
            kw.update(iso2=iso2)
            yield Language(id=code,**kw)
        else:
            logger.debug("%r : no name for default babel language %s",code,DEFAULT_LANGUAGE)
    logger.info("Installed %d languages",n)
          