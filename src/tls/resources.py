#coding: latin1
#---------------------------------------------------------------------
# $Id: resources.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from twisted.web.resource import Resource

from twisted.web import error
from twisted.web import static

#from lino.adamo.widgets import Window

from lino.adamo import InvalidRequestError

from lino.adamo.html import MemoParser
from lino.adamo.widgets import Action
from lino.adamo.forms import FormTemplate
from lino.misc.attrdict import AttrDict

from response import ContextedResponse

#from response import Response
#from widgets import Widget

#from skipper import Skipper
#from widgets import Widget, ErrorWidget
#from webcal import WebCalendar

	
CATCH_ERRORS = False

class AdamoResource(Resource):

	def __init__(self, parent, stylesheet=None):
		Resource.__init__(self)
		#Window.__init__(self,parent)
		if stylesheet is None:
			if (parent is None) or (parent.stylesheet is None):
				stylesheet="default.css"
			else:
				stylesheet = parent.stylesheet
		self.stylesheet = stylesheet
		#print self, stylesheet

	def render_POST(self,request):
		target = self.findTarget(request)
		responder = target.getRenderer(self,request,None)
		
		frm = responder.getSession().getCurrentForm()
		if frm is None:
			raise "POST without active form"
		if request.postdata['formName'][0] != frm.getFormName():
			msg = "POSTDATA form %s != current form '%s'" % \
					(repr(request.postdata['formName'][0]),
					 frm.getFormName())
			raise msg
		del request.postdata['formName']
		d = {}
		for k,v in request.postdata.items():
			if len(v[0]) == 0:
				d[k] = None
			else:
				d[k] = v[0]
		#print d # request.postdata
		frm.update(**d)
		#print frm._values
		frm.onSubmit()
		print "form has been submitted!"
		#return self.render_GET(request)
		
		return self.letRespond(responder)
		
		
	def render_GET(self,request):
		target = self.findTarget(request)
		responder = target.getRenderer(self,request,None)
		return self.letRespond(responder)

	def letRespond(self,responder):
		if CATCH_ERRORS:
			try:
				responder.writeWholePage()
			except Exception,e:
				responder.write(str(e))
		else:
			responder.writeWholePage()
		
		return responder._writer.getvalue()

	def getChild(self, name, request):
		if name == '':
			return self
		return Resource.getChild(self,name,request)
	


## class TargetResource(AdamoResource):
##  	"Resource who serves a constant (renderable) target"
	
##  	def __init__(self,parent,target,**kw):
## 		assert hasattr(target,"getRenderer")
## 		self._target = target
## 		AdamoResource.__init__(self,parent,**kw)
		
## 	def render_GET(self,request):
## 		#renderer = TwistedRenderer(self,request)
## 		return self.respond(request,self._target)
## 		#resp = Response(self,request)
## 		#self._row.asPage(resp)


## class TwistedWindow(Window):
## 	def __init__(self,ctx):
## 		Window.__init__(self,label=ctx.getLabel())
## 		self.context = ctx
		
## 	def getRenderer(self,resource,request,writer=None):
## 		return WindowResponse(resource,request,self,writer)

## 	def getContext(self):
## 		return self.context

## class FormResponse(ContextedResponse):
## 	handledClass = FormTemplate
	
## 	def onBeginResponse(self):
## 		for k,v in self.request.args.items():
## 			if k == "a":
## 				actionId = int(v[0])
## 			else:
## 				raise "invalid argument in URL"
		
	
## 	def writePage(self):
## 		wr = self.write
## 		wr('<ul>')
## 		for mnu in self.target.getMenus():
## 			self.renderMenu(self,mnu)
			
## 			#wr('<li>')
## 			#self.renderMenuBar(mb)
## 			#wr('</li>')
## 		wr('</ul>')


## 	def renderMenuBar(self,mb):
## 		raise "no longer used"
## 		wr = self.write
## 		if mb.getLabel():
## 			wr('<p class="menu"><b>%s</b> ' % self.formatLabel(mb.getLabel()))
## 		wr('<ul>')
## 		for mnu in mb.getMenus():
## 			wr('<li><b>%s</b>: ' % self.formatLabel(mnu.getLabel()))
## 			for mi in mnu.getItems():
## 				wr('<br>')
## 				self.renderFormattedLink(self.uriToAction(mi),
## 												 self.formatLabel(mi.getLabel()))

## 			wr('</li>')
## 		wr('</ul>')

