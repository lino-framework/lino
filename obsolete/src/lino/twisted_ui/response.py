#coding: latin1
#---------------------------------------------------------------------
# $Id: response.py $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

## class Response:
	

## 	def __init__(self,resource,request,context):
## 		self.resource = resource
## 		self.context = context
## 		self.request = request
		
## 		updirsToBase = len(self.request.prepath) \
## 							+ len(self.request.postpath) \
## 							-1
## 		self.baseuri = '../' * updirsToBase
		



## 	def refToSelf(self,label,**kw):
## 		url = self.uriToSelf(**kw)
## 		return '<a href="%s">%s</a>' % (url,label)

## 	#def uriToFile(self):
		

	
import types
from cStringIO import StringIO
from urllib import quote 

from twisted.web.html import escape

from lino.misc.etc import issequence

from lino import adamo
from lino.adamo.html import txt2html
from lino.adamo.rowattrs import Field, Pointer, Detail
#from lino.adamo.session import WebSession
from lino.adamo.widgets import Command


#from quixote.html import htmltext  # to be replaced by equivalent
def htmltext(s):
	s = escape(s)
	# s = s.replace('<','&lt;')
	# s = s.replace('>','&gt;')
	# s = s.replace('&','&amp;')
	return txt2html(s)


from lino.adamo.datatypes import MemoType, UrlType, EmailType, LogoType, ImageType


