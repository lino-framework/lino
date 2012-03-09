# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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

from lino.modlib.vocbook.fr import French, Autre, Nom, NomPropre, Adjectif, Numerique, Verbe, NomGeographique
from lino.modlib.vocbook.et import Estonian
from lino.modlib.vocbook.base import Book, FR, M, F, ET, PRON, GEON, GEOM, GEOF

book = Book(French,Estonian,u"Kutsealane prantsuse keel kokadele")

Pronounciation = book.add_section(1,u"Hääldamine",intro=u"""
Esimeses osas keskendume hääldamisele.
Eesmärk ei ole meelde jätma kõik sõnad, mida tuuakse näiteks, 
vaid et õpilane oskaks neid ette lugeda õigesti hääldades 
ka siis kui hääldamiskirjeldust on peidetud.
""")
Vocabulary = book.add_section(2,u"Sõnavara",intro=u"""
Teises osa hakkame õpima sõnavara,
oletades et hääldamine on enam vähem selge.
""")

Pronounciation.add_lesson(u"Hääldamiskirjeldus", u"""
Prantsuse keele hääldamine tuleb pähe õppida koos sõnavaraga.
Sellepärast paneme sõnade taha nurksulgudes ([]) *hääldamiskirjeldused*.

Hääldamiskirjeldustes kasutame kohandatud
`X-SAMPA <http://fr.wiktionary.org/wiki/Annexe:Prononciation/fran%C3%A7ais>`_
variant, mis on eestlastele intuitiivsem õpida 
kui puhas X-SAMPA või 
`IPA <http://en.wiktionary.org/wiki/Wiktionary:IPA>`_ 
(International Phonetic Alphabet).

Üldiselt loed lihtsalt seda, mis on nurksulgudes, välja arvatud
mõned kirjatähed, mis ei ole olemas eesti keeles, need tuleb õpida:

==== ================== =================== ===============================
täht selgitus           näided
==== ================== =================== ===============================
[ə]  tumm e             Lott\ **e**         **je** [žə], **ne** [nə]
[o]  kinnine o          L\ **oo**\ ne       **mot** [mo], **beau** [boo]
[O]  avatud o           L\ **o**\ tte       **bonne** [bOn], **mort** [mOOr]
[ö]  kinnine ö          l\ **öö**\ ve       **feu** [föö], **peu** [pöö]
[Ö]  avatud ö           ingl. "g\ *ir*\ l"  **beurre** [bÖÖr], **jeune** [žÖÖn]
[w]  ingl. k. "where"   ingl. "\ **w**\ e"  **trois** [trw'a], **foie** [fw'a]
[O~] palatiseeritud [O]                     **bonjour** [bO~'žuur], **mon** [mO~]
[A~] palatiseeritud [A]                     **tante** ['tA~tə] **bilan** [bi'lA~], **prendre** ['prA~drə]
[Ö~] palatiseeritud [Ö]                     **un** [Ö~], **parfum** [par'fÖ~]
[Ä~] palatiseeritud ä                       **chien** [šiä~], **rien** [riä~]
==== ================== =================== ===============================

- Pikad kaashälikud on topelt, lihtne kaashäälik on lühike.

- Hääldamiskirjelduses paneme apostrofi (') rõhutatud silbi ette.
  (Prantsuse keeles on tavaliselt rõhk viimasel silbil.)
  


""")


Pronounciation.add_lesson(u"Tuntud sõnad", u"""
Mõned sõnad, mida te juba teate.
Tutvumine hääldamiskirjaga.
""")
Pronounciation.parse_words(None,u"""
la soupe [sup] : supp
la carte [kart] : kaart
à la carte [ala'kart] : menüü järgi
le vase [vaaz] : vaas
la douche [duš] : dušš
le disque [disk] : ketas
merci [mär'si] : aitäh
le garage [ga'raaž] : garaaž
le journal [žur'nal] : päevik | ajaleht
le choc [žok] : šokk | löök
""")
Pronounciation.add_after(u"""
- Tähekombinatsioon **ou** hääldatakse [u]
- **e** sõna lõpus kaob ära
- raske on teada, kas täishäälikuid hääldatakse 
  lühikesena või pikana.
- "Mesilashäälikud" on **s**, **š**, **z** ja **ž**.
  Nende erinevus on prantsuse keeles tähtis.
  
  =========== ===========================
  terav       pehme
  =========== ===========================
  **s**\ upp  **z**\ oom
  **š**\ okk  **ž**\ urnaal, **ž**\ anre
  =========== ===========================
 
""")

Pronounciation.add_lesson(u"Artikkel", u"""
Prantsuse keeles on kõikidel asjadel oma sugu.
Näiteks laud on naissoost, telefon on meessoost.
""")
Pronounciation.parse_words(Autre,u"""
le [lə] : (määrav meessoost artikkel)
la [la] : (määrav naissoost artikkel)
""")



Pronounciation.add_lesson(u"u", u"""
Kirjatäht **u**
(siis kui see pole teise täishäälikuga koos)
hääldatakse [ü] või [üü]
""")
Pronounciation.parse_words(Nom,u"""
le bureau [bü'roo] : büroo
le bus [büs] : buss
le mur [müür] : sein | müür
la puce [püs] : kirp
le jus [žü] : mahl
le but [büt] : eesmärk
la pute [püt] : hoor
le sucre ['sükrə] : suhkur
""")


Pronounciation.add_lesson(u"Umbmäärane artikkel", u"""
Inglise keeles on olemas määrav 
artikkel **the** ja umbmäärane artikel **a**.
Olenevalt kontekstist kasutatakse kas see või teine.
Näiteks
"I am **a** man from Vigala"
ja 
"I am **the** man you need".

Sama asi tehakse ka prantsuse keeles, ja kuna seal on 
veel mees-/naissoo erinevus, on meil nüüd juba neli artiklit:

========== ====== ==========
sugu       määrav umbmäärane
========== ====== ==========
meessoost  le     un 
naissoost  la     une
========== ====== ==========

Sõnavara tabellites on tavaliselt nimisõnade 
ees *määrav* artikkel, sest *un* on algajatele 
raske hääldada.

""")
Pronounciation.parse_words(Autre,u"""
un [Ö~] : (umbmäärane meessoost artikkel)
une [ün] : (umbmäärane naissoost artikkel)
""")



Pronounciation.add_lesson(u"*au* ja *eau*", 
u"""
Tähekombinatsioon **au** hääldatakse **[o]** või **[oo]**.
Kui **e** on veel ees, siis see sulab ka nendega kokku ja pole 
mingit erinevust kuulda.
""")
Pronounciation.parse_words(None,u"""
une auberge [o'bäržə] : võõrastemaja
un auteur [o'tÖÖr] : autor
le château [ža'too] : loss
le bateau [ba'too] : laev
une eau [oo] : vesi
""")

Pronounciation.add_lesson(u"Kui *le* ja *la* muutuvad *l'*-ks", 
u"""
Kes arvab ära, miks on eelmises peatükis ikkagi mõnikord umbmäärane artikkel?

Vastus: kui sõna algab täishäälikuga, siis kaob artiklitest *le* ja *la* 
viimane täht ära ja nad muutuvad  mõlemad *l'*-ks.
mis on 

""")


Pronounciation.add_lesson(u"Rõhutud, aga lühike!", u"""
Rõhutatud täishäälikud ei ole sellepärast tingimata pikad.
Prantsuse keeles tuleb tihti ette, et sõna lõpeb *lühikese* 
täishäälikuga.
""")
Pronounciation.parse_words(Nom,u"""
le menu [mə'nü] : menüü
le chocolat [šoko’la] : šokolaad
le plat [pla] : roog | kauss
le cinéma [sine’ma] : kino
le paradis [para'di] : paradiis
""")


