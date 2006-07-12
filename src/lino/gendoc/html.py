#coding: iso-8859-1

## Copyright 2003-2006 Luc Saffre 

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
from cStringIO import StringIO
from HTMLParser import HTMLParser


from lino.gendoc import gendoc # import WriterDocument

# from twisted.web.microdom
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
    "replace a few special chars with HTML entities."
    for ch, h in ESCAPE_CHARS:
        text = text.replace(ch, h)
    return text 


                    

from lino.oogen.elements import CDATA, Element, Container, InvalidRequest

class BR(Element):
    pass

class IMG(Element):
    allowedAttribs=dict(src="src",
                        width="width",
                        height="height")



class Fragment(Container):
    allowedAttribs=dict(xclass='class',
                        id='id',
                        lang='lang',
                        style='style',
                        title='title')
class SPAN(Fragment):
    allowedContent = (CDATA,Fragment)

#class DIV(Fragment):
#    allowedContent = (CDATA,P,TABLE,SPAN,BR,IMG)
    

class B(SPAN): pass    
class EM(SPAN): pass    
class I(SPAN): pass
class U(SPAN): pass
class SUP(SPAN): pass
class TT(SPAN): pass    
class FONT(SPAN): pass

class LI(Fragment):
    
    """Maybe P must be the first element because MemoParser wouln't
    otherwise handle empty lines inside a LI correctly.  To be
    tested."""

class UL(Fragment): 
    allowedContent = (LI,)
    def li(self,*args,**kw):
        return self.append(LI(*args,**kw))

class OL(UL): 
    pass



class TD(Fragment):
    pass
    
class TH(Fragment):
    pass
    
class TR(Fragment):
    allowedContent=(TD,TH)
    
class COL(Element):
    allowedAttribs=dict(span="span",width="width")

class COLGROUP(Fragment):
    allowedContent=(COL,)
    allowedAttribs=dict(span="span",width="width")

class TABLE(Fragment):
    allowedContent=(TR,COLGROUP,COL)
    



class P(Fragment):
    autoClosedBy=(UL,OL,TABLE)
    allowedContent = (CDATA,SPAN,BR,IMG)
    allowedAttribs = dict(
        align="align",
        **SPAN.allowedAttribs)
    
class H(P):
    def __init__(self,level,*args,**kw):
        assert level > 0 and level <= 9
        self.level=level
        Container.__init__(self,*args,**kw)
        
    def tag(self):
        return self.__class__.__name__+str(self.level)
        


class PRE(P):
    allowedContent = (CDATA,)

class A(SPAN):
    allowedAttribs=dict(href="href",
                        **SPAN.allowedAttribs)


class Story(Container):
    def __init__(self,doc,*args,**kw):
        self.document=doc
        Container.__init__(self,*args,**kw)

    def format(self,**kw):
        self.document.format(self,**kw)
            
    def table(self,*args,**kw):
        return self.append(Table(self.doc,*args,**kw))

    def par(self,*args,**kw):
        return self.append(P(*args,**kw))
        
    def heading(self,level,text,**kw):
        return self.append(H(level,text,**kw))
    def h1(self,txt,**kw): self.heading(1,txt,**kw)
    def h2(self,txt,**kw): self.heading(2,txt,**kw)
    def h3(self,txt,**kw): self.heading(3,txt,**kw)
    
    



TD.autoClosedBy=(TD,TH,TR,TABLE)
TH.autoClosedBy=(TD,TH,TR,TABLE)
TR.autoClosedBy=(TR,TABLE)
LI.autoClosedBy=(LI,TABLE)
LI.allowedContent = TD.allowedContent \
                    = TH.allowedContent \
                    = (CDATA,P,SPAN,IMG)
    

    
    
##     def __init__(self,href=None,label=None,doc=None):
##         if label is None: label=href
##         self.href=href
##         self.label=label
##         self.doc=doc
        
##     def __html__(self,doc,wr):
##         wr('<a href="'+self.href+'">')
##         wr(escape(self.label))
##         wr('</a>')


class MemoParser(HTMLParser):

    def __init__(self,story,style,**kw):
        HTMLParser.__init__(self)
        self.story=story
        self.style=style
        self.kw=kw
        self.stack=[]
        self.buffer=""
        self.newpar=False # "start new par on next data"

##     def reset(self):
##         HTMLParser.reset(self)

    def autopar(self,txt=''):
        p=P(txt,xclass=self.style,**self.kw)
        self.stack.append(p)
        return self.story.append(p)
        
    def handle_data(self,data):
        """process arbitrary data."""
        if len(self.stack) == 0:
            self.autopar()
        tail=self.stack[-1]
        #print self.story.toxml()
        #print "%r -> %r" % (data, tail)
        #raw_input()
        if tail.__class__ is P:
            a = [ line for line in data.split('\n\n')
                  if len(line.strip()) > 0]
            if len(a):
                tail.append(a[0])
                for line in a[1:]:
                    self.autopar(line)
        elif tail.__class__ is BR:
            pass
        elif CDATA in tail.__class__.allowedContent:
            tail.append(data)
        elif len(data.strip()) > 0:
            raise "cannot handle %r inside <%s>" % (data,tail.tag())
