#coding: latin1

from lino.gendoc.pdf import PdfMaker
from lino.gendoc.styles import mm, TA_RIGHT


class Song:
    def __init__(self,number,title1,text1,title2,text2=None):
        self.number=number
        self.title1=title1
        self.text1=text1
        self.title2=title2
        self.text2=text2

songs=[]

def song(*args,**kw):
    songs.append(Song(*args,**kw))


def footer(story):
    story.memo("""
    <table class="EmptyTable">
    <tr><td align="left">
    (Left footer)
    <td align="right">
    (Right footer)
    </table>
    """)

def header(story):
    story.memo("""
    <table class="EmptyTable">
    <tr><td align="left">
    (Left header)
    <td align="right">
    (Right header)
    </table>
    """)

    
    
def body(story):
    story.getStyle().update(
        #showBoundary=True,
        leftMargin=60*mm,
        rightMargin=30*mm,
        topMargin=40*mm,
        bottomMargin=40*mm,
        footer=footer,
        header=header,
        )
    
    for s in songs:
        #story.h1(str(s.number)+" "+s.title2+" ("+s.title1+")")
        #story.table(s.text1,s.text2)
        
        story.memo("""
        
        <b>%(number)d. %(title2)s (%(title1)s)</b>
        
        <table class="EmptyTable">
        <tr>
        <td valign="top">%(text2)s</td>
        <td align="left">%(text1)s</td>
        </table>
        
        """ % (s.__dict__))
                   
        
        
    

song(1,
     "Dans nos obscurités",
     """Dans nos obscurités allume le feu qui ne s'éteint jamais, qui ne s'étein jamais.""",
     "Me pimeduse sees",
     """Me pimeduse sees sa sära ja süüta kustumatu leek, su kustumatu leek. (2x)""",
     )

song(2,
     "Wait for the Lord","",
     "Oota Issandat",
     """Oota Issandat, ta päev on pea,
     oota Issandat, ja kindlaks jää!""")

song(3,"Bleibet hier","",
     "Siia jää",
     """Siia jää, sa minuga koos, valva ja palu, valva ja palu.""")

song(4,"Ubi caritas Deus ibi est","",
     "Kus on halastus, seal on Jumal ka.",
     """Kus on halastus, armastus,  kus on halastus, seal on Jumal ka.""")