class HtmlResponse:
	
	CLEAR = "__CLEAR"
	showRowCount = True
	
	BEFORE_HEAD='''\
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
	<HTML>
	<HEAD>
	'''
	
	AFTER_HEAD='''
	<META HTTP-EQUIV="Content-Type"
	content="text/html;charset=latin-1" />
	</HEAD>
	<BODY>
	'''
	
	BEFORE_LEFT_MARGIN='''
	<table class="main"><tr>
	<td class="left" width="15%%">
	'''
	
	AFTER_LEFT_MARGIN='''
	</td>
	<td valign="top">
	'''

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
	</BODY>
	</HTML>
	"""
	
	def __init__(self,writer):
		if writer is None:
			self._writer = StringIO()
		else:
			assert hasattr(writer,"write")
			self._writer = writer


	def getStyleSheet(self):
		return None
	
	def onBeginResponse(self):
		pass

	def renderButton(self,url,label=None):
		if label is None:
			label="click!"
		return self.renderLink(url,'[%s]' % label)
	
	def renderLink(self,url,label=None):
		if label is None:
			label = url
		else:
			label = htmltext(label)
		self.renderFormattedLink(url,label)

	def renderFormattedLink(self,url,label):
		"label can contain tags and must be valid HTML"
		self.write('<a href="%s">%s</a>' % (url,label))

	def write(self,html):
		self._writer.write(html)

	def writeDebugMessage(self,msg):
		self.write('<font size="1" color="grey">')
		self.write(escape(msg))
		self.write('</font>')

	def writeDebugPanel(self):
		pass

## 	def refToSelf(self,label,*args,**options):
## 		raise NotImplementedError


	def buildURL(self,url,*args,**kw):
		if len(args):
			url += "/" + "/".join([str(v) for v in args])
		sep = "?"
		for (k,v) in kw.items():
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
		
	def writePage(self):
		raise NotImplementedError
	
	def writeBody(self):
		self.writePage()
		self.writePageBottom()

	def writeUserPanel(self):
		pass
	
	def writePageBottom(self):
		pass

	def writeLeftMargin(self):
		pass
	
	def writePreTitle(self):
		pass
		#self.write('preTitle')

	def writeLeftFooter(self):
		pass
	
	def getTitle(self):
		raise NotImplementedError
		
	def writeWholePage(self):
		#assert isinstance(widget,Widget)

		self.onBeginResponse()
		
		title = self.getTitle()

		wr = self.write

		wr(self.BEFORE_HEAD)
		wr("<title>%s</title>" % title)
		css = self.getStyleSheet()
		if css is not None:
			wr("""<link rel=stylesheet type="text/css" href="%s"/>
			""" % css)
		wr(self.AFTER_HEAD)
		wr(self.BEFORE_LEFT_MARGIN)
		self.writeUserPanel()
		self.writeLeftMargin()
		if True:
			self.writeDebugPanel()
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
		self.writeFooter()
		
	def writeFooter(self):
		wr = self.write
		wr("""<td align="left" valign="center">""")
		self.writeLeftFooter()
		wr("</td>")
		wr(self.BETWEEN_FOOT)
		self.writeRightFooter()
		wr(self.AFTER_FOOT)
		
	def writeRightFooter(self):
		self.renderButton(url=self.uriToSelf(),
								label="reload")


		
		
class TwistedResponse(HtmlResponse):
	
	def __init__(self,resource,request,writer):
		self.request = request
		self.resource = resource
		HtmlResponse(self,writer)


	def renderCellValue(self,col,value):
		if isinstance(col.rowAttr,Detail):
			r = self.child(value)
			r.writeParagraph()
		elif isinstance(col.rowAttr,Pointer):
			r = self.child(value)
			r.writeLabel()
		elif isinstance(col.rowAttr,Field):
			self.renderValue(value,col.rowAttr.type)
		else:
			self.write("<tt>"+htmltext(str(value))+"</tt>")

	def getStyleSheet(self):
		if self.resource.stylesheet is None:
			return None
		return self.fileURI(self.resource.stylesheet)
	
	def renderValue(self,value,type,size=(10,3)):

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

	def writeLabel(self):
		raise NotImplementedError
	
	def writeParagraph(self):
		self.writeLabel()

	def writeForm(self,labeledValues):
		wr = self.write
		wr('<table border="0" class="data">')
		for label,value in labeledValues:
			#if not name in ('abstract','body'):
			#value = getattr(row,attr.name)
			if value is not None:
				wr('\n<tr><td align="right">' + label + '</td>\n<td>')
				wr('\n<tr><td>' + value + '</td>\n<td>')
## 				if hasattr(value,'asFormCell'):
## 					value.asFormCell(renderer)
## 				else:
## 					type = getattr(attr,'type',None)
## 					renderer.renderValue(value,type)
				wr('</td>\n</tr>')

		wr('\n</table>')
		

	
	def homeURI(self,*args,**kw):
		inet, addr, port = self.request.getHost()
		if self.request.isSecure():
			default = 443
		else:
			default = 80
		if port == default:
			hostport = ''
		else:
			hostport = ':%d' % port
		uri = quote('http%s://%s%s' % (
			self.request.isSecure() and 's' or '',
			self.request.getRequestHostname(),
			hostport), "/:")
		return self.buildURL(uri,*args,**kw)

		

	def uriToSelf(self,**kw):
		
		d = self.request.args.copy()
		for (k,v) in kw.items():
			d[k] = v
			
		return self.buildURL(self.request.prePathURL(),
									*self.request.postpath,
									**d)

		
	def fileURI(self,*args):
		return self.homeURI("files",*args)
	
	def uriToImage(self,*args):
		return self.fileURI("images",*args)
	


	def formatLabel(self,label):
		return htmltext(label)


	def writeDebugPanel(self):
		wr = self.write
		wr("""<p><b>Debug panel:</b></p>""")
		wr("renderer: " + self.__class__.__name__)
		#wr("<br>baseuri="+self.response.baseuri)
		#wr("<br>prePathURL="+self.request.prePathURL())
		wr("<br>stylesheet="+self.resource.stylesheet+"<br>")
		
	def writeLeftFooter(self):
		self.write("""
		<font size=1>
		This site is hosted on a
		<a href="%s"
		target="_top">Twisted Lino Server</a>.
		Copyright 1999-2004 Luc Saffre.
		
		</font>
		""" % self.homeURI())




		

	
class ContextedResponse(TwistedResponse):

	def __init__(self,resource,request,target,writer):
		self.target = target
		self._context = target.getContext()
		assert self._context is not None
		TwistedResponse.__init__(self,resource,request,writer)


		
	def child(self,target):
		return target.getRenderer(self.resource,
										  self.request,
										  self._writer)
		
	def getTitle(self):
		return htmltext(self.target.getLabel())
	
	def contextURI(self,*args,**kw):
		return self.homeURI( self._context._db.getName(),
									*args,**kw)
	def fileURI(self,*args):
		return HtmlResponse.homeURI(self,
											 "files",
											  self._context._db.getName(),
											  *args)

	def uriToDatasource(self,ds,**p):
		for k,v in ds.get_GET().items():
			p.setdefault(k,v)
		return self.uriToTable(ds._table,**p)

	def uriToTable(self,table,**p):
		return self.contextURI( "db",
										table.getTableName(), **p)

		
	def uriToRow(self,row):
		url = self.uriToTable(row._ds._table)
		url += '/' + ','.join([str(v) for v in row.getRowId()])
		return url



	def formatLabel(self,label):
		p = label.find(self._context._db.schema.HK_CHAR)
		if p != -1:
			return htmltext(label[:p]) \
					  + '<u>' \
					  + htmltext(label[p+1]) \
					  + '</u>' \
					  + htmltext(label[p+2:])
		return htmltext(label)

	def renderPicture(self,src,tags=None,label=None):
		imageType = "pictures"
		src = src.replace('\\','/')
		pos = src.rfind('.')
		if pos == -1:
			raise "picture filename without extension"
		webSrc = src[:pos]+"_web"+src[pos:]
		self.write(
			'<a href="%s">' % self.uriToImage(imageType,src))
		if tags is None:
			tags = 'height="150"'
		else:
			if not ("width=" in tags or "height=" in tags):
				tags += 'height="150"'
		self.renderImage(imageType,webSrc,tags,label)
		self.write('</a>')
					  
	def renderImage(self,imageType,src,tags=None,label=None):
		src = self.uriToImage(imageType,src)
		self.write(self.refToImage(src,tags,label))
					  
	def refToImage(self,src,tags=None,label=None):
		if label is None:
			label = src
		s = '<img src="%s" alt="%s"' % (src,htmltext(label))
		if tags is not None:
			s += " "+tags
		s += ">"
		return s

	
	def renderMemo(self,txt):
		self._context.memo2html(self,txt)

	def renderForm(self,frm):
		for mnu in frm.getMenus():
			self.renderMenu(mnu)
		wr = self.write
		if len(frm):
			wr("""<p><form
			style="padding:5px;border:1px solid black;"
			action="%s"
			method="POST">
			""" % self.uriToSelf())

			for cell in frm:
				wr("\n")
				wr(cell.col.name)
				wr(": ")
				wr("""<input type="text" name="%s" value="%s">""" % \
					(cell.col.name,htmltext(cell.format())))
				wr("\n<br>")
			wr("""\n<input type="hidden" name="formName" value="%s">""" \
				% frm.getFormName())
			wr("""\n<input type="submit" value="OK">""")

			wr("</form></p>")
	
	def writeUserPanel(self):
		wr = self.write
		sess = self.getSession()
## 		frm = sess.getCurrentForm()
## 		if frm is not None:
## 			pass
## 		else:
## 			wr("""<p style="padding:5px;border:1px solid black;">""")
## 			wr("no form</p>")


	def renderMenu(self,mnu):
		wr = self.write
		wr('<p class="menu"><b>%s</b> :' % \
			self.formatLabel(mnu.getLabel()))

		for mi in mnu.getItems():
			wr('<br>')
			if isinstance(mi,Command):
				self.renderFormattedLink(self.uriToCommand(mi),
												 self.formatLabel(mi.getLabel()))
			else:
				wr(self.formatLabel(mi.getLabel()))
			
	def uriToCommand(self,a):
		l =[ a.getName() ]
		owner = a._owner
		while owner is not None:
			l.insert(0,owner.getName())
			owner = getattr(owner,'_owner',None)
		l.insert(0,"cmds")
		return self.contextURI(*l)
	
		
	def writeLeftMargin(self):
		wr = self.write
		wr('''<a href="%s">Home</a>''' % self.contextURI())
		wr('''<br><a href="%s">Menu</a>''' % self.contextURI("menu"))
	