##         elif self.newpar:
##             if self.stack[-1].__class__==P:
##                 popped=pop(self.stack)
##                 #print "popped",popped
##             self.stack.append(self.story.par())
##         self.newpar=False

    def handle_charref(self,name):
        """process a character reference of the form "&#ref;"."""
        print "handle_charref", name
        raise NotImplemented
        
    def handle_entityref(self,name):
        """process a general entity reference of the form "&name;"."""
        print "handle_entityref", name
        raise NotImplemented

    def _append(self,elem):
        self.stack[-1].append(elem)
        
    def starttag(self,tag,attrs):
        tag=tag.upper()
        cl=globals()[tag]
        #print attrs
        d={}
        for hk,hv in attrs:
            for k,v in cl.allowedAttribs.items():
                if v == hk:
                    d[k]=hv
                    break
        return cl(**d)
        
    def handle_startendtag(self,tag, attrs):
        elem=self.starttag(tag,attrs)
        self._append(elem)

    def handle_starttag(self, tag, attrs):
        elem=self.starttag(tag,attrs)
        try:
            self._append(elem)
        except InvalidRequest,e:
            if elem.__class__ in self.stack[-1].autoClosedBy:
                popped=self.stack.pop()
                print "<%s> autoClosedBy <%s>" % (
                    popped.tag(),elem.tag())
                self.story.append(elem)
##             if self.stack[-1].__class__ is P \
##                and elem.__class__ in(UL,OL,TABLE):
##                 popped=self.stack.pop()
##                 #print "popped",popped
##                 self.story.append(elem)
            else:
                raise
        self.stack.append(elem)
        

    def handle_endtag(self, tag):
        while True:
            if len(self.stack) == 0:
                raise "stack underflow"
            popped=self.stack.pop()
            if tag.upper() == popped.tag():
                return
            cl=globals()[tag.upper()]
            if cl in popped.autoClosedBy:
                print "<%s> autoClosedBy </%s>" % (
                    popped.tag(),tag.upper())
            else:
                raise "Found </%s> where </%s> expected" % (
                    tag.upper(), popped.tag())


class BODY(Story):
    allowedAttribs= dict(
        bgcolor='bgcolor',
        **Fragment.allowedAttribs)
        
    def report(self,rpt):
        rpt.beginReport()
        header=[TH(col.getLabel()) for col in rpt.columns]
        t=TABLE(TR(*header))
        for row in rpt.rows():
            line=[TD(s) for (c,s) in row.cells()]
            t.append(TR(*line))

        rpt.endReport()
        return self.append(t)

    def par(self,txt,style=None,**kw):
        return self.append(P(txt,xclass=style,**kw))

    def pre(self,txt,style=None,**kw):
        return self.append(PRE(txt,xclass=style,**kw))

    def heading(self,level,txt,style=None,**kw):
        return self.append(H(level,txt,xclass=style,**kw))

    def memo(self,txt,style=None,**kw):
        p=MemoParser(self,style,**kw)
        p.feed(txt)
        p.close()

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
        return self.append(TABLE(*args,**kw))
    def ul(self,*args,**kw):
        return self.append(UL(*args,**kw))
    def ol(self,*args,**kw):
        return self.append(OL(*args,**kw))
    
    def getDocument(self):
        return None



class Document:

    def __init__(self,
                 title="Untitled",
                 date=None,
                 stylesheet=None):

        self.title = title
        self.date = date
        self.stylesheet = stylesheet
        self.body=self.createStory()

    def createStory(self):
        return BODY(self)

##     def makeStory(self,func,textWidth):
##         if func is not None:
##             s=HtmlStory(self)
##             func(s)
##             return s

        
class HtmlDocument(Document):
    
    def saveas(self,filename):
        f=file(filename,"wt")
        self.__xml__(f.write)
        f.close()

    def __xml__(self,wr):
        wr("<html><head><title>")
        wr(escape(self.title))
        wr("""</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
""")
        if self.stylesheet is not None:
            wr('<link rel=stylesheet type="text/css" href="%s">\n'
               % self.urlto(self.stylesheet))
        wr('<meta name="KEYWORDS" content="">\n')
        wr('<meta name="GENERATOR" content="Lino">\n')
        wr('<meta name="author" content="">\n')
        wr('<meta name="date" content="%s">')
        wr("<head>\n")
        self.body.__xml__(wr)
        wr("""\
        </html>
        """)




