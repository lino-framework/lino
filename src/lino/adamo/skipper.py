#coding: latin1
#---------------------------------------------------------------------
# $Id: skipper.py,v 1.6 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

raise "no longer used. replaced by tls package"

from widgets import Widget
from datasource import Datasource


class Skipper(Widget):
	
	firstPageButton = '[<<]'
	lastPageButton = '[>>]'
	prevPageButton = '[<]'
	nextPageButton = '[>]'
	beginNavigator = '''
	<p class="nav">Navigator:
	'''
	endNavigator = "</p>"

	def __init__(self,area,request):
		self.request = request
		csvSamples = {}
		qryParams = {}
		pageLen = 15
		pageNum = None
		qryid = None
		tplid = 0
		for k,v in request.args.items():
			assert len(v) == 1
			if k == 'pg':
				pageNum = int(v[0])
			elif k == 'pl':
				pageLen = int(v[0])
			elif k == 'tpl':
				tplid = int(v[0])
			elif k == 'qry':
				qryid = v[0]
			elif k == 'ob':
				qryParams['orderBy'] = " ".join(v)
			#elif k == 'col':
			#	p['columnList'] = " ".join(v)
			elif k == 'search':
				qryParams['search'] = v[0]
			elif k == 'flt':
				qryParams['filters'] = (v[0],)
				#qryParams['filters'] = tuple(l)

			else:
				csvSamples[k] = v[0]
				#qryParams['atomicSamples'][k] = v[0]
				#qryParams['samples'][k] = v[0]
				#p[k] = self.area.cellAtoms2Value(k,v)


		qry = area._table.query(name=qryid, **qryParams)
		self.rpt = qry.report(None)

		ds = Datasource(area,qry)
		ds.setCsvSamples(**csvSamples)
			
		
		self.ds = ds
		#self.area = area
		#self.rpt = ds._query.report(None)
		#self.query = qry
		self.tpl = reportTemplates[tplid]
		#self.ds = Datasource(area,qry)
		self.pageNum = pageNum
		self.pageLen = pageLen
		
		if self.pageLen is None:
			self.lastPage = 1
		elif len(self.ds) == 0:
			self.lastPage = 1
		else:
			#rowcount = len(self)
			#rowcount = self.area._connection.executeCount(
			#	self.query,**kw)
				
			#rowCount = self.executeCount
			#rowCount = area._connection.executeCount(self.query)
			self.lastPage = int((len(self.ds)-1) / self.pageLen) + 1
			"""
			if pageLen is 10:
			- [0..10] rows --> 1 page
			- [11..20] rows --> 2 pages
			- [21..30] rows --> 2 pages
			- 10 rows --> 1 page
			- 11 rows --> 2 pages
			"""

			
## 	def __init__(self,ds,tplid=0,pageNum=None,pageLen=None):
## 		#self.area = area
## 		self.rpt = ds._query.report(None)
## 		#self.query = qry
## 		self.tpl = reportTemplates[tplid]
## 		self.ds = ds
## 		#self.ds = Datasource(area,qry)
## 		self.pageNum = pageNum
## 		self.pageLen = pageLen
		
## 		if self.pageLen is None:
## 			self.lastPage = 1
## 		elif len(self.ds) == 0:
## 			self.lastPage = 1
## 		else:
## 			#rowcount = len(self)
## 			#rowcount = self.area._connection.executeCount(
## 			#	self.query,**kw)
				
## 			#rowCount = self.executeCount
## 			#rowCount = area._connection.executeCount(self.query)
## 			self.lastPage = int((len(self.ds)-1) / self.pageLen) + 1
## 			"""
## 			if pageLen is 10:
## 			- [0..10] rows --> 1 page
## 			- [11..20] rows --> 2 pages
## 			- [21..30] rows --> 2 pages
## 			- 10 rows --> 1 page
## 			- 11 rows --> 2 pages
## 			"""
			
	def asPreTitle(self,renderer):
		if self.pageLen == 1:
			url = renderer.uriToDatasource(self.ds)
			label = self.rpt.getLabel()
			renderer.renderLink(url,label)
		#renderer.write(self.ds.getSqlSelect())
	
	
	def asBody(self,renderer):
		#self.asPreTitle(renderer)
		self.asPage(renderer)
		renderer.write(self.ds.getSqlSelect())
			
	def getLabel(self):
		if self.pageLen == 1:
			atomicRow = self.ds[self.pageNum-1]
			row = self.ds.atoms2instance(atomicRow)
			return row.getLabel()
		return self.rpt.getLabel()

	def asLabel(self,renderer):
		return renderer.renderLink(
			url=renderer.uriToSkipper(self),
			label=self.getLabel())

	def asLeftMargin(self,renderer):
		self.ds._area._db.asLeftMargin(renderer)
	
	def asParagraph(self,renderer):
		self.ds.asParagraph(renderer)
