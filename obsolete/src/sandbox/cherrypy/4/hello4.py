#!/usr/bin/python
import cherrypy

from HyperText.Documents import Document
from HyperText import HTML as html

from lino.apps.pinboard import demo

class Root:
    def __init__(self,dbsess):
        self.dbsess = dbsess
        
    def default(self,*args,**kw):
        title=str(self.dbsess)
        doc=Document(title=html.TITLE(title))
        
        div = html.DIV(klass="title")
        doc.append(div)
        div.append(html.H1(title))

        
        div = html.DIV(klass="menu")
        doc.append(div)
        
        p = html.P("Menu:")
        div.append(p)
        p.append(html.BR())
        p.append(html.A("home",href="/"))
        p.append(html.BR())
        p.append(html.A("foo",href="foo/bar/baz"))
        p.append(html.BR())
        p.append(html.A("reports",href="report"))
        

        doc.append(html.P(self.dbsess.app.aboutString()))
        doc.append(html.P('args='+repr(args)))
        doc.append(html.P('kw='+repr(kw)))
        #
        div = html.DIV(klass="footer")
        doc.append(div)
        div.append(html.P("foo "+cherrypy.request.base + " bar"))
        return str(doc)
        
    default.exposed = True



dbsess=demo.startup()
frm = dbsess.db.app.showMainForm()

cherrypy.root = Root(dbsess)

cherrypy.server.start()


