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

from lino.misc.tsttools import TestCase, main, Toolkit

from lino.console import syscon

from lino.apps.keeper.keeper import Keeper
from lino.apps.keeper.tables import *

TESTDATA = os.path.join(
    os.path.dirname(__file__),"testdata")

class Case(TestCase):
    #todo="VolumeVisitor instance has no attribute 'reloading'"
    def test01(self):
        app=Keeper()
        sess=app.quickStartup() # toolkit=Toolkit())
        
        q=sess.query(Volumes)
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
1      |              |              |16 Files      |3 Directories
""")
        q=sess.query(Files,
                     orderBy="mtime",
                     columnNames="dir name mtime size")
        q.showReport(columnWidths="15 20 24 8")
        s=self.getConsoleOutput()
        #print s
        
        self.assertEquivalent(s,"""\
Files
=====
dir            |name                |mtime                   |size
---------------+--------------------+------------------------+--------
               |README.TXT          |Wed Jun 08 06:34:14 2005|2254
               |cp850b.txt          |Wed Jun 08 06:34:14 2005|23
               |cp1252b.txt         |Wed Jun 08 06:34:14 2005|23
               |cp1252a.txt         |Wed Jun 08 06:34:14 2005|372
               |gnosis-readme       |Wed Jun 08 06:34:15 2005|1662
               |cp850a.txt          |Wed Jun 08 06:34:15 2005|372
               |cp850box.txt        |Wed Jun 08 09:54:21 2005|50
               |NAT.DBF             |Wed Jun 08 10:05:21 2005|1735
               |PAR.DBF             |Wed Jun 08 10:10:15 2005|43411
               |PAR.DBT             |Wed Jun 08 10:10:19 2005|4481
               |5.pds               |Wed Jun 08 10:17:59 2005|500
               |5b.pds              |Wed Jun 08 10:18:06 2005|676
               |5c.pds              |Wed Jun 08 10:18:10 2005|2027
               |5d.pds              |Wed Jun 08 10:18:15 2005|850
webman         |init.wmi            |Wed Jun 08 10:32:44 2005|917
webman         |index.txt           |Wed Jun 08 10:32:44 2005|182
2              |init.wmi            |Wed Jun 08 10:32:44 2005|975
2              |index.txt           |Wed Jun 08 10:32:44 2005|193
2              |1.txt               |Wed Jun 08 10:32:44 2005|150
2              |.cvsignore          |Wed Jun 08 10:32:44 2005|28
webman         |1.txt               |Wed Jun 08 10:32:44 2005|138
               |ee_de.txt~          |Wed Jun 08 16:57:54 2005|72
               |PLZ.DBF             |Thu Jun 09 09:33:22 2005|25246
textprinter    |logo.jpg            |Thu Jun 09 10:21:04 2005|10126
textprinter    |5.prn~              |Thu Jun 09 10:21:04 2005|792
textprinter    |5.PRN               |Thu Jun 09 10:21:04 2005|794
textprinter    |2.prn               |Thu Jun 09 10:21:04 2005|1798
textprinter    |1.prn               |Thu Jun 09 10:21:05 2005|2387
timtools       |pds2pdf.help.txt    |Mon Jul 11 17:07:13 2005|953
timtools       |prn2pdf.help.txt    |Mon Jul 11 17:07:46 2005|868
timtools       |prnprint.help.txt   |Mon Jul 11 17:09:06 2005|1154
timtools       |sync.help.txt       |Mon Jul 11 17:09:18 2005|791
timtools       |diag.help.txt       |Mon Jul 11 17:09:37 2005|673
timtools       |openmail.help.txt   |Mon Jul 11 17:09:54 2005|955
timtools       |openurl.help.txt    |Mon Jul 11 17:10:03 2005|701
""")
        sess.shutdown()
        
        
if __name__ == '__main__':
    main()

