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


from lino.htgen.elements import \
     CDATA, Element, Container, escape, unescape

class BR(Element):
    #flowable=True
    pass

class IMG(Element):
    flowable=True
    allowedAttribs=dict(src="src",
                        width="width",
                        height="height")



class Fragment(Container):
    fragmentable=True
    flowable=False
##     allowedAttribs=dict(id='id',
##                         lang='lang',
##                         title='title')
    allowedAttribs=dict(xclass='class',
                        id='id',
                        lang='lang',
                        style='style',
                        title='title')


class SPAN(Fragment):
    allowedContent = (CDATA,IMG,Fragment)

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
    flowable=True
    
    """Maybe P must be the first element because MemoParser wouln't
    otherwise handle empty lines inside a LI correctly.  To be
    tested."""

class UL(Fragment): 
    flowable=True
    allowedContent = (LI,)
    def li(self,*args,**kw):
        return self.append(LI(*args,**kw))

class OL(UL): 
    pass



class Cell(Fragment):
    allowedAttribs=dict(
        align="align",
        valign="valign",
        **Fragment.allowedAttribs)
class TD(Cell):
    pass
    
class TH(Cell):
    pass
    
class TR(Fragment):
    allowedContent=(TD,TH)
    
class COL(Element):
    allowedAttribs=dict(span="span",width="width")

class COLGROUP(Fragment):
    allowedContent=(COL,)
    allowedAttribs=dict(span="span",width="width")

class THEAD(Fragment):
    allowedContent=(TR,)
class TFOOT(Fragment):
    allowedContent=(TR,)
class TBODY(Fragment):
    allowedContent=(TR,)
    
class TABLE(Fragment):
    fragmentable=False
    flowable=True
    allowedContent=(TR,COLGROUP,THEAD,TFOOT,TBODY)
    
    def addrow(self,*cells):
        return self.append(TR(*[TD(e) for e in cells]))
    
def tablerows(table,area):
    """
    area is one of 0:THEAD, 1:TFOOT, 2:TBODY

    subdividing a table into areas is optional. if present, it must be
    in the specified order. if no areas specified, all TR elements are
    considered part of the TBODY.
    
    """
    for elem in table.content:
        if elem.__class__ is THEAD:
            if area == 0:
                for cell in elem.content:
                    yield cell
        elif elem.__class__ is TFOOT:
            if area == 1:
                for cell in elem.content:
                    yield cell
        elif elem.__class__ is TBODY:
            if area == 2:
                for cell in elem.content:
                    yield cell
        elif elem.__class__ is TR:
            if area == 2:
                yield elem
        elif elem.__class__ is COLGROUP:
            pass
        else:
            raise "unhandled element %s" % elem
        




class P(Fragment):
    fragmentable=False
    flowable=True
    allowedContent = (CDATA,SPAN,BR,IMG)
    allowedAttribs = dict(
        align="align",
        **SPAN.allowedAttribs)
    
class H(P):
    level=None
    def __init__(self,level,*args,**kw):
        assert level > 0 and level <= 9
        self.level=level
        Container.__init__(self,*args,**kw)
        
    def tag(self):
        return self.__class__.__name__+str(self.level)
        
class H1(P): pass
class H2(P): pass
class H3(P): pass
class H4(P): pass
class H5(P): pass
class H6(P): pass
class H7(P): pass
class H8(P): pass
class H9(P): pass

class PRE(P):
    allowedContent = (CDATA,)

class A(SPAN):
    allowedAttribs=dict(href="href",
                        **SPAN.allowedAttribs)


P.autoClosedByStart=(P,LI,UL,OL,TABLE,PRE)
P.autoClosedByEnd=(LI,UL,OL,TABLE,TD,TH,TR)
TD.autoClosedByStart=(TD,TH,TR)
TD.autoClosedByEnd=(TH,TR,TABLE)
TH.autoClosedByStart=(TD,TH,TR)
TH.autoClosedByEnd=(TD,TR,TABLE)
TR.autoClosedByStart=(TR,TABLE)
TR.autoClosedByEnd=(TABLE,)
LI.autoClosedByStart=(LI,)
LI.autoClosedByEnd=(UL,OL)

LI.allowedContent = TD.allowedContent \
                    = TH.allowedContent \
                    = (CDATA,P,BR,SPAN,IMG,TABLE)
    

    
class BODY(Container):
    allowedAttribs=dict(
        bgcolor='bgcolor',
        **Fragment.allowedAttribs)
    allowedContent=(P,IMG,TABLE,UL,OL,PRE)

class HEAD(Container):
    ignore=True

class HTML(Container):
    flowable=True
    allowedContent=(BODY,HEAD)
    