## 		previewLimit = 10
## 		wr = renderer.write
## 		#ds = renderer.resource.db.datasource(self._query)
		
## 		#if len(self.dh) > 0:
## 		n = len(self)
## 		if n == 0:
## 			wr(self.getLabel() + " (empty)")
## 		else:
## 			self.asLabel(renderer)
## 			sep = ' : '
## 			for row in self.ds.instances(limit=previewLimit):
## 				wr(sep)
## 				row.asLabel(renderer)
## 				sep = ','
## 			if n > previewLimit:
## 				wr(' (... total %d items)' % n)

 	def asPage(self,renderer):
			
		pageNum = self.pageNum
		
		if self.pageLen is None:
			limit = offset = None
			rowcount = 0
		else:
			if self.pageNum is None:
				self.pageNum=1
			elif self.pageNum < 0:
				self.pageNum = self.lastPage + self.pageNum - 1
			elif self.pageNum > self.lastPage:
				raise "pageNum > lastPage",self.lastPage
			rowcount = offset = self.pageLen*(self.pageNum-1) 
			limit = self.pageLen
		
		self.renderNavigator(renderer)
		
		self.tpl.renderHeader(renderer,self)
		
		for atomicRow in self.ds.execute(offset=offset,limit=limit):
			rowcount += 1
			self.tpl.renderLine(renderer,self,rowcount,atomicRow)

		self.tpl.renderFooter(renderer,self)


	def renderNavigator(self,renderer):
		#rpt,ds,pageNum=None):
		rpt = self.rpt
		ds = self.ds
		pageNum = self.pageNum
		wr = renderer.write
		
		
		search = renderer.request.args.get('search',('',))[0]
		uri = renderer.uriToSelf()
		wr("""\
		<form action="%(uri)s" method="GET" enctype="Mime-Type">
		Search: <input type="text" name="search" value="%(search)s">
		</form>		
		""" % vars())
		#uri = renderer.uriToSkipper(self)
		if self.pageLen != 1:
			wr(" Format: ")
			renderer.renderLink(
				renderer.uriToSkipper(self,tpl=0),
				label="[table]")
															
			wr(" ")
			renderer.renderLink(
				renderer.uriToSkipper(self,tpl=1),
				label="[list]")
															
## 			body += " " + renderer.refToSelf(
## 												  label="[list]",
## 												  tpl=1)
			wr(" ")
		
		if True: # flup.lastPage > 1:
			wr(self.beginNavigator)
				
			if pageNum is None:
				pageNum = 1
			elif pageNum < 0:
				pageNum = self.lastPage + pageNum + 1
				# pg=-1 --> lastPage
				# pg=-2 --> lastPage-1
				
			if pageNum == 1:
				wr(self.firstPageButton)
				wr(self.prevPageButton)
			else:
## 				body += '<a href="%s">%s</a>' % (
## 					self.uriToSelf(request, pg = 1),
## 					self.firstPageButton)
				renderer.renderLink(
					renderer.uriToSkipper(self,pg=1),
					label=self.firstPageButton)

				renderer.renderLink(
					renderer.uriToSkipper(self,pg=pageNum-1),
					label=self.prevPageButton)

			wr(" [page %d of %d] " % (pageNum, self.lastPage))
				
			if pageNum == self.lastPage:
				wr(self.nextPageButton)
				wr(self.lastPageButton)
			else:
				renderer.renderLink(
					renderer.uriToSkipper(self,pg=pageNum+1),
					label=self.nextPageButton)
				renderer.renderLink(
					renderer.uriToSkipper(self,pg=self.lastPage),
					label=self.lastPageButton)
				
			wr(' (%d rows)' % len(ds))
			wr(self.endNavigator)

		

		
	def isFirstPage(self):
		#pageLen = self.getParam('pageLen') 
		if self.pageLen is None:
			return True
		return (self.pageLen == 1)
	
	def isLastPage(self):
		#pageLen = self.getParam('pageLen') 
		if self.pageLen is None:
			return True
		return self.pageNum
		return len(self) > self.pageLen * self.pageNum

	def lastPage(self):
		#pageLen = rpt.getParam('pageLen') 
		if self.pageLen is None:
			return 1
		return int(len(self) / self.pageLen) + 1

	


## class Skipper:

##    # _query = None

##    def __init__(self, values,
##                 new=False,
##                 locked=False):
##       assert self.__class__.__dict__['_table'] is not None
##       assert len(values) == len(self._table._comps)
## ##       values = tuple(len(self._cursor.columns))
## ##       for i in range(len(args)):
## ##          values[i] = args[i]
## ##       for (k,v) in keywords.items():
## ##          i = self._cursor.findColIndex(k)
## ##          values[i] = v
##       self.__dict__["_values"] = values 
##       self.__dict__["_dirty"] = False
##       self.__dict__["_new"] = new
##       self.__dict__["_locked"] = locked
##       #self.__dict__["_uncomplete"] = uncomplete
##       #self.__dict__["_table"] = table

