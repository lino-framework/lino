#coding: latin1
#---------------------------------------------------------------------
# $Id: $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

raise "no longer used"

from lino.adamo.html import HtmlRenderer, htmltext


## class TwistedRenderer(HtmlRenderer):
## 	defaultLangs = ('en,')

## 	def __init__(self,rsc,request):
## 		self.resource = rsc
## 		self.request = request
		
## 		if rsc.db is not None:
## 			self.defaultLangs = (rsc.db.getDefaultLanguage(),)
## 		self.langs = request.args.get('lng',self.defaultLangs)

## 		updirsToBase = len(self.request.prepath) \
## 							+ len(self.request.postpath) \
## 							-2
## 		self.baseuri = '../' * updirsToBase
		
## 		self._body = ''

## 	def formatLabel(self,label):
## 		p = label.find(self.resource.db.schema.HK_CHAR)
## 		if p != -1:
## 			label = label[:p] + '<u>' + label[p+1] + '</u>' + label[p+2:]
## 		return str(htmltext(label))

## 	def uriToTable(self,table):
## 		return self.baseuri + 'db/' + table.name
## 		#return self.request.prePathURL() + "/" + table.getName()

## 	def uriToRow(self,row):
## 		url = self.uriToTable(row._area._table)
## 		url += '/' + ','.join([str(v) for v in row.getRowId()])
## 		return url

## 	def uriToSkipper(self,skipper,**p):
## 		#p={}
## 		if skipper.pageLen != 15:
## 			p.setdefault('pl',skipper.pageLen)
## 		return self.uriToDatasource(skipper.ds,**p)
	
## 	def uriToDatasource(self,ds,**p):
## 		if ds._query.orderBy != None:
## 			p.setdefault('ob',ds._query.orderBy)
## 		if ds._query.search != None:
## 			p.setdefault('search', ds._query.search)
## 		if ds._query.filters != None:
## 			p.setdefault('flt',ds._query.filters)

## 		# todo : compare with query.setSamples(). Similar code
## 		atomicRow = [None] * len(ds._query.columnList._atoms)
## 		for (col,value) in ds._query.samples:
## 			col.rowAttr.value2atoms(value,atomicRow,col.getAtoms())
## 			l = []
## 			for atom in col.getAtoms():
## 				l.append( atomicRow[atom.index] )
## 			s = ','.join([str(v) for v in l])
## 			p[col.name] = s

		
## 		#for (atom,value) in ds._query.sampleColumns:
## 		#	p[atom.name] = value
			
## ## 		if ds._query.atomicSamples is not None:
## ## 			for (atom,value) in ds._query.atomicSamples:
## ## 				p[atom.name] = value

## 		#uri = self.baseuri + 'db/' + ds._query.leadTable.name
## 		uri = self.uriToTable(ds._query.leadTable)
## 		return self.buildURL(uri,p)

## 	def buildURL(self,url,flds):
## 		sep = "?"
## 		for (k,v) in flds.items():
## 			if issequence(v):
## 				for i in v:
## 					url += sep + k + "=" + str(i)
## 					sep = "&"
## 			elif v is not None:
## 				url += sep + k + "=" + str(v)
## 				sep = "&"
## 		return url
		
## 	def uriToSelf(self,*args,**options):
## 		flds = self.request.args.copy()
## 		for (k,v) in options.items():
## 			flds[k] = v
## 		url = self.request.prePathURL() 
		
## ## 		if len(self.request.postpath):
## ## 			url += "/" + "/".join(self.request.postpath)
## 		if len(args):
## 			url += "/" + "/".join([str(v) for v in args])
## 		return self.buildURL(url,flds)
	
## 	def refToSelf(self,label,**options):
## 		url = self.uriToSelf(**options)
## 		return '<a href="%s">%s</a>' % (url,label)

	
## 	def renderImage(self,src,tags=None,label=None):
## 		self.write(self.refToImage(src,tags,label))
					  
## 	def refToImage(self,src,tags=None,label=None):
## 		if label is None:
## 			label = src
## 		#print vars()
## 		src = self.baseuri+"images/"+src
## 		s = '<img src="%s" alt="%s"' % (src,htmltext(label))
## 		if tags is not None:
## 			s += tags
## 		s += ">"
## 		return s

## 	def renderMemo(self,txt):
## 		# memo2html
## 		self.resource.memo2html(self,txt)

	
## 	def getLabel(self):
## 		return self.main.getLabel()

## 	def write(self,s):
## 		#self.request.write(s)
## 		self._body += s

## 	def show(self,widget):
## 		self.writeWidget(widget)
## 		return self._body 
## 		#return server.NOT_DONE_YET
	
## 	def writeWidget(self,widget):
## 		assert isinstance(widget,Widget)
## 		title = htmltext(widget.getLabel())

## 		wr = self.write

## 		wr("""\
## 		<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
## 		"http://www.w3.org/TR/html4/loose.dtd">
## 		<html>
## 		<head>
## 		""")
## 		wr("<title>%s</title>" % title)
## 		if self.resource.stylesheet is not None:
## 			wr("""\
## 			<link rel=stylesheet type="text/css" href="%s">
## 			""" % (self.baseuri+self.resource.stylesheet))
## 		wr("""
## 		</head>
## 		<body>
## 		""")
## 		wr(self.BEFORE_LEFT_MARGIN)
## 		wr('''<a href="%s.">Home</a>''' % self.baseuri)
## 		if self.resource.db is not None:
## 			if len(self.resource.db._db.getBabelLangs()) > 1:
## 				wr('<p>')
## 				for lang in self.resource.db._db.getBabelLangs():
## 					if lang.id == self.langs[0]:
## 						wr(lang.id)
## 					else:
## 						self.renderLink(url=self.uriToSelf(lng=lang.id),
## 											 label=lang.id)
## 					wr(' ')
## 				wr('</p>')
					
## 		widget.asLeftMargin(self)
## 		wr(self.AFTER_LEFT_MARGIN)
## 		wr("""
## 		<table class="head">
## 		<tr>
## 		<td>
## 		""")
## 		widget.asPreTitle(self)
## 		wr('<p class="title">%s</p>' % title)
## 		wr("""
## 		</td>
## 		</tr>
## 		</table>
## 		""")

## 		widget.asBody(self)

## 		wr(self.BEFORE_FOOT)
## 		wr("""<td align="left" valign="center">""")
## 		self.writeLeftFooter()
## 		wr("</td>")
		
## 		wr(self.BETWEEN_FOOT)
## 		self.renderLink(url=self.uriToSelf())
## 		wr(self.AFTER_FOOT)



## 	def writeLeftFooter(self):
## 		self.write("""
## 		<font size=1>
## 		This is a
## 		<a href="http://www.twistedmatrix.com/"
## 		target="_top">Twisted</a> server.
## 		<A HREF="%scopyright">Copyright 1999-2004 Luc Saffre</A>.
## 		</font>
## 		""" % self.baseuri)
		

