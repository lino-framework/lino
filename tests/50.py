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
        
##         Rooma suvekuumuses on konklaavi sisenenud kardinalid
##         vedelikupuuduse tõttu minestanud ja mõned on saanud
##         südamerabanduse. Uudiste-agentuuri AP järgi otsustati
##         1274. aastal, et kardinalid võivad konklaavis nii hääletada
##         kui ka süüa ja magada, sest eelmise paavsti valimised olid
##         kestnud enam kui kolm aastat.  """))
    
    
if __name__ == '__main__':
    main()

