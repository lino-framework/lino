#coding: latin1
#---------------------------------------------------------------------
# $Id: twisted_ui.py,v 1.21 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

raise "no longer used. replaced by tls package"

import os
import webbrowser

from twisted.web.resource import Resource
from twisted.web import error, server, static, vhost
from twisted.internet import reactor

#from twisted.application import internet, service

from lino.misc.etc import issequence

from lino import copyright 
from widgets import Window
from widgets import Widget
#from lino.adamo.ui import UI
from html import HtmlRenderer, htmltext, MemoParser
from skipper import Skipper
		
class TwistedRenderer(HtmlRenderer):
	defaultLangs = ('en,')

	def __init__(self,rsc,request):
		self.resource = rsc
		self.request = request
		
		if rsc.db is not None:
			self.defaultLangs = (rsc.db.getDefaultLanguage(),)
		self.langs = request.args.get('lng',self.defaultLangs)

		updirsToBase = len(self.request.prepath) \
							+ len(self.request.postpath) \
							-2
		self.baseuri = '../' * updirsToBase
		
		self._body = ''

	def formatLabel(self,label):
		p = label.find(self.resource.db.schema.HK_CHAR)
		if p != -1:
			label = label[:p] + '<u>' + label[p+1] + '</u>' + label[p+2:]
		return str(htmltext(label))

	def uriToTable(self,table):
		return self.baseuri + 'db/' + table.name
		#return self.request.prePathURL() + "/" + table.getName()

	def uriToRow(self,row):
		url = self.uriToTable(row._area._table)
		url += '/' + ','.join([str(v) for v in row.getRowId()])
		return url

	def uriToSkipper(self,skipper,**p):
		#p={}
		if skipper.pageLen != 15:
			p.setdefault('pl',skipper.pageLen)
		return self.uriToDatasource(skipper.ds,**p)
	
	def uriToDatasource(self,ds,**p):
		if ds._query.orderBy != None:
			p.setdefault('ob',ds._query.orderBy)
		if ds._query.search != None:
			p.setdefault('search', ds._query.search)
		if ds._query.filters != None:
			p.setdefault('flt',ds._query.filters)

		# todo : compare with query.setSamples(). Similar code
		atomicRow = [None] * len(ds._query.columnList._atoms)
		for (col,value) in ds._query.samples:
			col.rowAttr.value2atoms(value,atomicRow,col.getAtoms())
			l = []
			for atom in col.getAtoms():
				l.append( atomicRow[atom.index] )
			s = ','.join([str(v) for v in l])
			p[col.name] = s

		
		#for (atom,value) in ds._query.sampleColumns:
		#	p[atom.name] = value
			
## 		if ds._query.atomicSamples is not None:
## 			for (atom,value) in ds._query.atomicSamples:
## 				p[atom.name] = value

		#uri = self.baseuri + 'db/' + ds._query.leadTable.name
		uri = self.uriToTable(ds._query.leadTable)
		return self.buildURL(uri,p)

	def buildURL(self,url,flds):
		sep = "?"
		for (k,v) in flds.items():
			if issequence(v):
				for i in v:
					url += sep + k + "=" + str(i)
					sep = "&"
			elif v is not None:
				url += sep + k + "=" + str(v)
				sep = "&"
		return url
		
	def uriToSelf(self,*args,**options):
		flds = self.request.args.copy()
		for (k,v) in options.items():
			flds[k] = v
		url = self.request.prePathURL() 
		
