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

import os
import sys

from lino.modlib.vocbook.fr import French, Autre, Nom, NomPropre, Adjectif, Numerique, Verbe, NomGeographique
from lino.modlib.vocbook.et import Estonian
from lino.modlib.vocbook.base import Book, FR, M, F, ET, PRON, GEON, GEOM, GEOF

if len(sys.argv) != 3:
    raise Exception("""
Usage : %(cmd)s rst OUTPUT_ROOT_DIR
    %(cmd)s odt OUTPUT_FILE
""" % dict(cmd=sys.argv[0]))
fmt = sys.argv[1]
if fmt == "rst":
    FULL_CONTENT = True
else:
    FULL_CONTENT = False

book = Book(French,Estonian,
    title=u"Kutsealane prantsuse keel kokkadele",
    input_template=os.path.join(os.path.dirname(__file__),'Default.odt'))
    #~ os.path.join(os.path.dirname(__file__),'cfr.odt')

Pronounciation = book.add_section(u"Hääldamine",intro=u"""
Esimeses osas keskendume hääldamisele.
Siin pole vaja meelde jätta näidissõnu,
vaid et sa oskaksid neid ette lugeda õigesti hääldades.
""")
Intro = Pronounciation.add_section(u"Kirjeldus",intro=u"""
""")
Reeglid = Pronounciation.add_section(u"Reeglid")
if FULL_CONTENT:
    Eesti = Pronounciation.add_section(u"Veel")

#~ Vocabulary = book.add_section(u"Sõnavara",intro=u"""
#~ Teises osa hakkame õpima sõnavara,
#~ oletades et hääldamine on enam vähem selge.
#~ """)
Vocabulary = book
#~ General = Vocabulary.add_section(u"Üldiselt")
General = Vocabulary.add_section(u"Üldine sõnavara")
Kokadele = Vocabulary.add_section(u"Kulinaaria")
if FULL_CONTENT:
  Fun = Vocabulary.add_section(u"Fun")


Intro.add_lesson(u"Tuntud sõnad", intro=u"""
Mõned sõnad, mida sa juba tead.
Tutvumine hääldamiskirjaga.
""")
Intro.parse_words(None,u"""
la soupe [sup] : supp
la carte [kart] : kaart
à la carte [ala'kart] : menüü järgi
le vase [vaaz] : vaas
la douche [duš] : dušš
le disque [disk] : ketas
merci [mär'si] : aitäh
le garage [ga'raaž] : garaaž
le journal [žur'nal] : päevik | ajaleht
""")
Intro.add_after(u"""
Kuna hääldamine on algaja peamine raskus, 
tuleb meil seda kuidagi kirja panna.
Seda teeme sõnade taha nurksulgudes (**[]**).

- Tähekombinatsioon **ou** hääldatakse **[u]**.

- **e** sõna lõpus kaob ära

- Prantsuse keeles on raske ette teada, kas täishäälikuid 
  hääldatakse lühikesena või pikana.
  Hääldamiskirjelduses kirjutame pikad 
  kaashäälikud topelt.

- Prantsuse keeles on rõhk tavaliselt viimasel silbil.
  Hääldamiskirjelduses paneme apostroofi (') rõhutatud silbi ette.
 
""")


Intro.add_lesson(u"Hääldamiskirjeldus", intro=u"""
Hääldamiskirjeldustes kasutame 
kohandatud `X-SAMPA 
<http://fr.wiktionary.org/wiki/Annexe:Prononciation/fran%C3%A7ais>`_ variant, 
mis on eestlastele intuitiivsem õppida 
kui näiteks `IPA 
<http://en.wiktionary.org/wiki/Wiktionary:IPA>`_ (International 
Phonetic Alphabet).

Üldiselt loed lihtsalt seda, mis on nurksulgudes.
Välja arvatud mõned helid, mida tuleb õppida:

==== ================== =================== =======================================
täht selgitus           näided e.k.         näided pr.k.
==== ================== =================== =======================================
[ə]  tumm e             Lott\ **e**         **je** [žə], **ne** [nə]
[o]  kinnine o          L\ **oo**\ ne       **mot** [mo], **beau** [boo]
[O]  avatud o           L\ **o**\ tte       **bonne** [bOn], **mort** [mOOr]
[ö]  kinnine ö          l\ **öö**\ ve       **feu** [föö], **peu** [pöö]
[Ö]  avatud ö           ingl. "g\ *ir*\ l"  **beurre** [bÖÖr], **jeune** [žÖÖn]
[w]  ingl. k. "where"   ingl. "\ **w**\ e"  **trois** [trw'a], **foie** [fw'a]
[O~] nasaalne [O]       -                   **bonjour** [bO~'žuur], **mon** [mO~]
[A~] nasaalne [A]       -                   **tante** ['tA~tə], **prendre** ['prA~drə]
[Ö~] nasaalne [Ö]       -                   **un** [Ö~], **parfum** [par'fÖ~]
[Ä~] nasaalne Ä         -                   **chien** [šiÄ~], **rien** [riÄ~]
==== ================== =================== =======================================

 

""")

Intro.add_lesson(u"Mesilashäälikud", intro=u"""
"Mesilashäälikud" on **s**, **š**, **z** ja **ž**.
  
=========== ===========================
terav       pehme
=========== ===========================
**s**\ upp  **z**\ oom
**š**\ okk  **ž**\ urnaal, **ž**\ anre
=========== ===========================
  
Nad on eesti keeles ka olemas, aga prantsuse keeles on
nende erinevus palju olulisem.
""")
Intro.parse_words(None,u"""
la soupe [sup] : supp
le garage [ga'raaž] : garaaž
le genre [žA~rə] : žanre
le journal [žur'nal] : päevik | ajaleht
le choc [žok] : šokk | löök
""")




Intro.add_lesson(u"Artikkel", intro=u"""
Prantsuse keeles on kõikidel asjadel oma sugu.
Näiteks laud (*la table*) on naissoost, 
raamat (*le livre*) on meessoost.

Kui sul on mitu lauda või mitu raamatu, 
siis on neil sama artikkel **les** (nt. *les tables*, *les livres*).

Kui sõna algab täishäälikuga, siis kaob 
artiklitest *le* ja *la* viimane 
täht ära ja nad muutuvad  mõlemad **l'**-ks.

Artiklid *le*, *la* ja *les* nimetatakse *määravaks* artikliteks.

Mmäärava artikli asemel võib ka olla **umbmäärane** artikkel: **un** (meessoost) 
või **une** (naissoost).
Erinevus on nagu inglise keeles, kus on olemas määrav 
artikkel **the** ja umbmäärane artikel **a**.
Olenevalt kontekstist kasutatakse kas see või teine.
Näiteks
"I am **a** man from Vigala"
ja 
"I am **the** man you need".

Mitmuses on umbmäärane artikkel **des** sama mõlemas soos.

Nii et kokkuvõteks:

========== ============= =============
sugu       määrav        umbmäärane
========== ============= =============
meessoost  **le** [lə]   **un** [Ö~]
naissoost  **la** [la]   **une** [ün]
mitmus     **les** [lä]  **des** [dä]
========== ============= =============

""")
#~ Intro.parse_words(Autre,u"""
#~ le [lə] : (määrav meessoost artikkel)
#~ la [la] : (määrav naissoost artikkel)
#~ les [lä] : (määrav artikkel mitmus)
#~ """)
#~ Intro.parse_words(Autre,u"""
#~ un [Ö~] : (umbmäärane meessoost artikkel)
#~ une [ün] : (umbmäärane naissoost artikkel)
#~ des [dä] : (umbmäärane artikkel mitmus)
#~ """)

