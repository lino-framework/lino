# -*- coding: Latin-1 -*-
## Copyright 2005 Luc Saffre

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

from lino.misc.tsttools import TestCase, main
from lino.tools.guesslang import guesslang


class Case(TestCase):
    def test01(self):
        
        self.assertEqual("de",guesslang(u"""
        Laut Kundenaussagen ist XYZ unter Windows 95 A und B sowie
        unter Windows NT einsatzfähig. Leider kann von unserer Seite
        aus unter diesen Betriebssystemen kein umfassender Support
        gewährleistet werden."""))
        
        self.assertEqual("en",guesslang(u"""
        Now that you are all excited about Python, you'll want to
        examine it in some more detail. Since the best way to learn a
        language is using it, you are invited here to do so.  """))
        
        self.assertEqual("et",guesslang(u"""
        Paavstivalimine on Vatikani jaoks äärmiselt tähendusrikas
        protseduur, kuid läbi sajandite on ikka ja jälle ette tulnud,
        et konklaav toob palju lisasekeldusi või midagi läheb viltu.
        """))
        
        self.assertEqual("et",guesslang(u"""
        Rooma suvekuumuses on konklaavi sisenenud kardinalid
        vedelikupuuduse tõttu minestanud ja mõned on saanud
        südamerabanduse. Uudiste-agentuuri AP järgi otsustati
        1274. aastal, et kardinalid võivad konklaavis nii hääletada
        kui ka süüa ja magada, sest eelmise paavsti valimised olid
        kestnud enam kui kolm aastat.  
        """))

        # source: http://www.france.attac.org/IMG/pdf/attacinfo545.pdf
        self.assertEqual("fr",guesslang(u"""

1.- LES ROIS SOIGNAIENT LES ECROUELLES

à propos du Chikungunya, par Raphaël Monticelli, 14 mars 2006 Les
épidémies sont choses terribles. Et notre époque a les siennes qui
nous laissent trop souvent aussi démunis que les pestes, grippes ou
choléras du passé. Les efforts que nous faisons pour lutter contre
elles sont souvent dérisoires. Parfois ils sont tragiques. Des
populations entières souffrent. On annonce des milliers, des centaines
de milliers de morts. On sait que la souffrance des mourants est
multipliée par celle des survivants, par la douleur et l'angoisse
des familles, des proches, et de nous tous, amis, connus et inconnus,
dans la simple solidarité des hommes et des femmes. Et nous avons bien
conscience que nous devons tout faire pour lutter contre ces
fléaux. Et nous avons bien conscience que nous ne faisons pas tout. Et
il faut tout faire, bien sûr, du raisonnable, en gardant raison. Il
faut tout faire, sans pourtant ajouter un mal à un mal.

Voici ce qu'on pouvait lire dans la presse ces jours-ci : Chikungunya
: une élue niçoise faxe son remède aux habitants de La Réunion 09-03
19:07:09 Une élue communiste de la ville de Nice suscite la polémique
pour avoir inondé l'Ile de la Réunion de fax vantant un traitement
personnel contre le chikungunya et avoir provoqué une ruée des
patients sur ce remède contesté par certains médecins, a-t-on appris
jeudi de sources concordantes.
        
        """))
        
        self.assertEqual("fr",guesslang(u"""
        Encore un essai.
        Il ne faut pas des textes trop courts.
        """))
        self.assertEqual("de",guesslang(u"Und noch ein Versuch."))
        self.assertEqual("et",guesslang(u"""
        Veel üks katse.
        Tekstid tõesti ei tohi olla liiga lühikesed.
        Muidu ta ütleb valesti.
        """))
        self.assertEqual("en",guesslang(u"Another test."))
    
if __name__ == '__main__':
    main()

