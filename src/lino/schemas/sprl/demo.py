# coding: latin1

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


import os
from lino import adamo
#from lino.schemas.sprl.sprl import makeSchema
from lino.schemas.sprl import sprl, tables 
from lino.tools.normalDate import ND


def makeSchema(populate=True,
               big=False,
               withDemoData=True,
               withJokes=False,
               **kw):
    schema = sprl.makeSchema(**kw)
    if populate:
        if withJokes:
            schema.addPopulator(JokesPopulator(label="Weisheiten"))
        elif withDemoData:
            schema.addPopulator(DemoPopulator(big=big,
                                              label="StandardDemo"))
        else:
            schema.addPopulator(Populator(big=big,
                                          label="Standard"))
    return schema
            
            
def startup(filename=None,
            langs=None,
            **kw):
    schema = makeSchema(**kw)
    sess = schema.quickStartup(langs=langs, filename=filename)
    
        #from lino.schemas.sprl.data import demo1
        #demo1.populate(sess)
        
    return sess


# very deprecated name for startup:
# getDemoDB = beginSession

# deprecated name for startup:
beginSession = startup




class Populator(adamo.Populator):
    def __init__(self,
                 big=False,**kw
                 #withDemoData=False,
                 #withJokes=False,
                 ):
        self.big = big
        adamo.Populator.__init__(self,**kw)
        #self.withDemoData = withDemoData
        #self.withJokes = withJokes
        
    def populateUsers(self,q):
        q = q.query('id firstName name')
        q.appendRow("luc", "Luc", "Saffre")
        q.appendRow("james", "James", "Bond")
        
    def populateCurrencies(self,q):
        q.setBabelLangs('en')
        self.EUR = q.appendRow(id="EUR",name="Euro")
        self.BEF = q.appendRow(id="BEF",name="Belgian Franc")
        self.USD = q.appendRow(id="USD",name="US Dollar")
    
    def populatePartnerTypes(self,q):
        q = q.query('id name')
        q.setBabelLangs('en de fr')
        q.appendRow('c',('Customer', 'Kunde', 'Client'))
        q.appendRow('s',('Supplier', 'Lieferant', 'Fournisseur'))
        q.appendRow('m',('Member', 'Mitglied', "Membre"))
        q.appendRow('e',('Employee', 'Angestellter', "Employé"))
        q.appendRow('d',('Sponsor', 'Sponsor', "Sponsor"))
	
        
    
    def populateNations(self,q):
        if self.big:
            from lino.schemas.sprl.data import nations
            nations.populate(q)
            if q.getDatabase().supportsLang("de"):
                from lino.schemas.sprl.data import nations_de
                nations_de.populate(q)
            
        else:
            q = q.query('id name')
            q.setBabelLangs('en')
            q.appendRow("ee","Estonia")
            q.appendRow("be","Belgium")
            q.appendRow("de","Germany")
            q.appendRow("fr","France")
            q.appendRow("us","United States of America")

        self.belgique = q.peek('be')
        self.eesti = q.peek('ee')
        self.deutschland = q.peek('de')

    
    def populateCities(self,q):
        if self.big:
            from lino.schemas.sprl.data import cities_be
            cities_be.populate(q)
        else:
            q = q.query('name',nation=self.belgique)
            q.appendRow(name="Bruxelles")
            q.appendRow("Brugge")
            q.appendRow("Eupen")
            q.appendRow("Kettenis")
            q.appendRow("Kelmis")
            q.appendRow("Raeren")
            q.appendRow("Mons")
            q.appendRow("Liège")
            q.appendRow("Charleroi")
            q.appendRow("Verviers")

        self.eupen = q.findone(name="Eupen")
        self.verviers = q.findone(name="Verviers")
            
        q = q.query('name inhabitants', nation=self.eesti)
        self.tallinn = q.appendRow("Tallinn",442000)