## 		if len(self.request.postpath):
## 			url += "/" + "/".join(self.request.postpath)
		if len(args):
			url += "/" + "/".join([str(v) for v in args])
		return self.buildURL(url,flds)
	
	def refToSelf(self,label,**options):
		url = self.uriToSelf(**options)
		return '<a href="%s">%s</a>' % (url,label)

	
	def renderImage(self,src,tags=None,label=None):
		self.write(self.refToImage(src,tags,label))
					  
	def refToImage(self,src,tags=None,label=None):
		if label is None:
			label = src
		#print vars()
		src = self.baseuri+"images/"+src
		s = '<img src="%s" alt="%s"' % (src,htmltext(label))
		if tags is not None:
			s += tags
		s += ">"
		return s

	def renderMemo(self,txt):
		# memo2html
		self.resource.memo2html(self,txt)

	
	def getLabel(self):
		return self.main.getLabel()

	def write(self,s):
		#self.request.write(s)
		self._body += s

	def show(self,widget):
		self.writeWidget(widget)
		return self._body 
		#return server.NOT_DONE_YET
	
	def writeWidget(self,widget):
		assert isinstance(widget,Widget)
		title = htmltext(widget.getLabel())

		wr = self.write

		wr("""\
		<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
		"http://www.w3.org/TR/html4/loose.dtd">
		<html>
		<head>
		""")
		wr("<title>%s</title>" % title)
		if self.resource.stylesheet is not None:
			wr("""\
			<link rel=stylesheet type="text/css" href="%s">
			""" % (self.baseuri+self.resource.stylesheet))
		wr("""
		</head>
		<body>
		""")
		wr(self.BEFORE_LEFT_MARGIN)
		wr('''<a href="%s.">Home</a>''' % self.baseuri)
		if self.resource.db is not None:
			if len(self.resource.db._db.getBabelLangs()) > 1:
				wr('<p>')
				for lang in self.resource.db._db.getBabelLangs():
					if lang.id == self.langs[0]:
						wr(lang.id)
					else:
						self.renderLink(url=self.uriToSelf(lng=lang.id),
											 label=lang.id)
					wr(' ')
				wr('</p>')
					
		widget.asLeftMargin(self)
		wr(self.AFTER_LEFT_MARGIN)
		wr("""
		<table class="head">
		<tr>
		<td>
		""")
		widget.asPreTitle(self)
		wr('<p class="title">%s</p>' % title)
		wr("""
		</td>
		</tr>
		</table>
		""")

		widget.asBody(self)

		wr(self.BEFORE_FOOT)
		wr("""<td align="left" valign="center">""")
		self.writeLeftFooter()
		wr("</td>")
		
		wr(self.BETWEEN_FOOT)
		self.renderLink(url=self.uriToSelf())
		wr(self.AFTER_FOOT)



	def writeLeftFooter(self):
		self.write("""
		<font size=1>
		This is a
		<a href="http://www.twistedmatrix.com/"
		target="_top">Twisted</a> server.
		<A HREF="%scopyright">Copyright 1999-2004 Luc Saffre</A>.
		</font>
		""" % self.baseuri)
		

class AdamoResource(Window,Resource):

	def __init__(self, db, stylesheet=None):
		Resource.__init__(self)
		Window.__init__(self)
		self.db = db
		#self.baseuri = baseuri
		if stylesheet is None:
			stylesheet="files/default.css"
		self.stylesheet = stylesheet
		
		cmds = {
			'url' : self.cmd_url,
			'ref' : self.cmd_ref,
			'xe' : self.cmd_ref,
			'img' : self.cmd_img
			}
		
		self.memoParser = MemoParser(cmds)

	def getLabel(self):
		return self.db.getLabel()

	def wholepage(self,renderer,title,body=None,preTitle=None):
		raise DeprecationError
## 		renderer.renderPage(
## 			title,
## 			body=body,
## 			preTitle=preTitle,
## 			leftMargin = self.renderLeftMargin,
## 			leftFooter = self.renderLeftFooter,
## 			stylesheet = self.stylesheet)
## 		return renderer._body

	def cmd_img(self,renderer,s):
		s = s.split(None,1)
		renderer.refToImage(*s)

	def cmd_ref(self,renderer,s):
		s = s.split(None,1)
		ref = s[0].split(':')
		if len(ref) != 2:
			return None
		try:
			if ref[0] == "MSX":
				ref[0] = "PAGES"
			elif ref[0] == "TPC":
				ref[0] = "TOPICS"
			elif ref[0] == "AUT":
				ref[0] = "AUTHORS"
			elif ref[0] == "NEW":
				ref[0] = "NEWS"
			elif ref[0] == "PUB":
				ref[0] = "PUBLICATIONS"
			area = getattr(self.db,ref[0])
		except AttributeError,e:
			return None
			#return str(e)
		s[0] = renderer.uriToTable(area._table)+"/"+ref[1]
		renderer.renderLink(*s)

	def cmd_url(self,renderer,s):
		s = s.split(None,1)
		renderer.renderLink(*s)
	## 	if len(s) == 2:
	## 		return renderLink(s[0],label=s[1])
	## 	else:
	## 		return renderLink(s[0])

	def memo2html(self,renderer,txt):
		if txt is None:
			return ''
		txt = txt.strip()
		self.memoParser.parse(renderer,txt)
		#return self.memoParser.html



					
		

