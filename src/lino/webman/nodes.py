import os

from xdocutils import publish

class WebManException(Exception):
	pass


class Site:
	def __init__(self,srcdir):
		self.menu = None
		localPath = os.path.normpath(srcdir)
		localPath = os.path.abspath(localPath)
		self.root = WebModule(self,"index",None,localPath)

	def init(self):
		self.menu = MenuItem(self.root)
		self.root.init()
	



class MenuItem:
	def __init__(self,node,level=-1):
		self.parent = None
		self.node = node
		self.level = level
		self.items = []

	def getNestingLevel(self):
		nl = 0
		p = self.parent
		while p is not None:
			nl += 1
			p = p.parent
		return nl
		

	def addItem(self,item):
		if len(self.items) == 0 or item.level == self.items[-1].level:
			self.items.append(item)
			item.parent = self
			return 
		if item.level > self.items[-1].level:
			self.items[-1].addItem(item)
			return 
		raise "%s : menu indentation error" % item.node.name
		 
	def findItem(self,node):
		if self.node == node:
			return self
		for item in self.items:
			i = item.findItem(node)
			if i is not None:
				return i
		
	def render_html(self,onPage,
						 before="",
						 after=""):
		if self.level == -1:
			html = ""
		else:
			html = before
			html += "<br>" + "&nbsp;" * 2 * self.getNestingLevel()
			if onPage.getURL(onPage) == self.node.getURL(onPage):
				html += self.node.getTitle()
			else:
				html += """<a href="%s">%s</a>""" % (\
				 self.node.getURL(onPage), self.node.getTitle())
				
		for item in self.items:
			html += item.render_html(onPage)

		html += after
		return html




class Node:
	def __init__(self, name, parent ):
	
		self.parent = parent
		self.title = None
		self.abstract = None
		self.name = name # os.path.dirname(self.__module__.__file__)
		#self.siteMap = None

	def setTitle(self,title):
		self.title = title

	def getTitle(self):
		return self.title

	def getChildren(self):
		return {}

	def setAbstract(self,abstract):
		self.abstract = abstract

	def getSourcePath(self):
		raise NotImplementedError
	
	def getModule(self):
		raise NotImplementedError

	def init(self):
		pass
	
	def render_html(self,request):
		# invoke docutils to read and parse the .txt source file
		return publish(self)
	
	def __str__(self):
		s = self.name
		p = self.parent
		while p is not None:
			s = p.name + "/"+s
			p = p.parent
		return s

	def getOutputFile(self):
		# this must return the filename
		# relative to self.getModule().getLocalPath()
		# raise NotImplementedError
		return self.name + ".html"
	
	def getURL(self,fromNode=None):
		if fromNode is None or fromNode.getModule() == self.getModule():
			return self.getOutputFile()
		fromBase = fromNode.getModule().getLocalPath().split(os.sep)
		toBase = self.getModule().getLocalPath().split(os.sep)
## 		print "%s -> %s : %s, %s" % ( str(fromNode),
## 												str(self),
## 												str(fromBase), str(toBase))
			
		while True:
			if len(fromBase) == 0: break
			if len(toBase) == 0: break
			if fromBase[0] == toBase[0]:
				del fromBase[0]
				del toBase[0]
			else:
				break
		url = ""
		for elem in fromBase:
			url += "../"
		for elem in toBase:
			url += elem + "/"
		return url + self.getOutputFile()

	
