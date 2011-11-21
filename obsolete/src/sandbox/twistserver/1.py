from twisted.web import server, static
from twisted.web.resource import Resource
from twisted.internet import reactor

## class Simple(resource.Resource):
##     def render_GET(self, request):
##         return "<html>Hello, world!</html>"

from lino.schemas.sprl import demo
from lino.etc.twisted import Resource


class Hello(Resource):
   #isLeaf = True
	def getChild(self, name, request):
		if name == '':
			return self
		return Resource.getChild( self, name, request)

	def render_GET(self, request):
		return """<html>
		<head>
		<title>Hello
		</title>
		</head>
      Hello, world!
		<p>I am located at %r
		<br>and postpath is %r.
		</html>"""               % (request.prepath,request.postpath) 


if __name__ == '__main__':
	db = demo.startup()
	resource = Hello()
	root = static.File(r't:\data\luc\www')
	root.putChild('hello', Hello())
	site = server.Site(root)
	reactor.listenTCP(8080, site)
	reactor.run()