class WidgetResource(AdamoResource):
	"""
	A resource who delivers content using a main widget
	"""
   #isLeaf = True
	def __init__(self,db,widget,**kw):
		assert isinstance(widget,Widget),\
				 "%s is not a Widget" % repr(widget)
		AdamoResource.__init__(self,db,**kw)
		self.widget = widget

	def render_GET(self, request):
		renderer = TwistedRenderer(self,request)
		return renderer.show(self.widget)

	def getChild(self, name, request):
		if name == '':
			return self
		return Resource.getChild(self,name,request)


	

from lino.schemas.sprl import web, events

	

class RowWidget(Widget):
	handledClass = adamo.Table
	def __init__(self,row):
		self.row = row



class MemoWidget(RowWidget):
	handledClass = adamo.MemoTable
	
	def asParagraph(self,row,renderer):
		self.asLabel(row,renderer)
		renderer.write('\n&mdash; ')
		renderer.renderMemo(self.row.abstract)

	def asPage(self,renderer):
		wr = renderer.write
		wr('<p>')
		renderer.renderMemo(self.row.abstract)
		wr('</p>')
		wr('<p>')
		renderer.renderMemo(self.row.body)
		wr('</p>')
		self.renderRowDetails(self.row,renderer)
		#return body

#declare_widget(web.MemoTable,MemoWidget)

class TreeWidget(RowWidget):
	handledClass = adamo.TreeTable
	def asPreTitle(self,renderer):
		wr = renderer.write
		sep = ""
		for superRow in self.row.getUpTree():
			wr(sep)
			renderer.renderLink(
				url=renderer.uriToRow(superRow),
				label=superRow.getLabel())
			sep = " &middot; "

## 		wr(" (")
## 		renderer.renderLink(
## 			url=renderer.tableUrl(self._area._table),
## 			label=self._area._table.getLabel())
## 		wr(")")
		#body += "]]]</p>"
		
	def asPage(self,renderer):
		wr = renderer.write
		wr("<ul>")
		for row in self.children.query(orderBy="seq").instances():
			wr('<li>')
			row.asParagraph(renderer)
			wr("</li>")
		wr("</ul>")

#declare_widget(web.TreeTable,TreeWidget)

	
class MemoTreeWidget(MemoWidget,TreeWidget):
	handledClass = adamo.MemoTreeTable
	def renderDetails(self,renderer):
		pass
	
	def asPage(self,renderer):
		MemoWidget.asPage(self,renderer)
		TreeWidget.asPage(self,renderer)

#declare_widget(web.TreeTable,MemoWidget)
		
		
class PageWidget(MemoTreeWidget):
	handledClass = web.Pages
	
	def asFooter(self,renderer):
		wr = renderer.write
		wr('<table border="0">')
		for name in 'created modified author lang'.split():
			value = getattr(self.row,name)
			if value is not None:
				attr = self.row._area._table._rowAttrs[name]
				wr('\n<tr><td>' + name+ '</td><td>')
				type = getattr(attr,'type',None)
				renderer.renderValue(value,type)
				wr('</td>\n</tr>')

		wr('\n</table>')


