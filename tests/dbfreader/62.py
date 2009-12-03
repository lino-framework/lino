#coding: latin1
## Copyright 2003-2009 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
discovering and extending Lars M. Garshol's dbfreader.py
"""
import os
import unittest
from cStringIO import StringIO
from lino.utils import dbfreader

dataPath = os.path.dirname(__file__)

class Case(unittest.TestCase):
    
    def test01(self):
        f = dbfreader.DBFFile(os.path.join(dataPath,"NAT.DBF"),
                              codepage="cp850")

        ae = self.assertEqual
        ae(f.get_version(),"dBASE III")
        ae(f.has_memo(),False)
        ae(str(f.lastUpdate),"2003-01-22")
        ae(f.get_record_count(),14)
        ae(f.get_record_len(),94)
        #print get_fields(f)
        ae(get_fields(f),"""\
IDNAT: Character (3)
NAME: Character (40)
INTRA: Character (3)
IDLNG: Character (1)
IDTLF: Character (1)
TELPREFIX: Character (6)
TVAPREFIX: Character (3)
IDDEV: Character (3)
TVAPICT: Character (25)
ATTRIB: Character (5)
IDREG: Character (1)
ISOCODE: Character (2)""")
        
        s = "\n".join([rec["NAME"].strip() for rec in f.fetchall()])
        #print s
        ae(s,u"""\
Belgien
Luxemburg
Deutschland
Niederlande
Frankreich
Großbritannien
Italien
Irland
Spanien
Portugal
Schweiz
Österreich
Dänemark
United States of America""")

        
    def test02(self):
        f = dbfreader.DBFFile(os.path.join(dataPath,"PAR.DBF"),
                              codepage="cp850")
        
        ae = self.assertEqual
        ae(f.has_memo(),True)
        ae(f.get_version(),"dBASE III+ with memo")
        ae(f.get_record_count(),48)
        ae(f.get_record_len(),879)
        s = get_fields(f)
        ae(s,"""\
IDPAR: Character (6)
IDGEN: Character (6)
FIRME: Character (35)
NAME2: Character (35)
RUE: Character (35)
CP: Character (8)
IDPRT: Character (1)
PAYS: Character (3)
TEL: Character (18)
FAX: Character (18)
COMPTE1: Character (47)
NOTVA: Character (18)
COMPTE3: Character (47)
IDPGP: Character (2)
DEBIT: Character (10)
CREDIT: Character (10)
ATTRIB: Character (5)
IDMFC: Character (3)
LANGUE: Character (1)
PROF: Character (4)
CODE1: Character (12)
CODE2: Character (12)
CODE3: Character (12)
DATCREA: Date (8)
IDREG: Character (1)
ALLO: Character (35)
NB1: Character (60)
NB2: Character (60)
IDDEV: Character (3)
MEMO: Memo field (10)
COMPTE2: Character (47)
RUENUM: Character (4)
RUEBTE: Character (6)
MVPDATE: Date (8)
VORNAME: Character (20)
EMAIL: Character (250)
GSM: Character (18)""")
        fmt = "|%(IDPAR)s|%(FIRME)s|"
        rows = f.fetchall()
        s = "\n".join([fmt % rec for rec in rows[10:15]])
        #print s
        ae(s,u"""\
|000008|Ausdemwald|
|000012|Müller AG|
|000013|Bodard|
|000014|Mendelssohn GmbH|
|000015|INTERMOBIL s.a.|""")

        norbert = rows[10]
        ae(norbert['FIRME'].strip(),"Ausdemwald")
        ae(norbert['IDPAR'],"000008")
        ae(norbert['MEMO'],u"""\
Das ist der Memotext zu Norbert Ausdemwald (IdPar 000008).
Hier ist eine zweite Zeile.

Auf der vierten Zeile kommen weiche Zeilensprünge (ASCII 141) hinzu, die von memoedit() automatisch eingefügt werden, wenn eine Zeile länger als der Texteditor ist. Hinter "von" und "der" müsste jeweils ein ASCII 141 sein.
Und jetzt ist Schluss. Ohne Leerzeile hinter dem Ausrufezeichen!""")



def get_fields(f):
    return "\n".join( ["%s: %s (%d)" % (field.get_name(),
                                        field.get_type_name(),
                                        field.get_len())
                       for field in f.get_fields()])

if __name__ == "__main__":
    unittest.main()
