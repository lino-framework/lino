#coding: latin1
#---------------------------------------------------------------------
# $Id: server.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import os
from twisted.internet import reactor
# from twisted.internet.app import Application
# see http://gnosis.cx/publish/programming/twisted_1.html

from twisted.web import server
from twisted.web import static

from lino import copyright 
from widgets import Widget

from resources import MainResource, WidgetResource

def hostname():
	if os.name == 'nt':
		name= os.getenv('COMPUTERNAME')
	else:
		name = os.getenv('HOSTNAME')
	#'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'

	if name is None:
		name = 'localhost'
	return name

class ServerWidget(Widget):

	def writeLeftFooter(self):
		self.write("""
		<font size=1>
		This is a
		<a href="http://www.twistedmatrix.com/"
		target="_top">Twisted</a>
		<a href="http://lino.sourceforge.net"
		target="_top">Lino</a>
		server.
		Copyright 1999-2004 Luc Saffre.
		</font>
		""")
		
	def writeBody(self):
		body = "<ul>"
		for name,a in self.target.accounts.items():
			body += "<li>"
			body += '<a href="'+name+'/">' + name + " : " + a.getLabel()+'</a>'
			body += "</li>"
		body += "</ul>"
		self.write(body)
		
	

class WebServer:
	def __init__(self,homeDir,ui,wf,
					 hostName=None,
					 port=8080 ):
		self.homeDir =homeDir
		self.ui = ui
		self.widgetFactory = wf
		self.port = port
		if hostName is None:
			hostName = hostname()
		self.hostName = hostName
		self.accounts = {}

	def getLabel(self):
		return 'Lino Server on '+self.hostName

	def addDatabase(self, db, staticDirs={},**kw):
		self.ui.addDatabase(db)
		ctx = db.beginContext()
		rsc = MainResource(ctx, self.widgetFactory, **kw)
		self.addAccount(db.getName(),rsc,staticDirs)

	def addAccount(self,accountName,rsc,staticDirs={}):
		for (name,path) in staticDirs.items():
			#print name, path
			rsc.putChild(name, static.File(path))

		self.accounts[accountName] = rsc

	def run(self,showOutput=False):
	
		if self.ui.verbose:
			print "Lino Web Server" # version " + __version__
			print copyright(year='2004',author='Luc Saffre')
			print

		if len(self.accounts.keys()) != 1:
			root = WidgetResource(None, ServerWidget, self)
			staticDirs = {
				'files' : os.path.join(self.homeDir,'files')
				}
			for (name,path) in staticDirs.items():
				root.putChild(name, static.File(path))
			for (name,accnt) in self.accounts.items():
				#accnt.renderer.setupRenderer(self.baseuri+"/"+name)
				root.putChild(name,accnt)
		else:
			accnt = self.accounts.values()[0]
			#accnt.renderer.setupRenderer(self.baseuri+"/"+name)
			root = accnt

		site = server.Site(root)
		reactor.listenTCP(self.port, site)
		reactor.addSystemEventTrigger("before","shutdown",
												self.ui.shutdown)

		#if showOutput:
		#	webbrowser.open(self.baseuri,new=True)
			
		if self.ui.verbose:
			print "Serving on port %s." % self.port
			print "(Press Ctrl-C to stop serving)"
			
		reactor.run()
		

