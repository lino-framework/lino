#
#	Base implementations for all Snakelet stuff.
#

import cgi,os,sys,time
import urllib, string, Cookie
import codecs

#
#	The SESSION object
#
class Session:
	def __init__(self, sessid, timeoutsecs):
		self.sessionID=sessid
		self.context=ContextContainer()	# session context
		self.timeoutsecs=timeoutsecs
		self.touch()
		self.new=1	# set this *after* the touch()
		self.user=None
	def setRequestData(self, request, response, webapp):
		self.request=request
		self.response=response
		self.webapp=webapp
	def getID(self):
		return self.sessionID
	def isNew(self):
		return self.new
	def getLoggedInUser(self):
		return self.user
	def loginUser(self, user):
		self.user=user
	def getContext(self):
		return self.context
	def touch(self):
		# called by server - don't call yourself
		self.lastused=time.time()
		self.new=0
	def isOverAged(self):
		return (time.time()-self.lastused)>self.timeoutsecs
	def destroy(self):
		print "XXX SESSION "+self.sessionID+" IS BEING DESTROYED"
		print "XXX  AGE: ",time.time()-self.lastused
		# XXX do some notification for objects on session????
		self.webapp._deleteSession(self.request, self.response)
	def destroyIfOverAged(self):
		if self.isOverAged():
			self.destroy()


#
#	The Request's FORM object (with the form parameters)
#	It's a dictionary parameter-->value
#	where value can be singular or a list of values.
#	Uploaded file attachments are treated differently!
#
class FormUploadedFile:
	def __init__(self, name, cgiFieldStorage):
		self.name=name
		self.file=cgiFieldStorage.file
		self.filename=os.path.basename(cgiFieldStorage.filename)
		# XXX this is always -1 :-(  --> self.length=cgiFieldStorage.length
		self.disposition=cgiFieldStorage.disposition
		self.dispositionOptions=cgiFieldStorage.disposition_options
		# self.length=cgiFieldStorage.length  <-- usually -1, unknown
		self.mimeType=cgiFieldStorage.type
		self.typeOptions=cgiFieldStorage.type_options
	def __repr__(self):
		return str(self)
	def __str__(self):
		return "<uploaded file '"+self.filename+"' in field '"+self.name+"' at "+hex(id(self))+">"

class Form(dict):
	def __init__(self, cgiFieldStorage):
		for param in cgiFieldStorage.keys():
			value=cgiFieldStorage[param]
			if type(value)==type([]):
				self[param]=[ mf.value for mf in value]
			elif value.file and value.filename:
				self[param]=FormUploadedFile(param,value)
			else:
				self[param]=value.value
	def simplifyValues(self):
		# every value that is a list with one element,
		# will be replaced by only that element.
		removelist=[]
		for (name, value) in self.items():
			if type(value)==type([]):
				if len(value)==1:
					self[name]=value[0]
				elif len(value)==0:
					removelist+=name
		for name in removelist:
			del self[name]

class FormFileUploadError(Exception):
	pass
	
