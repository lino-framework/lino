#coding: latin1
#---------------------------------------------------------------------
# $Id: widgets.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

from lino import adamo
from lino.adamo.html import txt2html
from lino.adamo.rowattrs import Field, Pointer, Detail
from lino.misc.etc import issequence

from twisted.web.html import escape


#from quixote.html import htmltext  # to be replaced by equivalent
def htmltext(s):
	s = escape(s)
	# s = s.replace('<','&lt;')
	# s = s.replace('>','&gt;')
	# s = s.replace('&','&amp;')
	return txt2html(s)


from lino.adamo.datatypes import MemoType, UrlType, EmailType, LogoType, ImageType


class HtmlRenderer:
	
	showRowCount = True
	
	BEFORE_LEFT_MARGIN="""
	<table class="main"><tr>
	<td class="left" width="15%%">
	"""
	AFTER_LEFT_MARGIN="""
	</td>
	<td valign="top">
	"""

	BEFORE_FOOT = """
	</td></tr></table>
	<table class="foot">
	<tr>
	"""
	
	BETWEEN_FOOT = """
	<td align="right" valign="center">
	"""
	
	AFTER_FOOT = """
	</td>
	</tr>
	</table>
	</body>
	</html>
	"""

	def renderLink(self,url,label=None):
		if label is None:
			label = url
		else:
			#print url, label
			label = htmltext(label)
		self.renderFormattedLink(url,label)

	def renderFormattedLink(self,url,label):
		self.write('<a href="%s">%s</a>' % (url,label))

	def renderMenuBar(self,mb):
		s = ""
		if mb.getLabel():
			s += '<p class="toc"><b>%s</b> ' \
				  % self.formatLabel(mb.getLabel())
		for mnu in mb.getMenus():
			s += '<br><b>%s</b>: ' % self.formatLabel(mnu.getLabel())
			for mi in mnu.getItems():
				s += "<br>" + self.renderAction(mi)
		self.write(s)


	def renderCellValue(self,col,value):
		if isinstance(col.rowAttr,Detail):
			self.asParagraph(value)
		if isinstance(col.rowAttr,Pointer):
			self.renderLink(
				url=self.uriToRow(value),
				label=value.getLabel())
		if isinstance(col.rowAttr,Field):
			self.renderValue(value,col.rowAttr.type)


	def renderValue(self,value,type,
						 size=(10,3)):

		if value is None:
			self.write("&nbsp;")
			return

		#if hasattr(value,'asParagraph'):
		#	return value.asParagraph(self)
		if hasattr(value,'asLabel'):
			return value.asLabel(self)

		if type is not None:
			if isinstance(type,MemoType):
				return self.renderMemo(value)
			if isinstance(type,LogoType):
				w = size[0]
				if w is None:
					w = 10
				w *= 10
				return self.renderImage(src=value,
												tags='width="%d"' % w,
												label=value)
			if isinstance(type,ImageType):
				return self.renderImage(src=value,label=value)
			if isinstance(type,UrlType):
				return self.renderLink(value)
			if isinstance(type,EmailType):
				return self.renderFormattedLink('mailto:'+value,
											  label=value)
			#self.write('unkown type %s'%repr(type))
		self.write(htmltext(str(value)))

	def writeForm(self,labeledValues):
		wr = self.write
		wr('<table border="0" class="data">')
		for label,value in labeledValues:
			#if not name in ('abstract','body'):
			#value = getattr(row,attr.name)
			if value is not None:
				wr('\n<tr><td>' + label + '</td>\n<td>')
				wr('\n<tr><td>' + value + '</td>\n<td>')
## 				if hasattr(value,'asFormCell'):
## 					value.asFormCell(renderer)
## 				else:
## 					type = getattr(attr,'type',None)
## 					renderer.renderValue(value,type)
				wr('</td>\n</tr>')

		wr('\n</table>')
		

	def writeDebugMessage(self,msg):
		self.write('<font size="1" color="grey">')
		self.write(escape(msg))
		self.write('</font>')


	def refToSelf(self,label,*args,**options):
		raise NotImplementedError




class TwistedRenderer(HtmlRenderer):
	#defaultLangs = ('en,')

	CLEAR = "__CLEAR"

	def __init__(self,rsc,request):
		self.resource = rsc
		self.request = request
		
