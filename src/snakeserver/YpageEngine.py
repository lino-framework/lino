import os, sys, cgi
import string
import shutil
import codecs
import urllib
from ypage.compiler import PageCompiler, CompilerError
from snakelet import Response, Snakelet

try:
	import cStringIO as StringIO
except ImportError:
	import StringIO
	
	
PAGECACHE = "pageCache"
COMPILED_SUFFIX = ".py"

class YpageEngine:
	def __init__(self,name,serverRoot):
		name="YP_"+name
		self.cachedir = os.path.join(serverRoot,PAGECACHE,name)
		self.cachedir = os.path.abspath(self.cachedir)
		self.name=name
		self.createCacheDir()
		# add the cache dir to the import path if it is not there already
		cacheRoot=os.path.abspath(PAGECACHE)
		if cacheRoot not in sys.path:
			sys.path.append(cacheRoot)

	def createCacheDir(self):
		if not os.path.isdir(self.cachedir):
			os.mkdir(self.cachedir)
		f=open(os.path.join(self.cachedir, "__init__.py"), "w")
		f.write("# package\n")
		f.close()
	
	def makeFileName(self,path):
		allowed=string.letters+string.digits
		result=[]
		for c in path:
			if c in allowed:
				result.append(c)
			else:
				result.append('_')
		result.append(COMPILED_SUFFIX)
		return ''.join(result)
		
	def clearCache(self):
		try:
			shutil.rmtree(self.cachedir)
		except OSError,x:
			print "WARNING: ERROR WHILE CLEARING CACHE:",x
		self.createCacheDir()
		
	def loadPage(self, pageFile, pageName, webapp):
		cachedPageFileName=os.path.join(self.cachedir,self.makeFileName(pageName))
		baseName=os.path.splitext(os.path.basename(cachedPageFileName))[0]
		pageModule=self.name+"."+baseName

		if os.path.isfile(cachedPageFileName):
			if os.path.getmtime(pageFile)>os.path.getmtime(cachedPageFileName):
				self.compilePage(pageFile, cachedPageFileName, pageModule)
		else:
			self.compilePage(pageFile, cachedPageFileName, pageModule)
		
		try:
			env={ }
			exec "import "+pageModule+" as YPAGEMODULE" in env
			return env["YPAGEMODULE"].Page(pageName, webapp)  # instantiate page object
		except Exception,x:
			raise CompilerError(str(x)+" (in generated source: "+cachedPageFileName+")")

	def runPage(self, page, _request, _response):
		output=StringIO.StringIO()
		if page.getPageEncoding():
			output=codecs.getwriter(page.getPageEncoding()) (output)
		page.createOutput(output,_request,_response)
		size=len(output.getvalue())
		output.seek(0)
		return output,size,page.getPageEncoding(), page.getPageContentType()

	def compilePage(self, pageFile, cachedPageFileName, pageModule):
		print "COMPILING YPAGE",pageFile
		output=StringIO.StringIO()
		PageCompiler().compilePage(pageFile, output)
		outfile=file(cachedPageFileName,"wb")
		outfile.write(output.getvalue())
		outfile.close()
		try:
			# delete the .pyc/.pyo files 
			os.remove(cachedPageFileName+"c")
		except OSError:
			pass
		try:
			os.remove(cachedPageFileName+"o")
		except OSError:
			pass
		try:
			# delete the imported module
			del sys.modules[pageModule]
		except KeyError:
			pass


class Ypage(Snakelet):

	class PageAbortError(Exception):
		pass
	class PageSendErrorError(Exception):
		def __init__(self, error, msg=None):
			self.error=error
			self.msg=msg
	class PageForwardURL(Exception):
		def __init__(self, url):
			self.url=url

	def __init__(self, pageName, webapp):
		Snakelet.__init__(self, pageName, webapp)
		# no further special init done...
		
	def getDescription(self):
		return "Ypage snakelet"
	def getPageEncoding(self):
		return None
	def getPageContentType(self):
		return None
	def createOutput(self, out,_request,_response):
		self.out=out
		try:
			self.addNoCacheHeaders(_response)
			self.create(out,_request,_response)
		except Ypage.PageAbortError,pax:
			self.out.write("<hr><strong>Page aborted<p>"+str(pax)+"</strong>")
		except Ypage.PageSendErrorError,pex:
			_response.sendError(pex.error, pex.msg)
			self.out.truncate(0)
			return
		except Ypage.PageForwardURL, pfx:
			self.out.truncate(0)
			return self.redirect(pfx.url, _request, _response)
		except Exception,x:
			self.reportPageException(x,self.out)
		self.out.flush()
	def write(self, string):			# support for "self.write(...)" in page
		self.out.write(str(string))

	def reportPageException(self,exc,out):
		# oops something went wrong, print the traceback.
		import traceback
		typ, value, tb = sys.exc_info()
		out.write("<html><head><title>Server error</title></head><body><hr><h2>Exception in server</h2>\n")
		out.write("<h3>Page &quot;"+self.getURL()+"&quot; caused an error: "+str(exc)+"</h3>\n")
		out.write("<H3>Traceback (innermost last):</H3>\n")
		list = traceback.format_tb(tb) + traceback.format_exception_only(typ, value)
		out.write("<PRE>%s<B>%s</B></PRE></body></html>\n" % ( cgi.escape("".join(list[:-1]),1), cgi.escape(list[-1],1) ) )
		del tb

	def escape(self, msg):
		return cgi.escape(msg,1)
		
	def abort(self,message=''):
		raise Ypage.PageAbortError(message)
	
	def include(self, URL, request, response):
		# overridden from Snakelet
		URL = urllib.basejoin(self.url, URL) # always absolute...
		return request.server.include_Ypage(URL, request, response)

	def sendError(self, error, msg=None):
		raise Ypage.PageSendErrorError(error,msg)

