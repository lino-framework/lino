## Copyright Luc Saffre 2004-2005.

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

from lino.adamo import *
from babel import Languages
from addrbook import Persons, SEX

NAME = STRING(width=30)

class Races(Table):
    def init(self):
        self.addField('id',ROWID) #STRING(width=6))
        self.addField('name1',NAME)
        self.addField('name2',NAME)
        self.addField('date',DATE)
        self.addField('status',STRING(width=1))
        self.addField('tpl',STRING(width=6))
        self.addPointer('type',RaceTypes)
        self.addField('startTime',TIME)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name1

        def writeReport(self,doc):
            sess = self.getSession()
            q = sess.query(Participants,"person.name cat time dossard",
                           orderBy="person.name",
                           race=self)
            q.executeReport(doc.report(),
                            label="First report",
                            columnWidths="20 3 8 4")

            q = sess.query(Participants,"time person.name cat dossard",
                           orderBy="time",
                           race=self)
            q.executeReport(doc.report(),
                            label="Another report",
                            columnWidths="8 20 3 4")

            self.ralGroupList(doc, xcKey="club", nGroupSize=3)
            self.ralGroupList(doc, xcKey="club", nGroupSize=5,sex="M")
            self.ralGroupList(doc, xcKey="club", nGroupSize=5,sex="F")

        def ralGroupList(self,doc,
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

            for pos in self.participants_by_race.query(orderBy="time"):
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

            


        
        
class RaceTypes(Table):
    def init(self):
        self.addField('id',STRING(width=5))
        self.addField('name',NAME)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        
class Clubs(Table):
    def init(self):
        self.addField('id',STRING(width=5))
        self.addField('name',NAME)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        
class Categories(Table):
    def init(self):
        self.addPointer('type',RaceTypes)
        self.addField('id',STRING(width=3))
        self.addField('seq',ROWID)
        self.addField('name',STRING(width=30))
        self.addField('sex',SEX)
        self.addField('ageLimit',INT)
        
        self.setPrimaryKey('type id')

    class Instance(Table.Instance):
        def getLabel(self):
            return self.id + " ("+self.name+")"
        
class Participants(Table):
    def init(self):
        self.setPrimaryKey("race dossard")
        
        self.addPointer('race',Races)
        self.addField('dossard',STRING(width=4))
        self.addPointer('person',Persons)
        self.addPointer('club',Clubs)
        self.addField('time',TIME)
        self.addPointer('cat',Categories)
        self.addField('payment',STRING(width=1))
        self.addField('place',INT)
        self.addField('catPlace',INT)
        

