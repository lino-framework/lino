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
from lino.adamo.datatypes import itod
from lino.apps.addrbook.addrbook import AddressBook

def startup(filename=None, langs=None,
            populate=True,
            big=False,
            withDemoData=True,
            **kw):
    schema = AddressBook(**kw)
    sess=schema.quickStartup(langs=langs, filename=filename)
    if populate:
        if withDemoData:
            sess.populate(DemoPopulator(big=big,
                                        label="StandardDemo"))
        else:
            sess.populate(Populator(big=big,
                                    label="Standard"))

    return sess



class Populator(adamo.Populator):
    def __init__(self, big=False,**kw):
        self.big = big
        adamo.Populator.__init__(self,None,**kw)
        
    def populateUsers(self,q):
        q = q.query('id firstName name')
        q.appendRow("luc", "Luc", "Saffre")
        q.appendRow("james", "James", "Bond")
        
    
    def populateNations(self,q):
        if self.big:
            from lino.schemas.sprl.data import nations
            nations.populate(q)
            if q.getDatabase().supportsLang("de"):
                from lino.schemas.sprl.data import nations_de
                nations_de.populate(q)
            
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
            from lino.schemas.sprl.data import cities_de
            cities_de.populate(q)
            from lino.schemas.sprl.data import cities_be
            cities_be.populate(q)
        else:
            r = self.belgique.cities.query('name inhabitants')
            r.appendRow("Bruxelles",1004239)
            r.appendRow("Brugge",116848)
            r.appendRow("Eupen",17872)
            #r.appendRow("Kettenis")
            r.appendRow("Kelmis",10175)
            r.appendRow("Raeren",9933)
            r.appendRow("Mons",90992)
            r.appendRow("Liège",185608)
            r.appendRow("Charleroi",200983)
            r.appendRow("Verviers",52739)

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
    

            
    def populatePartnerTypes(self,q):
        q.setBabelLangs('en de fr')
        q = q.query('id name')
        q.appendRow('c',('Customer', 'Kunde', 'Client'))
        q.appendRow('s',('Supplier', 'Lieferant', 'Fournisseur'))
        q.appendRow('m',('Member', 'Mitglied', "Membre"))
        q.appendRow('e',('Employee', 'Angestellter', "Employé"))
        q.appendRow('d',('Sponsor', 'Sponsor', "Sponsor"))
	
        


class DemoPopulator(Populator):
    
        
    def populatePartners(self,q):

        qr = q.query(
            'name firstName title email phone city')

        self.luc = qr.appendRow(
            'Saffre','Luc','Herrn',
            'luc.saffre@gmx.net', '6376783', self.tallinn)

        # fictive persons
        qr.appendRow('Arens'   ,'Andreas'  , "Herrn",
                    'andreas@arens.be', '087.55.66.77',
                    self.eupen)
        self.anton = qr.appendRow(
            'Ausdemwald','Anton'      , "Herrn",
            'ausdem@hotmail.com', None, self.aachen)
        qr.appendRow('Bodard'      ,'Henri'    , "Dr.",
                    None, None,self.verviers)
        qr.appendRow('Eierschal' ,'Emil'   , "Herrn",
                    None, None,self.eupen)
        qr.appendRow('Eierschal' ,'Erna'   , "Frau",
                    None, None,self.eupen)
        qr.appendRow('Großmann'  ,'Gerd'   , "Herrn",
                    None, None,self.eupen)
        qr.appendRow('Freitag'     ,'Frédéric' , "Herrn",
                    None, None,self.eupen)

        qr = q.query('name zip street house box city')

        rumma = qr.appendRow(
            'Rumma & Ko OÜ','10115', 'Tartu mnt.',71,'5',
            self.tallinn)
        girf = qr.appendRow(
            'Girf OÜ','10621','Laki',16, None, self.tallinn)
        pac = qr.appendRow(
            'PAC Systems PGmbH','4700','Hütte',79 , None, self.eupen)
        qr.appendRow(
            'Eesti Telefon','13415','Sõpruse pst.',193, None,
            self.tallinn)

        assert rumma.name == "Rumma & Ko OÜ"
        assert rumma.nation == self.eesti, \
               "%s != %s" % (repr(rumma.nation), repr(self.eesti))

            
            
    
