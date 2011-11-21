#coding: latin1
#---------------------------------------------------------------------
# $Id: skipper.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

#from response import ContextedResponse
#from lino.adamo.datasource import Datasource
#from lino.adamo.schema import LayoutComponent

#raise "Skipper muss noch angepasst werden, dass er den neuen Report nutzt. Siehe 20041007."

class Skipper:
	
	#handledClass = Datasource
	
	firstPageButton = '[<<]'
	lastPageButton = '[>>]'
	prevPageButton = '[<]'
	nextPageButton = '[>]'
	beginNavigator = '''
	<p class="nav">Navigator:
	'''
	endNavigator = "</p>"

	def onBeginResponse(self):
		pageLen = 15
		pageNum = None
		qryid = None
		tplid = 0
		forward = {}
		for k,v in self.request.args.items():
			assert len(v) == 1
			if k == 'pg':
				pageNum = int(v[0])
			elif k == 'pl':
				pageLen = int(v[0])
			elif k == 'tpl':
				tplid = int(v[0])
			elif k == 'qry':
				qryid = v[0]
			else:
				forward[k] = v
				
		self.ds = self.target#.query()
		self.ds.apply_GET(**forward)
		
		self.rpt = self.ds.report(pageNum=pageNum,pageLen=pageLen)
		self.tplid = tplid
		self.tpl = reportTemplates[tplid]
		#self.pageNum = pageNum
		#self.pageLen = pageLen
		
		# this is now also in Report
		# todo: use it there!
		#if self.pageLen is None:
		#	self.lastPage = 1
		#elif len(self.ds) == 0:
		#	self.lastPage = 1
		#else:
		#	self.lastPage = int((len(self.ds)-1) / self.pageLen) + 1
			#~ """
			#~ if pageLen is 10:
			#~ - [0..10] rows --> 1 page
			#~ - [11..20] rows --> 2 pages
			#~ - [21..30] rows --> 2 pages
			#~ - 10 rows --> 1 page
			#~ - 11 rows --> 2 pages
			#~ """

	def uriToSelf(self,**p):
		if self.rpt.pageNum != 1:
			p.setdefault('pg',self.rpt.pageNum)
		if self.rpt.pageLen != 15:
			p.setdefault('pl',self.rpt.pageLen)
		if self.tplid != 0:
			p.setdefault('tpl',self.tplid)
		return self.uriToDatasource(self.ds,**p)
	
	def writePreTitle(self):
		if self.rpt.pageLen == 1:
			url = self.uriToDatasource(self.ds)
			label = self.rpt.getLabel()
			self.renderLink(url,label)
		#renderer.write(self.ds.getSqlSelect())
	
	
	def writeBody(self):
		#self.asPreTitle(renderer)
		self.writePage()
		self.write(self.ds.getSqlSelect())
		#self.write("<br>samples:" + repr(self.ds._samples))
			
	def getLabel(self):
		if self.rpt.pageLen == 1:
			row = self.ds[self.rpt.pageNum-1]
			#row = self.ds.atoms2instance(atomicRow)
			return row.getLabel()
		return self.rpt.getLabel()

	def writeLabel(self):
		return self.renderLink(
			url=self.uriToSelf(),
			label=self.getLabel())

## 	def asParagraph(self,ds):
## 		widget = Skipper(ds,self.resource,self.request)
## 		widget.writeParagraph()
		
	def writeParagraph(self):
		previewLimit = 5
		wr = self.write
		#ds = renderer.resource.db.datasource(self._query)
		
		#if len(self.dh) > 0:
		uri = self.uriToDatasource(self.ds)
		n = len(self.ds)
		if n == 0:
			lbl = '(0 items)'
		else:
			l = [row.getLabel() \
				  for row in self.ds.iterate(limit=previewLimit)]
			lbl = ', '.join(l)
			if n > previewLimit:
				lbl += ' (... total %d items)' % n
		
		self.renderLink(uri,lbl)

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

 	def writePage(self):
		pageNum = self.rpt.pageNum
		# this is now also in Report
		# todo: use it there!
		if self.rpt.pageLen is None:
			limit = offset = None
			rowcount = 0
		else:
			if self.rpt.pageNum is None:
				self.pageNum=1
			elif self.pageNum < 0:
				self.pageNum = self.lastPage + self.pageNum - 1
			elif self.pageNum > self.lastPage:
				raise "pageNum > lastPage",self.lastPage
			rowcount = offset = self.pageLen * (self.pageNum-1) 
			limit = self.pageLen
		
		self.renderNavigator()
		
		if self.pageLen == 1:
			#row = self.ds[self.pageNum-1]
			row = self.rpt[0]
			self.child(row).writeBody()
		else:
			self.tpl.renderHeader(self)
			for row in self.rpt:
				rowcount += 1
				self.tpl.renderLine(self,rowcount,row)

			self.tpl.renderFooter(self)


	def renderNavigator(self):
		#rpt,ds,pageNum=None):
		rpt = self.rpt
		ds = self.ds
		pageNum = self.rpt.pageNum
		wr = self.write
		renderer = self
		
		
		#search = self.request.args.get('search',('',))[0]
		search = self.target._search
		if search is None:
			search = ""
		else:
			search = " OR ".join(search)
		uri = self.uriToSelf()
		wr("""\
		<form action="%(uri)s" method="GET" enctype="Mime-Type">
		Search: <input type="text" name="search" value="%(search)s">
		""" % vars())
		for k,v in self.request.args.items():
			if k != 'search':
				if v is not None:
					v = str(v[0])
					wr("""
					<input type="hidden" name="%s" value="%s">
					""" % (k,v))
		wr("""
		</form>		
		""" )
		if self.rpt.pageLen != 1:
			wr(" Format: ")
			self.renderLink(
				self.uriToSelf(tpl=0),
				label="[table]")
															
			wr(" ")
			renderer.renderLink(
				self.uriToSelf(tpl=1),
				label="[list]")
			if len(self.ds._table._views) > 0:
				wr(" View: ")
				lbl = "[full]"
				if self.ds._viewName is None:
					wr(lbl)
				else:
					self.renderLink(
						self.uriToSelf(v=self.CLEAR),
						label=lbl)
				for viewName in self.ds._table._views.keys():
					wr(" ")
					lbl = "[%s]"%viewName
					if self.ds._viewName == viewName:
						wr(lbl)
					else:
						renderer.renderLink(
							self.uriToSelf(v=viewName),
							label=lbl)
															
