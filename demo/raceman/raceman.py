## Copyright Luc Saffre 2004.

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
import sys
import unittest
from lino.ui import console
from lino.oogen import Document
from lino import adamo

from lino.schemas.sprl.races import Races, RaceTypes, Categories, \
     Participants, Persons

from lino.tools import dbfreader

opj = os.path.join


def dbfimport(q,filename,oneach=None,**kw):
    console.info(q.getLabel())
    if q.mtime() >= os.stat(filename).st_mtime:
        console.info("%s : no need to read again" % filename)
        return
        
    f = dbfreader.DBFFile(filename, codepage="cp850")
    q.zap()
    f.open()
    for row in f:
        try:
            if oneach is None:
                d = {}
                for k,v in kw.items():
                    d[k] = v(row)
                q.appendRow(**d)
            else:
                oneach(row)
        except adamo.DataVeto,e:
            console.info(str(e))
        except adamo.DatabaseError,e:
            console.info(str(e))
        except ValueError,e:
            console.info(str(e))
    f.close()
    q.commit()
    return q
    


def main(dbpath=r"c:\temp\timrun"):
    
    s = adamo.Schema()
    s.addTable(Races)
    s.addTable(RaceTypes)
    s.addTable(Categories)
    s.addTable(Participants)
    s.addTable(Persons)
    #sess = adamo.beginQuickSession(s,filename=":memory:")
    sess = adamo.beginQuickSession(s,
                                   filename="tmp.db",
                                   isTemporary=False)

    PAR = sess.query(Persons)
    dbfimport(PAR,opj(dbpath,"PAR.DBF"),
              id=lambda row:int(row['IDPAR']),
              name=lambda row:row['FIRME'],
              firstName=lambda row:row['VORNAME'],
              sex=lambda row:row['SEX'],
              birthDate=lambda row:row['BIRTH']
              )

    CTY = sess.query(RaceTypes)
    dbfimport(CTY,opj(dbpath,"CTY.DBF"),
            id=lambda row:row['IDCTY'],
            name=lambda row:row['NAME'],
              )
    
    CAT = sess.query(Categories)
    dbfimport(CAT,opj(dbpath,"CAT.DBF"),
            id=lambda row:row['IDCAT'],
            seq=lambda row:row['SEQ'],
            sex=lambda row:row['SEX'],
            type=lambda row:CTY.peek(row['IDCTY']),
            name=lambda row:row['NAME'],
            ageLimit=lambda row:row['MAXAGE'],
              )
    
    RAL = sess.query(Races)
    dbfimport(RAL,opj(dbpath,"RAL.DBF"),
            id=lambda row:int(row['IDRAL']),
            name1=lambda row:row['NAME1'],
            name2=lambda row:row['NAME2'],
            date=lambda row:row['DATE'],
              )


    POS = sess.query(Participants)
    def oneach(row):
        race = RAL.peek(int(row['IDRAL']))
        cat = CAT.peek(race.type,row['IDCAT'])
        POS.appendRow(
            race=race,
            person=PAR.peek(int(row['IDPAR'])),
            cat=cat,
            dossard=row['IDPOS'],
            time=row['TIME'],
            payment=row['PAYE'],
            )
    dbfimport(POS,opj(dbpath,"POS.DBF"),oneach)

    
    
    
##     q = sess.query(Races,"id name1 name2 date")
##     q.setupReport(rpt)
##     rpt.columns[0].configure(width=5)
##     rpt.columns[1].configure(width=30)
##     rpt.columns[2].configure(width=30)

    race = RAL.peek(53)
    q = sess.query(Participants,"person.name cat time dossard",
                   race=race)
    rpt = sess.data_report(q)
    #q.setupReport(rpt)
    rpt.columns[0].configure(width=20)
    rpt.columns[1].configure(width=3)
    rpt.columns[2].configure(width=8)
    rpt.columns[3].configure(width=4)

    
    rpt.beginReport()
    for r in q:
        rpt.processRow(r)
    rpt.endReport()
        
    
    
    
    
##     doc = Document("1")
##     doc.h(1,"Generating OpenOffice documents")
##     doc.p("Here is a table:")
##     t = doc.table()
##     t.addColumn()
##     t.addColumn()
##     t.addRow("Kunde","Datum")
##     t.addRow("Hinz","2004-11-16")
##     t.addRow("Kunz","2004-11-17")

##     doc.p("Here is another paragraph.")

##     doc.save(fn)

if __name__ == "__main__":
    main() # sys.argv[1])