class EventWidget(PageWidget):
	handledClass = events.Events
	def asParagraph(self,renderer):
		wr = renderer.write
		self.asLabel(renderer)
		wr('\n&mdash; ')
		if self.title:
			wr(" " + self.title)
			
		if self.type:
			wr(" ")
			self.type.asLabel(renderer)
		if self.place:
			wr("<br>Ort: ")
			self.place.asLabel(renderer)
		if self.responsible:
			wr("<br>Veranstalter: ")
			self.responsible.asLabel(renderer)
		if self.time:
			wr("<br>Uhrzeit: " + self.time )
		renderer.renderMemo(self.abstract)
		#if self.body is not None:
		wr("<br>")
		renderer.renderLink(renderer.uriToRow(self),
								  label="more")

	def asPage(self,renderer):
		MemoWidget.asPage(self,renderer)
		RowWidget.asPage(self,renderer)
		

widgets = {
	web.Pages : PageWidget,
	events.Events : EventWidget,
	}



def get_bases_widget(cl):
	for base in cl.__bases__:
		try:
			return widgets[cl]
		except KeyError:
			pass
	raise KeyError

		
def get_widget(cl):
	try:
		return widgets[cl]
	except KeyError:
		pass
	
	try:
		return get_bases_widget(cl)
	except KeyError:
		pass
	
	for base in cl.__bases__:
		try:
			return get_bases_widget(base)
		except KeyError:
			pass

def get_rowwidget(row):		
	cl = get_widget(row._ds._table.__class__)
	return cl(row)
		
class RowResource(WidgetResource):
	def __init__(self,row,**kw):
		db = row._ds._db
		widget = get_rowwidget(row)
		WidgetResource.__init__(self,db,widget,**kw)

class MainResource(RowResource):
	
	def __init__(self,ctx,staticDirs={},**kw):
		row = ctx.PAGES.findone(match="index")
		assert row is not None
		RowResource.__init__(self,row,**kw)
		q = ctx.PAGES.query()
		q.setSqlFilters("match NOTNULL")
		for pg in q:
			#print "%s --> %s" % (pg.match,pg.title)
			self.putChild(pg.match,
							  RowResource(pg,stylesheet=self.stylesheet))
		for (name,path) in staticDirs.items():
			#print name, path
			self.putChild(name, static.File(path))

		self.putChild('db',DbResource(ctx,stylesheet=self.stylesheet))
		from webcal import WebCalendar
		self.putChild('calendar',WebCalendar(ctx,
														 stylesheet=self.stylesheet))

		



class DbResource(AdamoResource):
	isLeaf = True
	def __init__(self,ctx,staticDirs={},**kw):
		AdamoResource.__init__(self,ctx,**kw)
		
		for (name,path) in staticDirs.items():
			#print name, path
			self.putChild(name, static.File(path))

	def getChild(self, name, request):
		raise "should never be called since isLeaf is True"
	
	def render_GET(self,request):
		renderer = TwistedRenderer(self,request)
		pp = list(request.postpath)
		if len(pp) and len(pp[-1]) == 0:
			pp = pp[:-1]
		
		if len(pp) == 0:
			row=self.db.PAGES.findone(match='index')
			return renderer.show(get_rowwidget(row))
		
		ds = getattr(self.db,pp[0])
		if len(pp) == 1:
			skipper = Skipper(ds,request)
			
			#skipper = Skipper(ds,tplid,**rptParams)

			return renderer.show(skipper)

		pp = pp[1:]
		id = pp[0].split(',')

		pka = area._table.getPrimaryAtoms()
		if len(id) != len(pka):
			return renderer.error(
				'invalid id "%s"' % pp[0]
				)
			#return "len(%s)!=len(%s)" % (repr(id), repr(pka))

			
		rid = []
		i = 0
		for (name,type) in pka:
			try:
				v = type.parse(id[i])
			except ValueError,e:
				msg="'%s' is not an %s" % (repr(id[i]), repr(type))
				return renderer.error(msg)
			rid.append(v)
			i += 1
		rid = tuple(rid)
		row = area[rid]
		#renderer.renderForm(row)
		return renderer.show(row)

		
		
		


	
	

## class Stopper(AdamoResource):

## 	def __init__(self,parent):
## 		AdamoResource.__init__(self,parent)
	
