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


import cherrypy
from HyperText.Documents import Document as HyperTextDocument
from HyperText import HTML as html

from lino.forms import base, HK_CHAR


def label2txt(s):
    return s.replace(HK_CHAR,'')


class Label(base.Label):
    pass
    
                
class Button(base.Button):
    pass
    
    
class DataGrid(base.DataGrid):
    pass
        
class DataForm(base.DataForm):
    pass
        

class TextViewer(base.TextViewer):

    def addText(self,s):
        self.getForm().notice(s)
    
class Panel(base.Panel):
    pass
    #def render(self,doc):
    #    pass
            
class Entry(base.Entry):
    pass

class DataEntry(base.DataEntry):
    pass



class Form(base.Form):

    def __init__(self,*args,**kw):
        self._isShown = False
        base.Form.__init__(self,*args,**kw)


    
    def status(self,msg,*args,**kw):
        self.app.toolkit.console.status(msg,*args,**kw)


    def onJobInit(self,job):
        pass


    def onJobRefresh(self,job):
        pass

    def onJobDone(self,job,msg):
        pass

    def onJobAbort(self,*args,**kw):
        pass

    def isShown(self):
        return self._isShown

    def close(self):
        self.session.toolkit.closeForm(self)
        base.Form.close(self)
    
            


class Toolkit(base.Toolkit):
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    viewerFactory = TextViewer
    panelFactory = Panel
    dataGridFactory = DataGrid
    navigatorFactory = DataForm
    formFactory = Form
    
    def __init__(self,file=None,**kw):
        base.Toolkit.__init__(self,**kw)
        self._running = False
        self._formStack=[]
        self.configFile=file

    def running(self):
        return self._running 

    def run_awhile(self):
        assert self.running()
        pass
    
    def run_forever(self,sess):
        assert not self.running()
        self._running = True
        cherrypy.root = Page(self,sess)
        if self.configFile is not None:
            cherrypy.config.update(file=self.configFile)
        cherrypy.server.start()
        
    def showForm(self,frm):
        if frm.modal:
            sess.notice("modal forms are not supported")
            return
        self._formStack.append(frm)

    def closeForm(self,frm):
        self._formStack.remove(frm)

    

##     def addApplication(self,app):
##         base.Toolkit.addApplication(self,app)





class Document(HyperTextDocument):
    """
    implements lino.gendoc.Document used e.g. by lino.reports.Report
    """
    def getLineWidth(self):
        return 100
    def getColumnSepWidth(self):
        return 0

    def p(self,txt):
        self.append(html.P(txt))
    
    def renderLabel(self,lbl):
        #self.append(html.P(lbl.getLabel()))
        self.append(label2txt(lbl.getLabel()))
        
    def renderButton(self,btn):
        if btn.enabled:
            self.append(html.A(label2txt(btn.getLabel()),
                               href=cherrypy.request.path+"/"+btn.name))
        else:
            self.append(btn.label2txt(getLabel()))
            
    def renderEntry(self,e):
        if e.enabled:
            self.p(e.name)
        
    def renderDataGrid(self,grid):
        if grid.enabled:
            self.report(grid.rpt)
            
    def report(self,rpt):
        self.append(html.H2(rpt.getTitle()))
        t=html.TABLE()
        self.append(t)

        tr=html.TR()
        t.append(tr)
        for col in rpt.columns:
            tr.append(html.TH(col.getLabel()))

        for row in rpt.rows(self):
            tr=html.TR()
            t.append(tr)
            i=0
            for col in rpt.columns:
                tr.append( html.TD(
                    self.cell2html(col.datacol,row.values[i])
                    ))
                i+=1

        
    def cell2html(self,col,value):
        if value is None: return ""
        return col.format(value)


class Page:
    def __init__(self,toolkit,dbsess):
        self.dbsess = dbsess
        self.toolkit=toolkit
        self.dbsess.db.app.showMainForm(self.dbsess)
        self.mainForm=self.toolkit._formStack.pop()


    def default(self,*args,**kw):
        frm=self.mainForm
        if len(args) >= 2:
            mnu=frm.menuBar.findMenu(args[0])
            mi=mnu.findItem(args[1])
            mi.click()
            frm=self.toolkit._formStack[-1]
        if len(args) >= 3:
            m=getattr(frm,args[2])
            m(*args[3:])
            frm=self.toolkit._formStack[-1]
            
        title=str(frm.getLabel())
        doc=Document(title=html.TITLE(title))
        
        div = html.DIV(klass="title")
        doc.append(div)
        div.append(html.H1(title))
        
        div = html.DIV(klass="menu")
        doc.append(div)
        
        p = html.P("Menu:")
        div.append(p)

        if frm.menuBar is not None:
            for mnu in frm.menuBar.menus:
                p.append(html.BR())
                #p.append(html.A(mnu.getLabel(),href=mnu.name))
                p.append(label2txt(mnu.getLabel()))
                for mi in mnu.items:
                    p.append(html.BR())
                    p.append(" &middot; &nbsp;",
                             html.A(label2txt(mi.getLabel()),
                                    href=mnu.name+"/"+mi.name))
        frm.mainComp.render(doc)
        #doc.append(html.HR())
        #doc.append(html.P(self.dbsess.app.aboutString()))
        #doc.append(html.P('args='+repr(args)))
        #doc.append(html.P('kw='+repr(kw)))
        #
        div = html.DIV(klass="footer")
        doc.append(div)
        div.append(html.P("foo "+cherrypy.request.base + " bar"))
        return str(doc)
        
    default.exposed = True

        






