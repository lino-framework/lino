#coding: latin1
#----------------------------------------------------------------------
# sitemap.py
# Copyright: (c) 2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import os
from nodes import WebModule, TxtWebPage, Node

class Site:
	def __init__(self,sourceRoot):
		self.menu = None
		sourceRoot = os.path.normpath(sourceRoot)
		sourceRoot = os.path.abspath(sourceRoot)
		self.sourceRoot = sourceRoot
		self.root = WebModule(self,"index",None)

	def init(self):
		self.menu = MenuItem(None,self.root)
		self.root.init()
	
	def addToSitemap(self,mod,menuText):
		menu = mod.menuItem
		#menu = self.menu.findItemFor(mod)
		if menu is None:
			menu = MenuItem(self.root,mod)
			#assert menu is not None, mod.getLocalPath()
			
		if menuText is None:
			for child in mod.getChildren():
				menu.addItem(child,0)
			return
		
		for line in menuText.splitlines():
			level = 0
			while line[level].isspace():
				level += 1
			nodeName = line[level:].strip()
			try:
				node = getattr(mod,nodeName)
			except AttributeError,e:
				#raise 
				node = OopsPage(mod,nodeName)
			#item = MenuItem(node,level)
			menu.addItem(node,level)
			



class MenuItem:
	def __init__(self,parent,node,level=-1):
		self.parent = parent
		self.node = node
		self.level = level
		self.items = []
		self.ancestors = []

		p = self.parent
		while p is not None:
			self.ancestors.insert(0,p)
			p = p.parent

		self.node.setMenuItem(self)
		

	def getNestingLevel(self):
		return len(self.ancestors)

		

	def addItem(self,node,level):
		if not node.isMenuItem: return
		if len(self.items) == 0 or level == self.items[-1].level:
			item = MenuItem(self,node,level)
			#item.parent = self
			self.items.append(item)
			return 
		if level > self.items[-1].level:
			self.items[-1].addItem(node,level)
			return 
		raise "%s : menu indentation error" % node.name
		 
	def findItemFor(self,node):
		if self.node == node:
			return self
		for item in self.items:
			i = item.findItemFor(node)
			if i is not None:
				return i
		
	def render_html(self,onItem,
						 expandChildren=True,
						 before="",
						 after=""):
		if self.level == -1:
			html = ""
		else:
			html = before
			html += "<br>" + "&nbsp;" * 2 * self.getNestingLevel()

		if onItem is not None:
			onNode = onItem.node
			if onNode.getURL(onNode) == self.node.getURL(onNode):
				html += self.node.getTitle()
				expandChildren = True
			else:
				html += """<a href="%s">%s</a>""" % (\
				 self.node.getURL(onNode), self.node.getTitle())
				if self.node in onNode.menuItem.ancestors:
					expandChildren = True
		if expandChildren:
			for item in self.items:
				html += item.render_html(onItem,expandChildren=False)

		html += after
		return html




class OopsPage(Node):

	def __init__(self,mod,name):
		Node.__init__(self,mod.site,name,mod)
	
	def writePageContent(self,response):
		response.write("oops")
