#coding: latin1

# Copyright 2006 Community of Taizé (http://www.taize.fr)

import time

from lino.gendoc.maker import DocMaker
from lino.gendoc.styles import mm, TA_RIGHT

today = time.strftime("%d.%m.%Y")


class Song:
    def __init__(self,number,title1,text1,title2,text2=None,
                 remark=None,source=None):
        self.number=number
        self.title1=title1.decode("latin1")
        self.text1=text1.decode("latin1")
        self.title2=title2.decode("latin1")
        assert type(text2) == type(""), "%r is not a string"%text2
        if text2 is not None: text2=text2.decode("latin1")
        self.text2=text2
        if source is not None: source=source.decode("latin1")
        self.source=source

songs=[]

def song(*args,**kw):
    songs.append(Song(*args,**kw))

def song0(*args,**kw):
    "arutelus"
    pass

def song1(*args,**kw):
    "jääb samaks"
    pass

def header(story):
    story.memo("""
    <table class="EmptyTable">
    <tr><td align="left">
    lk %d
    <td align="right">
    %s
    </table>
    """ % (story.getPageNumber(),today))

def footer(story):
    story.memo(u"""
    <table class="EmptyTable">
    <tr><td align="left">
    Taizé laulud
    <td align="right">
    Eestikeelsed tekstid
    </table>
    """)

FORMAT= 2 
    
def body(story):
##     story.getStyle().update(
##         #showBoundary=True,
##         leftMargin=15*mm,
##         rightMargin=15*mm,
##         topMargin=14*mm,
##         bottomMargin=153*mm, 
##         # 297/2 = 148
##         #footer=footer,
##         header=header,
##         )

##     story.getStyle("P").update(
##         fontSize=16,
##         leading=18,
##         spaceBefore=2)
    
    story.getStyle().update(
        #showBoundary=True,
        leftMargin=10*mm,
        rightMargin=5*mm,
        topMargin=11*mm,
        bottomMargin=(148+9)*mm, # 297/2 = 148
        #footer=footer,
        header=header,
        )

    story.getStyle("P").update(
        fontSize=18,
        leading=20,
        spaceBefore=5)
    
    for s in songs:
        #print s.number
        #story.h1(str(s.number)+" "+s.title2+" ("+s.title1+")")
        #story.table(s.text1,s.text2)

        if FORMAT == 1:
            story.memo(u"""<h1 style="font-weight: bold;">%(number)d. %(title2)s (%(title1)s)</h1>""" 
                     % s.__dict__)
            story.memo(s.text2)

        if FORMAT == 2:
            story.memo("("+str(s.number)+") "+s.text2.strip())
        elif FORMAT == 3:
            s=u"""

            <b>%(number)d. %(title2)s (%(title1)s)</b>

            <table class="EmptyTable">
            <tr>
            <td valign="top">%(text2)s</td>
            <td align="left">%(text1)s</td>
            </table>

            """ % (s.__dict__)

            #print s
            story.memo(s)

                   
        
        
    

song(1,
     "Dans nos obscurités",
     """Dans nos obscurités allume le feu qui ne s'éteint jamais, qui ne s'éteint jamais.""",
     "Me pimeduse sees",
     """Me pimeduse sees sa sära ja süüta kustumatu leek, su kustumatu leek.""",
     )

song(2,
     "Wait for the Lord","""Wait for the Lord, whose day is near.
     Wait for the Lord, keep watch, take heart.
     """,
     "Oota Issandat",
     """Oota Issandat, ta päev on pea,
     oota Issandat ja kindlaks jää.""")

song(3,"Bleibet hier","""Bleibet hier und wachet mit mir,
wachet und betet,
wachet und betet.
""",
     "Siia jää",
     """Siia jää sa minuga koos, valva ja palu, valva ja palu.""")


song(4,"Ubi caritas Deus ibi est","",
     "Kus on halastus, seal on Jumal ka.",
     """Kus on halastus, armastus, kus on halastus, seal on Jumal ka.""")



song(5,"Bless the Lord","""
Bless the Lord, my soul, and bless God's holy name.
Bless the Lord, my soul, who leads me into life.
""",
"Kiida Issandat",
"""Kiida Issandat ja ülista, mu hing. Kiida Issandat, ta ellu juhib mind.""")


