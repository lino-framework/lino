## Copyright 2005-2006 Luc Saffre 

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


from lino.adamo.ddl import *

from lino.apps.pinboard.babel import Language

SEX = STRING(width=1)


class Contact(StoredDataRow):
    "abstract"
    def initTable(self,table):
        table.addField('email',EMAIL,
                       label="e-mail",
                       doc="Primary e-mail address")
        table.addField('phone',STRING,
                       doc="phone number")
        table.addField('gsm',STRING,
                       label="mobile phone",
                       doc="mobile phone number")
        table.addField('fax',STRING, doc="fax number")
        table.addField('website',URL, doc="web site")

    def __str__(self):
        return self.name
        
class Address(StoredDataRow):
    "abstract"
    def initTable(self,table):
        table.addPointer('nation',Nation)
        table.addPointer('city',City)
        table.addField('zip',STRING)
        table.addField('street',STRING)
        table.addField('house',INT)
        table.addField('box',STRING)
        
    def after_city(self):
        if self.city is not None:
            self.nation = self.city.nation

class Organisation(Contact,Address):
    "An Organisation is any named group of people."
    tableName="Organisations"
    def initTable(self,table):
        table.addField('id',ROWID,\
                      doc="the internal id number")
        Contact.initTable(self,table)
        Address.initTable(self,table)
        table.addField('name',STRING)
        #table.addView('std',columnNames="name email phone website")

class OrganisationsReport(DataReport):
    "former std view"
    leadTable=Organisation
    columnNames="name email phone website"

class Person(StoredDataRow): #(Contact,Address):
    "A Person describes a specific physical human."
    tableName="Persons"
    def initTable(self,table):
        table.addField('id',ROWID)
        table.addField('name',STRING)
        table.addField('firstName',STRING)
        table.addField('sex',SEX)
        table.addField('birthDate',STRING(width=8))
        
        # table.setFindColumns("name firstName")

        #self.setColumnList("name firstName id")
        table.setOrderBy('name firstName')
        #table.addView('std',columnNames="name firstName id")

    def __str__(self):
        if self.firstName is None:
            return self.name
        return self.firstName+" "+self.name

    def validate(self):
        if (self.firstName is None) and (self.name is None):
            raise DataVeto(
                "Either name or firstName must be specified")

class PersonsReport(DataReport):
    "former std view"
    leadTable=Person
    columnNames="name firstName id"
    

class User(Person):
    "People who can access this database"
    tableName="Users"
    def initTable(self,table):
        Person.initTable(self,table)
        #self.addField('id',STRING,label="Username")
        i=table.getRowAttr('id')
        i.setType(STRING)
        i.setLabel("Username")
        #self.setField('id',STRING,label="Username")
        table.addField('pwd',PASSWORD)

class UsersReport(DataReport):
    leadTable=User
    

class Partner(Contact,Address):
    """A Person or Organisation with whom I have business contacts.
    """
    tableName="Partners"
    def initTable(self,table):
        table.addField('name',STRING)
        table.addField('firstName',STRING)
        Contact.initTable(self,table)
        Address.initTable(self,table)
        table.addField('id',ROWID)
        table.addPointer('type',PartnerType)
        #.setDetail('partnersByType',orderBy='name firstName')
        table.addField('title',STRING)
        table.addField('logo',LOGO)
        #self.addPointer('org',Organisation)
        #self.addPointer('person',Person)
        table.addPointer('lang',Language)
        #table.addView("std","name firstName email phone gsm")
        
    def validate(self):
        if self.name is None:
            raise("name must be specified")

    def __str__(self):
        if self.firstName is None:
            return self.name
        return self.firstName+" "+self.name
    
        
class PartnersReport(DataReport):
    "former std view"
    leadTable=Partner
    columnNames="name firstName email phone gsm"
    
class PartnerType(BabelRow):
    
    tableName="PartnerTypes"
    
    def initTable(self,table):
        table.addField('id',STRING)
        BabelRow.initTable(self,table)
        

    def validatePartner(self,partner):
        pass
    
class PartnerTypesReport(DataReport):
    leadTable=PartnerType
    
class Nation(BabelRow):
    tableName="Nations"
    def initTable(self,table):
        
        table.addField('id',STRING(width=2))
        BabelRow.initTable(self,table)
        table.addField('area',INT(width=8))
        table.addField('population',INT)
        table.addField('curr',STRING)
        table.addField('isocode',STRING(3))
        table.addDetail('cities',City,'nation')
        table.addDetail('partners_by_nation',Partner,'nation')
        
        #table.addView('std',columnNames="name isocode id")

    def validate_id(value):
        if len(value) != 2:
            raise DataVeto("must be 2 chars")
    validate_id = staticmethod(validate_id)

##     def cities(self,columnNames=None,orderBy='name',**kw):
##         kw['nation']=self
##         return self.detail(City,columnNames,
##                            orderBy=orderBy,
##                            **kw)
    
##     def cities(self,*args,**kw):
##         kw['nation']=self
##         return self.detail(City,*args,**kw)
    
##     def partners_by_nation(self,*args,**kw):
##         kw['nation']=self
##         return self.detail(Partner,*args,**kw)
        
##     def validate(self):
##         if len(self.id) != 2:
##             #return "Nation.id must be 2 chars"
##             raise DataVeto("Nation.id must be 2 chars")
        
class NationsReport(DataReport):
    leadTable=Nation
    columnNames="name isocode id"
        
class City(StoredDataRow):
    
    tableName="Cities"
    
    def initTable(self,table):
        table.addField('id',ROWID)
        table.addPointer('nation',Nation)
##         table.addPointer('nation',Nation).setDetail('cities',
##                                                     orderBy='name')
        
        table.addField('name',STRING)
        table.addField('zipCode',STRING)
        table.addField('inhabitants',INT(minWidth=5,maxWidth=9))
        
        table.setPrimaryKey("nation id")
        # complex primary key used by test cases
        #table.addView('std',columnNames="name nation zipCode")
        
    def __str__(self):
        if self.nation is None:
            return self.name
        return self.name + " (%s)" % self.nation.id


class CitiesReport(DataReport):
    leadTable=City
    columnNames="name nation zipCode"



class AddressBook(Schema):
    
    tableClasses = ( Language,
                     Nation, City,
                     Organisation, Person,
                     Partner, PartnerType)

    
        
    

TABLES = (Language,
          Nation, City,
          Organisation, Person, User,
          Partner, PartnerType)

REPORTS = (NationsReport, CitiesReport, OrganisationsReport,
           PersonsReport, UsersReport, PartnersReport,
           PartnerTypesReport)


__all__ = [t.__name__ for t in TABLES]
__all__.append('TABLES')

__all__ += [t.__name__ for t in REPORTS]
__all__.append('REPORTS')
__all__.append('AddressBook')


#__all__ = filter(lambda x: x[0] != "_", dir())
