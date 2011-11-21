#coding: latin1
#---------------------------------------------------------------------
# $Id: sprlwidgets.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino import adamo

from lino.schemas.sprl import web, events, news, quotes

from lino.adamo.database import Context
from lino.adamo.schema import LayoutComponent
from lino.adamo.datasource import Datasource

from lino.adamo.html import txt2html

#from widgets import Widget
from response import ContextedResponse

# not used here, but LayoutFactory must find it:
from skipper import Skipper

## class SprlDbResource(DbResource):
## 	def render_index(self,request):
## 		row=self.context.PAGES.findone(match='index')
## 		widget = self._wf.get_widget(row,self,request)
## 		#return widget.show()
## 		return self.show(widget)


class SprlPage(ContextedResponse,LayoutComponent):
	
	def writeLeftMargin(self):
		wr = self.write
		#row = self.target

		sess = self.getSession()
		frm = sess.forms.get('login',None)
		if frm is None:
			usr = sess.getUser()
			if usr is None:
				wr( "wie kann das?")
			else:
				wr("""Logged in as %s.
				<a href="logout">(log out)</a>""" % usr.getLabel())
		else:
			self.renderForm(frm)
			wr("""<br><a href="%s">register</a>""" % \
				self.contextURI("register"))

		msgs = sess.popMessages()
		if len(msgs) > 0:
			wr("""<p style="padding:5px;border:1px solid black;
				background-colr:gold;">""")
			for msg in msgs:
				wr("""<br><font color="red">%s</font>""" % txt2html(msg))
			wr('</p>')
			
			
		
		ContextedResponse.writeLeftMargin(self)
		#self.write('<p><a href="add">add row</a>')
		#self.write('<br><a href="delete">delete row</a></p>')
		self.writeContextMenu()
		#self.target._ds._context.writeLeftMargin(renderer)
		
	def writeContextMenu(self):
		ctx = self.target.getContext()
		wr = self.write
		
		sponsor = ctx.tables.PARTYPES.peek('d')
		ds = ctx.tables.PARTNERS.query(type=sponsor)
		#ds.setFilter("logo NOTNULL")
		if len(ds):
			wr( "<p>Sponsors:")
			for partner in ds:
				wr('<p align="center">')
				url = self.uriToRow(partner)
				img = self.refToImage(
					src=partner.logo,
					tags='width="80" border=0',
					label=partner.getLabel())
				self.renderFormattedLink(url,label=img)
		#renderer.write(leftMargin)


	
class SprlSkipper(Skipper,SprlPage):
	handledClass = Datasource
	
		
		
class SprlRowLayout(SprlPage):
	handledClass = adamo.Table.Instance

	def writeLabel(self):
		row = self.target
		self.renderLink(
			url=self.uriToRow(row),
			label=row.getLabel())
		
	def writePage(self):
		self.writeCellTable(self.target.__iter__())
		
	def writeCellTable(self,cells):
		wr = self.write
		wr('<table border="0" class="data">')
		for cell in cells:
			value = cell.getValue()
			if True or value is not None:
				label = cell.col.name
				wr('\n<tr>')
				wr('<td align="right">' + label + '</td>')
				wr('\n<td>')
				self.renderCellValue(cell.col,value)
## 				if hasattr(value,'asFormCell'):
## 					value.asFormCell(renderer)
## 				else:
## 					type = getattr(attr,'type',None)
## 					renderer.renderValue(value,type)
				wr('</td>')
				wr('\n</tr>')

		wr('\n</table>')
		




class MemoLayout(SprlRowLayout):
	handledClass = web.MemoTable.Instance
	
	def writeParagraph(self):
		row = self.target
		#print row
		self.renderLink(self.uriToRow(row),
							 label=row.getLabel())
		self.write('\n&mdash; ')
		self.renderMemo(row.abstract)

	def writePage(self):
		row = self.target
		wr = self.write
		wr('<p>')
		self.renderMemo(row.abstract)
		wr('</p>')
		wr('<p>')
		self.renderMemo(row.body)
		wr('</p>')


class TreeLayout(SprlRowLayout):
	handledClass = web.TreeTable.Instance
	
	def writePreTitle(self):
		row = self.target
		wr = self.write
		sep = ""
		for superRow in row.getUpTree():
			wr(sep)
			self.renderLink(
				url=self.uriToRow(superRow),
				label=superRow.getLabel())
			sep = " &middot; "

	def writeChildren(self):
		wr = self.write
		wr("<ul>")
		for row in self.target.children.query(orderBy="seq"):
			wr('<li>')
			self.child(row).writeParagraph()
			wr("</li>")
		wr("</ul>")

	def writePage(self):
		SprlRowLayout.writePage(self)
		self.writeChildren()


	
