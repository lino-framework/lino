# coding: latin1

## Copyright 2003-2006 Luc Saffre

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
from lino import config
from lino.adamo import ddl
from lino.adamo.datatypes import itod
#from lino.apps.addrbook.addrbook_schema import AddressBookSchema, City
#from lino.apps.addrbook import tables
from contacts_tables import *
#, City, Nation

rtlib_path=config.get(config.DEFAULTSECT,'rtlib_path')


def startup(filename=None,
            langs=None,
            populate=True,
            dump=None,
            big=False,
            withDemoData=True,
            **kw):
    schema=ContactsSchema(**kw)
    ctx=schema.quickStartup(langs=langs,
                            filename=filename,
                            dump=dump)
    if populate:
        ctx.populate(StandardPopulator(big=big))
        if withDemoData:
            ctx.populate(DemoPopulator())

##     if populate:
##         if withDemoData:
##             sess.populate(DemoPopulator(big=big,
##                                         label="StandardDemo"))
##         else:
##             sess.populate(Populator(big=big,
##                                     label="Standard"))

    return ctx


class StandardPopulator(ddl.Populator):
    
    #dataRoot=os.path.abspath(os.path.join(
    #    os.path.dirname(__file__),
    #    "..","..","..","..","data"))

    #dataRoot = lino.rtlib_path
    
    def __init__(self, big=False,**kw):
        self.big = big
        ddl.Populator.__init__(self,None,**kw)
        
    def populateUsers(self,q):
        q = q.query('id firstName name')
        q.appendRow("luc", "Luc", "Saffre")
        q.appendRow("james", "James", "Bond")
        
    
    def populateNations(self,q):
        if self.big:
            #q.startDump()
            q.appendfrom(os.path.join(rtlib_path,
                                      "data","nations.txt"))
            #print q.stopDump()
            #q.query("id population area name").appendfrom(
            #    os.path.join(self.dataRoot,"nations.txt"))
            #from lino.data import nations
            #nations.populate(q)
            #if q.getDatabase().supportsLang("de"):
            #    from lino.schemas.sprl.data import nations_de
            #    nations_de.populate(q)
            
        else:
            q.setBabelLangs('en')
            #qr = q.query('id name cities')
            qr = q.query('id name')
            qr.appendRow("ee","Estonia")
            qr.appendRow("be","Belgium")
            qr.appendRow("de","Germany")
            qr.appendRow("fr","France")
            qr.appendRow("us","United States of America")

        self.belgique = q.peek('be')
        self.eesti = q.peek('ee')
        self.deutschland = q.peek('de')

    
    def populateCities(self,q):
        if self.big:
            self.deutschland.cities().appendfrom(
                os.path.join(rtlib_path,
                             "data","cities_de.txt"))

            
            self.belgique.cities().appendfrom(
                os.path.join(rtlib_path,"data","cities_be.txt"))

            #from lino.schemas.sprl.data import cities_de
            #cities_de.populate(q)
            #from lino.schemas.sprl.data import cities_be
            #cities_be.populate(q)
        else:
            #r = self.belgique.cities.query('name inhabitants')
            r = self.belgique.cities('name inhabitants')
            r.appendRow("Bruxelles",1004239)
            r.appendRow("Brugge",116848)
            r.appendRow("Eupen",17872)
            #r.appendRow("Kettenis")
            r.appendRow("Kelmis",10175)
            r.appendRow("Raeren",9933)
            r.appendRow("Mons",90992)
            r.appendRow(u"Liège",185608)
            r.appendRow("Charleroi",200983)
            r.appendRow("Verviers",52739)

            q = self.deutschland.cities('name') 
            q.appendRow("Aachen")
            q.appendRow(u"Köln")
            q.appendRow("Berlin")
            q.appendRow("Bonn")
            q.appendRow(u"München")
            q.appendRow("Eschweiler")
            q.appendRow("Alfter-Oedekoven")
    
            

        q = q.query('name inhabitants', nation=self.eesti)
        q.appendRow("Tallinn",442000)