Pronounciation.add_lesson(u"y", u"""
Kirjatäht **y** 
hääldatakse alati [i] ja mitte kunagi [ü]
""")
Pronounciation.parse_words(Nom,u"""
le cygne ['sinjə] : luik
le système [sis'tääm] : süsteem
le mythe [mit] : müütos
""")


Pronounciation.add_lesson(u"ai", 
u"""
Tähekombinatsioon **ai** hääldatakse **[ä]** või **[ää]**,
v.a. siis kui järgneb **l**.

""")
Pronounciation.parse_words(Nom,u"""
la maison [mä'zO~] : maja
le domaine [do'mään] : domeen
la fraise [frääz] : maasikas
la paire [päär] : paar
""")
Pronounciation.parse_words(Adjectif,u"""
frais [frä] | fraiche [fräš] : värske
""")



Pronounciation.add_lesson(u"ail", 
u"""
Tähekombinatsioon **ail** hääldatakse **[aj]**.
""")
Pronounciation.parse_words(Nom,u"""
l'ail (m) [aj] : küüslauk
le travail [tra'vaj] : töö
le détail [detaj] : detail
""")
Pronounciation.parse_words(NomGeographique,u"""
Versailles [ver'saj] : Versailles
""")




Pronounciation.add_lesson(u"ou", u"""
Tähekombinatsioon **ou** hääldatakse **[u]** või **[uu]**.
""")
Pronounciation.parse_words(None,u"""
oui [wi] : jah
le cours [kuur] : kursus | tund (koolis)
le cou [ku] : kael
le goût [gu] : maitse
le chou [šu] : kapsas
le loup [lu] : hunt
un ours [urs] : karu
le journal [žur'nal] : päevik
""")

if False:
    Pronounciation.parse_words(None,u"""
    la loupe [lup] : luup
    la joue [žuu] : põsk
    le jour [žuur] : päev
    court (m) [kuur] : lühike
    mou (m) [mu] : pehme
    """)
    Pronounciation.parse_words(NomPropre,u"""
    Winnetou [winə'tu] : (isegi maailmakuulsa apatši pealiku nime hääldavad prantslased valesti)
    """)


Pronounciation.add_lesson(u"oi", 
u"""
Tähekombinatsioon **oi** hääldatakse peaaegu alati **[wa]**.
Hääldamiskirja **w** täht on "ülipehme", 
nagu nt. inglise sõnades "week", "wow", "where".
""")
Pronounciation.parse_words(Autre,u"""
voilà [vwa'la] : näe siin 
trois [trwa] : kolm
bonsoir [bO~'swaar] : head õhtut
au revoir [orə'vwaar] : nägemiseni
""")
Pronounciation.parse_words(Nom,u"""
le roi [rwa] : kuningas
la loi [lwa] : seadus
un oiseau [wa'zoo] : lind
le bois [bwa] : puu (materjal) | mets
le poids [pwa] : kaal
le toit [twa] : katus
le doigt [dwa] : sõrm
""")

#~ Pronounciation.parse_words(Autre,u"""
#~ Il était une fois [iletätünə'fwa] : Oli üks kord
#~ le boudoir [bud'waar] : buduaar
#~ """)

Pronounciation.add_lesson(u"Jah ja ei", u"""
""")
Pronounciation.parse_words(None,u"""
oui [wi] : jah
non [nO~] : ei
""")


Pronounciation.add_lesson(u"ui", 
u"""
Tähekombinatsioon **ui** hääldatakse tavaliselt 
**[wi]** või **[wii]**
(mida kirjutatakse vahest ka **[üi]** või **[üii]**).

""")
Pronounciation.parse_words(None,u"""
la suite [swit] : järg | tagajärg | rida, kord | saatjaskond
bonne nuit [bOn'nwi] : head ööd
la cuisine [kwi'zin] : köök
je cuis [žə kwi] : ma keedan
je suis [žə swi] : ma olen | ma järgnen
""")

#~ Pronounciation.parse_words(None,u"""
#~ l'huile (f) [wil] : õli
#~ cuire [kwiir] : keetma
#~ suivre ['swiivrə] : järgima
#~ la cuillère [kwi'jäär] : lusikas
#~ """)


Pronounciation.add_lesson(u"un ja um", 
u"""
Tähekombinatsioonid **um** ja **un** hääldatakse **[Ö~]**,
v.a. siis kui järgneb täishäälik või teine **m** / **n**.
""")
Pronounciation.parse_words(Nom,u"""
le parfum [par'fÖ~] : hea lõhn v. maitse
""")
Pronounciation.parse_words(NomPropre,u"""
Verdun [vär'dÖ~] : -
""")
Pronounciation.parse_words(Adjectif,u"""
brun [brÖ~] | brune [brün] : pruun
aucun [o'kÖ~] | aucune [o'kün] : mitte üks
parfumé [parfü'mee] | parfumée [parfü'mee] : parfümeeritud
""")

#~ chacun [ža'kÖ~] | chacun [ža'kün] : igaüks



Pronounciation.add_lesson(u"Lotte ja Loone", u"""
Lotte *O* on lühike ja *avatud*, Loone oma on pikk ja *kinnine*.
Eesti keeles on lühike *O* alati avatud, ja pikk *O* on alati kinnine.
Prantsuse keeles on lisaks ka kombinatsioonid *avatud ja pikk* 
ning *kinnine ja lühike*.

Hääldamiskirjelduses on olemas *kinnine* [o] (väikese tähega)
ja *avatud* [O] (suure tähega).
""")
Pronounciation.parse_words(Autre,u"""
je donne [dOn] : ma annan
je dors [dOOr] : ma magan
""")
Pronounciation.parse_words(Nom,u"""
la mort [mOOr] : surm
le mot [mo] : sõna
le boulot [bu'lo] : töö (kõnekeel)
le bouleau [bu'loo] : kask
le bureau [bü'roo] : büroo
""")


Pronounciation.add_lesson(u"Frère Jacques", 
u"""
| Frère Jacques, frère Jacques,
| dormez-vous? Dormez-vous? 
| Sonnez les matines, sonnez les matines
| ding, dang, dong! Ding, dang, dong!
""")
Pronounciation.parse_words(NomPropre,u"""
Jacques [žaak] : Jaak
""")
Pronounciation.parse_words(None,u"""
le frère [fräär] : vend
dormez-vous? [dOrme'vu] : kas Te magate?
Sonnez les matines [sO'ne lä ma'tinə] : lööge hommikukellad
""")

Pronounciation.add_lesson(u"Minu onu...", 
u"""
| Mon tonton et ton tonton sont deux tontons,
| mon tonton tond ton tonton 
| et ton tonton tond mon tonton.
| Qu'est-ce qui reste?

""")
Pronounciation.parse_words(None,u"""
mon [mO~] : minu
ton [tO~]: sinu
ils sont [sO~]: nad on
""")
Pronounciation.parse_words(Numerique,u"""
deux [döö] : kaks
""")
Pronounciation.parse_words(Nom,u"""
un tonton [tO~'tO~] : onu
""")
Pronounciation.parse_words(Verbe,u"""
tondre [tO~drə] : pügama
rester [räs'tee] : üle jääma
""")
Pronounciation.parse_words(None,u"""
Qu'est-ce qui reste? [käski'räst?] : Mis jääb üle?
""")


#~ """
#~ le nôtre ['nootrə] : meie oma
#~ """