## 		if rsc.db is not None:
## 			self.defaultLangs = (rsc.db.getDefaultLanguage(),)
## 		self.langs = request.args.get('lng',self.defaultLangs)

		updirsToBase = len(self.request.prepath) \
							+ len(self.request.postpath) \
							-2
		self.baseuri = '../' * updirsToBase
		
		#self._body = ''
		self._writer = None

	def write(self,s):
		#self.request.write(s)
		#self._body += s
		self._writer.write(s)

	def get_widget(self,target):
		w = self.resource.get_widget(target,self.request)
		w._writer = self._writer
## 		self.writeDebugMessage("widgets.py:get_widget(%s) -> %s" % \
## 									  (repr(target),repr(w)))
		return w
	
	def asLabel(self,target):
		widget = self.get_widget(target)
		widget.writeLabel()
		
	def asParagraph(self,target):
		widget = self.get_widget(target)
		#self.writeDebugMessage("foofoo")
		#self.writeDebugMessage(repr(widget))
		widget.writeParagraph()
		#self.write("[%s]" % widget.__class__.__name__)
		#self.writeDebugMessage("barbar")
		
	def asFormCell(self,target):
		self.asParagraph(target)


	def formatLabel(self,label):
		p = label.find(self.resource.context.schema.HK_CHAR)
		if p != -1:
			label = label[:p] + '<u>' + label[p+1] + '</u>' + label[p+2:]
		return str(htmltext(label))

	def uriToTable(self,table):
		return self.baseuri + 'db/' + table.getTableName()
		#return self.request.prePathURL() + "/" + table.getName()

	def uriToRow(self,row):
		url = self.uriToTable(row._ds._table)
		url += '/' + ','.join([str(v) for v in row.getRowId()])
		return url

	def uriToDatasource(self,ds,**p):
		if ds._orderBy != None:
			p.setdefault('ob',ds._orderBy)
		if ds._viewName != None:
			p.setdefault('v', ds._viewName)
		if ds._search != None:
			p.setdefault('search', ds._search)
		if ds._sqlFilters != None:
			p.setdefault('flt',ds._sqlFilters)

		for (key,value) in ds._samples.items():
			col = ds._clist.getColumn(key)
			p[key] = col.format(value,ds)

		uri = self.uriToTable(ds._table)
		return self.buildURL(uri,p)

	def buildURL(self,url,flds):
		sep = "?"
		for (k,v) in flds.items():
			if issequence(v):
				for i in v:
					url += sep + k + "=" + str(i)
					sep = "&"
			elif v is not self.CLEAR:
				if v is None:
					url += sep + k + "=" 
				else:
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

	
	def renderPicture(self,src,tags=None,label=None):
		self.write('<a href="%s">' % self.uriToImage('pictures',src))
		self.renderImage('thumbnails',src,tags,label)
		self.write('</a>')
					  
	def renderImage(self,imageType,src,tags=None,label=None):
		self.write(self.refToImage(imageType,src,tags,label))
					  
	def refToImage(self,imageType,src,tags=None,label=None):
		if label is None:
			label = src
		#print vars()
		src = self.uriToImage(imageType,src)
		s = '<img src="%s" alt="%s"' % (src,htmltext(label))
		if tags is not None:
			s += tags
		s += ">"
		return s

	def uriToImage(self,imageType,src):
		return self.baseuri+"images/"+imageType+"/"+src
	
	def renderMemo(self,txt):
		# memo2html
		self.resource.context.memo2html(self,txt)

	