##         assert tallinn.inhabitants == 442000
##         assert tallinn.nation == self.eesti
##         assert tallinn.nation.id == "ee"
##         assert tallinn.getRowId() == ['ee',1], \
##                  "%s != ['ee',1]" % repr(tallinn.getRowId())

        q.appendRow("Tartu",109100)
        #q.appendRow(u"Otepää")
        q.appendRow("Narva",80300)
        q.appendRow(u"Kilingi-Nõmme",2490)
        q.appendRow(u"Pärnu",52000)
        q.appendRow("Rakvere",18096)
        q.appendRow("Viljandi",20756)
        q.appendRow("Ruhnu",58)
        q.appendRow("Vigala",1858)
        q.appendRow(u"Kohtla-Järve",70800)


            
    def populateFunctions(self,q):
        q.setBabelLangs('en de fr')
        q = q.query('id name')
        q.appendRow('dir', ('Director', 'Direktor', 'Directeur'))
        q.appendRow('mbr', ('Member', 'Mitglied', 'Membre'))
        q.appendRow('sales', ('Sales representant', 'Vertreter',
                              u'Représentant'))
        
    def populatePartnerTypes(self,q):
        q.setBabelLangs('en de fr')
        q = q.query('id name')
        q.appendRow('c',('Customer', 'Kunde', 'Client'))
        q.appendRow('s',('Supplier', 'Lieferant', 'Fournisseur'))
        q.appendRow('m',('Member', 'Mitglied', "Membre"))
        q.appendRow('e',('Employee', 'Angestellter', u"Employé"))
        q.appendRow('d',('Sponsor', 'Sponsor', "Sponsor"))
	
        
MALE='m'
FEMALE='f'


class DemoPopulator(ddl.Populator):
    
        
    def populatePersons(self,q):
        #self.luc=q.appendRow(firstName="Luc",name="Saffre",sex=MALE)
        self.andreas=q.appendRow(firstName="Andreas",name="Arens",
                                 sex=MALE)
        self.anton=q.appendRow(firstName="Anton",name="Ausdemwald",
                               sex=MALE)
        self.emil=q.appendRow(firstName="Emil",name="Eierschal",
                              sex=MALE)
        self.henri=q.appendRow(firstName="Henri",name="Bodard",
                              sex=MALE)
        self.erna=q.appendRow(firstName="Erna",name="Eierschal",
                              sex=FEMALE)
        self.gerd=q.appendRow(firstName="Gerd",name=u"Großmann",
                              sex=MALE)
        self.fred=q.appendRow(firstName=u"Frédéric",name="Freitag",
                              sex=MALE)
        self.tonu=q.appendRow(firstName=u"Tõnu",name="Tamm",
                              sex=MALE)
        self.kati=q.appendRow(firstName="Kati",name="Kask",
                              sex=FEMALE)
        self.jean=q.appendRow(firstName="Jean",name="Dupont",
                              sex=MALE)
        self.joseph=q.appendRow(firstName="Joseph",name="Dupont",
                                sex=MALE)
        self.julie=q.appendRow(firstName="Julie",name="Dupont",
                                sex=FEMALE)
        
    def populateOrganisations(self,q):
        self.rumma = q.appendRow(name=u'Rumma & Ko OÜ')

        self.girf = q.appendRow(name=u'Girf OÜ')
        
        self.pac = q.appendRow(name=u'PAC Systems PGmbH')
        self.elion = q.appendRow(name=u'Elion')

    def populateContacts(self,q):

        cities = q.getContext().query(City)
        self.eupen = cities.findone(name="Eupen")
        self.verviers = cities.findone(name="Verviers")
        self.tallinn = cities.findone(name="Tallinn")
        self.aachen = cities.findone(name="Aachen")


        qr = q.query('person title email phone city')

        qr.appendRow(self.andreas, "Herrn",
                     'andreas@arens.be',
                     '087.55.66.77', self.eupen)
        qr.appendRow(self.anton , "Herrn",
                     'ausdem@kotmail.com',
                     None, self.aachen)
        qr.appendRow(self.henri, "Dr.", None, None,self.verviers)
        qr.appendRow(self.emil, "Herrn", None, None,self.eupen)
        qr.appendRow(self.erna  , "Frau", None, None,self.eupen)
        qr.appendRow(self.gerd  , "Herrn",None, None,self.eupen)
        qr.appendRow(self.fred, "Herrn", None, None,self.eupen)
        qr.appendRow(self.tonu, "Lp.", None, None,self.tallinn)
        qr.appendRow(self.kati, "Lp.", None, None,self.tallinn)

        qr = q.query('org zip street house box city website')

        rumma = qr.appendRow(
            self.rumma,'10115', 'Tartu mnt.',71,'5',
            self.tallinn,
            "http://www.saffre-rumma.ee")

        assert rumma.name == u"Rumma & Ko OÜ"
        assert rumma.nation.id == "ee", "%r!='ee'" % rumma.nation

        qr.appendRow(
            self.girf,'10621','Laki',16, None, self.tallinn,
            "http://www.girf.ee"
            )
        qr.appendRow(self.pac,'4700',u'Hütte',79 , None, self.eupen,
                     "http://www.pacsystems.be"
                     )
        qr.appendRow(
            self.elion,'13415',u'Sõpruse pst.',193, None,
            self.tallinn,
            "http://www.elion.ee"
            )

            
            
    