song(6,"Gloria ... et in terra pax (canon)","""
""",
"Olgu au (kaanon)",
"""Olgu au, olgu au Jumalale kõrges,
olgu au, olgu au, halleluuja!
Rahu olgu maa peal alati, inimestest he-a meel. """)

song(7,"Notre âme attend",
     "",
     "Sind Issand",
      """
      Sind, Issand, ootab me hing, sa meie südamete rõõm.
      """,remark="""

      (a) Sind, Issand, ootab me hing, sest sinust tuleb meie rõõm.
      
      """)


song(8,"C'est toi ma lampe, Seigneur","""
""",
"Mu valgus, Issand sa",
"""Mu valgus Issand sa, mu teed sa pimeduses näita.
Mu Jumal sa, teed pimeduses näita.
Mu Jumal sa, teed pimeduses näita.
""")

song(9,"Jésus le Christ","""
""",
     "Palume sind",
     """

 Palume sind, oh Kristus me valgus, keela me sees pimedusel kõnelda.
 Palume sind, oh Kristus me valgus, aita armule hing avada.

 """, remark="""

(a) Kristus, me rõõm ja hingede valgus, keela me sees pimedusel kõnelda.
    Kristus, me rõõm ja hingede valgus, täida meid oma armuga sa.

(b) Palume sind, me Kristus, me valgus, tule ja vaigista pimeduse hääl.
    Palume sind, me Kristus, me valgus, aita armule hing avada.

(c) Kristus, tõe vaim, me südame valgus, keela me sees pimedusel kõnelda.
    Kristus, tõe vaim, me südame valgus, täida meid oma armuga sa.

(d) Palume sind, oh Kristus me valgus, vaigista varjude kõne meie sees.
    Palume sind, oh Kristus me valgus, aita meil avada hing armule.

(e) Kristus, mu rõõm, sa valgus mu hinges, vaigista varjude kõne minu sees.
    Kristus, mu rõõm, sa valgus mu hinges, ava mind oma armastusele.

    Palume sind, oh Kristus me valgus, keela me pimedal poolel kõnelda.
    Palume sind, oh Kristus me valgus, aita armule hing avada.

    ärgu olgu see minu pimedus, kes mulle räägib

""")    





song(10,"Laudate Dominum","""
""",
     "Kiitke nüüd Jumalat",
     """Kiitke nüüd Jumalat, kiitke nüüd Jumalat,
     rahvad kõikjal, halleluja!""")


song(11,"Oculi nostri","""
""",
     "Pilgud meil pööratud",
     """Pilgud meil pööratud Jeesuse poole, pilgud meil pööratud Issanda poole.""")

song(12,"De noche","""
""",
     "On öö",
     """On öö me ümber nii pime, kuid loodame vett veel leida,
     janu vaid näitab meil valgust eluvee allika juurde.""")


song1(13,"Veni Creator Spiritus","Veni Creator Spiritus")
     
song(14,"Tui amoris ignem","""
""",
     "Me hinges armutuli",
"""
Tule, Looja Püha Vaim, süüta me hinges armutuli.
Tule, Looja Püha Vaim, tule, Looja Püha Vaim. 
     """)


song(15,"Ubi caritas","""
""",
     "Kus on halastus",
     """Kus on halastus ja armastus,
     kus on halastus, seal on Jumal ka.""")


song(16,"Bénissez le Seigneur","""
""",
     "Laulge kiituselaul",
     """Laulge kiituselaul! Laulge kiituselaul!
     Laulge kiituselaul, laulge nüüd Issandal! """)


song(17,"El Senyor","""
""",
     "Minu Jumal",
     """

     Minu Jumal on minu lootus, minu valgus, mu jõud.
     Kristus on mu karjane
     ja temas rõõmustab hing ja meel,
     ja temas rõõmustab hing ja meel.

     """, remark="""(Ps 28,7)""")


song(18,"Confitemini Domino","""
Confitemini Domino quoniam bonus,
Confitemini Domino, halleluja!
""",
     "Tulge tänage",
     """Tulge tänage Jumalat, tema on hea.
Tulge tänage Jumalat, halleluuja.
     """)

