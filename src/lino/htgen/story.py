## Copyright 2003-2008 Luc Saffre 

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


from lino.misc.tsttools import UniStringIO
from lino.htgen.memo import MemoParser, ParserError
from lino.htgen import html
from lino.misc import restify

import re

def url2html(s):
    a=s.split(None,1)
    url=a[0]
    if len(a) == 1:
        txt=url
    else:
        txt=a[1]
    return '<a href="%s">%s</a>' % (url,txt)

def parsekw(s,kw):
    "todo"
    pass

def img2html(s,**kw):
    a=s.split(None,1)
    name=a[0]
    if len(a) > 1:
        parsekw(a[1],kw)
    return '<img src="%s">' % name

## def url2html(matchobj):
##     url=matchobj.group(1)
##     txt=matchobj.group(2)
##     if len(txt) == 0:
##         txt=url
##     return '<a href="%s">%s</a>' % (url,txt)

## def ref2html(matchobj):
##     ref=matchobj.group(1)
##     txt=matchobj.group(2)
##     if len(txt) == 0:
##         txt=ref
##     return '<a href="%s">%s</a>' % (url,txt)

def mark_em(matchobj):
    return '<em>' + matchobj.group(1) + "</em>"

CMDS=dict(
    url=url2html,
    #ref=ref2html,
    img=img2html,
    )

def cmd_match(matchobj):
    cmd=matchobj.group(1)
    params=matchobj.group(2)
    try:
        return CMDS[cmd](params)
    except KeyError,e:
        return matchobj.group(0)

REGS = (
    ( re.compile(r"\*([^\*]+?)\*"), mark_em ),
#    ( re.compile(r"\[url\s+(\S+)\s*((?:[^[\]]|\[.*?\])*?)\]"), url2html ),
#    ( re.compile(r"\[ref\s+(\S+)\s*(.*)\]"), ref2html ),
    ( re.compile(r"\[(\w+)\s+((?:[^[\]]|\[.*?\])*?)\]"), cmd_match ),
    )


def oparse(s):
    for reg in REGS:
        s=reg[0].sub(reg[1],s)
    #s=s.replace("[B]","<b>")
    #s=s.replace("[b]","</b>")
    #return restify.reSTify(s)
    return s



class Story:
    """
    Implemented by Document
    """
    def append(self,*args,**kw):
        raise NotImplementedError
            
    def table(self,*args,**kw):
        return self.append(html.TABLE(*args,**kw))

    def par(self,*args,**kw):
        return self.append(html.P(*args,**kw))
        
    def heading(self,level,text,**kw):
        return self.append(html.H(level,text,**kw))
    def h1(self,txt,**kw): self.heading(1,txt,**kw)
    def h2(self,txt,**kw): self.heading(2,txt,**kw)
    def h3(self,txt,**kw): self.heading(3,txt,**kw)

    
    def memo(self,txt,style=None,**kw):
        assert style is None, "use keyword xclass=style instead"
        p=MemoParser(self,**kw)
        x=oparse(txt)
        #print x
        p.feed(x)
        p.close()

    def load_html(self,data):
        p=MemoParser()
        p.feed(data)
        p.close()
        assert p.container.__class__ is html.HTML
        assert p.container.content[0].__class__ is html.BODY,\
          "content[0] is %s" % p.container.content[0].__class__
        for e in p.container.content[0].content:
            self.append(e)

    def report(self,rpt):

        """ adamo is no longer supported, so this won't work. But I
        leave the code until I get a working usage example.  """
    
        rpt.beginReport()
        header=[html.TH(col.getLabel(),align=col.halign,valign=col.valign)
                for col in rpt.columns]
        t=html.TABLE()
        cols=[]
        for col in rpt.columns:
            cols.append(html.COL(width=str(col.width)+"*"))
        t.append(html.COLGROUP(*cols))
        t.append(html.THEAD(TR(*header)))
        # TFOOT if present must come before TBODY
        tbody=t.append(html.TBODY())
        for row in rpt.rows():
            line=[html.TD(s, align=col.halign,
                     valign=col.valign)
                  for (col,s) in row.cells()]
            tbody.append(html.TR(*line))
            
        rpt.endReport()
        #print t.toxml()
        return self.append(t)

    def par(self,txt,style=None,**kw):
        return self.append(html.P(txt,xclass=style,**kw))

    def pre(self,txt,style=None,**kw):
        return self.append(html.PRE(txt,xclass=style,**kw))

    def verses(self,txt,style=None,**kw):
        if False:
            # this would be better, but reportlab cannot handle
            # manual line breaks
            t2=""
            for line in txt.splitlines():
                if len(line.strip()):
                    t2 += "<br/>"+line
                else:
                    t2 += '\n'
            return self.memo(txt,style,False,**kw)
        # so we must use a trick:
        if style is None:
            style="Verses"
        return self.memo(txt,style,**kw)

    def example(self,intro,code):
        self.memo(intro)
        self.h2("Code:")
        self.pre(code)
        self.h2("Result:")
        self.memo(code)
    
            
        
    def table(self,*args,**kw):
        return self.append(html.TABLE(*args,**kw))
    def ul(self,*args,**kw):
        return self.append(html.UL(*args,**kw))
    def ol(self,*args,**kw):
        return self.append(html.OL(*args,**kw))
    
    
class Document(Story):
    extension=None
    def __init__(self,
                 title="Untitled",
                 date=None,
                 stylesheet=None):

        self.title=title
        self.date=date
        self.stylesheet=stylesheet
        self.body=html.BODY()

    def append(self,*args,**kw):
        return self.body.append(*args,**kw)
        
    def setTitle(self,title):
        self.title=title

    def __xml__(self,wr):
        wr("<html><head>\n<title>")
        wr(html.escape(self.title))
        wr("""</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
""")
        if self.stylesheet is not None:
            wr('<link rel=stylesheet type="text/css" href="%s">\n'
               % self.urlto(self.stylesheet))
        wr('<meta name="KEYWORDS" content="">\n')
        wr('<meta name="GENERATOR" content="lino.htgen">\n')
        wr('<meta name="author" content="">\n')
        wr('<meta name="date" content="%s">'%self.date)
        wr("<head>\n")
        self.body.__xml__(wr)
        wr("""\n</html>\n""")

        
    def toxml(self):
        u=UniStringIO()
        self.__xml__(u.write)
        return u.getvalue()


        
## class HtmlResponse(Document):
    
##     def render(self,wr):
##         return self.__xml__(wr)

## class HtmlDocument(Document):
    
##     extension=".html"
    
##     def saveas(self,filename,showOutput=False):
##         f=file(filename,"wt")
##         self.__xml__(f.write)
##         f.close()