## 	def uriToAction(self,a):
## 		if a.method == self.target.showReport:
## 			return self.uriToDatasource(*a.args,**a.keywords)
## 		#elif a.method == self.target.showMenu:
## 		#	return self.response.uriToMenu(*a.args,**a.keywords)
## 		return "oops"


## class MenuResource(AdamoResource):
## 	isLeaf = True
##  	def __init__(self,parent,ctx,**kw):
## 		AdamoResource.__init__(self,parent,**kw)
## 		self._window = TwistedWindow(ctx)
## 		ctx._db.schema.defineMenus(ctx,self._window)
		
## 	def render_GET(self,request):
## 		#renderer = TwistedRenderer(self,request)
## 		pp = list(request.postpath)
## 		if len(pp) and len(pp[-1]) == 0:
## 			pp = pp[:-1]
		
## 		if len(pp) == 0:
## 			return self.respond(request,self._window)

## 		return error.NoResource(
## 			'invalid postpath: %s' % str(pp)).render(request)

	
## 		mb = self.ui.getMenuBar(pp[0])
## 		if mb is None:
## 			return error.NoResource(
## 				'invalid menubar "%s"' % pp[0]).render(request)
## 		return self.respond(request,mb)
		
		

## class DbBrowser(AdamoResource):
## 	isLeaf = True
##  	def __init__(self,parent,ctx,**kw):
## 		self.context = ctx
## 		AdamoResource.__init__(self,parent,**kw)
	
## 	def getLabel(self):
## 		return "browse:" + self.context._db.getLabel()

## ## 	def __init__(self,ctx,**kw):
## ## 		AdamoResource.__init__(self,ctx,**kw)
## ## 		self._wf = wf
		
## 	def getChild(self, name, request):
## 		raise "should never be called since isLeaf is True"
	
## ## 	def get_widget(self,target,request):
## ## 		return self._wf.get_widget(target,self,request)
	
## ## 	def render_index(self,request):
## ## 		raise NotImplementedError

	
## 	def render_GET(self,request):
## 		#renderer = TwistedRenderer(self,request)
## 		pp = list(request.postpath)
## 		if len(pp) and len(pp[-1]) == 0:
## 			pp = pp[:-1]
		
## 		if len(pp) == 0:
## 			return self.respond(request,self.context)
## ## 			widget = self._wf.get_widget(self.context,
## ## 												  self,
## ## 												  request)
## ## 			return self.show(widget)
## 			#return self.render_index(request)

## 		ds = getattr(self.context,pp[0],None)
## 		if ds is None:
## 			return error.NoResource('invalid tablename "%s"' % pp[0]).render(request)

## ## 			return self.error(request,
## ## 				'invalid tablename "%s"' % pp[0]
## ## 				)
			
## 		if len(pp) == 1:
## 			return self.respond(request,ds)
## 			#return ds.asPage(resp)
## ## 			widget = self._wf.get_widget(ds,self,request,request.args)
## ## 			return self.show(widget)
		

## 		pp = pp[1:]
## 		id = pp[0].split(',')

## 		pka = ds._table.getPrimaryAtoms()
## 		if len(id) != len(pka):
## 			return error.NoResource(request, 'invalid id "%s"' % pp[0] ).render(request)
## 			#return "len(%s)!=len(%s)" % (repr(id), repr(pka))

			
## 		rid = []
## 		i = 0
## 		for (name,type) in pka:
## 			try:
## 				v = type.parse(id[i])
## 			except ValueError,e:
## 				msg="'%s' is not an %s" % (repr(id[i]), repr(type))
## 				return error.NoResource(request,msg).render(request)
## 			rid.append(v)
## 			i += 1
## 		#rid = tuple(rid)
## 		row = ds.peek(*rid)
## 		if row is None:
## 			return error.NoResource(request,
## 							 "%s(%s) : no such row"%\
## 							 (ds._table.getTableName(),
## 							  repr(id))).render(request)
## 		#row.asPage(resp)
## 		return self.respond(request,row)
## 		#widget = self._wf.get_widget(row,self,request)
## 		#return self.show(widget)

		
		
		




## class WidgetResource(AdamoResource):
	
## 	"""A resource who delivers content using a given target with a given Renderer. Even no WidgetFactory is used.
## 	Note that WidgetResource is also used by server.WebServer
## 	"""
	