song(19,"Magnificat","""
""",
     "Kiidab mu hing",
     """
     
     1. Kiidab mu hing, kiidab mu hing,
     kiidab mu hing ja süda Issand Jumalat.
     Kiidab mu hing, kiidab mu hing,
     kiidab mu hing ja süda teda.
     
     2. Kiidab mu hing,
     kiidab- mu hing,
     kiidab hing ja süda Jumalat,
     kiidab hing ja süda Ju-malat.
     
     """)

song(20,"Adoramus te Christe","""
""",
     "Kummardame sind Kristus",
     """Kummardame sind Kristus, õnnistame su nime,
su ristisurma läbi lunastatud maailm, 
su ristisurma läbi lunastatud maailm.
""")

song(21,"Christe Salvator","""
""",
     "Jeesus Kristus, Lunastaja",
     """Jee-sus Kristus, Lu-nastaja, anna meile rahu.
     """)

song(22,"Veni Creator Spiritus",
     """
     Veni Creator, veni, Creator, veni Creator Spiritus.
     """,
     "Tule, Looja Püha Vaim",
     """Tule, Looja, tule, Looja, tule, Looja Püha Vaim.""")


song(23,"Laudate omnes gentes","""
""",
     "Oh kiitke nüüd kõik rahvad",
     """Oh kiitke nüüd kõik rahvad, oh kiitke Jumalat.
Oh kiitke nüüd kõik rahvad, oh kiitke Jumalat.
     """)


song(24,"Singt dem Herrn","""
""",
     "Laulge Issandal uus laul",
     """Laulge Issandal uus laul, laulge talle kõik maailm, laulge talle kõik maailm!""")


song(25,"Gloria, gloria (canon)","""
""",
     "Kiitus, au (kaanon)",
     """Kiitus, au, kiitus, au Jumalale kõrges,
kiitus, au, kiitus, au, halleluuja, halleluuja. 
     """)


song(26,"La ténèbre","""
""",
     "Meie pimedus",
     """Meie pimedus pole pime sinu ees, ja öö on sama valge kui päev.""",
     remark="""(Ps 139,11-12)""")


song(27,"Jubilate, Alleluia","""
""",
     "Jumalale hõiska",
     """O--- Jumalale hõiska kogu ilmamaa!
O--- Halleluu-ja, halleluuja! 
     """)

song0(28,"")

song(29,
      "Ostende nobis Domine","""
      """,
      "Ostende nobis (kaanon)","""
      Sa meile Issand osuta
      oma halastust ja armu.
      Aamen! Aamen!
      Maaranata! Maaranata!
      """,remark="""

      Koraali tekst:
      Sa meile Issand, Issand osuta oma halastust ja armu,
      sopran: oma halastust ja armu.
      teised: armu, armu.
      
      (a) Ilmuta meile, Issand, sa oma armu ja heldust.
      Aamen! Aamen! Maranata! Maranata!

      (a) Osuta meile, Is-sand, osuta meile halastust. 

      (b) Sa meile Issand osuta oma halastust ja armu.

      (c) Osuta Issand armulik meil oma rohket halastust.

      (d) Sa meile Issand osuta halastust rohket ja armu. 

      """)


song(30,"In manus tuas, Pater","""
In manus tuas, pater, commendo spiritum meum.
""",
     "Oh Isa, sinu kätte",
     """Oh Isa, sinu kätte ma annan oma vaimu.""")


song(31,"Jubilate Deo (canon)",
     "",
     "Hõiska Jumalale",
     """

     Hõiska Jumalale, hõiska Jumala-le, halleluuja.

     """)


song(32,"Mon âme se repose",
     "",
     "Vaid Jumalas",
     """
     
     Vaid Jumalas võib leida rahu mu hing, sest temast tu-leb pääs.
     Jumalas leiab rahu minu hing, leiab ra-hu hing.

     """,remark="""

     (a) Vaid Jumalas võib leida rahu mu hing, sest temast tuleb mu
     pääs.  Jumalas leiab rahu minu hing, leiab rahu mu hing.

     "sest temast tuleb mu pääs" on keelelt imelik ja tähenduselt
     ähmane, ning tekitab aldis ja bassis segadust, kuna nad peavad
     ise välja mõtlema, kuidas teksti oma osale kohandada. (Sama
     aldi-bassi probleem tekib päris lõpus, kus on sama rütmipilt.)
     Pakun välja:

     (b) Vaid Jumalas võib leida rahu mu hing, on temas lu-nastus.
     Jumalas leiab rahu minu hing, leiab ra-hu hing.

     (c) Vaid Jumalas võib leida rahu mu hing, on seal mu
     lu-nastus. Jumalas leiab rahu minu hing, leiab ra-hu hing.

     """)


