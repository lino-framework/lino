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
20040513

20050228 : setBabelLangs() while rows are locked is no longer
supported.


"""

from lino.misc.tsttools import TestCase, main
from lino.adamo.ddl import *
#from lino.adamo.exceptions import InvalidRequestError
from lino import adamo


class Nation(StoredDataRow):
    tableName="Nations"
    def initTable(self,table):
        table.addField('id',STRING(width=2))
        table.addBabelField('name',STRING)
        table.addField('area',INT)
        table.addField('population',INT)
        table.addField('curr',STRING)
        table.addField('isocode',STRING)

class City(StoredDataRow):
    tableName="Cities"
    
    def initTable(self,table):
        table.addField('id',ROWID)
        table.addPointer('nation',Nation).setDetail('cities',
                                                    orderBy='name')
        table.addField('name',STRING)
        table.addField('zipCode',STRING)
        table.addField('inhabitants',INT)
        table.setPrimaryKey("nation id")
        
    def __str__(self):     
        if self.nation is None:
            return self.name
        return self.name + " (%s)" % self.nation.id
        

## class Contacts:
##     def init(self):
##         self.addField('email',EMAIL)
##         self.addField('phone',STRING)

## class Addresses:
##     def init(self):
##         self.addPointer('nation',Nations)
##         self.addPointer('city',Cities)
##         self.addField('street',STRING)

##     def after_city(self,row):
##         if row.city is not None:
##             row.nation = row.city.nation

## class Organisations(Table,Contacts,Addresses):
##     "An Organisation is any named group of people."
##     def init(self):
##         self.addField('id',ROWID, doc="the internal id number")
##         self.addField('name',STRING)
##         Contacts.init(self)
##         Addresses.init(self)


class MySchema(Schema):
    
    def setupSchema(self):
        self.addTable(Nation)
        self.addTable(City)
        #self.addTable(Organisation)
        


class Case(TestCase):
    
    def test01(self):

        schema = MySchema()

        sess = schema.quickStartup(langs='en de fr')

        #sess.setBabelLangs('en')
        
        ds = sess.query(Nation)

        be = ds.appendRow(id="be", name="Belgium")

        sess.setBabelLangs('de')
        self.assertEqual(be.name,None)
        be.lock()
        be.name = "Belgien"
        be.unlock()
        
        sess.setBabelLangs('fr')
        self.assertEqual(be.name,None)
        be.lock()
        be.name = "Belgique"
        be.unlock()
        
        
        be = sess.query(Nation).peek('be')

        
        eupen = sess.query(City).appendRow(nation=be,name="Eupen")
        
        sess.setBabelLangs('de')
        self.assertEqual(be.name,'Belgien')
        
        sess.setBabelLangs('fr')
        self.assertEqual(be.name,'Belgique')
        
        sess.setBabelLangs('en')
        self.assertEqual(be.name,'Belgium')
        
        sess.setBabelLangs('en de')
        self.assertEqual(be.name,['Belgium','Belgien'])

        sess.setBabelLangs('en fr')
        self.assertEqual(be.name,['Belgium','Belgique'])

        sess.setBabelLangs('fr de')
        self.assertEqual(be.name,['Belgique','Belgien'])
        
        try:
            sess.setBabelLangs('xx')
            self.fail("failed to raise InvalidRequestError")
        except InvalidRequestError,e:
            pass
        
        eupen.lock()
        try:
            sess.setBabelLangs('de')
            self.fail("failed to raise InvalidRequestError")
        except InvalidRequestError,e:
            pass
        eupen.unlock()
        
        
        sess.shutdown()

        

        
if __name__ == '__main__':
    main()

