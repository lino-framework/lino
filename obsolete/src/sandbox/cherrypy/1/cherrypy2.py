# coding: latin1

## Copyright 2005 Luc Saffre 

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

from cStringIO import StringIO
import cherrypy

from cherrypy.lib.cptools import PositionalParametersAware 



from lino.apps.pinboard import demo
#from lino.gendoc.gendoc import WriterDocument
from lino.gendoc.html import HtmlDocument
from lino.forms.base import MenuContainer

from HTMLgen import HTMLgen as html

from lino.console.htmlgen_toolkit import HtmlServer

if False:

    from Queue import Queue

    def DatabaseServerThread():

        def __init__(self):
            self.queue=Queue()

        def run_forever():
            while True:
                pass







# http://www.cherrypy.org/wiki/SQLObjectThreadPerConnection
# inspired by SQLObject.dbconnection.ConnectionHub:
#from util.threadinglocal import local as threading_local
class ConnectionHub(object):

    """
    This object serves as a hub for connections, so that you can pass
    in a ConnectionHub to a SQLObject subclass as though it was a
    connection, but actually bind a real database connection later.
    You can also bind connections on a per-thread basis.

    You must hang onto the original ConnectionHub instance, as you
    cannot retrieve it again from the class or instance.

    To use the hub, do something like::

        hub = ConnectionHub()
        class MyClass(SQLObject):
            _connection = hub

        hub.threadConnection = connectionFromURI('...')

    """

    def __init__(self):
        self.threadingLocal = threading_local()

    def __get__(self, obj, type=None):
        # I'm a little surprised we have to do this, but apparently
        # the object's private dictionary of attributes doesn't
        # override this descriptor.
        if obj and obj.__dict__.has_key('_connection'):
            return obj.__dict__['_connection']
        return self.getConnection()

    def __set__(self, obj, value):
        obj.__dict__['_connection'] = value

    def getConnection(self):
        try:
            return self.threadingLocal.connection
        except AttributeError:
            try:
                return self.processConnection
            except AttributeError:
                raise AttributeError(
                    "No connection has been defined for this thread "
                    "or process")

    def doInTransaction(self, func, *args, **kw):
        """
        This routine can be used to run a function in a transaction,
        rolling the transaction back if any exception is raised from
        that function, and committing otherwise.

        Use like::

            sqlhub.doInTransaction(process_request, os.environ)

        This will run ``process_request(os.environ)``.  The return
        value will be preserved.
        """
        # @@: In Python 2.5, something usable with with: should also
        # be added.
        old_conn = self.getConnection()
        conn = old_conn.transaction()
        self.threadConnection = conn
        try:
            try:
                value = func(*args, **kw)
            except:
                conn.rollback()
                raise
            else:
                conn.commit()
                return value
        finally:
            self.threadConnection = old_conn

    def _set_threadConnection(self, value):
        self.threadingLocal.connection = value

    def _get_threadConnection(self):
        return self.threadingLocal.connection

    def _del_threadConnection(self):
        del self.threadingLocal.connection

    threadConnection = property(_get_threadConnection,
                                _set_threadConnection,
                                _del_threadConnection) 












class MyRoot(MenuContainer,PositionalParametersAware):
    def __init__(self,dbsess):
        self.dbsess=dbsess
        self.beginResponse = dbsess.toolkit.beginResponse
        self.endResponse = dbsess.toolkit.endResponse
        
    def index(self):
        doc=self.beginResponse(title="index()")
        doc.append(html.Para("This is the top-level page"))
        return self.endResponse()
    index.exposed=True
    
##     def default(self, *args):
##         doc=self.beginResponse(title="default()")
##         doc.append(html.Para("This is the default page"))
##         #doc.h(1,doc.title)
##         doc.append(html.Para("args : %s" % repr(args)))
##         return self.endResponse()

##     default.exposed=True

    def report(self, *args,**kw):
        doc=self.beginResponse(title="report()")
        found=0
        if len(args) == 0:
            doc.append(html.Para("This is the report page"))
            doc.append(html.Para("args : " + repr(args)))
            doc.append(html.Para("kw : " + repr(kw)))
            doc.append(html.Para("dbsess : " + repr(self.dbsess)))
        else:
            for table in self.dbsess.db.app.getTableList():
                if table.getTableName() == args[0]:
                    self.dbsess.showViewGrid(table._instanceClass,
                                             *args[1:],**kw)
                    found+=1
                    doc.append(html.Para("dbsess : " + repr(self.dbsess)))
        doc.append(html.Para("found %d reports" % found))
        if found == 0:
            for table in self.dbsess.db.app.getTableList():
                doc.append(html.Para(table.getTableName()))
                    
                    
        return self.endResponse()

    report.exposed=True
    

from lino.console import syscon
syscon.setToolkit(HtmlServer())

if False:

    conn = ConnectionHub()

    def connect(threadIndex):
        "Function to create a connection at the start of the thread"
        conn.threadConnection = SQLiteConnection('test.db')

        # Tell cherrypy to run the connect() function when creating
        # threads
        cherrypy.server.onStartThreadList = [connect]

        
    
if __name__ == '__main__':

    
    sess = demo.startup()
    cherrypy.root = MyRoot(sess)

    settings = { 
        'global': {
            'server.socketPort' : 8080,
            'server.socketHost': "",
            'server.socketFile': "",
            'server.socketQueueSize': 5,
            'server.protocolVersion': "HTTP/1.0",
            'server.logToScreen': True,
            'server.logFile': "",
            'server.reverseDNS': False,
            'server.threadPool': 10,
            'server.environment': "development"
        },
        '/service/xmlrpc' : {
            'xmlRpcFilter.on': True
        },
        '/admin': {
            'sessionAuthenticateFilter.on' :True
        },
        '/css/default.css': {
            'staticFilter.on': True,
            'staticFilter.file': "data/css/default.css"
        }
        }
    cherrypy.config.update(settings)
    
    #cherrypy.config.update(file='tutorial.conf')
    cherrypy.server.start()
    sess.shutdown()

