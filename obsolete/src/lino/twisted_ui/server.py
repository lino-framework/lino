#coding: latin1
#---------------------------------------------------------------------
# $Id: server.py,v 1.1 2004/07/31 07:23:37 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""
WebServer ist the main application class for a Twisted Lino Server.
"""

__TODO__ = """
convert WebServer to a real Twisted Application

"""

import os
import cgi

# from twisted.internet.app import Application
# see http://gnosis.cx/publish/programming/twisted_1.html

from twisted.web import static
from twisted.web.server import Request

from twisted.copyright import version
if version >= "1.2.0":
	from twisted.protocols.http import parse_qs
else:	
	from twisted.web.http import parse_qs




#from widgets import Widget
from response import HtmlResponse
from resources import AdamoResource		

#from resources import DbBrowser, TargetResource, MenuResource
from resources import DbResource

def hostname():
	if os.name == 'nt':
		name= os.getenv('COMPUTERNAME')
	else:
		name = os.getenv('HOSTNAME')
	#'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'

	if name is None:
		name = 'localhost'
	return name


## class WebServer:
	
## 	def __init__(self,
## 					 homeDir,ui,
## 					 hostName=None,
## 					 port=8080 ):
## 		self.homeDir =homeDir
## 		#self.widgetFactory = wf
## 		self.port = port
## 		if hostName is None:
## 			hostName = hostname()
## 		self.hostName = hostName
## 		#self._rendererClass = ServerResponse
## 		self._root = ServerResource(None,self)
## 		#self._root = TargetResource(None,self)




			

	
class ServerResource(AdamoResource):
	def __init__(self,homeDir,**kw):
		self.homeDir =homeDir
		#self.app = app
		self.accounts = []
		self.responderClass = ServerResponse
		AdamoResource.__init__(self,parent=None,
									  **kw)
		staticDirs = {
			#'files' : os.path.join(self.homeDir,'files')
			'files' : self.homeDir
			}
		for (name,path) in staticDirs.items():
			self.putChild(name, static.File(path))
		
	def getLabel(self):
		return 'Lino Server on '+self.hostName

	def getRenderer(self,resource,request,writer):
		return self.responderClass(self, resource, request, None)

	def findTarget(self):
		return self
	
	def addDatabase(self, db, staticDirs={},**kw):
		#self.app.addDatabase(db)
		#ctx = db.beginContext()
		rsc = DbResource(self,db, staticDirs, **kw)
		#rsc.putChild('db', DbBrowser(rsc,ctx))
		#rsc.putChild('menu', MenuResource(rsc,ctx))
		#self.addAccount(db.getName(),rsc,staticDirs)
## 		for (name,path) in staticDirs.items():
## 			#print name, path
## 			rsc.putChild(name, static.File(path))
		self.putChild(db.getName(),rsc)
		self.accounts.append(db)

	def render_GET(self,request):
		#renderer = TwistedRenderer(self,request)
		rsp = self.responderClass(self, request, None)
		return self.letRespond(rsp)
		#resp = Response(self,request)
		#self._row.asPage(resp)


class ServerResponse(HtmlResponse):
	#handledClass = WebServer

	def getTitle(self):
		pass
	
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
		srv = self.resource
		wr = self.write
		wr("<ul>")
		for a in srv.accounts:
			wr("<li>")
			self.renderLink(url=a.getName())
			wr(" : " + a.getLabel())
			wr("</li>")
		wr("</ul>")


class MyRequest(Request):
	
	def requestReceived(self, command, path, version):
		"""
		twisted.web.http.Request.requestReceived() merges POST and
		GET arguments into self.args but Lino wants to have them
		separately."""
		
		self.content.seek(0,0)
		self.args = {}
		self.postdata = {}
		self.stack = []

		self.method, self.uri = command, path
		self.clientproto = version
		x = self.uri.split('?')

		if len(x) == 1:
			self.path = self.uri
		else:
			if len(x) != 2:
				log.msg("May ignore parts of this invalid URI: %s"
						  % repr(self.uri))
			self.path, argstring = x[0], x[1]
			self.args = parse_qs(argstring, 1)

		# cache the client and server information, we'll need this later to be
		# serialized and sent with the request so CGIs will work remotely
		self.client = self.channel.transport.getPeer()
		self.host = self.channel.transport.getHost()

		# Argument processing
		# store POST data to self.postdata instead of self.args
		args = self.postdata
		ctype = self.getHeader('content-type')
		if self.method == "POST" and ctype:
			mfd = 'multipart/form-data'
			key, pdict = cgi.parse_header(ctype)
			if key == 'application/x-www-form-urlencoded':
				args.update(parse_qs(self.content.read(), 1))
			elif key == mfd:
				try:
					args.update(cgi.parse_multipart(self.content, pdict))
				except KeyError, e:
					if e.args[0] == 'content-disposition':
						# Parse_multipart can't cope with missing
						# content-dispostion headers in multipart/form-data
						# parts, so we catch the exception and tell the client
						# it was a bad request.
						self.channel.transport.write(
							"HTTP/1.1 400 Bad Request\r\n\r\n")
						self.channel.transport.loseConnection()
						return
					raise
			else:
				pass

		self.process()
 
