#!/usr/bin/python
from cgi import escape
import cherrypy

class Page:
	def __init__(self,title):
		self.title = title
		
	def header(self):
		yield '''<html>
		<head><title>%s</title><head>
		<body><h2>%s</h2>''' % (self.title, self.title)
		yield '<a href="/">home</a>'

	def footer(self):
		yield '<div class="footer">%s</div>' % cherrypy.request.base
		yield '</div></body></html>' 
	
## 	def index(self):
## 		for y in self.header(): yield y
## 		yield """
## 		<p>Isn't this exciting? Click
## 		<a href="foo/bar/baz">here</a> and 
## 		<a href="bla?foo=1&bar=baz">there</a>!
## 		</p>"""
## 		for y in self.footer(): yield y
		
## 	index.exposed = True
	
	def default(self,*args,**kw):
		for y in self.header(): yield y
		yield '<p>args='+escape(repr(args))+"</p>"
		yield '<p>kw='+escape(repr(kw))+"</p>"
		yield """
		<p>Isn't this exciting? Click
		<a href="foo/bar/baz">here</a> and 
		<a href="?foo=1&bar=baz">there</a>!
		</p>"""
		for y in self.footer(): yield y
		
	default.exposed = True

cherrypy.root = Page("Hello, world!")
cherrypy.config.update(file='server.cfg')
cherrypy.server.start()
