#coding: iso-8859-1
## Copyright 2005-2007 Luc Saffre 

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

from pinboard_tables import *
from lino.apps.pinboard.pinboard import Pinboard
from lino.apps.contacts import contacts_demo 

from lino.adamo.ddl import Populator


def startup(**kw):
    app=DemoPinbord(**kw)
    return app.createContext()

class DemoPinbord(Pinboard):

    def __init__(self,
                 populate=True,big=False, withDemoData=True,
                 withJokes=False,
                 **kw):
        self.populate=populate
        self.big=big
        self.withDemoData=withDemoData
        self.withJokes=withJokes
        Pinboard.__init__(self,**kw)
    
    def createContext(self):
        ctx=Pinboard.createContext(self)
        if self.populate:
            if self.withDemoData:
                self.runtask(DemoPopulator(),ctx)
                #ctx.populate(DemoPopulator(big=self.big))
            else:
                self.runtask(StdPopulator(),ctx)
                #ctx.populate(StandardPopulator(big=self.big))
            if self.withJokes:
                self.runtask(JokesPopulator(),ctx)
                
        return ctx
        



## def startup(filename=None, langs=None,
##             populate=True,
##             dump=None,
##             withDemoData=True,
##             withJokes=False,
##             **kw):
##     schema = PinboardSchema(**kw)
##     sess=schema.quickStartup(langs=langs,
##                              filename=filename,
##                              dump=dump)
##     if populate:
        
##         if withDemoData:
##             sess.populate(DemoPopulator())
##         else:
##             sess.populate(StdPopulator())

##         if withJokes:
##             sess.populate(JokesPopulator())
        
##     return sess

class StdPopulator(contacts_demo.StandardPopulator):
        
    def populatePubTypes(self,q):
        q.setBabelLangs('en de')
        q = q.query('id name typeRefPrefix pubRefLabel')
        q.appendRow("book",
                    ('Book','Buch')        ,
                    'ISBN:',
                    ('page','Seite')  )
        q.appendRow("url" , ('Web Page','Webseite')    ,
                    'http:' , ( None, None)   )
        q.appendRow("cd"  , ('CompactDisc', 'CD') , 'cddb:',
                    ('track',u'Stück') )
        q.appendRow("art" , ('Article','Artikel')     ,
                    None      , ('page','Seite')  )
        q.appendRow("mag" , ('Magazine','Zeitschrift')    ,
                    None      , ('page','Seite')  )
        q.appendRow("sw"  , ('Software','Software')    ,
                    None      , (None,None)    )


    def populateAuthorEventTypes(self,q):
        q = q.query('id name')
        q.setBabelLangs('en de')
        q.appendRow(1,('born','geboren'))
        q.appendRow(2,('died','gestorben'))
        q.appendRow(3,('married','Heirat'))
        q.appendRow(4,('school','Schulabschluss'))
        q.appendRow(5,('other','Sonstige'))	

