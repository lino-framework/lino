#coding: latin1
#----------------------------------------------------------------------
# $Id: sprl.py,v 1.8 2004/06/18 12:23:58 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
from lino import adamo 

import babel, addrbook, news # , sdk


class BasePlugin(adamo.SchemaPlugin):

	def defineTables(self,schema,ui):
		schema.addTable( babel.Languages("LANGS","Languages"))
		schema.addTable( addrbook.Users( name="USERS",
													label="Users" ))
		schema.addForm(addrbook.LoginForm(name="login"))
		schema.addForm(addrbook.MainForm(name="main"))

class ContactsPlugin(adamo.SchemaPlugin):
	def defineTables(self,schema,ui):
		schema.addTable( addrbook.Nations(
			name="NATIONS",
			label="Nations" ))
		schema.addTable( addrbook.Cities("CITIES","Cities"))
		schema.addTable( addrbook.Organisations("ORGS","Organisations"))
		schema.addTable( addrbook.Partners("PARTNERS","Partners"))
		schema.addTable( addrbook.PartnerTypes(
			name="PARTYPES",
			label="Partner Types"))
		schema.addTable( addrbook.Currencies())


class WebPlugin(adamo.SchemaPlugin):

	def defineTables(self,schema,ui):
		import web
		schema.addTable( web.Pages("PAGES","Content Pages"))
		# self.addLinkTable("PAGE2PAGE",web.Page,web.Page,web.Page2Page)

		
class ProjectPlugin(adamo.SchemaPlugin):

	def defineTables(self,schema,ui):
		import projects
		schema.addTable( projects.Projects("PROJECTS","Projects"))
		schema.addTable( projects.ProjectStati("PRJSTAT",
															 label="Project States"))


class NewsPlugin(adamo.SchemaPlugin):

	def defineTables(self,schema,ui):
		import news
		schema.addTable( news.News("NEWS",
										 label="News Items"))
		schema.addTable( news.Newsgroups("NEWSGROUPS",
												 label="Newsgroups"))
		#self.addLinkTable("NEWS2NEWSGROUPS",
		#					 news.News, news.Newsgroup)

		
class EventsPlugin(adamo.SchemaPlugin):
	def defineTables(self,schema,ui):
		import events
		schema.addTable( events.Events("EVENTS","Events"))
		schema.addTable( events.EventTypes("EVENTTYPES",
													  label="Event Types"))

class SalesPlugin(adamo.SchemaPlugin):	
	def defineTables(self,schema,ui):
		import business, products, sales, ledger
		schema.addTable( business.Journals("JOURNALS","Journals"))
		schema.addTable( business.Years("YEARS","Fiscal Years"))

		schema.addTable( products.Products("PRODUCTS","Products"))

		schema.addTable( sales.Invoices("INVOICES","Invoices"))
		schema.addTable( sales.InvoiceLines("INVOICELINES",
													 "Invoice Lines"))
		schema.addTable( ledger.Bookings("BOOKINGS",
												  "Ledger Bookings"))

class JokesPlugin(adamo.SchemaPlugin):
	pass


class QuotesPlugin(adamo.SchemaPlugin):	
	def defineTables(self,schema,ui):
		import quotes
		schema.addTable( quotes.Authors("AUTHORS","Authors"))
		schema.addTable( quotes.AuthorEvents("PEREVENTS",
													  "Biographic Events"))
		schema.addTable( quotes.AuthorEventTypes(
			name="PEVTYPES",
			label="Biographic Event Types"))
		schema.addTable( quotes.Topics("TOPICS","Topics"))
		schema.addTable( quotes.Publications(
			name="PUBLICATIONS",
			label="Publications"))
		schema.addTable( quotes.Quotes("QUOTES","Quotes"))
		schema.addTable( quotes.PubTypes(
			name="PUBTYPES",
			label="Publication Types"))
		schema.addTable( adamo.LinkTable(
			quotes.Publications,
			quotes.Authors,
			name="PUB2AUTH",
			label="Publications By Author"))

		
def Schema( withEvents=True,
				withProjects=True,
				withWeb=True,
				withSales=True,
				withNews=True,
				withQuotes=True,
				withJokes=False,):
	schema = SprlSchema()
	
	schema.addPlugin(BasePlugin(True))
	schema.addPlugin(ContactsPlugin(True))
	
	schema.addPlugin(EventsPlugin(withEvents))
	schema.addPlugin(SalesPlugin(withSales))
	schema.addPlugin(QuotesPlugin(withQuotes))
	schema.addPlugin(WebPlugin(withWeb))
	schema.addPlugin(ProjectPlugin(withProjects))
	schema.addPlugin(NewsPlugin(withNews))
	schema.addPlugin(JokesPlugin(withJokes))

	return schema


class SprlSchema(adamo.Schema):

	def getContentRoot(self,ctx):
		return ctx.tables.PAGES.findone(match="index")

	def onStartUI(self,sess):
		sess.openForm('login',uid="luc")
		
## 	def defineMenus(self,context,win):
## 		#assert db.schema is self
		
## 		ui = win
## 		context.installto(globals())

		
## 		mb = win.addMenuBar("user","&User Menu")
## 		m = mb.addMenu("&Master data")
## 		#m.addItem("&Persons",       ui.showReport, PERSONS)
## 		m.addItem("&Organisations", ui.showReport, ORGS)
## 		m.addItem("&Partners",      ui.showReport, PARTNERS)
## 		m.addItem("&Pages",         ui.showReport, PAGES)

## 		m = mb.addMenu("&Journals")
## 		m.addItem("&Invoices",      ui.showReport, INVOICES)
## 		# m = self.addSystemMenu(ui,mb)
## 		#m.addItem("Ad&min menu",ui.setMainMenu,'admin')
		
		
## 		# mb = win.addMenuBar("admin","&Admin Menu")
## 		m = mb.addMenu("&Tables")
## 		for ds in context.getDatasources():
## 			table = ds._table
## 			if table.getLabel() is not None:
## 				#rpt = area.report()
## 				m.addItem(table.getLabel(),
## 							 ui.showReport,
## 							 ds)
## 		m = mb.addMenu("T&ests")
## 		m.addItem("&Decide",ui.test_decide)
		
## 		#m = self.addSystemMenu(ui,mb)
## 		#m.addItem("&User menu",ui.setMainMenu,'user')

## 		m = mb.addMenu("&System")
## 		m.addItem("&Exit",ui.exit)
## 		m.addItem("&About",ui.showAbout)
		
## 	def addSystemMenu(self,ui,mb):
## 		#m.addItem("~Main menu",self.getMainMenu)
## 		return m


## 	def getUserMenu(self,ui):
## 		raise NotImplementedError
		
## 	def getAdminMenu(self,ui):
## 		#win = ui.openWindow(label=self.getLabel())
## 		mb = MenuBar("Admin Menu")

## 		return mb





