# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Example usage:

Some fictive Estonians (each couple one male & one female):

>>> for i in range(5):
...    he = (MALE_FIRST_NAMES_ESTONIA.pop(), LAST_NAMES_ESTONIA.pop())
...    she = (FEMALE_FIRST_NAMES_ESTONIA.pop(), LAST_NAMES_ESTONIA.pop())
...    print("%s %s & %s %s" % (he + she))
Aadu Ivanov & Adeele Tamm
Aare Saar & Age Sepp
Aarne Mägi & Age-Kaie Smirnov
Aaro Vasiliev & Aili Petrov
Aaron Kask & Aili Kukk

>>> streets = Cycler(streets_of_tallinn())
>>> print(len(streets))
1523
>>> for i in range(5):
...     print("%s (%s)" % streets.pop())
Aarde tn (Põhja-Tallinn)
Aasa tn (Kesklinn)
Aate tn (Nõmme)
Abaja põik (Pirita)
Abaja tn (Pirita)


Sources:

- Estonian last names were originally extracted from
  `www.ekspress.ee <http://www.ekspress.ee/news/paevauudised/eestiuudised/top-500-eesti-koige-levinumad-perekonnanimed.d?id=27677149>`_
  (I manually added some less frequent names).

- Estonian first names are extracted from my personal database.

- Streets of Tallinn are originally from `www.eki.ee
  <http://www.eki.ee/knab/tallinn1.htm>`_ (Peter Päll confirmed
  permission to use it here on 2014-11-07).

"""

from __future__ import print_function
from __future__ import unicode_literals

from lino.utils import Cycler


def splitter1(s):
    for ln in s.splitlines():
        ln = ln.strip()
        if len(ln) > 1 and ln[0] != '#':
            yield ln


def splitter3(s):
    for ln in s.splitlines():
        ln = ln.strip()
        if len(ln) > 1 and ln[0] != '#':
            a = ln.split()
            name = a[0]
            yield name


STREETS_OF_TALLINN = """
# Tänavanimi                LINNAOSA - Asum (allasum)
# Street name               CITY DISTRICT - Division (subdivision)


Aarde tn                  PÕHJA-TALLINN - Pelgulinn
Aasa tn                   KESKLINN - Uus Maailm
Aate tn                   NÕMME - Nõmme
Abaja põik                PIRITA - Kose (Varsaallika)
Abaja tn                  PIRITA - Kose (Varsaallika)
Abara tn                  HAABERSTI - Vismeistri
Amandus Adamsoni tn       KESKLINN - Kassisaba
Aedvere tn                HAABERSTI - Pikaliiva
Adra tn                   NÕMME - Pääsküla
Aedvilja tn               KESKLINN - Sadama
Aegna puiestee            LASNAMÄE - Priisle
Ahingu tn                 HAABERSTI - Vismeistri
Ahju tn                   KESKLINN - Tatari
Ahtri tn                  KESKLINN - Sadama
Ahvena tn                 HAABERSTI - Kakumäe
Aia tn                    KESKLINN - Vanalinn
Aiandi tn                 MUSTAMÄE - Kadaka
Aianduse tee              PIRITA - Mähe (aedlinn)
Aiatee tn                 PIRITA - Merivälja
Aida tn                   KESKLINN - Vanalinn (all-linn)
Akadeemia tee             MUSTAMÄE - Kadaka, Mustamäe
Alajaama tn               KRISTIINE - Järve
Alasi tn                  PÕHJA-TALLINN - Kopli
Alemaa tn                 HAABERSTI - Pikaliiva
Alevi tn                  KESKLINN - Kitseküla
Algi põik                 KRISTIINE - Lilleküla (Mooni)
Algi tn                   KRISTIINE - Lilleküla (Mooni)
Algi tn                   MUSTAMÄE - Sääse
August Alle tn            KESKLINN - Kadriorg
Allika tn                 KESKLINN - Tatari
Alliksoo põik             NÕMME - Vana-Mustamäe
Alliksoo tn               NÕMME - Vana-Mustamäe
Allveelaeva tn            PÕHJA-TALLINN - Kalamaja
Alvari tn                 LASNAMÄE - Loopealse
Amburi tn                 PÕHJA-TALLINN - Kopli
Andrekse tee              PIRITA - Mähe, Merivälja
Angerja tn                PÕHJA-TALLINN - Karjamaa
Angerpisti tn             LASNAMÄE - Loopealse
Ankru tn                  PÕHJA-TALLINN - Kopli
Anni tn                   LASNAMÄE - Laagna
Ao tn                     KESKLINN - Kassisaba
Apteegi tn                KESKLINN - Vanalinn (all-linn)
Arbu tn                   LASNAMÄE - Laagna
Armatuuri tn              LASNAMÄE - Sõjamäe (Sõstramäe)
Arnika tee                PIRITA - Mähe (aedlinn)
Artelli tn                KRISTIINE - Lilleküla (Marja)
Aru tn                    PÕHJA-TALLINN - Pelgulinn
Arukaskede puiestee       NÕMME - Laagri
Asfaldi tn                LASNAMÄE - Sõjamäe
Astangu tn                HAABERSTI - Astangu
Astla tee                 PIRITA - Mähe (aedlinn)
Astri tn                  NÕMME - Männiku
Asula põik                KESKLINN - Kitseküla
Asula tn                  KESKLINN - Kitseküla
Asunduse tn               LASNAMÄE - Sikupilli
20. Augusti väljak        KESKLINN - Vanalinn (all-linn)
Auli tn                   KRISTIINE - Tondi
Auna tn                   PÕHJA-TALLINN - Pelgulinn
Auru tn                   KESKLINN - Luite

Bensiini tn               KESKLINN - Kadriorg, Sadama
Betooni põik              LASNAMÄE - Sõjamäe (Sõstramäe)
Betooni tn                LASNAMÄE - Sõjamäe (Sõstramäe)
Eduard Bornhöhe tee       PIRITA - Pirita
Bremeni käik              KESKLINN - Vanalinn (all-linn)
Börsi käik                KESKLINN - Vanalinn (all-linn)

Dunkri tn                 KESKLINN - Vanalinn (all-linn)

Edela tn                  NÕMME - Kivimäe, Pääsküla
Edu tn                    NÕMME - Nõmme
Eerikneeme tee            KESKLINN - Aegna
Eevardi tn                HAABERSTI - Tiskre
Eha tn                    KESKLINN - Kassisaba
Ehitajate tee             NÕMME - Nõmme
Ehitajate tee             MUSTAMÄE - Mustamäe
Ehitajate tee             HAABERSTI - Kadaka, Väike-Õismäe, Veskimetsa, Vana-Mustamäe
Ehte tn                   PÕHJA-TALLINN - Pelgulinn
Elektri tn                KRISTIINE - Järve
Elektroni tn              KRISTIINE - Järve
Endla tn                  KESKLINN - Kassisaba, Tõnismäe, Uus Maailm, Lilleküla (Lille), Lilleküla (Linnu), Lilleküla (Mooni)
Endla tn                  KRISTIINE - Kassisaba, Tõnismäe, Uus Maailm, Lilleküla (Lille), Lilleküla (Linnu), Lilleküla (Mooni)
Energia tn                KRISTIINE - Järve
Erika tn                  PÕHJA-TALLINN - Karjamaa
Esku tn                   PIRITA - Lepiku
Estonia puiestee          KESKLINN - Südalinn, Tatari

Friedrich Robert Faehlmanni tn | KESKLINN - Raua, Kadriorg
Falgi tee                 KESKLINN - Vanalinn (Toompea), Vanalinn
Filmi tn                  KESKLINN - Kadriorg
Filtri tee                KESKLINN - Juhkentali, Ülemiste järv
Forelli tn                KRISTIINE - Lilleküla (Marja)

Gaasi tn                  LASNAMÄE - Sõjamäe (Sõstramäe)
Gildi tn                  KESKLINN - Keldrimäe
Nikolai von Glehni põik   NÕMME - Nõmme
Nikolai von Glehni tn     NÕMME - Nõmme, Rahumäe
Gonsiori tn               KESKLINN - Südalinn, Kompassi, Raua, Torupilli, Kadriorg
Graniidi tn               PÕHJA-TALLINN - Kalamaja
Gümnaasiumi tn            KESKLINN - Vanalinn (all-linn)

Haabersti tn              HAABERSTI - Haabersti
Haava tn                  NÕMME - Nõmme, Rahumäe
Haaviku põik              PIRITA - Merivälja
Haaviku tee               PIRITA - Merivälja
Hagudi tn                 KESKLINN - Kitseküla
Haigru tn                 KRISTIINE - Lilleküla (Mooni)
Haldja tn                 NÕMME - Hiiu
Haljas tee                PIRITA - Maarjamäe, Kose
Halla tn                  HAABERSTI - Mustjõe
Hallikivi tn              NÕMME - Kivimäe
Hallivanamehe tn          KESKLINN - Kitseküla
Halu tn                   NÕMME - Raudalu
Hane tn                   KRISTIINE - Lilleküla (Linnu)
Hange tn                  NÕMME - Nõmme
Hansu tn                  HAABERSTI - Tiskre
Hao tn                    NÕMME - Raudalu
Haraka tn                 KRISTIINE - Tondi
Hargi tn                  HAABERSTI - Pikaliiva
Hariduse tn               KESKLINN - Tõnismäe
Harju tn                  KESKLINN - Vanalinn (all-linn), Vanalinn
Harksaba tn               PIRITA - Lepiku
Harku tn                  NÕMME - Nõmme, Hiiu
Harkumetsa tee            HAABERSTI, NÕMME - Astangu, Hiiu, Mäeküla, Vana-Mustamäe
Hauka tn                  KRISTIINE - Lilleküla (Linnu)
Havi tn                   HAABERSTI - Kakumäe
Heina tn                  PÕHJA-TALLINN - Pelgulinn
Heinamaa tn               HAABERSTI - Mustjõe
Heki tee                  PIRITA - Merivälja
Helbe tn                  NÕMME - Nõmme
Helme tn                  PÕHJA-TALLINN - Pelguranna
Helmiku põik              PIRITA - Kose
Helmiku tee               PIRITA - Kose
Herilase tn               MUSTAMÄE - Mustamäe
Karl August Hermanni tn   KESKLINN - Torupilli
Herne tn                  KESKLINN - Veerenni, Juhkentali
Hiidtamme tn              NÕMME - Raudalu
Hiie põik                 PIRITA - Kose (Varsaallika)
Hiie tn                   PIRITA - Kose (Varsaallika)
Hiiela tee                PIRITA - Merivälja
Hiiu tn                   NÕMME - Hiiu
Hiiu-Maleva tn            NÕMME - Hiiu, Nõmme
Hiiumetsa tee             NÕMME - Hiiu
Hiiu-Suurtüki tn          NÕMME - Hiiu
Hipodroomi tn             PÕHJA-TALLINN - Pelgulinn
Hirve põik                NÕMME - Pääsküla
Hirve tn                  NÕMME - Pääsküla
Hobujaama tn              KESKLINN - Sadama
Hoburaua tn               HAABERSTI - Tiskre
Hobusepea tn              KESKLINN - Vanalinn (all-linn)
Hommiku tn                NÕMME - Kivimäe, Pääsküla
Hoo tn                    NÕMME - Vana-Mustamäe
Hooldekodu tee            LASNAMÄE - Priisle
Hospidali tn              KESKLINN - Veerenni
Humala tn                 HAABERSTI - Mustjõe
Hundipea tn               PÕHJA-TALLINN - Karjamaa (Hundipea)
Hunditubaka tee           PIRITA - Kose
Hõbeda tn                 KESKLINN - Raua
Hõbekuuse tee             PIRITA - Merivälja
Hõberebase tn             NÕMME - Raudalu
Hõimu tn                  NÕMME - Kivimäe
Hälli põik                HAABERSTI - Õismäe
Hälli tn                  HAABERSTI - Õismäe
Hämar tee                 PIRITA - Mähe
Hämariku tn               NÕMME - Nõmme
Härgmäe tn                HAABERSTI - Mäeküla
Härjapea tn               PÕHJA-TALLINN - Pelgulinn
Miina Härma tn            LASNAMÄE - Laagna
Härmatise tn              HAABERSTI - Mustjõe
Hüübi tn                  KRISTIINE - Lilleküla (Linnu)

Ida tee                   PIRITA - Merivälja
Idakaare põik             NÕMME - Nõmme
Idakaare tn               NÕMME - Nõmme
Ilmarise tn               NÕMME - Kivimäe, Hiiu
Ilo tn                    NÕMME - Rahumäe
Ilvese tn                 NÕMME - Pääsküla
Imanta tn                 KESKLINN - Keldrimäe
Inseneri tn               KESKLINN - Vanalinn
Invaliidi tn              KESKLINN - Veerenni
Irusilla tn               PIRITA - Iru
Islandi väljak            KESKLINN - Südalinn
Iva tn                    MUSTAMÄE - Kadaka

Jaagu tn                  HAABERSTI - Tiskre
Jaama tn                  NÕMME - Nõmme
Jaaniku tn                PIRITA - Kose (Varsaallika)
Jaanilille tee            PIRITA - Kose
Jahe tee                  PIRITA - Mähe
Jahimehe põik             PIRITA - Pirita
Jahimehe tee              PIRITA - Pirita
Jahu tn                   PÕHJA-TALLINN - Kalamaja
Jakobi tn                 KESKLINN - Keldrimäe
Carl Robert Jakobsoni tn  KESKLINN - Torupilli
Jalaka tn                 NÕMME - Männiku
Jalami tn                 HAABERSTI - Astangu
Johann Voldemar Jannseni tn | NÕMME - Kivimäe
Jasmiini tee              PIRITA - Mähe (aedlinn)
Joa tn                    KESKLINN - Kadriorg
Joone tn                  HAABERSTI - Mustjõe
Jugapuu põik              PIRITA - Merivälja
Jugapuu tee               PIRITA - Merivälja
Juhkentali tn             KESKLINN - Veerenni, Keldrimäe, Juhkentali
Juhtme tn                 KESKLINN - Mõigu
Jumika tee                PIRITA - Mähe
Juurdeveo tn              KESKLINN - Kitseküla
Jõe tn                    KESKLINN - Sadama
Jõekalda tn               PIRITA - Kose (Lükati)
Jõeküla tee               HAABERSTI - Kakumäe, Vismeistri
Jõeoti tn                 HAABERSTI - Vismeistri
Jõhvika tn                NÕMME - Männiku
Järve tn                  KRISTIINE - Järve
Järvekalda tee            HAABERSTI - Väike-Õismäe
Järveotsa tee             HAABERSTI - Väike-Õismäe
Järvevana tee             KESKLINN - Kitseküla, Luite, Juhkentali, Ülemiste järv
Jääraku põik              PIRITA - Kose
Jääraku tee               PIRITA - Kose

