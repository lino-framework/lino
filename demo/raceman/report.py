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
     Participants, Persons, Clubs

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
                oneach(q,row)
        except adamo.DataVeto,e:
            console.info(str(e))
        except adamo.DatabaseError,e:
            console.info(str(e))
        except ValueError,e:
            console.info(str(e))
    f.close()
    q.commit()
    return q

class DbfPopulator:
    dbfpath="."
    def populate(self,sess):
        q = sess.query(self.__class__)
        dbfimport(q,opj(self.dbfpath,self.name+".DBF"),
                  self.appendFromDBF)

class PAR(DbfPopulator,Persons):
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDPAR'],
            name=row['FIRME'],
            firstName=row['VORNAME'],
            sex=row['SEX'],
            birthDate=row['BIRTH'])
        
class CLB(DbfPopulator,Clubs):
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDCLB'],
            name=row['NAME'],
            )

class CTY(DbfPopulator,RaceTypes):
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDCTY'],
            name=row['NAME'],
            )


class CAT(DbfPopulator,Categories):
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDCAT'],
            seq=row['SEQ'],
            sex=row['SEX'],
            type=q.getSession().peek(CTY,row['IDCTY']),
            name=row['NAME'],
            ageLimit=row['MAXAGE'],
            )
        

class RAL(DbfPopulator,Races):
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDRAL'],
            name1=row['NAME1'],
            name2=row['NAME2'],
            date=row['DATE'],
            )
        

class POS(DbfPopulator,Participants):
    def appendFromDBF(self,q,row):
        sess = q.getSession()
        race = sess.peek(RAL,row['IDRAL'])
        person = sess.peek(PAR,row['IDPAR'])
        if race.type is None:
            cat = None
        else:
            cat = sess.peek(race.type,CAT,row['IDCAT'])
        club = sess.peek(CLB,row['IDCLB'])
        q.appendRow(
            race=race,
            person=person,
            cat=cat,
            club=club,
            dossard=row['IDPOS'],
            time=row['TIME'],
            place=int(row['PLACE']),
            catPlace=int(row['CATPLACE']),
            payment=row['PAYE'],
            )
    


def main2(dbfpath,dbpath):
    
    schema = adamo.Schema()
    schema.addTable(CLB)
    schema.addTable(PAR)
    schema.addTable(CTY)
    schema.addTable(CAT)
    schema.addTable(RAL)
    schema.addTable(POS)
    
    for t in schema.getTableList():
        t.dbfpath = dbfpath

    sess = schema.quickStartup(filename=opj(dbpath,"raceman.db"))

##     PAR = sess.query(Persons)
##     dbfimport(PAR,opj(dbfpath,"PAR.DBF"),
##               id=lambda row:int(row['IDPAR']),
##               name=lambda row:row['FIRME'],
##               firstName=lambda row:row['VORNAME'],
##               sex=lambda row:row['SEX'],
##               birthDate=lambda row:row['BIRTH']
##               )

##     CLB = sess.query(Clubs)
##     dbfimport(CLB,opj(dbfpath,"CLB.DBF"),
##             id=lambda row:row['IDCLB'],
##             name=lambda row:row['NAME'],
##               )
    
##     CTY = sess.query(RaceTypes)
##     dbfimport(CTY,opj(dbfpath,"CTY.DBF"),
##             id=lambda row:row['IDCTY'],
##             name=lambda row:row['NAME'],
##               )
    
##     CAT = sess.query(Categories)
##     dbfimport(CAT,opj(dbfpath,"CAT.DBF"),
##             id=lambda row:row['IDCAT'],
##             seq=lambda row:row['SEQ'],
##             sex=lambda row:row['SEX'],
##             type=lambda row:CTY.peek(row['IDCTY']),
##             name=lambda row:row['NAME'],
##             ageLimit=lambda row:row['MAXAGE'],
##               )
    
##     RAL = sess.query(Races)
##     dbfimport(RAL,opj(dbfpath,"RAL.DBF"),
##             id=lambda row:int(row['IDRAL']),
##             name1=lambda row:row['NAME1'],
##             name2=lambda row:row['NAME2'],
##             date=lambda row:row['DATE'],
##               )


##     POS = sess.query(Participants)
##     def oneach(row):
##         race = RAL.peek(int(row['IDRAL']))
##         cat = CAT.peek(race.type,row['IDCAT'])
##         club = CLB.peek(row['IDCLB'])
##         POS.appendRow(
##             race=race,
##             person=PAR.peek(int(row['IDPAR'])),
##             cat=cat,
##             club=club,
##             dossard=row['IDPOS'],
##             time=row['TIME'],
##             place=int(row['PLACE']),
##             catPlace=int(row['CATPLACE']),
##             payment=row['PAYE'],
##             )
##     dbfimport(POS,opj(dbfpath,"POS.DBF"),oneach)

    if True:
    
        doc = Document("1")
    
        doc.h(1,"Raceman Generating OpenOffice documents")

        main3(doc,sess)
        outFile = opj(dbpath,"raceman_report.sxc")
        doc.save(outFile,showOutput=True)
    else:
        main3(console,sess)


def main3(doc,sess):
    
    race = sess.peek(RAL,"000053")
    
    q = sess.query(POS,"person.name cat time dossard",
                   orderBy="person.name",
                   race=race)
    q.executeReport(doc.report(),
                    label="First report",
                    columnWidths="20 3 8 4")

    q = sess.query(POS,"time person.name cat dossard",
                   orderBy="time",
                   race=race)
    q.executeReport(doc.report(),
                    label="Another report",
                    columnWidths="8 20 3 4")

    ralGroupList(doc,race, xcKey="club", nGroupSize=3)
    ralGroupList(doc,race, xcKey="club", nGroupSize=5,sex="M")
    ralGroupList(doc,race, xcKey="club", nGroupSize=5,sex="F")






def ralGroupList(doc,race,
                 xcKey="club",
                 xnValue="place",
                 nGroupSize=3,
                 sex=None,
                 xcName=None):
    class Group:
        def __init__(self,id):
            self.id = id
            self.values = []
            self.sum = 0
            self.names = []
            
    groups = []

    def collectPos(groups,key):
        for g in groups:
            if g.id == key:
                if len(g.values) < nGroupSize:
                    return g
        g = Group(key)
        groups.append(g)
        return g
        
    for pos in race.pos_by_race.query(orderBy="time"):
        if pos.time != "X":
            if sex is None or pos.person.sex == sex:
                v = getattr(pos,xnValue)
                key = getattr(pos,xcKey)
                g = collectPos(groups,key)
                g.values.append(v)
                g.sum += v
                if xcName is not None:
                    g.names.append(xcName(pos))

    groups.sort(lambda a,b: a.sum > b.sum)

    rpt = doc.report(label="inter %s %s by %d" % (xcKey,
                                                  sex,
                                                  nGroupSize))
    rpt.addColumn(meth=lambda g: str(g.id),
                  label=xcKey,
                  width=20)
    rpt.addColumn(meth=lambda g: str(g.sum),
                  label=xnValue,
                  width=5)
    rpt.addColumn(meth=lambda g: str(g.values),
                  label="values",
                  width=30)
    rpt.execute(groups)

    

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




