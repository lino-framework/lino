# A Web Application

import os, urllib, copy, cStringIO
import time, random, sha, sys, random
import SimpleHTTPServer
import snakelet
from threading import Lock
from YpageEngine import YpageEngine
from ypage.compiler import CompilerError

class NotHandled(Exception):
	pass


class WebAppContext:
	# storage container for the web app context.
	def __init__(self, webapp):
		# initialize initial context values.
		self.AbsPath=webapp.getFileSystemPath()
		self.Name=webapp.getName()
		self.UrlPrefix=webapp.getURLprefix()


class WebApp:
	def __init__(self,abspath, shortname, name, urlprefix, docroot, snakelets, sessionTimeoutSecs, configdict, dirlistallower, start, server):
		self.configitems=configdict
		self.absFSpath=abspath
		self.docrootFSPath=os.path.normpath(os.path.join(self.absFSpath,docroot))
		self.name=(shortname,name)
		self.urlprefix=urlprefix
		self.snakelets=snakelets
		self.sessionTimeoutSecs=sessionTimeoutSecs
		self.server=server
		self.dirListAllower=dirlistallower
		self.start=self.urlprefix+start
		self.enabled=1
		# create a context for this web application.
		self.context=WebAppContext(self)
		# initialize snakelets
		for snk in self.snakelets:
			snakeletClass = self.snakelets[snk]
			if isinstance(snakeletClass, snakelet.Snakelet):
				# it already is an instance (webapps haven't been
				# properly unloaded); grab the class from it.
				snakeletClass=snakeletClass.__class__
			# instantiate the snakelet class
			self.snakelets[snk]=snakeletClass(snk,self)
			
		# session tracking
		self.sessions={}
		self.lock = Lock()	# thread lock for session management
		self.pageEngine=YpageEngine(shortname,
                                            server.serverRoot)

	def __str__(self):
		return "[WebApp '"+self.getName()[1]+"' urlprefix="+self.getURLprefix()+"]"

	def getFileSystemPath(self):
		return self.absFSpath
	def getDocRootPath(self):
		return self.docrootFSPath
	def getName(self):
		return self.name
	def isEnabled(self):
		return self.enabled
	def setEnabled(self, enabled):
		self.enabled=enabled
			
	def getContext(self):
		return self.context
	def getURLprefix(self):
		return self.urlprefix
	def getConfigItems(self):
		return self.configitems
	def getConfigItem(self, item):
		return self.configitems[item]
	def getSnakelets(self):
		return self.snakelets
	def getStartLocation(self):
		return self.start
		
	def _getPath(self, handlerpath):
		return handlerpath[len(self.getURLprefix()):]

	def do_HEAD(self, handler):
		path=self._getPath(handler.path)
		result=self.is_snakelet(path)
		if result:
			handler.send_response(200,"OK")
			handler.send_header("Pragma","No-cache")		# no caching of snakelets...
			handler.send_header("Cache-Control","No-cache")
			handler.send_header("Expires","-1")
			handler.end_headers()
			return None
		result=self.is_Ypage(path)
		if result:
			handler.send_response(200,"OK")
			handler.send_header("Pragma","No-cache")		# no caching of ypages...
			handler.send_header("Cache-Control","No-cache")
			handler.send_header("Expires","-1")
			handler.end_headers()
			return None
		raise NotHandled()

	def do_GET(self, handler, passtroughRequest, passtroughResponse):
		path=self._getPath(handler.path)
		result=self.is_snakelet(path)
		if result:
			self.run_snakelet(handler,result[0],result[1], passtroughRequest, passtroughResponse)
			return None
		result=self.is_Ypage(path)
		if result:
			return self.run_Ypage_GET(handler,result[0],result[1], passtroughRequest, passtroughResponse)
		raise NotHandled()

	def do_POST(self, handler):
		# this works without the passtroughRequest/response,
		# because a POST is never used for inclusion/redirection.
		path=self._getPath(handler.path)
		result = self.is_snakelet(path)
		if result:
			return self.run_snakelet(handler,result[0],result[1])
		result = self.is_Ypage(path)
		if result:
			return self.run_Ypage_POST(handler,result[0],result[1])
		else:
			handler.send_error(501, "Can only POST to scripts (not static pages), or your POST url is invalid.")

	def is_snakelet(self,path):
		# Test whether path corresponds to a snakelet.
		# Return a tuple (dir, rest) if path requires running a snakelet, None if not.
		# NOTE: checking algorithm is not optimized; linear scan of snakelet list...
		for snake in self.snakelets:
			i=len(snake)
			(url,args) = (path[:i], path[i:])
			if url == snake and (not args or args[0] in ('?','/')):
				return (url,urllib.unquote_plus(args))
		return None

	def is_Ypage(self,path):
		# Test whether path corresponds to an Ypage.
		# Return a tuple (dir, rest) if path requires running an Ypage, None if not.
		suffix=".y"
		if path.endswith(suffix) or path.find(suffix+'?')>=0:
			i=path.index(suffix)+len(suffix)
			return (path[:i], urllib.unquote_plus(path[i:]))
		else:
			return None

	def allowDirListing(self, path):
		# allow directory listing of this path??
		if self.dirListAllower:
			# use relative path
			return self.dirListAllower(self._getPath(path))
		return 0 #default: not allowed

	def run_snakelet(self, handler, context, query, passtroughRequest=None, passtroughResponse=None):
		# find the path info (if query starts with /, upto end of string or ?)
		i = query.rfind('?')
		if i >= 0:
			pathinfo, query = query[:i], query[i+1:]
		else:
			pathinfo, query = query, ""

		snake = self.snakelets[context]
		
		try:
			if passtroughRequest:
				# we were called as a result of forwarding or including in another request
				req=passtroughRequest
				# By design, the new query args are NOT PARSED,
				# so DO NOT DO THIS: req._init_query(pathinfo,query)
			else:
				req = snakelet.Request(self,pathinfo, query, handler, handler.rfile);

			# run the snakelet with a Request and Response object
			resp=passtroughResponse or snakelet.Response(handler, handler.wfile)
			
			if snake.needsSession() or snake.requiresUser():
				session = self.addSessionCookie(req,resp)
			if snake.requiresUser() and not req.getSession().getLoggedInUser():
				resp.sendError(403, "You must be logged in to access this page.");
				return
			snake.addNoCacheHeaders(resp)
			snake.serve(req, resp)
			if not resp.used():
				resp.sendError(404,"snakelet had no output")
		except Exception,x:
			handler.reportSnakeletException()
			# done... error has also been sent to the client.

	def run_Ypage_POST(self,handler,page,query):
		# get the result from the GET, and write it to the output stream
		result = self.run_Ypage_GET(handler,page,query)
		if result:
			handler.copyfile(result,handler.wfile)
		
	def run_Ypage_GET(self,handler, path, query, passtroughRequest=None, passtroughResponse=None):
		fullpath=os.path.join(self.getDocRootPath(),urllib.url2pathname(path))
		if query and query[0]=='?':
			query=query[1:]
		try:
			f=open(fullpath)
			if passtroughRequest:
				# we were called as a result of forwarding or including in another request
				req=passtroughRequest
				# By design, the new query args are NOT PARSED,
				# so DO NOT DO THIS: req._init_query("",query)
			else:	
				req=snakelet.Request(self,"", query, handler, handler.rfile)
	
			resp = passtroughResponse or snakelet.Response(handler,handler.wfile)
			outputEncoding = contentType = None

			try:
				page = self.pageEngine.loadPage(fullpath,path,self)
				page.Request = req
				page.RequestCtx = req.getContext()
				page.ApplicationCtx = self.context
				page.WebApp = self
				page.URLprefix = self.getURLprefix()
				if page.needsSession():
					session=self.addSessionCookie(req,resp)
					if session:
						page.SessionCtx=session.getContext()
						page.User=session.getLoggedInUser()
				if page.requiresUser():
					if not hasattr(page,"User") or not page.User:
						resp.sendError(403, "You must be logged in to access this page.");
						return
				(output, outputSize, outputEncoding, contentType)=self.pageEngine.runPage(page,req,resp)
			except CompilerError,cx:
				output=cStringIO.StringIO()
				print "COMPILER ERROR!!!!!!",cx
				# oops something went wrong, print the traceback.
				output.write("<html><head><title>Server error</title></head><body><hr><h2>Exception in server</h2>\n")
				output.write("<h3>Error compiling page &quot;"+path+"&quot;: "+str(cx)+"</h3></body></html>\n")
				outputSize=len(output.getvalue())
				output.seek(0)

			if outputEncoding:
				resp.setEncoding(outputEncoding)
			if contentType:
				resp.setContentType(contentType)
				
			resp.setContentLength(outputSize)
			if not resp.used():
				resp.writeHeader()
			return output

		except IOError,x:
			handler.send_error(404, "File not found")
			return None

	def clearCache(self):
		self.pageEngine.clearCache()
		
	def addSessionCookie(self,request, response):
		try:
			self.lock.acquire()
			if request.session:
				# already got the session, don't try again
				return request.session
			try:
				# try to find the session ID with associated Session object
				sessionID=request.getCookies()["SNSESSID"].value
				print "---Searching Session ",sessionID
				session = self.sessions[sessionID]
				request.setSession(session)
				session.touch()   # update last-used timestamp
				session.setRequestData(request,response,self)
				return session
			except KeyError:
				# no session cookie or invalid, set a new one, create new session
				print "--- No session cookie or invalid id, creating new"
				sessionID=sha.sha(request.getRemoteAddr()+str(time.time())+str(random.random())).hexdigest()
				response.setCookie("SNSESSID",sessionID,path=self.getURLprefix()[:-1]) # omit trailing slash
				session=snakelet.Session(sessionID, self.sessionTimeoutSecs)
				self.sessions[sessionID]=session
				request.setSession(session)
				session.setRequestData(request,response,self)
				print "--- new sessionID=",sessionID
				return session
		finally:
			self.lock.release()

	def getSnakeletLocalURL(self, snakeletClass):
		# import cgi # XXX
		# print "GETSNAKELETURL",cgi.escape(repr(snakeletClass)) # XXX
		for (url,snk) in self.snakelets.items():
			# print "SNAKELET?",url,cgi.escape(repr(snk)) # XXX
			if isinstance(snk, snakeletClass):
				# print "FOUND",url # XXX
				return url
		raise KeyError('no such snakelet')

	def _deleteSession(self, request, response):
		try:
			self.lock.acquire()
			# don't call yourself... 
			session=request.getSession()
			del self.sessions[session.getID()]
			response.delCookie("SNSESSID", path=self.getURLprefix()[:-1])
			request.setSession(None)
			print "SERVER: deleted session ",session.getID()
		finally:
			self.lock.release()
		
	def scanSessionTimeouts(self):
		for session in self.sessions.values()[:]:
			# print self.getURLprefix(),"---> check session ",session.getID() # XXX
			session.destroyIfOverAged()