##    #isLeaf = True
## 	def __init__(self,ctx,wcl,target,**kw):
## 		AdamoResource.__init__(self,ctx,**kw)
## 		self._wcl = wcl
## 		self._target = target

## 	def render_GET(self, request):
## 		widget = self._wcl(self._target,self,request)
## 		return self.show(widget)



## class RowResource(WidgetResource):
## 	"Resource who serves a known Row instance"
## 	def __init__(self,row,wf,**kw):
## 		#self.row = row
## 		self._wf = wf
## 		wcl = wf.get_wcl(row.__class__)
## 		WidgetResource.__init__(self,
## 										row._ds._context,
## 										wcl,
## 										row,**kw)

## 	def get_widget(self,target,request):
## 		return self._wf.get_widget(target,self,request)
	

## class MainResource(TargetResource):
	
## 	def __init__(self,ctx,**kw):

		
## 		row = ctx.PAGES.findone(match="index")
## 		assert row is not None
## 		TargetResource.__init__(self,row,**kw)
		
## 		q = ctx.PAGES.query()
## 		q.setSqlFilters("match NOTNULL")
## 		for pg in q:
## 			#print "%s --> %s" % (pg.match,pg.title)
## 			self.putChild(pg.match,
## 							  TargetResource(pg,stylesheet=self.stylesheet))

## 		self.putChild('db',ContextResource(ctx,
## 													  stylesheet=self.stylesheet))
## 		#self.putChild('calendar',WebCalendar(ctx,
## 		#												 wf,
## 		#												 stylesheet=self.stylesheet))

		



		


	
	

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




class DbResource(AdamoResource):
	isLeaf = True
 	def __init__(self,parent,ctx,staticDirs,**kw):
		self.context = ctx
		
## 		self.staticDirs = {}
## 		for (alias,path) in staticDirs.items():
## 			fr = static.File(path)
## 			print alias,"=", fr
## 			self.staticDirs[alias] = fr
			
		AdamoResource.__init__(self,parent,**kw)
		#self._window = TwistedWindow(ctx)
		#ctx._db.schema.defineMenus(ctx,self._window)
	

	#def getChild(self, name, request):
	#	raise "should never be called since isLeaf is True"
	
	def findTarget(self,request):
		#self.onRender(request)
		#renderer = TwistedRenderer(self,request)
		pp = list(request.postpath)
		if len(pp) and len(pp[-1]) == 0:
			pp = pp[:-1]
		
		if len(pp) == 0:
			return self.context.getContentRoot()
			#return self.context.getContentRoot().getRenderer(request)

		cmd = pp[0]
		if cmd == "db":

			del pp[0]
			#ds = getattr(self.context.tables,pp[0],None)
			ds = self.context.getDatasource(pp[0])
## 			if ds is None:
## 				raise 
## 				return error.NoResource(
## 					'invalid tablename "%s"' % pp[0]).render(request)

			if len(pp) == 1:
				return ds
				#return ds.getRenderer(request)
			   #return self.respond(request,ds)

			del pp[0]
			#pp = pp[1:]
			id = pp[0].split(',')

			pka = ds._table.getPrimaryAtoms()
			if len(id) != len(pka):
				raise InvalidRequestError('invalid id "%s"' % pp[0])
## 				return error.NoResource(
## 					request, 'invalid id "%s"' % pp[0]
## 					).render(request)


			rid = []
			i = 0
			for (name,type) in pka:
				try:
					v = type.parse(id[i])
				except ValueError,e:
					msg="'%s' is not an %s" % (repr(id[i]), repr(type))
					raise InvalidRequestError(msg)
					#return error.NoResource(msg).render(request)
				rid.append(v)
				i += 1
			row = ds.peek(*rid)
			if row is None:
				msg = "%s(%s) : no such row"% (
					ds._table.getTableName(), repr(id))
				raise InvalidRequestError(msg)
				#return error.NoResource(msg).render(request)
			#return self.respond(request,row)
			return row
			#return row.getRenderer(request)

		if cmd == "menu":
			#return self.respond(request,self._window)
			#return self._window.getRenderer(request)
			raise "und jetzt?"
			#return self._window
		
## 		try:
## 			#print request.method
## 			fr = self.staticDirs[cmd]
## 			del request.postpath[0]
## 			return fr.render(request)
## 		except KeyError,e:
## 			print str(e)
			
		return error.NoResource(
			'invalid postpath: %s' % str(pp)).render(request)

		
