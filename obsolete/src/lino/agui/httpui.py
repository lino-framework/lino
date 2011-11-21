#coding:latin1

from ui import UI
from widgets import Action, Grid, Window, Label, Button, MenuBar, Editor, Form

from lino.adamo.row import BaseRow

HEAD = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
			 "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>%s</title>
</head>
<body>
<table class="main"><tr><td valign="top">
"""

FOOT = """
</td></tr></table>
</body>
</html>
"""

def processForm(ui,frm):
	ui.message("form processing is not implemented")



class HttpUI(UI):
	
	""" abstract UI whose methods should be usable by any Web UI. There
	should be one instance of HttpUI for each session. MainSnakelet
	stores a SessionContext variable `ui` to do this.
	"""
	
	def __init__(self,db):
		UI.__init__(self,db)
		self.renderedPages = []
		
	def addPage(self):
		p = RenderedPage(len(self.renderedPages))
		self.renderedPages.append(p)

	def releasePage(self,page):
		assert self.renderedPages[page.id] is page
		self.renderedPages[page.id] = None

	

class RenderedPage:

	""" A Rendered Page instance keeps track especially of the actions
	that have been rendered on a page. 
	
	"""
	def __init__(self,id):
		self.id = id
		self.actions = []
		self.window = None

	def addAction(self,a):
		ra = RenderedAction(len(self._actions),a)
		self._actions.append(ra)
		return ra

class RenderedAction:
	def __init__(self,id,action):
		self.id = id
		self.action = action
		


class HtmlRenderer:
	"""General HTML renderer. To be called by a HTML ui.
	"""

	def __init__(self,ui):
		self.renderedPage = RenderedPage()
		# self._actions = []
		self.ui = ui

	def addAction(self,a):
		return self.renderedPage.addAction(a)

	def wr(self):
		raise NotImplementedError
	
	def getURL(self):
		raise NotImplementedError
	
	def escape(self,text):
		raise NotImplementedError

	#def getRenderedActions(self):
	#	 return self._actions
	
	def beginPage(self,title):
		self.wr(HEAD % title)
		self.wr('\n<br>'+self.windowLink(self.ui.getWindow(0)))
		#self.wr('\n<br><a href="main.sn">%s</a>' % _("Main menu"))
		self.wr('\n<br><a href="/manage/manage.sn">Manager menu</a>')
		self.wr('\n</td><td valign="top">')
		# self.wr('<H1>%s</H1>' % title)

	def endPage(self):
		# self.renderMenuBar(win.getMenuBar())
		if len(self.ui.getMessages()) > 0:
			self.wr('<p class="message">%s</p>' % \
					  "<br>".join(self.ui.getMessages()))
			self.ui.clearMessages()
		self.wr(FOOT)

	def renderWindow(self,target):
		# called by MainSnakelet
		self.beginPage(target.getLabel())
		self.renderComponent(target)
		self.endPage()
		
	def renderComponent(self,comp):
		if isinstance(comp,Grid):
			self.renderGrid(comp)
		elif isinstance(comp,Window):
			for subcomp in comp.getComponents():
				self.renderComponent(subcomp)
		elif isinstance(comp,BaseRow):
			self.renderGrid(comp.getGrid(self))
		elif isinstance(comp,MenuBar):
			self.renderMenuBar(comp)
		elif isinstance(comp,Label):
			self.wr(self.escape(comp.getLabel()))
		elif isinstance(comp,Editor):
			attr = comp.getAttr()
			value = getattr(comp.getRow(),attr.name)
			self.wr('<input type="text" value="%s">' \
					  % self.formatValue(value))
		elif isinstance(comp,Button):
			ra = self.addAction(comp)
			self.wr('['+self.formatLink(ra,comp.getLabel())+']')
		else:
			self.ui.message("Cannot render " + repr(comp))

	def windowLink(self,win):
		return '<a href="main.sn?w=%s">%s</a>' % \
				 (str(win.getId()), self.formatLabel(win.getLabel()))

	def formatLink(self,action,label):
		return '<a href="%s">%s</a>' % (self.formatAction(action),
												  self.formatLabel(label))

	def formatAction(self,ra):
		return '%s?w=%d&a=%d' % (self.getURL(),\
										 self.ui.getCurrentWindow().winid,\
										 ra.id)
	
	def formatLabel(self,label):
		label = self.escape(label)
		p = label.find('&')
		if p != -1:
			label = label[:p] + '<u>' + label[p+1] + '</u>' + label[p+2:]
		return label
	
	def formatValue(self,value):
		if value is None:
			return '&mdash;'
		#if isinstance(value,BaseRow):
		#	 a = Action(label=str(row.id),
		#					func=row.ui_openFormWindow)
		#	 return self.formatAction(a)
		return self.escape(str(value))
		
		

	def renderMenuBar(self,mb):
		if mb.getLabel():
			self.wr('<p class="menu"><b>%s</b> ' % \
					  self.formatLabel(mb.getLabel()))
		for mnu in mb.getMenus():
			self.wr('<br><b>%s</b>: ' % self.formatLabel(mnu.getLabel()))
			for mi in mnu.getItems():
				ra = self.addAction(mi)
				self.wr(' [%s] ' % self.formatLink(ra,mi.getLabel()))

	#def renderView(self,view):
	#	 pass
	
	#def renderForm(self,comp):


	def renderGrid(self,grid):
		q = grid.query
		q.setLimitOffset(grid.pageLen,
							  (grid.currentPage-1)*grid.pageLen)
		if grid.isEditing:
			a = Action(func=processForm,args=(grid,))
			ra = self.addAction(a)
			self.wr('\n<form action="%s" method="POST">' % \
					  self.formatAction(ra))
		if grid.asTable:
			self.wr('<table border="1">')
			self.wr('<tr>')
			for col in q.getVisibleColumns():
				a = Action( func=grid.setOrderBy, args=(col.name,))
				ra = self.addAction(a)
				self.wr('<td>')
				self.wr(self.formatLink(label=col.getLabel(),
												action=ra))
				self.wr("</td>\n")
			self.wr('</tr>')
			for atomicRow in q.executeSelect():
				self.wr('\n<tr>\n')
				l = []
				for col in q.getVisibleColumns():
					self.wr('<td>')
					value = col.atoms2value(atomicRow)

					if isinstance(value,BaseRow):
						a = Action( func=value.getGrid )
						ra = self.addAction(a)
						self.wr( self.formatLink(label=value.getLabel(),
														 action=ra))
					else:
						self.wr(self.formatValue(value))
					self.wr('</td>')
				self.wr('\n</tr>')

			self.wr('\n</table>')
		else:
			for atomicRow in q.executeSelect():
				row = q.provideRow(atomicRow)
				self.wr('<h2>%s</h2>' % row.getLabel())
				self.wr('\n<table border="1">')
				for col in q.getVisibleColumns():
					self.wr('\n<tr>')
					self.wr("\n<td>")
					self.wr(self.formatLabel(col.getLabel()))
					self.wr("\n</td>")
					self.wr("\n<td>")
					value = col.atoms2value(atomicRow)
					self.wr('<input type="text" value="%s">' \
							  % self.formatValue(value))
					
					self.wr("\n</td>")
					self.wr('\n</tr>')

				self.wr('\n</table>')


		if grid.isEditing:
			self.wr('\n<input type="submit">')
			self.wr('\n</form>')
			

