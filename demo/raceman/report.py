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


from lino.ui import console
from lino.oogen import Document
from lino import adamo
from lino import copyleft

from schema import makeSchema

from lino.schemas.sprl.races import Races, RaceTypes, Categories, \
     Participants, Persons, Clubs

from lino.tools import dbfreader

opj = os.path.join


def main2(dbfpath,dbpath):

    schema = makeSchema(dbfpath)
    
    sess = schema.quickStartup( filename=opj(dbpath,"raceman.db"))

    sess.progress("Generating reports...")
    if True:
    
        doc = Document("1")
    
        doc.h(1,"Raceman Generating OpenOffice documents")

        main3(doc,sess)
        outFile = opj(dbpath,"raceman_report.sxc")
        doc.save(outFile,showOutput=True)
    else:
        main3(console,sess)


def main3(doc,sess):
    
    race = sess.peek(Races,53)
    
    assert race is not None
    
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
        
    for pos in race.participants_by_race.query(orderBy="time"):
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