Pronounciation.add_lesson(u"eu", u"""
Tähekombinatsioon **eu** hääldatakse tavaliselt **[öö]** või **[ÖÖ]**.
Heli **[ö]** on eesti keeles alati *kinnine* (hääldamiskirjelduses väikese tähega). 
Prantsuse keeles on lisaks *avatud* **[ÖÖ]** (hääldamiskirjelduses suure tähega).
Ja nende erinevus on oluline.

Hääldamiskirjelduses on *kinnine* ö *väikese* tähega, 
*avatud* Ö *suure* tähega.
""")
Pronounciation.parse_words(Nom,u"""
le feu [föö] : tuli
le neveu [nə'vöö] : onupoeg | tädipoeg
je veux [žə vöö] : ma tahan
""")
Pronounciation.parse_words(Autre,u"""
neutre (mf) ['nöötrə] : neutraalne
""")
Pronounciation.parse_words(Numerique,u"""
neuf [nÖf] : üheksa
""")
Pronounciation.parse_words(Nom,u"""
le professeur [profesÖÖr] : professor
le beurre [bÖÖr] : või
la peur [pÖÖr] : hirm
""")

Pronounciation.add_lesson(u"œ", u"""
""")
Pronounciation.parse_words(Nom,u"""
le nœud [nöö] : sõlm
le cœur [kÖÖr] : süda
le chœur [kÖÖr] : koor (laulu-)
le bœuf [bÖff] : härg
un œuf [Öf] : muna
une œuvre [ÖÖvrə] : töö, teos
le *hors d'œuvre [hOOr 'dÖÖvrə] : eelroog
""")





Pronounciation.add_lesson(u"Palatiseeritud O", 
u"""
Tähekombinatsioonid **om** ja **on** hääldatakse tavaliselt **[O~]**,
välja arvatud siis kui järgneb täishäälik või teine **m** või **n**.
""")
Pronounciation.parse_words(Nom,u"""
le salon [sa’lO~] : salong (= uhke tuba)
un oncle [O~klə] : onu
""")
Pronounciation.parse_words(None,u"""
bonjour [bO~'žuur] : tere | head päeva | tere hommikust
bonne nuit [bOn'nwi] : head ööd
bon appétit [bOnappe'ti] : head isu
""")



Pronounciation.add_lesson(u"Palatiseeritud A", 
u"""
Tähekombinatsioonid **an** ja **en** (mitte *i* taga) 
hääldatakse tavaliselt **[A~]**.
""")
Pronounciation.parse_words(Nom,u"""
le rendez-vous [rA~de’vu] : kohtumine
un an [A~] : aasta
la lampe [lA~pə] : lamp
le commentaire [komA~’täär] : märkus, kommentar
le centre ['sA~trə] : keskus
le genre [žA~rə] : žanre
un enfant [A~'fA~] : laps
""")

Pronounciation.add_lesson(u"Palatiseeritud Ä", 
u"""
Tähekombinatsioon **in** ja **en** hääldatakse tavaliselt **[Ä~]**.
Tähekombinatsioon **ien** hääldatakse tavaliselt **[iÄ~]**.
""")
Pronounciation.parse_words(Nom,u"""
le bassin [ba'sÄ~] : bassein
le pain [pÄ~] : sai | leib
le vin [vÄ~]: vein
le coin [kwÄ~] : nurk
le chien [šiÄ~] : koer
une information [Ä~formasjO~] : informatsioon
""")
Pronounciation.parse_words(Autre,u"""
rien [riÄ~] : ei midagi
bien [biÄ~] : hästi
besoin [bə'zwÄ~] : vaja
""")




Pronounciation.add_lesson(u'il', 
u"""
Tähekombinatsioon **il** (sõna lõpus ja kaashääliku taga)
hääldatakse kas **[i]** või **[il]**.
""")
Pronounciation.parse_words(None,u"""
il [il] : tema
le persil [pär'sil] : petersell
subtil (m) [süp'til] : peen, subtiilne
un outil [u'ti] : tööriist
le fusil [fü'zi] : püss
gentil (m) [žA~'ti] : armas
un exil [äg'zil] : eksiil
""")

Pronounciation.add_lesson(u'*eil* ja *eille*', 
u"""
Tähekombinatsioon **eil** hääldatakse **[eij]**.
""")
Pronounciation.parse_words(None,u"""
le réveil [re'veij] : äratuskell
le soleil [so'leij] : päike
la merveille [mär'veij] : ime
merveilleux [märvei'jöö] : imeline
le réveillon [revei'jO~] : vana-aasta õhtu söök
la groseille [gro'zeij] : sõstras (punane v. valge) | tiker
vieille (f) [vjeij] : vana
la veille [veij] : eesõhtu
""")
Pronounciation.add_lesson(u"ueil", 
u"""
Tähekombinatsioon **ueil** hääldatakse **[Öj]**.
""")
Pronounciation.parse_words(None,u"""
un accueil [a'kÖj] : vastuvõtt
le chevreuil [šəv'rÖj] : metskits
un écureuil [ekü'rÖj] : orav
""")

Pronounciation.add_lesson(u"ille", u"""
""")
Pronounciation.parse_words(None,u"""
la bille [biij] : kuul
une anguille [A~'giij] : angerjas
la myrtille [mir'tiij] : mustikas
la famille [fa'miij] : perekond
tranquillle [trA~kiij] : rahulik
la cuillère [kwi'jäär] : lusikas
le million [mi'jO~] : miljon
""")










Pronounciation.add_lesson(u"h", u"""
Kirjatäht **h** ei hääldata kunagi.
""")
Pronounciation.parse_words(Nom,u"""
le hélicoptère [elikop'täär] : helikopter
le hôtel [o'täl] : hotell
le autel [o'täl] : altar
""")

Pronounciation.add_lesson(u"h aspiré", u"""
Kuigi kirjatähe **h** ei hääldata kunagi,
on neid kaks tüüpi: «h muet» (tumm h) 
ja «h aspiré» (sisse hingatud h).
Viimane tähistatakse sõnaraamatutes tärniga (*).
Erinevus koosneb selles, kuidas nad liituvad eesoleva sõnaga.
Artiklitest "le" ja "la" kaob "e" või "a" 
siis kui järgnev sõna algab täishäälikuga.
""")
Pronounciation.parse_words(Nom,u"""
le hélicoptère [elikop'täär] : helikopter
le hôtel [o'täl] : hotell
le homme [Om] : mees
le *haricot [ari'ko] : uba
le *héros [e'ro] : kangelane
le *hibou [i'bu] : öökull
""")





Pronounciation.add_lesson(u"ch", u"""
Tähekombinatsioon **ch** hääldatakse tavaliselt **[š]** 
ja mõnikord (kreeka päritolu sõnades) **[k]**,
ja mitte kunagi **[tš]**.

""")
Pronounciation.parse_words(Nom,u"""
le chat [ša] : kass
le chien [šjÄ~] : koer
la chèvre ['šäävrə] : kits
la biche [biš] : emahirv
un achat [a'ša] : ost
la chambre [šA~mbrə] : tuba
une chope [žOp] : õlu
le parachute [para'šüt] : langevari
le Christe [krist] : Kristus
le chœur [kÖÖr] : koor (laulu-)
le psychologue [psiko'lOOgə] : psüholoog
""")


Pronounciation.add_lesson(u"gn", u"""
Tähekombinatsioon **gn** prantsuse keeles hääldatakse 
peaaegu alati **[nj]**.
""")
Pronounciation.parse_words(None,u"""
magnifique (nf) [manji'fik] : surepärane
le cognac [kon'jak] : konjak
la ligne ['linjə] : liin | rida
le signe ['sinjə] : märk
le signal [sin'jal] : signaal
la besogne [bə'zOnjə] : töö | tegu | ülesanne
""")
Pronounciation.parse_words(Verbe,u"""
soigner [swan'jee] : ravima | hoolitsema
""")
Pronounciation.parse_words(NomGeographique,u"""
Avignon [avin'jO~] : -
""")





