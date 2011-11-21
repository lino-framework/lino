#coding: latin1
"""
Starts the web server who serves the content at
http://lsaffre.dyndns.org:8080

"""

from optparse import OptionParser
import sys, getopt, os

from lino import copyleft
from lino.adamo.dbds.sqlite_dbd import Connection
from lino.adamo import center

#from lino.adamo.twisted_ui import WebServer
from lino.schemas.sprl.sprl import Schema
from lino.twisted_ui import sprlwidgets

from lino.adamo.database import Database
from lino.misc.my_import import my_import

from lino.twisted_ui.server import ServerResource, MyRequest

if os.name == 'nt':
    wwwRoot = r'u:\htdocs\timwebs'
    dbRoot = r'u:\tim2lino'
else:
    wwwRoot = '/mnt/wwwroot/timwebs'
    dbRoot = '/mnt/dbroot'
    #wwwRoot = '/var/lino/wwwroot'
    #dbRoot = '/var/lino/dbroot'
    
class DBinfo:
    def __init__(self,name,label,langs,dbfile,staticDirs):
        self.name = name
        self.langs = langs
        self.label = label
        self.dbfile = dbfile
        self.staticDirs = staticDirs


def TIMtree(root):
    return {
        'files': root ,
        'images': os.path.join(root,'images') ,
        #'thumbnails': os.path.join(root,'thumbnails') ,
        }


dbinfos = []

dbinfos.append(DBinfo(
    'luc',
    label="Lucs Heimatseite",
    langs='de en fr et',
    dbfile = os.path.join(dbRoot,'luc.db'),
    staticDirs = TIMtree(os.path.join(wwwRoot,'luc'))))

dbinfos.append(DBinfo(
    'tim',
    label="Die TIM-Webseite",
    langs='de en',
    dbfile = os.path.join(dbRoot,'tim.db'),
    staticDirs = TIMtree(os.path.join(wwwRoot,'tim'))))

dbinfos.append(DBinfo(
    'lino',
    label="The Lino Project",   
    langs='en',
    dbfile = os.path.join(dbRoot,'comp.db'),
    staticDirs = TIMtree(os.path.join(wwwRoot,'comp'))))


def main(argv):

    parser = OptionParser()
    parser.add_option("-v", "--verbose",
                            help="display many messages",
                            action="store_true",
                            dest="verbose",
                            default=True)
    parser.add_option("-s", "--skip-dbcheck",
                            help="skip integrity check of foreign databases",
                            action="store_true",
                            dest="skipTest",
                            default=False)
    parser.add_option("-p", "--port",
                            help="alternate PORT where to listen"
                            "(default is 8080)",
                            action="store",
                            dest="port",
                            type="int",
                            default=8080,
                            )

    (options, args) = parser.parse_args(argv)
    del args[0] 
    
    demoDir = os.path.dirname(__file__)
    
    #center.start(verbose=options.verbose)

    #info = center.getSystemConsole().info
    from lino.ui.console import info, progress

    #progress = app.console.progress
    
    schema = Schema(big=False) 
    
    schema.startup()
    schema.setLayout(sprlwidgets)

    serverRsc = ServerResource(wwwRoot)

    #sess = ConsoleSession()
    sess = center.createSession()

    if True:
        """
        Shared tables are the same for each database
        """

        info("Starting std.db...")
        conn = Connection(schema=schema)
        stddb = Database(langs="en de fr et",
                         schema=schema,
                         name="std",
                         label="shared standard data")

        sharedTables = (Languages, Nations, 
                        PartnerTypes, Currencies,
                        AuthorEventTypes,
                        PublicationTypes,
                        ProjectStati, Users) 

        stddb.connect(conn,sharedTables)
        
##         stddb.createTables()
##         sess.use(stddb)

##         from lino.schemas.sprl.data import std
##         std.populate(sess,big=False)
        #sess.end()

        
    for dbi in dbinfos:
        if len(args) == 0 or dbi.name in args:
            info("Opening %s..." % dbi.name)

            db = Database(
                langs=dbi.langs,
                schema=schema,
                name=dbi.name,
                label=dbi.label)
            
            conn = Connection(filename=dbi.dbfile,
                              schema=schema)

            db.update(stddb)
            db.connect(conn)

##             sess.use(db)
            serverRsc.addDatabase(db, stylesheet="www.css")

    sess = center.startup(checkIntegrity=not options.skipTest)
##     if not options.skipTest:
##         db.checkIntegrity(sess)


    if True:

        sys.path.insert(0,demoDir)

        #for modName in ('vor', 'etc'):
        for modName in ('etc',):

            info("Opening %s..." % modName)

            mod = __import__(modName) # my_import(modName)

            #print "%s (%s)" % (modName,mod.label)

            conn = Connection(filename=modName+'.db',
                                    isTemporary=True,
                                    schema=schema)
            db = Database( langs='en de',
                              schema=schema,
                              name=modName,
                              label=mod.label)

            db.startup(conn)
            db.createTables()
            
            sess.use(db)
            mod.populate(sess)

            serverRsc.addDatabase(db)
##          , staticDirs = {
##              'files': os.path.join(demoDir,modName,'files'),
##              'images': os.path.join(demoDir,modName,'images'),
##              #'thumbnails': os.path.join(demoDir,modName,'thumbnails')
##              })

            #db.flush()

        del sys.path[0]


    progress("Twisted Lino Server")
    progress(copyleft(year='2004',author='Luc Saffre'))
        

    from twisted.web import server
    from twisted.internet import reactor

    site = server.Site(serverRsc)
    site.requestFactory = MyRequest
    reactor.listenTCP(options.port, site)
    reactor.addSystemEventTrigger("before","shutdown", \
                                  center.shutdown)

            
    progress("Serving on port %s." % options.port)
    progress("(Press Ctrl-C to stop serving)")
            
    reactor.run()

    
    



    
if __name__ == '__main__':
    main(sys.argv)