Kaabli tn                 KESKLINN - Mõigu
Kaare tn                  NÕMME - Nõmme
Kaarla tn                 NÕMME - Raudalu
Kaarlepere tn             HAABERSTI - Tiskre
Kaarli puiestee           KESKLINN - Tõnismäe, Vanalinn
Kaarna tn                 KRISTIINE - Lilleküla (Mooni)
Kaaruti tn                HAABERSTI - Pikaliiva
Kaasiku tn                NÕMME - Pääsküla
Kabli tn                  HAABERSTI - Pikaliiva
Kadaka puiestee           NÕMME, MUSTAMÄE - Pääsküla, Vana-Mustamäe, Hiiu, Kadaka
Kadaka tee                KRISTIINE, MUSTAMÄE - Lilleküla (Marja), Kadaka, Mustamäe
Kadri tee                 KESKLINN - Kadriorg
Kaera tn                  PÕHJA-TALLINN - Pelgulinn
Kaeravälja tn             HAABERSTI - Haabersti
Kaevu tn                  NÕMME - Rahumäe
Kaevuri tn                PÕHJA-TALLINN - Kopli
Kagu tn                   NÕMME - Männiku, Liiva, Rahumäe
Kaheküla tee              HAABERSTI - Vismeistri, Kakumäe
Kahlu tn                  HAABERSTI - Pikaliiva
Kahu tn                   LASNAMÄE - Laagna
Kahva tn                  HAABERSTI - Kakumäe
Kai tn                    KESKLINN - Sadama
Kailu tee                 PIRITA - Mähe
Kaisla tn                 HAABERSTI - Tiskre
Kaitse tn                 NÕMME - Liiva
Kaja tn                   NÕMME - Nõmme
Kajaka tn                 KRISTIINE - Tondi, Lilleküla (Linnu)
Kakumäe tee               HAABERSTI - Kakumäe, Vismeistri
Kaladi tn                 HAABERSTI - Vismeistri
Kalamehe tee              PIRITA - Pirita
Kalaranna tn              PÕHJA-TALLINN - Kalamaja
Kalasadama tn             PÕHJA-TALLINN - Kalamaja
Kalavälja tee             KESKLINN - Aegna
Kalda tn                  NÕMME - Pääsküla
Kalevala tn               NÕMME - Kivimäe
Kalevi tn                 PÕHJA-TALLINN - Kalamaja
Kalevipoja põik           LASNAMÄE - Laagna
Kalevipoja tn             LASNAMÄE - Laagna
Kaljase tn                KESKLINN - Sadama
Kalju tn                  PÕHJA-TALLINN - Kalamaja
Kallaste tn               PIRITA - Kose (Kose-Kallaste)
Kalmistu tee              NÕMME - Liiva
Kalmuse tee               PIRITA - Pirita
Kaluri tn                 PÕHJA-TALLINN - Kopli
Kammelja tn               HAABERSTI - Kakumäe
Kampri tn                 KRISTIINE - Tondi
Kanali tee                KESKLINN, LASNAMÄE - Mõigu, Sõjamäe
Kanarbiku tn              NÕMME - Pääsküla
Kandle tn                 NÕMME - Kivimäe
Kanepi tn                 PÕHJA-TALLINN - Sitsi
Kangru tn                 PÕHJA-TALLINN - Pelguranna
Kannikese tn              KRISTIINE - Lilleküla (Lille)
Kannustiiva tn            PIRITA - Lepiku
Kantsi tn                 LASNAMÄE - Ülemiste
Kanuti tn                 KESKLINN - Vanalinn
Artur Kapi tn             KESKLINN - Kassisaba
Johannes Kappeli tn       KESKLINN - Torupilli
Karamelli tn              KESKLINN - Kitseküla
Kari tn                   PÕHJA-TALLINN - Pelguranna
Karjamaa tn               PÕHJA-TALLINN - Karjamaa
Karnapi tee               KESKLINN - Aegna
Karsti tn                 MUSTAMÄE - Kadaka
Karu tn                   KESKLINN - Sadama
Karukella tee             PIRITA - Kose
Karusambla tn             NÕMME - Pääsküla
Karuse tn                 NÕMME - Raudalu
Karusmarja tn             NÕMME - Männiku
Kase tn                   PIRITA - Maarjamäe, Kose (Varsaallika)
Kassi tn                  MUSTAMÄE - Kadaka
Kassikäpa tee             PIRITA - Laiaküla
Kaskede puiestee          NÕMME - Laagri
Kastani tn                NÕMME - Pääsküla
Kaste tn                  NÕMME - Vana-Mustamäe
Kasteheina tn             NÕMME - Pääsküla
Kastevarre tee            PIRITA - Mähe
Kastiku tee               PIRITA - Mähe
Kasvu tn                  KRISTIINE - Lilleküla (Lille)
Katariina käik            KESKLINN - Vanalinn (all-linn)
Katleri tn                LASNAMÄE - Katleri
Katusepapi tn             LASNAMÄE - Sikupilli
Kauba tn                  KESKLINN - Kitseküla
Kaubamaja tn              KESKLINN - Südalinn
Kauge tn                  NÕMME - Männiku
Kauka tn                  KESKLINN - Sibulaküla
Kauna tn                  KESKLINN - Veerenni
Kaunis tn                 PIRITA - Kose (Varsaallika)
Kaupmehe tn               KESKLINN - Sibulaküla
Kauri tn                  KRISTIINE - Lilleküla (Linnu)
Keava tn                  KESKLINN - Kitseküla
Kedriku tn                PIRITA - Lepiku
Keemia tn                 KRISTIINE - Lilleküla (Mooni)
Keeru tee                 PIRITA - Mähe
Keevise tn                LASNAMÄE - Ülemiste
Keldrimäe tn              KESKLINN - Keldrimäe
Kelluka tee               PIRITA - Kose
Kentmanni põik            KESKLINN - Tatari
Kentmanni tn              KESKLINN - Tatari, Sibulaküla, Südalinn
Paul Kerese tn            NÕMME - Nõmme, Männiku
Kesk-Ameerika tn          KESKLINN - Uus Maailm
Kesk-Kalamaja tn          PÕHJA-TALLINN - Kalamaja
Keskküla tn               HAABERSTI - Pikaliiva
Kesk-Luha tn              KESKLINN - Uus Maailm
Kesk-Sõjamäe tn           LASNAMÄE - Ülemiste, Sõjamäe
Kesktee                   PIRITA - Merivälja, Mähe
Keskuse tn                MUSTAMÄE - Mustamäe
Kessi tn                  HAABERSTI - Kakumäe
Ketraja tn                PÕHJA-TALLINN - Pelguranna
Ketta tn                  PÕHJA-TALLINN - Kopli
Kevade tn                 KESKLINN - Kassisaba
Kibuvitsa tn              KRISTIINE - Lilleküla (Lille)
Kihnu tn                  LASNAMÄE - Kuristiku
Kiige tn                  NÕMME - Nõmme
Kiikri tn                 KESKLINN - Kadriorg
Kiili tn                  MUSTAMÄE - Sääse
Kiini tn                  HAABERSTI - Vismeistri
Kiire tn                  KESKLINN - Uus Maailm
Kiisa tn                  KESKLINN - Kitseküla
Kiive tn                  LASNAMÄE - Ülemiste
Kilbi tn                  PÕHJA-TALLINN - Kopli
Kilde tn                  HAABERSTI - Pikaliiva
Killustiku tn             LASNAMÄE - Sikupilli
Kilu tn                   HAABERSTI - Kakumäe
Kinga tn                  KESKLINN - Vanalinn (all-linn)
Kirde tn                  NÕMME - Rahumäe
Kiriku plats              KESKLINN - Vanalinn (Toompea)
Kiriku põik               KESKLINN - Vanalinn (Toompea)
Kiriku tn                 KESKLINN - Vanalinn (Toompea)
Kirilase tn               PIRITA - Lepiku
Kirsi tn                  KRISTIINE - Lilleküla (Mooni)
Kitsas tn                 NÕMME - Rahumäe
Kitseküla tn              KESKLINN, KRISTIINE - Kitseküla, Tondi
August Kitzbergi tn       NÕMME - Hiiu
Kiuru tn                  KRISTIINE - Lilleküla (Linnu)
Kivi tn                   NÕMME - Rahumäe
Kiviaia tee               PIRITA - Kloostrimetsa, Laiaküla, Iru
Kivila tn                 LASNAMÄE - Mustakivi, Tondiraba
Kivimurru tn              LASNAMÄE - Sikupilli
Kivimäe tn                NÕMME - Kivimäe
Kiviranna tee             HAABERSTI - Kakumäe
Kiviriku tn               LASNAMÄE - Loopealse
Kivisilla tn              KESKLINN - Maakri, Kompassi
Klaasi tn                 PÕHJA-TALLINN - Kopli
Kloostri tee              PIRITA - Pirita
Kloostrimetsa tee         PIRITA - Pirita, Kloostrimetsa, Lepiku, Laiaküla
Kodu tn                   KESKLINN - Veerenni
Koge tn                   KESKLINN - Sadama
Kohila tn                 KESKLINN - Kitseküla
Kohtu tn                  KESKLINN - Vanalinn (Toompea)
Koidiku tn                NÕMME - Kivimäe
Koidu tn                  KESKLINN - Kassisaba, Uus Maailm
Lydia Koidula tn          KESKLINN - Kadriorg
Kolde puiestee            PÕHJA-TALLINN - Pelgulinn, Merimetsa, Pelguranna
Koldrohu tee              PIRITA - Kose
Kollane tn                KESKLINN - Raua
Komandandi tee            KESKLINN - Vanalinn (Toompea), Vanalinn
Komeedi tn                KESKLINN - Uus Maailm
Koogu tn                  HAABERSTI - Pikaliiva
Kooli tn                  KESKLINN - Vanalinn (all-linn)
Jaan Koorti tn            LASNAMÄE - Laagna
Kopli tn                  PÕHJA-TALLINN - Kalamaja, Karjamaa, Sitsi, Paljassaare, Pelguranna, Kopli
Kopliranna tn             PÕHJA-TALLINN - Kopli
Korese tn                 HAABERSTI - Vismeistri
Korgi tn                  KESKLINN - Mõigu
Kose põik                 PIRITA - Kose (Lükati)
Kose tee                  PIRITA - Maarjamäe, Kose (Varsaallika), Kose, Kose (Kallaste)
Kosemetsa tn              PIRITA - Kose (Lükati)
Koskla tn                 KRISTIINE - Lilleküla (Linnu), Lilleküla (Mooni)
Kotermaa tn               HAABERSTI - Astangu
Kotka tn                  KRISTIINE - Tondi, Lilleküla (Linnu)
Kotkapoja tn              KRISTIINE - Lilleküla (Linnu)
Kotlepi tn                HAABERSTI - Tiskre
Kotzebue tn               PÕHJA-TALLINN - Kalamaja
Kraavi tn                 NÕMME - Männiku
Kreegi tn                 NÕMME - Männiku, Nõmme
Kressi tee                PIRITA - Mähe (aedlinn)
Friedrich Reinhold Kreutzwaldi tn | KESKLINN - Raua, Torupilli, Keldrimäe
Kriibi tn                 PIRITA - Lepiku
Kriidi tn                 LASNAMÄE - Sõjamäe
Kristeni tn               HAABERSTI - Tiskre
Kristiina tn              KESKLINN - Uus Maailm
Kruusa tn                 NÕMME - Kivimäe
Kruusaranna tee           HAABERSTI - Kakumäe
Kubu tn                   HAABERSTI - Pikaliiva
Kudu tn                   HAABERSTI - Kakumäe
Kuhja tn                  HAABERSTI - Pikaliiva
Friedrich Kuhlbarsi tn    KESKLINN - Torupilli
Kuiv tn                   NÕMME - Nõmme
Kuke tn                   KESKLINN - Maakri
Kuklase tn                MUSTAMÄE - Sääse
Kuldnoka tn               KRISTIINE - Lilleküla (Mooni)
Kuldtiiva tn              PIRITA - Lepiku
Kuljuse tn                NÕMME - Nõmme
Kullassepa tn             KESKLINN - Vanalinn (all-linn)
Kullerkupu tn             KRISTIINE - Lilleküla (Lille)
Kullese tn                PIRITA - Kose (Varsaallika)
Kulli tn                  KRISTIINE - Lilleküla (Linnu)
Kumalase tn               NÕMME - Pääsküla
Kume tn                   NÕMME - Raudalu
Kummeli tee               PIRITA - Mähe (aedlinn)
Juhan Kunderi põik        KESKLINN - Torupilli
Juhan Kunderi tn          KESKLINN - Torupilli
Kungla tn                 PÕHJA-TALLINN - Kalamaja
Kuninga tn                KESKLINN - Vanalinn (all-linn)
Kupra tee                 PIRITA - Mähe (aedlinn), Lepiku
Kura tn                   NÕMME - Raudalu
Kure tn                   KRISTIINE - Lilleküla (Mooni)
Kuremarja tn              NÕMME - Männiku
Kurepõllu tn              LASNAMÄE - Kurepõllu
Kurereha tee              PIRITA - Kose
Kurikneeme tee            KESKLINN - Aegna
Kuristiku tn              KESKLINN - Kadriorg
Kurmu tn                  HAABERSTI - Pikaliiva
Kurni põik                NÕMME - Rahumäe
Kurni tn                  NÕMME - Rahumäe
Kuru tn                   NÕMME - Nõmme
Kuslapuu tn               PIRITA - Maarjamäe
Kuukressi tee             PIRITA - Kose
Kuuli tn                  LASNAMÄE - Tondiraba, Sõjamäe, Sõjamäe (Sõstramäe)
Kuunari tn                KESKLINN - Sadama
Kuuse tn                  NÕMME - Nõmme
Kuusenõmme tee            PIRITA - Mähe
Kuusiku tee               PIRITA - Mähe
Kvartsi tn                NÕMME - Männiku
Kõdra tee                 PIRITA - Mähe (aedlinn)
Kõivu põik                PIRITA - Merivälja
Kõivu tee                 PIRITA - Merivälja
Kõla tn                   NÕMME - Kivimäe
Kõlviku põik              PIRITA - Lepiku
Kõlviku tee               PIRITA - Lepiku
Kõnnu tn                  NÕMME - Raudalu
Kõrge tn                  NÕMME - Rahumäe
Kõrgepinge tn             HAABERSTI - Mustjõe
Kõrkja tee                PIRITA - Pirita
Kõrre tn                  PÕHJA-TALLINN - Pelgulinn
Kõue tn                   NÕMME - Nõmme
Kõver tn                  NÕMME - Nõmme
Käba tn                   HAABERSTI - Vismeistri
Käbi tn                   NÕMME - Liiva
Käbliku tn                KRISTIINE - Lilleküla (Linnu)
Käia tn                   HAABERSTI - Pikaliiva
Kännu tn                  KRISTIINE - Lilleküla (Linnu)
Käo põik                  KRISTIINE - Lilleküla (Linnu)
Käo tn                    KRISTIINE - Tondi, Lilleküla (Linnu)
Käokannu tee              PIRITA - Mähe (aedlinn)
Käokeele tee              PIRITA - Mähe
Käokäpa tee               PIRITA - Mähe (aedlinn)
Käolina tn                NÕMME - Pääsküla
Kristjan Kärberi tn       LASNAMÄE - Seli, Mustakivi
Kärbi tn                  NÕMME - Pääsküla
Kärestiku tn              PIRITA - Kose (Lükati)
Kärje tn                  NÕMME - Hiiu
Kärneri tn                HAABERSTI - Haabersti
Käru tn                   KESKLINN - Kitseküla
Kätki tn                  HAABERSTI - Õismäe
Käänu tn                  HAABERSTI - Tiskre
Köie tn                   PÕHJA-TALLINN - Kalamaja
Johann Köleri tn          KESKLINN - Kadriorg
Köömne tn                 HAABERSTI - Mustjõe
Külaniidu tee             KESKLINN - Aegna
Külma tn                  HAABERSTI - Mustjõe
Külmallika põik           NÕMME - Vana-Mustamäe
Külmallika tn             NÕMME - Vana-Mustamäe
Külvi tn                  NÕMME - Pääsküla (Vana-Pääsküla)
Künka tn                  NÕMME - Rahumäe, Nõmme
Künkamaa tn               HAABERSTI - Tiskre
Künnapuu tn               PIRITA - Maarjamäe
Künni tn                  NÕMME - Kivimäe
Küti tn                   PÕHJA-TALLINN - Kalamaja
Küüvitsa tee              PIRITA - Mähe

