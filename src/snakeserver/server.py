import SocketServer
import mimetypes
import urllib, cgi, socket
import os, time, sys, types, copy, shutil 
import binascii
import BaseHTTPServer
import dirlister
import webapp

try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

#
#	The actual HTTP request handler used by the HTTP server.
#	Doesn't use SimpleHTTPServer because that one is TOO simple
#	and has many features we override anyhow.
#
class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	rbufsize = -1		# input stream is fully buffered
	wbufsize = 1024		# a little buffering on the output stream

	server_version = BaseHTTPServer.BaseHTTPRequestHandler.server_version+" (Snakelets 1.3)"
	
	error_message_format = """\
<head>
<title>Error %(code)d</title>
</head>
<body>
<h1>Error response</h1>
<p>%(code)s = %(explain)s.
<p>Server message: %(message)s.
<p><hr><address>"""+server_version+" Python/"+sys.version.split()[0]+" </body>"

	# extensions_map contains the mime type definitions.
	extensions_map=mimetypes.types_map.copy()
	extensions_map.update(
	  {
		"":	"text/plain", # Default, *must* be present
		".mp3":	"audio/mpeg",
		".m3u":	"audio/x-mpegurl",
		".y": "text/html",
		".spy": "text/html",
		".py": "text/plain",
		".jar": "application/x-jar",
		".class": "application/x-java-class",
		".ogg": "application/ogg"
	  }
	)

	def do_GET(self):
		self.path=self.normpath(self.path)
		if self.path:
			f=self.send_head()
			if f:
				self.copyfile(f,self.wfile)
				f.close()

	def do_HEAD(self):
		self.path=self.normpath(self.path)
		if self.path:
			f=self.send_head()
			if f:
				f.close()

	def do_POST(self):
		self.path=self.normpath(self.path)
		if self.path:
			# Handle form POST requests.
			app=self.server.getWebApp(self.path)
			return app.do_POST(self)

	def normpath(self, path):
		# normalize path (remove things like foo/./bar and /foo/../bar/)
		# XXX simpler (and safer!) is to just refuse those kinds of urls
		if path.find('/./')>=0 or path.find('/../')>=0:
			self.send_error(400, "Unsupported url path notation with relative directories")
			return None
		return path

	def kill(self):
		try:
			# XXX ONLY WORKS ON *NIX?
			self.connection.close()
			# use low-level IO to close streams, otherwise we block...
			os.close(self.wfile.fileno())
			os.close(self.rfile.fileno())
		except:
			pass

	def send_head(self,
                 passtroughRequest=None,
                 passtroughResponse=None):
		# common code for GET and HEAD requests. (supports scripts / snakelets)
		web = self.server.getWebApp(self.path)
		if not web:
			self.send_error(404,"File not found (no context enabled for URL "+self.path+")")
			return
		path = urllib.url2pathname(self.path)
		path = os.path.join(web.getDocRootPath(),
                          path[len(web.getURLprefix()):])

		# check for index pages if path is a directory
		if os.path.isdir(path):
			for index in "index.html", "index.htm", "index.y", "index.spy":
				indexf = os.path.join(path, index)
				if os.path.exists(indexf):
					path = indexf
					self.path=os.path.join(self.path,index)
					break
			else:
				return self.list_directory(web,path,passtroughResponse)
		try:
			if self.command=="GET":
				return web.do_GET(self, passtroughRequest, passtroughResponse)
			elif self.command=="HEAD":
				return web.do_HEAD(self)
			else:
				if not passtroughResponse or not passtroughResponse.used():
					self.send_error(501, "Unsupported method")
				else:
					passtroughResponse.getOutput().write("Unsupported method "+self.command)
		except webapp.NotHandled:	
			path=urllib.splitquery(path)[0]	# chop off any ?query=foo
			ctype = self.guess_type(path)
			if ctype.startswith('text/'):
				mode='r'
			else:
				mode='rb'
			try:
				f=open(path,mode)
				stats = os.stat(path)
			except IOError,x:
				if not passtroughResponse or not passtroughResponse.used():
					self.send_error(404,"File not found")
				else:
					passtroughResponse.getOutput().write("File not found: "+path)
				return None

			if not passtroughResponse or not passtroughResponse.used():
				self.send_response(200)
				self.send_header("Content-type",ctype)
				self.send_header("Content-length",stats.st_size)
				(etag,lmod) = self.create_ETag_LMod_headers(stats.st_mtime, stats.st_size, stats.st_ino)
				self.send_header("ETag", etag)
				self.send_header("Last-Modified", lmod)
				self.end_headers()
				if passtroughResponse:
					passtroughResponse.header_written=1
			return f

	def create_ETag_LMod_headers(self, timestamp, size, locationid):
		etag='%x%x%x' % (timestamp,size,locationid)
		etag='"%s"' % binascii.b2a_base64(etag).strip()
		return (etag, time.strftime("%a, %d %b %Y %H:%M:%S GMT",time.gmtime(timestamp)))

	def reportSnakeletException(self):		
		# oops something went wrong, print the traceback.
		typ, value, tb = sys.exc_info()
		if type(typ)==types.StringType:
			name=typ
		else:
			name=typ.__name__
		self.log_error("SNAKELET threw exception: "+name+": "+str(value))
		import traceback
		self.wfile.write("<html><head><title>Server error</title></head><body><hr><h2>Exception in server</h2>\n<H3>Traceback (innermost last):</H3>\n")
		list = traceback.format_tb(tb) + traceback.format_exception_only(typ, value)
		self.wfile.write("<PRE>%s<B>%s</B></PRE>\n"
                                 % ( cgi.escape("".join(list[:-1]),1), cgi.escape(list[-1],1) ) )
		del tb
                self.wfile.write('<p><a href="/manage/manage.sn?q=shutdown&confirm=yes">shutdown</a>\n')
                self.wfile.write('<a href="/manage/manage.sn?q=restart&confirm=yes">restart</a>')
                self.wfile.write("</body></html>\n")

	def getServerIP(self):
		# return the IP address of the interface the request arrived on
		return self.request.getsockname()[0]

	def getServerName(self):
		return self.server.servername

	def getRealServerName(self):
		return self.server.getHostName(self.getServerIP())

	def guess_type(self, path):
		# overloaded & called from base class: guess the content type
		base, ext = os.path.splitext(path)
		if self.extensions_map.has_key(ext):
			return self.extensions_map[ext]
		ext = ext.lower()
		if self.extensions_map.has_key(ext):
			return self.extensions_map[ext]
		else:
			return self.extensions_map[""]

	def getBaseURL(self,useip=0):
		# XXX NO HTTPS SUPPORT.
		if useip:
			url='http://'+self.getServerIP()
		else:
			url='http://'+self.getServerName()
		if self.server.server_port!=80:
			return url+':'+str(self.server.server_port)
		else:
			return url

	def list_directory(self, webapp, physicalpath, passtroughResponse=None):
		# overloaded & called from base class: list directory contents. Don't list forbidden dirs
		# Note that self.path has already been adjusted for the webapp.
		path=urllib.unquote(self.path)
		if not webapp.allowDirListing(path):
			if not passtroughResponse or not passtroughResponse.used():
				self.send_error(403, "No permission (by server config) to list directory");
			else:
				passtroughResponse.getOutput().write("No permission (by server config) to list directory "+path)
			return None
		if path and not path.endswith('/'):
			# it doesn't end in a slash, send a redirect WITH a slash
			f=StringIO.StringIO()
			f.write("<html><head><title>Redirection</title></head>\n"
			        "<body>For correct directory listing, you're being <a href=\""+path+"/\">redirected</a>.</body></html>")
			if not passtroughResponse or not passtroughResponse.used():
				self.send_response(302, "Document moved")
				self.send_header("Content-type","text/html")
				path=self.getBaseURL()+path+'/'
				self.send_header("Location",path)
				self.end_headers()
			f.seek(0)
			return f
		# path ends in '/' and is allowed to be listed.
		try:
			filelist,dirlist = dirlister.listdir(physicalpath)
			filelist.sort(lambda a, b: cmp(a.lower(), b.lower()))
			dirlist.sort(lambda a, b: cmp(a.lower(), b.lower()))
			f = StringIO.StringIO()
			f.write(("<head>\n<title>Directory listing for %s</title>\n</head>\n" % path ) +
			        ("<body>\n<h2>Directory listing for %s</h2>\n<hr>\n" % path))
			if path:
				f.write("<a href=\"..\">parent directory</a>")
			if dirlist:
				f.write("<p>--Directories--\n<ul>\n")
				f.write( '\n'.join( ['<li><a href="%s/">%s</a>\n' % (urllib.quote(name), name) for name in dirlist ]) )
				f.write("</ul>\n");
			if filelist:
				f.write("<p>--Files--\n<ul>\n")
				f.write( '\n'.join( ['<li><a href="%s">%s</a>\n' % (urllib.quote(name), name) for name in filelist ]) )
				f.write("</ul>\n");
			else:
				f.write("There are no files in this location.\n");
			f.write("<hr>\n\n<address>Server: Python "+self.server_version+"</address>\n</body>")
			f.seek(0)
			if not passtroughResponse or not passtroughResponse.used():
				self.send_response(200,"Directory content follows")
				self.send_header("Content-type", "text/html")
				self.end_headers()
			return f
		except os.error:
			if not passtroughResponse or not passtroughResponse.used():
				self.send_error(403, "No permission to list directory");
			else:
				passtroughResponse.getOutput().write("No permission to list directory "+path)

	def translate_path(self, path):
		# translate path to local filesystem syntax
		path = os.path.normpath(urllib.unquote(path))
		web=self.server.getWebApp(self.path)
		path = os.path.join(web.getDocRootPath(),
								  path[len(web.getURLprefix()):])
		return path

	def copyfile(self, source, outputfile):
		shutil.copyfileobj(source, outputfile)

	def address_string(self):
		# override the base version that looks up the FQ hostname.
		# we just stick with the IP address...
		host, port = self.client_address
		return str(host)

	def include(self, url, request, response):
		# read the other URL and write the result to the output stream.
		# Perform this in a clone of our current request handler object.
		response.initiateRedirectionOrInclude(url)
		handler=copy.copy(self)
		handler.doRedirect(self, url, request, response, 1)

	def include_Ypage(self, url, request, response):
		# read the other URL and return the result as string (for Ypages).
		# Perform this in a clone of our current request handler object.
		# url must be absolute http://foo/bar.html  or /foo/bar.html
		handler=copy.copy(self)
		output = StringIO.StringIO()
		response=response.getDummy(output) # work on a dummy response
		handler.doRedirect(self, url, request, response, 1)
		return output.getvalue() # return the result from our output 'stream' :)
	
	def redirect(self, url, request, response):
		# read the other URL and write the result to the output stream.
		# Perform this in a clone of our current request handler object.
		# url must be absolute http://foo/bar.html  or /foo/bar.html
		response.initiateRedirectionOrInclude(url)
		handler=copy.copy(self)
		handler.doRedirect(self, url, request, response, 0)
		response.setRedirectionDone()
		
	def doRedirect(self, parentHandler, url, request, response, isInclude=0):
		if not url[0]=='/':
			# assume http(s):// external url
			try:
				result=urllib.urlopen(url)
				if result:
					if not isInclude and not response.used():
						# copy HTTP headers (only with redirect)
						for (header, value) in result.headers.items():
							response.setHeader(header, value)
						response.writeHeader()
					self.copyfile(result, response.outs)
			except Exception,x:
				response.sendError(404,"not found: "+str(x))
		else:
			# call our custom version of send_head for the new url and reusing the request object
			self.path=url
			self.command="GET"
			result=self.send_head(request,response)
			if result:
				if not response.used():
					response.writeHeader()
				self.copyfile(result, response.outs)


