import os

from xdocutils import publish

class WebManException(Exception):
	pass


class Node:
	def __init__(self, srcpath, parent ):
	
		self.parent = parent
		self.title = None
		self.abstract = None
		self.srcpath = srcpath # os.path.dirname(self.__module__.__file__)
		self.siteMap = None

	def setTitle(self,title):
		self.title = title

	def setAbstract(self,abstract):
		self.abstract = abstract

	def getSourcePath(self):
		return self.srcpath
	
	def getURL(self):
		(url,ext) = os.path.splitext(self.getSourcePath())
		return url + ".html"
	
class WebModule(Node):

	def __init__(self,
					 srcdir,
					 parent = None
					 ):

		"""
		`srcdir` : local directory 
		"""

		self.filerefBase = None
		self.filerefURL = None

		
		if parent is None:
			self.leftArea = None
			self.topArea = None
			self.bottomArea = None
			self.defaults = {
				'input_encoding': 'latin-1',
				'output_encoding': 'latin-1',
				'stylesheet_path': 'default.css',
				'embed_stylesheet': False,
				'source_link': 0,
				'tab_width': 3,
				'datestamp' : None, # '%Y-%m-%d %H:%M UTC',
				'generator': 0 
				}
		
		else:
			srcdir = os.path.join(parent.getSourcePath(),srcdir)
			# inherit from parent
			self.leftArea = parent.leftArea
			self.topArea = parent.topArea
			self.bottomArea = parent.bottomArea
			self.defaults = dict(parent.defaults)
			if parent.filerefBase is not None:
				self.filerefBase = os.path.join(parent.filerefBase,"..")
		
		srcdir = os.path.normpath(srcdir)
		srcdir = os.path.abspath(srcdir)
		if not os.path.isdir(srcdir):
			raise WebManException("%s is not a directory" % srcdir)
		Node.__init__(self,srcdir,parent)
		
		self.argv = ['--traceback']
		
		# private members:
		self._q_exports = ['default.css']
		self._pages = {}


		print "Loading WebMan module from %s..." % srcdir
		cwd = os.getcwd()
		os.chdir(srcdir)
		try:
			execfile(os.path.join(srcdir,"init.wmi"))
			for fn in os.listdir('.'):
				(name,ext) = os.path.splitext(fn)
				if ext == ".txt":
					self.addPage(name,TxtWebPage(self,name))
				elif os.path.isdir(fn):
					if os.path.exists(os.path.join(fn,'init.wmi')):
						if name != fn:
							raise WebManException("module names cannot contain '.'")
						self.addModule(name,fn)

		except IOError,e:
			raise WebManException("Missing init.wmi in %s" % srcdir)
		else:
			os.chdir(cwd)

		self._q_index = self.index
		
		# self._writer = Writer(self.leftArea)

	def setStyleSheet(self,name):
		self.defaults['stylesheet_path']=name

	def setFilerefBase(self,pth):
		self.filerefBase = pth
		
	def setFilerefURL(self,url):
		
		""" Set URL pattern for `fileref` roles `url` must be a string
		containing one '%s' which will be replaced by the fileref
		text. The result should be a valid URI.  """

		self.filerefURL = url
		
	def setLeftArea(self,f):
		self.leftArea = f
		
	def setBottomArea(self,f):
		self.bottomArea = f

	def getPages(self):
		return self._pages.values()

	def addPage(self,name,page):
		if self._pages.has_key(name):
			raise WebManException('Page %s already defined' % name)
		self._pages[name] = page
		self._q_exports.append(name)
		
	def addModule(self,name,srcdir):
		# assert not self._pages.has_key(name)
		m = WebModule(srcdir,parent=self)
		self.addPage(name,m)
		#self._pages[name] = m
		
		
## 	def leftArea(self,page=None):
## 		return """<a href="index.html">Home</a>
## 		<br>Hint:
## 		<br>set self.leftArea()!
## 		"""

	def __getattr__(self,name):
		try:
			return self._pages[name]
		except KeyError,e:
			raise AttributeError,name


	#def _q_access(self,request):
	#	pass
	
	def __call__(self,request):
		return self.index(request)

	def getURL(self):
		return self.index.getURL()
	
	
class TxtWebPage(Node):
	
	def __init__(self,mod,name):
		Node.__init__(self,
						  srcpath=os.path.join(mod.getSourcePath(),
													  name)+'.txt',
						  parent=mod)

	def getURL(self):
		(url,ext) = os.path.splitext(self.getSourcePath())
		return url + ".html"
		
	def __call__(self,request):
		# invoke docutils to read and parse the .txt source file
		# os.chdir() to 
		cwd = os.getcwd()
		os.chdir(self.parent.getSourcePath())
		r = publish(webmod=self.parent,
						source=self.getSourcePath())
		os.chdir(cwd)
		return r
	