song(33,"Nunc dimittis",
      """
      """,
      "Oma sulasel",
      """

      Oma sulasel lase minna nüüd, Issand Jumal (Jumal), sinu sõna
      järele lahkub ta sinu rahus (Jumalas).
      
      """, remark="""

      (Lk 2,26, 29-30)

      (a) Oma sulasel luba minna nüüd sinu teed (sinu teed), oma
      sõnaga saada teele ta sinu rahus (Jumalas).

      (b) Issand, nüüd sa lased oma sulasel (sulasel), rahus lahkuda
      oma ütlust mööda (?).

      (c) Lase rahus nüüd minna oma sulasel (Issand), nagu lubasid on
      ta näinud oma päästet (Jumalas).

      (d) Oma sulasel lase rahus minna nüüd, Jumal (Jumal), tema
      silmad on näinud talle lubatud päästet (Jumalas).

      (e) Oma sulasel luba ära minna nüüd, Jumal (Jumal), sinu sõna
      järele lahkub ta sinu rahus (Jumalas).

      (f) Oma sulasel lase minna nüüd, Issand Jumal (Jumal), sinu sõna
      järele lahkub ta sinu rahus (Jumalas).

      

      (Arutelus selgus, et vähemalt esimene lauseosa peab tingimata
      lõppema sõnaga “Jumal” nagu originaalis, ja mõlema osa lõpus
      peavad teised hääled kordama sõna “Jumal” nagu originaalis. Asja
      komplitseerib see, et eesti keeles on Jumal kahesilbiline,
      mistõttu tuleb kas rütmi muuta või sõna käändesse panna
      (Jumalas, Jumalat, Jumalal). Tähendus võiks ka muidugi mõistlik
      olla.)

      """)




song(34,"Cantate Domino (canon)","""
""",
     "Issandale laula (kaanon)",
     """Issandale laula.
     Halleluuja, halleluuja! Jumalale hõiska. """)

song(35,"Bonum est confidere",
     """
     """,
     "Issand on me pelgupaik",
     """
     
     Issand on me pelgupaik, me loo-tus ta.
     Issand on kal-ju, mil toe-tuda.
     
     """)

song(36,"Spiritus Jesu Christi",
     """
     """,
     "Kristus on arm ja elu",
     """

     Kristus on arm ja elu,
     Kristus on sinu valgus:
     ta kinnitab su südant, ta kinnitab su südant.
     
     """)


song(37,"Jesus, remember me","""
Jesus, remember me when you come into your kingdom.
""",
     "Jeesus, mind meeles pea",
     """Jeesus, mind meeles pea oma kuningriiki tulles.
     """)


song(38,"Psallite Deo",
     """
     """,
     "Hõisake rahvad",
     """O--- Hõisake rahvad Jumalal!
     O--- Halleluuja, halleluuja!
     """)


song(39,"Tu sei sorgente viva",
     """
     """,
     "Sa oled eluandja",
     """

     Sa oled eluandja, eluallikas, eluleek.
     Tule, Püha Vaim, tule.
     Tule, Püha Vaim, tule.

     """,remark="""
     
     (a) Sa oled eluläte, oled tuleleek, armastus. Meid sa Püha Vaim
     täida. Meid sa Püha Vaim täida.
     
     (b) Sa oled elu läte, oled tuli ja armastus. Püha Vaim meid
     täida. Püha Vaim meid täida.
     
     (c) Sa oled eluandja, oled allikas, oled leek. Meid sa Püha Vaim
     täida. Meid sa Püha Vaim täida.

     (d) Sa oled eluandja, eluallikas, eluleek. Meid sa Püha Vaim
     täida. Meid sa Püha Vaim täida.

     """)