Pronounciation.add_lesson(u"j", 
u"""
Kirjatäht **j** hääldatakse **[ž]** (ja mitte [dž]).
""")
Pronounciation.parse_words(None,u"""
majeur [mažÖÖr] : suurem
je [žə] : mina
jamais [ža'mä] : mitte iialgi
jaune (mf) [žoon] : kollane
""")
Pronounciation.parse_words(NomPropre,u"""
Josephe [žo'zäf] : Joosep
""")


Pronounciation.add_lesson(u"g", 
u"""
Kirjatäht **g** hääldatakse 

- [ž] kui järgneb **e**, **i** või **y**,
- [g] kui järgneb **a**, **o**, **u**.

Kui hääldamine on [gi], [ge], [gə], [gä] või [gi], siis lisatakse tumm **u**.
""")
Pronounciation.parse_words(None,u"""
le gorille [go'rij] : gorilla
la giraffe [ži'raf] : kaelkirjak
la gazelle [ga'zäl] : gazell?
le guépard [ge'paar] : gepard
le guide [giid] : reisijuht
la guitare [gi'taar] : kitarr
le gymnase [žim'naaz] : gümnaasium
le juge [žüüž] : kohtunik
la géologie [žeolo'žii] : geoloogia
général [žene'ral] : üldine
la guerre [gäär] : sõda
""")










Pronounciation.add_lesson(u"C", u"""
Kirjatäht **c** hääldatakse kas **[k]** või **[s]**:

- **[s]** siis kui järgneb e, i, y
- **[k]** siis kui järgneb a, o, u või kaashäälik

""")
Pronounciation.parse_words(None,u"""
le câble ['kaablə] : kaabel
la comédie [kome'dii] : komöödia
le comble ['kO~blə] : kõrgeim v. ülim aste
la cure [küür] : kuur
la cible ['siiblə] : märklaud
le certificat [särtifi'ka] : tsertifikaat
la cire [siir] : vaha
le centre ['sA~trə] : keskus
le cygne ['sinjə] : luik
la classe [klas] : klass
la croûte [krut] : koorik
un acacia [akasj'a] : akaatsia (põõsas)
""")
Pronounciation.parse_words(NomPropre,u"""
octobre [ok'tOObrə] : oktoober
""")
Pronounciation.parse_words(Numerique,u"""
cinq [sÄ~k] : viis
""")

Pronounciation.add_lesson(u"ç", u"""
ç
""")
Pronounciation.parse_words(None,u"""
la leçon [lə~sO]~: lektsioon
la rançon [rA~sO]~: lunaraha
le reçu [rə'sü] : kviitung
le maçon [ma'sO~] : müürsepp
""")


Pronounciation.add_lesson(u"b ja p", u"""
b ja p on prantsuse keeles selgelt erinevad.
""")
Pronounciation.parse_words(None,u"""
la bière [bjäär] : õlu
la pierre [pjäär] : kivi
le bon [bO~] : tšekk | talong
le pont [pO~] : sild
le bon ton [bO~'tO~] : viisakus
le ponton [pO~'tO~] : pontoon (nt. pontoonsild)
la peau [poo] : nahk
beau (m.) : ilus
""")



Pronounciation.add_lesson(u"d ja t", u"""
d ja t on prantsuse keeles selgelt erinevad.
""")
Pronounciation.parse_words(None,u"""
le don [dO~] : annetus
le ton [tO~] : toon
le centre ['sA~trə] : keskus
la cendre ['sA~drə] : tuhk
je donne [dOn] : ma annan
la tonne [tOn] : tonn
""")

Pronounciation.add_lesson(u"g ja k", u"""
g ja k on prantsuse keeles selgelt erinevad.
""")
Pronounciation.parse_words(None,u"""
le gond [gO~] : uksehing
le con [kO~] : loll
la gare [gaar] : raudteejaam
le car [kaar] : reisibuss
car [kaar] : sest
le garçon [gar'sO~] : poiss
Qui est Guy? [ki ä gi] : Kes on Guy?
""")




Pronounciation.add_lesson(u"[äär]", u"""
Kui kuuled [äär], siis kirjutad kas **ère**, **aire**, **ère**, **erre** või **er**.
""")
Pronounciation.parse_words(None,u"""
le père [päär] : isa
la paire [päär] : paar
le maire [määr] : linnapea
la mère [määr] : ema
la mer [määr] : meri
amer (m) [a'määr] : kibe
la bière [bjäär] : õlu
la pierre [pjäär] : kivi
la terre [täär] : muld
""")



Pronounciation.add_lesson(u"v ja f", u"""
Ettevaatust, **v** ei ole **f**!
""")
Pronounciation.parse_words(None,u"""
vous [vu] : teie
fou [fu] : hull
# vous êtes fous [vu'zäät fu] : te olete lollid
je veux [žə vöö] : ma tahan
le feu [föö] : tuli
la fille [fii] : tüdruk | tütar
la vie [vii] : elu
la fin [fÄ~] : lõpp
le vin [vÄ~] : vein
""")

Pronounciation.add_lesson(u"Ahv pole märk", u"""
Ettevaatust, **gn** ei ole **ng**!
""")
Pronounciation.parse_words(Nom,u"""
le singe [sÄ~ž] : ahv
le signe ['sinjə] : märk
le linge [lÄ~ž] : pesu
la ligne ['linjə] : liin | rida
""")

Pronounciation.add_lesson(u"Sugu on oluline", u"""
Siin mõned näited, et sugu pole sugugi ebatähtis.
""")
Pronounciation.parse_words(Nom,u"""
le père [päär] : isa
la paire [päär] : paar
le maire [määr] : linnapea
la mère [määr] : ema
le tour [tuur] : tiir
la tour [tuur] : torn
le mur [müür] : sein | müür
la mûre [müür] : põldmari
le cours [kuur] : kursus | tund (koolis)
la cour [kuur] : õu, hoov | kohus
""")






Pronounciation.add_lesson(u"Ebaloogilised", u"""
Siin mõned sõnad, mille hääldamine on "ebaloogiline"
""")
Pronounciation.parse_words(Nom,u"""
la ville [vil] : linn
mille [mil] : tuhat
""")


Pronounciation.add_lesson(u"Ära aja segamini!", u"""
Mõned ilusad harjutused veel.
""")
Pronounciation.parse_words(Autre,u"""
ces ingrédients [säz Ä~gre'djA~] : need koostisained
c'est un crétin [sätÖ~ kre’tÄ~] : ta on kretiin
je dors [žə dOOr] : ma magan
j'ai tort [že tOOr] : ma eksin
""")
Pronounciation.parse_words(Nom,u"""
la jambe [žA~mbə] : jalg
la chambre [šA~mbrə] : tuba
un agent [la' žA~] : agent
le chant [lə šA~] : laul
les gens [žA~] : inimesed, rahvas
les chants [šA~] : laulud
""")



Vocabulary.add_lesson(u"Tervitused", u"""
""")
Vocabulary.parse_words(Autre,u"""
salut [sa'lü] : tervist
bonjour [bO~'žuur] : tere | head päeva | tere hommikust
bonsoir [bO~'swaar] : head õhtut
bonne nuit [bOn'nwi] : head ööd
au revoir [orə'vwaar] : nägemiseni

Monsieur [məs'jöö] : härra
Madame [ma'dam] : proua
Mademoiselle [madəmwa'zel] : preili

Comment tu t'appelles? [ko'mA~ tü ta'päl] : Kuidas on sinu nimi?
Je m'appelle... [zə ma'päl] : Minu nimi on...
Comment vas-tu? [ko'mA~va'tü] : Kuidas sul läheb?

s'il vous plaît [silvu'plä] : palun (Teid)
s'il te plaît [siltə'plä] : palun (Sind)
merci [mär'si] : aitäh
""")


Vocabulary.add_lesson(u"Prantsuse automargid", u"""
""",columns=[FR,PRON],show_headers=False)
Vocabulary.parse_words(NomPropre,u"""
Peugeot [pö'žo] : - 
Citroën [sitro'än] : - 
Renault [re'noo] : - 
""")



