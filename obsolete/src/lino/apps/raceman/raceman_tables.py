#coding: latin1

## Copyright 2004-2006 Luc Saffre

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

from datetime import datetime

from lino.adamo.ddl import *
#from lino.schemas.sprl.babel import Languages
from lino.apps.contacts.contacts_tables import Language, Person, SEX

NAME = STRING(width=30)
DOSSARD = STRING(width=4)


class Event(StoredDataRow):
    tableName="Events"
    def initTable(self,table):
        table.addField('date',DATE)
        table.addField('name',NAME)
        #table.addView( "std","date name races")

    def getLabel(self):
        return self.name
        
    def printRow(self,doc):
        if len(self.races) == 0:
            doc.p("no races")
            return
        
        for race in self.races:
            rpt=ParticipantsByEventReport(race.participants)
            doc,report(rpt)
        
    def printRowUnused(self,doc):
        #print self.races
        if len(self.races) == 0:
            doc.p("no races")
            return
        columnNames = "place duration person.name cat dossard"
        columnWidths = "4 20 3 8 4"
        rpt = doc.report()
        q = self.races[0].participants.query(columnNames)
        q.setupReport( rpt, columnWidths=columnWidths)
        rpt.beginReport()
        rpt.table.h(1,__unicode__(self))

        for race in self.races:
            rpt.table.h(2,unicode(race))
            q = race.participants.query( columnNames,
                                         orderBy="place")
            for prt in q:
                rpt.processRow(prt)

        rpt.endReport()

class EventsReport(DataReport):
    leadTable=Event
    columnNames="date name races"


class Race(StoredDataRow):
    tableName="Races"
    def initTable(self,table):
        table.addField('id',ROWID) #STRING(width=6))
        table.addField('name1',NAME)
        table.addField('name2',NAME)
        table.addField('date',DATE)
        table.addField('status',STRING(width=1))
        table.addField('tpl',STRING(width=6))
        table.addPointer('type',RaceType)
        table.addField('startTime',TIME)
        table.addField('known',INT)
        table.addField('unknown',INT)
        table.addField('invalid',INT)
        table.addField('missing',INT)
        table.addPointer('event',Event)
        #.setDetail("races")
        table.addDetail('participants',Participant,'race')
##         table.addView( "std",
##                        "date event name1 status startTime "
##                        "arrivals participants "
##                        "known unknown invalid missing "
##                        "tpl type name2 id")

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Race")
        def f():
            race = nav.getCurrentRow()
            race.showArrivalEntry(frm)
            frm.refresh()
            
        m.addItem(label="&Arrivals",
                  action=f,
                  accel="F6")
        
        m.addItem(label="&Compute results", accel="F3").setHandler(
            nav.withCurrentRow,self.Instance.computeResults,frm)


    def getLabel(self):
        return self.name1

##     def participants(self,*args,**kw):
##         kw['race']=self
##         return self.detail(Participant,*args,**kw)
    
    def showArrivalEntry(self,ui):
        #self.lock()
        frm = ui.form(
            label="Arrivals for "+str(self),
            doc="""\
Ankunftszeiten an der Ziellinie erfassen.
Jedesmal wenn einer ankommt, ENTER drücken.
    """)

        frm.addEntry("dossard",STRING,
                     label="Dossard",
                     value="*",
                     doc="""Hier die Dossardnummer des
                     ankommenden Läufers eingeben,
                     oder '*' wenn sie später
                     erfasst werden soll.""")



        def arriveNow():
            if self.startTime is None:
                frm.buttons.start.setFocus()
                raise InvalidRequestError(
                    "cannot arrive before start")
            now = datetime.now()
            #assert now.date() == self.date,\
            #       "%s != %s" % (repr(now.date()),repr(self.date))
            #duration = now - datetime.datetime.combine(
            #    now.date(), self.startTime)
            a = self.arrivals.appendRow(
                dossard=frm.entries.dossard.getValue(),
                time=now.time())
            frm.status("%s arrived at %s" % (a.dossard,a.time))
            frm.entries.dossard.setValue('*')
            frm.entries.dossard.setFocus()



        #bbox = frm.addHPanel()
        bbox = frm
        bbox.addButton(name="arrive",
                      label="&Arrive",
                      action=arriveNow).setDefault()
        #bbox.addButton("write",
        #               label="&Write",
        #               action=self.writedata)
        bbox.addButton("exit",label="&Exit",action=frm.close)

