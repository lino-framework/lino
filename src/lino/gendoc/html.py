#coding: latin1

## Copyright 2003-2005 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import sys
import os
opj = os.path.join


from lino.gendoc.gendoc import WriterDocument
from lino.forms.base import MenuContainer

ESCAPE_CHARS = (('&', '&amp;'),
                ('<', '&lt;'),
                ('>', '&gt;'),
                ('"', '&quot;'))

def unescape(text):
    "Perform the exact opposite of 'escape'."
    for ch, h in ESCAPE_CHARS:
        text = text.replace(h, ch)
    return text

def escape(text):
    "Escape a few XML special chars with XML entities."
    for ch, h in ESCAPE_CHARS:
        text = text.replace(ch, h)
    return text 

txt2html = escape

## from twisted.web.html import escape

## def txt2html(s):
## 	return escape(s)
## 	#s = escape(s)
## 	# s = s.replace('<','&lt;')
## 	# s = s.replace('>','&gt;')
## 	# s = s.replace('&','&amp;')
## 	#return txt2html(s)

def locdiff(l1,l2):
    if l1 == l2: return ""
    back = len(l1.split("/"))-1
    toloc = l2.split("/")
    l = [".."]*back + toloc
    return "/".join(l)+"/"




BEGIN_PAGE = """
  <html>
  <head>
  <title>%s</title>
  <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
  <link rel=stylesheet type="text/css" href="wp-admin.css">
  <meta name="KEYWORDS" content="">
  <meta name="GENERATOR" content="Lino">
  <meta name="author" content="">
  <meta name="date" content="%s">
  <head>

  <body>

"""
END_PAGE = """
  </body>
  </html>
"""



class Location:
    # local URL. URL for a local resource
    extension=".html"
    def __init__(self,href):
        l = href.split("/")
        assert len(l) > 0
        self.head = l[:-1]
        self.tail = l[-1]
        assert os.path.splitext(self.tail) == self.extension
        
    def filename(self):
        return self.tail

    def dirname(self):
        return opj(self.head)

    def child(self,href):
        l = href.split("/")
        ch = copy(self)
        ch.tail = l[-1]
        ch.head = list(self.head)
        head = l[:-1]
        while head[0] == "..":
            ch.head.pop()
            del head[0]
        ch.head += head
        return ch
        

    def __str__(self):
        if len(self.head):
            return "/".join(self.head)+self.tail
        return self.tail

class HtmlFile(Location):    
    extension=".html"

class StyleSheet(Location):    
    extension=".css"


