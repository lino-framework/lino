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


from lino.adamo.ddl import *

SEX = STRING(width=1)


class Language(BabelRow):
    
    tableName="Languages"
    
    def initTable(self,table):
        table.addField(DEFAULT_PRIMARY_KEY,ASTRING(width=2))
        #table.addBabelField('name',STRING).setMandatory()
        BabelRow.initTable(self,table)
    
##     def getLabel(self):
##         #if self.name is None: return str(self.id)
##         return self.name
    

class Organisation(StoredDataRow):
    "An Organisation is any named group of people."
    tableName="Organisations"
    def initTable(self,table):
        table.addField(DEFAULT_PRIMARY_KEY,ROWID,\
                      doc="the internal id number")
        #Contact.initTable(self,table)
        table.addField('name',STRING)
        table.addField('name2',STRING)
        #table.addView('std',columnNames="name email phone website")
        table.addField('logo',LOGO)
        table.addField('memo',MEMO)
        
    def getLabel(self):
        return self.name

class OrganisationsReport(DataReport):
    "former std view"
    leadTable=Organisation
    columnNames="name name2 id logo memo"
    orderBy='name id'

class Person(StoredDataRow):
    "A Person describes a specific physical human."
    tableName="Persons"
    def initTable(self,table):
        table.addField(DEFAULT_PRIMARY_KEY,ROWID)
        table.addField('name',STRING)
        table.addField('firstName',STRING)
        table.addField('sex',SEX)
        table.addField('birthDate',STRING(width=8))
        table.addField('memo',MEMO)
        table.addField('title',STRING)
        
        # table.setFindColumns("name firstName")

        #self.setColumnList("name firstName id")
        #table.setOrderBy('name firstName')
        #table.addView('std',columnNames="name firstName id")
        table.addDetail('contacts',Contact,'person')

    def getLabel(self):
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
    columnSpec="""
    title name firstName 
    sex birthDate id
    memo
    """
    orderBy='name firstName title sex birthDate id memo'
    

class User(Person):
    "People who can access this database"
    tableName="Users"
    def initTable(self,table):
        Person.initTable(self,table)
        #self.addField('id',STRING,label="Username")
        i=table.getRowAttr(DEFAULT_PRIMARY_KEY)
        i.setType(ASTRING)
        i.setLabel("Username")
        #self.setField('id',STRING,label="Username")
        table.addField('pwd',PASSWORD)

class UsersReport(DataReport):
    leadTable=User
    

class Function(BabelRow):
    
    tableName="Functions"
    
    def initTable(self,table):
        table.addField(DEFAULT_PRIMARY_KEY,ASTRING)
        BabelRow.initTable(self,table)
        
class FunctionsReport(DataReport):
    leadTable=Function

class Contact(StoredDataRow):
    tableName="Contacts"
    
    def initTable(self,table):
        table.addField(DEFAULT_PRIMARY_KEY,ROWID)
        table.addField('name',STRING)
        
        table.addPointer('org',Organisation)
        table.addPointer('person',Person)

        table.addPointer('function',Function)
        table.addPointer('lang',Language)
        
        
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

        table.addPointer('nation',Nation)
        table.addPointer('city',City)
        table.addField('zip',STRING)
        table.addField('street',STRING)
        table.addField('house',INT)
        table.addField('box',STRING)
        
    def getLabel(self):
        return self.name
        
    def after_city(self):
        if self.city is not None:
            self.nation = self.city.nation

    def setname(self):
        if self.org is not None:
            if self.person is not None:
                self.name=u"%s (%s)" % (unicode(self.org),
                                        unicode(self.person))
            else:
                self.name=unicode(self.org)
        else:
            self.name=unicode(self.person)
        #print "setname()", self.name
            
    def after_org(self):
        self.setname()
    def after_person(self):
        self.setname()
        
class ContactsReport(DataReport):
    leadTable=Contact
    columnSpec="""
    id name lang
    org
    person function
    email website
    phone gsm fax
    nation city zip
    street house box
    """
    orderBy='name id'
    
    
        