"""     
5 Bless the Lord
Kiida Issandat ja ülista, mu hing. Kiida Issandat, ta ellu juhib mind.
6 Gloria ... et in terra pax (kaanon)
Olgu au, olgu au, Jumalale kõrges, olgu au, olgu au, halleluuja! Rahu olgu maa peal alati, inimestest he-a meel. 
8 C’est toi ma lampe, Seigneur
Mu valgus Issand sa, mu teed sa pimeduses näita. Mu Jumal sa, teed pimeduses näita. 
Mu Jumal sa, teed pimeduses näita.
10 Laudate Dominum
Kiitke nüüd Jumalat, kiitke nüüd Jumalat, rahvad kõikjal, alleluja!
11 Oculi nostri
Pilgud meil pööratud Jeesuse poole, pilgud meil pööratud Issanda poole.
12 De noche
On öö me ümber nii pime, kuid loodame vett veel leida, janu vaid näitab meil valgus eluvee allika juurde.
13 Veni Creator Spiritus (jääb samaks)
14 Tui amoris ignem
Tule, Looja Püha Vaim, süüta me hinges armutuli.
Tule, Looja Püha Vaim, tule, Looja Püha Vaim. 
15 Ubi caritas
Kus on halastus ja armastus, kus on halastus, seal on Ju-mal ka.
16 Bénissez le Seigneur
Laulge kiituselaul! Laulge kiituselaul! Laulge kiituselaul, laulge nüüd Issandal! 
17 El Senyor
Minu Jumal on minu lootus, minu valgus, mu jõud. Kristus on mu karjane ja temas rõõmustab hing ja meel ja temas rõõmustab hing ja meel. (Ps 28,7)
18 Confitemini Domino
Tulge tänage Jumalat, tema on hea. 
Tulge tänage Jumalat, halleluuja.
19 Magnificat
1. Kiidab mu hing, kiidab mu hing, kiidab mu hing ja süda Issand Jumalat. Kiidab mu hing, kiidab mu hing, kiidab mu hing ja süda teda. 
2. Kiidab mu hing, kiidab- mu hing, kiidab hing ja süda Jumalat, kiidab hing ja süda Ju-malat. 
20 Adoramus te Christe
Kummardame sind Kristus, õnnistame su nime, 
su ristisurma läbi lunastatud maailm, 
su ristisurma läbi lunastatud maailm. 
21 Christe Salvator
Jee-sus Kristus, Lu-nastaja, anna meile rahu. 
22 Veni Creator Spiritus
Tule, Looja, tule, Looja, tule, Looja Püha Vaim.
23 Laudate omnes gentes
Oh kiitke nüüd kõik rahvad, oh kiitke Jumalat. 
Oh kiitke nüüd kõik rahvad, oh kiitke Jumalat.
24 Singt dem Herrn
Laulge Issandal uus laul, laulge talle kõik maailm, laulge talle kõik maailm!
25 Gloria, gloria (kaanon)
Kiitus, au, kiitus, au Jumalale kõrges, 
kiitus, au, kiitus, au, halleluuja, halleluuja. 
26 La ténèbre
Meie pimedus pole pime sinu ees, ja öö on sama valge kui päev. (Ps 139,11-12)
27 Jubilate, Alleluia
O--- Jumalale hõiska kogu ilmamaa! 
O--- Halleluu-ja, halleluuja! 
30 In manus tuas, Pater
Oh Isa, sinu kätte ma annan oma vaimu (2x).
34 Cantate Domino (kaanon)
Issandale lau-la. Halleluuja, halleluuja! Jumalale hõiska. 
36 Spiritus Jesu Christi
Kristus on arm ja elu, Kristus on sinu valgus, 
ta kinnitab su südant, ta kinnitab su südant.
37 Jesus, remember me
Jeesus, mind meeles pea, oma kuningriiki tulles. Jeesus, mind meeles pea, oma kuningriiki tulles.
38 Psallite Deo
O--- Hõisake rahvad Jumalal! 
O--- Halleluuja, halleluuja!
41 Magnificat
Hing rõõmusta ja ülista mu Jumalat. 
O--- Hing rõõmusta. O--- Hing rõõmusta.
42 Da pacem … in diebus (kaanon)
Too rahu ilmale, too rahu Kristus sa, meie päevadesse.
43 Veni Lumen (koraal)
O--- Tule Looja, Püha Vaim. 
O--- Valgusta me südameid, valgusta me südameid.
45 Christus resurrexit
O--- Kristus ülestõusnud, Kristus ülestõusnud. 
O--- Halleluuja, halleluuja!
46 In te confido
O--- Jeesus Kristus. O--- Sind usaldame. 
48 Crucem tuam
Kummardame, Issand, sinu risti ees, kiidame su ülestõusmist, su ülestõusmist me. Me kiidame ja ülistame. Kiidame su ülestõusmist, su ülestõusmist me.
50 Nada te turbe
Ära sa karda, ära sa pelga: kellel on Jumal, midagi ei puudu. Ära sa karda, ära sa pelga: Jumalast piisab.
51 Dieu ne peut que donner son amour
Ainus, mis Jumal anda võib sul, on ta arm ja halastus. O--- Ta kingib armu. O--- Ta annab andeks
52 Veni Sancte Spiritus
Tule, Looja Püha Vaim!
53 Dona la pace
Anna sa rahu nüüd neile, kes sinusse usuvad, 
anna, anna sa rahu nüüd neile, anna sa ra-hu.
54 Toi, tu nous aimes
Armastad meid sa, eluvee andja.
57 Vieni Spirito creatore (kaanon)
Tule, Püha Vaim, e-luandja, tule, tu-le.
58 Misericordias Domini
On Jumal halastav, armastav, talle ikka laulan ma.
59 Venite, exultemus Domino
Kõik tulge, rõõmustage Is-sandas, kõik tulge, ülista-ge.
Venite, exultemus Domino, venite, adoremus.
60 O Christe Domine Jesu
O Issand Jee-sus Kristus, O Issand Jee-sus Kristus.
O Christe Domine Jesu, O Christe Domine Jesu!
61 Jubilate coeli (kaanon)
Hõisa-ke kõik taevad, hõisake kõik maad,- Kristus Jee-sus ülestõusnud on.
Jubilate cœli, jubilate mundi, Christus Jesus surrexit vere.
62 Une soif emplit notre âme
Üks ja ainus soov mu hinges: alistuda sinule, Kristus. O--- O--- (Võta kuulda mu häält) Võta kuulda mu häält. O---

63 Benedictus (kaanon)
Kiidetud on kes tuleb, / kiidetud on kes tuleb, / 
me Issanda, me Issanda, / me Issanda ni-mel. 
64 Grande est ta bonté
(a) Suurim armastus on ju see, oma elugi anda meie eest. O--- Jumal sinu heldust kiidame! O---
(b) ...?
65 Dona nobis pacem
(a) Anna meile rahu südameis.
(b) Südamesse anna ra-hu
66 Qui regarde vers Dieu
(a) Pööra Jumala poole oma pilk, 
siis lööd sa särama, kibedus kaob (2x)
(b) Siis kui seisame Isa palge ees, 
särame rõõmust, näos pole kurbust (2x)
(c) Siis kui rändame, pilk on Jumalal,
kaob palgelt kibedus, täidab meid valgus,
meis särab valgus, kaob palgelt kurbus. 
(d) Meie Jumala palge valguses, 
kiirgab me nägu, taganeb valu (2x).
(e) Siis kui rändame, pilk on Jumalal, 
kaob hingest kurbus, täidab meid valgus, 
kaob hingest kurbus, täidab meid valgus.
(f) Kui me Jumala poole vaatame, särame rõõmust, täidab meid valgus, särame rõõmust, täidab meid valgus. 
(g) Kui ma vaatan su poole, säran ma, kaob minu palgelt kurbus ja häbi.
(h) Jumal täidab me palged säraga, kaob hingest kurbus, valu ja häbi, kaob hingest kurbus, valu ja häbi.
(i) Jumal täidab me palged säraga, kaob meie hingest kurbus ja häbi, kaob meie hingest kurbus ja häbi.
(Ps 34,6: Kes tema poole vaatavad, säravad rõõmust ja nende palgeile ei tule kunagi häbi.)
67 Une soif
(a) Kristus, kuule mind, kui palun, ole minu elu siht ja kroon. Rahutu ja ootust täis mu süda, kuni Sinus rahu saan.
(b) Vaid üks soov mul täidab hinge, ennast sulle anda, Kristus. Rahutu ja ootust täis mu süda, kuni sinus puhkan ma.
(c) Ainus igatsus mu hinges: Kristusele ennast kaotada. Rahutu ja ootust täis mu süda, kuni sinus puhkab ta.
(Ps 63; Mk10,28; Mt 19,27; Mt 11,29)
68-97 (jäävad samaks)
98 Bogoroditse Dievo 1
(jääb samaks)
99 Les Béatitudes  (todo)
100 Lumière de nos coeurs
(a) Me südamete valgus, Issand, igavikutee; me looja ja eluandja, ühendab meid su Püha Vaim. Halleluuja! Sa armastus ja arm, meid hüüad enda juurde. Su hääl lõhestab me öö, vastuseks hõiskame me sulle kiitust. Halleluuja!
(b) ...Su hääl lõhestab me öö ja hinges kiituseväravad avab. Halleluuja! 
101 Rendez grâce au Seigneur
Halleluuja, halleluuja, halleluuja. 1. Andke tänu Issandal, sest ta on hea, igavene tema arm, halleluuja. 2. Andke tänu ülestõusnud Kristusel, igavene tema arm, halleluuja. 3. Andke tänu Pühale Vaimule, igavene tema arm, halleluuja. 
102 Souviens-toi de Jésus Christ
(todo)
103-115 (jäävad samaks)
116-119 Meie isa  (todo)
120 Sviaty Bože (jääb samaks)
121 In resurrectione tua
Su ülestõusmises, oh Jeesus Kristus, taevas ja maa rõõmustavad (2x). 
122 Cristos voskrésié iz miertvih
(todo)
123 Bóg jest miloscia
(a) Jumal on armastus. Andesta, siis sul Issand on ligi. Jumal on armastus, ole julge sa.
(b) Jumal on armastus. Andesta, siis ta on sinu kõrval. Jumal on armastus, ära pelga sa.
(c) Jumal on armastus. Elada julge sa armastades. Jumal on armastus. Ära pelga sa. 
124 Beati voi poveri
(a) Nii õndsad, te vaesed, teie päralt Taevariik igavene.
(b) ...?
125 The kingdom of God
On õiglus ja rahu Jumalariik ja rõõm tema Pühas Vaimus. Tule ja ava me sees su kuningriigi värav.
126 Jesu redemptor
Jeesus, me kõigi lunastus, sa valgus ja Isa hiilgus, au olgu sinule, Jeesus, au olgu sinule.
127 Nebojte se
Unusta hirm, rõõmusta nüüd! Kristus surnuist ülestõusnud on.
128 Eat this bread

129 Bleib mit deiner Gnade
Meie juurde armuga jää – öö saabub pea. Sa meie juurde armuga jää, Kristus me valgus. 
130 Amen, amen (jääb samaks)
131 Wyslawiajcie Pana
Hüüdke Issandale, O---. Hüüdke Issandale, O---. Laulge talle kogu maailm, halleluuja, halleluuja. 
132 El alma que anda en amor
Hing, mis on täis armastust, ei väsi ega tüdi. O--- O---
133 Bendigo al Señor
(a) Ma kiidan Issandat, sest ta kuuleb minu häält, 
Issand on minu kalju ja teda ma usaldan.
(b) ... Issand jõudu mul annab, mu südant ta kinnitab.
(c) ...oma jõu saan ma temalt, mu südant ta kinnitab.
134 L’ajuda em vindrà
Kõik abi ma saan Jumalalt, Jumalalt, kes meie Issand, ta teinud taeva ja maa, kõik taeva ja maa.
135 Christe, lux mundi
Kristus me valgus, kes järgib Sinu teed, on temal eluvalgus, eluvalgus.
136 Esprit consolateur
(a) Mu Lohutaja Vaim, sa armastus ja arm. O--- O---
(b) Sa Lohutaja Vaim...
137 Nothing can ever
Mitte miski ei saa meid lahutada Jumalast, ta armastust meil ilmutas Jeesus Kristus. O---.
138 Kristus, din Ande
Kristus, su Vaim meie sees, eluallikas on igavene.
139 Bogoroditse Dievo 2 
(jääb samaks)
140 I am sure I shall see
(a) Kindlalt tean, et kord näen ma elavate maal meie Jumala headust. Jah, ükskord näen ma elavate maal meie Jumala headust.
(b) Näha loodan ma siin sel elavate maal meie Jumala headust. Jah, näha loodan elavate maal ta headust, kindlaks jään!
(c) Näha saan ükskord ma siin elavate maal meie Jumala headust. Ta peale loodan, usus kindlaks jään, ma ootan Issandat!
Ps 27,13-14: Ometi ma usun, et saan näha Issanda headust elavate maal. Oota Issandat, ole vahva, ja su süda olgu kindel! Oh, oota Issandat! 

141 Que j’exulte et jubile
O--- Sinu heldus mu hinge rõõmustab!
142 Cantate Domino canticum novum
Nüüd laulge Jumalal kiituselaulu. Halleluuja, halleluuja. Nüüd laulge Jumalal kogu maailm. Halleluuja, halleluuja. 
143 Magnificat 3 (jääb samaks)
144 Cantarei ao Senhor
(a) Tahan Issandat kiita ja hõisata, talle laulda nii kaua kui elan ma. Minu hing see rõõmustab temas, minu hing see rõõmustab temas. 
(b) Oma südames laulan lakkamata, hinges tänan ja kiidan Issandat ma. Temas rõõmustan kuni elan, temas rõõmustan kuni elan.
(c) Tahan eluaeg kiita Issandat ma, tahan temale laulda ja mängida. Minu süda rõõmustab temas, minu süda rõõmustab temas.
(d) Tahan alati kiita Issandat ma, tahan lõputult laulda ja mängida. Jumal on mu südame rõõm, Jumal on mu südame rõõm.
(Ps 104,33-34: Ma tahan laulda Issandale oma eluaja / ja mängida oma Jumalale, / niikaua kui ma olen elus. / Olgu mu mõlgutus armas tema meelest; / mina rõõmutsen Issandas. )
145 Dominus Spiritus est
Issand me Jumal on Vaim. Jumal on Vaim, kes teeb elavaks. Jumal on Vaim, kes teeb elavaks. 
146 Ad te Jesu Christe
Su poole, oh Jee-sus ma tõstan o-ma hinge. Mu Lunasta-ja, su peale loodan. 
Su poole, oh Jee-sus nüüd oma hinge ma tõstan. Me kõigi Pääst-ja, su peale loodan. 
147 Seigneur, tu gardes mon âme
Oo arm, Sa valvad mu hinge, oo Jumal, Sa tunned mind. Juhi minu südant igavesel teel, juhi minu südant igavesel teel.
148 Frieden, Frieden
(a) Rahu, rahu, rahu jätan ma teil. Oma rahu annan- ma teie südametesse.
(b) ...?
(Joh 14,27: Rahu ma jätan teile, oma rahu ma annan teile. (...) Teie süda ärgu ehmugu ega mingu araks!)
149 Viešpatie, tu viska žinai
Issand, minust kõike sa tead. Sina tead, oled mul armas.
(Joh 21,17) 
150 Behüte mich Gott
(a) Oh, hoia mind sa, sind ma usaldan, Sa kutsud mu teele ellu. Su juures rõõm ja täiuslik rahu. 
(b) Mind hoia nüüd sa, sind ma usaldan, sa saadad mu teele ellu. Su juures rõõm ja täiuslik rahu. 
151 Sit nomen Domini
Kiidetud ol-gu su ni-mi- Issand. Kiidetud nü-üd ja igavesti.
152 Fiez-vous en Lui
Usaldame sind, ei karda me. Su rahu hoiab me südameid. Usaldame sind. Alleluja, alleluja!
153 Je sais que mon rédempteur est vivant
154 Jésus Christ, o clarté d'en haut
155 Vous qui sur la terre habitez


Järgmised tõlged on veel arutelus:
7 Notre âme attend
(a) Sind, Issand, ootab me hing, sest sinust tuleb meie rõõm.
(b) Sind, Issand, ootab me hing, sa meie südamete rõõm. 

9 Jésus le Christ
(a) Kristus, me rõõm ja hingede valgus, keela me sees pimedusel kõnelda. Kristus, me rõõm ja hingede valgus, täida meid oma armuga sa.
(b) Palume sind, me Kristus, me valgus, tule ja vaigista pimeduse hääl. Palume sind, me Kristus, me valgus, aita armule hing avada.
(c) Kristus, tõe vaim, me südame valgus, keela me sees pimedusel kõnelda. Kristus, tõe vaim, me südame valgus, täida meid oma armuga sa.
(d) Palume sind, oh Kristus me valgus, vaigista varjude kõne meie sees. Palume sind, oh Kristus me valgus, aita meil avada hing armule.
(e) Kristus, mu rõõm, sa valgus mu hinges, vaigista varjude kõne minu sees. Kristus, mu rõõm, sa valgus mu hinges, ava mind oma armastusele.

28 Toi qui nous aimes (canon)
Sa, kes meid hoiad, armastad ja andeks annad, kiitust sul lauldes paraneb me murtud süda. 
(lauluga 28 on mingi copyrightiga seotud probleem ja paistab, et seda laul ei tohi tõlgida ega trükida... kui sain ise aru, miks see nii on, siis annan teada.)

29 Ostende nobis (kaanon)
Ilmuta meile, Issand, sa oma armu ja heldust. Aamen! Aamen! Maranata! Maranata! 
(a) Osuta meile, Is-sand, osuta meile halastust. 
(b) Sa meile Issand osuta oma halastust ja armu.
(c) Osuta Issand armulik meil oma rohket halastust.
(d) Sa meile Issand osuta halastust rohket ja armu. 

31 Jubilate Deo (kaanon) (jääb samaks)
32 Mon âme se repose
(a) Vaid Jumalas võib leida rahu mu hing, sest temast tuleb mu pääs. Jumalas leiab rahu minu hing, leiab rahu mu hing.
"sest temast tuleb mu pääs" on keelelt imelik ja tähenduselt ähmane, ning tekitab aldis ja bassis segadust, kuna nad peavad ise välja mõtlema, kuidas teksti oma osale kohandada. (Sama aldi-bassi probleem tekib päris lõpus, kus on sama rütmipilt.) Pakun välja:
(b) Vaid Jumalas võib leida rahu mu hing, on temas lu-nastus. Jumalas leiab rahu minu hing, leiab ra-hu hing.
(c) Vaid Jumalas võib leida rahu mu hing, on seal mu lu-nastus. Jumalas leiab rahu minu hing, leiab ra-hu hing.
33 Nunc dimittis (Lk 2,26, 29-30)
(a) Oma sulasel luba minna nüüd sinu teed (sinu teed), oma sõnaga saada teele ta sinu rahus (Jumalas). 
(b) Issand, nüüd sa lased oma sulasel (sulasel), rahus lahkuda oma ütlust mööda (?). 
(c) Lase rahus nüüd minna oma sulasel (Issand),
nagu lubasid on ta näinud oma päästet (Jumalas). 
(d) Oma sulasel lase rahus minna nüüd, Jumal (Jumal), tema silmad on näinud talle lubatud päästet (Jumalas). 
(e) Oma sulasel luba ära minna nüüd, Jumal (Jumal), sinu sõna järele lahkub ta sinu rahus (Jumalas).
(f) Oma sulasel lase minna nüüd, Issand Jumal (Jumal), sinu sõna järele lahkub ta sinu rahus (Jumalas).
(Arutelus selgus, et vähemalt esimene lauseosa peab tingimata lõppema sõnaga “Jumal” nagu originaalis, ja mõlema osa lõpus peavad teised hääled kordama sõna “Jumal” nagu originaalis. Asja komplitseerib see, et eesti keeles on Jumal kahesilbiline, mistõttu tuleb kas rütmi muuta või sõna käändesse panna (Jumalas, Jumalat, Jumalal). Tähendus võiks ka muidugi mõistlik olla.)
35 Bonum est confidere
(a) Issand on me pelgupaik, me lootus ta. Issand on kalju, mil toetuda.
(c) Hea on ikka usaldada Jumalat, hea on mul loota ta peale.
39 Tu sei sorgente viva
(a) Sa oled eluläte, oled tuleleek, armastus. Meid sa Püha Vaim täida. Meid sa Püha Vaim täida.  
(b) Sa oled elu läte, oled tuli ja armastus. Püha Vaim meid täida. Püha Vaim meid täida.
(c) Sa oled eluandja, oled allikas, oled leek. Meid sa Püha Vaim täida. Meid sa Püha Vaim täida.
(d) Sa oled eluandja, eluallikas, eluleek. Meid sa Püha Vaim täida. Meid sa Püha Vaim täida.
40 Surrexit Christus
(a) O--- On Kristus tõusnud, halleluuja! 
O--- Nüüd laulge temale, halleluuja!
(b) ... Nüüd laulge Jumalat, halleluuja!
(c) ... Me kiitust laulame, halleluuja!


44 Adoramus te O Christe
(a) O--- Kummardame sind Kris-tus.
(b) O--- Issand Kristus austame sind. 
47 Per crucem 
(jääb samaks)
49 Surrexit Dominus vere
(jääb samaks)
55 Da pacem cordium (kaanon)
(jääb samaks)
56 Sanctum nomen Domini
(jääb samaks)


"""



PdfMaker().main(body)