Laagna tee                LASNAMÄE - Sikupilli, Uuslinn, Pae, Kurepõllu, Laagna, Tondiraba, Mustakivi, Seli
Laane tn                  NÕMME - Kivimäe
Laaniku tn                NÕMME - Pääsküla
Laboratooriumi tn         KESKLINN - Vanalinn (all-linn)
Laeva tn                  KESKLINN - Sadama
Laevastiku tn             PÕHJA-TALLINN - Paljassaare
Lagedi tee                LASNAMÄE - Väo
Lageloo tn                LASNAMÄE - Loopealse
Lagle puiestee            KRISTIINE - Lilleküla (Linnu)
Lahe tn                   KESKLINN - Kadriorg
Lai tn                    KESKLINN - Vanalinn (all-linn)
Laiaküla tee              PIRITA - Laiaküla
Ants Laikmaa tn           KESKLINN - Südalinn, Kompassi
Laine tn                  KRISTIINE - Järve
Laki tn                   KRISTIINE, MUSTAMÄE, HAABERSTI - Lilleküla (Marja), Mustjõe, Kadaka
Lambi tn                  KESKLINN - Mõigu
Landi tn                  HAABERSTI - Kakumäe
Laose tn                  HAABERSTI - Kakumäe
Lasnamäe tn               LASNAMÄE - Sikupilli
Laste tn                  NÕMME - Hiiu
Lastekodu tn              KESKLINN - Keldrimäe, Juhkentali
Latika tn                 HAABERSTI - Kakumäe
Lauka tn                  NÕMME - Vana-Mustamäe
Lauliku tn                NÕMME - Pääsküla, Kivimäe
Laulu tn                  NÕMME - Kivimäe
Laulupeo tn               KESKLINN - Torupilli
Lauri tee                 PIRITA - Mähe, Merivälja
Lauripere tn              HAABERSTI - Vismeistri
Ants Lauteri tn           KESKLINN - Sibulaküla, Maakri
Lavamaa tn                LASNAMÄE - Loopealse, Paevälja
Lee tn                    HAABERSTI - Õismäe
Leediku tn                PIRITA - Lepiku
Leedri tee                PIRITA - Merivälja, Mähe
Leegi tn                  NÕMME - Pääsküla, Kivimäe
Leesika tn                NÕMME - Liiva
Leete tn                  KESKLINN - Luite
Leevikese tn              KRISTIINE - Lilleküla (Linnu)
Lehe tn                   KRISTIINE - Lilleküla (Linnu)
Lehiku tee                PIRITA - Mähe, Merivälja
Lehise tn                 PIRITA - Maarjamäe
Lehiste puiestee          NÕMME - Laagri
Lehola tn                 NÕMME - Hiiu
Lehtmäe tn                HAABERSTI - Kakumäe
Lehtpuu tn                NÕMME - Pääsküla
Lehtri tn                 MUSTAMÄE - Kadaka
Leigeri tn                PÕHJA-TALLINN - Kalamaja
Leina tn                  NÕMME - Hiiu
Lelle tn                  KESKLINN - Kitseküla
Lembitu tn                KESKLINN - Sibulaküla
Lemle tn                  HAABERSTI - Vismeistri
Lemmiku põik              NÕMME - Pääsküla
Lemmiku tn                NÕMME - Pääsküla
Lennujaama tee            LASNAMÄE - Ülemiste
Lennuki tn                KESKLINN - Maakri
Lennusadama tn            PÕHJA-TALLINN - Kalamaja
Lepa põik                 PIRITA, KESKLINN - Maarjamäe, Kadriorg
Lepa tn                   PIRITA, KESKLINN - Maarjamäe, Kadriorg
Lepatriinu tn             MUSTAMÄE - Mustamäe
Lepiku tee                PIRITA - Lepiku
Lesta tn                  HAABERSTI - Kakumäe
Liblika tn                KRISTIINE - Lilleküla (Linnu)
Liikuri tn                LASNAMÄE - Kurepõllu, Laagna, Paevälja, Loopealse
Liilia tee                PIRITA - Mähe (aedlinn)
Liimi tn                  KRISTIINE - Lilleküla (Marja)
1. liin                   PÕHJA-TALLINN - Kopli
2. liin                   PÕHJA-TALLINN - Kopli
3. liin                   PÕHJA-TALLINN - Kopli
4. liin                   PÕHJA-TALLINN - Kopli
5. liin                   PÕHJA-TALLINN - Kopli
Liinivahe tn              PÕHJA-TALLINN - Kopli
Liipri tn                 NÕMME - Pääsküla
Liiva tn                  NÕMME - Nõmme, Rahumäe
Liivalaia tn              KESKLINN - Tatari, Veerenni, Sibulaküla, Keldrimäe, Maakri
Liivaluite tn             NÕMME - Liiva
Liivametsa tn             NÕMME - Liiva
Liivamäe tn               KESKLINN - Keldrimäe
Liivaoja tn               KESKLINN - Kadriorg
Liivaranna tee            HAABERSTI - Kakumäe
Liiviku tn                NÕMME - Kivimäe
Lille tn                  KRISTIINE - Lilleküla (Lille)
Lilleherne tee            PIRITA - Mähe (aedlinn)
Lillevälja tn             HAABERSTI - Haabersti
Lina tn                   PÕHJA-TALLINN - Sitsi
Linda tn                  PÕHJA-TALLINN - Kalamaja
Lindakivi puiestee        LASNAMÄE - Laagna
Linnamäe tee              LASNAMÄE - Kuristiku, Priisle
Linnu tee                 KRISTIINE - Tondi, Lilleküla (Linnu), Lilleküla (Mooni)
Linnuse tee               LASNAMÄE - Priisle
Lobjaka tn                HAABERSTI - Mustjõe
Lodjapuu tee              PIRITA - Merivälja
Lodumetsa tee             PIRITA - Mähe
Logi tn                   KESKLINN - Sadama
Lohu tn                   NÕMME - Vana-Mustamäe
Loigu tn                  HAABERSTI - Kakumäe
Loite tn                  KESKLINN - Kassisaba
Loitsu tn                 LASNAMÄE - Laagna
Loo tn                    KRISTIINE - Lilleküla (Lille)
Loode põik                KESKLINN - Kassisaba
Loode tn                  KESKLINN - Kassisaba
Looga tn                  HAABERSTI - Mustjõe
Looklev tee               PIRITA - Mähe
Loometsa tn               LASNAMÄE - Loopealse
Loomuse tn                HAABERSTI - Kakumäe
Loopealse puiestee        LASNAMÄE - Loopealse
Lootsi tn                 KESKLINN - Sadama
Lootuse puiestee          NÕMME - Hiiu, Nõmme, Männiku, Rahumäe
Lootuse põik              NÕMME - Nõmme
Lossi plats               KESKLINN - Vanalinn (Toompea)
Lossi tn                  NÕMME, MUSTAMÄE - Vana-Mustamäe, Kadaka
Lubja tn                  KESKLINN - Torupilli
Luha tn                   KESKLINN - Uus Maailm
Luige tn                  KRISTIINE - Lilleküla (Linnu)
Luise tn                  KESKLINN - Kassisaba
Luisu tn                  HAABERSTI - Pikaliiva
Luite tn                  KESKLINN - Luite
Luku tn                   KESKLINN - Veerenni
Lume tn                   PÕHJA-TALLINN - Karjamaa (Hundipea)
Lumikellukese tee         PIRITA - Mähe (aedlinn)
Lumiku tn                 PIRITA - Lepiku
Lummu tn                  LASNAMÄE - Laagna
Luste tn                  PÕHJA-TALLINN - Pelgulinn
Lõhe tn                   HAABERSTI - Kakumäe
Lõhmuse põik              PIRITA - Merivälja
Lõhmuse tee               PIRITA - Merivälja
Lõikuse tn                NÕMME - Pääsküla (Vana-Pääsküla)
Lõime tn                  PÕHJA-TALLINN - Pelguranna, Sitsi
Lõimise tn                HAABERSTI - Vismeistri
Lõkke tn                  KESKLINN - Tõnismäe, Uus Maailm
Lõo tn                    NÕMME - Pääsküla
Lõokese tn                KRISTIINE - Tondi
Lõosilma tee              PIRITA - Kose
Lõuka tn                  HAABERSTI - Õismäe, Haabersti
Lõuna tn                  NÕMME - Nõmme
Lõvi tn                   NÕMME - Hiiu
Lõõtsa tn                 LASNAMÄE - Ülemiste
Läike tn                  NÕMME - Pääsküla
Lätte tn                  KESKLINN - Tatari
Lääne tee                 PIRITA - Merivälja
Läänekaare tn             NÕMME - Hiiu
Läänemere tee             LASNAMÄE - Kuristiku, Priisle
Lühike jalg               KESKLINN - Vanalinn (all-linn)
Lühike tn                 NÕMME - Hiiu, Nõmme
Lükati tee                PIRITA - Kose (Lükati), Kloostrimetsa
Lüli tn                   KESKLINN - Mõigu
Lüüsi tn                  KESKLINN - Sadama