##    def setDirty(self,dirty=True):
##       self.__dict__["_dirty"] = dirty

##    def isDirty(self):
##       return self._dirty
   
## ##    def SetNew(self,new):
## ##       self.__dict__["_new"] = new

## ##    def IsNew(self):
## ##       return self._new

##    def skip(self,n=1):
##       pass
         
##    def __getattr__(self,name):
##       try:
##          i = self.__class__.__dict__['_query'].findColIndex(name)
##          return self.__dict__["_values"][i]
##          #return self._values[name]
##       except KeyError,e:
##          s = "%s row has no attribute '%s'" % (self.__class__.__name__,
##                                                name)
##          raise AttributeError,s
   
##    def __setattr__(self,name,value):
##       i = self._query.findColIndex(name)

##       if value is not None:
##          comp = self._query.leadTable.FindComponent(name)
##          if isinstance(comp,Field):
##             pass
##          elif isinstance(comp,Join):
##             if not isinstance(value,WritableRow):
##                raise "cannot assign %s to column %s" % \
##                      ( repr(value), name )
##          elif isinstance(comp,Detail):
##             if not isinstance(value,Cursor):
##                raise "cannot assign %s to column %s" % \
##                      ( repr(value), name )
      
      
##       #self.__dict__["_values"][name] = comp.assign(value)
##       self.__dict__["_values"][i] = value
##       self.__dict__["_dirty"] = True
##       #self.SetDirty()

##    def __repr__(self):
##       if True: # hide None values
##          s = ""
##          sep = ""
##          i = 0
##          for v in self.__dict__["_values"]:
##             if v is not None:
##                s += sep + "%s=%s" % (self._query.columnList[i],
##                                      repr(v))
##                sep = ", "
##             i += 1
               
##          return "row %s" % s #self.__dict__["_values"]
##       # show all values, including None
##       return "row %s" % repr(self.__dict__["_values"])
   



class ReportTemplate:
	
	def __init__(self,label):
		self.label= label

class TableReportTemplate(ReportTemplate):
	
	def renderHeader(self,renderer,skipper):
		rpt = skipper.rpt
		if skipper.pageLen == 1:
			return
		wr = renderer.write
		wr('<table border="0" class="data">\n')
		wr('<tr class="headerRow">\n')
		if renderer.showRowCount:
			wr("<td>#</td>")
		for col in rpt.getColumns():
			#print col.queryCol.name
			#~ a = Action( func=grid.setOrderBy, args=(col.name,))
			#~ ra = self.addAction(a)
			wr('<td>')
			renderer.renderLink(
				renderer.uriToSkipper(skipper,
											 ob=col.queryCol.name),
				label=col.getLabel())
			#~ self.wr(self.formatLink(label=col.getLabel(), action=ra))
			wr("</td>\n")
		wr('</tr>')
	
	def renderLine(self,renderer,skipper,rowcount,atomicRow):
		rpt = skipper.rpt
		dh = skipper.ds
		row = dh.atoms2instance(atomicRow)
		if skipper.pageLen == 1:
			return row.asBody(renderer)
		
		wr = renderer.write
		if int(rowcount) == rowcount:
			wr('\n<tr class="evenDataRow">\n')
		else:
			wr('\n<tr class="oddDataRow">\n')

		if renderer.showRowCount:
			wr("<td>")
			renderer.renderLink(
				renderer.uriToSkipper(skipper,pl=1,pg=rowcount),
				label=str(rowcount))
			wr("</td>")

		i = 0
		for col in rpt.getColumns():
			wr('<td>')
			# value = col.atoms2value(atomicRow)
			# value = values[i]
			attr = col.queryCol.rowAttr
			value = attr.getValueFromRow(row)
			if value is not None:
				attr.asFormCell(renderer,value,(col.preferredWidth,
														  rpt.rowHeight))
## 			if hasattr(value,'asParagraph'):
## 				value.asParagraph(renderer)
## 			else:
## 				type= getattr(attr,'type',None)
## 				renderer.renderValue(value,type)
			i += 1

			wr('</td>')
		wr('\n</tr>')
		#return body

	def renderFooter(self,renderer,skipper):
		renderer.write('\n</table>')

class ListReportTemplate(ReportTemplate):
	
	def renderHeader(self,renderer,skipper):
		#renderer.renderNavigator(flup)
		renderer.write('<ul>')
		
	def renderLine(self,renderer,skipper,rowcount, atomicRow):
		rpt = skipper.rpt
		dh = skipper.ds
		row = dh.atoms2instance(atomicRow)
		renderer.write('<li>')
		row.asParagraph(renderer)
		renderer.write('</li>')
		
	def renderFooter(self,renderer,skipper):
		renderer.write( '</ul>')
		

reportTemplates = (
	TableReportTemplate("Table"),
	ListReportTemplate("List"),
	)