Vocabulary.add_lesson(u"Prantsuse eesnimed", u"""
""")
Vocabulary.parse_words(NomPropre,u"""
Albert [al'bäär] : - 
André [A~'dree] : Andre
Anne [anə] : Anne
Bernard [bär'naar] : - 
Catherine [kat'rin] : Katrin
Charles [šarl] : Karl
François [frA~'swa] : -
Isabelle [iza'bäl] : Isabel
Jacques [žaak] : Jaak
Jean [žA~] : Jaan
Luc [lük] : Luukas
Marie [ma'rii] : Maria
Paul [pOl] : Paul
Philippe [fi'lip] : Filip
Pierre [pjäär] : Peeter
""")



Vocabulary.add_lesson(u"Katame lauda!", u"""
""")
Vocabulary.parse_words(Nom,u"""
la table ['taablə] : laud
la chaise [šääz] : tool
le couteau [ku'too] : nuga
la fourchette [fur'šet] : kahvel
la cuillère [kwi'jäär] : lusikas
une assiette [as'jät] : taldrik
le verre [väär] : klaas
la tasse [tas] : tass
le plat [pla] : kauss
""")

Vocabulary.add_lesson(u"Liha (üld)", u"""
""")
Vocabulary.parse_words(Nom,u"""
la boucherie [bušə'rii] : lihakauplus, lihakarn
la viande [vjA~də] : liha
la volaille [vo'laij] : linnuliha
le gibier [žibiee] : jahiloomad
le poisson [pwa'sO~] : kala
""")

Vocabulary.add_lesson(u"Liha (kehaosad)", u"""
""")
Vocabulary.parse_words(Nom,u"""
un os [os] : kont
la côte [koot] : ribi
le dos [do] : selg
la langue [lA~gə] : keel
les abats [a'ba] : (maks,süda, neerud, keel, jalad)
le foie [fu'a] : maks
# les tripes [trip] : 
le cœur [kÖÖr] : süda
le rognon [ron'jO~] : neer
la cervelle [ser'vell] : aju
""")

Vocabulary.add_lesson(u"Taluloomad", u"""
""")
Vocabulary.parse_words(Nom,u"""
la chèvre ['šäävrə] : kits
la brebis [brə'bis] : lammas
le porc [pOOr] : siga
le cochon [ko'šO~] : siga
le cheval [šə'val] : hobune
la vache [vaš] : lehm
le taureau [to'roo] : pull
le bœuf [bÖff] : härg
la souris [su'ri] : hiir
""")

Vocabulary.add_lesson(u"Metsloomad", u"""
""")
Vocabulary.parse_words(Nom,u"""
la chasse [šas] : jaht
le chasseur [ša'sÖÖr] : jahimees
le chevreuil [šəv'rÖj] : metskits
le cerf [säär] : hirv
la biche [biš] : emahirv
un élan [e'lA~] : põder
le lapin [lapÄ~] : küünik
le lièvre [li'äävrə] : jänes
le renard [rə'naar] : rebane
un écureuil [ekü'rÖj] : orav
le blaireau [blä'roo] : mäger | habemeajamispintsel
le *hérisson [eri'sO~] : siil
une hermine [är'min] : hermeliin
la martre ['martrə] : nugis
la belette [bə'lät] : nirk  
le loup [lu] : hunt
un ours [urs] : karu
le lynx [lÄ~ks] : ilves
le sanglier [sA~gli'e] : metssiga
le marcassin [marka'sÄ~] : metsseapõrsas
""")

# belette : nirk 

Vocabulary.add_lesson(u"Põdral maja", u"""
| Dans sa maison un grand cerf 
| regardait par la fenêtre
| un lapin venir à lui         
| et frapper ainsi.
| «Cerf, cerf, ouvre moi
| ou le chasseur me tuera!»    
| «Lapin, lapin entre et viens 
| me serrer la main.»          
""")
Vocabulary.parse_words(Verbe,u"""
regarder [rəgar'dee] : vaatama
ouvrir [uv'riir] : avama
tuer [tü'ee] : tapma
serrer [sä'ree] : suruma
""")
Vocabulary.parse_words(Nom,u"""
la maison [mä'zO~] : maja
la fenêtre [fə'näätrə] : aken
le cerf [säär] : hirv
le lapin [lapÄ~] : küünik
le chasseur [ša'sÖÖr] : jahimees
la main [mÄ~] : käsi
""")

Vocabulary.add_lesson(u"Linnud", u"""
""")
Vocabulary.parse_words(Nom,u"""
la poule [pul] : kana
le poulet [pu'lä] : tibu | kanapoeg
une oie [wa] : hani
le dindeon [dÄ~dO~] : kalkun
la dinde [dÄ~də] : emakalkun
le pigeon [pi'žO~] : tuvi
""")

Vocabulary.add_lesson(u"Kalad", u"""
""")
Vocabulary.parse_words(Nom,u"""
le brochet [bro'šä] : haug
une anguille [A~'gii] : angerjas
la perche [pärš] : ahven
le hareng [ar'~A] : heringas
le sprat [sprat] : sprot
le thon [tO~] : tuunikala
le requin [rə'kÄ~] : haikala
""")



Vocabulary.add_lesson(u"Liharoad", u"""""")
Vocabulary.parse_words(Nom,u"""
l'escalope (f) [eska'lOp] : žnitsel
le carré [ka'ree] : karree
le ragoût [ra'gu] : raguu
l'aspic (m) [as'pik] : sült
le filet [fi'lä] : filee | võrk
l'entrecôte (f) [A~trə'koot] : antrekoot (loomaliha ribatükk)
le bifteck [bif'tekk] : biifsteek
le médaillon [medai'jO~] : medaljon
la brochette [bro'šätt] : šašlõk
les attereaux [attə'roo] : paneeritud šašlõk
la côtelette [kot'lätt] : kotlet, ribitükk
le goulasch [gu'laš] : guljašš
le *hachis [ha'ši] : hakkliha
la boulette [bu'lett] : lihapall
le bœuf bourguignon [bÖff burgin'jO~] : härjapraad burgundia veiniga
le bœuf à la tartare [bÖff a la tar'taar] : härjapraad tartaari moodi (?)
""")



Vocabulary.add_lesson(u"Piim ja juust", u"""""")
Vocabulary.parse_words(None,u"""
le lait [lä] : piim
le beurre [bÖÖr]: või
la crème [kr’ääm] : kreem | koor
le fromage [fro'maaž] : juust
la caillebotte [kai'bott] : (kodujuust)
la raclette [rak'lett] : kuumaga sulatud juust
le Camembert [kamA~'bäär] : (valgehallitusjuust)
un Emmental [ämmen'taal] : (juust)
le Rocquefort [rOk'fOOr] : (sinihallitusjuust)
le Gouda [gu'da] : (halandi juust)
""")


Vocabulary.add_lesson(u"Magustoidud", u"""""")
Vocabulary.parse_words(Nom,u"""
la crème [krääm] : koor
la crème fraiche [krääm 'fräš] : rõõsk koor
la crème brûlée [krääm brü'lee] : põletud koor
la crème bavaroise [krääm bavaru'aaz] : muna-piima-seguga kreem želatiiniga 
le dessert [des'säär] : magustoit
la crêpe [kräp] : pannkook
la glace [glass] : jäätis
le sorbet [sor'bä] : jäätis (ilma kooreta)
le gâteau [ga'too] : kook
la gaufre ['goofrə] : vahvel
la tarte [tart] : tort
la tarte aux prunes [tarto'prün] : ploomikook
un petit-beurre [pəti'bÖÖr]: (kuiv küpsis)
""")