Intro.add_lesson(u"Rõhutud, aga lühike!", intro=u"""
Rõhutatud täishäälikud ei ole sellepärast tingimata pikad.
Prantsuse keeles tuleb tihti ette, et sõna 
lõpeb *lühikese* täishäälikuga.
""")
Intro.parse_words(Nom,u"""
le menu [mə'nü] : menüü
le chocolat [šoko’la] : šokolaad
le plat [pla] : roog | kauss
le cinéma [sine’ma] : kino
le paradis [para'di] : paradiis
""")




Reeglid.add_lesson(u"u", intro=u"""
Kirjatäht **u** (siis kui see pole teise täishäälikuga koos)
hääldatakse **[ü]** või **[üü]**.

""")
Reeglid.parse_words(Nom,u"""
le bureau [bü'roo] : büroo
le bus [büs] : buss
le mur [müür] : sein | müür
la puce [püs] : kirp
le jus [žü] : mahl
le but [büt] : eesmärk
la pute [püt] : hoor
le sucre ['sükrə] : suhkur
""")

Reeglid.add_lesson(u"ou", intro=u"""
Tähekombinatsioon **ou** hääldatakse **[u]** või **[uu]**.
""")
Reeglid.parse_words(None,u"""
le cours [kuur] : kursus | tund (koolis)
le cou [ku] : kael
le goût [gu] : maitse
le chou [šu] : kapsas
le loup [lu] : hunt
un ours [urs] : karu
le journal [žur'nal] : päevik
""")

Reeglid.parse_words(None,u"""
la loupe [lup] : luup
la joue [žuu] : põsk
le jour [žuur] : päev
court (m) [kuur] : lühike
mou (m) [mu] : pehme
""")
#~ Reeglid.parse_words(NomPropre,u"""
#~ Winnetou [winə'tu] : (isegi maailmakuulsa apatši pealiku nime hääldavad prantslased valesti)
#~ """)


Reeglid.add_lesson(u"oi", 
u"""
Tähekombinatsioon **oi** hääldatakse peaaegu alati **[wa]**.
Hääldamiskirja **w** täht on "ülipehme", 
nagu nt. inglise sõnades "week", "wow", "where".
""")
Reeglid.parse_words(Autre,u"""
voilà [vwa'la] : näe siin 
trois [trwa] : kolm
bonsoir [bO~'swaar] : head õhtut
au revoir [orə'vwaar] : nägemiseni
""")
Reeglid.parse_words(Nom,u"""
le roi [rwa] : kuningas
la loi [lwa] : seadus
la toilette [twa'lät] : tualett
un oiseau [wa'zoo] : lind
""")



Reeglid.add_lesson(u"*au* ja *eau*", 
u"""
Tähekombinatsioon **au** hääldatakse **[o]** või **[oo]**.
Kui **e** on veel ees, siis see sulab ka nendega kokku ja kaob ära.
""")
Reeglid.parse_words(None,u"""
une auberge [o'bäržə] : võõrastemaja
un auteur [o'tÖÖr] : autor
le château [ža'too] : loss
le bateau [ba'too] : laev
la eau [oo] : vesi
""")



Reeglid.add_lesson(u"y", u"""
Kirjatäht **y** hääldatakse 
alati **[i]** ja mitte kunagi **[ü]**.
""")
Reeglid.parse_words(Nom,u"""
le cygne ['sinjə] : luik
le système [sis'tääm] : süsteem
le mythe [mit] : müüt
""")


Reeglid.add_lesson(u"ai", 
u"""
Tähekombinatsioon **ai** hääldatakse **[ä]** või **[ää]**,
v.a. siis kui järgneb **l**.
""")
Reeglid.parse_words(Nom,u"""
la maison [mä'zO~] : maja
le domaine [do'mään] : domeen
la fraise [frääz] : maasikas
la paire [päär] : paar
""")
Reeglid.parse_words(Adjectif,u"""
frais [frä] | fraiche [fräš] : värske
""")


Reeglid.add_lesson(u"ail", 
u"""
Tähekombinatsioon **ail** hääldatakse **[aj]**.
""")
Reeglid.parse_words(Nom,u"""
l'ail (m) [aj] : küüslauk
le travail [tra'vaj] : töö
le détail [detaj] : detail
""")
Reeglid.parse_words(NomGeographique,u"""
Versailles [ver'sajə] : Versailles
""")





Reeglid.add_lesson(u"j", 
u"""
Kirjatäht **j** hääldatakse **[ž]** (ja mitte [dž]).
""")
Reeglid.parse_words(None,u"""
majeur [mažÖÖr] : suurem
je [žə] : mina
jamais [ža'mä] : mitte iialgi
jaune (mf) [žoon] : kollane
""")
Reeglid.parse_words(NomPropre,u"""
Josephe [žo'zäf] : Joosep
""")


Reeglid.add_lesson(u"g", 
u"""
Kirjatäht **g** hääldatakse **[g]** kui järgneb **a**, **o**, **u** 
või kaashäälik, aga **[ž]** kui järgneb **e**, **i** või **y**.
""")
Reeglid.parse_words(None,u"""
le gorille [go'rijə] : gorilla
la gazelle [ga'zäl] : gasell
la giraffe [ži'raf] : kaelkirjak
le gymnase [žim'naaz] : gümnaasium
le juge [žüüž] : kohtunik
la géologie [žeolo'žii] : geoloogia
général [žene'ral] : üldine
""")

Reeglid.add_lesson(u"gue, gui, guy", 
u"""
Kui hääldamine on [ge], [gə], [gä] või [gi], 
siis lisatakse tumm **u**: *gui*, *gue*, *guy*
""")
Reeglid.parse_words(None,u"""
le guépard [ge'paar] : gepard
le guide [giid] : reisijuht
la guitare [gi'taar] : kitarr
la guerre [gäär] : sõda
Guy [gi] : (eesnimi)
""")