song(40,"Surrexit Christus",
     """
     """,
     "On Kristus tõusnud",
     """
     O--- On Kristus tõusnud, halleluuja!
     O--- Nüüd laulgem temale, halleluuja!
     """,remark="""
     
     (a) O--- On Kristus tõusnud, halleluuja! 
     O--- Nüüd laulge temale, halleluuja!
     (b) ... Nüüd laulge Jumalat, halleluuja!
     (c) ... Me kiitust laulame, halleluuja!
     
     """)


song(41,"Magnificat","""
""",
     "Hing rõõmusta",
     """Hing rõõmusta ja ülista mu Jumalat.
O--- Hing rõõmusta. O--- Hing rõõmusta.
     """)


song(42,"Da pacem... in diebus (canon)","""
""",
     "To rahu (kaanon)",
     """

     Too rahu ilmale,
     too rahu Kristus sa
     meie päevadesse.

     """)


song(43,"Veni Lumen (choral)","""
""",
     "Valgusta me südameid (koraal)",
     """

     O--- Tule, Looja Püha Vaim.
     O--- Valgusta me südameid,
     valgusta me südameid.
     """)

song(44,"Adoramus te, o Christe",
     """
     """,
     "Issand Kristus, austame sind",
     """O--- Issand Kristus, austame sind.""",
     remark="""

a) O--- Kummardame sind, Kris-tus.
b) O--- Issand Kristus, austame sind.

Tõstatati “kummardamise” asendamine “austamisega” tähenduse pärast ja
Christe-Domine-vahekord. B) sobib silpide arvult paremini. Paaris
teises laulus me küll tõlkisime adoramus “kummardamiseks”, aga mulle
sobib ka b). Hääletagem. ;-) A või B?
     
     """)


song(45,"Christus resurrexit","""
""",
     "Kristus ülestõusnud",
     """O--- Kristus ülestõusnud, Kristus ülestõusnud.
O--- Halleluuja, halleluuja!
     """)


song(46,"In te confido","""
""",
     "Sind usaldame",
     """O--- Jeesus Kristus. O--- Sind usaldame. """)


song(48,"Crucem tuam","""
""",
     "Kummardame, Issand",
     """Kummardame, Issand, sinu risti ees, kiidame su ülestõusmist, su ülestõusmist me. Me kiidame ja ülistame. Kiidame su ülestõusmist, su ülestõusmist me.""")


song(50,"Nada te turbe","""
""",
     "Ära sa karda",
     """Ära sa karda, ära sa pelga: kellel on Jumal, midagi ei puudu. Ära sa karda, ära sa pelga: Jumalast piisab.""")


song(51,"Dieu ne peut que donner son amour","""
""",
     "Ainus, mis Jumal anda võib sul",
     """
     Ainus, mis Jumal anda võib sul,
     on ta arm ja ta halastus.
     O--- Ta kingib armu.
     O--- Ta annab andeks.""")


song(52,"Veni Sancte Spiritus","""
""",
     "Tule, Looja Püha Vaim",
     """Tule, Looja Püha Vaim.""")


song(53,"Dona la pace","""
""",
     "Anna sa rahu",
     """Anna sa rahu nüüd neile, kes sinusse usuvad.
     Anna, anna sa rahu nüüd neile, anna sa ra-hu.
     """)


song(54,"Toi, tu nous aimes","""
""",
     "Armastad meid sa",
     """Armastad meid sa, eluvee andja.""")


song(57,"Vieni Spirito creatore (canon)","""
""",
     "Tule, Püha Vaim, eluandja (kaanon)",
     """Tule, Püha Vaim, eluandja, tule, tule.""")


song(58,"Misericordias Domini","""
""",
     "On Jumal halastav",
     """On Jumal halastav, armastav, talle ikka laulan ma.""")


song(59,"Venite, exultemus Domino",
     """
     
     Venite, exultemus Domino, venite, adoremus.
     
     """,
     "Kõik tulge, rõõmustage",
     
     """Kõik tulge, rõõmustage Is-sandas, kõik tulge, ülista-ge.
     """)


song(60,"O Christe Domine Jesu",
     """
     O Christe Domine Jesu, O Christe Domine Jesu.
     """,
     "O Issand Jeesus Kristus",
     """O Issand Jee-sus Kristus, O Issand Jee-sus Kristus.
     """)

