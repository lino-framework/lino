import os
import sys
from quixote.html import htmltext
#from quixote.demo.integer_ui import IntegerUI
#from quixote.errors import PublishError
from quixote.util import StaticDirectory

from lino.adamo.row import BaseRow
from lino.agui.ui import UI
from lino.agui.widgets import Window

# Get current directory
curdir = os.path.dirname(__file__)

## db = None
## def setDatabase(_db):
## 	global db
## 	db = _db




class DatabaseNamespace(UI):
	_q_exports = [ "_q_index", "main",  "dumpreq",  "srcdir" ]
	
	srcdir = StaticDirectory(curdir, list_directory=1)


## 	def __init__ (self, db):
## 		UI.__init__(self,db)
		# self.db = db
		
	def _q_index(self,request):
		body = """This is the main menu. Hello world!"""
		for (name,mb) in self.getMainWindow().getMenuBars().items():
			body += self.renderMenuBar(mb)
		return wholepage(self.db.getLabel(),body)


	def _q_lookup (self,request, name):
		name = name.upper()
		try:
			table = self.db.tables[name]
		except KeyError,e:
			raise TraversalError("No table named '%s'" % name)
		#rpt = table.report()
		return TableNamespace(table)
		# return IntegerUI(request, component)

	def _q_resolve (self,component):
		 # _q_resolve() is a hook that can be used to import only
		 # when it's actually accessed.  This can be used to make
		 # start-up of your application faster, because it doesn't have
		 # to import every single module when it starts running.
		 if component == 'form_demo':
			  from quixote.demo.forms import form_demo
			  return form_demo
		 # return wholepage('bla',"bla")

		 elif component == 'dumpreq':
			 from quixote.demo.pages import dumpreq
			 return dumpreq

	def renderMenuBar(self,mb):
		s = ""
		if mb.getLabel():
			s += '<p class="menu"><b>%s</b> ' % formatLabel(mb.getLabel())
		for mnu in mb.getMenus():
			s += '<br><b>%s</b>: ' % formatLabel(mnu.getLabel())
			for mi in mnu.getItems():
				s += self.renderAction(mi)
		return s

	def renderAction(self,mi):
		if mi.method == self.show:
			rpt = mi.args[0]
			url = "/" + rpt.query.leadTable.getName()+"/"
			#if hasattr(mi.target,"getName"):
			return ' [%s] ' % renderLink(url,mi.getLabel())
		else:
			return " [%s] " % htmltext(repr(mi))
	



class TableNamespace(Window):

	_q_exports = [ "_q_index" ]
	
	def __init__ (self, table):
		self.table = table
		Window.__init__(self,table.getLabel())

	def _q_index(self, request):
		rpt = self.table.getReport()
		return renderReport(rpt)
		
	def _q_lookup(self,request, name):
		try:
			i = int(name)
		except ValueError:
			try:
				rpt = self.table.getReport(name)
			except KeyError,e:
				raise TraversalError("No table named '%s'" % name)
			#rpt = table.report()
			return TableNamespace(table)
			# return IntegerUI(request, component)
		else:
			row = self.table[i]
			return RowNamespace(row)
		
class ReportNamespace(UI):
	_q_exports = [ "_q_index" ]
	#_q_exports = ['grid','form']

	def __init__ (self, request, report):
		self.report = report

	def _q_index (self, request):
		# ... generate summary page ...
		return renderGrid(self.report)

	def form (self, request):
		return wholepage(self.report.getLabel(),"... generate form page ...")

class RowNamespace(UI):
	_q_exports = [ "_q_index" ]
	#_q_exports = ['grid','form']

	def __init__ (self, request, report):
		raise "todo : continue here"
	   # and what about Window.setupMenu() ?
		self.report = report

	def _q_index (self, request):
		# ... generate summary page ...
		return renderGrid(self.report)

	def form (self, request):
		return wholepage(self.report.getLabel(),"... generate form page ...")


HEAD = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
          "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>%(title)s</title>