Reeglid.add_lesson(u"c", u"""
Kirjatäht **c** hääldatakse **[s]** siis 
kui järgneb **e**, **i** või **y**,
ja muidu **[k]** (ja mitte kunagi **[tš]**).

""")
Reeglid.parse_words(None,u"""
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
Reeglid.parse_words(NomPropre,u"""
octobre [ok'tOObrə] : oktoober
Marc [mark] : Markus
""")
Reeglid.parse_words(Numerique,u"""
cinq [sÄ~k] : viis
""")

Reeglid.add_lesson(u"ç", u"""
Kirjatäht **ç** hääldatakse alati **[s]**.
""")
Reeglid.parse_words(None,u"""
la leçon [lə~sO~]: lektsioon
la rançon [rA~sO~]: lunaraha
le reçu [rə'sü] : kviitung
le maçon [ma'sO~] : müürsepp
""")


#~ Pronounciation.parse_words(Autre,u"""
#~ Il était une fois [iletätünə'fwa] : Oli üks kord
#~ le boudoir [bud'waar] : buduaar
#~ """)

#~ Intro.add_lesson(u"Jah ja ei", u"""
#~ """)
#~ Intro.parse_words(None,u"""
#~ """)


Reeglid.add_lesson(u"ui", 
u"""
Tähekombinatsioon **ui** hääldatakse **[wi]** või **[wii]** (mida 
kirjutatakse vahest ka **[üi]** või **[üii]**).

""")
Reeglid.parse_words(None,u"""
la suite [swit] : järg | tagajärg | rida, kord | saatjaskond
bonne nuit [bOn'nwi] : head ööd
la cuisine [kwi'zin] : köök
je cuis [žə kwi] : ma keedan
je suis [žə swi] : ma olen | ma järgnen
""")

#~ Reeglid.parse_words(None,u"""
#~ l'huile (f) [wil] : õli
#~ cuire [kwiir] : keetma
#~ suivre ['swiivrə] : järgima
#~ la cuillère [kwi'jäär] : lusikas
#~ """)


Reeglid.add_lesson(u"un, um", 
u"""
Tähekombinatsioonid **um** ja **un** hääldatakse **[Ö~]**,
v.a. siis kui järgneb täishäälik või teine **m** / **n**.
""")
Reeglid.parse_words(Nom,u"""
le parfum [par'fÖ~] : hea lõhn v. maitse
""")
Reeglid.parse_words(NomPropre,u"""
Verdun [vär'dÖ~] : -
""")
Reeglid.parse_words(Adjectif,u"""
brun [brÖ~] | brune [brün] : pruun
aucun [o'kÖ~] | aucune [o'kün] : mitte üks
parfumé [parfü'mee] | parfumée [parfü'mee] : lõhnastatud
""")

#~ chacun [ža'kÖ~] | chacun [ža'kün] : igaüks



Intro.add_lesson(u"Lotte ja Loone", u"""
Hääldamiskirjelduses on olemas *kinnine* [o] (väikese tähega)
ja *avatud* [O] (suure tähega).

Lotte **O** on lühike ja *avatud*, Loone oma on pikk ja *kinnine*.
Prantsuse keeles on lisaks veel olemas *avatud ja pikk* [OO].
""")
Intro.parse_words(Autre,u"""
je donne [dOn] : ma annan
je dors [dOOr] : ma magan
""")
Intro.parse_words(Nom,u"""
la mort [mOOr] : surm
le mot [mo] : sõna
le or [OOr] : kuld
le boulot [bu'lo] : töö (kõnekeel)
le bouleau [bu'loo] : kask
le bureau [bü'roo] : büroo
""")

if FULL_CONTENT:

    Fun.add_lesson(u"Frère Jacques", 
    u"""
    | Frère Jacques, frère Jacques,
    | dormez-vous? Dormez-vous? 
    | Sonnez les matines, sonnez les matines
    | ding, dang, dong! Ding, dang, dong!
    """)
    Fun.parse_words(NomPropre,u"""
    Jacques [žaak] : Jaak
    """)
    Fun.parse_words(None,u"""
    le frère [fräär] : vend
    dormez-vous? [dOrme'vu] : kas Te magate?
    Sonnez les matines [sO'ne lä ma'tinə] : lööge hommikukellad
    """)

if FULL_CONTENT:

    Fun.add_lesson(u"Minu onu...", 
    u"""
    | Mon tonton et ton tonton sont deux tontons,
    | mon tonton tond ton tonton 
    | et ton tonton tond mon tonton.
    | Qu'est-ce qui reste?

    """)
    Fun.parse_words(None,u"""
    mon [mO~] : minu
    ton [tO~]: sinu
    ils sont [sO~]: nad on
    """)
    Fun.parse_words(Numerique,u"""
    deux [döö] : kaks
    """)
    Fun.parse_words(Nom,u"""
    un tonton [tO~'tO~] : onu
    """)
    Fun.parse_words(Verbe,u"""
    tondre [tO~drə] : pügama
    rester [räs'tee] : üle jääma
    """)
    Fun.parse_words(None,u"""
    Qu'est-ce qui reste? [käski'räst?] : Mis jääb üle?
    """)


#~ """
#~ le nôtre ['nootrə] : meie oma
#~ """

Reeglid.add_lesson(u"eu", u"""
Tähekombinatsioon **eu** hääldatakse **[öö]** või **[ÖÖ]**.
Heli **[ö]** on eesti keeles alati *kinnine* (hääldamiskirjelduses väikese tähega). 
Prantsuse keeles on lisaks *avatud* **[ÖÖ]** (hääldamiskirjelduses suure tähega).
Ja nende erinevus on oluline.

Hääldamiskirjelduses on *kinnine* **ö** *väikese* tähega, 
*avatud* **Ö** *suure* tähega.
""")
Reeglid.parse_words(Nom,u"""
le feu [föö] : tuli
le neveu [nə'vöö] : onupoeg | tädipoeg
je veux [žə vöö] : ma tahan
""")
Reeglid.parse_words(Autre,u"""
neutre (mf) ['nöötrə] : neutraalne
""")
Reeglid.parse_words(Numerique,u"""
neuf [nÖf] : üheksa
""")
Reeglid.parse_words(Nom,u"""
le professeur [profesÖÖr] : professor
le beurre [bÖÖr] : või
la peur [pÖÖr] : hirm
""")

Reeglid.add_lesson(u"œ", u"""
""")
Reeglid.parse_words(Nom,u"""
le nœud [nöö] : sõlm
le cœur [kÖÖr] : süda
le chœur [kÖÖr] : koor (laulu-)
le bœuf [bÖff] : härg
un œuf [Öf] : muna
une œuvre [ÖÖvrə] : töö, teos
le *hors d'œuvre [hOOr 'dÖÖvrə] : eelroog
""")





Reeglid.add_lesson(u"on ja om", 
u"""
Tähekombinatsioonid **on** ja **om** hääldatakse **[O~]**,
välja arvatud siis kui järgneb täishäälik või teine **n** või **m**.
""")
Reeglid.parse_words(Nom,u"""
le salon [sa’lO~] : salong (= uhke tuba)
un oncle [O~klə] : onu
la bombe ['bO~mbə] : pomm
""")
Reeglid.parse_words(Autre,u"""
bonjour [bO~'žuur] : tere | head päeva | tere hommikust
bonne nuit [bOn'nwi] : head ööd
bon appétit [bOnappe'ti] : head isu
""")



Reeglid.add_lesson(u"an, am, en, em", 
u"""
Tähekombinatsioonid **an**, **am**, **en**, **em** hääldatakse **[A~]**,
välja arvatud siis kui järgneb täishäälik või teine **n** või **m**.
""")
Reeglid.parse_words(Nom,u"""
le rendez-vous [rA~de’vu] : kohtumine
un an [A~] : aasta
une année [a'nee] : aasta
la lampe [lA~pə] : lamp
le commentaire [komA~’täär] : märkus, kommentar
le centre ['sA~trə] : keskus
le genre [žA~rə] : žanre
un enfant [A~'fA~] : laps
un employeur [A~plwa'jÖÖr] : tööandja
""")

Reeglid.add_lesson(u"in, im", 
u"""
Tähekombinatsioonid **in** ja **im** hääldatakse **[Ä~]**,
välja arvatud siis kui järgneb täishäälik või teine **n** või **m**.
""")
Reeglid.parse_words(Nom,u"""
une information [Ä~formasjO~] : informatsioon
un imperméable [Ä~pärme'aablə] : vijmajope
une image [i'maaž] : pilt
le bassin [ba'sÄ~] : bassein
le dessin [de'sÄ~] : joonistus
le vin [vÄ~]: vein
""")
Reeglid.parse_words(Adjectif,u"""
inutile (mf) [inü'til] : kasutu
""")


Reeglid.add_lesson(u"ain, aim, ein, eim", 
u"""
Kui **a** või **e** on **in**/**im** ees, 
siis see sulab nendega kokku ja kaob ära.
""")
Reeglid.parse_words(Nom,u"""
le pain [pÄ~] : sai | leib
le gain [gÄ~] : kasu
la main [mÄ~] : käsi
la faim [fÄ~] : nälg
""")
Reeglid.parse_words(NomPropre,u"""
Reims [rÄ~s] : (linn)
""")

Reeglid.add_lesson(u"ien", 
u"""
Tähekombinatsioon **ien** hääldatakse **[jÄ~]**.
""")
Reeglid.parse_words(None,u"""
le chien [šiÄ~] : koer
""")
Reeglid.parse_words(Autre,u"""
bien [biÄ~] : hästi
rien [riÄ~] : ei midagi
""")

Reeglid.add_lesson(u"oin", 
u"""
Tähekombinatsioon **oin** hääldatakse **[wÄ~]**.
""")
Reeglid.parse_words(None,u"""
le coin [kwÄ~] : nurk
le point [pwÄ~] : punkt
""")
Reeglid.parse_words(Autre,u"""
besoin [bə'zwÄ~] : vaja
loin [lwÄ~] : kauge
""")



Reeglid.add_lesson(u'il', 
u"""
Tähekombinatsioon **il** (sõna lõpus ja kaashääliku taga)
hääldatakse kas **[i]** või **[il]**.
""")
Reeglid.parse_words(None,u"""
il [il] : tema
le persil [pär'sil] : petersell
subtil (m) [süp'til] : peen, subtiilne
un outil [u'ti] : tööriist
le fusil [fü'zi] : püss
gentil (m) [žA~'ti] : armas
un exil [äg'zil] : eksiil
""")

Reeglid.add_lesson(u'*eil* ja *eille*', 
u"""
Tähekombinatsioon **eil** hääldatakse **[eij]**.
""")
Reeglid.parse_words(None,u"""
le réveil [re'veij] : äratuskell
le soleil [so'leij] : päike
la merveille [mär'veijə] : ime
merveilleux [märvei'jöö] : imeline
le réveillon [revei'jO~] : vana-aasta õhtu söök
la groseille [gro'zeijə] : sõstar (punane v. valge) | tikker
vieille (f) [vjeijə] : vana
# la veille [veijə] : pühalaupäev
""")
Reeglid.add_lesson(u"ueil", 
u"""
Tähekombinatsioon **ueil** hääldatakse **[Öj]**.
""")
Reeglid.parse_words(None,u"""
un accueil [a'kÖj] : vastuvõtt
le chevreuil [šəv'rÖj] : metskits
un écureuil [ekü'rÖj] : orav
""")

Reeglid.add_lesson(u"ill", u"""
Tähekombinatsioon **ill** hääldatakse **[iij]** või  **[ij]**.
Erandid on sõnad *ville* ja *mille*.
""")
Reeglid.parse_words(None,u"""
la bille [biije] : kuul
une anguille [A~'giije] : angerjas
la myrtille [mir'tiije] : mustikas
la famille [fa'miije] : perekond
tranquille [trA~kiije] : rahulik
la cuillère [kwi'jäär] : lusikas
le pillage [pij'aaž] : rüüstamine
""")

Reeglid.parse_words(None,u"""
la ville [vil] : linn
mille [mil] : tuhat
le million [mil'jO~] : miljon
""")










Reeglid.add_lesson(u"h", u"""
Kirjatäht **h** ei hääldata kunagi.
""")
Reeglid.parse_words(Nom,u"""
le hélicoptère [elikop'täär] : helikopter
le hôtel [o'täl] : hotell
le autel [o'täl] : altar
""")

if FULL_CONTENT:
  
  Reeglid.add_lesson(u"h aspiré", u"""
  Kuigi kirjatähe **h** ei hääldata kunagi,
  on neid kaks tüüpi: «h muet» (tumm h) 
  ja «h aspiré» (sisse hingatud h).
  Viimane tähistatakse sõnaraamatutes tärniga (*).
  Erinevus koosneb selles, kuidas nad liituvad eesoleva sõnaga.
  Artiklitest "le" ja "la" kaob "e" või "a" 
  siis kui järgnev sõna algab täishäälikuga.
  """)
  Reeglid.parse_words(Nom,u"""
  le hélicoptère [elikop'täär] : helikopter
  le hôtel [o'täl] : hotell
  le homme [Om] : mees
  le *haricot [ari'ko] : uba
  le *héros [e'ro] : kangelane
  le *hibou [i'bu] : öökull
  """)





Reeglid.add_lesson(u"ch", u"""
Tähekombinatsioon **ch** hääldatakse tavaliselt **[š]** 
ja mõnikord (kreeka päritolu sõnades) **[k]**,
ja mitte kunagi **[tš]**.

""")
Reeglid.parse_words(Nom,u"""
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


Reeglid.add_lesson(u"gn", u"""
Tähekombinatsioon **gn** hääldatakse **[nj]**.
""")
Reeglid.parse_words(None,u"""
magnifique (nf) [manji'fik] : surepärane
le cognac [kon'jak] : konjak
la ligne ['linjə] : liin | rida
le signe ['sinjə] : märk
le signal [sin'jal] : signaal
la besogne [bə'zOnjə] : töö | tegu | ülesanne
""")
Reeglid.parse_words(Verbe,u"""
soigner [swan'jee] : ravima | hoolitsema
""")
Reeglid.parse_words(NomGeographique,u"""
Avignon [avin'jO~] : -
""")

Reeglid.add_lesson(u"ing, ang", u"""
Ettevaatust: tähekombinatsioonides **ing** sulavad **in** kokku, 
ja reegel **ng** kohta ei kehti.
Ettevaatust ka: **gn** ei ole **ng**!
""")
Reeglid.parse_words(Nom,u"""
un ange [A~ž] : ingel
un agneau [an'joo] : tall
le singe [sÄ~ž] : ahv
le signe ['sinjə] : märk
le linge [lÄ~ž] : pesu
la ligne ['linjə] : liin | rida
""")





if FULL_CONTENT:

    Eesti.add_lesson(u"b ja p", u"""
    b ja p on prantsuse keeles selgelt erinevad.
    """)
    Eesti.parse_words(None,u"""
    la bière [bjäär] : õlu
    la pierre [pjäär] : kivi
    le bon [bO~] : tšekk | talong
    le pont [pO~] : sild
    le bon ton [bO~'tO~] : viisakus
    le ponton [pO~'tO~] : pontoon (nt. pontoonsild)
    la peau [poo] : nahk
    beau (m.) : ilus
    le bois [bwa] : puu (materjal) | mets
    le poids [pwa] : kaal
    """)



    Eesti.add_lesson(u"d ja t", u"""
    d ja t on prantsuse keeles selgelt erinevad.
    """)
    Eesti.parse_words(None,u"""
    le don [dO~] : annetus
    le ton [tO~] : toon
    le centre ['sA~trə] : keskus
    la cendre ['sA~drə] : tuhk
    je donne [dOn] : ma annan
    la tonne [tOn] : tonn
    le toit [twa] : katus
    le doigt [dwa] : sõrm
    """)

    Eesti.add_lesson(u"g ja k", u"""
    g ja k on prantsuse keeles selgelt erinevad.
    """)
    Eesti.parse_words(None,u"""
    le gond [gO~] : uksehing
    le con [kO~] : loll
    la gare [gaar] : raudteejaam
    le car [kaar] : reisibuss
    car [kaar] : sest
    le garçon [gar'sO~] : poiss
    Qui est Guy? [ki ä gi] : Kes on Guy?
    """)



if False:
  
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


if FULL_CONTENT:
  
    Eesti.add_lesson(u"v ja f", u"""
    Ettevaatust, **v** ei ole **f**!
    """)
    Eesti.parse_words(None,u"""
    vous [vu] : teie
    fou [fu] : hull
    # vous êtes fous [vu'zäät fu] : te olete lollid
    je veux [žə vöö] : ma tahan
    le feu [föö] : tuli
    la fille [fiijə] : tüdruk | tütar
    la vie [vii] : elu
    la fin [fÄ~] : lõpp
    le vin [vÄ~] : vein
    """)

    Eesti.add_lesson(u"Ahv pole märk", u"""
    Ettevaatust, **gn** ei ole **ng**!
    """)
    Eesti.parse_words(Nom,u"""
    le singe [sÄ~ž] : ahv
    le signe ['sinjə] : märk
    le linge [lÄ~ž] : pesu
    la ligne ['linjə] : liin | rida
    """)

    Eesti.add_lesson(u"Sugu on oluline", u"""
    Siin mõned näited, et sugu pole sugugi ebatähtis.
    """)
    Eesti.parse_words(Nom,u"""
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


    Eesti.add_lesson(u"Ära aja segamini!", u"""
    Mõned ilusad harjutused veel.
    """)
    Eesti.parse_words(Autre,u"""
    ces ingrédients [säz Ä~gre'djA~] : need koostisained
    c'est un crétin [sätÖ~ kre’tÄ~] : ta on kretiin
    je dors [žə dOOr] : ma magan
    j'ai tort [že tOOr] : ma eksin
    """)
    Eesti.parse_words(Nom,u"""
    la jambe [žA~mbə] : jalg
    la chambre [šA~mbrə] : tuba
    un agent [la' žA~] : agent
    le chant [lə šA~] : laul
    les gens [žA~] : inimesed, rahvas
    les chants [šA~] : laulud
    """)





General.add_lesson(u"Tervitused", u"""
""")
General.parse_words(Autre,u"""
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
oui [wi] : jah
non [nO~] : ei
""")


if FULL_CONTENT:
  
    General.add_lesson(u"Prantsuse automargid",columns=[FR,PRON],show_headers=False)
    General.parse_words(NomPropre,u"""
    Peugeot [pö'žo] : - 
    Citroën [sitro'än] : - 
    Renault [re'noo] : - 
    """)


    General.add_lesson(u"Prantsuse eesnimed", u"""
    """)
    General.parse_words(NomPropre,u"""
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

General.add_lesson(u"Taluloomad", u"""
""")
General.parse_words(Nom,u"""
la chèvre ['šäävrə] : kits
la brebis [brə'bis] : lammas
le porc [pOOr] : siga
le cochon [ko'šO~] : siga
le cheval [šə'val] : hobune
la vache [vaš] : lehm
le taureau [to'roo] : pull
le veau [voo] : vasikas
le bœuf [bÖff] : härg
""")

General.add_lesson(u"Metsloomad", u"""
""")
General.parse_words(Nom,u"""
la chasse [šas] : jaht
le chasseur [ša'sÖÖr] : jahimees
le chevreuil [šəv'rÖj] : metskits
le cerf [säär] : hirv
la biche [biš] : emahirv
un élan [e'lA~] : põder
le lapin [la'pÄ~] : küülik
le lièvre [li'äävrə] : jänes
le renard [rə'naar] : rebane
un écureuil [ekü'rÖj] : orav
la souris [su'ri] : hiir
le blaireau [blä'roo] : mäger | habemeajamispintsel
le *hérisson [eri'sO~] : siil
la hermine [är'min] : hermeliin
la martre ['martrə] : nugis
la belette [bə'lät] : nirk  
le loup [lu] : hunt
un ours [urs] : karu
le lynx [lÄ~ks] : ilves
le sanglier [sA~gli'e] : metssiga
le marcassin [marka'sÄ~] : metsseapõrsas
""")

# belette : nirk 

if FULL_CONTENT:

  Fun.add_lesson(u"Põdral maja", u"""
  | Dans sa maison un grand cerf 
  | regardait par la fenêtre
  | un lapin venir à lui         
  | et frapper ainsi.
  | «Cerf, cerf, ouvre moi
  | ou le chasseur me tuera!»    
  | «Lapin, lapin entre et viens 
  | me serrer la main.»          
  """)
  Fun.parse_words(Verbe,u"""
  il regardait [rəgar'dä] : ta vaatas
  ouvrir [uv'riir] : avama
  tuer [tü'ee] : tapma
  serrer [sä'ree] : suruma
  """)
  Fun.parse_words(Nom,u"""
  la maison [mä'zO~] : maja
  la fenêtre [fə'näätrə] : aken
  le cerf [säär] : hirv
  le lapin [lapÄ~] : küünik
  le chasseur [ša'sÖÖr] : jahimees
  la main [mÄ~] : käsi
  """)

General.add_lesson(u"Linnud", u"""
""")
General.parse_words(Nom,u"""
la poule [pul] : kana
le poulet [pu'lä] : tibu | kanapoeg
une oie [wa] : hani
le dindeon [dÄ~dO~] : kalkun
la dinde [dÄ~də] : emakalkun
le pigeon [pi'žO~] : tuvi
""")

General.add_lesson(u"Kalad", u"""
""")
General.parse_words(Nom,u"""
le brochet [bro'šä] : haug
une anguille [A~'giijə] : angerjas
la perche [pärš] : ahven
le *hareng [ar'~A] : heeringas
le sprat [sprat] : sprot
le thon [tO~] : tuunikala
le requin [rə'kÄ~] : haikala
""")






Kokadele.add_lesson(u"Katame lauda!", u"""
""")
Kokadele.parse_words(Nom,u"""
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

Kokadele.add_lesson(u"Joogid", u"""""")
Kokadele.parse_words(Nom,u"""
la boisson [bwa'sO~] : jook
la bière [bjäär] : õlu
la eau [oo] : vesi
le jus [žu] : mahl
le café [ka'fee] : kohv
le thé [tee] : tee

le vin rouge [vÄ~ 'ruuz]: punane vein
le vin blanc [vÄ~ 'blA~]: valge vein
le vin rosé [vÄ~ ro'zee] : roosa vein
le cidre ['siidrə] : siider
la région [rež'jO~] : regioon, ala
le terroir [ter'waar] : geograafiline veinirühm
une appellation d'origine contrôlée (AOC) [apela'sjO~ dori'žin kO~trO'lee] : kontrollitud päritolumaa nimetus

la bavaroise [bavaru'aaz] : jook teest, piimast ja liköörist
""")

Kokadele.add_lesson(u"Menüü", intro=u"""""")
Kokadele.parse_words(Nom,u"""
le plat [pla] : roog 
le plat du jour [pla dü žuur] : päevapraad
le *hors d'œuvre [OOr 'dÖÖvrə] : eelroog
le dessert [des'säär] : magustoit
""")

Kokadele.add_lesson(u"Supid", u"""
""")
Kokadele.parse_words(Nom,u"""
la soupe [sup] : supp 
le potage [po'taažə] : juurviljasupp
le potage purée [po'taažə pü'ree] : püreesupp
le velouté [vəlu'tee] : koorene püreesupp
le velouté Dubarry [vəlu'tee düba'ri] : koorene püreesupp lillkapsaga
le bouillon [bui'jO~] :  puljong 
le consommé [kO~som'mee] : selge puljong 
le consommé de volaille [kO~som'mee də vo'lajə] : linnulihast puljong 
le consommé de gibier [kO~som'mee də žib'jee] : ulukilihast puljong 
le consommé de poisson [kO~som'mee də pwa'sO~] : kala puljong 
le consommé double [kO~som'mee 'duublə] : kahekordne puljong 
#rammuleem?
""")



Kokadele.add_lesson(u"Liha", u"""
""")
Kokadele.parse_words(Nom,u"""
la boucherie [bušə'rii] : lihakauplus, lihakarn
la viande [vjA~də] : liha
la volaille [vo'lajə] : linnuliha
le gibier [žibiee] : jahiloomad
le poisson [pwa'sO~] : kala
le lard [laar] : pekk
un os [os] : kont
la côte [koot] : ribi
le dos [do] : selg
la langue [lA~gə] : keel
le foie [fwa] : maks
les tripes [trip] : soolestik
le cœur [kÖÖr] : süda
le rognon [ron'jO~] : neer
la cervelle [ser'vell] : aju
les abats [a'ba] : subproduktid (maks,süda, neerud, keel, jalad)
""")



Kokadele.add_lesson(u"Liharoad", u"""""")
Kokadele.parse_words(Nom,u"""
l'escalope (f) [eska'lOp] : eskalopp, šnitsel
le ragoût [ra'gu] : raguu
la roulade [ru'laadə] : rulaad
la paupiette [pop'jät] : liharull
l'aspic (m) [as'pik] : sült
le filet [fi'lä] : filee | võrk
le bifteck [bif'täk] : biifsteek
la brochette [bro'šät] : lihavarras, šašlõk
les attereaux [attə'roo] : fritüüris praetud varras, paneeritud šašlõk
la côtelette [kot'lät] : naturaalne kotlet
la côtelette de porc [kot'lät də pOOr] : sealiha kotlet
la noisette de porc [nwa'zät də pOOr] : filee sealiha
le goulasch [gu'laš] : guljašš
le *hachis [ha'ši] : hakkliha
la boulette [bu'lett] : lihapall
le tournedos [turnə'do] : veise sisefilee portsjon toode
la entrecôte [A~trə'koot] : antrekoot
le Chateaubriand [šatobri'A~] : praetud liharoog
le carré d'agneau [ka'ree dan'joo] : praetud tallerind
la poitrine d'agneau farcie [pwa'trin dan'joo far'sii] : täidetud tallerind
le cœur de filet [kÖÖr də fi'lä] : veise sisefilee
le filet mignon [fi'lä min'jO~] : veise sisefilee portsjon toode
le filet médaillon [fi'lä meda'jO~] : medaljon (veise sisefilee portsjon toode)
le médaillon de veau [meda'jO~ də'voo] : vasika medaljon
le bœuf bourguignon [bÖff burgin'jO~] : härjapraad burgundia veiniga
le bœuf à la tartare [bÖff a la tar'taar] : väiketükiline toode sisefileest
le bœuf à la Strogonov [bÖff a la strogo'nov] : böfstrogonov
le sauté de bœuf à la suédoise [so'tee də bÖff a la süee'dwaazə] : klopsid
le sauté de veau [so'tee də voo] : pajaroog vasikalihast
la selle de mouton [säl də mu'tO~] : lamba (talle) sadul
""")


Kokadele.add_lesson(u"Road", intro=u"""""")
Kokadele.parse_words(Nom,u"""
la purée [pü'ree] : püree
un œuf [Öf] : muna
les œufs brouillés [öö brui'jee] : omlett
les œufs pochés [öö po'šee] : ilma kooreta keedetud muna
le gratin [gra'tÄ~] : gratään (ahjus üleküpsetatud roog)
le gratin dauphinois [gra'tÄ~ dofinw'a] : (tuntud retsept)
le gratin savoyard [gra'tÄ~ savwa'jaar] : (juustuga gratin dauphinois)
le soufflé [suff'lee] : suflee

la fondue [fO~'düü] : fondüü
le fumet [fü'mä] : hea lõhn (nt. veini, liha kohta)
le pâté [pa'tee] : pasteet
le pâté en croûte [pa'tee A~'krut] : küpsetatud taignas pasteet
le pâté en terrine [pa'tee A~ter'rin] : küpsetatud pasteet kausis
la galantine [galA~'tin] : galantiin
le cassoulet [kasu'lä] : Languedoc'ist pärit ühepajatoit ubadest ja lihast, mida küpsetatakse mitu tundi madala temperatuuriga ahjus.
le pot-au-feu [poto'föö] : ühepajatoit
""")



Kokadele.add_lesson(u"Juust", u"""""")
Kokadele.parse_words(None,u"""
le fromage [fro'maaž] : juust
la caillebotte [kajə'bott] : (kodujuust)
la raclette [rak'lett] : kuumaga sulatud juust
le Camembert [kamA~'bäär] : (valgehallitusjuust)
le Emmental [emən'taal] : -
le Rocquefort [rOk'fOOr] : (sinihallitusjuust)
le Gruyère [grüi'jäär] : -
le Edam [e'dam] : -
le Brie [brii] : -
le Fontal [fO~'tal] : -
le Parmesan [parmə'zA~] : -
le Gouda [gu'da] : (holandi juust)
le Aura [o'ra] : -
""")


Kokadele.add_lesson(u"Magustoidud", u"""""")
Kokadele.parse_words(Nom,u"""
le dessert [des'säär] : magustoit
la crème [krääm] : koor
la crème fraiche [krääm 'fräš] : rõõsk koor
la crème brûlée [krääm brü'lee] : põletud koor
la crème bavaroise [krääm bavaru'aaz] : muna-piima-seguga kreem želatiiniga 
la sauce melba [soos mel'ba] : melba kaste
la sauce vanille [soos va'niijə] : vanillikaste
la sauce caramel [soos kara'mäl] : karamellkaste
la crêpe [kräp] : pannkook
la glace [glass] : jäätis
le sorbet [sor'bä] : jäätis (ilma kooreta)
le parfait [par'fä] : parfee
le gâteau [ga'too] : kook
la gaufre ['goofrə] : vahvel
la tarte [tart] : tort
la compote [kO~'pOt] : kompott
la gelée [žə'lee] : tarretis
la confiture [kO~fi'tüür] : moos
la mousse [mus] : vaht
la tarte aux prunes [tarto'prün] : ploomikook
la salade de fruits [sa'laad də frü'i] : puuviljasalat
la salade de baies [sa'laad də bä] : marjasalat
un petit-beurre [pəti'bÖÖr]: (kuiv küpsis)
""")



Kokadele.add_lesson(u"Puuviljad", u"""""")
Kokadele.parse_words(Nom,u"""
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

Kokadele.add_lesson(u"Marjad", u"""""")
Kokadele.parse_words(Nom,u"""
la baie [bä] : mari
la fraise [frääz] : maasikas
la myrtille [mir'tiijə] : mustikas
la mûre [müür] : põldmari
la groseille [gro'zeijə] : sõstar (punane v. valge) | tikker
le cassis [ka'sis] : mustsõstar 
""")


Kokadele.add_lesson(u"Juurviljad", u"""""")
Kokadele.parse_words(Nom,u"""
la légume [le'güm] : juurvili
la pomme de terre [pom də 'täär] : kartul
la tomate [to'mat] : tomat
la carotte [ka'rOt] : porgand
# la betterave []
# le panais
# le radis
# le salsifis
# le cerfeuil
la asperge [as'pärž] : spargel
le épinard [epi'naar] : spinat
le concombre [kO~kO~brə]: kurk
un *haricot [ari'ko] : uba
la salade [sa'laadə] : salat
la endive [A~'diiv] : endiiv
# le chicon [ši'kO~] : 
le chou [šu] : kapsas
le chou-fleur [šu 'flÖÖr] : lillkapsas
""")

Kokadele.add_lesson(u"Teraviljad", u"""""")
Kokadele.parse_words(Nom,u"""
le blé [blee] : teravili
l'avoine (f) [avu'ann] : kaer
le froment [fro'mA~] : nisu
le sarrasin [sara'zÄ~] : tatar
le blé noir  [blee'nwaar] : tatar
le riz [ri] : riis
le seigle ['sääglə] : rukis
l'orge (m) ['Oržə] : oder
""")

Kokadele.add_lesson(u"Teraviljatooded", u"""""")
Kokadele.parse_words(Nom,u"""
le riz pilaf [ri pi'laf] : pilaff
les pâtes ['paat] : pastaroad
la farine [far'in] : jahu
la bouillie [bui'jii] : puder
le gruau [grü'oo] : puder
le pain [pÄ~] : sai | leib
la tartine [tar'tin] : võileib
la baguette [ba'gät] : prantsuse pikk sai
le croustillon [krusti'jO~] : õlis praetud kohupiimapall
""")


Kokadele.add_lesson(u"Koostisosad", u"""""")
Kokadele.parse_words(Nom,u"""
le ingrédient [Ä~gre'djA~] : koostisosa 
le lait [lä] : piim
le beurre [bÖÖr]: või
la crème [kr’ääm] : kreem | koor
le sucre ['sükrə] : suhkur
le sel [säl] : sool
le poivre ['pwaavrə] : pipar
""")


Kokadele.add_lesson(u"Ürdid", u"""""")
Kokadele.parse_words(Nom,u"""
un assaisonnement [asäzon'mA~] : maitsestamine
le condiment [kO~di'mA~] : maitseaine
une épice [e'pis] : vürts
les fines herbes [fin'zärbə] : fines herbes ("peened ürdid")
une herbe [ärbə] : ürt
le persil [pär'sil] : petersell
le céléri [sele'ri] : seller
la gousse d'ail [guss 'daij] : küüslaugu küün
l'ail (m) [aj] : küüslauk
un oignon [on'jO~] : sibul
la ciboulette [sibu'lät] : murulauk
la câpre ['kaaprə] : kappar
le gingembre [žÄ~žA~brə] : ingver
""")


Kokadele.add_lesson(u"Köögiriistad", u"""""")
Kokadele.parse_words(Nom,u"""
la cuisine [kwi'zin] : köök
la cuisinière [kwizin'jäär] : pliit
le four [fuur] : ahi
le four à micro-ondes [fuur a mikro 'O~də] : mikrolaine ahi
le fouet [fu'ä] : vispel
le moulin [mu'lÄ~] : veski
la alumette [alu'mät] : tuletikk
la coquille [ko'kiijə] : merekarp
la cocotte [ko'kot] : malmkastrul, kokott
la poêle [pwal] : pann
la râpe [rap] : riiv
la casserole [kas'roll] : kastrul
la marmite [mar'mit] : katel
la braisière [bräz'jäär] : pott smoorimiseks 
le caquelon [kak'lO~] : fondüüpott
le bain-marie [bÄ~ma'rii] : veevann
""")


Kokadele.add_lesson(u"Mida kokk teeb", intro=u"""
""")
Kokadele.parse_words(Verbe,u"""
préparer [prepa'ree] : ette valmistama
# composer [kO~po'zee] : koostama
# baisser [bäs'see] : alla laskma, madaldama
# porter [por'tee] : kandma
laver [la'vee] : pesema
concasser [kO~kas'see] : peenestama (tükkideks)
farcir [far'siir] : farssima (täidisega täitma)
*hacher [a'šee] : hakkima
éplucher [eplü'šee]: koorima
émincer [émÄ~'see] : lõikama viiludeks
tourner [tur'nee] : keerama, pöörama
# utiliser [ütili'zee] : kasutama
préchauffer [préšoo'fee] : ette kütma
""")


Kokadele.add_lesson(u"Pliidil", u"""""")
Kokadele.parse_words(Nom,u"""
la cuisson [küis'sO~] : keetmine
le blanchiment [blA~ši'mA~] : blanšeerimine
le rôtissage [rotis'saaž] : praadimine (panni peal)
le rissolement [risol'mA~] : praadimine 
la friture [fri'tüür] : friipraadimine (õlis või rasvas)
le grillage [gri'jaaž] : röstimine
le braisage [bre'zaaž] : smoorimine
""")

#~ le bain marie [bÄ~ ma'rii] : 

Kokadele.parse_words(Verbe,u"""
cuire [kwiir] : keetma
blanchir [blA~'šiir] : blanšeerima
rôtir [ro'tiir] : praadima (panni peal)
rissoler [risso'lee]: (rasvas) pruunistama
frire [friir] :  praadima (õlis)
griller [gri'jee] : röstima
braiser [brä'zee] : smoorima
""")







u"""
On met une majuscule 
uniquement quand l’adjectif est employé comme 
nom pour désigner une personne. 
Ex. : Les Français parlent en français à leurs amis français
"""
General.add_lesson(u"Riigid",columns=[GEON("Riik"), GEOM, GEOF, ET])
General.parse_words(None,u"""
la France [frA~s] | français [fra~'sä] | française [fra~'sääz] : Prantsusmaa
l'Estonie (f) [ästo'nii] | estonien [esto'njÄ~] | estonienne [esto'njän] : Eesti
l'Allemagne (f) [al'manjə] | allemand [al'mA~]| allemande [al'mA~də] : Saksamaa
l'Angleterre (f) [A~glə'täär] | anglais [A~'glä]| anglaise [A~'glääz] : Inglismaa
la Belgique [bel'žik] | belge [belžə]| belge [belžə] : Belgia
la *Hollande [o'lA~də] | hollandais [olA~'dä] | hollandaise [olA~'dääz] : Holland
l'Espagne (f) [es'panjə] | espagnol [espan'jol] | espagnole [espan'jol] : Hispaania
l'Italie (f) [ita'lii] | italien [ital'jÄ~]| italienne [ital'jen] : Itaalia
""")

if FULL_CONTENT:
    General.add_lesson(u"Linnad prantsusmaal",columns=[GEON("Linn"), GEOM, GEOF])
    General.parse_words(NomGeographique,u"""
    Avignon [avin'jO~] | avignonnais [avinjo'nä] | avignonnaise [avinjo'nääz] : -
    Bordeaux [bor'doo] | bordelais [bordə'lä] | bordelaise [bordə'lääz] : -
    Bourgogne [burgOnjə] | bourguignon [burgin'jO~] | bourguignonne [burgin'jOnn] : -
    Dijon [di'žO~] | dijonnais [dižon'nä] | dijonnaise [dižon'nääz] : -
    Lyon [li'O~] | lyonnais [lio'nä] | lyonnaise [lio'nääzə] : -
    Marseilles [mar'säijə] | marseillais [marsäi'jä]| marseillaise [marsäi'jääz] : - 
    Paris [pa'ri] | parisien [pariz'jÄ~]| parisienne [pariz'jän] : Pariis
    Reims [rÄ~s] | rémois [rem'wa]| rémoise [rem'waaz] : Reims
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

Kokadele.add_lesson(u"Omadussõnad (kulinaaria)", intro=u"""
Selliseid omadussõnu leidub erinevates kulinaaria väljundites.
""",columns=[M, F, ET])
Kokadele.parse_words(Adjectif,u"""
beurré [bÖÖ'ree] | beurrée [bÖÖ'ree]: võiga
bouilli [bui'ji] | bouillie [bui'jii] : keedetud
braisé [brä'zee] | braisée [brä'zee] : smooritud
coupé [ku'pee] | coupée [ku'pee] : lõigatud
épicé [epi'see] | épicée [epi'see] : vürtsitatud, vürtsikas
glacé [glas'see] | glacée [glas'see] : jäätunud
haché [a'šee] | hachée [a'šee] : hakkitud
manié [man'jee] | maniée [man'jee] : käsitletud
poché [po'še] | pochée [po'šee] : uputatud keeva vette
rissolé [riso'lee] | rissolée [riso'lee] :  (rasvas) pruunistatud
sauté [soo'tee] | sautée [soo'tee] : rasvas praetud
velouté [velu'tee] | veloutée [velu'tee] : sametine, sametitaoline
croustillant [krusti'jA~] | croustillante [krusti'jA~t] : krõbe
gourmand [gur'mA~] | gourmande [gur'mA~d] : maiasmokk
paysan [pei'zA~] | paysanne [pei'zann] : talu-, talupoja-
royal [rwa'jal] | royale [rwa'jal] : kuninglik
suprême (mf) [sü'prääm] : ülem, kõrgem, ülim
""")




Kokadele.add_lesson(u"Kastmete valmistamine", intro=u"""""")
Kokadele.parse_words(Nom,u"""
la sauce [soos] : kaste

la moutarde [mu'tardə] : sinep
le vinaîgre [vin'äägrə] : äädikas
la mayonnaise [majo'nääz] : majonees
la vinaîgrette [vine'grät] : vinegrett

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

la coupe en brunoise [kup A~ brün'waaz] : juur- või puuvilja kuubikud (2mm)
la coupe julienne [kup jül'jän] : juurvilja lõikamine ribadeks (2mm)
la coupe jardinière [kup žardin'jäär] : juurvilja lõikamine ribadeks
la coupe à la paysanne [kup ala päi'zan] : juurvilja lõikamine ketasteks
""")

Kokadele.add_lesson(u"Kastmed", intro=u"""""")
Kokadele.parse_words(Nom,u"""
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
la sauce Mornay [mOr'nä] : juustukaste
la sauce Porto [pOr'to] : portveini kaste
la sauce Sabayon [saba'jO~] : Sabayon-kaste
la sauce italienne [ital'jän] : itaalia kaste
la sauce veloutée [vəlu'tee] : hele põhikaste
la sauce blanche [blA~šə] : tuletatud hele kaste
la sauce bordelaise [bOrdə'lääz] : punase veini kaste
la sauce béarnaise [bear'nääz] : bernoo kaste

la sauce béchamel [beša'mäl] : valge põhikaste
la sauce aurore [o'rOOr] : aurorakaste
la sauce Choron [šo'rO~] : choronkaste
la sauce Foyot [fwa'jo] : foyotkaste

la macédoine [mase'dwan] : juurviljasalat
""")

Kokadele.add_lesson(u"Veinialad Prantsusmaal", u"""
""",columns=[FR,PRON])
Kokadele.parse_words(NomGeographique,u"""
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

Kokadele.add_lesson(u"Prantsuse veinid", u"""
Prantsuse veinid on üle 400, siin ainult mõned.
""",columns=[FR,PRON])
Kokadele.parse_words(Nom,u"""
le Chasselas [šas'la] : -
le Grand Cru [grA~'krü] : - 
le Pinot Noir [pi'no nwaar] : - 
la Côte de Brouilly [koot də bru'ji] : -
le Saint-Amour [sÄ~ta'muur] : - 
le Bordeaux clairet [bOr'doo klä'rä] : - 
le Médoc [me'dok] : - 
le Saint-Émilion [sÄ~temi'jO~] : - 
la Côte de Beaune [koot də boon] : - 
les Côtes du Ventoux [kootə du vA~'tu] : -
le Minervois [minerv'wa] : - 
les Côtes d'Auvergne [kootə do'värnjə] : -
""")




if FULL_CONTENT:

    General.add_lesson(u"Omadussõnad (üld)", intro=u"""
    Omadussõnad, mis lõpevad "e"-ga, ei muutu soo järgi.
    """,columns=[M, F, ET])
    General.parse_words(Adjectif,u"""
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



    General.add_lesson(u"Loeme kümneni", intro=u"""""")
    General.parse_words(Numerique,u"""
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


    General.add_lesson(u"Värvid", columns=[M, F, ET])
    General.parse_words(Adjectif,u"""
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


if FULL_CONTENT:
    General.add_lesson(u"Kuulsad inimesed")
    General.parse_words(NomPropre,u"""
    Jacques Chirac [žaak ši'rak] : # endine president
    Georges Brassens [žorž bra'sÄ~s] : # laulja
    Brigitte Bardot [bri'žit bar'do] : # laulja
    Louis de Funès [lu'i də fü'nääz] : # näitleja
    """)

    General.add_lesson(u"Kuud")
    General.parse_words(NomPropre,u"""
    janvier [žA~'vjee] : jaanuar
    février [fevri'ee] : veebruar
    mars [mars] : märts
    avril [a'vril] : aprill
    mai [mä] : mai
    juin [žwÄ~] : juuni
    juillet [žwi'jä] : juuli
    août [ut] : august
    septembre [sep'tA~brə] : september
    octobre [ok'tOObrə] : oktoober
    novembre [no'vA~brə] : november
    décembre [de'sA~brə] : detsember
    """)

    General.add_lesson(u"Majad ja nende osad")
    General.parse_words(Nom,u"""
    la maison [mä'zO~] : maja
    la cave [kaav] : kelder
    la cuisine [kwi'zin] : köök
    la salle de bain : vannituba
    la chambre à coucher : magamistuba
    le salon [sa’lO~] : elutuba
    un escalier [eskal'jee] : trepp
    la fenêtre [fə'näätrə] : aken
    le parterre [par'täär] : esimene korrus
    le premier étage [prəm'jeer_etaaž] : teine korrus
    le jardin [žar'dÄ~] : aed
    """)

if FULL_CONTENT:


    Fun.add_lesson(u"Virelangues", intro=u"""
    #. Poisson sans boisson est poison. 
    #. Un chasseur sachant chasser doit savoir chasser sans son chien. 
    #. Ecartons ton carton, car ton carton me gêne. 
    #. Ton thé t'a-t-il ôté ta toux? 
    #. Chacun cherche son chat.
    #. Tante, en ton temps teintais-tu tes tempes?
    """)
    Fun.parse_words(Nom,u"""
    le poisson [pwa'sO~] : kala
    le poison [pwa'zO~] : mürk
    la boisson [bwa'sO~] : jook
    le chasseur [ša'sÖÖr] : jahimees
    le chien [šiÄ~] : koer
    la toux [tu] : köha
    """)
    Fun.parse_words(Verbe,u"""
    savoir [sa'vuaar] : teadma | oskama
    chercher [šär'šee] : otsima
    écarter [ekar'tee] : eest ära liigutama
    ôter [oo'tee] : ära võtma
    """)
    Fun.parse_words(Autre,u"""
    sans [sA~] : ilma
    chacun [ža'kÖ~] : igaüks
    """)


if FULL_CONTENT:

    General.add_lesson(u"Lisa", intro=u"""
    """)
    General.parse_words(Autre,u"""
    environ [A~vi'rO~] : umbes
    facilement [fasil'mA~] : lihtsalt
    rapidement [rapidə'mA~]: kiiresti
    le autre [ootrə] : teine
    le même [määm] : sama
    """)

    General.parse_words(Verbe,u"""
    filer [fi'lee] : ketrama
    baiser [bä'zee] : musitama
    sauter [soo'tee] : hüppama
    """)

    General.parse_words(Nom,u"""
    le midi [mi'di] : lõun | keskpäev
    le soir [swaar] : õhtu
    le matin [ma'tÄ~] : hommik
    la tranche [trA~š] : lõik | viilukas
    la coupe [kupp] : lõikamine | pokaal
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

if __name__ == '__main__':
    if fmt == "rst":
        book.add_index(u"Sõnaraamat")
        book.write_rst_files(sys.argv[2])
    elif fmt == "odt":
        book.add_dictionary(u"Sõnade nimekiri")
        fn = sys.argv[2]
        book.write_odt_file(fn)
        os.startfile(fn)
