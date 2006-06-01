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



raise """
TODO:

Each Form gets one URL. Will this work?

Forms instantiated only once? Or for each request?

"""

import os
import sys
import time

from cStringIO import StringIO

from lino.forms import base

from HyperText.Documents import Document
from HyperText import HTML as html

def text2html(s):
    s2=""
    for c in s:
        o=ord(c)
        if o <= 127:
            s2 += c
        else:
            s2 += '&#%d;' % o
    return s2
    


def Page(title):
    doc = Document(title=title)
    doc.append(html.H1(title))
    p = html.P("Menu:")
    p.append(html.BR())
    p.append(html.A("home",href="/"))
    p.append(html.BR())
    p.append(html.A("foo",href="foo/bar/baz"))
    p.append(html.BR())
    p.append(html.A("reports",href="report"))
    doc.append(p)
    doc.append(html.HR())
    return doc


class MyRoot(PositionalParametersAware):
    
    def __init__(self,dbsess):
        self.dbsess=dbsess
        self.beginResponse = dbsess.toolkit.beginResponse
        self.endResponse = dbsess.toolkit.endResponse
        
    def index(self, *args,**kw):
        doc=self.beginResponse(title="index()")
        doc.append(html.P("This is the top-level page"))
        return self.endResponse()
    index.exposed=True
    
    def report(self, *args,**kw):
        doc=self.beginResponse(title="report()")
        if len(args) > 0:
            tcl=self.dbsess.getTableClass(args[0])
            if tcl is not None:
                self.dbsess.showViewGrid(tcl,*args[1:],**kw)
            else:
                self.dbsess.warning("%s : no such table",args[0])
                #doc.append(html.P(args[0]+" : no such table"))
                
            return self.endResponse()
        list=html.UL(); doc.append(list)
        for table in self.dbsess.db.app.getTableList():
            li=html.LI() ; list.append(li)
            li.append(html.A(table.getLabel(),
                             href="report/"+table.getTableName()))
            li.append(" (%d rows)" %
                len(self.dbsess.query(table._instanceClass)))

        return self.endResponse()

    report.exposed=True


class Label(base.Label):
    def __html__(self,wr):
        wr(text2html(self.getLabel()))
    
class Button(base.Button):
    def __html__(self,wr):
        url=self.name
        wr(html.A(text2html(self.getLabel()),href=url))

class DataGrid(base.DataGrid):
    def __html__(self,wr):
        wr(self.__class__.__name__)
        
class DataForm(base.DataForm):
    def __html__(self,wr):
        wr(self.__class__.__name__)

class TextViewer(base.TextViewer):
    def __html__(self,wr):
        wr(self.__class__.__name__)
            
class Panel(base.Panel):
    def __html__(self,wr):
        wr(self.__class__.__name__)

class Entry(EntryMixin,base.Entry):
    def __html__(self,wr):
        wr(self.__class__.__name__)

class DataEntry(EntryMixin,base.DataEntry):
    def __html__(self,wr):
        wr(self.__class__.__name__)

class Form(base.Form):
    def __html__(self,wr):
        wr(self.__class__.__name__)
        if self.menuBar is not None:
            for mnu in self.menuBar.menus:
                mnu.__html__(wr)
                for mi in mnu.items:
                    mi.__html__(wr)
        self.mainComp.__html__(wr)

    