class DemoPopulator(contacts_demo.DemoPopulator):
            
    def populateAuthors(self,q):
        #q = q.query('name firstName quotesByAuthor' )
        q = q.query('name firstName' )
        q.appendRow( 'Gates'         ,'Bill') #       ,usa)
        q.appendRow( 'Huxley'    ,'Aldous') #     ,None)
        q.appendRow( 'Tolkien'   ,'J.R.R.') #     ,None)
        q.appendRow( 'Watzlawick','Paul') #       ,usa)
        q.appendRow( 'Bisset'    ,'Donald') #     ,None)
        q.appendRow( 'Meves'         ,'Christa') #    ,None)
        q.appendRow( 'Brel'      ,'Jacques') #    ,belgique)
        self.brassens = q.appendRow(
            'Brassens' ,'Georges') #    ,belgique)
        q.appendRow( 'Lorenz'    ,'Konrad') #     ,deutschland)
        q.appendRow( 'Zink'      ,u'Jörg') #       ,deutschland)
        # q.appendRow( 'Robinson'   ,'Larry H.'  ,None, None, None)
        self.anon = q.appendRow('Anonymus' ,None) #   ,None)
        self.lauster = q.appendRow( 'Lauster'  ,'Peter') 

        self.mencken = q.appendRow(firstName="Henry Louis",
                                   name="Mencken")
        self.churchill = q.appendRow(firstName="Winston",
                                     name="Churchill")


    def populateProjectStati(self,q):
        q = q.query('id name')
        q.setBabelLangs('en de')
        q.appendRow('T',('to do','zu erledigen'))
        q.appendRow('D',('done','erledigt'))
        q.appendRow('W',('waiting','wartet'))
        q.appendRow('A',('abandoned','storniert'))
        q.appendRow('S',('sleeping',u'schläft'))

        
    def populateProjects(self,q):
        p1 = q.appendRow(title="Project 1")
        p2 = q.appendRow(title="Project 2")
        p3 = q.appendRow(title="Project 3")
        p11 = q.appendRow(title="Project 1.1",super=p1)
        p12 = q.appendRow(title="Project 1.2",super=p1)
        p13 = q.appendRow(title="Project 1.3",super=p1)
        p131 = q.appendRow(title="Project 1.3.1",super=p13)
        p132 = q.appendRow(title="Project 1.3.2",super=p13)
        p1321 = q.appendRow(title="Project 1.3.2.1",super=p132)
        p1322 = q.appendRow(title="Project 1.3.2.2",super=p132)

    def populateContacts(self,q):
        #don't used inherited method  because Pinboard doesn't have a Functions table
        pass
    
    def populateQuotes(self,q):
        q = q.query('lang quote author')

        q.appendRow(self.fr, u"""\
Entre nous soit dit, bonnes gens:
pour reconnaître que l'on est pas intelligent il faudrait
l'être.""", self.brassens)

        q.appendRow(self.de, u"""\
Körper, Geist und Seele sind die drei Bereiche des Menschen. Der
Körper sollte gesund sein, der Geist intelligent, und die Seele - das
Kostbarste und Wichtigste - sollte frei sein. Dann kann das Leben
gelingen und zum Geschenk werden.\
""",self.lauster)


        q.appendRow(self.en, """\
It is much easier to suggest solutions
when you know nothing about the problem.
""", self.anon)

        q.appendRow(self.en,"""\
Many people are desperately looking for some wise advice which will
recommend that they do what they want to do.    
""", self.anon)

        q.appendRow(self.en, """
Carelessly planned projects take
three times longer to complete than expected.  Carefully planned
projects take four times longer to complete than expected,
mostly because the planners expect their planning to reduce the
time it takes.""",self.anon)

        q.appendRow(self.en, """\
Don't believe everything you hear or anything you say.""",
                    self.anon)

        q = self.mencken.quotesByAuthor('lang quote')
        quote = q.appendRow(self.en,"""\
An idealist is one who, on noticing that a rose smells better than a
cabbage, concludes that it will also make better soup.
""")
        assert quote.author.name == "Mencken"
        quote = q.appendRow(self.en,"""\
Conscience is the inner voice that warns us that someone may be looking.        
""")
        q = self.churchill.quotesByAuthor('lang quote')
        quote = q.appendRow(self.en,"""\
A fanatic is one who can't change his mind and won't change the subject.
""")

        # http://www.io.com/~gibbonsb/mencken.html
        #a.events.appendRow()

        if False:
            # cannot appendRow with value outside of leadTable:
            q = q.query('lang quote author.firstName author.name')
            q.appendRow(self.en,
                        """\
Trusting a scientist on questions of metaphysics is like paying
someone else to worship God for you.""",\
                    "Bill","Welton"\
                    )


class JokesPopulator(Populator):

        
    def populateQuotes(self,q):
        de=q.getContext().peek(Language,"de")
        from lino.apps.pinboard import quotes_de
        quotes_de.populate(q,de)
        #print "%d Weisheiten" % len(q)
            