#
#	The threading HTTP server.
#
class ThreadingServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):

	def __init__(self, address, handler, serverRoot="."):
		self.servername=address[0]
		BaseHTTPServer.HTTPServer.__init__(self,address,handler)
		self.mustShutdown=0
		self.mustRestart=0
                self.serverRoot = serverRoot
                sys.path.append(serverRoot)
			
	def server_activate(self):
		# initialize the server
		self.webApps = {}
		self.rootWebApp = None		# webapp that handles '/' url root.
		BaseHTTPServer.HTTPServer.server_activate(self)		# activate socket listener
		self._hostname_cache = {}

	def getHostName(self, ip):
		# get the FQ hostname that belongs to the specified IP address
		if self._hostname_cache.has_key(ip):
			return self._hostname_cache[ip]
		else:
			x=socket.getfqdn(ip)
			self._hostname_cache[ip]=x
			return x

	def readWebApps(self,clearPageCache=0):
		# scan web applications
		appsPath = os.path.join(self.serverRoot,"webapps")
		for fn in os.listdir(appsPath):
			pfn = os.path.join(appsPath,fn)
			if os.path.isdir(pfn):
				if os.path.exists(os.path.join(pfn,'__init__.py')):
					self.readWebApp(fn)
		try:
			self.rootWebApp=self.webApps['/']
			print 'ROOT webapp: ',self.rootWebApp.getFileSystemPath()
		except KeyError:
			print "No ROOT webapp for url '/' has been defined!"
			raise SystemExit(1)
		print len(self.webApps),"webapps registered."
		if clearPageCache:
			print "Clearing page caches"
			for webapp in self.webApps.values():
				webapp.clearCache()

	def readWebApp(self, web, mustReload=0):
           # add the webapps dir to the module search path.
           # (only if we're not reloading)
           abspath=os.path.abspath(os.path.join(self.serverRoot,"webapps",web))
           if mustReload:
              # reloading. first, remove the old webapp
              name=os.path.split(web)[1]
              url='/'+name+'/'
              web=name
              self.unloadWebApp(url)
           try:
              exec "import webapps."+web+" as WA"
              WA.configItems=getattr(WA,"configItems",{})
              WA.dirListAllower=getattr(WA,"dirListAllower",None)
              WA.start=getattr(WA,"start","")
              WA.sessionTimeoutSecs=getattr(WA,"sessionTimeoutSecs",600) # default=10 minutes
              url='/'+web+'/'
              if hasattr(WA,"ROOT_WEBAPP") and WA.ROOT_WEBAPP:
                 url='/'
              try:
                 wa=webapp.WebApp(abspath, web, WA.name, url,
                                  WA.docroot, WA.snakelets,
                                  WA.sessionTimeoutSecs,
                                  WA.configItems,
                                  WA.dirListAllower,
                                  WA.start, self)
              except AttributeError,x:
                 # XXX weird?? occurs when reloading server?
                 print "!!! problem during webapp load:",x
                 print "!!! webapp=",url
                 print "!!! webapp NOT installed"
                 import traceback
                 traceback.print_exc()
                 sys.path.remove(abspath)
              else:
                 if self.webApps.has_key(url):
                    print "Duplicate webapp url: ",url," (webapp:",web,")"
                    raise SystemExit(1)
                 self.webApps[url]=wa
                 print "WEBAPP",web," (",len(wa.getSnakelets()),"snakelets )"
                 print " name =",WA.name
                 print "  url =",url
           except ImportError,x:
              # not a correct webapp
              print "!!! No correct config found for webapp",web,":",x
              print "!!! webapp NOT installed"
              # LS 20030925 sys.path.remove(abspath)

	def getWebApp(self, url):
		# find the webapp (except '/') that handles this url
		for web in self.webApps:
			if len(web)>1 and url.startswith(web):
				webapp=self.webApps[web]
				if webapp.isEnabled():
					return webapp
				else:
					break
		# fallback to ROOT webapp, IF it is enabled
		if self.rootWebApp.isEnabled():
			return self.rootWebApp
		return None

	def enableWebApp(self, url, enabled):
		# enable/disable the webapp for this url prefix
		self.webApps[url].setEnabled(enabled)

	def reloadWebApp(self, url):
		# reload the webapp for this url prefix
		web=self.webApps[url].getFileSystemPath()
		self.readWebApp(web,1)
		self.rootWebApp=self.webApps['/']

	def clearWebAppCache(self, url):
		self.webApps[url].clearCache()

	def unloadAllWebApps(self):
		for web in self.webApps.keys()[:]:
			self.unloadWebApp(web)
	def unloadWebApp(self, web):
           isRootWebApp=0
           try:
              name=os.path.split(self.webApps[web].getFileSystemPath())[1]
           except KeyError:
              # check if it is the root webapp
              name=os.path.split(self.rootWebApp.getFileSystemPath())[1]
              if web == '/'+name+'/':
                 isRootWebApp=1
              else:
                 raise KeyError("cannot find webapp "+web)
           modulename="webapps."+name
           for n in sys.modules.keys()[:]:
              if n.startswith(modulename) and \
                    type(sys.modules[n]) is types.ModuleType:
                 del sys.modules[n]
           if isRootWebApp:
              del self.webApps['/']
              del self.rootWebApp
           else:
              del self.webApps[web]
              
	def reloadAllWebApps(self, clearPageCache=0):
		self.unloadAllWebApps()
		self.readWebApps()
		if clearPageCache:
			for wa in self.webApps.values():
				wa.clearCache()
	
	def getWebRoot(self):
		return self.rootWebApp.getDocRootPath()

	def setServerName(self, servername):
		self.servername=servername

	def shutdown(self):
		self.mustShutdown=1
		self.newHostnamePort=None
	def restart(self,hostname=None,port=None):
		self.mustShutdown=1
		self.mustRestart=1
		self.newHostnamePort=(hostname,port)

	def serve_forever(self):
		import select
		self.mustShutdown=0
		self.mustRestart=0
		while not self.mustShutdown:
			ins,outs,excs=select.select([self],[],[self],5)
			if self in ins:
				self.handle_request()
			self.reapSessions()
		print "Shutting down gracefully."

	def reapSessions(self):
		# close and delete all web sessions that have timed out.
		for webapp in self.webApps.values():
			webapp.scanSessionTimeouts()



		


