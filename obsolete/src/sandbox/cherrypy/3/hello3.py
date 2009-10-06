#!/usr/bin/python
import cherrypy

from HyperText.Documents import Document
from HyperText import HTML as html

from lino.apps.pinboard import demo

class Page(Document):

    def __init__(self,title,*args,**kw):
        self.title=html.TITLE(title)
        Document.__init__(self,*args,**kw)

    def setup(self):
        div = html.DIV(klass="title")
        self.append(div)
        div.append(html.H1(self.title))

    def addMenu(self):
        div = html.DIV(klass="menu")
        self.append(div)
        
        p = html.P("Menu:")
        div.append(p)
        p.append(html.BR())
        p.append(html.A("home",href="/"))
        p.append(html.BR())
        p.append(html.A("foo",href="foo/bar/baz"))
        p.append(html.BR())
        p.append(html.A("reports",href="report"))

    def addFooter(self):
        div = html.DIV(klass="footer")
        self.append(div)
        div.append(html.P("foo "+cherrypy.request.base + " bar"))
        

class Root:
    def __init__(self,dbsess):
        self.dbsess = dbsess
        
    def default(self,*args,**kw):
        page=Page(str(self.dbsess))
        page.addMenu()
        page.append(html.P('args='+repr(args)))
        page.append(html.P('kw='+repr(kw)))
        page.addFooter()
        return str(page)
        
    default.exposed = True



dbsess=demo.startup()

cherrypy.root = Root(dbsess)

cherrypy.config.update(file='server.cfg')
cherrypy.server.start()