song(61,"Jubilate coeli (kaanon)",
     """
     Jubilate cœli, jubilate mundi, Christus Jesus surrexit vere.
     
     """,
     "Hõisake kõik taevad (kaanon)",
     """

     Hõisake kõik taevad, hõisake kõik maad,
     Kristus Jeesus ülestõusnud on.
     
     """)

song(62,"Une soif emplit notre âme",
     """
     """,
     "Üks ja ainus soov",
     """

     Üks ja ainus soov mu hinges:
     alistuda sinule, Kristus.
     O--- O--- (Võta kuulda mu häält) Võta kuulda mu häält. O---

     """)


song(63,"Benedictus (kaanon)","""
""",
     "Kiidetud on",
     """

     Kiidetud on kes tuleb,
     kiidetud on kes tuleb,
     me Issanda, me Issanda,
     me Issanda nimel.""")

song0(
    64,"Grande est ta bonté","""
    """,
    "",
    """

    Suurim armastus on ju see, oma elugi anda meie eest. O---
    Jumal sinu heldust kiidame! O---
    
    Suurim armastus on ju see, kui sa ohverdad elu teiste eest. O---
    Jumal sinu heldust kiidame! O---.
    """,
    
      
    source="Jh 15,13")


song(65,"Dona nobis pacem",
     """
     Dona nobis pacem cordium.""",
     "Südamesse anna rahu",
     """Südamesse anna ra-hu
     """)

song(66,"Qui regarde vers Dieu",
     """
     """,
     "Jumal täidab me palged säraga",
     """

     Jumal täidab me palged säraga,
     kaob hingest valu, kurbus ja häbi,
     kaob hingest valu, kurbus ja häbi. 

     """,
      remark="""

      (Ps 34,6: Kes tema poole vaatavad, säravad rõõmust ja nende
      palgeile ei tule kunagi häbi.)

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

     (f) Kui me Jumala poole vaatame, särame rõõmust, täidab meid
     valgus, särame rõõmust, täidab meid valgus.
     
     (g) Kui ma vaatan su poole, säran ma, kaob minu palgelt kurbus ja
     häbi.

     (h) Jumal täidab me palged säraga, kaob hingest kurbus, valu ja
     häbi, kaob hingest kurbus, valu ja häbi.

     (i) Jumal täidab me palged säraga, kaob meie hingest kurbus ja
     häbi, kaob meie hingest kurbus ja häbi.
     
      """)

song(67,"Une soif",
     """
     """,
     "Ainus igatsus",
     """
     
     Ainus igatsus mu hinges: Kristusele ennast kaotada.
     Rahutu ja ootust täis mu süda, kuni sinus puhkab ta.
     
     """, remark="(Ps 63; Mk10,28; Mt 19,27; Mt 11,29)")


song(100,"Lumière de nos coeurs","""
""",
     "Me südamete valgus",
     """

     Me südamete valgus, Issand, igavikutee; me looja ja eluandja,
     meid ühendagu sinu Vaim. Halleluuja!
     Sa armastus ja arm, meid hüüad enda juurde.
     Su hääl lõhestab me öö,
     vastuseks hõiskame me sulle kiitust.
     Halleluuja!
     """)

song(101,"Rendez grâce au Seigneur","""
""",
     "Andke tänu Issandal",
     """Halleluuja, halleluuja, halleluuja.
     <br>1. Andke tänu Issandal, sest ta on hea, igavene tema arm, halleluuja.
     <br>2. Andke tänu ülestõusnud Kristusel, igavene tema arm, halleluuja.
     <br>3. Andke tänu Pühale Vaimule, igavene tema arm, halleluuja. """)



song(121,"In resurrectione tua",
     """
     """,
     "Su ülestõusmises",
     """

     Su ülestõusmises, oh Jeesus Kristus,
     taevas ja maa rõõmustavad.

     """)


song(123,"Bóg jest miloscia","""
""",
     "Jumal on armastus",
     """Jumal on armastus. Elada julge sa armastades. Jumal on armastus. Ära pelga sa.
""")


song(124,"Beati voi poveri",
     """
     """,
     "Nii õndsad, te vaesed",
     """

     Nii õndsad, te vaesed, teie päralt taevariik igavene.

     """)

song(125,"The kingdom of God","""
""",
     "On õiglus ja rahu Jumalariik",
     """On õiglus ja rahu Jumalariik ja rõõm tema Pühas Vaimus.
     Tule ja ava me sees su kuningriigi värav.""")

