"""
to run this script:: 
  twistd -ny nevow_webserver.py
"""
from twisted.web import static
from twisted.application import service, internet
from nevow import appserver

root = static.File('../www')
#root = '../www'
application = service.Application('LucsTwistedApp')
site = appserver.NevowSite(root)
webServer = internet.TCPServer(8080, site)
webServer.setServiceParent(application) 

