#coding: latin1

## Copyright Luc Saffre 2003-2005

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

"""
"""

raise "no longer used"

import os

from lino.tools.normalDate import ND
from lino.schemas.sprl.tables import *


def populate(sess):

    LANGS = sess.query(Languages)
    NATIONS = sess.query(Nations)
    CITIES = sess.query(Cities)
    PAGES = sess.query(Pages)
    CURR = sess.query(Currencies)
    PARTNERS = sess.query(Partners)
    ORGS = sess.query(Organisations)
    AUTHORS = sess.query(Authors)
    QUOTES = sess.query(Quotes)
    PROJECTS = sess.query(Projects)
    
    en = LANGS.peek('en')
    de = LANGS.peek('de')
    fr = LANGS.peek('fr')
        
    eesti = NATIONS.peek('ee')
    belgique = NATIONS.peek('be')
    deutschland = NATIONS.peek('de')
    france = NATIONS.peek('fr')
    usa = NATIONS.peek('us')

    
##     if len(belgique.cities) == 0:
##         q = belgique.cities.query('name')
##         #print q.sampleColumns
##         q.appendRow(name="Bruxelles")
##         q.appendRow("Brugge")

##         q.appendRow("Eupen")
##         q.appendRow("Kettenis")
##         q.appendRow("Kelmis")
##         q.appendRow("Raeren")
##         q.appendRow("Mons")
##         q.appendRow("Liège")
##         q.appendRow("Charleroi")
##         q.appendRow("Verviers")
    
##     eupen = CITIES.findone(name="Eupen")
##     assert eupen is not None
##     verviers = CITIES.findone(name="Verviers")
##     assert verviers is not None
    
##     assert eupen.name == "Eupen"
##     assert eupen.nation == belgique, \
##              "%s != %s" % (repr(eupen.nation),repr(belgique))
##     q = CITIES.query('name inhabitants', nation=eesti)
    
##     tallinn = q.appendRow("Tallinn",442000)
##     assert tallinn.inhabitants == 442000
##     assert tallinn.nation == eesti
##     assert tallinn.nation.id == "ee"
##     assert tallinn.getRowId() == ['ee',1], \
##              "%s != ['ee',1]" % repr(tallinn.getRowId())
##     q.appendRow("Tartu",109100)
##     #q.appendRow("Otepää")
##     q.appendRow("Narva",80300)
##     q.appendRow("Kilingi-Nõmme",2490)
##     q.appendRow("Pärnu",52000)
##     q.appendRow("Rakvere",18096)
##     q.appendRow("Viljandi",20756)
##     q.appendRow("Ruhnu",58)
##     q.appendRow("Vigala",1858)
##     q.appendRow("Kohtla-Järve",70800)


##     q = deutschland.cities.query('name') 
##     aachen = q.appendRow("Aachen")
##     q.appendRow("Köln")
##     q.appendRow("Berlin")
##     q.appendRow("Bonn")
##     q.appendRow("München")
##     q.appendRow("Eschweiler")
##     q.appendRow("Alfter-Oedekoven")
    

    

##     if False:
##         home = PAGES.appendRow(
##             match='index',
##             super=None,
##             lang=en,
##             title="Lino Demo Data",
##             abstract="""
##             This is a collection of data from various sources.
##             """,body="""
##             """)

##         import bullshit
##         PAGES.appendRow(
##             match=None,
##             super=home,
##             lang=de,
##             title="Bullshit Bingo",
##             abstract=bullshit.abstract(),body=bullshit.body())



        

##     EUR = CURR.peek('EUR')
##     BEF = CURR.peek('BEF')

    
##     q = PARTNERS.query('name firstName title email phone city currency')
    
##     luc = q.appendRow('Saffre','Luc','Herrn',
##                       'luc.saffre@gmx.net', '6376783', tallinn)
##     assert luc.id == 1 # "Saffre"
##     assert luc.name == 'Saffre'
##     assert luc.city == tallinn, \
##              "%s != %s" % (repr(luc.city), repr(tallinn))
    