Vocabulary.add_lesson(u"Puuviljad", u"""""")
Vocabulary.parse_words(Nom,u"""
le fruit [frü'i] : puuvili
un ananas [ana'na] : ananass 
la banane [ba'nan] : banaan
le citron [si'trO~] : sidrun
une orange [o'rA~ž] : apelsin
la pomme [pom] : õun
la poire [pu'aar] : pirn
la prune [prünn] : ploom
la cerise [sə'riiz] : kirss
la noix [nwa] : pähkel
la noisette [nwa'zett] : sarapuupähkel
""")

Vocabulary.add_lesson(u"Marjad", u"""""")
Vocabulary.parse_words(Nom,u"""
la baie [bä] : mari
la fraise [frääz] : maasikas
la myrtille [mir'tij] : mustikas
la mûre [müür] : põldmari
la groseille [gro'zeij] : sõstras (punane v. valge) | tiker
le cassis [ka'sis] : mustsõstras 
la compote [kO~'pott] : kompott
la confiture [kO~fi'tüür] : moos
""")


Vocabulary.add_lesson(u"Juurviljad", u"""""")
Vocabulary.parse_words(Nom,u"""
la légume [le'güm] : juurvili
la pomme de terre [pom də 'täär] : kartul
la tomate [to'mat] : tomat
le concombre [kO~kO~brə]: kurk
un *haricot [ari'ko] : uba
la salade [sa'laadə] : salat
la gousse d'ail [guss 'daij] : küüslaugu küün
l'ail (m) [aj] : küüslauk
un oignon [on'jO~] : sibul
""")

Vocabulary.add_lesson(u"Teraviljad ja -tooded", u"""""")
Vocabulary.parse_words(Nom,u"""
le blé [blee] : teravili
l'avoine (f) [avu'ann] : kaer
le froment [fro'mA~] : nisu
le sarrasin [sara'zÄ~] : tatar
le blé noir  [blee'nwaar] : tatar
le riz [ri] : riis
le seigle ['sääglə] : rukis
l'orge (m) [Oržə] : oder
la farine [far'inn] : jahu
la bouillie [bui'jii] : puder
le gruau [grü'oo] : puder
le pain [pÄ~] : sai | leib
la tartine [tar'tin] : võileib
""")


Vocabulary.add_lesson(u"Ürdid", u"""""")
Vocabulary.parse_words(Nom,u"""
le sel [säl] : sool
le poivre ['pwaavrə] : pipar
un assaisonnement [asäzonn'mA~] : maitsestamine
le condiment [kO~di'mA~] : maitseaine
une épice [e'pis] : vürts
les fines herbes [fin'zärbə] : fines herbes ("peened ürdid")
une herbe [ärbə] : ürt
le persil [pär'sil] : petersell
le céléri [sele'ri] : seller
la câpre ['kaaprə] : kaaper
le gingembre [žÄ~žA~brə] : ingver
""")

Vocabulary.add_lesson(u"Ürdid", u"""""")
Vocabulary.parse_words(Nom,u"""
la moutarde [mu'tardə] : sinep
le vinaîgre [vin'äägrə] : äädikas
la mayonnaise [majo'nääz] : majonees
la vinaîgrette [vine'grätt] : vinegrett

""")

Vocabulary.add_lesson(u"Pliidil", u"""""")
Vocabulary.parse_words(Nom,u"""
la cuisson [küis'sO~] : keetmine
le blanchiment [blA~ši'mA~] : blanžeerimine
le rôtissage [rotis'saaž] : praadimine (panni peal)
la friture [fri'tüür] : praadimine (õlis või rasvas)
le grillage [gri'jaaž] : röstimine
le braisage [bre'zaaž] : moorimine
""")

#~ le bain marie [bÄ~ ma'rii] : 

Vocabulary.parse_words(Verbe,u"""
rissoler [risso'lee]: (rasvas) pruunistama
cuire [kwiir] : keetma
blanchir [blA~'šiir] : blanžeerima
rôtir [ro'tiir] : praadima (panni peal)
frire [friir] :  praadima (õlis)
griller [gri'jee] : röstima
braiser [bre'zee] : moorima
manier [man'jee] : käsitsema
""")


Vocabulary.add_lesson(u"Köögiriistad", u"""""")
Vocabulary.parse_words(Nom,u"""
le fouet [fu'ä] : vispel
une alumette [alu'mät] : tuletikk
la braisière [bräz'jäär] : grosse marmite de cuisson souvent en cuivre étamé ou en terre cuite qui permet de braiser de grosses pièces de viande.
la cocotte :  marmite souvent en fonte destinée à la cuisson des aliments.
la poêle [pwal] : pann
la râpe [rap] : riivija
la cuisinière [kwizin'jäär] : pliit
le four [fuur] : ahi
le four à micro-ondes [fuur a mikro 'O~də] : mikrolaine ahi
""")

Vocabulary.add_lesson(u"Joogid", u"""""")
Vocabulary.parse_words(Nom,u"""
le café [ka'fee] : kohv
le thé [tee] : tee
le vin rouge [vÄ~ 'ruuz]: punane vein
le vin blanc [vÄ~ 'blA~]: valge vein
le vin rosé [vÄ~ ro'zee] : roozé vein
la bière [bjäär] : õlu
le cidre ['siidrə] : siider
le jus [žu] : mahl
une eau [oo] : vesi
la bavaroise [bavaru'aaz] : gastronoomiline jook valmistatud teest, piimast ja liköörist
""")



Vocabulary.add_lesson(u"Veinialad Prantsusmaal", u"""
""")
Vocabulary.parse_words(None,u"""
la région [rež'jO~] : ala
le terroir [ter'waar] : geograafiline veinirühm
""")
Vocabulary.parse_words(NomGeographique,u"""
Alsace [al'zas] : Elsass
Beaujolais [boožo'lä] : -
Bordeaux [bOr'doo] : -
Bourgogne [bur'gonjə] : -
Champagne [šA~'panjə] : -
Charente [ša'rA~tə] : -
Poitou [pwa'tu] : -
Corse ['korsə] : Korsika
Jura [žü'ra] : -
Savoie [savu'a] : -
Languedoc [lA~gə'dok] : -
Roussillon [russi'jO~] : -
Provence [pro'vA~sə] : - 
Sud-Ouest [süd'uest] : - 
Gascogne [gas'konjə] : -
Val de Loire [val də 'lwaarə] : Loire'i org
Vallée du Rhône [val'lee dü roonə] : Rhône'i org
""")

Vocabulary.add_lesson(u"Prantsuse veinid", u"""
Prantsuse veinid on üle 400, siin ainult mõned.
""")
Vocabulary.parse_words(Nom,u"""
une appellation d'origine contrôlée (AOC) [apela'sjO~ dori'žin kO~trO'lee] : kontrollitud päritolumaa nimetus
le Chasselas [šas'la] : -
le Grand Cru [grA~'krü] : - 
le Pinot Noir [pi'no nwaar] : - 
le Côte de Brouilly [koot də bru'ji] : -
le Saint-Amour [sÄ~ta'muur] : - 
le Bordeaux clairet [bOr'doo klä're] : - 
le Médoc [me'dok] : - 
le Saint-Émilion [sÄ~temi'jO~] : - 
le Beaune [boon] : - 
le Côtes du Ventoux [koot du vA~'tu] : -
le Minervois [minerv'wa] : - 
le Côtes d'Auvergne [koot do'värnjə] : -
""")