## class Partner(Contact):
##     """A Person or Organisation with whom I have business contacts.
##     """
##     tableName="Partners"
##     def initTable(self,table):
##         table.addField('name',STRING)
##         table.addField('firstName',STRING)
##         Contact.initTable(self,table)
##         table.addPointer('type',PartnerType)
##         #.setDetail('partnersByType',orderBy='name firstName')
        
##     def validate(self):
##         if self.name is None:
##             raise("name must be specified")

##     def __str__(self):
##         if self.firstName is None:
##             return self.name
##         return self.firstName+" "+self.name

## class PartnersReport(DataReport):
##     "former std view"
##     leadTable=Partner
##     columnNames="name firstName email phone gsm"
    

## class PartnerType(BabelRow):
    
##     tableName="PartnerTypes"
    
##     def initTable(self,table):
##         table.addField('id',STRING)
##         BabelRow.initTable(self,table)
        

##     def validatePartner(self,partner):
##         pass


## class PartnerTypesReport(DataReport):
##     leadTable=PartnerType

    
class Nation(BabelRow):
    
    tableName="Nations"
    
    def initTable(self,table):
        
        table.addField(DEFAULT_PRIMARY_KEY,ASTRING(width=2))
        BabelRow.initTable(self,table)
        table.addField('area',INT(width=8))
        table.addField('population',INT)
        table.addField('curr',STRING)
        table.addField('isocode',STRING(3))
        table.addDetail('cities',City,'nation')
        #table.addDetail('partners_by_nation',Partner,'nation')
        table.addDetail('contacts_by_nation',Contact,'nation')
        
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
        table.addField(DEFAULT_PRIMARY_KEY,ROWID)
        table.addPointer('nation',Nation)
##         table.addPointer('nation',Nation).setDetail('cities',
##                                                     orderBy='name')
        
        table.addField('name',STRING)
        table.addField('zipCode',STRING)
        table.addField('inhabitants',INT(minWidth=5,maxWidth=9))
        
        table.setPrimaryKey("nation id")
        # complex primary key used by test cases
        
        #table.addView('std',columnNames="name nation zipCode")
        
    def getLabel(self):
        if self.nation is None:
            return self.name
        return self.name + " (%s)" % self.nation.id


class CitiesReport(DataReport):
    leadTable=City
    columnNames="name nation zipCode"



class ContactsSchema(Schema):
    
    tableClasses = ( Language,
                     Nation, City,
                     Organisation, Person,
                     Function,
                     Contact)
                     #Partner, PartnerType)

class ContactsMainForm(DbMainForm):

    schemaClass=ContactsSchema
    
    def layout(self,panel):

        panel.label("""
    
Welcome to Contacts, a Lino demo application to manage your contacts.

Warning: This application is not stable and there are no known users.

""")
    

    def setupMenu(self):
        self.addContactsMenu()
        self.addProgramMenu()
        
    def addContactsMenu(self):
        m = self.addMenu("contacts","&Contacts")
        self.addReportItem(
            m,"nations",NationsReport,label="&Nations")
        self.addReportItem(
            m,"cities",CitiesReport,label="&Cities")
        self.addReportItem(
            m,"contacts",ContactsReport,label="&Contacts")
        self.addReportItem(
            m,"orgs",OrganisationsReport,label="&Organisations")
        self.addReportItem(
            m,"persons",PersonsReport,label="&Persons")
        
    
class Contacts(DbApplication):
    name="Lino Contacts"
    version="0.0.1"
    copyright="Copyright 2002-2007 Luc Saffre"
    #author="Luc Saffre"
    mainFormClass=ContactsMainForm
    #dbname="contacts"
    url="http://lino.saffre-rumma.net/contacts.html"
    description="""A Lino demo application to manage your contacts.
    """
    

    

## TABLES = (Language,
##           Nation, City,
##           Organisation, Person, User,
##           Partner, PartnerType)

REPORTS = (NationsReport, CitiesReport, OrganisationsReport,
           PersonsReport, UsersReport,
           FunctionsReport, ContactsReport,
           #PartnersReport,
           #PartnerTypesReport
           )


__all__ = [t.__name__ for t in ContactsSchema.tableClasses]
__all__.append('ContactsSchema')
__all__.append('Contacts')

__all__ += [t.__name__ for t in REPORTS]
__all__.append('REPORTS')


#__all__ = filter(lambda x: x[0] != "_", dir())
