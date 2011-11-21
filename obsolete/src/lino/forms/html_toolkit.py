## Copyright 2005-2006 Luc Saffre 

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


from lino import forms
from lino.forms import toolkit

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
# end of from twisted.web.microdom


firstPageButton = '[<<]'
lastPageButton = '[>>]'
prevPageButton = '[<]'
nextPageButton = '[>]'
beginNavigator = '''
<p class="nav">Navigator:
'''
endNavigator = "</p>"



class Locatable:
    # local URL. URL for a local resource
    extension=None
    def __init__(self,name,location=None,parent=None):
        pos=name.rfind("/")
        if pos != -1:
            assert location is None
            location=name[:pos]
            name=name[pos+1:]
            
        if location is None:
            if parent is None:
                location=""
            else:
                location = parent.location
        else:
            assert not location.endswith('/')
            assert not location.startswith('/')
            if parent is not None:
                location = parent.addloc(location)
            
        self.location=location
        if name.endswith(self.extension):
            name = name[:-len(self.extension)]
        self.name=name
        self.parent=parent
        
    def filename(self):
        return self.name + self.extension

    def dirname(self):
        return self.location.replace("/",os.path.sep)

    def getRoot(self):
        if self.parent is None:
            return self
        return self.parent.getRoot()

    def urlto(self,other):
        if self.location == other.location:
            return other.filename()
        return self.locto(other.location) + "/" + other.filename()
    
    def locto(self,dest):
        if self.location=="": return dest
        l1=self.location.split("/")
        if dest=="": return "/".join([".."]*len(l1))
        l2=dest.split("/")
        while len(l1) and len(l2) and l1[0] == l2[0]:
            del l1[0]
            del l2[0]
        #l= [".."]*(len(l1)-1) + l2
        l= [".."]*len(l1) + l2
        return "/".join(l)

    def addloc(self,location):
        if self.location == "":
            return location
        return self.location+"/"+location

class StyleSheet(Locatable): 
    extension=".css"



class Label(toolkit.Label):

    def __html__(self,wr):
        wr()
        
class Button(toolkit.Button):
    
##     def __repr__(self):
##         return "Button %s %s at %s" % (
##             self.getLabel(),
##             repr(self.wxctrl.GetSize()),
##             repr(self.wxctrl.GetPosition()))
        
    def wxsetup(self,form,panel,box):
        #parentFormCtrl = self.getForm().ctrl
        #winId = wx.NewId()
        btn = wx.Button(panel,-1,self.getLabel(),
                        wx.DefaultPosition,
                        wx.DefaultSize)
        #btn.SetBackgroundColour('YELLOW')
        #parentFormCtrl.Bind(wx.EVT_BUTTON, lambda e:self.click(), btn)
        panel.Bind(wx.EVT_BUTTON,
                   EventCaller(self.click),
                   btn)
##         if self.hotkey is not None:
##             #print 'Button.wxsetup', self.hotkey
##             wx.EVT_CHAR(panel, self.EVT_CHAR)
##             #form.Bind(wx.EVT_KEY_DOWN,self.EVT_CHAR)
        if self.doc is not None:
            btn.SetToolTipString(self.doc)

        box.Add(btn,DONTSTRETCH,0,NOBORDER) #, 0, wx.CENTER,10)
        self.wxctrl = btn

##     def EVT_CHAR(self,evt):
##         print "Button.EVT_CHAR"
##         if self.hotkey.match_wx(evt):
##             self.click()
##             return
##         evt.Skip()

    def setFocus(self):
        self.wxctrl.SetFocus()

class DataGrid(toolkit.DataGrid):
    def __html__(self,wr):
        rpt=self.rpt
        ds=rpt.ds
        pageNum=self.pageNum
        sortColumn=self.sortColumn
        rpt.beginReport(self.doc)

        # title

        #if rpt.label is not None:
        #    self.h(1,rpt.label)


        # navigator

        if True: # flup.lastPage > 1:
            wr(beginNavigator)
                
            if pageNum is None:
                pageNum = 1
            elif pageNum < 0:
                pageNum = ds.lastPage + pageNum + 1
                # pg=-1 --> lastPage
                # pg=-2 --> lastPage-1
                
            if pageNum == 1:
                wr(firstPageButton)
                wr(prevPageButton)
            else:

                doc.writeLink(
                    href=rptname(doc,rpt,
                                 sortColumn=sortColumn,
                                 pageNum=1)+doc.extension,
                    label=firstPageButton)
                
                doc.writeLink(
                    href=rptname(doc,rpt,
                                 sortColumn=sortColumn,
                                 pageNum=pageNum-1)+doc.extension,
                    label=prevPageButton)

##                 ch=self.getChild(rptname(rpt,pageNum=pageNum-1))
##              self.link(uri=self.urito(ch),
##                           label=prevPageButton)



            wr(" [page %d of %d] " % (pageNum, ds.lastPage))
                
            if pageNum == ds.lastPage:
                wr(nextPageButton)
                wr(lastPageButton)
            else:
                doc.writeLink(
                    href=rptname(doc,rpt,
                                 sortColumn=sortColumn,
                                 pageNum=pageNum+1)+doc.extension,
                    label=nextPageButton)
                doc.writeLink(
                    href=rptname(doc,rpt,
                                 sortColumn=sortColumn,
                                 pageNum=ds.lastPage)+doc.extension,
                    label=lastPageButton)
                
                
