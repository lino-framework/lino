# -*- coding: Latin-1 -*-
# based on Dirk Holtwick
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/355807

import zlib

_guesser = None

class Entropy:

    def __init__(self):
        self.entro = []

    def register(self, name, corpus):
        """
        register a text as corpus for a language or author.
        <name> may also be a function or whatever you need
        to handle the result.
        """
        corpus = str(corpus)
        ziplen = len(zlib.compress(corpus))
        self.entro.append((name, corpus, ziplen))

    def guess(self, part):
        """
        <part> is a text that will be compared with the registered
        corpora and the function will return what you defined as
        <name> in the registration process.
        """
        what = None
        diff = 0
        part = str(part)
        for name, corpus, ziplen in self.entro:
            nz = len(zlib.compress(corpus + part)) - ziplen
            # print name, nz, ziplen, nz-ziplen, (1.0 * (nz-ziplen)) / len(part)
            if diff==0 or nz<diff:
                what = name
            diff = nz
        return what


def guesslang(x):
    global _guesser
    if _guesser is None:
        _guesser = Entropy()
    
        _guesser.register("en","""If you ever wrote a large shell
        script, you probably know this feeling: you'd love to add yet
        another feature, but it's already so slow, and so big, and so
        complicated; or the feature involves a system call or other
        function that is only accessible from C ...Usually the problem
        at hand isn't serious enough to warrant rewriting the script
        in C; perhaps the problem requires variable-length strings or
        other data types (like sorted lists of file names) that are
        easy in the shell but lots of work to implement in C, or
        perhaps you're not sufficiently familiar with C.  """)

        _guesser.register("de","""
        Über spirito (http://www.spirito.de) Die spirito GmbH mit Sitz
        in Duisburg ist Dienstleister im Bereich maßgeschneiderte
        Programmierung für Internet und Intranet sowie Hersteller von
        Software für Content Management, Groupware, E-Learning und
        Online Shops.  Unsere Philosophie Wenn Sie uns mit einem
        Projekt beauftragen, so sollen Sie dabei nicht nur ein «Gutes
        Gefühl» haben, Sie sollen sich wohlfühlen! Die Anwendung
        unserer Software soll Leichtigkeit vermitteln, Freude, Witz
        und Geist versprühen. Daher nennen wir uns «spirito», was im
        Italienischen soviel bedeutet wie Geist / Witz /
        Kreativität. Unsere Produkte haben wir nach italienischen
        Städten benannt, weil wir denken, dass das allein schon eine
        gewisse Leichtigkeit vermittelt. Diese Produkte liefern so
        manche Vorlage für die Ausgestaltung konkreter
        Projekte. Aufgrund der sehr hohen Flexibilität aller unserer
        Produkte fällt uns die punktgenaue Anpassung unserer Produkte
        an Ihre Wünsche besonders leicht. Schließlich sollen es auch
        diejenigen, die nachher damit arbeiten müssen besonders leicht
        haben.  Die schweren und die langweiligen Dinge wollen wir so
        weit wie möglich der Software überlassen ...  """)


        _guesser.register("et","""
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
        “Klassikalist aeda, mis oli valdav pärast sõda ning kus oli
        eraldi juur- ja puuviljaaed ning pisike iluaed, enam ei
        rajata,” räägib Aaspõllu, kes on seotud 1990ndatel
        president Lennart Meri eestvedamisel taastatud üle-eestilise
        kauni koduaia konkursiga.
        """)

    return _guesser.guess(x)



if __name__=="__main__":

    # Test some probes

    print "DEUTSCH", guesslang(""" Laut Kundenaussagen ist XYZ unter
    Windows 95 A und B sowie unter Windows NT einsatzfähig. Leider
    kann von unserer Seite aus unter diesen Betriebssystemen kein
    umfassender Support gewährleistet werden.  """)

    print "ENGLISH", guesslang(""" Now that you are all excited about
    Python, you'll want to examine it in some more detail. Since the
    best way to learn a language is using it, you are invited here to
    do so.  """)