class MemoTreeLayout(TreeLayout,MemoLayout):
	handledClass = adamo.MemoTreeTable.Instance
	
	def writePage(self):
		MemoLayout.writePage(self)
		self.writeChildren()
		
	def writeParagraph(self):
		MemoLayout.writeParagraph(self)
		
		
class PageLayout(MemoTreeLayout):
	handledClass = web.Pages.Instance
	
	def writePage(self):
		row = self.target
		MemoTreeLayout.writePage(self)
		wr = self.write
		if len(row.news_by_page) > 0:
			wr('<p><b>')
			wr('Comments and notes:')
			wr('</b></p>')
			wr('<ul>')
			for newsRow in row.news_by_page:
				wr('<li>')
				#self.asParagraph(newsRow)
				self.renderLink(url=self.uriToRow(newsRow),
									 label=newsRow.getLabel())
				wr('</li>')
			wr('</ul>')

		
	def writePageBottom(self):
		row = self.target
		wr = self.write
		wr('<table border="0">')
		for name in 'created modified author lang'.split():
			value = getattr(row,name)
			if value is not None:
				attr = row._ds._table._rowAttrs[name]
				wr('\n<tr><td>' + name+ '</td><td>')
				type = getattr(attr,'type',None)
				self.renderValue(value,type)
				wr('</td>\n</tr>')

		wr('\n</table>')


class EventLayout(PageLayout):
	handledClass = events.Events.Instance
	def writeParagraph(self):
		row = self.target
		wr = self.write
		self.writeLabel()
		wr('\n&mdash; ')
		if row.title:
			wr(" " + row.title)
			
		if row.type:
			wr(" ")
			self.asLabel(row.type)
		if row.place:
			wr("<br>Ort: ")
			self.asLabel(row.place)
		if row.responsible:
			wr("<br>Veranstalter: ")
			self.asLabel(row.responsible)
		if self.time:
			wr("<br>Uhrzeit: " + row.time )
		self.renderMemo(self.abstract)
		#if self.body is not None:
		wr("<br>")
		self.renderLink(self.uriToRow(row), label="more")

	def writePage(self):
		MemoLayout.writePage(self)
		RowLayout.writePage(self)
		

class TopicLayout(TreeLayout):
	handledClass = quotes.Topics.Instance
		
	def writePage(self):
		row = self.target
		self.writeCellTable(row.getCells("dmoz wikipedia url"))
		#TreeLayout.writePage(self)
		self.writeChildren()



class NewsLayout(MemoLayout):
	handledClass = news.News.Instance
	
	def writeParagraph(self):
		row = self.target
		wr = self.write

		wr(row.getLabel())
		if row.abstract is not None:
			wr('\n&mdash; ')
## 		if self.project:
## 			body += " (Project: " + self.project.asLabel(renderer,request)
## 		if self.newsgroup:
## 			body += " (Group: " + self.newsgroup.asLabel(renderer,request)+")"
## 		if self.author:
## 			body += " (Author: " + self.author.asLabel(renderer,request)+")"
			self.renderMemo(row.abstract)
			if row.body is not None:
				self.renderLink(self.uriToRow(row),"(more)")

		
## class ContextLayout(PageLayout):
## 	handledClass = Context
## 	def __init__(self,target,rsc,request):
## 		row=target.PAGES.findone(match='index')
## 		PageLayout.__init__(row,rsc,request)


class ContextLayout(ContextedResponse,LayoutComponent):
 	handledClass = Context

## 	def writeLeftMargin(self,ctx):
## 		if len(ctx._db.getBabelLangs()) > 1:
## 			wr('<p>')
## 			for lang in ctx._db.getBabelLangs():
## 				#if lang.id == self.langs[0]:
## 				#	wr(lang.id)
## 				#else:
## 				self.renderLink(
## 					url=self.response.uriToSelf(lng=lang.id),
## 					label=lang.id)
## 				wr(' ')
## 			wr('</p>')
					
## 	def writePreTitle(self):
## 		self.renderLink(
## 			url=self.homeURI(),
## 			label=self.target.getLabel())
		
	def getLabel(self):
		return "List of tables"

	def writePage(self):
		ctx = self.target
		wr = self.write
		wr("<ul>")
		for ds in ctx.getDatasources():
			table = ds._table
			if table.getLabel() is not None:
				#if len(ds) != 0:
				wr('<li><a href="%s">%s</a>' % (
					self.uriToDatasource(ds),
					table.getLabel()))
				doc = table.getDoc()
				if doc is not None:
					wr('\n&mdash; ')
					self.renderMemo(doc)
		wr("</ul>")
		
					
	def writeParagraph(self):
		ctx = self.target
		wr = self.write
		sep =""
		for ds in ctx.getDatasources():
			table = ds._table
			if table.getLabel() is not None:
				if len(ds) != 0:
					wr(sep+'<a href="%s">%s</a>' % (
						self.uriToDatasource(ds),
						table.getLabel()))
					sep=", "