## 	def getLabel(self):
## 		return self.main.getLabel()

	def writeBody(self):
		self.writePage()
		self.writeFooter()

	def writeFooter(self):
		pass

	def writeLeftMargin(self):
		self.write('''<br><a href="%scalendar">Calendar</a>'''
			% self.baseuri)

	def writePreTitle(self):
		pass
		#self.write('preTitle')
		
	def writeWholePage(self):
		#assert isinstance(widget,Widget)
		#target = self.target
		title = htmltext(self.getLabel())

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
		if self.resource.context is not None:
			if len(self.resource.context._db.getBabelLangs()) > 1:
				wr('<p>')
				for lang in self.resource.context._db.getBabelLangs():
					#if lang.id == self.langs[0]:
					#	wr(lang.id)
					#else:
					self.renderLink(url=self.uriToSelf(lng=lang.id),
										 label=lang.id)
					wr(' ')
				wr('</p>')
					
		self.writeLeftMargin()
		wr(self.AFTER_LEFT_MARGIN)
		wr("""
		<table class="head">
		<tr>
		<td>
		""")
		self.writePreTitle()
		wr('<p class="title">%s</p>' % title)
		wr("""
		</td>
		</tr>
		</table>
		""")

		self.writeBody()

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
		This site is hosted on a
		<a href="http://localhost:8080"
		target="_top">Twisted Lino Server</a>.
		<A HREF="%scopyright">Copyright 1999-2004 Luc Saffre</A>.
		%s
		</font>
		""" % (self.baseuri,self.__class__.__name__))
		
	

	




class Widget(TwistedRenderer):
	#handledClass = None
	def __init__(self, target, rsc, request):
		self.target = target
		TwistedRenderer.__init__(self,rsc,request)

	def show(self,writer):
		self._writer = writer
		self.writeWholePage()
		#return self._body 
		#return server.NOT_DONE_YET
	
	def getLabel(self):
		return self.target.getLabel()

	


class RowWidget(Widget):
	#handledClass = adamo.Table.Row
	#def __init__(self,row):
	#	self.row = row

	def writeLeftMargin(self):
		Widget.writeLeftMargin(self)
		self.write('<p><a href="add">add row</a>')
		self.write('<br><a href="delete">delete row</a></p>')
		self.writeContextMenu(self.target._ds._context)
		#self.target._ds._context.writeLeftMargin(renderer)
		
	def writeContextMenu(self,ctx):
		raise NotImplementedError

## 	def writePreTitle(self):
## 		pass
	
	def writeLabel(self):
		self.renderLink(
			url=self.uriToRow(self.target),
			label=self.target.getLabel())
		
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
				wr('<td>' + label + '</td>')
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
		

## 	def renderDetails(self):
## 		pass
## 		wr = renderer.write
## 		if False:
## 			wr("<ul>")
## 			for (name,dtl) in self._area._table._details.items():
## 				rpt = dtl.query(self)
## 				wr('<li>')
## 				rpt.asParagraph(renderer)
## 				wr("</li>")

## 			wr("</ul>")
		
			
	def writeParagraph(self):
		self.writeLabel()
## 		wr = renderer.write
## 		for name,attr in self._area._table._rowAttrs.items():
## 			if not name in ('body'):
## 				value = getattr(self,name)
## 				if value is not None:
## 					wr('<b>%s:</b> ' % name)
## 					type = getattr(attr,'type',None)
## 					renderer.renderValue(value,type)
## 					wr(" ")


class ErrorWidget(Widget):
	handledClass = None
	
	def writeLeftMargin(self):
		pass
	
	def writeBody(self):
		self.write(self.target)
	
	def getLabel(self):
		return "Error"
	
	def writePreTitle(self):
		pass
	
class WidgetFactory:
	def __init__(self,mod):
		self._widgets = {}
		for k,v in mod.__dict__.items():
			if type(v) is types.ClassType:
				if issubclass(v,Widget):
					try:
						hcl = v.handledClass
					except AttributeError:
						pass
					else:
						assert not self._widgets.has_key(hcl),\
								 repr(v) + ": duplicate class handler for " + repr(hcl)
						self._widgets[hcl] = v
						#print k,v.handledClass,v

		for k,v in self._widgets.items():
			print str(k), ":", str(v)
		print len(self._widgets), "class widgets"

	def get_bases_widget(self,cl):
		#print "get_bases_widget(%s)" % repr(cl)
		try:
			return self._widgets[cl]
		except KeyError:
			pass #print "no widget for " + repr(cl)

		for base in cl.__bases__:
			try:
				return self._widgets[base]
			except KeyError:
				#print "no widget for " + repr(cl)
				pass
		raise KeyError


	def get_wcl(self,cl):
		#print "get_wcl(%s)" % repr(cl)
		try:
			return self.get_bases_widget(cl)
		except KeyError:
			pass

		for base in cl.__bases__:
			try:
				return self.get_bases_widget(base)
			except KeyError:
				pass
		return None
	
	def get_widget(self,o,*args,**kw):
		#print "get_widget(%s)" % repr(o)
		wcl = self.get_wcl(o.__class__)
		if wcl is None:
			msg = "really no widget for "+repr(o)
			#+" (bases = " + str([repr(b) for b in cl.__bases__])
			raise msg
		#print "--> found widget " + repr(wcl)
		return wcl(o,*args,**kw)

## def get_rowwidget(row):		
## 	cl = get_widget(row._ds._table.__class__)
## 	return cl(row)
		