##         fileMenu  = frm.addMenu("&File")
##         fileMenu.addButton(frm.buttons.write,accel="Ctrl-S")
##         fileMenu.addButton(frm.buttons.exit,accel="Ctrl-Q")

##         fileMenu  = frm.addMenu("&Edit")
##         fileMenu.addButton(frm.buttons.start)
##         fileMenu.addButton(frm.buttons.arrive,accel="Ctrl-A")
        #self.frm = frm
        frm.show()
        #frm.showModal()
        #self.unlock()

    def computeResults(self,ui):
        ui.status("go")
        self.lock()
        #    return
        self.unknown = 0
        self.known = 0
        self.invalid = 0
        self.missing = 0
        ui.status("scanning %d arrivals" % len(self.arrivals))
        for a in self.arrivals:
            if a.dossard == '*':
                self.unknown += 1
            else:
                p = self.participants().peek(self,a.dossard)
                if p is None:
                    self.invalid += 1
                elif p.lock():
                    p.duration = a.time - datetime.combine(
                        self.date, self.startTime)
                    p.unlock()
                    self.known += 1
                else:
                    raise RowLockFailed

        #ui.status(
        #    "%d recognized, %d unknown and %d invalid arrivals"\
        #    % (self.known, self.unknown, invalid))
        q=self.participants()
        ui.status("scanning %d participants" % \
                  len(q))
        place = 0
        for p in q.query(orderBy='duration'):
            if p.duration is None:
                self.missing  += 1
            else:
                place += 1
                if p.lock():
                    print p, place
                    p.place = place
                    p.unlock()
                else:
                    raise RowLockFailed

        ui.status("scanning %d participants" % \
                  len(q))
        place = 0
        cat = None
        for p in q.query(orderBy='cat duration'):
            if p.duration is not None:
                if cat == p.cat:
                    place += 1
                else:
                    place = 1
                    cat = p.cat
                if p.lock():
                    p.place = place
                    p.unlock()
                else:
                    raise RowLockFailed

        self.unlock()


    def printRow(self,prn):
        raise "not converted after 20060213"
        sess = self.getSession()
        q = self.participants(
            "person.name cat time dossard",
            orderBy="person.name")
        q.executeReport(prn.report(),
                        label="First report",
                        columnWidths="20 3 8 4")

        q = sess.query(Participants,"time person.name cat dossard",
                       orderBy="time",
                       race=self)
        q.executeReport(prn.report(),
                        label="Another report",
                        columnWidths="8 20 3 4")

        self.ralGroupList(prn,
                          xcKey="club",
                          nGroupSize=3)
        self.ralGroupList(prn, xcKey="club",
                          nGroupSize=5,
                          sex="M")
        self.ralGroupList(prn,
                          xcKey="club",
                          nGroupSize=5,
                          sex="F")

    def ralGroupList(self,prn,
                     xcKey="club",
                     xnValue="place",
                     nGroupSize=3,
                     sex=None,
                     xcName=None,
                     maxGroups=10):
        raise "not converted after 20060213"
    
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

        for pos in self.participants( \
            orderBy="duration"):
            if pos.duration != None:
                if sex is None or pos.person.sex == sex:
                    key = getattr(pos,xcKey)
                    if key is not None:
                        v = getattr(pos,xnValue)
                        g = collectPos(groups,key)
                        g.values.append(v)
                        g.sum += v
                        if xcName is None:
                            g.names.append(str(v))
                        else:
                            g.names.append(xcName(pos))

        groups = filter(lambda g: len(g.values) == nGroupSize,
                        groups)
        groups.sort(lambda a,b: a.sum - b.sum)

        rpt = prn.report(label="inter %s %s by %d" % (xcKey,
                                                      sex,
                                                      nGroupSize))
        rpt.addColumn(meth=lambda g: str(g.id),
                      label=xcKey,
                      width=20)
        rpt.addColumn(meth=lambda g: str(g.sum),
                      label=xnValue,
                      width=5)
        rpt.addColumn(
            meth=lambda g: " + ".join(g.names)+" = " +str(g.sum),
            label="values",
            width=40)
        rpt.execute(groups[:maxGroups])