u"""
On met une majuscule 
uniquement quand l’adjectif est employé comme 
nom pour désigner une personne. 
Ex. : Les Français parlent en français à leurs amis français
"""
Vocabulary.add_lesson(u"Riigid", u"""
""",columns=[GEON("Riik"), GEOM, GEOF, ET])
Vocabulary.parse_words(None,u"""
la France [frA~s] | français [fra~'sä] | française [fra~'sääz] : Prantsusmaa
l'Estonie (f) [ästo'nii] | estonien [esto'njÄ~] | estonienne [esto'njän] : Eesti
l'Allemagne (f) [al'manjə] | allemand [al'mA~]| allemande [al'mA~də] : Saksamaa
l'Angleterre (f) [A~glə'täär] | anglais [A~'glä]| anglaise [A~'glääz] : Inglismaa
la Belgique [bel'žik] | belge [belžə]| belge [belžə] : Belgia
la *Hollande [o'lA~də] | hollandais [olA~'dä] | hollandaise [olA~'dääz] : Holland
l'Espagne (f) [es'panjə] | espagnol [espan'jol] | espagnole [espan'jol] : Hispaania
l'Italie (f) [ita'lii] | italien [ital'jÄ~]| italienne [ital'jen] : Itaalia
""")

Vocabulary.add_lesson(u"Prantsusmaa linnad", u"""
""",columns=[GEON("Linn"), GEOM, GEOF])
Vocabulary.parse_words(NomGeographique,u"""
Avignon [avin'jO~] | avignonnais [avinjo'nä] | avignonnaise [avinjo'nääz] : -
Bordeaux [bor'doo] | bordelais [bordə'lä] | bordelaise [bordə'lääz] : -
Bourgogne [burgOnjə] | bourguignon [burgin'jO~] | bourguignonne [burgin'jOnn] : -
Dijon [di'žO~] | dijonnais [dižon'nä] | dijonnaise [dižon'nääz] : -
Lyon [li'O~] | lyonnais [lio'nä] | lyonnaise [lio'nääz] : -
Marseilles [mar'säij] | marseillais [marsäi'jä]| marseillaise [marsäi'jääz] : - 
Paris [pa'ri] | parisien [pariz'jÄ~]| parisienne [pariz'jenn] : Pariis
Verdun [vär'dÖ~] | verdunois [värdü'nwa]| verdunoise [värdü'nwaaz] : -
Versailles [ver'saj] | versaillais [värsa'jä] | versaillaise [värsa'jääz] : -
""")
#~ Vocabulary.parse_words(NomGeographique,u"""
#~ la France [frA~s] : Prantsusmaa
#~ la Belgique [bel'žik] : Belgia
#~ une Allemagne [al'manjə] : Saksamaa
#~ une Angleterre [A~glə'täär] : Inglismaa
#~ une Estonie [ästo'nii]: Eesti
#~ une Hollande [o'lA~də]: holland
#~ une Espagne [es'panjə]: hispaania
#~ une Italie [ita'lii]: hispaania
#~ """)
#~ Vocabulary.parse_words(Adjectif,u"""
#~ français [fra~'sä] | français [fra~'sääz] : prantsuse
#~ estonien [esto'njÄ~] | estonien [esto'njän] : eesti
#~ espagnol [espan'jol] | espagnole [espan'jol] : hispaania
#~ hollandais [olA~'dä] | hollandaise [olA~'dääz]: holandi
#~ """)

Vocabulary.add_lesson(u"Omadussõnad (kulinaaria)", u"""
Sellised sõnu leidub restoranide menüüdes.
""",columns=[M, F, ET])
Vocabulary.parse_words(Adjectif,u"""
suprême (mf) [sü'prääm] : ülem, kõrgem, ülim
royal [rwa'jal] | royale [rwa'jal] : kuninglik
paysan [pei'zA~] | paysanne [pei'zann] : talu-, talupoja-
bouilli [bui'ji] | bouillie [bui'jii] : keedetud
poché [po'še] | pochée [po'šee] : uputatud keeva vette
beurré [bÖÖ'ree] | beurrée [bÖÖ'ree]: võiga
épicé [epi'see] | épicée [epi'see] : vürtsitatud, vürtsikas
sauté [soo'tee] | sautée [soo'tee] : rasvas praetud
velouté [velu'tee] | veloutée [velu'tee] : sametine, sametitaoline
gourmand [gur'mA~] | gourmande [gur'mA~d] : maiasmokk
glacé [glas'see] | glacée [glas'see] : jäätunud
""")



Vocabulary.add_lesson(u"Menüü", u"""""")
Vocabulary.parse_words(Nom,u"""
le plat [pla] : roog 

le bouillon [bui'jO~] :  puljong | leem
le potage [po'taažə] : püreesupp
le consommé [kO~som'mee] : selge puljong 
#rammuleem?

la purée [pü'ree] : püree
la mousse [mus] : vaht
un œuf [Öf] : muna
les œufs brouillés [öö brui'jee] : omlett
les œufs pochés [öö po'šee] : ilma kooreta keedetud muna
le gratin [gra'tÄ~] : gratään (ahjus üleküpsetatud roog)
le hors d'œuvre [OOr 'dÖÖvrə] : eelroog
le soufflé [suff'lee] : suflee
# le parfait [par'fä] : 
la coquille [ko'kiij] : merekarp
la cocotte [ko'kott] : malmkastrul, kokott
la fondue [fO~'düü] : fondüü
le fumet [fü'mä] : hea lõhn (nt. veini, liha kohta)
les pâtes ['paat] : pastarood
le pâté [pa'tee] : pasteet
le pâté en croûte [pa'tee A~'krut] : taignas pasteet
le pâté en terrine [pa'tee A~ter'rin] : pasteet kaussis
la galantine [galA~'tin] : galantiin
le cassoulet [kassu'lä] : Languedoc'ist pärit ühepajatoit ubadest ja lihast, mida küpsetatakse mitu tundi madala temperatuuriga ahjus.
le pot-au-feu [pOto'föö] : ühepajatoit
""")



Vocabulary.add_lesson(u"Kastmete valmistamine", u"""""")
Vocabulary.parse_words(Nom,u"""
la sauce [soos] : kaste
le beurre manié [bÖÖr man'jee]: jahuvõi
le roux [ru] : rasvas kuumutatud jahu
le roux blanc [ru blA~] : valge segu
le roux blond [ru blO~] : kollane segu
le roux brun [ru brÖ~] : pruun segu
la sauce espagnole [espan'jOl] : pruun põhikaste
la sauce demi-glace [dəmi'glas] : redutseeritud pruun põhikaste
le jus de rôti [žu də ro'ti] : redutseeritud puljong, "praeliha mahl"
le jus lié [žu li'ee] : maisi või nooljuurejahuga pruun kaste

le mirepoix [mirə'pwa] : praetud kuubikud (sibul, porgand, seller)
la brunoise [brün'waaz] : juur- või puuvili kuubikud (2mm)
la julienne [jül'jän] : juurvilja lõikamise viis lamellideks
la macédoine [mase'dwan] : juurviljasalat
""")

Vocabulary.add_lesson(u"Kastmed", u"""""")
Vocabulary.parse_words(Nom,u"""

la sauce paysanne [pei'zan] : talupoja kaste
la sauce chasseur [ša'sÖÖr] : jahimehe kaste
la sauce jardinière [žardin'jäär] : aedniku kaste

la sauce piquante [pi'kA~tə] : pikantne kaste
la sauce poivrade [pwav'raadə] : piprakaste

la sauce Grand Veneur [grA~ və'nÖÖr] : jäägri kaste
la sauce Bigarrade [biga'raadə] : apelsinikaste
la sauce smitane [smi'tanə] : hapukoorekaste
la sauce Lyonnaise [lio'nääzə] : pruun sibulakaste
la sauce Bourguignonne [burgin'jOn] : Burgundia kaste
la sauce Robert [ro'bäär] : Roberti kaste
la sauce Madère [ma'däär] : Madeira kaste
la sauce Porto [pOr'to] : portveini kaste
la sauce Sabayon [saba'jO~] : Sabayon-kaste
la sauce italienne [ital'jän] : itaalia kaste
la sauce veloutée [vəlu'tee] : hele põhikaste
la sauce blanche [blA~šə] : tuletatud hele kaste
la sauce bordelaise [bOrdə'lääz] : punase veini kaste
la sauce aurore [o'rOOr] : aurora kaste

la sauce béchamel [beša'mäl] : valge põhikaste
""")