class HtmlDocument(WriterDocument,MenuContainer,):
    def __init__(self,
                 content=None,
                 title=None,
                 date=None,
                 location="index.html",
                 css="wp-admin.css",
                 **kw):
        WriterDocument.__init__(self)
        MenuContainer.__init__(self)
        self.date = date
        self.css = StyleSheet(css)
        #self.cssName = cssName
        #self.cssLocation = cssLocation
        self.content=content
        if type(location) == type(''):
            location = HtmlFile(location)
        self.location = location
        #self.name=name

        self.children = []
        #assert self.name is not None
        if title is None:
            title = self.location.filename()
        self.title = title

    def child(self,content=None,location=None,**kw):
        kw.setdefault("css",str(self.css))
        if content is not None:
            kw.setdefault("location",self.location.child(
                content.getName()+self.location.extension))
            #kw.setdefault("name",content.getName())
            kw.setdefault("title",content.getTitle())
            kw['content'] = content
        c = self.__class__(**kw)
        self.children.append(c)
        return c


    def text(self,txt):
        self.write(txt2html(txt))
        
    def a(self,href,label,doc=None):
        self.write('<a href="'+href+'">')
        self.text(label)
        self.write('</a>')


    def h(self,level,txt):
        assert level > 0 and level <= 9
        tag = "H"+str(level)
        self.write("<%s>" % tag)
        self.text(txt)
        self.write("</%s>\n" % tag)


    def beginDocument(self,wr):
        self.writer = wr
        self.write(BEGIN_PAGE)
    
    def endDocument(self):
        self.write(END_PAGE)
        self.writer = None


    def render(self,wr):
        self.beginDocument(wr)
        if self.menuBar is not None:
            for menu in self.menuBar.menus:
                self.write('<ul id="adminmenu">')
                for mi in menu.items:
                    #assert mi.action is not None
                    self.write('<li>')
                    self.a(href=mi.action,
                           label=mi.getLabel())
                    self.write('</li>')
                self.write('</ul>')


                    
        if self.content is not None:
            self.content.render(self)
        self.endDocument()

    
    def save(self,ui,targetRoot="."):
        filenames = []
        dirname = opj(targetRoot,
                      self.location.replace("/",os.path.sep))
        fn = opj(dirname, self.leafname())
        print fn
        ui.status("Writing %s...",fn)
        if not os.path.isdir(dirname):
            ui.notice("makedirs(%s)",dirname)
            os.makedirs(dirname)
        if not ui.confirm(fn):
            return []
        filenames.append(fn)
        fd = file(fn,"wt")
        self.render(fd.write)
        fd.close()
        for ch in self.children:
            filenames += ch.save(ui,targetRoot)
        return filenames

        
    def report(self,rpt):
        if rpt.iterator.lastPage > 1:
            self._report(rpt.child(name="index",pageNum=1))
            for i in range(1,rpt.iterator.lastPage):
                childrpt = rpt.child(name=str(i+1),pageNum=i+1)
                self.child(content=childrpt)
        else:
            self._report(rpt)
        
    def _report(self,rpt):
        
        # initialize...
        rpt.beginReport(self)

        # title

        if rpt.label is not None:
            self.h(1,rpt.label)

        # renderHeader

        self.write(
            '<table width="100%" cellpadding="3" cellspacing="3">')
        self.write('<tr>\n')
        for col in rpt.columns:
            self.write('<th scope="col">')
            self.text(col.getLabel())
            self.write('</th>\n')
        self.write('</tr>\n')

        self.write("<tr>")
        for col in rpt.columns:
            self.write("<th>")
            if len(rpt.iterator.orderByColumns) == 0 \
               or col == rpt.iterator.orderByColumns[0]:
                self.text(col.getLabel())
            else:
                ds2 = rpt.iterator.query(orderBy=col.name)
                rpt2 = rpt.child(iterator=ds2)
                name = self.name
                if rpt.iterator.pageNum is not None:
                    name += str(rpt.iterator.pageNum)
                name += "_" + col.name
                child = self.child(name=name,content=rpt2)
                url = self.urlto(child)
                self.a(
                    href=url,
                    label=col.getLabel(),
                    doc="Click here to sort by "+col.getLabel())
            self.write("<th>")
            
        self.write("</tr>")
            
            
        # iterate...
        rowno = 0
        for row in rpt.iterator:
            rowno += 1
            if rowno % 2 == 0:
                self.write("<tr class=''>\n")
            else:
                self.write("<tr class='alternate'>\n")
            
            cells = rpt.processRow(self,row)

            for cell in cells:
                if cell.value is None:
                    s = ""
                else:
                    s = cell.col.format(cell.value)
                    
                self.write('<td>')
                #self.write('<th scope="row">')
                self.text(s)
                self.write("</td>")
            self.write("</tr>\n")
            
            
        # renderFooter
        
        self.write("</table>")
        
        rpt.endReport(self)

    
    def urlto(self,to):
        return locdiff(self.location,to.location) + to.leafname()

    def leafname(self):
        return self.name + ".html"    
        


## class Node:
##     def __init__(self,parent=None,name=None,targetDir=None):
##         self.parent=parent
##         self.name=name
##         self.targetDir = targetDir
##         self.children=[]
##         if parent is not None:
##             parent.addChild(self)
        
##     def addChild(self,node):
##         self.children.append(node)

##     def filename()

##     def urlto(self,to,*args,**kw):
##         relPath
        

## class DataReportNode(Node):
##     def __init__(self,site,parent,ds):
##         Node.__init__(self,site,parent,ds.
##         self.ds=ds

##     def myurl(self,orderBy=None,pageNum=None):
        
##         if pageNum is None:
##             pageNum = self.ds.pageNum # usually 1
##         if pageNum is None:
##             pageNum = 1
##         if pageNum == 1:
##             if orderBy is None or orderBy == self.ds.orderByColumns[0]:
##                 return "index.html"
            
##         s = str(pageNum) + "_" + orderBy.name
##         return s + ".html"
    
##     def generate(self):
##         filenames = []
##         for i in range(0,self.ds.lastPage):
##             for col in self.ds.getVisibleColumns():
##                 q = self.ds.query(pageNum=i+1,orderBy=col.name)
##                 fn = self.myurl(orderBy=col)
##                 filenames.append(fn)
##                 fd = file(opj(self.targetDir,fn),"wt")
##                 rpt = MpsHtmlReport(self,fd.write)
##                 q.executeReport(rpt)
##                 fd.close()
                
##         return filenames

