




raise "no longer used. import from webware_ui!"







from WebKit.SidebarPage import SidebarPage
from WebKit.Page import Page
from quixote.html import htmltext
from lino import __version__

class ParamSpec:
	def __init__(self,shortName,s2v,v2s=str):
		self.shortName = shortName
		self.v2s = v2s
		self.s2v = s2v

class SitePage(SidebarPage):

	allowedParams = {
		'table': ParamSpec('t',,str),
		}
	
	def awake(self,tx):
		Page.awake(self,tx)
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