song(126,"Jesu redemptor","""
""",
     "Jeesus, me kõigi lunastus",
     """Jeesus, me kõigi lunastus, sa valgus ja Isa hiilgus, au olgu sinule, Jeesus, au olgu sinule.""")

song(127,"Nebojte se","""
""",
     "Unusta hirm",
     """Unusta hirm, rõõmusta nüüd! Kristus surnuist ülestõusnud on.""")


song(128,"Eat this bread","""

""",
     "Võtke leib",
     """

     Võtke leib, jagage, sööge ja te ei tunne nälga.
     Võtke vein, jagage, jooge ja te ei tunne janu.

     """)


song(129,"Bleib mit deiner Gnade","""
""",
     "Meie juurde armuga jää",
     """Meie juurde armuga jää, öö saabub pea.
     Sa meie juurde armuga jää, Kristus me valgus. """)


song(131,"Wyslawiajcie Pana","""
""",
     "Hüüdke Issandale",
     """Hüüdke Issandale, O---. Hüüdke Issandale, O---. Laulge talle kogu maailm, halleluuja, halleluuja. """)


song(132,"El alma que anda en amor","""
""",
     "Hing mis on täis armastust",
     """Hing, mis on täis armastust ei väsi ega tüdi. O--- O---""")


song(133,"Bendigo al Señor",
      """
      """,
      "Ma kiidan Issandat",
      """
      
      Ma kiidan Issandat, sest ta kuuleb minu häält,
      oma jõu saan ma temalt, mu südant ta kinnitab.

      """,remark="""

      (a) Ma kiidan Issandat, sest ta kuuleb minu häält, 
      Issand on minu kalju ja teda ma usaldan.
      
      (b) ... Issand jõudu mul annab, mu südant ta kinnitab.
      
      (c) ...oma jõu saan ma temalt, mu südant ta kinnitab.
      
      """)



song(134,"L'ajuda em vindrà","""
""",
     "Kõik abi ma saan Jumalalt",
     """Kõik abi ma saan Jumalalt,
     Jumalalt, kes meie Issand,
     ta teinud taeva ja maa,
     kõik taeva ja maa.""")

song(135,"Christe, lux mundi","""
""",
     "Kristus, me valgus",
     """

     Kristus me valgus, kes järgib sinu teed,
     on temal eluvalgus, eluvalgus.

     """)


song(136,"Esprit consolateur","""
""",
     "Sa Lohutaja Vaim",
     """Sa Lohutaja Vaim, sa armastus ja arm.
     O--- O---
""")


song(137,"Nothing can ever","""
""",
     "Mitte miski ei saa",
     """Mitte miski ei saa meid lahutada Jumalast,
     ta armastust meil ilmutas Jeesus Kristus. O---.""")

song(138,"Kristus, din Ande","""
""",
     "Kristus, su Vaim",
     """Kristus, su Vaim meie sees eluallikas on igavene.""")

song(140,"I am sure I shall see","""
""",
     "Näha loodan ma siin",
     """

     Näha loodan ma siin sel elavate maal meie Jumala headust.
     Ta peale loodan, usus kindlaks jään, ma ootan Issandat!

     """,

     remark="""Ps 27,13-14: Ometi ma usun, et saan näha Issanda
     headust elavate maal. Oota Issandat, ole vahva, ja su süda olgu
     kindel! Oh, oota Issandat!  """)

song(141,"Que j'exulte et jubile",

     """
     """,
     "Sinu heldusest",
     """

     O--- Sinu heldusest rõõmustab mu hing!


     """)

song(142,"Cantate Domino canticum novum","""
""",
     "Nüüd laulge Jumalal",
     """Nüüd laulge Jumalal kiituselaulu. Halleluuja, halleluuja. Nüüd laulge Jumalal kogu maailm. Halleluuja, halleluuja. """)