</head>
<body>
<table class="main"><tr><td valign="top">
%(leftMargin)s
<tr><td valign="top">
<h1>%(title)s</h1>
"""

FOOT = """
</td></tr></table>
</body>
</html>
"""


def wholepage(title,body,leftMargin=""):
	title= htmltext(title)
	return HEAD % vars() + body + FOOT

def renderLink(url,label):
   return '<a href="%s">%s</a>' % (url,formatLabel(label))


def formatLabel(label):
   p = label.find('~')
   if p != -1:
      label = label[:p] + '<u>' + label[p+1] + '</u>' + label[p+2:]
   return htmltext(label)
   
   #~ def formatValue(self,value):
      #~ if value is None:
         #~ return '&mdash;'
      #~ #if isinstance(value,BaseRow):
      #~ #   a = Action(label=str(row.id),
      #~ #              func=row.ui_openFormWindow)
      #~ #   return self.formatAction(a)
      #~ return self.escape(str(value))
      
      


def renderRow(row):
	return wholepage(title=row.getLabel(),
						  body=htmltext(str(row)))
	
def renderReport(report):
	report.setupReport()
	body = '<table border="1">'
	body += '<tr>'
	for col in report.getColumns():
		#~ a = Action( func=grid.setOrderBy, args=(col.name,))
		#~ ra = self.addAction(a)
		body += '<td>'
		body += col.getLabel()
		#~ self.wr(self.formatLink(label=col.getLabel(), action=ra))
		body += "</td>\n"
	body += '</tr>'
	for qrow in report:
		body += '\n<tr>\n'
		l = []
		i = 0
		for col in report.getColumns():
			body += '<td>'
			# value = col.atoms2value(atomicRow)
			value = qrow[i]
			i += 1

			if isinstance(value,BaseRow):
				body += value.getLabel()
				#~ a = Action( func=value.getGrid )
				#~ ra = self.addAction(a)
				#~ self.wr( self.formatLink(label=value.getLabel(),
												 #~ action=ra))
			else:
				body += str(value)# self.formatValue(value))
			body += '</td>'
		body += '\n</tr>'

	body += '\n</table>'

	return wholepage(report.getLabel(),body)
		









   
   #~ def renderGrid(self,grid):
      #~ q = grid.query
      #~ q.setLimitOffset(grid.pageLen,
                       #~ (grid.currentPage-1)*grid.pageLen)
      #~ if grid.isEditing:
         #~ a = Action(func=processForm,args=(grid,))
         #~ ra = self.addAction(a)
         #~ self.wr('\n<form action="%s" method="POST">' % \
                 #~ self.formatAction(ra))
      #~ if grid.asTable:
         #~ self.wr('<table border="1">')
         #~ self.wr('<tr>')
         #~ for col in q.getVisibleColumns():
            #~ a = Action( func=grid.setOrderBy, args=(col.name,))
            #~ ra = self.addAction(a)
            #~ self.wr('<td>')
            #~ self.wr(self.formatLink(label=col.getLabel(),
                                    #~ action=ra))
            #~ self.wr("</td>\n")
         #~ self.wr('</tr>')
         #~ for atomicRow in q.executeSelect():
            #~ self.wr('\n<tr>\n')
            #~ l = []
            #~ for col in q.getVisibleColumns():
               #~ self.wr('<td>')
               #~ value = col.atoms2value(atomicRow)

               #~ if isinstance(value,BaseRow):
                  #~ a = Action( func=value.getGrid )
                  #~ ra = self.addAction(a)
                  #~ self.wr( self.formatLink(label=value.getLabel(),
                                           #~ action=ra))
               #~ else:
                  #~ self.wr(self.formatValue(value))
               #~ self.wr('</td>')
            #~ self.wr('\n</tr>')

         #~ self.wr('\n</table>')
      #~ else:
         #~ for atomicRow in q.executeSelect():
            #~ row = q.provideRow(atomicRow)
            #~ self.wr('<h2>%s</h2>' % row.getLabel())
            #~ self.wr('\n<table border="1">')
            #~ for col in q.getVisibleColumns():
               #~ self.wr('\n<tr>')
               #~ self.wr("\n<td>")
               #~ self.wr(self.formatLabel(col.getLabel()))
               #~ self.wr("\n</td>")
               #~ self.wr("\n<td>")
               #~ value = col.atoms2value(atomicRow)
               #~ self.wr('<input type="text" value="%s">' \
                       #~ % self.formatValue(value))
               
               #~ self.wr("\n</td>")
               #~ self.wr('\n</tr>')

            #~ self.wr('\n</table>')


      #~ if grid.isEditing:
         #~ self.wr('\n<input type="submit">')
         #~ self.wr('\n</form>')
         

