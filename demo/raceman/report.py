## Copyright 2004-2005 Luc Saffre 

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
from lino import copyleft

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
    


def main2(dbfpath,dbpath):
    
    schema = adamo.Schema()
    schema.addTable(Persons)
    schema.addTable(RaceTypes)
    schema.addTable(Categories)
    schema.addTable(Races)
    schema.addTable(Participants)
    sess = schema.quickStartup(filename=opj(dbpath,"raceman.db"))

    PAR = sess.query(Persons)
    dbfimport(PAR,opj(dbfpath,"PAR.DBF"),
              id=lambda row:int(row['IDPAR']),
              name=lambda row:row['FIRME'],
              firstName=lambda row:row['VORNAME'],
              sex=lambda row:row['SEX'],
              birthDate=lambda row:row['BIRTH']
              )

    CTY = sess.query(RaceTypes)
    dbfimport(CTY,opj(dbfpath,"CTY.DBF"),
            id=lambda row:row['IDCTY'],
            name=lambda row:row['NAME'],
              )
    
    CAT = sess.query(Categories)
    dbfimport(CAT,opj(dbfpath,"CAT.DBF"),
            id=lambda row:row['IDCAT'],
            seq=lambda row:row['SEQ'],
            sex=lambda row:row['SEX'],
            type=lambda row:CTY.peek(row['IDCTY']),
            name=lambda row:row['NAME'],
            ageLimit=lambda row:row['MAXAGE'],
              )
    
    RAL = sess.query(Races)
    dbfimport(RAL,opj(dbfpath,"RAL.DBF"),
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
    dbfimport(POS,opj(dbfpath,"POS.DBF"),oneach)

    
    doc = Document("1")
    
    doc.h(1,"Raceman Generating OpenOffice documents")
    
    race = RAL.peek(53)
    
    q = sess.query(Participants,"person.name cat time dossard",
                   orderBy="person.name",
                   race=race)
    q.executeReport(doc.report(),
                    label="First report",
                    columnWidths="20 3 8 4")

    q = sess.query(Participants,"time person.name cat dossard",
                   orderBy="time",
                   race=race)
    q.executeReport(doc.report(),
                    label="Another report",
                    columnWidths="8 20 3 4")

    outFile = opj(dbpath,"raceman_report.sxc")
    doc.save(outFile,showOutput=True)

    

def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options] DBFPATH",
        description="""\
where DBFPATh is the directory containing TIM files""")
    
    parser.add_option("-t", "--tempdir",
                      help="""\
directory for raceman files""",
                      action="store",
                      type="string",
                      dest="tempDir",
                      default=r'c:\temp')
    
    (options, args) = parser.parse_args(argv)

    if len(args) == 1:
        dbfpath = args[0]
    else:
        dbfpath = r"c:\temp\timrun"
        
    main2(dbfpath,options.tempDir)
    




if __name__ == '__main__':
    console.copyleft(name="Lino/Raceman", years='2002-2005')
    main(sys.argv[1:])