class Toolkit(base.Toolkit):
    labelFactory = Label
    entryFactory = Entry
    dataEntryFactory = DataEntry
    buttonFactory = Button
    viewerFactory = TextViewer
    panelFactory = Panel
    dataGridFactory = DataGrid
    navigatorFactory = DataNavigator
    formFactory = Form
    
    def __init__(self,*args,**kw):
        base.Toolkit.__init__(self,*args,**kw)
        self._session = None
        self.response=None
        self._actions={} # URL : (method, args,kw)

    def running(self):
        return self._session is not None

    def run_awhile(self):
        assert self.running()
        pass
    
    def run_forever(self,sess):
        assert not self.running()
        self._session=sess
        sess.showMainForm()
        cherrypy.root = MyRoot(sess)
        cherrypy.server.start()
        

    def write(self,msg):
        #self.response.append(html.Para(msg))
        self.response.append(html.P(msg))
        
    def writeout(self,msg):
        self.response.append(html.P(msg))

            
    def showStatus(self,sess,msg):
        if msg is not None:
            sess.verbose(msg)

    def error(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        self._stderr(msg + "\n")
        sess.logmessage(msg)

    def critical(self,sess,msg,*args,**kw):
        "Something terrible has happened..."
        #self.writelog(msg)
        #if sound:
        #    sound.asterisk()
        self.error(sess,"critical: " + msg,*args,**kw)

    
    def showException(self,sess,e,details=None):
        if details is not None:
            print details
        raise

    def warning(self,sess,msg,*args,**kw):
        "Display message if verbosity is normal. Logged."
        msg = sess.buildMessage(msg,*args,**kw)
        sess.logmessage(msg)
        #self.writelog(msg)
        if self._verbosity >= 0:
            self.writeout(msg)

    def notice(self,sess,msg,*args,**kw):
        "Display message if verbosity is normal. Logged."
        if self._verbosity >= 0:
            msg = sess.buildMessage(msg,*args,**kw)
            sess.logmessage(msg)
            self.writeout(msg)

    def verbose(self,sess,msg,*args,**kw):
        "Display message if verbosity is high. Not logged."
        if self._verbosity > 0:
            msg = sess.buildMessage(msg,*args,**kw)
            self.writeout(msg)
        
    def debug(self,sess,msg,*args,**kw):
        "Display message if verbosity is very high. Not logged."
        if self._verbosity > 1:
            msg = sess.buildMessage(msg,*args,**kw)
            self.writeout(msg)
            #self.out.write(msg + "\n")

            


    def onTaskBegin(self,task):
        if task.getLabel() is not None:
            task.session.notice(task.getLabel())

    def onTaskDone(self,task):
        self.onTaskStatus(task)
        task.session.status()
        #task.summary()
        #if msg is not None:
        #    task.session.notice(task.getLabel() + ": " + msg)
    
    def onTaskAbort(self,task):
        self.onTaskStatus(task)
        task.session.status()
        #task.summary()
        #if task.getLabel() is not None:
        #    msg = task.getLabel() + ": " + msg
        #task.session.error(msg)

    def onTaskIncrement(self,task):
        self.onTaskStatus(task)
        
    def onTaskBreathe(self,task):
        if self.abortRequested():
            task.requestAbort()
    
    def onTaskResume(self,task):
        pass
    
    def onTaskStatus(self,task):
        self.showStatus(task.session,
                        task.session.statusMessage)
    
    def abortRequested(self):
        if not msvcrt: return False
        # print "abortRequested"
        while msvcrt.kbhit():
            ch = msvcrt.getch()
            #print ch
            if ord(ch) == 0: #'\000':
                ch = msvcrt.getch()
                if ord(ch) == 27:
                    return True
            elif ord(ch) == 27:
                return True
        return False


    def message(self,sess,msg,**kw):
        self.writeout(msg)

            
    def confirm(self,sess,prompt,default=True):
        """Ask user a yes/no question and return only when she has
        given her answer. returns True or False.
        
        """
        assert type(default) is type(False)
        return default
            

    def decide(self,sess,prompt,answers,
               dfault=None,
               ignoreCase=True):
        
        """Ask user a question and return only when she has given her
        answer. Returns the index of chosen answer or -1 if user
        refused to answer.
        
        """
        if dfault is None:
            dfault = answers[0]

        return dfault

    
    def textprinter(self,sess,**kw):
        from lino.textprinter.plain import PlainTextPrinter
        return PlainTextPrinter(self._stdout,**kw)
        

    def onShowForm(self,frm):
        #frm...
        self._forms.append(frm)

    def onRefreshForm(self,frm):
        self.onShowForm(frm)


    def beginResponse(self,title):
        doc = Page(title=title)
        self.response=doc
        self._forms=[]
        return doc

    def endResponse(self):
        s= str(self.response)
        self.response=None
        return s
    

    def showReport(self,sess,rpt):
        doc=self.response
        rpt.setupReport()
        table=html.TABLE(title=rpt.getTitle()); doc.append(table)

        tr=html.TR(); table.append(tr)
        for col in rpt.columns:
            tr.append(html.TH(col.getLabel()))

        for row in rpt:
            tr=html.TR() ; table.append(tr)
            for col in rpt.columns:
                v=col.getCellValue(row)
                if v is None:
                    tr.append(html.TD("&nbsp;"))
                else:
                    s=text2html(col.format(v).decode())
                    tr.append(html.TD(s))
    
        
