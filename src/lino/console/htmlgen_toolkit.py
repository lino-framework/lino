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

import os
import sys
import time

from cStringIO import StringIO


#from lino.forms.base import AbstractToolkit
from lino.forms.base import Toolkit



## from HTMLgen import HTMLgen as html
## def Page(title):
##     doc = html.SimpleDocument(title=title)
##     doc.append(html.Heading(1,doc.title))
##     p = html.Para("Menu:")
##     p.append(html.BR())
##     p.append(html.Href(url="/",text="home"))
##     p.append(html.BR())
##     p.append(html.Href(url="foo/bar/baz",text="foo"))
##     p.append(html.BR())
##     p.append(html.Href(url="report",text="report"))
##     doc.append(p)
##     doc.append(html.HR())

##     return doc

from HyperText.Documents import Document
from HyperText import HTML as html
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
            
class HtmlServer(Toolkit):

    def __init__(self,*args,**kw):
        self.response=None
        Toolkit.__init__(self,*args,**kw)


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
        
    def beginResponse(self,title):
        doc = Page(title=title)
        self.response=doc
        return doc

    def endResponse(self):
        s= str(self.response)
        self.response=None
        return s
    

    def showReport(self,sess,rpt,*args,**kw):
        from lino.gendoc.plain import PlainDocument
        fd=StringIO()
        gd = PlainDocument(writer=fd.write)
        gd.beginDocument()
        gd.report(rpt)
        gd.endDocument()
        s=fd.getvalue()
        self.response.append(html.PRE(s))
    

    def showForm(self,frm):
        from lino.gendoc.plain import PlainDocument
        #gd = PlainDocument()
        gd = PlainDocument(writer=self._stdout)
        gd.beginDocument()
        gd.form(frm)
        gd.endDocument()

    def refreshForm(self,frm):
        self.showForm(frm)


