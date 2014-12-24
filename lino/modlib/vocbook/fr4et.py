# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Work in progress.

See :srcref:`docs/tickets/92`.

"""

from __future__ import unicode_literals

import os
import sys

from lino.modlib.vocbook.fr import French, Autre, Nom, NomPropre, Adjectif, Numerique, Verbe, NomGeographique
from lino.modlib.vocbook.et import Estonian
from lino.modlib.vocbook.base import Book, FR, M, F, ET, PRON, GEON, GEOM, GEOF

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception("""
    Usage : %(cmd)s rst OUTPUT_ROOT_DIR
        %(cmd)s odt OUTPUT_FILE
    """ % dict(cmd=sys.argv[0]))
    output_format = sys.argv[1]
else:
    output_format = 'rst'

if output_format == "rst":
    FULL_CONTENT = True
else:
    FULL_CONTENT = False


HAS_FUN = True
HAS_EXERCICES = True

book = Book(French, Estonian,
            title="Kutsealane prantsuse keel kokkadele",
            input_template=os.path.join(
                os.path.dirname(__file__), 'Default.odt'))
    #~ os.path.join(os.path.dirname(__file__),'cfr.odt')

Pronounciation = book.add_section(u"Hääldamine", intro=u"""
Esimeses osas keskendume hääldamisele.
Siin pole vaja meelde jätta näidissõnu,
vaid et sa oskaksid neid ette lugeda õigesti hääldades.
""")
Intro = Pronounciation.add_section("Sissejuhatus", intro="""
""")
Eestlastele = Pronounciation.add_section("Eestlastele", intro="""
""")
Pronounciation.add_lesson(u"Hääldamisreeglite spikker", intro=u"""

Hääldamisreeglid:

[ruleslist 
ai
ail
ain
an
au
c
cedille
ch
eau
eil
ein
en
ent
er
et
eu
euil
g
gn 
gu
h
ien
il
ill 
in
j
oi
oe
oin
on
ou
u
ueil
ui 
un
y]

""")


Reeglid = Pronounciation.add_section(u"Reeglid", ref="reeglid")

if output_format == "rst":
    Reeglid.intro = u"""

    Ülevaade:

    - [ref u], [ref ou], [ref ui], [ref eu], [ref au], [ref eau], [ref oi], [ref ai], [ref y], [ref oe]
    - [ref on], [ref an], [ref en], [ref un], [ref in], [ref ain], [ref ein], [ref ien], [ref oin]
    - [ref c],  [ref h], [ref ch], [ref cedille]
    - [ref er], [ref et], [ref ent] 
    - [ref j], [ref g], [ref gu], [ref gn]
    - [ref il], [ref ill], [ref ail], [ref eil], [ref euil], [ref ueil]

    """


#~ if FULL_CONTENT:
    #~ Eesti = Pronounciation.add_section(u"Veel")
#~ Vocabulary = book.add_section(u"Sõnavara",intro=u"""
#~ Teises osa hakkame õpima sõnavara,
#~ oletades et hääldamine on enam vähem selge.
#~ """)
Vocabulary = book
#~ General = Vocabulary.add_section(u"Üldiselt")
General = Vocabulary.add_section(u"Üldine sõnavara")
Kokadele = Vocabulary.add_section(u"Kulinaaria")
if HAS_FUN:
    Fun = Vocabulary.add_section(u"Laulud")

if HAS_EXERCICES:
    Exercices = Vocabulary.add_section(u"Harjutused")
    Viktoriin = Vocabulary.add_section(u"Viktoriin")


Intro.add_lesson(u"Esimene tund", intro=u"""
Esimeses tunnis teeme väike soojendus huultele.
Erinevus tugeva ja nõrda K, P või T vahel on prantsuse keeles sama
oluline nagu inglise ja saksa keeles.
""")
Intro.parse_words(None, u"""
Pierre, une bière! [pjäär ün bjäär] : Pierre, üks õlu!
le toit et le doigt [lə twa ee lə dwa] : katus ja sõrm
Tu veux du feu? [tü vöö dü föö] : kas tahad tuld?
bonjour [bO~'žuur] : tere | head päeva | tere hommikust
au revoir [orə'vwaar] : nägemiseni
Je m'appelle... [zə ma'päl] : Minu nimi on...
""")

Intro.add_lesson(u"Tuntud sõnad", intro=u"""
Mõned sõnad, mida sa juba tead.
Tutvumine hääldamiskirjaga.
""")
Intro.parse_words(None, u"""
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

- **ou** hääldatakse **[u]**.

- **e** sõna lõpus kaob ära

""")


Intro.add_lesson(u"Hääldamiskirjeldus", intro=u"""
Hääldamiskirjeldustes kasutame 
kohandatud `X-SAMPA 
<http://fr.wiktionary.org/wiki/Annexe:Prononciation/fran%C3%A7ais>`_ variant, 
mis on eestlastele intuitiivsem õppida 
kui näiteks `IPA 
<http://en.wiktionary.org/wiki/Wiktionary:IPA>`_ (International 
Phonetic Alphabet).

- Üldiselt loed lihtsalt seda, mis on nurksulgudes.

- Pikad kaashäälikud on topelt. 

- Apostroof (') näitab, milline silp on **rõhutatud**.
  Prantsuse keeles on rõhk tavaliselt viimasel silbil.

Mõned helid tuleb õppida:

==== ================== ====================== =======================================
täht selgitus           näided e.k.            näided pr.k.
==== ================== ====================== =======================================
[ə]  tumm e             Lott\ **e**            **je** [žə], **ne** [nə]
[o]  kinnine o          L\ **oo**\ ne          **mot** [mo], **beau** [boo]
[O]  avatud o           L\ **o**\ tte          **bonne** [bOn], **mort** [mOOr]
[ö]  kinnine ö          l\ **öö**\ ve          **feu** [föö], **peu** [pöö]
[Ö]  avatud ö           ingl.k. "g\ **ir**\ l" **beurre** [bÖÖr], **jeune** [žÖÖn]
[w]  pehme w            ingl.k. "\ **w**\ ow"  **toilettes** [twa'lät], **boudoir** [bud'waar]
[O~] nasaalne [o]       -                      **bonjour** [bO~'žuur], **mon** [mO~]
[A~] nasaalne [O]       -                      **tante** ['tA~tə], **prendre** ['prA~drə]
[Ö~] nasaalne [Ö]       -                      **un** [Ö~], **parfum** [par'fÖ~]
[Ä~] nasaalne [ä]       -                      **chien** [šiÄ~], **rien** [riÄ~]
==== ================== ====================== =======================================


""")

Eestlastele.add_lesson("Mesilashäälikud", intro="""
"Mesilashäälikud" on **s**, **š**, **z** ja **ž**.
Nad on eesti keeles ka olemas, aga prantsuse keeles on
nende erinevus palju olulisem.
  
=========== ===========================
terav       pehme
=========== ===========================
**s**\ upp  **z**\ oom
**š**\ okk  **ž**\ est
=========== ===========================
  
""", ref="s")
Eestlastele.parse_words(None, u"""
la soupe [sup] : supp
le garage [ga'raaž] : garaaž
le geste [žäst] : žest | liigutus
le choc [žOk] : šokk | löök
""")

if FULL_CONTENT:
    Eestlastele.parse_words(None, u"""
    le genre [žA~rə] : žanre
    """)


