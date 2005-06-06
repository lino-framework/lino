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

#from lino import adamo 

#import babel, addrbook, news # , sdk

from addrbook import ContactsPlugin
from lino.schemas.sprl.tables import *
from lino.adamo.schema import Schema, SchemaPlugin

class BasePlugin(SchemaPlugin):

    def defineTables(self,schema):
        #schema.addTable(Languages,label="Languages")
        schema.addTable(Users, label="Users" )
        #schema.addForm(LoginForm)
        #schema.addForm(MainForm)


## class WebPlugin(SchemaPlugin):

##     def defineTables(self,schema):
##         schema.addTable( Pages,label="Content Pages")
##         # self.addLinkTable("PAGE2PAGE",web.Page,web.Page,web.Page2Page)

        
## class ProjectPlugin(SchemaPlugin):

##     def defineTables(self,schema):
##         schema.addTable( Projects,
##                          label="Projects")
##         schema.addTable( ProjectStati,
##                          label="Project States")

## class NewsPlugin(SchemaPlugin):

##     def defineTables(self,schema):
##         schema.addTable( News,
##                          label="News Items")
##         schema.addTable( Newsgroups,
##                          label="Newsgroups")
##         #self.addLinkTable("NEWS2NEWSGROUPS",
##         #                    news.News, news.Newsgroup)

        
## class EventsPlugin(SchemaPlugin):
##     def defineTables(self,schema):
##         schema.addTable( Events,
##                          label="Events")
##         schema.addTable( EventTypes,
##                          label="Event Types")

class SalesPlugin(SchemaPlugin):  
    def defineTables(self,schema):
        schema.addTable( Journals,
                         label="Journals")
        schema.addTable( Years,
                         label="Fiscal Years")

        schema.addTable( Products,
                         label="Products")

        schema.addTable( Invoices,label="Invoices")
        schema.addTable( InvoiceLines,
                         label="Invoice Lines")

        import ledger
        for t in ledger.tables:
            schema.addTable(t)
            
        #schema.addTable(Accounts)
        #schema.addTable(Statements)
        #schema.addTable(StatementLines)
        
        #schema.addTable(Bookings)
        

#class JokesPlugin(SchemaPlugin):
#    pass


## class QuotesPlugin(SchemaPlugin):
    
##     def defineTables(self,schema):
##         schema.addTable( Authors,label="Authors")
##         schema.addTable( AuthorEvents,
##                          label="Biographic Events")
##         schema.addTable( AuthorEventTypes,
##                          label="Biographic Event Types")
##         schema.addTable( Topics,
##                          label="Topics")
##         schema.addTable( Publications,
##                          label="Publications")
##         schema.addTable( Quotes,
##                          label="Quotes")
##         schema.addTable( PubTypes,
##                          label="Publication Types")
##         schema.addTable( PubByAuth,
##                          label="Publications By Author")
        

        
class Sprl(Schema):
    #name="Sprl"
    #years="2002-2005"
    #author="Luc Saffre"
    def __init__(self,
                 #withEvents=True,
                 #withProjects=True,
                 #withWeb=True,
                 withSales=True,
                 #withNews=True,
                 #withQuotes=True,
                 **kw):
        Schema.__init__(self,**kw)
        self.addPlugin(BasePlugin(True))
        self.addPlugin(ContactsPlugin(True))
    
        #self.addPlugin(EventsPlugin(withEvents))
        self.addPlugin(SalesPlugin(withSales))
        #self.addPlugin(QuotesPlugin(withQuotes))
        #self.addPlugin(WebPlugin(withWeb))
        #self.addPlugin(ProjectPlugin(withProjects))
        #self.addPlugin(NewsPlugin(withNews))
        
##     def getContentRoot(self,db):
##         return db.tables.PAGES.findone(match="index")

##     def onBeginSession(self,sess):
##         if not sess.hasAuth():
##             sess.showForm("login",modal=True)
##         sess.showForm("main")

        
## def makeSchema( withEvents=True,
##                 withProjects=True,
##                 withWeb=True,
##                 withSales=True,
##                 withNews=True,
##                 withQuotes=True):
## ##                 withJokes=False,
## ##                 big=False):
    
##     schema = Sprl() 
    
##     schema.addPlugin(BasePlugin(True))
##     schema.addPlugin(ContactsPlugin(True))
    
##     schema.addPlugin(EventsPlugin(withEvents))
##     schema.addPlugin(SalesPlugin(withSales))
##     schema.addPlugin(QuotesPlugin(withQuotes))
##     schema.addPlugin(WebPlugin(withWeb))
##     schema.addPlugin(ProjectPlugin(withProjects))
##     schema.addPlugin(NewsPlugin(withNews))
##     #schema.addPlugin(JokesPlugin(withJokes))
##     #schema.initialize()
##     return schema


        
        
##  def onStartUI(self,sess):
##      sess.openForm('login',uid="luc")
        
##  def defineMenus(self,context,win):
##      #assert db.schema is self
        
##      ui = win
##      context.installto(globals())

        
##      mb = win.addMenuBar("user","&User Menu")
##      m = mb.addMenu("&Master data")
##      #m.addItem("&Persons",       ui.showReport, PERSONS)
##      m.addItem("&Organisations", ui.showReport, ORGS)
##      m.addItem("&Partners",      ui.showReport, PARTNERS)
##      m.addItem("&Pages",         ui.showReport, PAGES)

##      m = mb.addMenu("&Journals")
##      m.addItem("&Invoices",      ui.showReport, INVOICES)
##      # m = self.addSystemMenu(ui,mb)
##      #m.addItem("Ad&min menu",ui.setMainMenu,'admin')
        
        
##      # mb = win.addMenuBar("admin","&Admin Menu")
##      m = mb.addMenu("&Tables")
##      for ds in context.getDatasources():
##          table = ds._table
##          if table.getLabel() is not None:
##              #rpt = area.report()
##              m.addItem(table.getLabel(),
##                           ui.showReport,
##                           ds)
##      m = mb.addMenu("T&ests")
##      m.addItem("&Decide",ui.test_decide)
        
##      #m = self.addSystemMenu(ui,mb)
##      #m.addItem("&User menu",ui.setMainMenu,'user')

##      m = mb.addMenu("&System")
##      m.addItem("&Exit",ui.exit)
##      m.addItem("&About",ui.showAbout)
        
##  def addSystemMenu(self,ui,mb):
##      #m.addItem("~Main menu",self.getMainMenu)
##      return m


##  def getUserMenu(self,ui):
##      raise NotImplementedError
        
##  def getAdminMenu(self,ui):
##      #win = ui.openWindow(label=self.getLabel())
##      mb = MenuBar("Admin Menu")

##      return mb





