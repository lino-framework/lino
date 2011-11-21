"""\
Usage : db2html [options] FILE

DOES NOT WORK.

Publish an Adamo database as static html

Options:
  
  -o DIR, --output         DIR where generated files are to be placed
                           (default is ./public_html)
  -b, --batch              don't start a browser 
  -h, --help               display this text
"""

import sys, getopt, os
import webbrowser

from lino import copyleft

from lino.adamo.dbds.sqlite_dbd import Connection
from lino.adamo.ui import UI
from lino.schemas.sprl.sprl import Schema
#from lino.adamo.widgets import Window


#from lino.adamo.html import HtmlRenderer

class StaticRequest:
	def __init__(self,baseuri,reqpath):
		#self.path = baseuri + '/' + reqpath
		self.uri = baseuri + '/' + reqpath
		self.basepath = '.'
		for p in reqpath.split('/'):
			self.basepath += './.'

class StaticHtmlRenderer: #(HtmlRenderer,Window):
	
	def __init__(self,db,localBasepath,baseuri):
		#Window.__init__(self)
		#HtmlRenderer.__init__(self,db,baseuri)
		self.db.schema.defineMenus(self)
		self.localBasepath = localBasepath
		
	def writeRowPage(self, row, reqpath):
		request = StaticRequest(self.baseuri,reqpath)
		# self.filename = filename
		body = self.renderForm(request,row,None)
		html = self.wholepage(
			request,
			basepath=request.basepath,
			title=row.getLabel(),
			body=body,
			leftMargin=self.getLeftMargin(request))
		
		l = reqpath.split('/')
		filename = os.path.join(self.localBasepath,*l)
		filename += ".html"

		if os.path.exists(filename):
			raise "PilatusProblem : file %s already exists" % filename
		
		(head,tail) = os.path.split(filename)
		if not os.path.exists(head):
			os.makedirs(head)
			
		file(filename,'w').write(html)
	
	def showReport(self,rpt,**kw):
		raise NotImplementedError

	def showForm(self,rpt,**kw):
		raise NotImplementedError

	def setMainMenu(self,evt,name):
		raise NotImplementedError

	def showAbout(self,evt,id,**kw):
		raise AbstractError,self.__class__
	
	def test_decide(self,evt,id,**kw):
		raise AbstractError,self.__class__
	
	def showWindow(self,evt,id,**kw):
		raise NotImplementedError

	def exit(self,evt):
		raise NotImplementedError
	

	def getLeftMargin(self,request):
		s = ''
		for name,mb in self.getMenuBars().items():
			s += self.renderMenuBar(request,mb)
		return s
	
	def renderAction(self,mi,request):
		if mi.method == self.showReport:
			rpt = mi.args[0]
## 			url = "/"
## 			for p in request.prepath:
## 				if len(p) > 0:
## 					url += p + "/"
			url = self.tableUrl(rpt.leadTable)
			#url = self.basepath + "/" + rpt.leadTable.getName() + "/"
			if rpt.getName() is not None:
				url += "?view=" + rpt.getName()
			#if hasattr(mi.target,"getName"):
			return ' [%s] ' % self.renderLink(\
				url, self.formatLabel(mi.getLabel()))
		else:
			return " [%s] " % self.formatLabel(mi.getLabel())

	def tableUrl(self,table):
		return self.baseuri + "/" + table.getName()

	def rowUrl(self,row):
		url = self.tableUrl(row._area._table) + "/"
		url += ",".join([str(v) for v in row.getRowId()])
		return url


	def urlToSelf(self,request,label,**options):
		# path = self.request().servletURI()
		url = request.uri
		#url = self.baseuri + request.path
		return '<a href="%s">%s</a>' % (url,self.formatLabel(label))
	


def db2html(db,localBasepath,baseuri):
	r = StaticHtmlRenderer(db,localBasepath,baseuri)
	for page in db.PAGES.query():
		if page.match:
			fn = page.match
		else:
			fn = str(page.id)
		r.writeRowPage(page,fn)
		
	for page in db.NEWS.query():
		r.writeRowPage(page,'news/'+str(page.id))
		
	


if __name__ == '__main__':
	print "Lino db2html" # version " + __version__
	print copyleft(year='2004',author='Luc Saffre')

	localBasepath = 'public_html'
	baseuri = "http://my.tele2.ee/lsaffre"
	showOutput = True

	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"?ho:b",
											["help", "output=","batch"])

	except getopt.GetoptError,e:
		print __doc__
		print e
		sys.exit(-1)

	if len(args) != 1:
		print __doc__
		sys.exit(-1)

	
	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		elif o in ("-o", "--output"):
			localBasepath = a
		elif o in ("-b", "--batch"):
			showOutput = False

	dbfile = args[0]

	ui = UI(verbose=True)
	schema = Schema()
	schema.startup(ui)
	
	conn = Connection(dbfile) #, isTemporary=True)
	
	db = ui.addDatabase(None,
							  conn,schema,
							  label="Lino Demo Database")
	
	db2html(db,localBasepath,baseuri)
	
	url = os.path.join(localBasepath,'index.html')
	if showOutput:
		webbrowser.open(url,new=True)
	
