#coding: latin1
#----------------------------------------------------------------------
# $Id: sprl.py,v 1.8 2004/06/18 12:23:58 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
from lino import adamo 

import babel, addrbook, news # , sdk


class Schema(adamo.Schema):

	defaults = {
		'withEvents' : True,
		'withProjects' : True,
		'withWeb' : True,
		'withSales' : True,
		'withNews' : True,
		'withQuotes' : True,
		'withJokes' : False,
		}


	def defineTables(self,ui):
		self.addTable( babel.Languages("LANGS","Languages"))
		
		if True:
			self.addTable( addrbook.Users(
				name="USERS",
				label="Users" ))
			self.addTable( addrbook.Nations(
				name="NATIONS",
				label="Nations" ))
			self.addTable( addrbook.Cities("CITIES","Cities"))
			self.addTable( addrbook.Organisations("ORGS","Organisations"))
			self.addTable( addrbook.Partners("PARTNERS","Partners"))
			self.addTable( addrbook.PartnerTypes(
				name="PARTYPES",
				label="Partner Types"))
			self.addTable( addrbook.Currencies())

		#self.addLinkTable("PERS2PERS", Person, Person)
		#self.addLinkTable("ORG2ORG",	 Organisation,		Organisation)
		#self.addLinkTable("ORG2PERS",	 Organisation,		Person,
		#					 addrbook.Org2Pers)

		if self.withSales:
			import business, products, sales, ledger
			self.addTable( business.Journals("JOURNALS","Journals"))
			self.addTable( business.Years("YEARS","Fiscal Years"))

			self.addTable( products.Products("PRODUCTS","Products"))

			self.addTable( sales.Invoices("INVOICES","Invoices"))
			self.addTable( sales.InvoiceLines("INVOICELINES",
														 "Invoice Lines"))
			self.addTable( ledger.Bookings("BOOKINGS",
													 "Ledger Bookings"))

		if self.withQuotes:
			import quotes
			self.addTable( quotes.Authors("AUTHORS","Authors"))
			self.addTable( quotes.AuthorEvents("PEREVENTS",
														  "Biographic Events"))
			self.addTable( quotes.AuthorEventTypes(
				name="PEVTYPES",
				label="Biographic Event Types"))
			self.addTable( quotes.Topics("TOPICS","Topics"))
			self.addTable( quotes.Publications(
				name="PUBLICATIONS",
				label="Publications"))
			self.addTable( quotes.Quotes("QUOTES","Quotes"))
			self.addTable( quotes.PubTypes(
				name="PUBTYPES",
				label="Publication Types"))
			self.addTable( adamo.LinkTable(
				quotes.Publications,
				quotes.Authors,
				name="PUB2AUTH",
				label="Publications By Author"))

		if self.withWeb:
			import web
			self.addTable( web.Pages("PAGES","Content Pages"))
			# self.addLinkTable("PAGE2PAGE",web.Page,web.Page,web.Page2Page)

		if self.withProjects:
			import projects
			self.addTable( projects.Projects("PROJECTS","Projects"))
			self.addTable( projects.ProjectStati("PRJSTAT",
															 label="Project States"))
			
		if self.withNews:
			import news
			self.addTable( news.News("NEWS",
											 label="News Items"))
			self.addTable( news.Newsgroups("NEWSGROUPS",
													 label="Newsgroups"))
			#self.addLinkTable("NEWS2NEWSGROUPS",
			#					 news.News, news.Newsgroup)
			
		if self.withEvents:
			import events
			self.addTable( events.Events("EVENTS","Events"))
			self.addTable( events.EventTypes("EVENTTYPES",
														label="Event Types"))
			
	#def defaultAction(self,ui):
	#	return ui.show(self.tables['PAGES'][1])
		

	def defineMenus(self,win):
		#assert db.schema is self
		
		self.installto(globals())
		ui = win

		frm = PAGES.form()
		frm.setRange("1")
		#ui.setDefaultAction(ui.showForm,frm)
		
		
		mb = ui.addMenuBar("user","&User Menu")
## 		m = mb.addMenu("&Master data")
## 		m.addItem("&Persons",       ui.showReport, PERSONS.report())
## 		m.addItem("&Organisations", ui.showReport, ORGS.report())
## 		m.addItem("&Partners",      ui.showReport, PARTNERS.report())
## 		m.addItem("&Pages",         ui.showReport, PAGES.report())

		# m = self.addSystemMenu(ui,mb)
		#m.addItem("Ad&min menu",ui.setMainMenu,'admin')
		
		
		# mb = win.addMenuBar("admin","&Admin Menu")
		m = mb.addMenu("&Tables")
		for area in win.db._areas.values():
			table = area._table
		#for (name,table) in self.getTableDict().items():
			if table.getLabel() is not None:
				rpt = area.report()
				m.addItem(table.getLabel(),
							 ui.showReport,
							 rpt)
		m = mb.addMenu("T&ests")
		m.addItem("&Decide",ui.test_decide)
		
		#m = self.addSystemMenu(ui,mb)
		#m.addItem("&User menu",ui.setMainMenu,'user')

		m = mb.addMenu("&System")
		m.addItem("&Exit",ui.exit)
		m.addItem("&About",ui.showAbout)
		
## 	def addSystemMenu(self,ui,mb):
## 		#m.addItem("~Main menu",self.getMainMenu)
## 		return m


## 	def getUserMenu(self,ui):
## 		raise NotImplementedError
		
## 	def getAdminMenu(self,ui):
## 		#win = ui.openWindow(label=self.getLabel())
## 		mb = MenuBar("Admin Menu")

## 		return mb




## 	def getUserMenu(self,ui):
## 		#win = ui.openWindow(label=self.getLabel())
## 		mb = MenuBar("Main Menu")

## 		m = mb.addMenu("&Master")
## 		m.addItem("&Persons", ui.showReport,"PERSONS")
## 		m.addItem("&Organisations", ui.showReport,"ORGS")
## 		m.addItem("&Partners", ui.showReport,"PARTNERS")

## 		m = self.addSystemMenu(ui,mb)
## 		m.addItem("Ad&min menu",ui.showAdminMenu)

## 		return mb
	
	

## def quickdb(**kw):
## 	sch = Schema(**kw)
## 	return schema.quickdb(schema=sch)
	