#
#	The REQUEST encapsulation object
#
class Request:
	def __init__(self,webapp, pathinfo, query, server, ins):
		self.webapp=webapp
		self.ins=ins
		self.server=server
		self.context=ContextContainer()	# only for this request
		self.session=None
		# simulate minimal CGI environment, so we can use the CGI module later
		# to parse the GET/POST requests into a Form object.
		self.env={}
		self._init_query(pathinfo, query)
		self.env['REQUEST_METHOD'] = server.command
		self.env['CONTENT_TYPE'] = server.headers.typeheader or server.headers.type
		self.env['CONTENT_LENGTH'] = server.headers.getheader('content-length') or -1

		co = filter(None, server.headers.getheaders('cookie'))
		if co:
			self.HTTP_COOKIE=', '.join(co)
		else:
			self.HTTP_COOKIE=None
		self.cookies=Cookie.SimpleCookie()
		if self.HTTP_COOKIE:
			self.cookies.load(self.HTTP_COOKIE)
		self.maxPOSTsize=200000  # 200Kbytes 

	def _init_query(self, pathinfo, query):
		# this is called by __init__() but also when constructing
		# a new request object as a result of redirection/inclusion
		self.PATH_INFO=pathinfo
		self.arg=None
		possible_query_arg = string.replace(query, '+', ' ').split('&')
		if '=' not in possible_query_arg[0]:
			self.arg=possible_query_arg[0]
			if len(possible_query_arg)>1:
				query='&'.join(possible_query_arg[1:])
			else:
				query=''
		self.QUERY_STRING=self.env['QUERY_STRING'] = query or ""
		self._cgi_form=None

	def getServerSoftware(self): 	return self.server.version_string()
	def getServerIP(self): 			return self.server.getServerIP()
	def getServerName(self): 		return self.server.getServerName()
	def getRealServerName(self):	return self.server.getRealServerName()
	def getServerProtocol(self): 	return self.server.protocol_version
	def getServerPort(self): 		return self.server.server.server_port
	def getBaseURL(self,useip=0):	return self.server.getBaseURL(useip)
	def getPathInfo(self): 		return self.PATH_INFO
	def getMethod(self):		return self.env['REQUEST_METHOD']
	def setMethod(self, method): self.env['REQUEST_METHOD']=method
	def getQuery(self):			return self.QUERY_STRING
	def getRemoteHost(self):	return self.server.address_string()
	def getRemoteAddr(self):	return self.server.client_address[0]
	def getContentType(self):	return self.env['CONTENT_TYPE']
	def getContentLength(self):	return self.env['CONTENT_LENGTH']
	def getUserAgent(self):		return self.server.headers.getheader('user-agent') or None
	def getCookie(self):		return self.HTTP_COOKIE
	def getCookies(self):		return self.cookies
	def getInput(self):			return self.ins
	def getArg(self):			return self.arg
	def setArg(self, arg):		self.arg=arg
	def getWebApp(self):		return self.webapp
	def getRangeStr(self):		return self.server.headers.getheader('range') or None
	def getRange(self):
		rangeStr=self.getRangeStr()
		if rangeStr:
			# content range is like "bytes=9000-12000" or "bytes=234-"
			(t,r) = rangeStr.split('=')
			if t.lower()=="bytes":
				(frm,to)=r.split('-')
				if frm:
					frm=int(frm)
				else:
					frm=0
				if to:
					to=int(to)
				else:
					to=sys.maxint
				return (frm,to)
			else:
				# only supports bytes ranges...
				raise ValueError("only supports range header in BYTES")
		else:
			return None

	def getRealRemoteAddr(self):
		return self.server.headers.get("x-forwarded-for") or self.getRemoteAddr()
	def getAuth(self):				return self.server.headers.getheader('Authorization') or None
	def getAllHeaders(self):		return self.server.headers
	def getHeader(self, header):	return self.server.headers[header]
	def getForm(self):
		# return a cached form if it exists (once it has been parsed)
		if self._cgi_form:
			return self._cgi_form
		else:
			try:
				maxlen, cgi.maxlen=(cgi.maxlen, self.maxPOSTsize)
				try:
					self._cgi_form = Form(cgi.FieldStorage(fp=self.ins, environ=self.env))
				except ValueError,x:
					raise FormFileUploadError(x)

				# XXX if the method is POST, we have to parse the QUERY_STRING ourselves...????
				if self.getMethod()=='POST':
					extraParams={}
					for key,value in cgi.parse_qsl(self.getQuery()):
						extraParams.setdefault(key,[]).append(value)
					self._cgi_form.update(extraParams)
				self._cgi_form.simplifyValues()
				return self._cgi_form
			finally:
				cgi.maxlen=maxlen
	def setParameter(self,param,value):
		self.getForm()[param]=value
	def getParameter(self,param):
		return self.getForm().get(param,'')
	def getContext(self):
		return self.context
	def setSession(self, session):
		self.session=session
	def getSession(self):
		return self.session
	def deleteSession(self):
		self.session.destroy()
	def getSessionContext(self):
		return self.session.getContext()
	def setMaxPOSTsize(self, numbytes):
		self.maxPOSTsize=numbytes
		