Maakri tn                 KESKLINN - Maakri, Kompassi
Maarjaheina tn            KESKLINN - Kadriorg
Maarjamäe tn              KESKLINN - Kadriorg
Maasika tn                KRISTIINE - Lilleküla (Lille)
Madala tn                 PÕHJA-TALLINN - Pelguranna
Madalmaa tn               KESKLINN - Sadama
Madara tn                 KRISTIINE - Lilleküla (Lille)
Magasini tn               KESKLINN - Veerenni
Magdaleena tn             KESKLINN - Kitseküla
Mahla tn                  NÕMME - Liiva, Männiku
Mahtra tn                 LASNAMÄE - Mustakivi
Mai põik                  NÕMME - Nõmme
Mai tn                    NÕMME - Nõmme
Maikellukese tee          PIRITA - Mähe (aedlinn)
Mailase tee               PIRITA - Kose
Maimu tn                  HAABERSTI - Vismeistri
Maisi tn                  PÕHJA-TALLINN - Pelgulinn
Majaka põik               LASNAMÄE - Sikupilli
Majaka tn                 LASNAMÄE - Sikupilli
Maleva põik               PÕHJA-TALLINN - Kopli
Maleva tn                 PÕHJA-TALLINN - Kopli
Malmi tn                  PÕHJA-TALLINN - Kalamaja
Maneeži tn                KESKLINN - Kompassi
Manufaktuuri tn           PÕHJA-TALLINN - Sitsi
Marana tn                 LASNAMÄE - Loopealse
Marati tn                 PÕHJA-TALLINN - Kopli
Mardi tn                  KESKLINN - Keldrimäe
Mardipere tn              HAABERSTI - Vismeistri
Marja tn                  KRISTIINE - Lilleküla (Marja), Mustjõe
Marjamaa tn               HAABERSTI - Mustjõe
Marsi tn                  KRISTIINE - Tondi
Marta tn                  KESKLINN - Kitseküla
Martsa tn                 LASNAMÄE - Katleri
Masina tn                 KESKLINN - Juhkentali
Masti tn                  PIRITA - Pirita
Matka tee                 PIRITA - Mähe
Meeliku tn                LASNAMÄE - Loopealse
Meeruse tn                PÕHJA-TALLINN - Kopli
Mehaanika põik            KRISTIINE - Lilleküla (Mooni)
Mehaanika tn              KRISTIINE - Lilleküla (Mooni)
Meika tn                  KRISTIINE - Lilleküla (Linnu)
Meistri tn                HAABERSTI - Veskimetsa
Meleka tn                 KRISTIINE - Lilleküla (Mooni)
Mere puiestee             KESKLINN - Vanalinn, Sadama
Merelahe tee              PÕHJA-TALLINN - Merimetsa
Meremehe tee              PIRITA - Pirita
Merihärja tn              HAABERSTI - Kakumäe
Merikanni tn              PIRITA - Lepiku
Merimetsa tee             PÕHJA-TALLINN - Merimetsa, Pelgulinn
Merinõela tn              HAABERSTI - Kakumäe
Merirahu tn               HAABERSTI - Õismäe
Merivälja tee             PIRITA - Pirita, Mähe, Mähe (Kaasiku), Merivälja
Mesika põik               PIRITA - Kose
Mesika tee                PIRITA - Kose
Mesila tn                 NÕMME - Pääsküla, Kivimäe
Metalli tn                KRISTIINE - Lilleküla (Mooni)
Metsa põik                NÕMME - Nõmme
Metsa tn                  NÕMME - Hiiu, Nõmme
Metsakooli põik           PIRITA - Kose
Metsakooli tee            PIRITA - Kose
Mait Metsanurga tn        NÕMME - Nõmme
Metsavahi põik            PIRITA - Pirita
Metsavahi tee             PIRITA - Pirita
Metsaveere tn             NÕMME - Pääsküla
Metsise tn                KRISTIINE - Lilleküla (Mooni)
Metsniku tee              PIRITA - Pirita
Mineraali tn              KRISTIINE - Lilleküla (Lille)
Mirta tn                  HAABERSTI - Vismeistri
Moonalao tn               HAABERSTI - Astangu
Mooni tn                  KRISTIINE, MUSTAMÄE - Lilleküla (Lille), Lilleküla (Mooni), Sääse
Moora tn                  NÕMME - Vana-Mustamäe
Moora umbtänav            NÕMME - Vana-Mustamäe
Moskva puiestee           LASNAMÄE - Mustakivi
Mugula tee                PIRITA - Mähe (aedlinn)
Muhu tn                   LASNAMÄE - Kuristiku
Mulla põik                PÕHJA-TALLINN - Pelgulinn
Mulla tn                  PÕHJA-TALLINN - Pelgulinn
Munga tn                  KESKLINN - Vanalinn (all-linn)
Muraka tn                 NÕMME - Pääsküla
Mureli tn                 HAABERSTI, KRISTIINE - Mustjõe, Lilleküla (Marja)
Muru tn                   NÕMME - Rahumäe
Mustakivi tee             LASNAMÄE - Mustakivi, Kuristiku, Katleri, Tondiraba
Mustamäe tee              KRISTIINE, MUSTAMÄE - Lilleküla (Marja), Lilleküla (Mooni), Kadaka, Sääse, Mustamäe
Mustika tn                NÕMME - Raudalu
Mustjuure tn              HAABERSTI - Mustjõe
Mustjõe põik              HAABERSTI - Mustjõe
Mustjõe tn                HAABERSTI - Mustjõe
Muti tn                   KRISTIINE - Lilleküla (Mooni)
Muuga tee                 PIRITA - Laiaküla
Muuluka tn                NÕMME - Pääsküla
Mõigu tn                  KESKLINN - Mõigu
Mõisa tn                  HAABERSTI - Haabersti
Mõisapõllu tn             HAABERSTI - Haabersti
Mõrra tee                 PIRITA - Pirita
Mõtuse tn                 KRISTIINE - Lilleküla (Mooni)
Mõõna tee                 PIRITA - Merivälja
Mäe tn                    LASNAMÄE - Paevälja
Mäealuse tn               MUSTAMÄE - Kadaka
Mäekalda tn               KESKLINN - Kadriorg
Mäekõrtsi tn              HAABERSTI - Haabersti
Mäepealse tn              MUSTAMÄE - Kadaka
Mäepere tn                HAABERSTI - Kakumäe
Mägra tn                  NÕMME - Pääsküla
Mähe tee                  PIRITA - Mähe
Mähe-Kaasiku tee          PIRITA - Mähe, Merivälja
Jakob Mändmetsa tn        NÕMME - Nõmme
Mängu tn                  NÕMME - Rahumäe
Männi tn                  NÕMME - Nõmme
Männiku tee               NÕMME - Rahumäe, Liiva, Männiku
Männiliiva tn             MUSTAMÄE - Mustamäe
Männimetsa põik           NÕMME - Laagri
Männimetsa tee            NÕMME - Laagri
Möldre tee                NÕMME - Pääsküla
Mündi tn                  KESKLINN - Vanalinn (all-linn)
Müta tn                   HAABERSTI - Vismeistri
Müürivahe tn              KESKLINN - Vanalinn (all-linn)

Naadi tee                 PIRITA - Merivälja, Mähe
Naaritsa tn               NÕMME - Pääsküla
Nabra tn                  PÕHJA-TALLINN - Pelgulinn
Naeri tn                  KESKLINN - Veerenni
Nafta tn                  KESKLINN - Kadriorg, Sadama
Naistepuna tee            PIRITA - Laiaküla
Narva maantee             KESKLINN, LASNAMÄE, PIRITA - Südalinn, Sadama, Kompassi, Raua, Kadriorg, Kurepõllu, Paevälja, Loopealse, Katleri, Kuristiku, Priisle, Iru
Nata tn                   HAABERSTI - Kakumäe
Neeme põik                PÕHJA-TALLINN - Kopli
Neeme tn                  PÕHJA-TALLINN - Kopli
Neemiku tn                LASNAMÄE - Paevälja (Paekalda kv)
Neiuvaiba tee             PIRITA - Mähe
Nelgi tn                  NÕMME - Männiku
Nepi tn                   KRISTIINE - Lilleküla (Linnu)
Nigli tn                  HAABERSTI - Kakumäe
Niguliste tn              KESKLINN - Vanalinn (all-linn)
Niidi põik                PÕHJA-TALLINN - Sitsi
Niidi tn                  PÕHJA-TALLINN - Sitsi
Niidu tee                 PIRITA - Kose
Niine põik                PÕHJA-TALLINN - Kalamaja
Niine tn                  PÕHJA-TALLINN - Kalamaja
Nirgi tn                  KRISTIINE, MUSTAMÄE - Lilleküla (Mooni), Sääse
Nisu tn                   PÕHJA-TALLINN - Pelgulinn
Nooda tee                 HAABERSTI - Kakumäe
Noole tn                  PÕHJA-TALLINN - Kalamaja
Noorkuu tn                HAABERSTI - Pikaliiva
Nugise tn                 NÕMME - Pääsküla
Nuia tn                   LASNAMÄE - Sõjamäe
Nulu tn                   PIRITA - Maarjamäe
Nunne tn                  KESKLINN - Vanalinn (all-linn), Vanalinn
Nurklik tn                HAABERSTI - Mustjõe
Nurme tn                  NÕMME - Nõmme
Nurmenuku tee             PIRITA - Mähe (aedlinn)
Nurmiku põik              PIRITA - Kose
Nurmiku tee               PIRITA - Kose
Nõeliku tn                HAABERSTI - Vismeistri
Nõgikikka tn              HAABERSTI - Pikaliiva
Nõlva tn                  PÕHJA-TALLINN - Karjamaa (Hundipea)
Nõmme põik                KRISTIINE - Lilleküla (Linnu)
Nõmme tee                 KRISTIINE, MUSTAMÄE - Lilleküla (Linnu), Tondi, Siili
Nõmme-Kase tn             NÕMME - Hiiu, Nõmme
Nõo tee                   PIRITA - Mähe
Nõva tn                   NÕMME - Vana-Mustamäe
Näituse tn                NÕMME - Rahumäe
Näsiniine tee             PIRITA - Mähe

Oa tn                     KESKLINN - Veerenni
Oblika tee                PIRITA - Mähe (aedlinn)
Oda tn                    PÕHJA-TALLINN - Kalamaja
Odra tn                   KESKLINN - Keldrimäe, Juhkentali
Oja tn                    HAABERSTI - Pikaliiva
Ojakääru tn               HAABERSTI - Kakumäe
Ojaveere tn               HAABERSTI - Mustjõe
Oksa tn                   KRISTIINE - Tondi
Olevi põik                NÕMME - Kivimäe
Olevi tn                  NÕMME - Kivimäe
Olevimägi                 KESKLINN - Vanalinn (all-linn)
Oleviste tn               KESKLINN - Vanalinn (all-linn)
Oomi tn                   KESKLINN - Mõigu
Orase tn                  PÕHJA-TALLINN - Pelgulinn
Orava tn                  NÕMME - Liiva
Oru tn                    KESKLINN - Kadriorg
Osja tee                  PIRITA - Kose
Osmussaare tn             LASNAMÄE - Tondiraba, Mustakivi
Oti tn                    HAABERSTI - Kakumäe
Georg Otsa tn             KESKLINN - Südalinn
Otsatalu tn               HAABERSTI - Kakumäe
Otse tn                   HAABERSTI - Mustjõe

Paadi tn                  KESKLINN - Sadama
Paagi tn                  PÕHJA-TALLINN - Paljassaare
Paakspuu tee              PIRITA - Merivälja
Paasiku tn                LASNAMÄE - Katleri
Paavli tn                 PÕHJA-TALLINN - Sitsi, Karjamaa
Padriku tee               PIRITA - Mähe
Padu tn                   NÕMME - Vana-Mustamäe
Pae tn                    LASNAMÄE - Sikupilli, Ülemiste, Pae
Paekaare tn               LASNAMÄE - Pae
Paekalda tn               LASNAMÄE - Paevälja (Paekalda kv)
Paekivi tn                LASNAMÄE - Sikupilli
Paepargi tn               LASNAMÄE - Sikupilli
Paevälja puiestee         LASNAMÄE - Paevälja
Pagari tn                 KESKLINN - Vanalinn (all-linn)
Paide tn                  KESKLINN - Kitseküla
Paiste tn                 NÕMME - Hiiu
Paisu tn                  PIRITA - Kose
Paju tn                   PIRITA - Maarjamäe
Pajude puiestee           NÕMME - Laagri
Pajulille tee             PIRITA - Kose
Pajustiku tee             PIRITA - Mähe
Pakase tn                 HAABERSTI - Mustjõe
Palderjani tee            PIRITA - Mähe
Paldiski maantee          KESKLINN, PÕHJA-TALLINN, KRISTIINE, HAABERSTI - Kassisaba, Kelmiküla, Pelgulinn, Lilleküla (Lille), Lilleküla (Marja), Merimetsa, Mustjõe, Haabersti, Veskimetsa, Pikaliiva, Väike-Õismäe, Astangu, Mäeküla
Paljandi tn               HAABERSTI - Õismäe
Paljassaare põik          PÕHJA-TALLINN - Paljassaare
Paljassaare tee           PÕHJA-TALLINN - Paljassaare
Pallasti tn               LASNAMÄE - Sikupilli, Uuslinn
Palli tn                  NÕMME - Rahumäe
Palu tn                   NÕMME - Pääsküla
Palusambla tn             NÕMME - Pääsküla
Paneeli tn                LASNAMÄE - Sõjamäe (Sõstramäe)
Panga tn                  LASNAMÄE - Paevälja
Papli tn                  PIRITA - Maarjamäe
Paplite puiestee          NÕMME - Laagri
Parda tn                  KESKLINN - Sadama
Pardi tn                  KRISTIINE - Tondi
Pardiloigu tn             PÕHJA-TALLINN - Kopli
Pargi tn                  NÕMME - Hiiu
Parmu tn                  MUSTAMÄE - Sääse
Parve tn                  HAABERSTI - Vismeistri
Patriarh Aleksius II väljak | LASNAMÄE - Loopealse
Pebre tn                  PÕHJA-TALLINN - Pelgulinn
Pedaja tn                 NÕMME - Liiva
Peetri tn                 PÕHJA-TALLINN - Kalamaja
Pelguranna tn             PÕHJA-TALLINN - Pelguranna, Kopli
Pesa tn                   NÕMME - Nõmme
Peterburi tee             LASNAMÄE - Sikupilli, Ülemiste, Sõjamäe, Väo, Mustakivi, Seli
Petrooleumi tn            KESKLINN - Sadama, Kadriorg
Pidu tn                   NÕMME - Hiiu
Pihlaka tn                NÕMME - Männiku
Pihlametsa tee            PIRITA - Merivälja
Piibelehe tn              HAABERSTI, KRISTIINE - Mustjõe, Lilleküla (Marja)
Piibri tn                 NÕMME - Raudalu
Piima tn                  KESKLINN - Kitseküla
Piiri tn                  NÕMME - Nõmme, Rahumäe
Piiritsa tn               HAABERSTI - Vismeistri
Piiskopi tn               KESKLINN - Vanalinn (Toompea)
Pikaliiva tn              HAABERSTI - Pikaliiva
Pikk jalg                 KESKLINN - Vanalinn (all-linn), Vanalinn (Toompea)
Pikk tn                   KESKLINN - Vanalinn (all-linn)
Pikksilma tn              KESKLINN - Kadriorg
Pikri tn                  LASNAMÄE - Laagna
Pikse tn                  HAABERSTI - Mustjõe
Piksepeni tn              PIRITA - Lepiku
Pille tn                  KESKLINN - Veerenni
Pilliroo tn               NÕMME - Pääsküla
Pilve tn                  KESKLINN - Uus Maailm
Pilviku tn                NÕMME - Nõmme
Paul Pinna tn             LASNAMÄE - Laagna
Pinu tn                   NÕMME - Raudalu
Pirita tee                PIRITA, KESKLINN - Maarjamäe, Pirita, Kadriorg
Pirni tn                  KRISTIINE, HAABERSTI - Lilleküla (Marja), Mustjõe
Planeedi tn               KESKLINN - Uus Maailm
Plangu tn                 NÕMME - Kivimäe
Plasti tn                 LASNAMÄE - Sõjamäe
Pohla tn                  NÕMME - Liiva
Pojengi tee               PIRITA - Mähe (aedlinn)
Poldri tn                 KESKLINN - Sadama
Poordi tn                 KESKLINN - Sadama
Poru tn                   HAABERSTI - Kakumäe
Jaan Poska tn             KESKLINN - Kadriorg, Raua
Postitalu tn              HAABERSTI - Tiskre
Preesi tn                 PÕHJA-TALLINN - Pelgulinn
Prii tn                   NÕMME - Rahumäe
Priimula tee              PIRITA - Mähe (aedlinn)
Priisle tee               LASNAMÄE - Priisle
Printsu tee               HAABERSTI - Pikaliiva
Pronksi tn                KESKLINN - Raua, Kompassi, Torupilli
Puhangu tn                PÕHJA-TALLINN - Pelguranna
Puhke tn                  KESKLINN - Veerenni
Puhkekodu tee             PIRITA - Kose
Puhma tn                  NÕMME - Nõmme
Puju tn                   LASNAMÄE - Loopealse
Puki tee                  PIRITA - Mähe
Punane tn                 LASNAMÄE - Pae, Ülemiste, Sõjamäe, Laagna
Pune tee                  PIRITA - Kose
Punga tn                  PIRITA - Maarjamäe
Puraviku tn               NÕMME - Liiva
Purde tn                  PIRITA - Kose (Varsaallika)
Purje tn                  PIRITA - Pirita
Puu tn                    NÕMME - Hiiu
Puusepa tn                NÕMME - Liiva
Puuvilja tn               NÕMME - Nõmme
Puuvilla tn               PÕHJA-TALLINN - Sitsi
Põdra tn                  NÕMME - Pääsküla, Laagri
Põdrakanepi tee           PIRITA - Laiaküla
Põhja puiestee            PÕHJA-TALLINN, KESKLINN - Kalamaja, Vanalinn
Põhjakaare tn             NÕMME - Hiiu, Nõmme
Põlde põik                HAABERSTI - Kakumäe
Põlde tn                  HAABERSTI - Kakumäe, Vismeistri
Põldma tn                 PIRITA - Lepiku
Põldmarja tn              HAABERSTI - Mustjõe
Põlendiku tn              HAABERSTI - Pikaliiva
Põllu põik                NÕMME - Pääsküla
Põllu tn                  NÕMME - Nõmme, Hiiu, Kivimäe, Pääsküla
Põllumäe tn               HAABERSTI - Vismeistri
Põõsa tee                 PIRITA - Mähe
Päevakoera tn             PIRITA - Lepiku
Pähkli tn                 PIRITA - Maarjamäe
Päikese puiestee          NÕMME - Pääsküla
Pärituule tn              HAABERSTI - Mustjõe
Pärja tn                  NÕMME - Pääsküla
Jakob Pärna tn            KESKLINN - Torupilli
Pärnade puiestee          NÕMME - Laagri
Pärnamäe tee              PIRITA - Iru, Laiaküla, Lepiku, Mähe (aedlinn)
Pärnaõie tee              PIRITA - Laiaküla
Pärniku tee               PIRITA - Merivälja
Pärnu maantee             KESKLINN, KRISTIINE, NÕMME - Vanalinn, Südalinn, Tatari, Tõnismäe, Uus Maailm, Veerenni, Kitseküla, Järve, Liiva, Rahumäe, Nõmme, Hiiu, Kivimäe, Pääsküla
Pärnulõuka tn             PÕHJA-TALLINN - Kopli
Pääsküla tn               NÕMME - Pääsküla
Pääsukese tn              KESKLINN - Maakri
Pääsusilma tee            PIRITA - Kose
Pöörise tn                MUSTAMÄE - Kadaka
Pühavaimu tn              KESKLINN - Vanalinn (all-linn)
Püssirohu tn              KESKLINN - Juhkentali
Püü põik                  KRISTIINE - Lilleküla (Linnu)
Püü tn                    KRISTIINE - Lilleküla (Linnu)