Vocabulary.add_lesson(u"Mida kokk teeb", u"""
""")
Vocabulary.parse_words(Verbe,u"""
tourner [tur'nee] : keerama, pöörama
composer [kO~po'zee] : koostama
baisser [bäs'see] : alla laskma, madaldama
porter [por'tee] : kandma
laver [la'vee] : pesema
concasser [kO~kas'see] : peenestama (tükkideks)
farcir [far'siir] : farssima (täidisega täitma)
hacher [a'šee] : hakkima
éplucher [eplü'šee]: koorima
émincer [émÄ~'see] : lõikama viiludeks
utiliser [ütili'zee] : kasutama
préparer [prepa'ree] : ette valmistama
préchauffer [préšoo'fee] : ette kütma
""")



Vocabulary.add_lesson(u"Omadussõnad (üld)", u"""
Omadussõnad, mis lõpevad "e"-ga, ei muutu soo järgi.
""",columns=[M, F, ET])
Vocabulary.parse_words(Adjectif,u"""
chaud [šoo] | chaude [šoodə] : kuum
froid [fru'a] | froide [fru'aadə] : külm
gros [gro] | grosse [grossə] : paks
mince (mf) [mÄ~s] : õhuke
bon [bO~] | bonne [bonnə] : hea
beau [boo] | belle [bellə] : ilus
joli [žo'li] | jolie [žo'lii] : ilus
demi [də'mi] | demie [də'mii]: pool
entier [A~'tjee] | entière [A~'tjäär] : terve, täis
double (mf) ['duublə] : topelt
facile (mf) [fa'sil] : lihtne
possible (mf) [po'siblə] : võimalik
""")



Vocabulary.add_lesson(u"Loeme kümneni", u"""""")
Vocabulary.parse_words(Numerique,u"""
un [Ö~] : üks
deux [döö] : kaks
trois [trwa] : kolm
quatre [katrə] : neli
cinq [sÄ~k] : viis
six [sis] : kuus
sept [sät] : seitse
huit [üit] : kaheksa
neuf [nÖf] : üheksa
dix [dis] : kümme
""")


Vocabulary.add_lesson(u"Värvid", u"""""",columns=[M, F, ET])
Vocabulary.parse_words(Adjectif,u"""
brun [brÖ~] | brune [brünn] : pruun
vert [väär] | verte [värtə] : roheline
bleu [blöö] | bleue [blöö] : sinine
rouge (mf) [ruuž] : punane
jaune (mf) [žoon] : kollane
blond [blO~] | blonde [blO~də] : blond 
beige (mf) [bääž]  : beež
orange (mf) [o'ra~ž]  : oranž
blanc [blA~] | blanche [blA~š] : valge
noir [nwaar] | noire [nwaar] : must
""")



Vocabulary.add_lesson(u"Kuulsad inimesed", u"""
""")
Vocabulary.parse_words(NomPropre,u"""
Jacques Chirac [žaak ši'rak] : # endine president
Georges Brassens [žorž bra'sÄ~s] : # laulja
Brigitte Bardot [bri'žit bar'do] : # laulja
Louis de Funès [lu'i də fü'nääz] : # näitleja
""")

Vocabulary.add_lesson(u"Kuud", u"""
""")
Vocabulary.parse_words(NomPropre,u"""
janvier [žA~'vjee] : jaanuar
février [fevri'ee] : veebruar
mars [mars] : märts
avril [a'vril] : aprill
mai [mä] : mai
juin [žwÄ~] : juuni
juillet [žüi'jä] : juuli
août [ut] : august
septembre [sep'tA~brə] : september
octobre [ok'tOObrə] : oktoober
novembre [no'vA~brə] : november
décembre [de'sA~brə] : detsember
""")

Vocabulary.add_lesson(u"Majad ja nende osad", 
u"""
""")
Vocabulary.parse_words(Nom,u"""
la maison [mä'zO~] : maja
la cave [kaav] : kelder
la cuisine [kwi'zin] : köök
la salle de bain : vannituba
la chambre à coucher : magamistuba
le salon [sa’lO~] : elutuba
un escalier [eskal'jee] : trepp
la fenêtre [fə'näätrə] : aken
le parterre [par'täär] : esimene korrus
le premier étage : teine korrus
le jardin [žar'dÄ~] : aed
""")



Vocabulary.add_lesson(u"Virelangues", u"""
#. Poisson sans boisson est poison. 
#. Un chasseur sachant chasser doit savoir chasser sans son chien. 
#. Ecartons ton carton, car ton carton me gêne. 
#. Ton thé t'a-t-il ôté ta toux? 
#. Chacun cherche son chat.
#. Tante, en ton temps teintais-tu tes tempes?
""")
Vocabulary.parse_words(Nom,u"""
le poisson [pwa'sO~] : kala
le poison [pwa'zO~] : mürk
la boisson [bwa'sO~] : jook
le chasseur [ša'sÖÖr] : jahimees
le chien [šiÄ~] : koer
la toux [tu] : köha
""")
Vocabulary.parse_words(Verbe,u"""
savoir [sa'vuaar] : teadma | oskama
chercher [šär'šee] : otsima
écarter [ekar'tee] : eest ära liigutama
ôter [oo'tee] : ära võtma
""")
Vocabulary.parse_words(Autre,u"""
sans [sA~] : ilma
chacun [ža'kÖ~] : igaüks
""")

Vocabulary.add_lesson(u"Lisa", u"""
""")
Vocabulary.parse_words(Autre,u"""
environ [A~vi'rO~] : umbes
facilement [fasil'mA~] : lihtsalt
rapidement [rapidə'mA~]: kiiresti
le autre [ootrə] : teine
le même [määm] : sama
""")

Vocabulary.parse_words(Verbe,u"""
filer [fi'lee] : ketrama
baiser [bä'zee] : musitama
sauter [soo'tee] : hüppama
""")

Vocabulary.parse_words(Nom,u"""
le midi [mi'di] : lõun | keskpäev
le soir [swaar] : õhtu
le matin [ma'tÄ~] : hommik
le sucre ['sükrə] : suhkur
la tranche [trA~š] : lõik | viilukas
la coupe [kupp] : lõikamine | pokaal
la casserole [kas'roll] : pott
la marmite [mar'mit] : pott
le caquelon [kak'lO~] : fondüüpott
le moulin [mu'lÄ~] : veski
une ébullition [ebüjis'jO~] : keemine
le feu [föö] : tuli
le baiser [bä'zee] : suudlus
un appétit [appe'ti] : isu
""")

unused = u"""
une aurore [or'Or] : koit
le fil [fil] : niit | lõng | nöör
une heure [ÖÖr] : tund
le dauphinois [dofinw'a] : lõunaprantsuse dialekt
"""

book.add_index(3,u"Prantsuse-Eesti")

if __name__ == '__main__':
    import os
    import sys
    if len(sys.argv) != 3:
        raise Exception("""
Usage : %(cmd)s rst OUTPUT_ROOT_DIR
        %(cmd)s odt OUTPUT_FILE
""" % dict(cmd=sys.argv[0]))
    fmt = sys.argv[1]
    if fmt == "rst":
        book.write_rst_files(sys.argv[2])
    elif fmt == "odt":
        tpl = os.path.join(os.path.dirname(__file__),'cfr.odt')
        fn = sys.argv[2]
        assert os.path.abspath(tpl) != os.path.abspath(fn)
        book.write_odt_file(tpl,fn)
        os.startfile(fn)