## 			body += " " + renderer.refToSelf(
## 												  label="[list]",
## 												  tpl=1)
			wr(" ")
		
		if True: # flup.lastPage > 1:
			wr(self.beginNavigator)
				
			if pageNum is None:
				pageNum = 1
			elif pageNum < 0:
				pageNum = self.rpt.lastPage + pageNum + 1
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
					self.uriToSelf(pg=1),
					label=self.firstPageButton)

				renderer.renderLink(
					self.uriToSelf(pg=pageNum-1),
					label=self.prevPageButton)

			wr(" [page %d of %d] " % (pageNum, self.lastPage))
				
			if pageNum == self.rpt.lastPage:
				wr(self.nextPageButton)
				wr(self.lastPageButton)
			else:
				renderer.renderLink(
					self.uriToSelf(pg=pageNum+1),
					label=self.nextPageButton)
				renderer.renderLink(
					self.uriToSelf(pg=self.rpt.lastPage),
					label=self.lastPageButton)
				
			wr(' (%d rows)' % len(ds))
			wr(self.endNavigator)

		

		
	#~ def isFirstPage(self):
		#~ #pageLen = self.getParam('pageLen') 
		#~ if self.pageLen is None:
			#~ return True
		#~ return (self.pageLen == 1)
	
	#~ def isLastPage(self):
		#~ #pageLen = self.getParam('pageLen') 
		#~ if self.pageLen is None:
			#~ return True
		#~ return self.pageNum
		#~ return len(self) > self.pageLen * self.pageNum

	#~ def lastPage(self):
		#~ #pageLen = rpt.getParam('pageLen') 
		#~ if self.pageLen is None:
			#~ return 1
		#~ return int(len(self) / self.pageLen) + 1

	


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
	
	def renderHeader(self,skipper):
		renderer = skipper
		rpt = skipper.rpt
		if skipper.pageLen == 1:
			return
		wr = renderer.write
		wr('<table border="0" class="data">\n')
		wr('<tr class="headerRow">\n')
		if renderer.showRowCount:
			wr("<td>#</td>")
		for col in rpt.getColumns():
			wr('<td>')
			renderer.renderLink(
				renderer.uriToSelf(ob=col.queryCol.name),
				label=col.getLabel())
			wr("</td>\n")
		wr('</tr>')
	
	def renderLine(self,skipper,rowcount,row):
		renderer = skipper
		rpt = skipper.rpt
		dh = skipper.ds
		wr = renderer.write
		
		if int(rowcount) == rowcount:
			wr('\n<tr class="evenDataRow">\n')
		else:
			wr('\n<tr class="oddDataRow">\n')

		if renderer.showRowCount:
			wr("<td>")
			renderer.renderLink(
				skipper.uriToSelf(pl=1,pg=rowcount),
				label=str(rowcount))
			wr("</td>")

		for cell in row:
			wr('<td>')
			value = cell.getValue()
			if value is not None:
				skipper.renderCellValue(cell.col,value)

			wr('</td>')
		wr('\n</tr>')

	def renderFooter(self,skipper):
		skipper.write('\n</table>')

class ListReportTemplate(ReportTemplate):
	
	def renderHeader(self,skipper):
		renderer = skipper
		#renderer.renderNavigator(flup)
		renderer.write('<ul>')
		
	def renderLine(self,skipper,rowcount, row):
		renderer = skipper
		#rpt = skipper.rpt
		#dh = skipper.ds
		# row = dh.atoms2instance(atomicRow)
		renderer.write('<li>')
		renderer.asParagraph(row)
		renderer.write('</li>')
		
	def renderFooter(self,skipper):
		skipper.write( '</ul>')
		

reportTemplates = (
	TableReportTemplate("Table"),
	ListReportTemplate("List"),
	)