Raadiku tn                LASNAMÄE - Seli, Mustakivi
Raba tn                   NÕMME - Pääsküla
Rabaküla tn               MUSTAMÄE - Kadaka
Rabaveere tn              NÕMME - Pääsküla
Raekoja plats             KESKLINN - Vanalinn (all-linn)
Raekoja tn                KESKLINN - Vanalinn (all-linn)
Rahe tn                   HAABERSTI - Mustjõe
Rahu tee                  LASNAMÄE - Paevälja, Loopealse, Katleri, Kuristiku, Priisle, Seli
Rahu tn                   NÕMME - Hiiu
Rahukohtu tn              KESKLINN - Vanalinn (Toompea)
Rahumäe tee               KRISTIINE, NÕMME - Rahumäe, Järve, Tondi
Rahvakooli tee            PIRITA - Kose
Raie tn                   NÕMME - Pääsküla
Raja tn                   MUSTAMÄE, NÕMME - Vana-Mustamäe, Kadaka, Mustamäe
Rajametsa tn              NÕMME - Vana-Mustamäe
Rajapere tn               HAABERSTI - Kakumäe
Rakise tn                 LASNAMÄE - Sõjamäe
Randla tn                 PÕHJA-TALLINN - Pelguranna
Randvere tee              PIRITA - Pirita, Mähe, Mähe (aedlinn)
Rangu tn                  HAABERSTI - Pikaliiva
Ranna tee                 PIRITA - Merivälja
Rannamõisa tee            HAABERSTI - Pikaliiva, Haabersti, Tiskre
Rannamäe tee              KESKLINN, PÕHJA-TALLINN - Vanalinn, Kalamaja
Rannaniidu tn             HAABERSTI - Tiskre
Ranniku põik              PIRITA - Merivälja
Ranniku tee               PIRITA - Merivälja, Mähe
Rao tn                    NÕMME - Pääsküla
Rapla tn                  KESKLINN - Kitseküla
Rataskaevu tn             KESKLINN - Vanalinn (all-linn)
Ratta tn                  NÕMME - Liiva
Raua põik                 KESKLINN - Raua
Raua tn                   KESKLINN - Raua, Kompassi
Kristjan Raua tn          NÕMME - Nõmme
Raudosja tee              PIRITA - Kose
Raudtee tn                NÕMME - Rahumäe, Nõmme, Hiiu, Kivimäe, Pääsküla
Ravi tn                   KESKLINN - Veerenni
Ravila tn                 NÕMME - Nõmme
Rebase tn                 NÕMME - Pääsküla
Rebasesaba tee            PIRITA - Mähe
Regati puiestee           PIRITA - Pirita
Reha tn                   HAABERSTI - Pikaliiva
Rehe põik                 HAABERSTI - Astangu
Rehe tn                   HAABERSTI - Astangu
Reidi tee                 KESKLINN - Kadriorg, Sadama
Villem Reimani tn         KESKLINN - Kompassi
Ado Reinvaldi tn          KESKLINN - Torupilli
Reisijate tn              PÕHJA-TALLINN - Kalamaja
Reketi tn                 KESKLINN - Kitseküla
Remmelga tn               NÕMME - Männiku
Retke tee                 MUSTAMÄE, KRISTIINE - Mustamäe, Järve
Riida tn                  NÕMME - Raudalu
Riisika tn                NÕMME - Liiva
Risti tn                  NÕMME - Rahumäe, Liiva
Ristiku põik              PÕHJA-TALLINN - Pelgulinn
Ristiku tn                PÕHJA-TALLINN - Pelgulinn
Rivi tn                   KRISTIINE - Tondi
Rocca al Mare tn          HAABERSTI - Rocca al Mare
Roheline aas              KESKLINN - Kadriorg
Roheline tn               NÕMME - Nõmme
Rohu tn                   PÕHJA-TALLINN - Pelgulinn, Kelmiküla
Rohula tn                 NÕMME - Pääsküla
Rohumaa tn                HAABERSTI - Mustjõe
Ronga tn                  KRISTIINE - Lilleküla (Mooni)
Roo tn                    PÕHJA-TALLINN - Pelgulinn
Roolahe tn                HAABERSTI - Tiskre
Roopa tn                  KESKLINN - Kassisaba
Roosi tn                  NÕMME - Pääsküla
Roosikrantsi tn           KESKLINN - Tõnismäe
Roostiku tn               HAABERSTI - Tiskre
Roseni tn                 KESKLINN - Sadama
Rotermanni tn             KESKLINN - Sadama
Rukki tn                  PÕHJA-TALLINN - Pelgulinn
Rukkilille tee            PIRITA - Mähe (aedlinn)
Rulli tn                  NÕMME - Liiva
Rumbi tn                  KESKLINN - Sadama
Rummu tee                 PIRITA - Pirita, Maarjamäe, Kose
Rutu tn                   KESKLINN - Vanalinn (Toompea)
Ruunaoja tn               LASNAMÄE - Sõjamäe
Rõika tn                  HAABERSTI - Mustjõe
Rõugu tn                  HAABERSTI - Pikaliiva
Rõõmu tn                  NÕMME - Pääsküla
Räga tn                   HAABERSTI - Pikaliiva
Rähkloo tn                LASNAMÄE - Loopealse
Rähni tn                  KRISTIINE - Tondi
Räime tn                  HAABERSTI - Kakumäe
Räitsaka tn               HAABERSTI - Mustjõe
Rändrahnu tee             PIRITA - Merivälja
Ränduri tn                NÕMME - Pääsküla
Rännaku puiestee          NÕMME - Pääsküla
Rästa põik                KRISTIINE - Lilleküla (Linnu)
Rästa tn                  KRISTIINE - Lilleküla (Linnu)
Rätsepa tee               PIRITA - Mähe, Pirita
Rävala puiestee           KESKLINN - Südalinn, Sibulaküla, Maakri
Räägu tn                  KRISTIINE - Lilleküla (Mooni), Lilleküla (Linnu)
Ründi tn                  HAABERSTI - Vismeistri
Rünga tn                  LASNAMÄE - Paevälja
Rüütli tn                 KESKLINN - Vanalinn (all-linn)

Saadu tn                  HAABERSTI - Pikaliiva
Saagi tn                  NÕMME - Pääsküla (Vana-Pääsküla)
Saani tn                  PÕHJA-TALLINN - Kelmiküla
Saare tn                  PIRITA - Maarjamäe
Saaremaa puiestee         LASNAMÄE - Kuristiku
Saarepiiga puiestee       LASNAMÄE - Laagna
Saarepuu tn               NÕMME - Pääsküla
Saariku tee               PIRITA - Mähe
Saarma põik               HAABERSTI - Mustjõe
Saarma tn                 HAABERSTI - Mustjõe
Saarvahtra puiestee       NÕMME - Laagri
Sadama tn                 KESKLINN - Sadama
Saeveski tn               NÕMME - Liiva
Sagari tn                 HAABERSTI - Pikaliiva
Saha põik                 NÕMME - Pääsküla
Saha tn                   NÕMME - Pääsküla
Saiakang                  KESKLINN - Vanalinn (all-linn)
Sakala tn                 KESKLINN - Tatari, Südalinn
Saku tn                   KESKLINN - Kitseküla
Salme tn                  PÕHJA-TALLINN - Kalamaja
Salu tee                  PIRITA - Merivälja
Salve tn                  NÕMME - Hiiu
Sambla tn                 NÕMME - Nõmme
Sambliku tn               NÕMME - Pääsküla
Sammu tn                  KRISTIINE - Tondi
Sanatooriumi tn           NÕMME - Hiiu, Kivimäe
Sanglepa tn               PIRITA - Maarjamäe
Sarapiku tee              PIRITA - Merivälja
Sarapuu tn                PIRITA - Maarjamäe
Sarra tn                  HAABERSTI - Pikaliiva
Sarruse tn                LASNAMÄE - Sõjamäe
Sarve tn                  NÕMME - Pääsküla
Saturni tn                KESKLINN - Uus Maailm
Saue tn                   PÕHJA-TALLINN - Pelgulinn
Sauna tn                  KESKLINN - Vanalinn (all-linn)
Saviliiva tee             HAABERSTI - Vismeistri
Seebi tn                  KRISTIINE - Järve, Tondi
Seedri põik               NÕMME - Pääsküla
Seedri tn                 NÕMME - Pääsküla
Seemne tn                 KRISTIINE - Lilleküla (Marja)
Seene tn                  NÕMME - Nõmme
Seli puiestee             LASNAMÄE - Seli
Selise tn                 HAABERSTI - Kakumäe
Selja tn                  HAABERSTI - Õismäe
Seljaku tn                NÕMME - Hiiu
Sepa tn                   PÕHJA-TALLINN - Kopli
Sepapaja tn               LASNAMÄE - Ülemiste
Sepapere tn               HAABERSTI - Pikaliiva
Sepise tn                 LASNAMÄE - Ülemiste
Serva tn                  NÕMME - Nõmme, Hiiu
Side tn                   NÕMME - Rahumäe
Siduri tn                 KESKLINN - Luite
Sihi tn                   NÕMME - Rahumäe, Nõmme, Hiiu, Kivimäe
Siia tn                   HAABERSTI - Kakumäe
Siidisaba tn              KRISTIINE - Lilleküla (Linnu)
Siili tn                  MUSTAMÄE - Siili
Siire tn                  HAABERSTI - Mustjõe
Sikupilli tn              LASNAMÄE - Sikupilli
Sikuti tn                 HAABERSTI - Kakumäe
Silde tn                  LASNAMÄE - Sõjamäe
Silgu tn                  HAABERSTI - Kakumäe, Vismeistri
Silikaltsiidi tn          NÕMME - Männiku, Liiva
Silla tn                  NÕMME - Nõmme
Silluse tn                LASNAMÄE - Sõjamäe
Silmiku tn                PIRITA - Lepiku
Silmu tn                  HAABERSTI - Kakumäe
Sinika tn                 KRISTIINE - Lilleküla (Lille)
Siniladva tee             PIRITA - Mähe
Sinilille tn              NÕMME - Männiku
Sinimäe tn                LASNAMÄE - Seli
Sinirebase tn             NÕMME - Raudalu
Sinitiiva tn              PIRITA - Lepiku
Sipelga tn                MUSTAMÄE - Sääse
Sirbi tn                  PÕHJA-TALLINN - Kopli
Sireli tn                 NÕMME - Pääsküla
Sirge tn                  HAABERSTI - Mustjõe
Sirptiiva tn              PIRITA - Lepiku
Sisaski tn                NÕMME - Pääsküla
Sitsi tn                  PÕHJA-TALLINN - Sitsi
Sitska tee                PIRITA - Mähe
Juhan Smuuli tee          LASNAMÄE - Laagna, Paevälja, Pae, Kurepõllu
Sompa tee                 PIRITA - Lepiku, Kloostrimetsa
Soo tn                    PÕHJA-TALLINN - Kalamaja
Sookaskede puiestee       NÕMME - Laagri
Soolahe tee               HAABERSTI - Kakumäe
Soone põik                NÕMME - Vana-Mustamäe
Soone tn                  NÕMME, MUSTAMÄE - Vana-Mustamäe, Kadaka
Sooranna tn               HAABERSTI - Kakumäe
Sooviku tn                NÕMME - Vana-Mustamäe
Soovildiku tn             NÕMME - Pääsküla
Soovõha tee               PIRITA - Mähe
Spordi tn                 KRISTIINE - Lilleküla (Linnu)
Staadioni tn              KESKLINN - Juhkentali
Staapli tn                PÕHJA-TALLINN - Kalamaja
Suislepa tee              PIRITA - Mähe (aedlinn)
Suitsu põik               KESKLINN - Luite
Suitsu tn                 KESKLINN - Luite
Sule tn                   KRISTIINE - Lilleküla (Linnu)
Sulevi tn                 NÕMME - Kivimäe
Sulevimägi                KESKLINN - Vanalinn (all-linn)
Sumba tn                  HAABERSTI - Vismeistri
Supluse puiestee          PIRITA - Pirita
Suru tn                   PIRITA - Lepiku
Suur-Ameerika tn          KESKLINN - Tõnismäe, Uus Maailm
Suurekivi tn              PIRITA - Lepiku
Suurevälja tn             HAABERSTI - Kakumäe
Suur-Karja tn             KESKLINN - Vanalinn (all-linn), Vanalinn
Suur-Kloostri tn          KESKLINN - Vanalinn (all-linn), Vanalinn
Suur-Laagri tn            PÕHJA-TALLINN - Kalamaja
Suur-Männiku tn           NÕMME - Männiku
Suur-Paala tn             LASNAMÄE - Ülemiste
Suur-Patarei tn           PÕHJA-TALLINN - Kalamaja
Suur Rannavärav           KESKLINN - Vanalinn
Suur-Sõjamäe põik         LASNAMÄE - Sõjamäe
Suur-Sõjamäe tn           LASNAMÄE - Ülemiste, Sõjamäe
Suurtüki tn               KESKLINN, PÕHJA-TALLINN - Vanalinn (all-linn), Vanalinn, Kalamaja
Suusa tn                  NÕMME - Nõmme
Suve tn                   PÕHJA-TALLINN - Kelmiküla
Suvila tn                 NÕMME - Pääsküla
Sõbra põik                NÕMME - Pääsküla
Sõbra tn                  NÕMME - Pääsküla, Kivimäe
Sõjakooli tn              KRISTIINE - Tondi
Sõle tn                   PÕHJA-TALLINN - Pelgulinn, Pelguranna, Sitsi
Sõlme tn                  NÕMME - Hiiu
Sõmera tn                 PÕHJA-TALLINN - Pelgulinn
Sõnajala tn               NÕMME - Pääsküla
Sõpruse puiestee          KRISTIINE - Lilleküla (Linnu), Lilleküla (Mooni), Sääse, Siili, Mustamäe
Sõpruse puiestee          MUSTAMÄE - Lilleküla (Linnu), Lilleküla (Mooni), Sääse, Siili, Mustamäe
Sõstra tn                 KRISTIINE - Lilleküla (Mooni)
Sõstramäe tn              LASNAMÄE - Sõjamäe
Sõudebaasi tee            HAABERSTI - Pikaliiva (Viki)
Sõõru tn                  HAABERSTI - Pikaliiva
Sädeme tn                 HAABERSTI - Pikaliiva
Säina tn                  HAABERSTI - Kakumäe
Ernst Särgava allee       PIRITA - Kose (Kallaste)
Särje tn                  NÕMME - Kivimäe, Pääsküla
Särjesilma tn             HAABERSTI - Kakumäe
Sääse tn                  MUSTAMÄE - Sääse
Söe tn                    KESKLINN - Luite
Söödi tn                  PÕHJA-TALLINN - Pelgulinn
Peeter Süda tn            KESKLINN - Tatari
Sügise tn                 PÕHJA-TALLINN - Kelmiküla
Sügislase tn              PIRITA - Lepiku
Süsta tn                  PÕHJA-TALLINN - Kopli
Juhan Sütiste tee         MUSTAMÄE - Mustamäe

