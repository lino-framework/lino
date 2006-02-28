# coding: latin1

## Copyright 2003-2005 Luc Saffre

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
from lino import rtlib_path, adamo
from lino.adamo.datatypes import itod
from lino.apps.addrbook.addrbook import AddressBook
from lino.apps.addrbook import tables
#, City, Nation

def startup(filename=None, langs=None,
            populate=True,
            dump=None,
            big=False,
            withDemoData=True,
            **kw):
    schema = AddressBook(**kw)
    sess=schema.quickStartup(langs=langs, filename=filename, dump=dump)
    if populate:
        sess.populate(StandardPopulator(big=big,
                                        label="Standard"))
        if withDemoData:
            sess.populate(DemoPopulator(label="StandardDemo"))

##     if populate:
##         if withDemoData:
##             sess.populate(DemoPopulator(big=big,
##                                         label="StandardDemo"))
##         else:
##             sess.populate(Populator(big=big,
##                                     label="Standard"))

    return sess



class StandardPopulator(adamo.Populator):
    
    #dataRoot=os.path.abspath(os.path.join(
    #    os.path.dirname(__file__),
    #    "..","..","..","..","data"))

    #dataRoot = lino.rtlib_path
    
    def __init__(self, big=False,**kw):
        self.big = big
        adamo.Populator.__init__(self,None,**kw)
        
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
            qr = q.query('id name cities')
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
            self.deutschland.cities.appendfrom(
                os.path.join(rtlib_path,
                             "data","cities_de.txt"))

            
            self.belgique.cities.appendfrom(
                os.path.join(rtlib_path,
                             "data","cities_be.txt"))

            #from lino.schemas.sprl.data import cities_de
            #cities_de.populate(q)
            #from lino.schemas.sprl.data import cities_be
            #cities_be.populate(q)
        else:
            r = self.belgique.cities.query('name inhabitants')
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

            q = self.deutschland.cities.query('name') 
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


            
    def populatePartnerTypes(self,q):
        q.setBabelLangs('en de fr')
        q = q.query('id name')
        q.appendRow('c',('Customer', 'Kunde', 'Client'))
        q.appendRow('s',('Supplier', 'Lieferant', 'Fournisseur'))
        q.appendRow('m',('Member', 'Mitglied', "Membre"))
        q.appendRow('e',('Employee', 'Angestellter', u"Employé"))
        q.appendRow('d',('Sponsor', 'Sponsor', "Sponsor"))
	
        


class DemoPopulator(adamo.Populator):
    
        
    def populatePartners(self,q):

        cities = q.getSession().query(tables.City)
        self.eupen = cities.findone(name="Eupen")
        self.verviers = cities.findone(name="Verviers")
        self.tallinn = cities.findone(name="Tallinn")
        self.aachen = cities.findone(name="Aachen")

        #nations = q.getSession().query(tables.Nation)
        #self.belgique = nations.peek('be')
        #self.eesti = nations.peek('ee')
        #self.deutschland = nations.peek('de')

        
            
        qr = q.query(
            'name firstName title email phone city')

        luc = qr.appendRow(
            'Saffre','Luc','Herrn',
            'luc.saffre@gmx.net', '6376783', self.tallinn)

        # fictive persons
        qr.appendRow('Arens'   ,'Andreas'  , "Herrn",
                    'andreas@arens.be', '087.55.66.77',
                    self.eupen)
        anton = qr.appendRow(
            'Ausdemwald','Anton'      , "Herrn",
            'ausdem@kotmail.com', None, self.aachen)
        qr.appendRow('Bodard'      ,'Henri'    , "Dr.",
                    None, None,self.verviers)
        qr.appendRow('Eierschal' ,'Emil'   , "Herrn",
                    None, None,self.eupen)
        qr.appendRow('Eierschal' ,'Erna'   , "Frau",
                    None, None,self.eupen)
        qr.appendRow(u'Großmann'  ,'Gerd'   , "Herrn",
                    None, None,self.eupen)
        qr.appendRow('Freitag'     ,u'Frédéric' , "Herrn",
                    None, None,self.eupen)

        qr = q.query('name zip street house box city')

        rumma = qr.appendRow(
            u'Rumma & Ko OÜ','10115', 'Tartu mnt.',71,'5',
            self.tallinn)
        assert rumma.name == u"Rumma & Ko OÜ"
        assert rumma.nation.id == "ee", "%r!='ee'" % rumma.nation

        girf = qr.appendRow(
            u'Girf OÜ','10621','Laki',16, None, self.tallinn)
        pac = qr.appendRow(
            'PAC Systems PGmbH','4700',u'Hütte',79 , None, self.eupen)
        qr.appendRow(
            'Eesti Telefon','13415',u'Sõpruse pst.',193, None,
            self.tallinn)

            
            
    
