#coding: latin1
#---------------------------------------------------------------------
# $Id: sprlwidgets.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino import adamo

#from lino.schemas.sprl import Schema
from lino.schemas.sprl import web, events, news, quotes

from lino.adamo.database import Context

from widgets import Widget, RowWidget

#from resources import DbResource

# not used here, but WidgetFactory must find it:
from skipper import Skipper

## class SprlDbResource(DbResource):
## 	def render_index(self,request):
## 		row=self.context.PAGES.findone(match='index')
## 		widget = self._wf.get_widget(row,self,request)
## 		#return widget.show()
## 		return self.show(widget)
		
class SprlRowWidget(RowWidget):
	handledClass = adamo.Table.Row
	#def __init__(self,db):
	#	self.db = db
	def writeContextMenu(self,ctx):
		wr = self.write
		
		sponsor = ctx.PARTYPES.peek('d')
		ds = ctx.PARTNERS.query(type=sponsor)
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





class MemoWidget(SprlRowWidget):
	handledClass = web.MemoTable.Row
	
	def writeParagraph(self):
		#self.writeDebugMessage("foofoo")
		row = self.target
		#self.asLabel(row)
		self.renderLink(self.uriToRow(row),
							 label=row.getLabel())
		self.write('\n&mdash; ')
		self.renderMemo(self.target.abstract)

	def writePage(self):
		wr = self.write
		row = self.target
		wr('<p>')
		self.renderMemo(row.abstract)
		wr('</p>')
		wr('<p>')
		self.renderMemo(row.body)
		wr('</p>')


class TreeWidget(SprlRowWidget):
	handledClass = web.TreeTable.Row
	
	def writePreTitle(self):
		wr = self.write
		row = self.target
		sep = ""
		for superRow in row.getUpTree():
			wr(sep)
			self.renderLink(
				url=self.uriToRow(superRow),
				label=superRow.getLabel())
			sep = " &middot; "

	def writeChildren(self):
		wr = self.write
		row = self.target
		wr("<ul>")
		for row in row.children.query(orderBy="seq"):
			wr('<li>')
			self.asParagraph(row)
			wr("</li>")
		wr("</ul>")

	def writePage(self):
		SprlRowWidget.writePage(self)
		self.writeChildren()


	
class MemoTreeWidget(TreeWidget,MemoWidget):
	handledClass = adamo.MemoTreeTable.Row
	
	def writePage(self):
		MemoWidget.writePage(self)
		self.writeChildren()
		
	def writeParagraph(self):
		MemoWidget.writeParagraph(self)
		
		
class PageWidget(MemoTreeWidget):
	handledClass = web.Pages.Row
	
	def writePage(self):
		MemoTreeWidget.writePage(self)
		row = self.target
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

		
	def writeFooter(self):
		wr = self.write
		wr('<table border="0">')
		for name in 'created modified author lang'.split():
			value = getattr(self.target,name)
			if value is not None:
				attr = self.target._ds._table._rowAttrs[name]
				wr('\n<tr><td>' + name+ '</td><td>')
				type = getattr(attr,'type',None)
				self.renderValue(value,type)
				wr('</td>\n</tr>')

		wr('\n</table>')


class EventWidget(PageWidget):
	handledClass = events.Events.Row
	def writeParagraph(self):
		wr = self.write
		row = self.target
		self.asLabel(row)
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
		MemoWidget.writePage(self)
		RowWidget.writePage(self)
		

class TopicWidget(TreeWidget):
	handledClass = quotes.Topics.Row
		
	def writePage(self):
		self.writeCellTable(self.target.getCells("dmoz wikipedia url"))
		#TreeWidget.writePage(self)
		self.writeChildren()



class NewsWidget(MemoWidget):
	handledClass = news.News.Row
	
	def writeParagraph(self):
		wr = self.write
		row = self.target

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

		
## class ContextWidget(PageWidget):
## 	handledClass = Context
## 	def __init__(self,target,rsc,request):
## 		row=target.PAGES.findone(match='index')
## 		PageWidget.__init__(row,rsc,request)


class ContextWidget(Widget):
 	handledClass = Context

	def writePreTitle(self):
		ctx = self.target
		self.renderLink(
			url=self.baseuri,
			label=ctx.getLabel())
		
	def getLabel(self):
		return "List of tables"

	def writePage(self):
		wr = self.write
		ctx = self.target
		wr("<ul>")
		for ds in ctx.getDatasources():
			table = ds._table
			if table.getLabel() is not None:
				#if len(ds) != 0:
				wr('<li><a href="%s">%s</a>' % (
					self.uriToTable(table),
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
						self.uriToTable(table),
						table.getLabel()))
					sep=", "
