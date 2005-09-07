#coding: iso-8859-1
## Copyright 2005 Luc Saffre 

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

from lino.apps.pinboard.pinboard import Pinboard
from lino.apps.pinboard.tables import *
from lino.apps.pinboard.tables import TABLES

from lino.adamo.ddl import Schema, Populator

def startup(filename=None, langs=None,
            populate=True,
            dump=None,
            withDemoData=True,
            withLangs=False,
            withJokes=False,
            **kw):
    schema = Pinboard(**kw)
    sess=schema.quickStartup(langs=langs,
                             filename=filename,
                             dump=dump)
    if populate:
        if withLangs:
            sess.populate(LangsPopulator())
            
        sess.populate(StdPopulator())
        
        if withJokes:
            sess.populate(JokesPopulator())
        
        if withDemoData:
            sess.populate(DemoPopulator())
            assert len(sess.query(Project))==10

    return sess

class StdPopulator(Populator):
        
    def populateLanguages(self,q):
        if len(q): return # done by LangsPopulator
        #q.setVisibleColumns('id name')
        q=q.query('id name')
        q.setBabelLangs('en de fr')
        q.appendRow(
            'en',('English','Englisch','Anglais')     )
        q.appendRow(
            'de',('German','Deutsch', 'Allemand')     )
        q.appendRow(
            'et',('Estonian','Estnisch','Estonien')   )
        q.appendRow(
            'fr',('French','Französisch','Français')  )
        q.appendRow(
            'nl',('Dutch','Niederländisch','Neerlandais'))

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
                    ('track','Stück') )
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

class DemoPopulator(Populator):
            
    def populateLanguages(self,q):
        for lng in ('en','de','et','fr'):
            setattr(self,lng,q.peek(lng))
            
    def populateAuthors(self,q):
        q = q.query('name firstName quotesByAuthor' )
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
        q.appendRow( 'Zink'      ,'Jörg') #       ,deutschland)
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
        q.appendRow('S',('sleeping','schläft'))

        
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
    
    def populateQuotes(self,q):
        q = q.query('lang quote author')

        q.appendRow(self.fr, """\
Entre nous soit dit, bonnes gens:
pour reconnaître que l'on est pas intelligent il faudrait
l'être.""", self.brassens)

        q.appendRow(self.de, """\
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

        q = self.mencken.quotesByAuthor.query('lang quote')
        quote = q.appendRow(self.en,"""\
An idealist is one who, on noticing that a rose smells better than a
cabbage, concludes that it will also make better soup.
""")
        assert quote.author.name == "Mencken"
        quote = q.appendRow(self.en,"""\
Conscience is the inner voice that warns us that someone may be looking.        
""")
        q = self.churchill.quotesByAuthor.query('lang quote')
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
        de=q.getSession().peek(Language,"de")
        from lino.apps.pinboard import quotes_de
        quotes_de.populate(q,de)
        #print "%d Weisheiten" % len(q)
            


class LangsPopulator(Populator):
    def populateLanguages(self,q):
        from lino.schemas.sprl.data import languages
        languages.populate(q)