Taara tn                  NÕMME - Kivimäe, Hiiu
Taela tn                  HAABERSTI - Õismäe
Taevakivi tn              LASNAMÄE - Tondiraba
Taevastiiva tn            PIRITA - Lepiku
Tagala tn                 HAABERSTI - Astangu
Tagamaa tee               KESKLINN - Aegna
Taime tn                  PÕHJA-TALLINN - Pelgulinn
Tala tn                   LASNAMÄE - Sõjamäe
Tallinna tn               NÕMME - Rahumäe
Taludevahe tn             HAABERSTI - Tiskre
Talve tn                  NÕMME - Nõmme
Talviku tn                KRISTIINE - Lilleküla (Linnu)
Tambeti tn                LASNAMÄE - Ülemiste
Tamme tn                  PIRITA - Maarjamäe
Tammede puiestee          NÕMME - Laagri
Tammepärja tn             NÕMME - Pääsküla
Tammiku tn                NÕMME - Pääsküla
A. H. Tammsaare tee       MUSTAMÄE, KRISTIINE, KESKLINN - Mustamäe, Kadaka, Sääse, Siili, Tondi, Järve, Kitseküla
Tanuma tn                 HAABERSTI - Õismäe
Tapri tn                  LASNAMÄE - Sõjamäe
Tare tn                   KESKLINN - Veerenni
Tarja tn                  PIRITA - Maarjamäe
Tarna tn                  HAABERSTI - Mustjõe
Tartu maantee             KESKLINN - Kompassi, Maakri, Torupilli
Tartu maantee             LASNAMÄE - Keldrimäe, Juhkentali, Sikupilli, Ülemiste järv, Ülemiste, Mõigu
Tasuja puiestee           LASNAMÄE - Kuristiku, Mustakivi, Priisle, Seli
Tatari tn                 KESKLINN - Tatari, Veerenni
Teaduspargi tn            MUSTAMÄE - Kadaka
Teatri väljak             KESKLINN - Südalinn
Tedre põik                KRISTIINE - Lilleküla (Linnu)
Tedre tn                  KRISTIINE - Tondi, Lilleküla (Linnu), Lilleküla (Mooni)
Tedrepere tn              HAABERSTI - Vismeistri
Tehnika tn                PÕHJA-TALLINN, KESKLINN - Kelmiküla, Kassisaba, Uus Maailm
Teisepere tn              HAABERSTI - Tiskre
Teivi tn                  HAABERSTI - Kakumäe
Telliskivi tn             PÕHJA-TALLINN - Pelgulinn, Kalamaja
Terase tn                 KESKLINN - Raua
Tervise tn                KRISTIINE, MUSTAMÄE, NÕMME - Järve, Rahumäe, Mustamäe
Tihase tn                 KRISTIINE - Lilleküla (Linnu), Lilleküla (Mooni)
Tihniku tn                NÕMME - Vana-Mustamäe, Pääsküla
Tiigi tn                  NÕMME - Vana-Mustamäe
Tiiru tn                  NÕMME - Nõmme
Tiiu tn                   KESKLINN - Veerenni
Tiiva tn                  KRISTIINE - Lilleküla (Linnu)
Tildri põik               MUSTAMÄE - Sääse
Tildri tn                 MUSTAMÄE, KRISTIINE - Sääse, Lilleküla (Mooni)
Timuti tn                 PÕHJA-TALLINN - Pelgulinn
Tina tn                   KESKLINN - Raua
Tindi tn                  HAABERSTI - Kakumäe
Tirgu tn                  HAABERSTI - Kakumäe
Tiskre tee                HAABERSTI - Vismeistri, Tiskre
Tiskrevälja tn            HAABERSTI - Tiskre
Rudolf Tobiase tn         KESKLINN - Raua
Tohu tn                   PIRITA - Maarjamäe
Tolli tn                  KESKLINN - Vanalinn (all-linn)
Tolmuka tee               PIRITA - Mähe (aedlinn)
Tondi tn                  KESKLINN, KRISTIINE - Kitseküla, Tondi
Tondiraba tn              LASNAMÄE - Katleri
Tooma tn                  LASNAMÄE - Väo
Toomapere tn              HAABERSTI - Tiskre
Toome puiestee            NÕMME - Pääsküla
Toome põik                NÕMME - Pääsküla
Toomiku tee               PIRITA - Mähe, Merivälja
Toominga tn               PIRITA - Pirita
Toom-Kooli tn             KESKLINN - Vanalinn (Toompea)
Toom-Kuninga tn           KESKLINN - Tõnismäe, Uus Maailm
Toompea tn                KESKLINN - Vanalinn (Toompea), Vanalinn
Toompuiestee              KESKLINN, PÕHJA-TALLINN - Kelmiküla, Kassisaba, Vanalinn
Toom-Rüütli tn            KESKLINN - Vanalinn (Toompea)
Toonela tee               KESKLINN - Juhkentali
Topi tn                   PIRITA - Pirita
Tormi tn                  KESKLINN - Kadriorg
Torni tn                  NÕMME - Hiiu
Tornimäe tn               KESKLINN - Maakri
Torupilli ots             KESKLINN - Keldrimäe
Trahteri tn               HAABERSTI - Vismeistri
Treiali tn                PÕHJA-TALLINN - Kopli
Trepi tn                  NÕMME - Vana-Mustamäe
Trummi põik               NÕMME - Vana-Mustamäe
Trummi tn                 NÕMME - Vana-Mustamäe
Tuha tn                   LASNAMÄE - Sikupilli
Tuhkru tn                 HAABERSTI - Mustjõe
Tuisu tn                  KRISTIINE - Järve, Tondi
Tuki tn                   HAABERSTI - Pikaliiva
Tulbi tn                  KRISTIINE - Lilleküla (Lille)
Tulekivi tn               HAABERSTI - Õismäe
Tuleraua tn               HAABERSTI - Õismäe
Tulika põik               KRISTIINE - Lilleküla (Lille)
Tulika tn                 KRISTIINE - Lilleküla (Lille), Lilleküla (Linnu)
Tulimulla tn              HAABERSTI - Pikaliiva
Tuluste tn                HAABERSTI - Õismäe
Tungla tn                 NÕMME - Kivimäe
Tupsi tee                 PIRITA - Kose
Turba tn                  LASNAMÄE - Kurepõllu
Turbasambla tn            NÕMME - Pääsküla
Tursa tn                  HAABERSTI - Kakumäe
Turu plats                NÕMME - Nõmme
Turu tn                   KESKLINN - Keldrimäe
Tuukri põik               KESKLINN - Sadama
Tuukri tn                 KESKLINN - Sadama
Tuule tee                 PIRITA - Merivälja
Tuulemaa tn               PÕHJA-TALLINN - Pelguranna
Tuulemäe tn               LASNAMÄE - Sikupilli
Tuulenurga tn             PIRITA - Maarjamäe
Tuuleveski tn             HAABERSTI - Mustjõe, Veskimetsa
Tuuliku tee               HAABERSTI, MUSTAMÄE, KRISTIINE - Mustjõe, Veskimetsa, Kadaka, Lilleküla (Marja)
Tuvi tn                   KESKLINN - Tõnismäe
Tõivu tn                  LASNAMÄE - Ülemiste
Tõllu tn                  PÕHJA-TALLINN - Kalamaja
Tõnismägi                 KESKLINN - Tõnismäe
Tõnu tn                   HAABERSTI - Vismeistri
Tõru tn                   PIRITA - Maarjamäe
Tõrviku tn                LASNAMÄE - Ülemiste
Tõusu tee                 PIRITA - Merivälja
Tähe tn                   NÕMME - Hiiu, Nõmme
Tähesaju tee              LASNAMÄE - Tondiraba
Tähetorni tn              NÕMME, HAABERSTI - Hiiu, Vana-Mustamäe, Mäeküla
Täpiku tn                 PIRITA - Lepiku
Töökoja tn                KESKLINN - Veerenni
Tööstuse tn               PÕHJA-TALLINN - Kalamaja, Karjamaa, Karjamaa (Hundipea)
Türi tn                   KESKLINN - Kitseküla
Konstantin Türnpu tn      KESKLINN - Torupilli
Tüve tn                   KRISTIINE - Tondi, Lilleküla (Linnu)

Ubalehe tee               PIRITA - Mähe
Udeselja tn               PIRITA - Lepiku
Ugala tn                  NÕMME - Hiiu, Kivimäe
Uime tn                   HAABERSTI - Kakumäe
Ujuki tn                  HAABERSTI - Kakumäe
Uku tn                    NÕMME - Kivimäe
Umboja tn                 HAABERSTI - Õismäe
Uneliblika tn             PIRITA - Lepiku
Unna tn                   HAABERSTI - Kakumäe
Urva tn                   PIRITA - Maarjamäe
Ussilaka tee              PIRITA - Mähe
Ussimäe tee               LASNAMÄE - Priisle, Seli
Uue Maailma tn            KESKLINN - Uus Maailm
Uuepere tn                HAABERSTI - Vismeistri
Uus tn                    KESKLINN - Vanalinn
Uus-Kalamaja tn           PÕHJA-TALLINN - Kalamaja
Uuslinna tn               LASNAMÄE - Uuslinn, Kurepõllu
Uus-Maleva tn             PÕHJA-TALLINN - Kopli
Uus-Sadama tn             KESKLINN - Sadama
Uustalu tn                HAABERSTI - Vismeistri
Uus-Tatari tn             KESKLINN - Veerenni

