# -*- coding: Latin-1 -*-

## Copyright 2005-2006 Luc Saffre 

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

# based on a recipe by Dirk Holtwick:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/355807

import sys
import zlib

_guesser = None

class Entropy:
    
    #encoding='utf-8'
    encoding=sys.getfilesystemencoding()

    def __init__(self):
        self.entro = []

    def register(self, name, corpus):
        """
        register a text as corpus for a language or author.
        <name> may also be a function or whatever you need
        to handle the result.
        """
        corpus=corpus.encode(self.encoding)
        ziplen=len(zlib.compress(corpus))
        self.entro.append((name, corpus, ziplen))

    def guess(self, part):
        """
        <part> is a text that will be compared with the registered
        corpora and the function will return what you defined as
        <name> in the registration process.
        """
        what = None
        diff = 0
        part = part.encode(self.encoding)
        for name, corpus, ziplen in self.entro:
            nz = len(zlib.compress(corpus+part))-ziplen
            #print name, nz, ziplen, nz-ziplen, (1.0 * (nz-ziplen)) / len(part)
            if diff==0 or nz<diff:
                what=name
                diff=nz
                
        return what


def guesslang(x):
    global _guesser
    if _guesser is None:
        _guesser = Entropy()
    
        _guesser.register("en","""

If you ever wrote a large shell script, you probably know this
feeling: you'd love to add yet another feature, but it's already so
slow, and so big, and so complicated; or the feature involves a system
call or other function that is only accessible from C ...Usually the
problem at hand isn't serious enough to warrant rewriting the script
in C; perhaps the problem requires variable-length strings or other
data types (like sorted lists of file names) that are easy in the
shell but lots of work to implement in C, or perhaps you're not
sufficiently familiar with C.


        """)

## In the beginning God created the heavens and the earth.  Now the
## earth was formless and empty, darkness was over the surface of the
## deep, and the Spirit of God was hovering over the waters.  And God
## said, "Let there be light," and there was light. God saw that the
## light was good, and He separated the light from the darkness.  God
## called the light "day," and the darkness he called "night." And
## there was evening, and there was morning—the first day.  And God
## said, "Let there be an expanse between the waters to separate water
## from water." So God made the expanse and separated the water under
## the expanse from the water above it. And it was so. God called the
## expanse "sky." And there was evening, and there was morning—the
## second day.  And God said, "Let the water under the sky be gathered
## to one place, and let dry ground appear." And it was so. God called
## the dry ground "land," and the gathered waters he called "seas."
## And God saw that it was good.  Then God said, "Let the land produce
## vegetation: seed-bearing plants and trees on the land that bear
## fruit with seed in it, according to their various kinds." And it
## was so. The land produced vegetation: plants bearing seed according
## to their kinds and trees bearing fruit with seed in it according to
## their kinds. And God saw that it was good. And there was evening,
## and there was morning—the third day.

        



        _guesser.register("de",u"""
        
Über spirito (http://www.spirito.de) Die spirito GmbH mit Sitz in
Duisburg ist Dienstleister im Bereich maßgeschneiderte Programmierung
für Internet und Intranet sowie Hersteller von Software für Content
Management, Groupware, E-Learning und Online Shops.  Unsere
Philosophie Wenn Sie uns mit einem Projekt beauftragen, so sollen Sie
dabei nicht nur ein «Gutes Gefühl» haben, Sie sollen sich wohlfühlen!
Die Anwendung unserer Software soll Leichtigkeit vermitteln, Freude,
Witz und Geist versprühen. Daher nennen wir uns «spirito», was im
Italienischen soviel bedeutet wie Geist / Witz / Kreativität. Unsere
Produkte haben wir nach italienischen Städten benannt, weil wir
denken, dass das allein schon eine gewisse Leichtigkeit
vermittelt. Diese Produkte liefern so manche Vorlage für die
Ausgestaltung konkreter Projekte. Aufgrund der sehr hohen Flexibilität
aller unserer Produkte fällt uns die punktgenaue Anpassung unserer
Produkte an Ihre Wünsche besonders leicht. Schließlich sollen es auch
diejenigen, die nachher damit arbeiten müssen besonders leicht haben.
Die schweren und die langweiligen Dinge wollen wir so weit wie möglich
der Software überlassen ...

        """)


        _guesser.register("et",u"""
        Iluaed tõuseb, kapsamaa langeb
        14.04.2005 Annika Poldre, Sirje Pärismaa, Merike Pitk
        Kuigi elukutseliste põllumeeste arv on tänases Eestis väike,
        panevad uskumatult paljud meist kevadel sõrmed mulda. Kahanema
        kippuva köögiviljanduse ja marjanduse asemel võidab üha uusi
        harrastajaid iluaiandus.
        Eestlase koduaed teeb läbi suuri muudatusi. Suund on
        iluaiandusele, viljapuid pannakse vähe kasvama, kinnitab Eesti
        Dendroloogia Seltsi president Aino Aaspõllu. Eelkõige Tallinna
        ümber, aga mujalgi tekkinud aiandusfirmad ja puukoolid püsivad
        hästi konkurentsis, laienevad ning suurendavad kauba
        sortimenti. Enamik neist müüb importtaimi ja
        -istikuid. Ostjaid jätkub.  foto: Raivo Tasso Pensionär Arno
        Kaup eelistab turult ostmise asemel ise köögivilju kasvatada.
        Klassikalist aeda, mis oli valdav pärast sõda ning kus oli
        eraldi juur- ja puuviljaaed ning pisike iluaed, enam ei
        rajata, räägib Aaspõllu, kes on seotud 1990ndatel
        president Lennart Meri eestvedamisel taastatud üle-eestilise
        kauni koduaia konkursiga.
        """)

        # Eric Brasseur: Les impostures
        # http://www.lulu.com/content/255713
        _guesser.register("fr",u"""

Le canon du bonheur est peut-être un bébé cajolé par sa maman.  Ses
besoins sont simples et très forts. Sa maman souriante est toute
entière disponible pour s'occuper de lui.

Peut-on retrouver ce bonheur à l'âge adulte? Oui, sans doute : après
une belle et bonne journée de travail, quand votre amoureux ou votre
amoureuse, le regard empli d'estime, vous passe la main dans les
cheveux... Pour recevoir du bonheur, le bébé se contente de hurler ou
de faire risette. Quand on est adulte, le bonheur se mérite à force de
travail et d'apprentissages. C'est cela, la maturité.

Suffirait-il que chaque humain soit mature pour que l'humanité vive
heureuse? Votre patron mesquin et votre épouse boudeuse indiquent que
ce modeste objectif n'est pas encore atteint.

Suis-je un imposteur, pour parler du bonheur de façon aussi simpliste?
Sans doute... Je prétend néanmoins que les véritables imposteurs sont
ceux qui ne sont pas devenus adultes. Ils sont restés bloqués dans une
ornière de l'enfance. Le malheur vient des adultes infantiles.

        """)
        #print [(name, ziplen)
        #       for name, corpus, ziplen
        #       in _guesser.entro]
    return _guesser.guess(x)