class RacesReport(DataReport):
    leadTable=Race
    columnNames="date event name1 status startTime "\
                "arrivals participants "\
                "known unknown invalid missing "\
                "tpl type name2 id"


        
        
class RaceType(StoredDataRow):
    tableName="RaceTypes"
    def initTable(self,table):
        table.addField('id',STRING(width=5))
        table.addField('name',NAME)

    def getLabel(self):
        return self.name

class RaceTypesReport(DataReport):
    leadTable=RaceType
        
class Club(StoredDataRow):
    tableName="Clubs"
    def initTable(self,table):
        table.addField('id',STRING(width=5))
        table.addField('name',NAME)

    def getLabel(self):
        return self.name
        
class ClubsReport(DataReport):
    leadTable=Club
    
class Category(StoredDataRow):
    tableName="Categories"
    def initTable(self,table):
        table.addPointer('type',RaceType)
        table.addField('id',STRING(width=3))
        table.addField('seq',ROWID)
        table.addField('name',STRING(width=30))
        table.addField('sex',SEX)
        table.addField('ageLimit',INT)
        
        table.setPrimaryKey('type id')

    def getLabel(self):
        return self.id + " ("+self.name+")"

class CategoriesReport(DataReport):
    leadTable=Category
        
class Participant(StoredDataRow):
    tableName="Participants"
    def initTable(self,table):
        table.setPrimaryKey("race dossard")
        
        table.addPointer('race',Race)
        #.setDetail('participants')
        table.addField('dossard',DOSSARD)
        table.addPointer('person',Person)
        table.addPointer('club',Club)
        table.addField('duration',DURATION)
        table.addPointer('cat',Category)
        table.addField('payment',STRING(width=1))
        table.addField('place',INT)
        table.addField('catPlace',INT)
        

class ParticipantsReport(DataReport):
    leadTable=Participant
    
class ParticipantsByEventReport(DataReport):
    leadTable=Participant
    columnNames = "place duration person.name cat dossard"
    columnWidths = "4 20 3 8 4"
    orderBy="place"
    masterColumns="event"
    
    
class Arrival(StoredDataRow):
    tableName="Arrivals"
    def initTable(self,table):
        table.addPointer('race',Race)
        #.setDetail('arrivals')
        table.addField('dossard',DOSSARD)
        table.addField('time',TIME)
        #table.addField('duration',DURATION)
        table.addField('ok',BOOL)
        

class ArrivalsReport(DataReport):
    leadTable=Arrival


class RacemanSchema(Schema):
    tableClasses=(
        Event,
        Club,
        Person,
        RaceType,
        Category,
        Race,
        Participant,
        Arrival,
        )


class RacemanMainForm(DbMainForm):
    """\
This is the Raceman main menu.                                     
    """
    
    schemaClass=RacemanSchema
    
    def setupMenu(self):

        m = self.addMenu("master","&Stammdaten")
        
        m.addReportItem("events",EventsReport,
                        label="&Events")
        
        m.addReportItem("races",RacesReport,
                        label="&Races")
        
        m.addReportItem("clubs",ClubsReport,
                        label="&Clubs")
        
        m.addReportItem("persons",PersonsReport,
                        label="&Persons")
        
        self.addProgramMenu()
        


    

__all__ = [t.__name__ for t in RacemanSchema.tableClasses]
__all__.append('RacemanSchema')