class WebModule(Node):

	def __init__(self, site, name, parent, localPath=None):
		self.site = site
		"""
		`localPath` : local directory 
		"""
		self.filerefBase = None
		self.filerefURL = None

		
		Node.__init__(self,name,parent)
		
		self.argv = ['--traceback']
		
		# private members:
		self._q_exports = ['default.css']
		self._nodes = {}

		if localPath is None:
			localPath = os.path.join(parent.getLocalPath(),name)
			
		if not os.path.isdir(localPath):
			raise WebManException("%s is not a directory" % localPath)
		self.localPath = localPath

		print "Loading WebMan module from %s..." % localPath
		# scan directory 

		for fn in os.listdir(self.localPath):
			(name,ext) = os.path.splitext(fn)
			if len(name) and name[0] != "_":
				if name != self.name:
					if ext == ".txt":
						self.addPage(name,TxtWebPage(self,name))
					elif os.path.isdir(fn):
						if name != fn:
							raise WebManException("module names cannot contain '.'")
						self.addModule(name,fn)

		#self._q_index = self
		self.title = self.name
		

	def init(self):

		if self.parent is None:
			#self.menu = None
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
			#self._oopsNode = None
		else:
			# inherit from parent
			parent = self.parent
			self.leftArea = parent.leftArea
			#self.menu = parent.menu
			self.topArea = parent.topArea
			self.bottomArea = parent.bottomArea
			self.defaults = dict(parent.defaults)
			#self.defaults['stylesheet_path'] = "../" + \
			#  self.defaults['stylesheet_path']
			#print "TODO: " + self.defaults['stylesheet_path']
			if parent.filerefBase is not None:
				self.filerefBase = os.path.join(parent.filerefBase,"..")
			#self._oopsNode = parent._oopsNode
		
		
		fn = os.path.join(self.localPath,'init.wmi')
		if os.path.exists(fn):
			cwd = os.getcwd()
			os.chdir(self.localPath)
			execfile(fn)
			os.chdir(cwd)

		for node in self._nodes.values():
			node.init()


	def setMenu(self,menuText):
		menu = self.site.menu.findItem(self)
		for line in menuText.splitlines():
			level = 0
			while line[level].isspace():
				level += 1
			nodeName = line[level:].strip()
			try:
				node = getattr(self,nodeName)
			except AttributeError,e:
				#raise 
				node = OopsPage(self,nodeName)
			item = MenuItem(node,level)
			menu.addItem(item)
			
		
	def getSourcePath(self):
		return os.path.join(self.getLocalPath(), self.name)+'.txt'
	
	def getModule(self):
		return self

	def getChildren(self):
		return self._nodes
	
	def getChild(self,name):
		return self._nodes[name]
	
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

	def getLocalPath(self):
		return self.localPath

	def getPages(self):
		return self._nodes.values()

	def addPage(self,name,page):
		if self._nodes.has_key(name):
			raise WebManException('Page %s already defined' % name)
		self._nodes[name] = page
		self._q_exports.append(name)
		
	def addModule(self,name,srcdir):
		# assert not self._nodes.has_key(name)
		m = WebModule(self.site,srcdir,parent=self)
		self.addPage(name,m)
		#self._pages[name] = m
		
		
## 	def leftArea(self,page=None):
## 		return """<a href="index.html">Home</a>
## 		<br>Hint:
## 		<br>set self.leftArea()!
## 		"""

	def __getattr__(self,name):
		try:
			return self._nodes[name]
		except KeyError,e:
			raise AttributeError,name


	#def getOutputFile(self):
	#	return os.path.join(self.name, self.name + ".html")
	
	#def _q_access(self,request):
	#	pass
	
	
class TxtWebPage(Node):
	"""
	TODO: self.title should be set by the docutils parser
	"""
	def __init__(self,mod,name,title=None):
		Node.__init__(self,name,parent=mod)
		if title is None:
			title = name
		self.title = title

	def getSourcePath(self):
		return os.path.join(self.parent.getLocalPath(), self.name)+'.txt'
	
## 	def getURL(self):
## 		(url,ext) = os.path.splitext(self.getSourcePath())
## 		return url + ".html"
		
	def getModule(self):
		return self.parent
	
	#def getOutputFile(self):
	#	return self.name + ".html"
	
	
class OopsPage(TxtWebPage):

	def __init__(self,mod,name):
		TxtWebPage.__init__(self,mod,'_oops',title=name)
	