song(144,"Cantarei ao Senhor",
     """
     """,
     "Kuni elan",
     """

     Kuni elan, mu huulil kiituselaul,
     kuni olen, tal annan tänu ja au.
     Olen rõõmus Jumala juures,
     olen rõõmus Jumala juures.

     """, remark="""

     (a) Tahan Issandat kiita ja hõisata, talle laulda nii kaua kui
     elan ma. Minu hing see rõõmustab temas, minu hing see rõõmustab
     temas.

     (b) Oma südames laulan lakkamata, hinges tänan ja kiidan Issandat
     ma. Temas rõõmustan kuni elan, temas rõõmustan kuni elan.

     (c) Tahan eluaeg kiita Issandat ma, tahan temale laulda ja
     mängida. Minu süda rõõmustab temas, minu süda rõõmustab temas.

     (d) Tahan alati kiita Issandat ma, tahan lõputult laulda ja
     mängida. Jumal on mu südame rõõm, Jumal on mu südame rõõm.
     
     (Ps 104,33-34:
     Ma tahan laulda Issandale oma eluaja / ja mängida
     oma Jumalale, / niikaua kui ma olen elus. / Olgu mu mõlgutus
     armas tema meelest; / mina rõõmutsen Issandas. )

     """,source="Ps 104,33-34")


song(145,"Dominus Spiritus est","""
""",
     "Issand me Jumal on Vaim",
     """Issand me Jumal on Vaim.
     Jumal on Vaim, kes teeb elavaks.
     Jumal on Vaim, kes teeb elavaks. """)

song(146,"Ad te Jesu Christe","""
""",
     "Su poole, oh Jeesus",
     """

     Su poole, oh Jee-sus ma tõstan o-ma hinge.
     Mu Lunasta-ja, su peale loodan.

     """,remark="""
     
     Su poole, oh Jee-sus nüüd oma hinge ma tõstan.
     Me kõigi Pääst-ja, su peale loodan.

     """)

song(147,"Seigneur, tu gardes mon âme",
     """
     """,
     "Oo arm, sa valvad mu hinge",
     """Oo arm, sa valvad mu hinge, oo Jumal, sa tunned mind.
     Juhi minu südant igavesel teel,
     juhi minu südant igavesel teel.""")


song(148,"Frieden, Frieden","""
""",
     "Rahu, rahu",
     """Rahu, rahu, rahu jätan ma teil.
     Oma rahu annan- ma teie südametesse.""",
     remark="""
     
     (Joh 14,27: Rahu ma jätan teile, oma rahu ma annan teile. (...)
     Teie süda ärgu ehmugu ega mingu araks!)

     """)

song(149,"Viešpatie, tu viska žinai",
     """
     """,
     "Issand minust kõike sa tead",
     """

     Issand, minust kõike sa tead. Sina tead, oled mul armas.
     O--- O--- 

     """,
     remark="(Joh 21,17)")

song(150,"Behüte mich Gott",
     """
     """,
     "Jumal hoia mind",
     """

     Ma usaldan sind, Jumal hoia mind
     sel teel, mis viib uude ellu.
     Su juures leian tõelise rõõmu.
     
     """, remark="""

     (a) Oh, varja mind sa, sind ma usaldan,
     Sa kutsud mu teele ellu.
     Su juures rõõm ja täiuslik rahu.

     (b) Mind hoia nüüd sa, sind ma usaldan, sa saadad mu teele
     ellu. Su juures rõõm ja täiuslik rahu.

     """)

song(151,"Sit nomen Domini","""
""",
     "Su nimi Issand",
     """Kiidetud ol-gu su ni-mi- Issand.
     Kiidetud nü-üd ja igavesti.""")

song(152,"Fiez-vous en Lui","""
""",
     "Usaldame sind",
     """Usaldame sind, ei karda me.
     Su rahu hoiab me südameid.
     Usaldame sind. Halleluja, halleluja!""")


"""

Järgmised tõlged on veel arutelus:

28 Toi qui nous aimes (canon)
Sa, kes meid hoiad, armastad ja andeks annad, kiitust sul lauldes paraneb me murtud süda. 
(lauluga 28 on mingi copyrightiga seotud probleem ja paistab, et seda laul ei tohi tõlgida ega trükida... kui sain ise aru, miks see nii on, siis annan teada.)


47 Per crucem 
(jääb samaks)
49 Surrexit Dominus vere
(jääb samaks)
55 Da pacem cordium (kaanon)
(jääb samaks)
56 Sanctum nomen Domini
(jääb samaks)


"""



DocMaker().main(body)