##         assert tallinn.inhabitants == 442000
##         assert tallinn.nation == self.eesti
##         assert tallinn.nation.id == "ee"
##         assert tallinn.getRowId() == ['ee',1], \
##                  "%s != ['ee',1]" % repr(tallinn.getRowId())

        q.appendRow("Tartu",109100)
        #q.appendRow("Otepää")
        q.appendRow("Narva",80300)
        q.appendRow("Kilingi-Nõmme",2490)
        q.appendRow("Pärnu",52000)
        q.appendRow("Rakvere",18096)
        q.appendRow("Viljandi",20756)
        q.appendRow("Ruhnu",58)
        q.appendRow("Vigala",1858)
        q.appendRow("Kohtla-Järve",70800)

        q = self.deutschland.cities.query('name') 
        self.aachen = q.appendRow("Aachen")
        q.appendRow("Köln")
        q.appendRow("Berlin")
        q.appendRow("Bonn")
        q.appendRow("München")
        q.appendRow("Eschweiler")
        q.appendRow("Alfter-Oedekoven")
    

            

    def populatePubTypes(self,q):
        q.setBabelLangs('en de')
        q = q.query('id name typeRefPrefix pubRefLabel')
        q.appendRow("book",
                    ('Book','Buch')        ,
                    'ISBN: ',
                    ('page','Seite')  )
        q.appendRow("url" , ('Web Page','Webseite')    ,
                    'http:' , ( None, None)   )
        q.appendRow("cd"  , ('CompactDisc', 'CD') , 'cddb: ',
                    ('track','Stück') )
        q.appendRow("art" , ('Article','Artikel')     ,
                    ''      , ('page','Seite')  )
        q.appendRow("mag" , ('Magazine','Zeitschrift')    ,
                    ''      , ('page','Seite')  )
        q.appendRow("sw"  , ('Software','Software')    ,
                    ''      , (None,None)    )


    def populateAuthorEventTypes(self,q):
        q = q.query('id name')
        q.setBabelLangs('en de')
        q.appendRow(1,('born','geboren'))
        q.appendRow(2,('died','gestorben'))
        q.appendRow(3,('married','Heirat'))
        q.appendRow(4,('school','Schulabschluss'))
        q.appendRow(5,('other','Sonstige'))	

    def populateLanguages(self,q):
        q = q.query('id name')
        if self.big:
            from lino.schemas.sprl.data import languages
            languages.populate(q)
        else:
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

        for lng in ('en','de','et','fr'):
            setattr(self,lng,q.peek(lng))
            
    def populateProjectStati(self,q):
        q = q.query('id name')
        q.setBabelLangs('en de')
        q.appendRow('T',('to do','zu erledigen'))
        q.appendRow('D',('done','erledigt'))
        q.appendRow('W',('waiting','wartet'))
        q.appendRow('A',('abandoned','storniert'))
        q.appendRow('S',('sleeping','schläft'))


class DemoPopulator(Populator):
    
        
    def populateAuthors(self,q):
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
        q.appendRow( 'Zink'      ,'Jörg') #       ,deutschland)
        # q.appendRow( 'Robinson'   ,'Larry H.'  ,None, None, None)
        self.anon = q.appendRow('Anonymus' ,None) #   ,None)
        self.lauster = q.appendRow( 'Lauster'  ,'Peter') 

        self.mencken = q.appendRow(firstName="Henry Louis",
                                   name="Mencken")

        

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
    
    def populateJournals(self,q):
        q = q.query("id name tableName")
        self.OUT = q.appendRow("OUT","outgoing invoices","INVOICES")
        
    def populateProducts(self,q):
        self.chair = q.appendRow(id=3,name="Chair",price=12)
        self.table = q.appendRow(id=16,name="Table",price=56)
        
    def populateInvoices(self,q):
        self.invoice = q.appendRow(jnl=self.OUT,
                                   partner=self.anton,
                                   date=ND(20030822))
    def populateInvoiceLines(self,q):
        q.appendRow(invoice=self.invoice,product=self.chair,qty=4)
        q.appendRow(invoice=self.invoice,product=self.table,qty=1)

        
    def populateQuotes(self,q):
        q = q.query('lang abstract author')

        q.appendRow(self.fr, """Entre nous soit dit, bonnes gens:
        pour reconnaître que l'on est pas intelligent il faudrait
        l'être. """, self.brassens)

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

        q.appendRow(self.en, """Carelessly planned projects take
        three times longer to complete than expected.  Carefully planned
        projects take four times longer to complete than expected,
        mostly because the planners expect their planning to reduce the
        time it takes. """,self.anon)

        q.appendRow(self.en, """Don't believe everything you hear or
        anything you say.""",self.anon)

        q = self.mencken.quotesByAuthor.query('lang abstract')
        quote = q.appendRow(self.en,"""\
An idealist is one who, on noticing that a rose smells better than a
cabbage, concludes that it will also make better soup.
""")
        assert quote.author.name == "Mencken"
        quote = q.appendRow(self.en,"""\
Conscience is the inner voice that warns us that someone may be looking.        
""")
        # http://www.io.com/~gibbonsb/mencken.html
        #a.events.appendRow()

        if False:
            # cannot appendRow with value outside of leadTable:
            q = q.query('lang abstract author.firstName author.name')
            q.appendRow(self.en,
                        """Trusting a scientist on questions of metaphysics is like paying someone else to worship God for you.""",\
                    "Bill","Welton"\
                    )


    def populatePartners(self,q):

