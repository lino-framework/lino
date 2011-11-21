#!/usr/bin/env python
import os
import asyncore

from quixote.server.medusa_http import QuixoteHandler
from quixote.publish import SessionPublisher
from medusa import http_server, xmlrpc_handler

__revision__ = "$Id: serve.py,v 1.3 2003/11/20 15:16:51 lsaffre Exp $"

# A simple HTTP server, using Medusa, that publishes a Quixote application.

# import rfc822, socket
#from StringIO import StringIO
#from quixote.http_request import HTTPRequest
#from quixote.errors import PublishError

timeout = 10 # timeout for main loop in seconds

def startServer (namespace,servername,configPath=None):
	if configPath is None:
		configPath = os.path.dirname(namespace.__file__)
	print "config path is %s" % configPath
	print 'Now serving %s on port 8080' % servername
	server = http_server.http_server('', 8080)
	publisher = SessionPublisher(namespace)
		
	try:
		publisher.read_config(os.path.join(configPath,"default.conf"))
	except IOError,e:
		print e
		return
	
	publisher.setup_logs()
	dh = QuixoteHandler(publisher, servername, server)
	server.install_handler(dh)
	asyncore.loop(timeout)

#def main(db):

## def cli():	

## if __name__ == '__main__':
## 	cli()

