#coding:latin1
#----------------------------------------------------------------------
# $Id: webware_ui.py,v 1.1 2004/03/04 12:22:21 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------


from lino.adamo import ui
#from lino.agui.widgets import Action, Grid, Window, Label, Button, MenuBar, Editor, Form

#from lino.adamo.row import BaseRow
# from lino.adamo.report import Report

# from SitePage import ParamSpec, SitePage

from WebKit.SidebarPage import SidebarPage
from WebKit.Page import Page
from quixote.html import htmltext
from lino import __version__


class ParamSpec:
	def __init__(self,shortName,s2v,v2s=str):
		self.shortName = shortName
		self.v2s = v2s
		self.s2v = s2v


class DataPage(SidebarPage):

	dbname = "default"
	allowedParams = {
		'table': ParamSpec('t',str,str),
		'report': ParamSpec('rpt',str,str),
		}

	
	def __init__(self):
		SidebarPage.__init__(self)
		
	
 	def awake(self,tx):
		Page.awake(self,tx)
		self.db = self.application().lino_ui.getDatabase(self.dbname)
		
		# convert flds to params:
		flds = tx.request().fields().copy()
		params = {}
		for (name,v) in flds.items():
			try:
				ps = self.allowedParams[name]
				params[name] = ps.s2v(v)
			except KeyError:
				raise "TODO"
			
		# instanciate page controller:
		self._ctrl = ReportCtrl(params)
			

## 	def allowParam(self,longName,shortName,s2v,v2s):
## 		self.allowParam[longName] = ParamSpec(shortName,s2v,v2s)

	def urlToSelf(self,label,**options):
		# path = self.request().servletURI()
		url = 'http://' + self.request().serverURL()
		flds = self.transaction().request().fields().copy()
		for (k,v) in options.items():
			ps = self.allowedParams[k]
			flds[ps.shortName] = ps.v2s(v)
			
		sep = "?"
		for (k,v) in flds.items():
			url += sep + k + "=" + v
			sep = "&"
		
		return '<a href="%s">%s</a>' % (url,self.formatLabel(label))
		

##		def writeBodyParts(self):
##			self.writeln('<TABLE class="main">')
##			self.writeln('<TR>')
##			self.writeln('<TD WIDTH="20%">')
##			self.writeSideBar()
##			self.writeln('</TD>')
##			self.writeln('<TD width="80%">')
##			self.writeContent()
##			self.writeln('</TD>')
##			self.writeln('</TR>')
##			self.writeln('</TABLE>')
 
	def cornerTitle(self):
		return self.application().lino_ui.db.getLabel()

	def writeSidebar(self):

		self.startMenu()
		self.writeMenu()
				
		self.writeContextsMenu()
		self.menuHeading('E-Mail')
		self.menuItem('Announce',
						  'mailto:lino-announce@lists.sourceforge.net')
		self.writeWebwareExitsMenu()
		self.writeVersions()
		self.write(' &nbsp; Lino %s <br>' % __version__)
		self.endMenu()

	def writeMenu(self):
		pass
				
 
## 	def writeContent(self):
## 		a = self.abstract()
## 		if a is not None:
## 			self.writeln('<p class="abstract">')
## 			self.writeln(self.abstract())
## 			self.writeln('</p>')
			
		
## 		# r = WebwareRenderer(self)
		
## 		self.writeText()
 

	def formatLabel(self,label):
		p = label.find('&')
		if p != -1:
			label = label[:p] + '<u>' + label[p+1] + '</u>' + label[p+2:]
		return label
   

	def renderMenuBar(mb):
		# not used
		s = ""
		if mb.getLabel():
			s += '<p class="menu"><b>%s</b> ' % self.formatLabel(mb.getLabel())
		for mnu in mb.getMenus():
			s += '<br><b>%s</b>: ' % self.formatLabel(mnu.getLabel())
			for mi in mnu.getItems():
				if hasattr(mi.target,"getName"):
					s += ' [%s] ' % renderAction(mi.target,mi.method,mi.getLabel())
				else:
					s += " [%s] " % htmltext(repr(mi.target))
		return s