#
#	The RESPONSE encapsulation object
#
class Response:
	def __init__(self, server, outs):
		self.server=server
		self._outs=self.outs=outs
		self.content_type="text/html"
		self.content_encoding=None
		self.content_length=-1
		self.header_written=0
		self.error_sent=0
		self.redirection_performed=0
		self.response_code=200
		self.response_string="Snakelet output follows"
		self.userHeaders={}
		self.cookies=Cookie.SimpleCookie()
	def getDummy(self, output):
		# create a dummy response object with a custom output stream
		# (used for instance in Ypages to include external URLs)
		dummy=Response(self.server, output)
		dummy.header_written=1
		dummy.error_sent=1
		return dummy
	def setContentType(self, type):
		self.content_type=type
	def setContentLength(self, len):
		self.content_length=len
	def setEncoding(self, encoding):
		self.content_encoding=encoding
		self.outs=codecs.getwriter(encoding)(self._outs)
	def guessMimeType(self, filename):
		return self.server.guess_type(filename)
	def setHeader(self, header, value):
		self.userHeaders[header]=value
	def setResponse(self, code, msg="Snakelet output follows"):
		self.response_code=code
		self.response_string=msg
	def HTTPredirect(self, URL):
		if self.header_written:
			raise RuntimeError('can not redirect when getOutput() has been called')
		self.setResponse(302,"Redirected") # HTTP 302=redirect
		self.setHeader("Location",URL)
		out=self.getOutput()
		out.write("<html><head><title>Redirection</title></head>\n"
				  "<body><h1>Redirection</h1>\nYou're being <a href=\""+URL+"\">redirected</a>.</body></html>")
		self.setRedirectionDone()
	def writeHeader(self):
		# minimalistic HTTP response header
		if self.header_written:
			raise RuntimeError("header has already been written")
		self.server.send_response(self.response_code, self.response_string)
		contentType=self.content_type
		if self.content_encoding:
			contentType+="; charset="+self.content_encoding
		self.server.send_header("Content-Type", contentType)
		if self.content_length>=0:
			self.server.send_header("Content-Length",str(self.content_length))
		for (h,v) in self.userHeaders.items():
			self.server.send_header(h,v)
		for c in self.cookies.values():
			self.server.send_header("Set-Cookie",c.OutputString())
		self.server.end_headers()
		self.header_written=1
	def getOutput(self):
		if self.redirection_performed:
			raise RuntimeError('cannot write after redirect() call')
		if not self.header_written:
			self.writeHeader()
		return self.outs
	def sendError(self, code, message=None):
		if not self.header_written:
			self.error_sent=1
			self.header_written=1
			return self.server.send_error(code, message)
		else:
			raise RuntimeError("cannot send error after header has been written")
	def getCookies(self):
		return self.cookies
	def setCookie(self, name, value, path=None, domain=None, maxAge=None, comment=None, secure=None):
		self.cookies[name]=value
		self.cookies[name]["version"]=1
		self.cookies[name]["path"]=''
		self.cookies[name]["domain"]=''
		self.cookies[name]["max-age"]=''
		self.cookies[name]["comment"]=''
		self.cookies[name]["secure"]=''
		if path: self.cookies[name]["path"]=path
		if domain: self.cookies[name]["domain"]=domain
		if maxAge!=None: self.cookies[name]["max-age"]=maxAge
		if comment: self.cookies[name]["comment"]=comment
		if secure: self.cookies[name]["secure"]=secure
		self.setHeader("P3P","CP='CUR ADM OUR NOR STA NID'")	# P3P compact policy
	def delCookie(self, name, path=None, domain=None, comment=None, secure=None):
		# delete the cookie by setting maxAge to zero.
		self.setCookie(name, "discarded", path, domain, 0, comment, secure)
		
	def setRedirectionDone(self):
		self.redirection_performed=1
	def used(self):
		return self.redirection_performed or self.header_written or self.error_sent
	def kill(self):
		self.server.kill()
		self.error_sent=1
	def initiateRedirectionOrInclude(self,url):
		if self.header_written:
			self.outs.flush()
		else:
			self.setHeader("Content-Location",url)
	def wasErrorSent(self):
		return self.error_sent

class ContextContainer:
	# just an empty class to store stuff into, it makes the 'context' storage of a snakelet.
	pass


#
#	The Snakelet base class.
#
class Snakelet:

	def __init__(self, url, webapp):
		self.webapp=webapp
		self.localUrl = url
		self.url = urllib.basejoin(webapp.getURLprefix(),url)
		self.snakeletctx = ContextContainer()
		self.content_type="text/html"
		self.init()

	def init(self):
		# initialize snakelet. Override this in subclasses.
		pass

	def getDescription(self):
		# override in subclass for meaningful string.
		return "-"

	def getContext(self):
		return self.snakeletctx
	def getAppContext(self):
		return self.webapp.getContext()

	def getFullURL(self,request,useip=0):
		return urllib.basejoin(request.getBaseURL(useip),self.url)
	def getURL(self):
		return self.url
	def getLocalURL(self):
		return self.localUrl
	def getSnakeletLocalURL(self, snakeletClass):
		return self.webapp.getSnakeletLocalURL(snakeletClass)
	def getWebApp(self):
		return self.webapp

	def needsSession(self):
		return 1		# by default, all snakelets are in a session.
	def requiresUser(self):
		return 0		# by default, does NOT require a user to be logged in.
		
	def serve(self, request, response):
		raise NotImplementedError("implement serve method in subclass!")

	def addNoCacheHeaders(self, response):
		response.setHeader("Pragma","No-cache")		# no caching of ypages...
		response.setHeader("Cache-Control","No-cache")
		response.setHeader("Expires","-1")

	def redirect(self, URL, request, response):
		URL = urllib.basejoin(self.url, URL)  # make always absolute...
		if response.header_written or response.redirection_performed:
			raise RuntimeError('can not redirect twice or when getOutput() has been called')
		request.server.redirect(URL, request, response)

	def include(self, URL, request, response):
		URL = urllib.basejoin(self.url, URL) # make always absolute...
		return request.server.include(URL, request, response)

	def escape(self,str):
		if str:
			return cgi.escape(str,1)	# force " --> &quot;
		else:
			return ""