##         tallinn = q.getSession().query(Cities).findone(
##             nation=self.eesti,
##             name="Tallinn")

##         # todo: eupen = belgique.cities.findone(name="Eupen")
##         eupen = q.getSession().query(Cities).findone(
##             nation=self.belgique,
##             name="Eupen")

##         verviers = q.getSession().query(Cities).findone(
##             nation=self.belgique,
##             name="Verviers")

##         aachen = q.getSession().query(Cities).findone(
##             nation=deutschland,
##             name="Aachen")


        q = q.query(
            'name firstName title email phone city currency')

        self.luc = q.appendRow(
            'Saffre','Luc','Herrn',
            'luc.saffre@gmx.net', '6376783', self.tallinn)
##         assert luc.id == 1 # "Saffre"
##         assert luc.name == 'Saffre'
##         assert luc.city == tallinn, \
##                  "%s != %s" % (repr(luc.city), repr(tallinn))

        #PARTNERS.flush()
        #luc = q.peek(1)
        #assert luc.id == 1 # "Saffre"
        #assert luc.name == 'Saffre'
        #assert luc.city == tallinn

        # fictive persons
        q.appendRow('Arens'   ,'Andreas'  , "Herrn",
                    'andreas@arens.be', '087.55.66.77',
                    self.eupen, self.BEF)
        self.anton = q.appendRow(
            'Ausdemwald','Anton'      , "Herrn",
            'ausdem@hotmail.com', None, self.aachen, self.EUR)
        q.appendRow('Bodard'      ,'Henri'    , "Dr.",
                    None, None,self.verviers, self.BEF)
        q.appendRow('Eierschal' ,'Emil'   , "Herrn",
                    None, None,self.eupen, self.EUR)
        q.appendRow('Eierschal' ,'Erna'   , "Frau",
                    None, None,self.eupen,self.EUR)
        q.appendRow('Großmann'  ,'Gerd'   , "Herrn",
                    None, None,self.eupen,self.EUR)
        q.appendRow('Freitag'     ,'Frédéric' , "Herrn",
                    None, None,self.eupen)

        q = q.query('name zip street house box city')

        rumma = q.appendRow(
            'Rumma & Ko OÜ','10115', 'Tartu mnt.','71','5',
            self.tallinn)
        girf = q.appendRow(
            'Girf OÜ','10621','Laki',"16", None, self.tallinn)
        pac = q.appendRow(
            'PAC Systems PGmbH','4700','Hütte',"79" , None, self.eupen)
        q.appendRow(
            'Eesti Telefon','13415','Sõpruse pst.',"193", None,
            self.tallinn)

        assert rumma.name == "Rumma & Ko OÜ"
        assert rumma.nation == self.eesti, \
               "%s != %s" % (repr(rumma.nation), repr(self.eesti))

            
            
    
class JokesPopulator(Populator):

        
    def populateQuotes(self,q):
        from lino.schemas.sprl.data import quotes_de
        quotes_de.populate(q,self.de)
        #print "%d Weisheiten" % len(q)
            