#
#	Start everything!
#

def createHTTPD(HTTPD_PORT, servername, bindname,clearPageCache,
                serverRoot="."):
	print 'Creating server on',bindname,'(servername='+servername+')'
	httpd = ThreadingServer( (bindname,HTTPD_PORT),
                                 MyRequestHandler,
                                 serverRoot)
	httpd.setServerName(servername)
	# read and initialize the webapps with their snakelets
	httpd.readWebApps(clearPageCache)
	print 'WEBROOT=',httpd.getWebRoot()
	print "Serving HTTP on port", HTTPD_PORT
	return httpd



def main(HTTPD_PORT=80, servername=None, bindname=None, clearPageCache=0):
	if not servername:
		servername=socket.gethostname()
	if bindname is None:
		bindname=servername
	
		
	httpd=createHTTPD(HTTPD_PORT,servername,bindname,clearPageCache)
	
	while 1:
		httpd.serve_forever()
		if not httpd.mustRestart:
			break
		print "RESTARTING SERVER"
		if httpd.newHostnamePort:
			(hostname,port) = httpd.newHostnamePort
			if hostname and port:
				print "HOSTNAME/PORT CONFIG CHANGED: %s:%d" % (hostname,port)
				httpd.server_close()
				httpd.unloadAllWebApps()
				httpd = createHTTPD(port, hostname, bindname, 0)
				continue
		httpd.reloadAllWebApps(clearPageCache)


if __name__=="__main__":
	main(80)
	