## 	def render_GET(self, request):
## 		reactor.stop()
## 		return self.wholepage(
## 			request,
## 			preTitle="Now it happened!",
## 			title="The Very End",
## 			body="""You asked me to stop serving.
## 			In deine Hände lege ich voll Vertrauen meinen Geist.
## 			""",
## 			leftMargin="")

## class Searcher(AdamoResource):

## 	def __init__(self,parent):
## 		AdamoResource.__init__(self,parent)
		
	
## 	def render_GET(self, request):
## 		search = request.args.get('search','')
## 		uri = self.uriToSelf()
## 		body = """\
## 		<form action="%(uri)s" method="GET" enctype="Mime-Type">
## 		Search: <input type="text" name="search" value="%(what)s">
## 		</form>		
## 		""" % vars()
## 		searchFields = ('title','abstract','body')
## 		if len(what):
## 			flt = " OR ".join(
## 				[n+" LIKE '%"+what+"%'" for n in searchFields])
			
## 			q = self.db.PAGES.report()
## 			for row in self.q.instances(filters=flt)
## 		return self.wholepage(
## 			request,
## 			title="Search",
## 			body="""
## 			""",
## 			leftMargin="")


def hostname():
	if os.name == 'nt':
		name= os.getenv('COMPUTERNAME')
	else:
		name = os.getenv('HOSTNAME')
	#'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'

	if name is None:
		name = 'localhost'
	return name


class WebServer(Widget):
	def __init__(self,ui,
					 hostName=None,
					 port=8080,**kw):
		self.ui = ui
		self.port = port
		if hostName is None:
			hostName = hostname()
		self.hostName = hostName
		#url = "http://" + self.hostName
		#if self.port != 80:
		#	url += ":" + str(self.port)
		#self.baseuri = url
		self.accounts = {}

	def addDatabase(self, db, **kw):
		rsc = MainResource(db.beginContext(),**kw)
		#rsc = DbResource(db,**kw)
		self.accounts[db.name] = rsc
		self.ui.addDatabase(db)

	def addAccount(self,name,staticDir):
		raise NotImplementedError

	def getLabel(self):
		return 'Lino Server'

	def asPreTitle(self,renderer):
		pass

	def asBody(self,renderer):
		body = ""
		for name,a in self.accounts.items():
			body += "<li>"
			body += '<a href="'+name+'/">' + name + " : " + a.getLabel()+'</a>'
			body += "</li>"
		body += "</ul>"
		renderer.write(body)
		
	
	def run(self,showOutput=False):
	
		if self.ui.verbose:
			print "Lino Web Server" # version " + __version__
			print copyright(year='2004',author='Luc Saffre')
			print
			print "Serving on port %s." % self.port

		if len(self.accounts.keys()) > 1:
			root = WidgetResource(None, self)
			for (name,accnt) in self.accounts.items():
				#accnt.renderer.setupRenderer(self.baseuri+"/"+name)
				root.putChild(name,accnt)
		else:
			accnt = self.accounts[0]
			#accnt.renderer.setupRenderer(self.baseuri+"/"+name)
			root = accnt

		site = server.Site(root)
		reactor.listenTCP(self.port, site)
		reactor.addSystemEventTrigger("before","shutdown",
												self.ui.shutdown)

		#if showOutput:
		#	webbrowser.open(self.baseuri,new=True)
			
		if self.ui.verbose:
			print "(Press Ctrl-C to stop serving)"
			
		reactor.run()
		



## 	root = UiResource
## 	dbr = DbResource(db,
## 						  baseuri=url,
## 						  staticDirs,
## 						  stylesheet=stylesheet,
## 						  leftMargin=leftMargin)

	#root = twisted_ui.RootResource(db)

   #root.putChild("stop", Stopper(root))
   #root.putChild("search", Searcher(root))
		

## 	if len(ui._databases.keys()) > 1:
## 		root = vhost.NameVirtualHost()
## 		root.default = ...
	
		
## 		application = service.Application('web')
## 		sc = service.IServiceCollection(application)
## 		site = server.Site(root)
## 		i = internet.TCPServer(80, site)
## 		i.setServiceParent(sc)

## 	else:
## 		root = dbr