##     #PARTNERS.flush()
##     luc = PARTNERS.peek(1)
##     assert luc.id == 1 # "Saffre"
##     assert luc.name == 'Saffre'
##     assert luc.city == tallinn

##     # fictive persons
##     q.appendRow('Arens'   ,'Andreas'  , "Herrn",
##                 'andreas@arens.be', '087.55.66.77', eupen, BEF)
##     q.appendRow('Ausdemwald','Anton'      , "Herrn",
##                 'ausdem@hotmail.com', None, aachen, EUR)
##     q.appendRow('Bodard'      ,'Henri'    , "Dr.",
##                 None, None,verviers, BEF)
##     q.appendRow('Eierschal' ,'Emil'   , "Herrn",
##                 None, None,eupen, EUR)
##     q.appendRow('Eierschal' ,'Erna'   , "Frau",
##                 None, None,eupen,EUR)
##     q.appendRow('Großmann'  ,'Gerd'   , "Herrn",
##                 None, None,eupen,EUR)
##     q.appendRow('Freitag'     ,'Frédéric' , "Herrn",
##                 None, None,eupen)

##     q = PARTNERS.query('name zip street house box city')
##     #q.appendRow('Lino Partners')
##     rumma = q.appendRow('Rumma & Ko OÜ','10115', 'Tartu mnt.','71','5',
##                         tallinn)
##     girf = q.appendRow('Girf OÜ','10621','Laki',"16", None,
##                        tallinn)
##     pac = q.appendRow('PAC Systems PGmbH','4700','Hütte',"79" , None,
##                       eupen)
##     q.appendRow('Eesti Telefon','13415','Sõpruse pst.',"193", None,
##                 tallinn)

##     assert rumma.name == "Rumma & Ko OÜ"
##     assert rumma.nation == eesti, \
##            "%s != %s" % (repr(rumma.nation), repr(eesti))



##     # personalities, authors...
##     q = AUTHORS.query('name firstName' )
##     q.appendRow( 'Gates'         ,'Bill') #       ,usa)
##     q.appendRow( 'Huxley'    ,'Aldous') #     ,None)
##     q.appendRow( 'Tolkien'   ,'J.R.R.') #     ,None)
##     q.appendRow( 'Watzlawick','Paul') #       ,usa)
##     q.appendRow( 'Bisset'    ,'Donald') #     ,None)
##     q.appendRow( 'Meves'         ,'Christa') #    ,None)
##     q.appendRow( 'Brel'      ,'Jacques') #    ,belgique)
##     brassens = \
##     q.appendRow( 'Brassens' ,'Georges') #    ,belgique)
##     q.appendRow( 'Lorenz'    ,'Konrad') #     ,deutschland)
##     q.appendRow( 'Zink'      ,'Jörg') #       ,deutschland)
##     # q.appendRow( 'Robinson'   ,'Larry H.'  ,None, None, None)
##     anon = q.appendRow('Anonymus' ,None) #   ,None)
##     lauster = \
##     q.appendRow( 'Lauster'  ,'Peter') 


    

##     q = ORGS.query('name')
##     q.appendRow('Microsoft Corporation')
##     #q.appendRow('')

##     sess.commit()

##     if sess.schema.plugins.SalesPlugin.isActive():
##         p = PARTNERS.peek(3)
##         q = sess.query(Journals,"id name tableName")
##         jnl = q.appendRow("OUT","outgoing invoices","INVOICES")
        
##         PRODUCTS = sess.query(Products)
##         chair = PRODUCTS.appendRow(id=3,name="Chair",price=12)
##         table = PRODUCTS.appendRow(id=16,name="Table",price=56)
##         assert table.name =="Table"
        # PRODUCTS.commit()

