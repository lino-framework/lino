# coding: latin1
## Copyright 2003-2005 Luc Saffre

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

import os

from lino.misc.tsttools import TestCase, main

from lino.console import syscon

from lino.apps.keeper.keeper import Keeper, SearchFormCtrl
from lino.apps.keeper.tables import *

TESTDATA = os.path.join(
    os.path.dirname(__file__),"testdata")

class Case(TestCase):
    #todo="VolumeVisitor instance has no attribute 'reloading'"
    def test01(self):
        app=Keeper()
        sess=app.quickStartup() 
        
        q=sess.query(Volume)
        vol=q.appendRow(name="test",path=TESTDATA)
        vol.load(sess)
        sess.showQuery(
            vol.directories,
            columnNames="id name parent files subdirs",
            width=70)
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
Directories (volume=testparent=None)
====================================
id     |name          |parent        |files         |subdirs
-------+--------------+--------------+--------------+--------------
1      |              |              |17 Files      |2 Directories
""")
        q=sess.query(File,
                     orderBy="size",
                     columnNames="dir name size mustParse occurences")
        q.showReport(columnWidths="20 18 8 5 15")
        s=self.getConsoleOutput()
        #print s
        
        self.assertEquivalent(s,"""\
Files
=====
dir                 |name              |size    |mustP|occurences     
                    |                  |        |arse |               
--------------------+------------------+--------+-----+---------------
test:               |cp1252b.txt       |23      |X    |1 Occurences   
test:               |cp850b.txt        |23      |X    |1 Occurences   
test:2              |.cvsignore        |28      |X    |0 Occurences   
test:               |cp850box.txt      |50      |X    |0 Occurences   
test:webman         |1.txt             |138     |X    |19 Occurences  
test:2              |1.txt             |150     |X    |19 Occurences  
test:webman         |index.txt         |182     |X    |15 Occurences  
test:2              |index.txt         |193     |X    |21 Occurences  
test:               |cp1252a.txt       |372     |X    |53 Occurences  
test:               |cp850a.txt        |372     |X    |53 Occurences  
test:               |5.pds             |500     |X    |0 Occurences   
test:               |5b.pds            |676     |X    |0 Occurences   
test:textprinter    |5.PRN             |794     |X    |0 Occurences   
test:               |5d.pds            |850     |X    |0 Occurences   
test:webman         |init.wmi          |917     |X    |0 Occurences   
test:2              |init.wmi          |975     |X    |0 Occurences   
test:               |gnosis-readme     |1662    |X    |0 Occurences   
test:               |NAT.DBF           |1735    |X    |0 Occurences   
test:textprinter    |2.prn             |1798    |X    |0 Occurences   
test:               |5c.pds            |2027    |X    |0 Occurences   
test:               |README.TXT        |2254    |X    |263 Occurences 
test:textprinter    |1.prn             |2387    |X    |0 Occurences   
test:               |PAR.DBT           |4481    |X    |0 Occurences   
test:               |jona.txt          |7803    |X    |1382 Occurences
test:textprinter    |logo.jpg          |10126   |X    |0 Occurences   
test:               |PLZ.DBF           |25246   |X    |0 Occurences   
test:               |PAR.DBF           |43411   |X    |0 Occurences   
test:               |eupen.pdf         |232672  |X    |799 Occurences 
""")

        ctrl=SearchFormCtrl()
        sess.showForm(ctrl)
        
        s=self.getConsoleOutput()
        # print s
        self.assertEquivalent(s,"""\
&Words to look for: [None]
&any word (OR): [None]
[&Search]        
        """)
        
        ctrl.searchString.setValue("Stadt")
        ctrl.go.click()
        
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,u"""\
&Words to look for: [Stadt]
&any word (OR): [None]
[&Search]
Files where 'occurences' not empty
==================================
name                |occur|content                                 
                    |ences|                                        
--------------------+-----+----------------------------------------
eupen.pdf           |8    |Eupen aus Wikipedia, der freien         
                    |     |Enzyklopädie Eupen ( altfranzösisch Néau
                    |     |) ist die "Hauptstadt" der  (...)       
jona.txt            |8    |# source: http://theol.uibk.ac.at/lesera
                    |     |um/bibel/jona1.html  Die Berufung Jonas:
                    |     |1,1- 2          Jona 1,1         (...)  

        """)
        sess.shutdown()
        
        
if __name__ == '__main__':
    main()