##                 ch=self.getChild(rptname(rpt,pageNum=pageNum+1))
##              self.link(uri=self.urito(ch),
##                           label=nextPageButton)
##                 ch=self.getChild(rptname(rpt,pageNum=rpt.lastPage))
##              self.link(uri=self.urito(ch),
##                           label=lastPageButton)
                
            wr(' (%d rows)' % len(ds))
            wr(endNavigator)

        
        

        # renderHeader

        wr('<table width="100%" cellpadding="3" cellspacing="3">')
        wr('<tr>\n')
        for col in rpt.columns:
            wr('<th scope="col">')
            if col.datacol == sortColumn:
                doc.writeText(col.getLabel())
            else:
                url=rptname(doc,rpt,
                            pageNum=pageNum,
                            sortColumn=col.datacol)+doc.extension
                doc.writeLink(
                    href=url,
                    label=col.getLabel(),
                    doc="Click here to sort by "+col.getLabel())
            wr('</th>\n')
            
        wr("</tr>\n")
            
            
        # iterate...
        rowno = 0
        for datarow in ds.child(pageNum=pageNum,
                                sortColumns=[sortColumn]):
            rowno += 1
            if rowno % 2 == 0:
                wr("<tr class=''>\n")
            else:
                wr("<tr class='alternate'>\n")
            
            #rptrow = rpt.processItem(doc,datarow)
            rptrow = rpt.processItem(datarow)
            
            i=0
            for col in rpt.columns:
            #for cell in rptrow.cells:
                wr('<td>')
                doc.writeColValue(col.datacol,rptrow.values[i])
                # cell.value)
                #wr('<th scope="row">')
                wr("</td>")
                i+=1
            wr("</tr>\n")
            
            
        # renderFooter
        
        wr("</table>")
        
        rpt.endReport(doc)

    
        

class TextViewer(toolkit.TextViewer):

    def __html__(self,wr):
        wr(self.__class__.__name__)


class VPanel(toolkit.Panel):
    direction=forms.VERTICAL
    
    def __html__(self,wr):
        for c in self._components:
            c.__html__(wr)

class HPanel(toolkit.Panel):
    direction=forms.HORIZONTAL
    def __html__(self,wr):
        wr('<table border="0"><tr>')
        for c in self._components:
            wr('<td>')
            c.__html__(wr)
            wr('</td>')
        wr('</tr></table>')


class EntryMixin:

    def __html__(self,wr):
        if self.hasLabel():
            wr('<P>'+escape(self.getLabel())+'</P>')
        if self.doc is not None:
            wr('<P>'+escape(self.doc)+'</P>')

        type = self.getType()
        if isinstance(type,datatypes.BoolType):
            wr(' type="checkbox"')
            v=self.getValue()
            if v is None:
                v=self.getType().defaultValue
            wr(' value="%r"'%v)
        else:
            wr(' type="text"')
        
        if self.enabled:
            wr(' enabled="true"')
        else:
            wr(' enabled="false"')
            
class Entry(EntryMixin,toolkit.Entry):
    pass

class DataEntry(EntryMixin,toolkit.DataEntry):
    pass

class Link:

    def __init__(self,href,label=None,doc=None):
        if label is None: label=href
        self.label=label
        self.href=href
        
    def __html__(self,wr):
        wr('<a href="'+self.href+'">')
        wr(escape(self.label))
        wr('</a>')

    

class HtmlForm(Locatable):
    extension=".html"
    def __init__(self,
                 form,
                 date=None,
                 name=None,
                 location=None,
                 parent=None,
                 stylesheet=None,
                 **kw):

        self.form=form

        if name is None:
            name="index"
        
        Locatable.__init__(self,name,location,parent)
        
        
        if stylesheet is None:
            if parent is not None:
                stylesheet=parent.stylesheet
        else:
            assert type(stylesheet)==type('')
            stylesheet = StyleSheet(stylesheet,parent=self)

        self.stylesheet = stylesheet
        
        self.date = date


    def getLineWidth(self):
        return 100
    
    def getColumnSepWidth(self):
        return 0
    

    def beginDocument(self,wr):
        wr("<html><head><title>")
        wr(escape(self.form.getTitle()))
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
        wr("<head><body>\n")

        if self.form.menuBar is not None:
            for menu in self.form.menuBar.menus:
                wr('<ul class="adminmenu">')
                for mi in menu.items:
                    #assert mi.action is not None
                    wr('<li>')
                    self.writeLink(
                        href=mi.action,
                        label=mi.getLabel())
                    wr('</li>')
                wr('</ul>')


        
        
    
    def endDocument(self,wr):
        wr("""\
        </body>
        </html>
        """)


    def __html__(self,wr):
        self.beginDocument(wr)
        self.form.mainComp.__html__(wr)
        self.endDocument(wr)
        
    

class Toolkit(toolkit.Toolkit):
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    viewerFactory = TextViewer
    hpanelFactory = HPanel
    vpanelFactory = VPanel
    dataGridFactory = DataGrid

    
    def createFormCtrl(self,frm):
        return HtmlForm(frm)
    
    def executeShow(self,frm):
        frm.ctrl.__html__(self.console.stdout.write)
        

    def executeRefresh(self,frm):
        self.executeShow(frm)
        frm.ctrl.SetTitle(frm.getTitle())

    def closeForm(self,frm,evt):
        #print "closeForm()"
        frm.ctrl.Destroy()