##         INVOICES = sess.query(Invoices)
##         inv = INVOICES.appendRow(jnl=jnl,seq=1,
##                                          partner=p,
##                                          date=ND(20030822))
##         inv.lines.appendRow(product=chair,qty=4)
##         inv.lines.appendRow(product=table,qty=1)
##         #inv.register()
##         assert len(inv.lines) == 2
##         sess.commit()


##     if sess.schema.plugins.QuotesPlugin.isActive():
##      q = PUBTYPES.query('id name typeRefPrefix pubRefLabel')
##      q.appendRow("book",'Book','ISBN: ','page')
##      q.appendRow("url",'Web Page','http:',None)
##      q.appendRow("CD",'CompactDisc','cddb: ','track')
##      q.appendRow("article",'Article','','page')

##         q = QUOTES.query('lang abstract author')

##         q.appendRow(fr, """Entre nous soit dit, bonnes gens:
##         pour reconnaître que l'on est pas intelligent il faudrait
##         l'être. """, brassens)

##         q.appendRow(de, """\
## Körper, Geist und Seele sind die drei Bereiche des Menschen. Der
## Körper sollte gesund sein, der Geist intelligent, und die Seele - das
## Kostbarste und Wichtigste - sollte frei sein. Dann kann das Leben
## gelingen und zum Geschenk werden.\
## """,lauster)


##         q.appendRow(en, """\
## It is much easier to suggest solutions
## when you know nothing about the problem.
## """, anon)

##         q.appendRow(en,"""\
## Many people are desperately looking for some wise advice which will
## recommend that they do what they want to do.    
## """, anon)

##         q.appendRow(en, """Carelessly planned projects take
##         three times longer to complete than expected.  Carefully planned
##         projects take four times longer to complete than expected,
##         mostly because the planners expect their planning to reduce the
##         time it takes. """,anon)

##         q.appendRow(en, """Don't believe everything you hear or
##         anything you say.""",anon)

##         a = AUTHORS.appendRow(firstName="Henry Louis",
##                                      name="Mencken")
##         q = a.quotesByAuthor.query('lang abstract')
##         quote = q.appendRow(en,"""\
## An idealist is one who, on noticing that a rose smells better than a
## cabbage, concludes that it will also make better soup.
## """)
##         assert quote.author.name == "Mencken"
##         quote = q.appendRow(en,"""\
## Conscience is the inner voice that warns us that someone may be looking.        
## """)
##         # http://www.io.com/~gibbonsb/mencken.html
##         #a.events.appendRow()

##     if sess.schema.plugins.ProjectPlugin.isActive():
##         p1 = PROJECTS.appendRow(title="Project 1")
##         p2 = PROJECTS.appendRow(title="Project 2")
##         p3 = PROJECTS.appendRow(title="Project 3")
##         p11 = PROJECTS.appendRow(title="Project 1.1",super=p1)
##         p12 = PROJECTS.appendRow(title="Project 1.2",super=p1)
##         p13 = PROJECTS.appendRow(title="Project 1.3",super=p1)
##         p131 = PROJECTS.appendRow(title="Project 1.3.1",super=p13)
##         p132 = PROJECTS.appendRow(title="Project 1.3.2",super=p13)
##         p1321 = PROJECTS.appendRow(title="Project 1.3.2.1",super=p132)
##         p1322 = PROJECTS.appendRow(title="Project 1.3.2.2",super=p132)
        

##     if sess.schema.plugins.JokesPlugin.isActive():
##         from lino.schemas.sprl.data import quotes_de
##         quotes_de.populate(sess)
##         sess.commit()

##     if False:
##         # cannot appendRow with value outside of leadTable:
##         QUOTES
##         q = QUOTES.query('lang abstract author.firstName author.name')
##         q.appendRow(en,
##                     """Trusting a scientist on questions of metaphysics is like paying someone else to worship God for you.""",\
##                     "Bill","Welton"\
##                     )


