#coding: latin1

## Copyright 2003-2009 Luc Saffre 

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
from lino.console import syscon
from lino.console.exceptions import UserAborted

from lino.i18n import itr,_

itr("Are you sure you want to abort?",
    de="Arbeitsvorgang abbrechen?",
    fr="Interrompre le travail en cours?")


class Session:
    """A process capable to interact with the user.
    
    The user is usually a human sitting in front of a computer.
    A Session runs in a given Toolkit.

    Session is the base class for Application and for Task.

    """
    name=None

    def __init__(self,toolkit=None,**kw):
        #assert toolkit is not None
        if toolkit is None:
            toolkit=syscon.getSystemConsole()
        self.toolkit=toolkit
        #self.debug(self.__class__.__name__+".__init__()")

        self._connections = []
        self._databases = []
        
        self.configure(**kw)
    
    def configure(self):
        pass
        
    def buildMessage(self,msg,*args):
        if len(args) == 0:
            return msg
        return msg % args
    
    def isInteractive(self):
        return True
    def isDebug(self):
        return self.toolkit.isDebug()

    def confirm(self,*args,**kw):
        return self.toolkit.show_confirm(self,*args,**kw)
    def decide(self,*args,**kw):
        return self.toolkit.show_decide(self,*args,**kw)
    def message(self,*args,**kw):
        return self.toolkit.show_message(self,*args,**kw)
    def notice(self,*args,**kw):
        return self.toolkit.show_notice(self,*args,**kw)
    def debug(self,*args,**kw):
        return self.toolkit.show_debug(self,*args,**kw)
    def warning(self,*args,**kw):
        return self.toolkit.show_warning(self,*args,**kw)
    def verbose(self,*args,**kw):
        return self.toolkit.show_verbose(self,*args,**kw)
    def error(self,*args,**kw):
        return self.toolkit.show_error(self,*args,**kw)
    def exception(self,*args,**kw):
        print "session.py", args, kw
        return self.toolkit.showException(self,*args,**kw)

    def logmessage(self,*args,**kw):
        return self.toolkit.logmessage(self,*args,**kw)
    
    def showfile(self,filename):
        if self.isInteractive():
            os.system("start "+filename)
        else:
            assert os.path.exists(filename)
        
    def loop(self,func,label,maxval=0,*args,**kw):
        "run func with a Task or Progresser"
        if maxval == 0:
            task=Task(label)
        else:
            task=Progresser(label,maxval)
        task.toolkit=self.toolkit
        func(task,*args,**kw)
        #task.runfrom(self,*args,**kw)
        #task=Task(self,label,maxval)
        #task.loop(func,*args,**kw)
        return task

    def runtask(self,task,*args,**kw):
        # used by lino.scripts.sync.Sync.run()
        return task.runfrom(self.toolkit,*args,**kw)

    def showReport(self,*args,**kw):
        return self.toolkit.show_report(*args,**kw)
    def textprinter(self,*args,**kw):
        return self.toolkit.textprinter(self,*args,**kw)

    def breathe(self):
        return self.toolkit.on_breathe(self)
    
    def requestAbort(self):
        if self.confirm( _("Are you sure you want to abort?"),
                         default=False):
            raise UserAborted()
        #self._abortRequested=False
        self.toolkit.onTaskResume(self)
        #self._abortRequested=True

    def showForm(self,frm):
        return frm.show(self)
    


    def connection(self,*args,**kw):
        
        from lino.adamo.qtconn import Connection
        #from lino.adamo.dbds.firebird import Connection
        #from lino.adamo.dbds.sqlite_dbd import Connection
        #from lino.adamo.dbds.mysql_dbd import Connection
        #from lino.adamo.dbds.gadfly_dbd import Connection
        
##         try:
##             from lino.adamo.dbds.sqlite_dbd import Connection
##         except ImportError:
##             try:
##                 from lino.adamo.dbds.mysql_dbd import Connection
##             except ImportError:
##                 try:
##                     from lino.adamo.dbds.gadfly_dbd import Connection
##                 except ImportError:
##                     raise DatabaseError("no database driver available")

        conn = Connection(self,*args,**kw)
        self._connections.append(conn)
        #print conn
        return conn

    def database(self,schema,name=None,**kw):
        #if name is None:
        #    name = str(schema)+str(len(self._databases)+1)
        from lino.adamo.database import Database
        db = Database(schema,name=name,**kw)
        self._databases.append(db)
        return db

    def startDump(self):
        assert len(self._connections) == 1
        self._connections[0].startDump()
    def stopDump(self):
        assert len(self._connections) == 1
        return self._connections[0].stopDump()
    
    def peekDump(self):
        assert len(self._connections) == 1
        return self._connections[0].peekDump()
        

    def shutdown(self):
        # tests/adamo/7.py failed when several tests
        # were run (because previous startups remained open.
        #if self.ui is None:
        #    return
        #self.app.debug("Center.shutdown()")
##         for sch in self._schemas:
##             sch.shutdown(syscon)
##         self._schemas = []
        for db in self._databases:
            db.close()
        self._databases = []
        for conn in self._connections:
            conn.close()
        self._connections = []
