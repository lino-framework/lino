#coding: latin1
#---------------------------------------------------------------------
# $Id: resources.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from cStringIO import StringIO

from twisted.web.resource import Resource

from lino.adamo.widgets import Window

from lino.adamo.html import MemoParser

#from skipper import Skipper
from widgets import Widget, ErrorWidget
#from webcal import WebCalendar

class AdamoResource(Window,Resource):

	def __init__(self, ctx, stylesheet=None):
		Resource.__init__(self)
		Window.__init__(self)
		self.context = ctx
		if stylesheet is None:
			stylesheet="files/default.css"
		self.stylesheet = stylesheet
		

	def getLabel(self):
		return self.context._db.getLabel()

	def show(self,widget):
		writer = StringIO()
		widget.show(writer)
		return writer.getvalue()

	def error(self,req,msg):
		w = ErrorWidget(msg,self,req)
		return self.show(w)


class DbResource(AdamoResource):
	isLeaf = True
	def __init__(self,ctx,wf,**kw):
		AdamoResource.__init__(self,ctx,**kw)
		self._wf = wf
		
	def getChild(self, name, request):
		raise "should never be called since isLeaf is True"
	
	def get_widget(self,target,request):
		return self._wf.get_widget(target,self,request)
	
	def render_index(self,request):
		raise NotImplementedError
	
	def render_GET(self,request):
		#renderer = TwistedRenderer(self,request)
		pp = list(request.postpath)
		if len(pp) and len(pp[-1]) == 0:
			pp = pp[:-1]
		
		if len(pp) == 0:
			widget = self._wf.get_widget(self.context,
												  self,
												  request)
			return self.show(widget)
			#return self.render_index(request)

		ds = getattr(self.context,pp[0],None)
		if ds is None:
			return self.error(request,
				'invalid tablename "%s"' % pp[0]
				)
			
		if len(pp) == 1:
			widget = self._wf.get_widget(ds,self,request,request.args)
			return self.show(widget)

		pp = pp[1:]
		id = pp[0].split(',')

		pka = ds._table.getPrimaryAtoms()
		if len(id) != len(pka):
			return self.error(request,
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
				return self.error(request,msg)
			rid.append(v)
			i += 1
		#rid = tuple(rid)
		row = ds.peek(*rid)
		if row is None:
			return self.error(request,
									"%s(%s) : no such row"%\
									(ds._table.getTableName(),
									 repr(id)))
		widget = self._wf.get_widget(row,self,request)
		return self.show(widget)

		
		
		




class WidgetResource(AdamoResource):
	
	"""A resource who delivers content using a given target with a given Renderer. Even no WidgetFactory is used.
	Note that WidgetResource is also used by server.WebServer
	"""
	
   #isLeaf = True
	def __init__(self,ctx,wcl,target,**kw):
		AdamoResource.__init__(self,ctx,**kw)
		self._wcl = wcl
		self._target = target

	def render_GET(self, request):
		widget = self._wcl(self._target,self,request)
		return self.show(widget)

	def getChild(self, name, request):
		if name == '':
			return self
		return Resource.getChild(self,name,request)

class RowResource(WidgetResource):
	"Resource who serves a known Row instance"
	def __init__(self,row,wf,**kw):
		#self.row = row
		self._wf = wf
		wcl = wf.get_wcl(row.__class__)
		WidgetResource.__init__(self,
										row._ds._context,
										wcl,
										row,**kw)

	def get_widget(self,target,request):
		return self._wf.get_widget(target,self,request)
	

class MainResource(RowResource):
	
	def __init__(self,ctx,wf,**kw):

		
		row = ctx.PAGES.findone(match="index")
		assert row is not None
		RowResource.__init__(self,row,wf,**kw)
		q = ctx.PAGES.query()
		q.setSqlFilters("match NOTNULL")
		for pg in q:
			#print "%s --> %s" % (pg.match,pg.title)
			self.putChild(pg.match,
							  RowResource(pg,wf,stylesheet=self.stylesheet))

		self.putChild('db',DbResource(ctx,wf,
												stylesheet=self.stylesheet))
		#self.putChild('calendar',WebCalendar(ctx,
		#												 wf,
		#												 stylesheet=self.stylesheet))

		



		


	
	

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