class ReportPage(DataPage):

	prevPageButton = '[&lt;]'
	nextPageButton = '[&gt;]'
	allowedParams = {
		'pageLen': ParamSpec('pl',int,str),
		'pageNum': ParamSpec('pg',int,str),
		}

	
## 	def initWindow(self,ui):
## 		return self.rpt.initWindow(ui)
	
	def writeContent(self):
		rpt = self._ctrl
		wr = self.wr
		# rpt.initReport()
		# rpt = evt.showable
		# wr("<h1>%s</h1>" % rpt.getLabel())
		pageLen = rpt.getParam('pageLen')
		if pageLen is not None:
			pageNum = rpt.getParam('pageNum')
			if pageNum == 1:
				wr(self.prevPageButton)
			elif pageNum < 1:
				raise "todo"
			else:
				wr(self.urlToSelf( label=self.prevPageButton,
										 pageNum=rpt.getParam('pageNum')-1))
			lastPage = int(len(rpt) / pageLen) + 1
			if pageNum == lastPage:
				wr(self.nextPageButton)
			elif pageNum > lastPage:
				raise "todo"
			else:
				wr(self.urlToSelf( label=self.nextPageButton,
										 pageNum=rpt.getParam('pageNum')+1))

		wr('<table border="1">')
		wr('<tr>')
		for col in rpt.getColumns():
			#~ a = Action( func=grid.setOrderBy, args=(col.name,))
			#~ ra = self.addAction(a)
			wr('<td>')
			wr(col.getLabel())
			#~ self.wr(self.formatLink(label=col.getLabel(), action=ra))
			wr("</td>")
		wr('</tr>')
		for qrow in rpt:
			wr('<tr>')
			l = []
			i = 0
			for col in rpt.getColumns():
				wr( '<td>')
				# value = col.atoms2value(atomicRow)
				value = qrow[i]
				i += 1

				if value is None:
					wr("&mdash;")
				elif hasattr(value,'getLabel'):
					wr(value.getLabel())
					#~ a = Action( func=value.getGrid )
					#~ ra = self.addAction(a)
					#~ self.wr( self.formatLink(label=value.getLabel(),
													 #~ action=ra))
				else:
					wr(self.htmlEncode(str(value)))
				wr('</td>')
			wr('</tr>')

		wr('</table>')
	
	

class UI(ui.UI):
	
	"""
	
	To be instanciated by the LinoKit plugin during Webware application
	server startup.
	
	
	"""
	
	def show(self,what,**kw):
		if isinstance(what,Report):
			db = self.getCurrentDb()
			win = ReportWindow(db,what)
		
		page.setPageController(ctrl)
		ui.clearMenus()
		ctrl.setupMenu(ui)

	def setMainMenu(self,page,mnuName,**kw):
		wr = page.writeln
		# parameters : which menubar to display
		# mnuName = flds.pop('menu','user')

		# display alternative menus
## 		for name,mb in ui.getMenuBars().items():
## 			if name == mnuName:
## 				wr("[" + self.formatLabel(mb.getLabel()) + "]")
## 			else:
## 				wr(self.urlToSelf(label=mb.getLabel(),
## 										options={'menu':name}))
## 		wr('<p><hr></p>')
		
		# now here is the requested menu
		mb = self.db.getMenuBars()[mnuName]
		
		wr( "This is the %s." % mb.getLabel())
		
		for mnu in mb.getMenus():
			page.menuHeading(self.formatLabel(mnu.getLabel())+':')
			for mi in mnu.getItems():
				page.menuItem(self.formatLabel(mi.getLabel()),
								  "Main?a=%d" % mi.getId())



	def showAbout(self,evt,id,**kw):
		raise AbstractError,self.__class__
	
	def test_decide(self,evt,id,**kw):
		raise AbstractError,self.__class__
	
	def showWindow(self,evt,id,**kw):
		raise NotImplementedError

	def exit(self,evt):
		raise NotImplementedError
	
	