Vaablase tn               MUSTAMÄE - Sääse
Vaagi tn                  HAABERSTI - Tiskre
Vaalu tn                  HAABERSTI - Pikaliiva
Vaari tn                  KESKLINN - Kitseküla
Vaarika tn                KRISTIINE - Lilleküla (Lille)
Vaate põik                PIRITA - Merivälja
Vaate tee                 PIRITA - Merivälja
Vabaduse puiestee         NÕMME - Liiva, Rahumäe, Nõmme, Hiiu, Kivimäe, Pääsküla
Vabaduse väljak           KESKLINN - Vanalinn, Tõnismäe
Vabarna tee               PIRITA - Mähe (aedlinn)
Vabaõhukooli tee          PIRITA - Kose
Vabaõhumuuseumi tee       HAABERSTI - Haabersti, Rocca al Mare, Õismäe, Kakumäe, Vismeistri
Vabe tn                   HAABERSTI - Kakumäe
Vabriku tn                PÕHJA-TALLINN - Kalamaja
Vahe tn                   NÕMME - Nõmme, Rahumäe
Vahepere tn               HAABERSTI - Tiskre
Vahtra tn                 NÕMME - Hiiu
Vahtramäe tee             PIRITA - Mähe
Vahtriku tee              PIRITA - Mähe, Merivälja
Vahulille tee             PIRITA - Kose
Vaigu tn                  NÕMME - Rahumäe
Vaikne tn                 KESKLINN - Veerenni
Vaimu tn                  KESKLINN - Vanalinn (all-linn)
Vainu tn                  NÕMME - Pääsküla
Vainutalu põik            HAABERSTI - Kakumäe
Vainutalu tn              HAABERSTI - Kakumäe
Vaksiku tn                PIRITA - Lepiku
Valdeku tn                NÕMME - Nõmme, Männiku, Liiva, Raudalu
Valge tn                  LASNAMÄE - Kurepõllu, Uuslinn
Valgevase tn              PÕHJA-TALLINN - Kalamaja
Valguse tn                NÕMME - Nõmme
Valguta tn                PIRITA - Lepiku
Valli tn                  KESKLINN - Vanalinn
Valukoja tn               LASNAMÄE - Ülemiste
Valve tn                  NÕMME - Kivimäe, Hiiu
Vambola tn                KESKLINN - Sibulaküla
Vana turg                 KESKLINN - Vanalinn (all-linn)
Vana-Kalamaja tn          PÕHJA-TALLINN - Kalamaja
Vana-Keldrimäe tn         KESKLINN - Keldrimäe
Vanakuu tn                HAABERSTI - Pikaliiva
Vana-Kuuli tn             LASNAMÄE - Paevälja
Vana-Liivamäe tn          KESKLINN - Keldrimäe
Vana-Lõuna tn             KESKLINN - Veerenni, Uus Maailm
Vana-Mustamäe tn          NÕMME - Nõmme, Hiiu, Vana-Mustamäe
Vana-Posti tn             KESKLINN - Vanalinn (all-linn)
Vana-Pärnu maantee        NÕMME - Nõmme
Vana-Rannamõisa tee       HAABERSTI - Õismäe, Vismeistri, Pikaliiva
Vana-Tartu maantee        KESKLINN - Mõigu
Vanaturu kael             KESKLINN - Vanalinn (all-linn)
Vana-Umboja tn            HAABERSTI - Kakumäe
Vana-Veerenni tn          KESKLINN - Veerenni
Vana-Viru tn              KESKLINN - Vanalinn
Vanemuise põik            NÕMME - Kivimäe, Hiiu
Vanemuise tn              NÕMME - Kivimäe, Hiiu
Vaniku tn                 PÕHJA-TALLINN - Pelgulinn
Varbola tn                NÕMME - Kivimäe, Pääsküla
Varese tn                 KRISTIINE - Lilleküla (Mooni)
Variku tee                PIRITA - Mähe
Varju tee                 PIRITA - Mähe
Varjulille tee            PIRITA - Mähe (aedlinn)
Varraku tn                LASNAMÄE - Laagna, Tondiraba
Varre tn                  KESKLINN - Veerenni
Varsaallika tn            PIRITA - Kose (Varsaallika)
Vasara tn                 PÕHJA-TALLINN - Kopli
Vase tn                   KESKLINN - Raua
Vati tn                   KESKLINN - Mõigu
Vedru tn                  LASNAMÄE - Sõjamäe
Veduri tn                 KESKLINN - Luite
Vee tn                    KESKLINN - Luite
Veerenni põik             KESKLINN - Luite
Veerenni tn               KESKLINN - Veerenni, Luite
Veeriku tee               PIRITA - Kose
Veerise tn                HAABERSTI - Vismeistri
Veetorni tn               KESKLINN - Tõnismäe
Vene tn                   KESKLINN - Vanalinn (all-linn)
Versta tn                 NÕMME - Nõmme
Vesikaare tn              NÕMME - Kivimäe, Pääsküla
Vesilennuki tn            PÕHJA-TALLINN - Kalamaja
Vesioina tn               NÕMME - Vana-Mustamäe
Vesiravila tn             HAABERSTI - Mustjõe
Vesiveski tn              PIRITA - Kose
Vesivärava tn             KESKLINN - Kadriorg, Torupilli
Veski tn                  KESKLINN - Keldrimäe
Veskilise tn              HAABERSTI - Veskimetsa
Veskimetsa tn             HAABERSTI, KRISTIINE - Mustjõe, Lilleküla (Marja)
Veskimäe tn               HAABERSTI - Veskimetsa
Veskiposti tn             KESKLINN - Juhkentali
Vesse põik                LASNAMÄE - Sõjamäe
Vesse tn                  LASNAMÄE - Sõjamäe
Vete tn                   NÕMME - Vana-Mustamäe
Viadukti tn               KESKLINN - Luite
Vibu tn                   PÕHJA-TALLINN - Kalamaja
Videviku tn               KESKLINN - Uus Maailm
Vigla tn                  HAABERSTI - Pikaliiva
Vihu tn                   HAABERSTI - Pikaliiva
Vihuri tn                 PÕHJA-TALLINN - Pelguranna
Viidika tn                HAABERSTI - Kakumäe
Viige tn                  HAABERSTI - Vismeistri
Viimsi põik               PIRITA - Merivälja
Viimsi tee                PIRITA - Merivälja
Eduard Viiralti tn        KESKLINN - Kompassi
Viirpuu tee               PIRITA - Merivälja
Vikerkaare tn             NÕMME - Pääsküla
Vikerlase tn              LASNAMÄE - Laagna
Eduard Vilde tee          MUSTAMÄE - Mustamäe
Vilisuu tn                LASNAMÄE - Laagna
Viljandi maantee          NÕMME, KESKLINN - Liiva, Kitseküla, Raudalu
Villardi tn               KESKLINN - Kassisaba, Uus Maailm
Villkäpa tn               PIRITA - Lepiku
Jüri Vilmsi tn            KESKLINN - Kadriorg, Raua, Torupilli
Vilu tee                  PIRITA - Mähe
Vimma tn                  HAABERSTI - Kakumäe
Vindi tn                  KRISTIINE - Lilleküla (Linnu)
Vineeri tn                KESKLINN - Uus Maailm, Veerenni
Vinkli tn                 MUSTAMÄE - Kadaka
Virbi tn                  LASNAMÄE - Laagna
Virmalise tn              KESKLINN - Uus Maailm
Viru tn                   KESKLINN - Vanalinn (all-linn), Vanalinn
Viru väljak               KESKLINN - Südalinn, Vanalinn, Sadama
Virve tn                  KRISTIINE - Järve
Visase tn                 LASNAMÄE - Sõjamäe
Vismeistri tn             HAABERSTI - Vismeistri
Viu tn                    KRISTIINE - Lilleküla (Linnu)
Volta tn                  PÕHJA-TALLINN - Kalamaja
Voo tn                    NÕMME - Rahumäe, Nõmme
Voolu tn                  NÕMME - Kivimäe
Voorimehe tn              KESKLINN - Vanalinn (all-linn)
Vormsi tn                 LASNAMÄE - Kuristiku
Vuti tn                   KRISTIINE - Lilleküla (Mooni)
Võidu põik                NÕMME - Männiku
Võidu tn                  NÕMME - Liiva, Rahumäe, Männiku
Võidujooksu tn            LASNAMÄE - Pae, Sikupilli, Kurepõllu
Võistluse tn              KESKLINN - Juhkentali
Võlvi tn                  KESKLINN - Keldrimäe
Võra tee                  PIRITA - Merivälja
Võrgu tn                  PÕHJA-TALLINN - Kalamaja
Võrgukivi tn              HAABERSTI - Kakumäe
Võrse tn                  KRISTIINE - Lilleküla (Linnu)
Võru tn                   LASNAMÄE - Laagna
Võsa tee                  PIRITA - Mähe
Võsara tn                 HAABERSTI - Pikaliiva
Võsu tn                   NÕMME - Nõmme
Võtme tn                  KESKLINN - Veerenni
Vähi tn                   HAABERSTI - Kakumäe, Vismeistri
Väike tn                  NÕMME - Rahumäe, Nõmme
Väike-Ameerika tn         KESKLINN - Uus Maailm
Väike-Karja tn            KESKLINN - Vanalinn (all-linn), Vanalinn
Väike-Kloostri tn         KESKLINN - Vanalinn (all-linn)
Väike-Laagri tn           PÕHJA-TALLINN - Kalamaja
Väike-Männiku tn          NÕMME - Männiku
Väike-Paala tn            LASNAMÄE - Ülemiste
Väike-Patarei tn          PÕHJA-TALLINN - Kalamaja
Väike-Pääsukese tn        KESKLINN - Maakri
Väike Rannavärav          KESKLINN - Vanalinn
Väikese Illimari tn       NÕMME - Rahumäe
Väike-Sõjamäe tn          LASNAMÄE - Ülemiste, Sõjamäe
Väina tee                 PIRITA - Merivälja
Välgu tn                  HAABERSTI - Mustjõe
Välja tn                  KRISTIINE - Lilleküla (Mooni)
Väo tee                   LASNAMÄE - Väo
Väomurru tn               LASNAMÄE - Väo
Värava tn                 NÕMME - Liiva
Värsi tn                  NÕMME - Kivimäe
Värvi tn                  KRISTIINE - Lilleküla (Marja)
Västra tn                 HAABERSTI - Vismeistri
Västriku tn               KRISTIINE - Tondi
Vääna tn                  NÕMME - Hiiu
Vööri tn                  KESKLINN - Sadama

August Weizenbergi tn     KESKLINN - Kadriorg
Ferdinand Johann Wiedemanni tn | KESKLINN - Kadriorg
Wismari tn                KESKLINN - Kassisaba, Vanalinn

Õhtu tn                   NÕMME - Pääsküla
Õie põik                  NÕMME - Nõmme, Rahumäe
Õie tn                    NÕMME - Nõmme
Õilme tn                  KESKLINN - Veerenni
Õismäe tee                HAABERSTI - Väike-Õismäe
Õitse tn                  NÕMME - Pääsküla
Õle tn                    PÕHJA-TALLINN - Pelgulinn
Õllepruuli tn             KESKLINN - Tõnismäe
Õnne tn                   NÕMME - Liiva
Õpetajate tn              KESKLINN - Veerenni
Õuna tn                   NÕMME - Hiiu

Ädala tn                  PÕHJA-TALLINN - Pelgulinn
Äigrumäe tee              PIRITA - Lepiku
Äkke tn                   HAABERSTI - Pikaliiva
Ääre tn                   NÕMME - Vana-Mustamäe
Ääsi tn                   LASNAMÄE - Ülemiste

Ööbiku tn                 KRISTIINE - Tondi
Öölase tn                 PIRITA - Lepiku