Intro.add_lesson(u"Artikkel", intro=u"""
Nagu inglise keeles pannakse ka prantsuse keeles nimisõnade ette *artikkel*.

Prantsuse keeles on kõikidel asjadel lisaks oma **sugu**.
Näiteks laud (*la table*) on naissoost, 
raamat (*le livre*) on meessoost.
Kui sul on mitu lauda või mitu raamatu, 
siis on neil sama artikkel **les**: *les tables* ja *les livres*.

Kui sõna algab täishäälikuga, siis kaob 
artiklitest *le* ja *la* viimane 
täht ära ja nad muutuvad  mõlemad **l'**-ks.

Artiklid *le*, *la* ja *les* nimetatakse **määravaks** artikliteks.
Määrava artikli asemel võib ka olla **umbmäärane** artikkel:
**un** (meessoost), **une** (naissoost) või **des** (mitmus).
Erinevus on nagu inglise keeles, kus on olemas määrav
artikkel **the** ja umbmäärane artikel **a**.
Olenevalt kontekstist kasutatakse kas see või teine.
Näiteks
"I am **a** man from Vigala"
ja 
"I am **the** man you need".

Kokkuvõteks:

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

Intro.add_lesson(u"Rõhutud, aga lühike", intro=u"""
Rõhutatud täishäälikud ei ole sellepärast tingimata pikad.
Prantsuse keeles tuleb tihti ette, et sõna lõpeb *lühikese* täishäälikuga.
""")
Intro.parse_words(Nom, u"""
le menu [mə'nü] : menüü
le chocolat [šoko'la] : šokolaad
le plat [pla] : roog | kauss
le cinéma [sine'ma] : kino
le paradis [para'di] : paradiis
""")


Intro.add_lesson("Liaison (sõnade sidumine)", intro="""
Prantsuse keeles juhtub, et sõnad sulavad kokku järmise sõnaga,
s.t. nende hääldamine muutub sõltuvalt sellest, mis järgneb.

""", ref="liaison")

Intro.parse_words(None, u"""
un grand homme  [Ö~ grA~ t‿Omm] : üks suur inimene
tout homme  [tu‿t‿Omm] : iga inimene
avec tout son savoir [avÄk tu so~ savuaar] : kõiki oma teadmistega
pas du tout! [pa dü 'tu] : mitte üldse!
les enfants [lÄ‿z‿A~'fA~] : lapsed
venez ici [ve'nee_z_i'si] : tulge sia
les faux amis [foo‿z‿a'mi] : valed sõbrad
bon appétit [bOn‿appe'ti] : head isu
""")


Intro.add_lesson(u"O on kinnine või avatud", u"""
Helid **[o]** ja **[ö]** on eesti keeles alati *kinnised*.
Prantsuse keeles on lisaks ka *avatud* vormid.
Hääldamiskirjelduses on kinnine vorm **väikese** tähega ja
avatud vorm **suure** tähega.
""")
Intro.parse_words(Autre, u"""
je donne [dOn] : ma annan
je dors [dOOr] : ma magan
""")
Intro.parse_words(Nom, u"""
le dos [do] : selg
le mot [mo] : sõna
le tome [toom] : köide
""")

if FULL_CONTENT:
    Intro.parse_words(Nom, u"""
  la mort [mOOr] : surm
  le or [OOr] : kuld
  le boulot [bu'lo] : töö (kõnekeel)
  le bouleau [bu'loo] : kask
  le bureau [bü'roo] : büroo
  """)

if not FULL_CONTENT:

    Eestlastele.add_lesson(u"Cold gold, big pigs and downtowns", u"""
    Erinevus tugeva ja nõrda K, P või T vahel on prantsuse keeles sama
    oluline nagu inglise ja saksa keeles.
    """, ref="kpt")
    Eestlastele.parse_words(Autre, u"""
    la gare [gaar] : raudteejaam | bussijaam
    le car [kaar] : reisibuss
    la bière [bjäär] : õlu
    la pierre [pjäär] : kivi
    le doigt [dwa] : sõrm
    le toit [twa] : katus
    """)


else:

    Eestlastele.add_lesson(u"b ja p", u"""
    b ja p on prantsuse keeles selgelt erinevad.
    """)
    Eestlastele.parse_words(None, u"""
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

    Eestlastele.add_lesson(u"d ja t", u"""
    d ja t on prantsuse keeles selgelt erinevad.
    """)
    Eestlastele.parse_words(None, u"""
    le don [dO~] : annetus
    le ton [tO~] : toon
    le centre ['sA~trə] : keskus
    la cendre ['sA~drə] : tuhk
    je donne [dOn] : ma annan
    la tonne [tOn] : tonn
    le toit [twa] : katus
    le doigt [dwa] : sõrm
    """)

    Eestlastele.add_lesson(u"g ja k", u"""
    g ja k on prantsuse keeles selgelt erinevad.
    """)
    Eestlastele.parse_words(None, u"""
    le gond [gO~] : uksehing
    le con [kO~] : loll
    la gare [gaar] : raudteejaam
    le car [kaar] : reisibuss
    car [kaar] : sest
    le garçon [gar'sO~] : poiss
    Qui est Guy? [ki ä gi] : Kes on Guy?
    """)


Reeglid.add_lesson(u"u", intro=u"""
**u** (siis kui see pole teise täishäälikuga koos)
hääldatakse **[ü]** või **[üü]**.
""", ref="u")
Reeglid.parse_words(Nom, u"""
le bureau [bü'roo] : büroo
le bus [büs] : buss
# le mur [müür] : sein | müür
la puce [püs] : kirp
le jus [žü] : mahl
# le but [büt] : eesmärk
# la pute [püt] : hoor
le sucre ['sükrə] : suhkur
""")

Reeglid.add_lesson(u"ou", intro=u"""
**ou** hääldatakse **[u]** või **[uu]**.
""", ref="ou")
Reeglid.parse_words(None, u"""
le journal [žur'nal] : päevik | ajaleht
le cours [kuur] : kursus | tund (koolis)
le cou [ku] : kael
le goût [gu] : maitse
""")

Reeglid.add_lesson(u"ui",
u"""
**ui** hääldatakse **[wi]** või **[wii]** (mida 
kirjutatakse vahest ka **[üi]** või **[üii]**).
""", ref="ui")
Reeglid.parse_words(None, u"""
la suite [swit] : järg | tagajärg | rida, kord | saatjaskond
bonne nuit [bOnə 'nwi] : head ööd
la cuisine [kwi'zin] : köök
je cuis [žə kwi] : ma keedan
je suis [žə swi] : ma olen | ma järgnen
""")


Reeglid.add_lesson(u"eu", u"""
**eu** hääldatakse **[öö]** või **[ÖÖ]**.
""", ref="eu")
Reeglid.parse_words(None, u"""
le feu [föö] : tuli
# le neveu [nə'vöö] : onupoeg | tädipoeg
je veux [žə vöö] : ma tahan
""")
Reeglid.parse_words(Autre, u"""
# neutre (mf) ['nöötrə] : neutraalne
""")
Reeglid.parse_words(Numerique, u"""
neuf [nÖf] : üheksa
""")
Reeglid.parse_words(Nom, u"""
le professeur [profesÖÖr] : professor
le beurre [bÖÖr] : või
la peur [pÖÖr] : hirm
""")


#~ Reeglid.parse_words(None,u"""
#~ l'huile (f) [wil] : õli
#~ cuire [kwiir] : keetma
#~ suivre ['swiivrə] : järgima
#~ la cuillère [kwi'jäär] : lusikas
#~ """)
Reeglid.add_lesson(u"au",
intro=u"""
**au** hääldatakse **[o]** või **[oo]**.
""", ref="au")
Reeglid.parse_words(None, u"""
une auberge [o'bäržə] : võõrastemaja
un auteur [o'tÖÖr] : autor
""")

Reeglid.add_lesson(u"eau",
intro=u"""
**eau** hääldatakse **[oo]**.
Nagu [ref au], aga **e** ühineb nendega ja kaob ära.
""", ref="eau")
Reeglid.parse_words(None, u"""
le château [ša'too] : loss
le bateau [ba'too] : laev
la eau [oo] : vesi
""")


Reeglid.add_lesson(u"oi",
u"""
**oi** hääldatakse **[wa]**.
Vaata ka [ref oin].
""", ref="oi")
Reeglid.parse_words(Autre, u"""
voilà [vwa'la] : näe siin 
trois [trwa] : kolm
bonsoir [bO~'swaar] : head õhtut
au revoir [orə'vwaar] : nägemiseni
""")
Reeglid.parse_words(Nom, u"""
le roi [rwa] : kuningas
la loi [lwa] : seadus
la toilette [twa'lät] : tualett
""")


Reeglid.add_lesson(u"ai",
u"""
**ai** hääldatakse **[ä]** või **[ää]** 
(mõnikord ka **[ə]**).
""", ref="ai")
Reeglid.parse_words(Nom, u"""
la maison [mä'zO~] : maja
le domaine [do'mään] : domeen
la fraise [frääz] : maasikas
# la paire [päär] : paar
""")
Reeglid.parse_words(Adjectif, u"""
frais [frä] | fraiche [fräš] : värske
""")
Reeglid.parse_words(None, u"""
nous faisons [nu fə'zO~] : meie teeme
le faisan [fə'zA~] : faasan
""")


Reeglid.add_lesson(u"y", u"""
**y** hääldatakse alati **[i]** ja mitte kunagi **[ü]**.
""", ref="y")
Reeglid.parse_words(Nom, u"""
le cygne ['sinjə] : luik
le système [sis'tääm] : süsteem
le mythe [mit] : müüt
""")


Reeglid.add_lesson(u"œ", u"""
**œ** hääldatakse alati **[ÖÖ]**.
""", ref="oe")
Reeglid.parse_words(Nom, u"""
# le nœud [nöö] : sõlm
le cœur [kÖÖr] : süda
#le chœur [kÖÖr] : koor (laulu-)
le bœuf [bÖff] : härg
le œuf [Öf] : muna
la œuvre [ÖÖvrə] : töö, teos
le *hors d'œuvre [hOOr 'dÖÖvrə] : eelroog
""")


if HAS_FUN:

    Fun.add_lesson(u"Frère Jacques", u"""
| Frère Jacques, frère Jacques,
| dormez-vous? Dormez-vous? 
| Sonnez les matines, sonnez les matines
| ding, dang, dong! Ding, dang, dong!
""")
    Fun.parse_words(NomPropre, u"""
    Jacques [žaak] : Jaak
    """)
    Fun.parse_words(None, u"""
    le frère [fräär] : vend
    dormez-vous? [dOrmee'vu] : kas Te magate?
    Sonnez les matines [sO'ne lä ma'tinə] : lööge hommikukellad
    """)

    Fun.add_lesson(u"Dans sa maison un grand cerf ", u"""
| Dans sa maison un grand cerf 
| regardait par la fenêtre
| un lapin venir à lui         
| et frapper ainsi.
| «Cerf, cerf, ouvre moi
| ou le chasseur me tuera!»    
| «Lapin, lapin entre et viens 
| me serrer la main.»   

..  youtube:: 8SW1dg7ZipU

""")

    Fun.parse_words(Verbe, u"""
  il regardait [rəgar'dä] : ta vaatas
""")

    Fun.parse_words(None, u"""
  ouvre-moi [uuvrə'mwa] : tee mulle lahti
  ou [u] : või
  il me tuera [il mə tüə'ra] : ta tapab mind 
  serrer [sä'ree] : suruma
  grand [grA~] | grande [grA~də]: suur
  """)
    Fun.parse_words(Nom, u"""
  la maison [mä'zO~] : maja
  le cerf [säär] : hirv
  la fenêtre [fə'näätrə] : aken
  le lapin [lapÄ~] : küünik
  le chasseur [ša'sÖÖr] : jahimees
  la main [mÄ~] : käsi
  """)

    Fun.add_lesson(u"Un kilomètre à pied", u"""
| Un kilomètre à pied,
| ça use, ça use, 
| un kilomètre à pied, 
| ça use les souliers.
""")
    Fun.parse_words(None, u"""
    le pied [pjee] : jalaots
    à pied [a'pjee] : jalgsi
    ça use [sa 'üüzə] : see kulutab
    le soulier [sul'jee] : king
    """)

    Fun.add_lesson(u"La peinture à l'huile", u"""
| La peinture à l'huile
| c'est bien difficile
| mais c'est bien plus beau
| que la peinture à l'eau
""")
    Fun.parse_words(None, u"""
    la peinture [pÄ~'tüür] : värvimine
    la huile [wilə] : õli
    la eau [oo] : vesi
    difficile [difi'silə] : raske
    mais [mä] : aga
    beau [boo] | belle [bälə] : ilus
    plus beau [plü boo] : ilusam
    """)


if HAS_FUN:

    Fun.add_lesson(u"Meunier, tu dors", u"""
| Meunier, tu dors, ton moulin va trop vite.
| Meunier, tu dors, ton moulin va trop fort.

| Ton moulin, ton moulin va trop vite.
| Ton moulin, ton moulin va trop fort.

""")
    Fun.parse_words(None, u"""
le meunier [mÖn'jee] : mölder
le moulin [mu'lÄ~] : veski
tu dors [dOOr] : sa magad
trop vite [tro'vitə] : liiga kiiresti
trop fort [tro'fOOr] : liiga kõvasti
    """)

if HAS_FUN and FULL_CONTENT:

    Fun.add_lesson(u"Minu onu...",
    u"""
| Mon tonton et ton tonton sont deux tontons,
| mon tonton tond ton tonton 
| et ton tonton tond mon tonton.
| Qu'est-ce qui reste?

    """)
    Fun.parse_words(None, u"""
    mon [mO~] : minu
    ton [tO~]: sinu
    ils sont [sO~]: nad on
    """)
    Fun.parse_words(Numerique, u"""
    deux [döö] : kaks
    """)
    Fun.parse_words(Nom, u"""
    le tonton [tO~'tO~] : onu
    """)
    Fun.parse_words(Verbe, u"""
    tondre [tO~drə] : pügama
    rester [räs'tee] : üle jääma
    """)
    Fun.parse_words(None, u"""
    Qu'est-ce qui reste? [käski'räst?] : Mis jääb üle?
    """)


#~ """
#~ le nôtre ['nootrə] : meie oma
#~ """


Reeglid.add_lesson(u"on & om",
u"""
**on** ja **om** hääldatakse **[O~]**,
v.a. siis kui järgneb täishäälik või teine **n** või **m**.
""", ref="on")
Reeglid.parse_words(Nom, u"""
le salon [sa'lO~] : salong (= uhke tuba)
# un oncle [O~klə] : onu
la bombe ['bO~mbə] : pomm
""")
Reeglid.parse_words(Autre, u"""
bonjour [bO~'žuur] : tere | head päeva | tere hommikust
bonne nuit [bOnə 'nwi] : head ööd
bon appétit [bOn‿appe'ti] : head isu
""")


Reeglid.add_lesson(u"an & am",
u"""
**an** ja **am** hääldatakse **[A~]**,
v.a. siis kui järgneb täishäälik või teine **n** või **m**.
""", ref="an")
Reeglid.parse_words(Nom, u"""
le an [A~] : aasta
la année [a'nee] : aasta
la lampe [lA~p] : lamp
le enfant [A~'fA~] : laps
""")


Reeglid.add_lesson(u"en & em",
u"""
**en** ja **em** hääldatakse **[A~]**,
v. a. siis kui järgneb täishäälik või teine **n** või **m**.
""", ref="en")
Reeglid.parse_words(Nom, u"""
le rendez-vous [rA~de'vu] : kohtumine
# le commentaire [komA~'täär] : märkus, kommentar
le centre ['sA~trə] : keskus
le renne [rän] : põhjapõder
# le genre [žA~rə] : žanre
un enfant [A~'fA~] : laps
le employeur [A~plwa'jÖÖr] : tööandja
""")

Reeglid.add_lesson(u"un & um",
u"""
**um** ja **un** hääldatakse **[Ö~]**,
v.a. siis kui järgneb täishäälik või teine **m** / **n**.
""", ref="un")
Reeglid.parse_words(NomPropre, u"""
Verdun [vär'dÖ~] : -
""")
Reeglid.parse_words(Nom, u"""
le parfum [par'fÖ~] : hea lõhn v. maitse
""")
Reeglid.parse_words(Adjectif, u"""
parfumé [parfü'mee] | parfumée [parfü'mee] : lõhnastatud
brun [brÖ~] | brune [brün] : pruun
# aucun [o'kÖ~] | aucune [o'kün] : mitte üks
""")

#~ chacun [ža'kÖ~] | chacun [ža'kün] : igaüks


Reeglid.add_lesson(u"in & im",
u"""
**in** ja **im** hääldatakse **[Ä~]**,
v.a. siis kui järgneb täishäälik või teine **n** või **m**.
Vaata ka [ref ain].
""", ref="in")
Reeglid.parse_words(None, u"""
la information [Ä~formasjO~] : informatsioon
le imperméable [Ä~pärme'aablə] : vihmajope
la image [i'maaž] : pilt
le vin [vÄ~]: vein
le bassin [ba'sÄ~] : bassein
le dessin [de'sÄ~] : joonistus
je dessine [de'sin] : ma joonistan
""")
Reeglid.parse_words(Adjectif, u"""
inutile (mf) [inü'til] : kasutu
""")


#~ Reeglid.add_lesson(u"ain, aim, ein, eim",
#~ u"""
#~ Kui **a** või **e** on **in**/**im** ees,
#~ siis see sulab nendega kokku ja kaob ära.
#~ """,ref="ain")
#~ Reeglid.parse_words(Nom,u"""
#~ le pain [pÄ~] : sai | leib
#~ le gain [gÄ~] : kasu
#~ la main [mÄ~] : käsi
#~ la faim [fÄ~] : nälg
#~ """)
#~ Reeglid.parse_words(NomPropre,u"""
#~ Reims [rÄ~s] : (linn)
#~ """)

Reeglid.add_lesson(u"ain & aim",
u"""
**ain** ja **aim** hääldatakse **[Ä~]**. **a** ühineb **in**/**im**-ga ja kaob ära.
Sama loogika nagu [ref ein].
""", ref="ain")
Reeglid.parse_words(Nom, u"""
le pain [pÄ~] : sai | leib
# le gain [gÄ~] : kasu
la main [mÄ~] : käsi
la faim [fÄ~] : nälg
""")

Reeglid.add_lesson(u"ein & eim",
u"""
**ein** ja **eim** hääldatakse **[Ä~]**. **e** ühineb **in**/**im**-ga ja kaob ära.
Sama loogika nagu [ref ain].
""", ref="ein")
Reeglid.parse_words(Nom, u"""
le rein [rÄ~] : neer (anat.)
la reine [rään] : kuninganna
""")
Reeglid.parse_words(NomPropre, u"""
Reims [rÄ~s] : (linn)
""")

Reeglid.add_lesson(u"ien",
u"""
**ien** hääldatakse **[jÄ~]** v.a. siis kui järgneb teine **n**.
""", ref="ien")
Reeglid.parse_words(None, u"""
le chien [šiÄ~] : koer
la chienne [šjän] : emakoer
""")
Reeglid.parse_words(Autre, u"""
bien [biÄ~] : hästi
rien [riÄ~] : ei midagi
""")

Reeglid.add_lesson(u"oin",
u"""
**oin** hääldatakse **[wÄ~]**.
Reegel [ref oi] ei kehti sel juhul, sest *i* sulab *n*-iga kokku.
""", ref="oin")
Reeglid.parse_words(None, u"""
# le coin [kwÄ~] : nurk
le point [pwÄ~] : punkt
""")
Reeglid.parse_words(Autre, u"""
besoin [bə'zwÄ~] : vaja
# loin [lwÄ~] : kauge
""")


Reeglid.add_lesson(u"c", u"""
**c** hääldatakse **[s]** siis 
kui järgneb **e**, **i** või **y**,
ja muidu **[k]** (ja mitte kunagi **[tš]**).
Sõna lõpus kaob mõnikord ära.
""", ref="c")
Reeglid.parse_words(None, u"""
la casserole [kas'roll] : kastrul
la confiture [kO~fi'tüür] : moos | keedis
la cuisse [kwis] : reis | kints
le certificat [särtifi'ka] : tsertifikaat
la cire [siir] : vaha
le centre ['sA~trə] : keskus
le cygne ['sinjə] : luik
la classe [klas] : klass
le tabac [ta'ba] : tubak
""")
Reeglid.parse_words(NomPropre, u"""
octobre [ok'tOObrə] : oktoober
Marc [mark] : Markus
""")
Reeglid.parse_words(Numerique, u"""
cinq [sÄ~k] : viis
""")

if FULL_CONTENT:
    Reeglid.parse_words(None, u"""
le câble ['kaablə] : kaabel
la cible ['siiblə] : märklaud
la comédie [kome'dii] : komöödia
le comble ['kO~blə] : kõrgeim v. ülim aste
la cure [küür] : kuur
la croûte [krut] : koorik
un acacia [akasj'a] : akaatsia (põõsas)
  """)


Reeglid.add_lesson(u"h", u"""
**h** ei hääldata kunagi.
""", ref="h")
#~ (Vaata ka [ref haspire])
Reeglid.parse_words(Nom, u"""
le hélicoptère [elikop'täär] : helikopter
le hôtel [o'täl] : hotell
le autel [o'täl] : altar
""")


if FULL_CONTENT:

    Reeglid.add_lesson(u"h aspiré", u"""
  Kuigi **h** ei hääldata kunagi ([vt. [ref h]]),
  on neid kaks tüüpi: «h muet» (tumm h) 
  ja «h aspiré» (sisse hingatud h).
  Viimane tähistatakse sõnaraamatutes tärniga (*).
  Erinevus koosneb selles, kuidas eesolev sõna liitub nendega.
  """, ref="haspire")
    Reeglid.parse_words(Nom, u"""
  le hélicoptère [elikop'täär] : helikopter
  le hôtel [o'täl] : hotell
  le homme [Om] : mees
  le *haricot [ari'ko] : uba
  le *héros [e'ro] : kangelane
  le *hibou [i'bu] : öökull
  """)


Reeglid.add_lesson(u"ch", u"""
**ch** hääldatakse tavaliselt **[š]** ja mõnikord (kreeka päritolu sõnades) **[k]**,
ja mitte kunagi **[tš]**.
""", ref="ch")
Reeglid.parse_words(Nom, u"""
le chat [ša] : kass
la biche [biš] : emahirv
le chœur [kÖÖr] : koor (laulu-)
le psychologue [psiko'lOOgə] : psüholoog
""")

"""
la chèvre ['šäävrə] : kits
la chambre [šA~mbrə] : tuba
le parachute [para'šüt] : langevari
le Christe [krist] : Kristus
une chope [žOp] : õlu
le chien [šjÄ~] : koer
un achat [a'ša] : ost
"""


Reeglid.add_lesson(u"ç", u"""
**ç** hääldatakse alati **[s]**.
""", ref="cedille")
Reeglid.parse_words(None, u"""
la leçon [lə~sO~]: lektsioon
# la rançon [rA~sO~]: lunaraha
le reçu [rə'sü] : kviitung
le maçon [ma'sO~] : müürsepp
""")


Reeglid.add_lesson(u"-er & -ez",
u"""
**-er** ja **-ez** sõna lõpus hääldatakse **[ee]**. 
""", ref="er")
Reeglid.parse_words(None, u"""
manger [mA~'žee] : sööma
vous mangez [mA~'žee] : te sööte
aimer [ä'mee] : armastama
vous aimez [ä'mee] : te armastate
""")

Reeglid.add_lesson(u"-et",
u"""
**-et** sõna lõpus hääldatakse **[ä]**. 
""", ref="et")
Reeglid.parse_words(None, u"""
le fouet [fu'ä] : vispel
le fumet [fü'mä] : hea lõhn (nt. veini, liha kohta)
""")

Reeglid.add_lesson(u"-ent",
u"""
**-ent** sõna lõpus hääldatakse **[ə]** siis kui tegemist 
on *tegusõna kolmada mitmuse vormiga*. 
Muidu kehtib reegel [ref en] (hääldatakse **[A~]**).
""", ref="ent")
Reeglid.parse_words(None, u"""
ils couvent [il 'kuuvə] : nad munevad
le couvent [ku'vA~] : klooster
souvent [su'vA~] : tihti
""")


Reeglid.add_lesson(u"j",
u"""
**j** hääldatakse **[ž]** (ja mitte [dž]).
""", ref="j")
Reeglid.parse_words(None, u"""
majeur [mažÖÖr] : suurem
je [žə] : mina
jamais [ža'mä] : mitte iialgi
""")
Reeglid.parse_words(NomPropre, u"""
Josephe [žo'zäf] : Joosep
""")


Reeglid.add_lesson(u"g",
u"""
**g** hääldatakse **[g]** kui järgneb **a**, **o**, **u** 
või kaashäälik, aga **[ž]** kui järgneb **e**, **i** või **y**.
""", ref="g")
Reeglid.parse_words(None, u"""
le gorille [go'rijə] : gorilla
la gazelle [ga'zäl] : gasell
la giraffe [ži'raf] : kaelkirjak
# le gymnase [žim'naaz] : gümnaasium
# le juge [žüüž] : kohtunik
# la géologie [žeolo'žii] : geoloogia
général [žene'ral] : üldine
le général [žene'ral] : generaal
""")

Reeglid.add_lesson(u"gu",
u"""
**gu** hääldatakse **[g]** (s.t. **u** kaob ära)
siis kui järgneb **e**, **i** või **y**.

""", ref="gu")
Reeglid.parse_words(None, u"""
le guépard [ge'paar] : gepard
le guide [giid] : reisijuht
la guitare [gi'taar] : kitarr
la guerre [gäär] : sõda
Guy [gi] : (eesnimi)
Gustave [güs'taav] : (eesnimi)
aigu [ä'gü] : terav, ...
""")


Reeglid.add_lesson(u"gn", u"""
**gn** hääldatakse **[nj]**.
""", ref="gn")
Reeglid.parse_words(None, u"""
magnifique (nf) [manji'fik] : surepärane
le cognac [kon'jak] : konjak
le signal [sin'jal] : signaal
""")
#~ Reeglid.parse_words(Verbe,u"""
#~ soigner [swan'jee] : ravima | hoolitsema
#~ """)
Reeglid.parse_words(NomGeographique, u"""
Avignon [avin'jO~] : -
""")

#~ """
#~ la ligne ['linjə] : liin | rida
#~ le signe ['sinjə] : märk
#~ la besogne [bə'zOnjə] : töö | tegu | ülesanne
#~ """


Reeglid.add_lesson(u'il',
u"""
**il** (sõna lõpus ja kaashääliku taga)
hääldatakse kas **[i]** või **[il]**.
""", ref="il")
Reeglid.parse_words(None, u"""
il [il] : tema
le persil [pär'sil] : petersell
le outil [u'ti] : tööriist
# le fusil [fü'zi] : püss
subtil (m) [süp'til] : peen, subtiilne
gentil (m) [žA~'ti] : armas
# le exil [äg'zil] : eksiil
""")

Reeglid.add_lesson(u"ill", u"""
**ill** hääldatakse **[iij]** või  **[ij]**.
Erandid on sõnad *ville* ja *mille*.
""", ref="ill")
Reeglid.parse_words(None, u"""
# la bille [biije] : kuul
la anguille [A~'giije] : angerjas
la myrtille [mir'tiije] : mustikas
la famille [fa'miije] : perekond
la cuillère [kwi'jäär] : lusikas
# le pillage [pij'aaž] : rüüstamine
""")

Reeglid.parse_words(None, u"""
la ville [vil] : linn
mille [mil] : tuhat
le million [mil'jO~] : miljon
""")

#~ tranquille [trA~kiije] : rahulik


Reeglid.add_lesson(u"ail",
u"""
**ail** hääldatakse **[aj]** :
siin ei kehti reegel [ref ai], sest *i* sulab *l*-iga kokku.
""", ref="ail")
Reeglid.parse_words(Nom, u"""
l'ail (m) [aj] : küüslauk
le travail [tra'vaj] : töö
le détail [detaj] : detail
# l'aile (f) [ääl] : tiib
""")
Reeglid.parse_words(NomGeographique, u"""
Versailles [ver'sajə] : Versailles
""")


Reeglid.add_lesson(u'eil',
u"""
**eil** ja **eille** hääldatakse **[eij]**.
""", ref="eil")
Reeglid.parse_words(None, u"""
le réveil [re'veij] : äratuskell
le soleil [so'leij] : päike
la merveille [mär'veij] : ime
merveilleux [märvei'jöö] : imeline
# le réveillon [revei'jO~] : vana-aasta õhtu söök
la groseille [gro'zeij] : sõstar (punane v. valge) | tikker
# vieille (f) [vjeij] : vana
# la veille [veij] : pühalaupäev
""")

Reeglid.add_lesson(u"ueil", u"""
**ueil** hääldatakse **[Öj]**.
""", ref="ueil")
Reeglid.parse_words(None, u"""
le accueil [a'kÖj] : vastuvõtt
le orgueil [Or'gÖj] : ülbus
""")


Reeglid.add_lesson(u"euil",
u"""
**euil** hääldatakse **[Öj]**.
""", ref="euil")
Reeglid.parse_words(None, u"""
le chevreuil [šəv'rÖj] : metskits
le écureuil [ekü'rÖj] : orav
""")


if False:

    Pronounciation.add_lesson(u"[äär]", u"""
    Kui kuuled [äär], siis kirjutad kas **ère**, **aire**, **ère**, **erre** või **er**.
    """)
    Pronounciation.parse_words(None, u"""
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

    Eestlastele.add_lesson(u"v ja f", u"""
Ettevaatust, **v** ei ole **f**!
    """)
    Eestlastele.parse_words(None, u"""
    vous [vu] : teie
    fou [fu] : hull
    # vous êtes fous [vu'zäät fu] : te olete lollid
    je veux [žə vöö] : ma tahan
    le feu [föö] : tuli
    la fille [fiij] : tüdruk | tütar
    la vie [vii] : elu
    la fin [fÄ~] : lõpp
    le vin [vÄ~] : vein
    """)

    Eestlastele.add_lesson("gn ja ng", """
Ettevaatust, **gn** ei ole **ng**!
    """)
    Eestlastele.parse_words(Nom, u"""
    le ange [A~ž] : ingel
    le agneau [an'joo] : tall
    le singe [sÄ~ž] : ahv
    le signe ['sinjə] : märk
    le linge [lÄ~ž] : pesu
    la ligne ['linjə] : liin | rida
    le songe [sO~ž] : unenägu
    la besogne [bə'zOnjə] : ülesanne | kohustus
    """)

    Eestlastele.add_lesson(u"Sugu on oluline", u"""
    Siin mõned näited, et sugu pole sugugi ebatähtis.
    """)
    Eestlastele.parse_words(Nom, u"""
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

    #~ Eestlastele.parse_words(None,u"""
    #~ court (m) [kuur] : lühike
    #~ """)

    Eestlastele.add_lesson(u"Ära aja segamini!", u"""
    Mõned harjutused veel...
    """)
    Eestlastele.parse_words(Autre, u"""
    ces ingrédients [säz Ä~gre'djA~] : need koostisained
    c'est un crétin [sätÖ~ kre'tÄ~] : ta on kretiin
    je dors [žə dOOr] : ma magan
    j'ai tort [žee tOOr] : ma eksin
    """)
    Eestlastele.parse_words(Nom, u"""
    la jambe [žA~mbə] : jalg
    la chambre [šA~mbrə] : tuba
    le agent [la' žA~] : agent
    le chant [lə šA~] : laul
    les gens [žA~] : inimesed, rahvas
    les chants [šA~] : laulud
    """)


if False:

    Eestlastele.parse_words(None, u"""
    le loup [lu] : hunt
    la loupe [lup] : luup
    la joue [žuu] : põsk
    le jour [žuur] : päev
    mou (m) [mu] : pehme
    """)
    #~ Reeglid.parse_words(NomPropre,u"""
    #~ Winnetou [winə'tu] : (isegi maailmakuulsa apatši pealiku nime hääldavad prantslased valesti)
    #~ """)


General.add_lesson(u"Tervitused", u"""
""")
General.parse_words(Autre, u"""
salut [sa'lü] : tervist
bonjour [bO~'žuur] : tere | head päeva | tere hommikust
bonsoir [bO~'swaar] : head õhtut
bonne nuit [bOnə 'nwi] : head ööd
au revoir [orə'vwaar] : nägemiseni

Monsieur [məs'jöö] : härra
Madame [ma'dam] : proua
Mademoiselle [madəmwa'zel] : preili

Comment t'appelles-tu? [ko'mA~ ta'päl tü] : Kuidas on sinu nimi?
Je m'appelle... [zə ma'päl] : Minu nimi on...
Comment vas-tu? [ko'mA~va'tü] : Kuidas sul läheb?

s'il vous plaît [silvu'plä] : palun (Teid)
s'il te plaît [siltə'plä] : palun (Sind)
merci [mer'si] : aitäh
merci beaucoup [mer'si bo'ku] : tänan väga

oui [wi] : jah
non [nO~] : ei

bon appétit [bOn‿appe'ti] : head isu
j'ai faim [žee fÄ~] : mul on kõht tühi
j'ai soif [žee swaf] : mul on janu
je suis fatigué [žə swi fati'gee] : ma olen väsinud
""")


if FULL_CONTENT:

    General.add_lesson(u"Prantsuse automargid",
                       columns=[FR, PRON], show_headers=False)
    General.parse_words(NomPropre, u"""
    Peugeot [pö'žo] : -
    Citroën [sitro'än] : -
    Renault [re'noo] : -
    """)

    General.add_lesson(u"Prantsuse eesnimed", u"""
    """)
    General.parse_words(NomPropre, u"""
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
    General.parse_words(Nom, u"""
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
    General.parse_words(Nom, u"""
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


if HAS_FUN and FULL_CONTENT:

    Fun.add_lesson(u"Au clair de la lune", u"""
| Au clair de la lune,
| Mon ami Pierrot,
| Prête-moi ta plume
| Pour écrire un mot.
| Ma chandelle est morte,
| Je n'ai plus de feu ;
| Ouvre-moi ta porte,
| Pour l'amour de Dieu.
  """)
    Fun.parse_words(None, u"""
  le clair de lune : kuuvalgus
  un ami : sõber
  """)
    Fun.parse_words(Verbe, u"""
  prêter : laenama
  écrire : kirjutama
  ouvrir : avama
  """)
    Fun.parse_words(None, u"""
  la plume : sulg
  """)
    Fun.parse_words(Verbe, u"""
  """)
    Fun.parse_words(None, u"""
  le mot : sõna
  la chandelle : küünlalamp
  """)
    Fun.parse_words(Adjectif, u"""
  mort | morte (adj.) : surnud
  """)
    Fun.parse_words(None, u"""
  le feu [föö] : tuli
  la porte [pOrt] : uks
  un amour : armastus
  Dieu : Jumal
  """)

if HAS_FUN:

    Fun.add_lesson(u"Sur le pont d'Avignon", u"""
| Sur le pont d'Avignon,
| on y danse, on y danse ;
| Sur le pont d’Avignon,
| on y danse tous en rond !
|
| Les beaux messieurs font comme ça,
| et puis encore comme ça.
|
| Les belles dames font comme ça,
| et puis encore comme ça.  
|
| Les cordonniers font comme ça,
| et puis encore comme ça.  
  """)
    Fun.parse_words(None, u"""
  sur : peal
  le pont [pO~] : sild
  on danse tous ['dA~sə] : me kõik tantsime
  en rond : ringis
  les beaux messieurs : ilusad härrad
  les belles dames : ilusad daamid
  ils font [il fO~] : nad teevad
  comme ci [kOm'sa] : niimoodi
  comme ça [kOm'sa] : naamoodi
  et puis encore [e pwi A~'kOOr] : ja siis veel
  le cordonnier [kOrdon'jee] : kingsepp
  """)


if HAS_FUN and FULL_CONTENT:

    Fun.add_lesson(u"J'ai du bon tabac", u"""

| J'ai du bon tabac dans ma tabatière,
| J'ai du bon tabac, tu n'en auras pas.

| J'en ai du fin et du bien râpé
| Mais, ce n'est pas pour ton vilain nez

| J'ai du bon tabac dans ma tabatière
| J'ai du bon tabac, tu n'en auras pas

  """)

if FULL_CONTENT:

    General.add_lesson(u"Linnud", u"""
    """)
    General.parse_words(Nom, u"""
    le oiseau [wa'zoo] : lind
    la poule [pul] : kana
    le poulet [pu'lä] : tibu | kanapoeg
    la oie [wa] : hani
    le dindeon [dÄ~dO~] : kalkun
    la dinde [dÄ~də] : emakalkun
    le pigeon [pi'žO~] : tuvi
    """)


Kokadele.add_lesson(u"Katame lauda!", u"""
""")
Kokadele.parse_words(Nom, u"""
la table ['taablə] : laud
la chaise [šääz] : tool
le couteau [ku'too] : nuga
la fourchette [fur'šet] : kahvel
la cuillère [kwi'jäär] : lusikas
les couverts [ku'väär] : noad-kahvlid
la assiette [as'jät] : taldrik
le bol [bOl] : joogikauss
le verre [väär] : klaas
la tasse [tas] : tass
le plat [pla] : kauss
""")

Kokadele.add_lesson(u"Joogid", u"""""")
Kokadele.parse_words(Nom, u"""
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
la appellation d'origine contrôlée (AOC) [apela'sjO~ dori'žin kO~trO'lee] : kontrollitud päritolumaa nimetus

la bavaroise [bavaru'aaz] : jook teest, piimast ja liköörist
""")

Kokadele.add_lesson(u"Menüü", intro=u"""""")
Kokadele.parse_words(Nom, u"""
le plat [pla] : roog 
le plat du jour [pla dü žuur] : päevapraad
le *hors d'œuvre [OOr 'dÖÖvrə] : eelroog
le dessert [des'säär] : magustoit
""")

Kokadele.add_lesson(u"Supid", u"""
""")
Kokadele.parse_words(Nom, u"""
la soupe [sup] : supp 
le potage [po'taaž] : juurviljasupp
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
Kokadele.parse_words(Nom, u"""
la viande [vjA~də] : liha
la volaille [vo'lajə] : linnuliha
le poulet [pu'lä] : kana
le gibier [žibiee] : jahiloomad

la boucherie [bušə'rii] : lihakauplus, lihakarn
le lard [laar] : pekk
le jambon [žA~'bO~] : sink
la saucisse [soo'sis] : vorst
la graisse [gräs] : rasv

le os [os] : kont
la côte [koot] : ribi
le dos [do] : selg
la cuisse [kwis] : kints
la langue [lA~gə] : keel
le foie [fwa] : maks
les tripes [trip] : soolestik
le cœur [kÖÖr] : süda
le rognon [ron'jO~] : neer (kulin.)
la cervelle [ser'vell] : aju
les abats [a'ba] : subproduktid (maks,süda, neerud, keel, jalad)
""")

Kokadele.add_lesson(u"Kala", u"""
""")
Kokadele.parse_words(Nom, u"""
le poisson [pwa'sO~] : kala
les crustacés [krüsta'see] : karploomad | koorikloomad
le brochet [bro'šä] : haug
la anguille [A~'giijə] : angerjas
la perche [pärš] : ahven
le *hareng [ar'A~] : heeringas
le sprat [sprat] : sprot
le thon [tO~] : tuunikala
le requin [rə'kÄ~] : haikala
""")


Kokadele.add_lesson(u"Liharoad", u"""""")
Kokadele.parse_words(Nom, u"""
la escalope [eska'lOp] : eskalopp, šnitsel
le ragoût [ra'gu] : raguu
la roulade [ru'laadə] : rulaad
la paupiette [pop'jät] : liharull
le aspic [as'pik] : sült
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
Kokadele.parse_words(Nom, u"""
la purée [pü'ree] : püree
le œuf [Öf] : muna
les œufs brouillés [öö brui'jee] : omlett
les œufs pochés [öö po'šee] : ilma kooreta keedetud muna
le gratin [gra'tÄ~] : gratään (ahjus üleküpsetatud roog)
le gratin dauphinois [gra'tÄ~ dofinw'a] : (tuntud retsept)
le gratin savoyard [gra'tÄ~ savwa'jaar] : (juustuga gratin dauphinois)
le soufflé [suff'lee] : suflee
la quiche lorraine [kiš lo'rään] : quiche
la pâte brisée [paat bri'zee] : (Mürbeteig, shortcrust pastry)
la tourte [turt] : (ingl. *pie*)

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
Kokadele.parse_words(None, u"""
le fromage [fro'maaž] : juust
la caillebotte [kajə'bott] : (kodujuust)
la raclette [rak'lett] : kuumaga sulatud juust
le Camembert [kamA~'bäär] : valgehallitusjuust
le Emmental [emən'taal] : suurte augudega kõva juust (Šveits)
le Rocquefort [rOk'fOOr] : (sinihallitusjuust)
le Gruyère [grüi'jäär] :  (Šveits)
le Edam [e'dam] : (Holland)
le Brie [brii] : valgehallitusjuust
le Parmesan [parmə'zA~] : (Itaalia)
le Mascarpone [maskar'poone] : toorjust (Itaalia)
""")


Kokadele.add_lesson(u"Magustoidud", u"""""")
Kokadele.parse_words(Nom, u"""
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
la confiture [kO~fi'tüür] : moos | keedis
la mousse [mus] : vaht
la tarte aux prunes [tarto'prün] : ploomikook
la salade de fruits [sa'laad də frü'i] : puuviljasalat
la salade de baies [sa'laad də bä] : marjasalat
le petit-beurre [pəti'bÖÖr] : (kuiv küpsis)
le pain d'épices [pÄ~ de'pis] : piparkook
""")


Kokadele.add_lesson(u"Puuviljad", u"""""")
Kokadele.parse_words(Nom, u"""
le fruit [frü'i] : puuvili
le ananas [ana'na] : ananass 
la banane [ba'nan] : banaan
le citron [si'trO~] : sidrun
la orange [o'rA~ž] : apelsin
la pomme [pom] : õun
la poire [pu'aar] : pirn
la prune [prünn] : ploom
la cerise [sə'riiz] : kirss
la noix [nwa] : pähkel
la noisette [nwa'zett] : sarapuupähkel
""")

Kokadele.add_lesson(u"Marjad", u"""""")
Kokadele.parse_words(Nom, u"""
la baie [bä] : mari
la fraise [frääz] : maasikas
la myrtille [mir'tiijə] : mustikas
la mûre [müür] : põldmari
la groseille [gro'zeijə] : sõstar (punane v. valge) | tikker
le cassis [ka'sis] : mustsõstar 
""")


Kokadele.add_lesson(u"Juurviljad", u"""""")
Kokadele.parse_words(Nom, u"""
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
le *haricot [ari'ko] : uba
la salade [sa'laadə] : salat
la endive [A~'diiv] : endiiv
# le chicon [ši'kO~] : 
le chou [šu] : kapsas
le chou-fleur [šu 'flÖÖr] : lillkapsas
""")

Kokadele.add_lesson(u"Teraviljad", u"""""")
Kokadele.parse_words(Nom, u"""
le blé [blee] : teravili
la avoine [avu'ann] : kaer
le froment [fro'mA~] : nisu
le sarrasin [sara'zÄ~] : tatar
le blé noir  [blee'nwaar] : tatar
le riz [ri] : riis
le seigle ['sääglə] : rukis
le orge ['Oržə] : oder
""")

Kokadele.add_lesson(u"Teraviljatooded", u"""""")
Kokadele.parse_words(Nom, u"""
le riz pilaf [ri pi'laf] : pilaff
les pâtes ['paat] : pastaroad
la farine [far'in] : jahu
la bouillie [bui'jii] : puder
le gruau [grü'oo] : puder
le pain [pÄ~] : sai | leib
la tartine [tar'tin] : võileib
la baguette [ba'gät] : prantsuse pikk sai
le croustillon [krusti'jO~] : õlis praetud kohupiimapall
le crouton [kru'tO~] : krutoon
""")


Kokadele.add_lesson(u"Koostisosad", u"""""")
Kokadele.parse_words(Nom, u"""
le ingrédient [Ä~gre'djA~] : koostisosa 
le lait [lä] : piim
le beurre [bÖÖr]: või
la crème [kr'ääm] : kreem | koor
le sucre ['sükrə] : suhkur
le sel [säl] : sool
le poivre ['pwaavrə] : pipar
""")


Kokadele.add_lesson(u"Ürdid", u"""""")
Kokadele.parse_words(Nom, u"""
le assaisonnement [asäzon'mA~] : maitsestamine
le condiment [kO~di'mA~] : maitseaine
la épice [e'pis] : vürts
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


Kokadele.add_lesson(u"Köögis", u"""""")
Kokadele.parse_words(Nom, u"""
la cuisine [kwi'zin] : köök
la cuisinière [kwizin'jäär] : pliit
le four [fuur] : ahi
le four à micro-ondes [fuur a mikro 'O~də] : mikrolaine ahi
le moulin [mu'lÄ~] : veski
le congélateur [kO~gela'tÖÖr] : külmutuskapp
un évier [evi'ee] : kraanikauss
la armoire [arm'waar] : kapp
le placard [pla'kaar] : seinakapp
""")

Kokadele.add_lesson(u"Köögiriistad", u"""""")
Kokadele.parse_words(Nom, u"""
le fouet [fu'ä] : vispel
la louche [lušə] : kulp
la alumette [alu'mätə] : tuletikk
la coquille [ko'kiijə] : merekarp
la cocotte [ko'kot] : malmkastrul, kokott
la poêle [pwal] : pann
la râpe [rap] : riiv
la casserole [kas'roll] : kastrul
la russe [rüs] : kastrul
la marmite [mar'mit] : katel
la braisière [bräz'jäär] : pott smoorimiseks 
le caquelon [kak'lO~] : fondüüpott
le bain-marie [bÄ~ma'rii] : veevann
la passoire [pas'waar] : sõel
""")


Kokadele.add_lesson(u"Mida kokk teeb", intro=u"""
""")
Kokadele.parse_words(Verbe, u"""
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
Kokadele.parse_words(Nom, u"""
la cuisson [küis'sO~] : keetmine
le blanchiment [blA~ši'mA~] : blanšeerimine
le rôtissage [rotis'saaž] : praadimine (panni peal)
le rissolement [risol'mA~] : praadimine 
la friture [fri'tüür] : friipraadimine (õlis või rasvas)
le grillage [gri'jaaž] : röstimine
le braisage [bre'zaaž] : smoorimine
""")

#~ le bain marie [bÄ~ ma'rii] :

Kokadele.parse_words(Verbe, u"""
cuire [kwiir] : keetma
blanchir [blA~'šiir] : blanšeerima
rôtir [ro'tiir] : praadima (panni peal)
rissoler [risso'lee]: (rasvas) pruunistama
frire [friir] :  praadima (õlis)
griller [gri'jee] : röstima
braiser [brä'zee] : smoorima
""")


if FULL_CONTENT:
    General.add_lesson(u"Linnad prantsusmaal",
                       columns=[GEON("Linn"), GEOM, GEOF])
    General.parse_words(NomGeographique, u"""
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
#~ français [frA~'sä] | français [frA~'sääz] : prantsuse
#~ estonien [esto'njÄ~] | estonien [esto'njän] : eesti
#~ espagnol [espan'jol] | espagnole [espan'jol] : hispaania
#~ hollandais [olA~'dä] | hollandaise [olA~'dääz]: holandi
#~ """)

Kokadele.add_lesson(u"Omadussõnad (kulinaaria)", intro=u"""
Selliseid omadussõnu leidub erinevates kulinaaria väljundites.
""", columns=[M, F, ET])
Kokadele.parse_words(Adjectif, u"""
beurré [bÖÖ'ree] | beurrée [bÖÖ'ree]: võiga
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

bouilli [bui'ji] | bouillie [bui'jii] : keedetud

croustillant [krusti'jA~] | croustillante [krusti'jA~t] : krõbe
piquant [pi'kA~] | piquant [pi'kA~t] : terav
gourmand [gur'mA~] | gourmande [gur'mA~d] : maiasmokk
paysan [pei'zA~] | paysanne [pei'zann] : talu-, talupoja-
royal [rwa'jal] | royale [rwa'jal] : kuninglik
suprême (mf) [sü'prääm] : ülem, kõrgem, ülim
""")


Kokadele.add_lesson(u"Kastmete valmistamine", intro=u"""""")
Kokadele.parse_words(Nom, u"""
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

la coupe en dés [kup A~ 'dee] : lõikamine kuubikuteks
la coupe en brunoise [kup A~ brün'waaz] : juurvilja lõikamine kuubikuteks (2mm)
la coupe julienne [kup jül'jän] : juurvilja lõikamine ribadeks (2mm)
la coupe jardinière [kup žardin'jäär] : juurvilja lõikamine ribadeks
la coupe à la paysanne [kup ala päi'zan] : juurvilja lõikamine ketasteks
""")

Kokadele.add_lesson(u"Kastmed", intro=u"""""")
Kokadele.parse_words(Nom, u"""
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
""", columns=[FR, PRON])
Kokadele.parse_words(NomGeographique, u"""
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
""", columns=[FR, PRON])
Kokadele.parse_words(Nom, u"""
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


Kokadele.add_lesson(u"Teenindussaalis", u"""
""")
Kokadele.parse_words(Autre, u"""
Puis-je prendre votre manteau? : Kas ma võtan Teie jope?
Avez-vous réservé une table? : Kas teil on laud kinni pandud?
Par ici, je vous prie. : Tulge siit kaudu, palun.
Suivez-moi s'il vous plaît. : Tulge mulle järele, palun.
Cette table-ci est libre. : See laud siin on vaba.
Est-ce que cette table vous convient? : Kas see laud sobib teile?
Voici la carte, Monsieur. : Siin on menüü, härra.
Je souhaite un bon appétit. : Soovin head isu.
Voulez-vous un déssert ou du café? : Kas soovite magustoitu või kohvi?
Est-ce que c'était bon? : Kas toit maitses?
""")





if FULL_CONTENT:

    General.add_lesson(u"Omadussõnad (üld)", intro=u"""
    Omadussõnad, mis lõpevad "e"-ga, ei muutu soo järgi.
    """, columns=[M, F, ET])
    General.parse_words(Adjectif, u"""
    chaud [šoo] | chaude [šoodə] : kuum
    froid [fru'a] | froide [fru'aadə] : külm
    gros [gro] | grosse [grossə] : paks
    mince (mf) [mÄ~s] : õhuke
    bon [bO~] | bonne [bonnə] : hea
    beau [boo] | belle [bälə] : ilus
    joli [žo'li] | jolie [žo'lii] : ilus
    demi [də'mi] | demie [də'mii]: pool
    entier [A~'tjee] | entière [A~'tjäär] : terve, täis
    double (mf) ['duublə] : topelt
    facile (mf) [fa'sil] : lihtne
    possible (mf) [po'siblə] : võimalik
    """)


General.add_lesson(u"Loeme kümneni", intro=u"""""")
General.parse_words(Numerique, u"""
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
General.parse_words(Adjectif, u"""
brun [brÖ~] | brune [brün] : pruun
vert [väär] | verte [värtə] : roheline
bleu [blöö] | bleue [blöö] : sinine
rouge (mf) [ruuž] : punane
jaune (mf) [žoon] : kollane
blond [blO~] | blonde [blO~də] : blond 
beige (mf) [bääž]  : beež
orange (mf) [o'rA~ž]  : oranž
blanc [blA~] | blanche [blA~š] : valge
noir [nwaar] | noire [nwaar] : must
""")

General.add_lesson("Nädalapäevad")
General.parse_words(NomPropre, u"""
lundi ['lÖ~di] : esmaspäev
mardi ['mardi] : teisipäev
mercredi ['merkrədi] : kolmapäev
jeudi ['žöödi] : neljapäev
vendredi ['vA~drədi] : reede
samedi ['samdi] : laupäev
dimanche ['dimA~š] : pühapäev
""")

General.add_lesson(u"Kuud")
General.parse_words(NomPropre, u"""
janvier [žA~vi'ee] : jaanuar
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

General.add_lesson("Reisil")
General.parse_words(None, u"""
la carte d'identité [kartə didA~ti'tee] : id-kaart
le hôtel [o'täl] : hotell
je voyage en voiture [žə vuajaaž A~ vua'tüür] : ma reisin autoga
je voyage en avion [žə vuajaaž A~ avio~] : ma reisin lennukiga
je voyage en train [žə vuajaaž A~ trÄ~] : ma reisin rongiga
""")

General.parse_words(Autre, u"""
Parlez-vous anglais? : Kas Te räägite inglise keelt?
Je parle français... un tout petit peu. : \
  Ma oskan prantsuse keelt... hästi natuke.
Une escalope aux pommes de terre au four, svp. : \
  Palun üks šnitsel ahjukartuliga.
""")



u"""
On met une majuscule 
uniquement quand l'adjectif est employé comme 
nom pour désigner une personne. 
Ex. : Les Français parlent en français à leurs amis français
"""
General.add_lesson(u"Riigid", columns=[GEON("Riik"), GEOM, GEOF, ET])
General.parse_words(None, u"""
la France [frA~s] | français [frA~'sä] | française [frA~'sääz] : Prantsusmaa
l'Estonie (f) [ästo'nii] | estonien [esto'njÄ~] | estonienne [esto'njän] : Eesti
l'Allemagne (f) [al'manjə] | allemand [al'mA~]| allemande [al'mA~də] : Saksamaa
l'Angleterre (f) [A~glə'täär] | anglais [A~'glä]| anglaise [A~'glääz] : Inglismaa
la Belgique [bel'žik] | belge [belžə]| belge [belžə] : Belgia
la *Hollande [o'lA~də] | hollandais [olA~'dä] | hollandaise [olA~'dääz] : Holland
l'Espagne (f) [es'panjə] | espagnol [espan'jol] | espagnole [espan'jol] : Hispaania
l'Italie (f) [ita'lii] | italien [ital'jÄ~]| italienne [ital'jen] : Itaalia
""")


if FULL_CONTENT:
    General.add_lesson(u"Kuulsad inimesed")
    General.parse_words(NomPropre, u"""
    Jacques Chirac [žaak ši'rak] : # endine president
    Georges Brassens [žorž bra'sÄ~s] : # laulja
    Brigitte Bardot [bri'žit bar'do] : # laulja
    Louis de Funès [lu'i də fü'nääz] : # näitleja
    """)

    General.add_lesson(u"Majad ja nende osad")
    General.parse_words(Nom, u"""
    la maison [mä'zO~] : maja
    la cave [kaav] : kelder
    la cuisine [kwi'zin] : köök
    la salle de bain : vannituba
    la chambre à coucher : magamistuba
    le salon [sa'lO~] : elutuba
    un escalier [eskal'jee] : trepp
    la fenêtre [fə'näätrə] : aken
    le parterre [par'täär] : esimene korrus
    le premier étage [prəm'jeer_etaaž] : teine korrus
    le jardin [žar'dÄ~] : aed
    """)

if FULL_CONTENT:

    Fun.add_lesson(u"Devinettes", intro=u"""
#. Que dit un vampire en quittant sa victime? 
   -- Merci beau cou.
#. Pourquoi les marins se marient-ils ? 
   -- Pour avoir une belle mer (mère).
    """)
    Fun.add_lesson(u"Virelangues", intro=u"""
#. Un chasseur sachant chasser doit savoir chasser sans son chien. ([ref s])
#. Chacun cherche son chat.
#. Poisson sans boisson est poison. 
#. Ecartons ton carton, car ton carton me gêne. 
#. Ton thé t'a-t-il ôté ta toux? 
#. Tante, en ton temps teintais-tu tes tempes?
#. Les poules couvent souvent au couvent.
    """)
    Fun.parse_words(Nom, u"""
    le poisson [pwa'sO~] : kala
    le poison [pwa'zO~] : mürk
    la boisson [bwa'sO~] : jook
    le chasseur [ša'sÖÖr] : jahimees
    le chien [šiÄ~] : koer
    la toux [tu] : köha
    """)
    Fun.parse_words(Verbe, u"""
    savoir [sa'vuaar] : teadma | oskama
    chercher [šär'šee] : otsima
    écarter [ekar'tee] : eest ära liigutama
    ôter [oo'tee] : ära võtma
    """)
    Fun.parse_words(Autre, u"""
    sans [sA~] : ilma
    chacun [ža'kÖ~] : igaüks
    """)


if FULL_CONTENT:

    General.add_lesson(u"Lisa", intro=u"""
    """)
    General.parse_words(Autre, u"""
    environ [A~vi'rO~] : umbes
    facilement [fasil'mA~] : lihtsalt
    rapidement [rapidə'mA~]: kiiresti
    le autre [ootrə] : teine
    le même [määm] : sama
    """)

    General.parse_words(Verbe, u"""
    filer [fi'lee] : ketrama
    baiser [bä'zee] : musitama
    sauter [soo'tee] : hüppama
    """)

    General.parse_words(Nom, u"""
    le midi [mi'di] : lõun | keskpäev
    le soir [swaar] : õhtu
    le matin [ma'tÄ~] : hommik
    la tranche [trA~š] : lõik | viilukas
    la coupe [kupp] : lõikamine | pokaal
    la ébullition [ebüjis'jO~] : keemine
    le feu [föö] : tuli
    le baiser [bä'zee] : suudlus
    le appétit [appe'ti] : isu
    """)

    unused = u"""
    une aurore [or'Or] : koit
    le fil [fil] : niit | lõng | nöör
    une heure [ÖÖr] : tund
    le dauphinois [dofinw'a] : lõunaprantsuse dialekt
    """

if HAS_EXERCICES:
    Exercices.add_lesson(u"Lugeda oskad?", u"""
Õpetaja kirjutab tahvlile sari hääldamiskirjeldusi.
Õpilased loevad ette.
Ainult lugeda, mitte tõlkida.
""")
    Exercices.parse_words(None, u"""
    au clair de lune [okläärdə'lün] : kuuvalguses
    le cœur de filet [kÖÖr də fi'lä] : veise sisefilee
    le dessert [des'säär] : magustoit
    la mousse au chocolat [musošoko'la] : šokoladivaht
    le pot-au-feu [poto'föö] : ühepajatoit
    le petit-beurre [pəti'bÖÖr]: (kuiv küpsis)
    la sauce chasseur [soos ša'sÖÖr] : jahimehe kaste
    Poitou [pwa'tu] : -
    la sauce italienne [soosital'jän] : itaalia kaste
    le gratin dauphinois [gra'tÄ~ dofinw'a] : (tuntud retsept)
    """)

    Exercices.add_lesson(u"Kirjutada oskad?", u"""
Õpetaja loeb ette sari sõnu.
Õpilased kirjutavad paberile, kasutades hääldamiskirjelduse tähestik.
""")
    Exercices.parse_words(None, u"""
le chevreuil [šəv'rÖj] : metskits
le soleil [so'leij] : päike
la boisson [bwa'sO~] : jook
le poisson [pwa'sO~] : kala
le requin [rə'kÄ~] : haikala
la cuillère [kwi'jäär] : lusikas
""")

    Viktoriin.add_lesson("", u"""
Nommez trois ingrédients principaux du tiramisu
""")
    Viktoriin.parse_words(None, u"""
le œuf [Öf] : muna
le sucre ['sükrə] : suhkur
le café [ka'fee] : kohv
le Mascarpone [maskar'poone] : toorjust (Itaalia)
""")

    Viktoriin.add_lesson("", u"""
 Smetana on (a) une épice, (2) une sauce au poisson ou (c) un produit laitier?
""")

    Viktoriin.add_lesson("","""
Kuidas valmistatakse "Glace au four'i" nimeline magustoitu?
(a) ahjus, (b) sügavkülmikus või (c) kaussis?
""")

if output_format == "rst":
    Files = book.add_section(u"Failid", intro=u"""
    
Järgmised faile saad siit alla laadida.

- `Trükitud õpik 2012-13 <dl/2012-13.pdf>`_
- `Trükitud õpik 2012-13 <dl/2013-14.pdf>`_

Kuulamiseks koos trükitud lehtedega:

- `lk. 5 <dl/lk05.mp3>`_
- `lk. 6 <dl/lk06.mp3>`_
- `lk. 7 <dl/lk07.mp3>`_
- `lk. 8 <dl/lk08.mp3>`_

Muu:

- `Laul <dl/o-grand-st-nicolas.pdf>`_
  (esitati detsembris 2012 Vana-Vigala TTK jõulupeol)

- Originaalmenüüd töötajate restoranist:
  `1 <dl/menus/20130415.pdf>`_
  `2 <dl/menus/20130923.pdf>`_
  `3 <dl/menus/20130930.pdf>`_
  `4 <dl/menus/20131007.pdf>`_
  `5 <dl/menus/20131014.pdf>`_
  `6 <dl/menus/20131028.pdf>`_
  `7 <dl/menus/20131104.pdf>`_
  `8 <dl/menus/20131111.pdf>`_


""")


if output_format == "rst":
    Files = book.add_section(u"Lingid", intro=u"""

Apprenez le français avec Vincent:

- `Home page <https://www.youtube.com/user/imagiers/>`_

- Learn French with 10 time-lapses and videos:
  `1 <https://www.youtube.com/watch?v=V_q59qWBsNk>`_
  `2 <https://www.youtube.com/watch?v=cVXWXcVBdl8>`_
  `3 <https://www.youtube.com/watch?v=_F_p09pHdj4>`_
  `4 <https://www.youtube.com/watch?v=tGsWmnDtynM>`_
  `9 <https://www.youtube.com/watch?v=ff5NmumRc8g>`_

- `La nourriture <https://www.youtube.com/watch?v=MjDcUT-UEBY>`_

- `Les légumes <https://www.youtube.com/watch?v=Wm7qZp_1gvg>`_

- `Dans la cuisine (Vol 1) <https://www.youtube.com/watch?v=EZhyOg0irCY>`_

- `Dans la cuisine (Vol 2)
  <https://www.youtube.com/watch?v=BcyJECjjCfo>`_

Chansons:

- 
  `Je l'aime à mourir <https://www.youtube.com/watch?v=bMZVtFCU0ZQ>`_
  (Francis Cabrel)
- `C'était l'hiver <https://www.youtube.com/watch?v=YgiSLsdBN0g>`_
  (Isabelle Boulay)

- Jacques Brel:
  `Dans le port d'Amsterdam <https://www.youtube.com/watch?v=r8lWkNnhJB0>`_
  /
  `Ne me quite pas <https://www.youtube.com/watch?v=5N0KLu4vfkE>`_
  /
  Les bourgeois (`vidéo <https://www.youtube.com/watch?v=dCHi5apc1lQ>`_ /
  `chant et texte <https://www.youtube.com/watch?v=KP5TtgwvWaM>`_)

- Edith Piaf:
  `Non, je ne regrette rien <https://www.youtube.com/watch?v=Q3Kvu6Kgp88>`_ /
  `La vie en rose <https://www.youtube.com/watch?v=kFzViYkZAz4>`_

- Renaud:
  `Manu <https://www.youtube.com/watch?v=DtCbYUcYK50>`_ /
  `Laisse béton <https://www.youtube.com/watch?v=iC5eMh1FuaU>`_ /
  `Hexagone <https://www.youtube.com/watch?v=2RQHsn2ilfA>`_ /
  `Mistral Gagnant <https://www.youtube.com/watch?v=jYb_aYgmGP4&list=PLFA40C2CDA5827B3D>`_ (chanté par `Coeur de pirate <https://www.youtube.com/watch?v=iRGGTaAhexc>`_)
  

""")


if __name__ == '__main__':
    if output_format == "rst":
        book.add_index(u"Sõnaraamat")
        book.write_rst_files(sys.argv[2])
    elif output_format == "odt":
        if False:
            book.add_dictionary(u"Sõnade nimekiri")
        fn = sys.argv[2]
        book.write_odt_file(fn)
        os.startfile(fn)