Ülase tn                  KRISTIINE - Lilleküla (Lille)
Ülemiste tee              LASNAMÄE - Ülemiste
Üliõpilaste tee           MUSTAMÄE, NÕMME - Mustamäe, Vana-Mustamäe
Ümera tn                  LASNAMÄE - Seli
"""


LAST_NAMES_ESTONIA = u"""
Ivanov	6789
Tamm	5241
Saar	4352
Sepp	3624
Mägi	3613
Smirnov	3402
Vasiliev	3153
Petrov	2937
Kask	2847
Kukk	2728
Kuznetsov	2339
Rebane	2265
Ilves	2165
Mihhailov	1968
Pärn	1 933
Pavlov	1 927
Semenov	1 909
Koppel	1 882
Andrejev	1 862
Aleksejev	1 845
Luik	1 826
Kaasik	1 817
Lepik	1 814
Oja	1 809
Raudsepp	1 775
Kuusk	1 747
Karu	1 704
Fjodorov	1 685
Nikolaev	1 675
Kütt	1 646
Põder	1 628
Vaher	1 614
Popov	1 611
Stepanov	1 592
Volkov	1 590
Moroz	1 573
Lepp	1 564
Koval	1 559
Kivi	1 531
Kallas	1 525
Kozlov	1 463
Mets	1 455
Sokolov	1 446
Liiv	1 426
Grigorieva	1 424
Jakovlev	1 422
Kuusik	1 384
Teder	1 381
Lõhmus	1 368
Laur	1 360
Jõgi	1 359
Kangur	1 337
Peterson	1 285
Lebedev	1 275
Kõiv	1 271
Kull	1 269
Ots	1 242
Leppik	1 226
Dmitriev	1 225
Nikitin	1 222
Mölder	1 214
Jegorov	1 210
Toom	1 201
Puusepp	1 181
Orlov	1 149
Raud	1 130
Kuzmin	1 122
Aleksandrov	1 089
Orav	1 086
Sild	1 084
Novikov	1 070
Bogdanov	1 062
Rand	1 053
Jakobson	1 039
Makarov	1 015
Nõmm	1 010
Põld	1 010
Sarapuu	1 004
Uibo	1 000
Paju	998
Mitt	997
Männik	961
Zaitsev	960
Antonov	956
Laas	951
Jürgenson	944
Saks	944
Järv	942
Vinogradov	940
Filippov	930
Johanson	929
Pukk	920
Tomson	919
Kalda	917
Belov	915
Romanov	911
Melnik	907
Allik	905
Solovjov	905
Sergejev	891
Tamme	877
Kruus	873
Mark	870
Aas	867
Rätsep	867
Gusev	866
Maksimov	866
Paas	860
Mänd	853
Hein	852
Roos	849
Parts	847
Kase	826
Väli	826
Järve	825
Lind	823
Mõttus	821
Palm	819
Rohtla	812
Timofejev	804
Valk	797
Hunt	794
Unt	781
Adamson	775
Pihlak	766
Iljin	759
Nurk	755
Baranov	742
Lember	736
Frolov	734
Gavrilov	732
Sikk	731
Kuus	730
Kala	722
Õunapuu	720
Pärna	716
Soosaar	712
Zahharov	706
Vares	703
Tsvetkov	696
Arro	695
Vorobjov	695
Aavik	690
Kurg	690
Sorokin	688
Tali	688
Vahtra	686
Jefimov	684
Vahter	682
Varik	678
Kalinin	673
Kolesnik	672
Mikk	668
Aru	663
Matvejev	661
Trofimov	657
Kikas	652
Õun	652
Luts	650
Roots	644
Tõnisson	641
Kolk	634
Lill	634
Must	631
Piir	631
Kallaste	626
Kurvits	625
Maripuu	622
Poljakov	622
Jänes	621
Golubev	618
Sidorov	618
Mäe	615
Nikiforov	614
Kirs	609
Kangro	605
Korol	605
Maasik	601
Kokk	597
Borissov	593
Kaur	590
Tomingas	590
Koort	581
Tammik	580
Fedorov	573
Müür	573
Danilov	566
Toomsalu	566
Martin	564
Susi	563
Ploom	560
Liiva	555
Hallik	554
Tarassov	553
Fomin	550
Tilk	550
Uustalu	550
Michelson	549
Valge	548
Tihhomirov	545
Miller	543
Kulikov	541
Toots	541
Vaino	541
Nõmmik	540
Talts	540
Jürgens	538
Kikkas	538
Kesküla	537
Anton	536
Post	535
Beljajev	532
Kärner	530
Martinson	530
Hansen	529
Rüütel	527
Veski	527
Rumjantsev	526
Mironov	525
Müürsepp	525
Meier	524
Ossipov	524
Sarv	518
Palu	517
Žukov	516
Aasa	513
Laanemets	512
Nazarov	511
Krõlov	509
Žuravljov	507
Titov	507
Juhkam	506
Luht	506
Jalakas	505
Kivistik	505
Karro	503
Annus	502
Rosenberg	501
Fedotov	499
Lääne	499
Viira	499
Jõesaar	497
Tooming	497
Komarov	492
Soo	491
Ott	488
Simson	485
Kotkas	483
Malõšev	482
Kink	478
Anderson	477
Toome	477
Kirillov	476
Aus	475
Ruus	474
Saare	473
Erm	471
Lang	471
Olesk	471
Afanasjev	468
Pettai	468
Reimann	467
Tuisk	467
Kriisa	465
Ojala	465
Kroon	463
Raag	462
Raid	462
Bõstrov	461
Org	461
Lauri	460
Laan	456
Pärtel	456
Taal	456
Kadak	455
Sander	455
Kattai	454
Truu	454
Konovalov	453
Sirel	453
Liivak	451
Raja	449
Abel	448
Siim	448
Männiste	445
Lipp	443
Kisseljov	440
Medvedev	440
Meister	440
Abramov	439
Kazakov	439
Sutt	439
Saveljev	438
Filatov	437
Soots	436
Schmidt	434
Gerassimov	432
Kotov	432
Allas	431
Ivask	429
Täht	429
Loginov	428
Juhanson	426
Kiik	425
Leht	425
Saul	425
Kasemets	421
Ševtšenko	421
Sobolev	420
Lass	419
Härm	418
Kont	415
Jeršov	414
Vlassov	414
Maslov	413
Konstantinov	411
Pruul	411
Teras	411
Visnapuu	411
Aun	409
Pajula	407
Gromov	406
Kool	406
Silm	406
Tamberg	406
Lumiste	402
Kirsipuu	401
Kirss	401
Kudrjavtsev	401
Sööt	401
Kalmus	400
Sokk	399
Kalm	398
Koit	398
Oras	398
Suits	398
Laine	396
Sulg	396
Põldma	395
Vaht	394
Klimov	391
Lukk	391
Randmaa	391
Gontšarov	389
Kiis	388
Paal	388
Võsu	388
Uus	387
Jaakson	386
Lillemets	385
Mürk	383
Tiits	382
Jaanus	381
Link	381
Erik	379
Lokk	379
Randoja	379
Bondarenko	378
Drozdov	377
Lehtmets	377
Voronin	377
Kuningas	376
Laane	376
Lumi	375
Salu	375
Lomp	372
Pent	372
Laks	370
Jermakov	369
Salumäe	369
Kutsar	368
Madisson	366
Koger	365
Muru	365
Niit	365
Põllu	365
Vähi	365
Kaljula	364
Viks	364
Nõmme	363
Urb	362
Nuut	361
Kaljuvee	360
Piho	359
Piirsalu	359
Sillaste	359
Arula	358
Kondratjev	357
Tuulik	357
Alas	356
Eller	356
Kostin	356
Käsper	356
Pikk	356
Salumets	356
Jürisson	355
Kruglov	355
Liivamägi	355
Hanson	354
Õispuu	354
Ignatjev	353
Kaljuste	352
Kiisk	351
Lehtla	351
Suvi	351
Gross	350
Poom	349
Egorov	348
Mäesalu	348
Davõdov	347
Lääts	347
Panov	347
Suvorov	347
Maidla	346
Mäeots	345
Põdra	345
Raidma	345
Teesalu	345
Holm	344
Loorits	344
Raamat	344
Liblik	343
Mändla	343
Štšerbakov	343
Lukin	342
Säde	342
Trei	342
Kaljurand	341
Kuuse	341
Kelder	339
Markus	339
Ader	338
Pärnpuu	338
Oks	337
Tuul	337
Gorbunov	336
Laht	336
Leis	336
Štšerbakov	335
Jaanson	334
Kasak	332
Zujev	332
Rosin	331
Heinsalu	330
Kivimäe	330
Naumov	330
Kapp	329
Kohv	329
Moor	327
Remmel	327
Treial	327
Klein	326
Pulk	326
Põldmaa	325
Kilk	324
Ojaste	323
Soosalu	323
Käärik	321
Paap	321
Sibul	321
Klaas	320
Kurm	320
Raadik	320
Safronov	320
Sarap	320
Treier	320
Reinsalu	319
Sillaots	318
Sisask	317
Soon	317
Tiik	317
Denissov	316
Kalamees	316
Jõe	315
Lätt	315
Karpova	313
Mandel	313
Kiil	312
Ernits	311
Kasemaa	311
Vain	311
Villemson	311
Suur	310
Heinsoo	309
Pihelgas	309
Roosileht	308
Aasmäe	306
Koitla	306
Lehiste	306
Merila	306
Vill	306
Nurm	304
Viik	304
Kass	303
Käär	303
Teearu	302
Anissimov	301
Karpov	300
Kivilo	300
Püvi	300
Lehismets 1
"""

FEMALE_FIRST_NAMES_ESTONIA = u"""
Adeele
Age
Age-Kaie
Aili
Aili
Aino
Aino
Aive
Aleksandra
Alla
Allar
Angeelika
Angela
Ann
Anna-Merike
Anne
Anne
Anne
Anne
Anne
Anne
Anneli
Anneli
Anneli
Anneli
Annely
Anni
Annika
Annika
Annika
Anu
Anu
Asta
Astra
Astrid
Astrid
Ave
Brigitte
Cathy
Clara
Claudine
Cris
Ebe
Eda
Edda
Eevi
Egle
Eha
Eha
Eike
Elis
Elisa
Eloliis
Emily
Ene
Ene
Eneli
Epp
Eva-Liisa
Eve
Eve
Eve
Eveli
Evely
Evi
Fatima
Florinda
Gabrielle
Grete
Halliki
Hedi
Hedi
Heidi
Helbe
Helen
Helena
Helena
Helgi
Heli
Heli
Heli
Helja
Heljo
Helju
Helve
Helyn
Iiris
Ija
Ilme
Ilona
Ilona
Imbi
Inge
Jaanika
Jana
Jana
Jana
Janika
Jenifer
Judith
Julia
Julia
Juta
Kaari
Kadi
Kadri
Kadri
Kadri
Kai
Kaia
Kaidi
Kaija
Kaili
Kaily
Kaja
Karin
Karolina
Katarina
Katerina
Kati
Kati
Katri
Katri
Katrin
Katrin
Katrin
Katrin
Kelli
Kendra
Kerle
Kersti
Kersti
Kersti
Kersti
Kersti
Kerstin
Kertu
Kirsti
Krista
Krista
Krista
Krista
Kristel
Kristel
Kristel
Kristel
Kristel
Kristel
Kristi
Kristiina
Kristiina
Kristiina
Kristin
Kristina
Kuma
Kärolin
Kärt
Kätlin
Kätlin
Kätlin
Kätlin
Küllike
Külliki
Külliki
Kyllikki
Laine
Laura
Lea
Lehte
Leili
Lia
Liesel
Liia
Liina
Liina
Liina
Liis
Liisa
Liisa
Liivi
Lili
Linda
Linda
Loone
Luule
Ly
Lya
Maarika
Maarja
Maarja
Madli
Madli
Mai
Maie
Maire
Malle
Mare
Mare
Maret
Margareta
Margi
Margit
Margus
Mari
Mari
Mari
Mari-Ann
Mari-Liis
Mari-Liis
Mari-Liis
Mari-Ly
Maria Joanna
Mariann
Marianne
Mariel
Marik
Mariliis
Marina
Marita
Marite
Marliese
Martti
Meeli
Meeli
Melissa
Merike
Merike
Merilin
Merilin
Merlin
Mery
Michelle
Milvi
Milvi
Mirjam
Mirjam
Nadia
Natalja
Nele
Nele
Paula
Petra
Pia
Pia
Piia
Pille-Riin
Piret
Piret
Piret
Piret
Ragne
Ragne
Raili
Reet
Riia
Riina
Riina
Rita
Rita
Rita
Ruth
Rutt
Rutt
Sadu
Saija
Sanna
Sass
Saule
Signe
Sigrid
Siina
Siiri
Siiri
Silja
Silja
Silja
Silvi
Sirle
Sophie
Stella
Teele
Teresa
Tiia
Tiina
Tiina
Tiina
Tiina
Tiina
Tiina
Tiiu
Tiiu
Titta
Triin
Triin
Triin
Triin
Triin
Triin
Triinu
Triinu
Triinu
Triinuly
Ulvi
Ursula
Urve
Valia
Veera
Veera
Veronika
Veronika
Viire
Viivi
Vilma
Vika
Virge
Virge
Virve
Õie
Ülle
Ülle
Ülle
"""


MALE_FIRST_NAMES_ESTONIA = u"""
Aadu
Aare
Aarne
Aaro
Aaron
Aaron
Ado
Ago
Ago
Ago
Ahti
Ain
Ainars
Aivar
Aivar
Aivar
Aivar
Alar
Alari
Albert
Allan
Ando
Andreas
Andreas
Andreas
Andres
Andres
Andres
Andres
Andres
Andres
Andres
Andri
Andrus
Andrus
Annar
Anti
Anti
Ants
Ants
Ants
Ants
Ants
Ants
Ardi
Argo
Argo
Arko
Armo
Arne
Arno
Artur
Arvo
Arvo
Arvo
Daniel
Diego
Eerik
Egert
Einar
Elmar
Enn
Enn
Enn
Enno
Enno
Erich
Erik
Fabio
Falko
Filip
Fred
Frédéric
Frederik
Gabriel
Gunnar
Hannes
Hannes
Hannes
Hannes
Harmo
Harri
Harri
Harri
Heino
Heinz
Helger
Henn
Henry
Hillar
Ilmar
Imre
Imre
Imre
Indrek
Indrek
Indrek
Indrek
Ivar
Ivo
Jaak
Jaak
Jaak
Jaan
Jaan
Jaan
Jaan
Jaan
Jaan
Jaan
Jaan
Jaanus
Jaanus
Janari
Janek
Jasper
Johannes
Joonas
Joosep
Juhan
Jüri
Jüri
Jürmo
Kahro
Kaido
Kaimo
Kalev
Kalev
Kalmer
Kardo
Karl Villem
Karla
Karlis
Kaur
Kenert
Klaus
Kristjan
Kristjan
Kristo
Kristo
Kristofer
Kristofer
Laurenz
Lehari
Lembit
Leo
Leo
Maarjo
Madis
Madis
Mads
Mairold
Manfred
Marek
Marek
Margo
Margus
Margus
Marko
Mart
Mart
Mart
Martel
Martin
Martti
Martti
Mati
Mati
Mati
Mati
Mati
Matthias
Meeli
Meelis
Meelis
Meelis
Michael
Michael
Mihkel
Mihkel
Mihkel
Mikk
Mikk
Olev
Oliver
Oliver
Oliver
Ott
Otto
Patrick
Patrik
Peeter
Peeter
Peter
Priit
Priit
Priit
Priit
Ragnar
Raigo
Raivu
Raivu
Rannes
Ranno
Raphael
Rasmus
Raul
Raul
Rauno
Rauno
Reemet
Reet
Rein
Rein
Rein
Riho
Risto
Roland
Ruudi
Sander
Sander
Sander
Sandor
Siim
Silver
Simon
Suigu
Sulev
Sulev
Sulo
Sune
Taavi
Taavi
Taivu
Tanel
Tarmo
Tarmo
Tarvo
Tarvo
Tauno
Tero
Tiit
Tiit
Tiit
Timo
Toivo
Toivo
Toivo
Toivo
Toomas
Toomas
Tõnis
Tõnis
Tõnis
Tõnu
Udo
Urmas
Urmas
Urmas
Urmas
Urmo
Urmo
Vahur-Paul
Vaiko
Valdo
Veiko
Veiko
Velio
Vello
Villu
Virgo
William
William
Ülo
"""


def streets_of_tallinn():
    POS = 25

    for ln in STREETS_OF_TALLINN.splitlines():
        if ln and ln[0] != '#':
            if '|' in ln:
                street, where = ln.split('|')
            else:
                street = ln[:POS]
                where = ln[POS:]
            street = street.strip()
            where = where.strip()
            linnaosa = where.split(' - ')[0].strip()
            if ',' in linnaosa:
                linnaosa = linnaosa.split(',')[0].strip()

            def convert(s):
                if s == "PÕHJA-TALLINN": return "Põhja-Tallinn"
                if s == "NÕMME": return "Nõmme"
                if s == "MUSTAMÄE": return "Mustamäe"
                if s == "LASNAMÄE": return "Lasnamäe"
                if s == "KESKLINN": return "Kesklinn"
                if s == "PIRITA": return "Pirita"
                return s
            linnaosa = convert(linnaosa)

            yield (street, linnaosa)


LAST_NAMES_ESTONIA = Cycler(splitter3(LAST_NAMES_ESTONIA))
MALE_FIRST_NAMES_ESTONIA = Cycler(splitter1(MALE_FIRST_NAMES_ESTONIA))
FEMALE_FIRST_NAMES_ESTONIA = Cycler(splitter1(FEMALE_FIRST_NAMES_ESTONIA))


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
