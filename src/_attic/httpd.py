#-------------------------------------------------------------------
# httpd.py
#           just copied from old lino. not finished.
#           
# Author:    Luc Saffre <luc.saffre@gmx.net>
# Copyright: (c) 2002 Luc Saffre
#-------------------------------------------------------------------

#from __future__ import nested_scopes

import BaseHTTPServer
import SocketServer
import Cookie
import urllib
import signal
import thread
import time

#import lino
#import parser

from job import *
from keyboard import *


"""

copied from MoinMoin : use of _abort, serve_in_thread() and signal to
make the server interruptible by Ctrl-C
  
"""


__head__ = """
<html>
<head>
<meta name="author" content="Name">
<meta name="description" content="Text">
<meta name="keywords" content="Wort, Wort, Wort">
<meta http-equiv="content-type"
      content="Mime-Type; charset=ISO-8859-1">
<style>
td { vertical-align:top;}
</style>
</head>
<body>
<table width="100%">
<tr>
<td width="20%" valign="top">
[! frame.menubar.HtmlRender(out,self.path)]
<td width="60%" valign="top">
[! frame.HtmlRender(out)]
<td>
client_address: [%s repr(self.client_address)]
<br>session : [%d id(self.session)]
</tr>
</table>
</body>
</html>
"""
    



__loginform__ = """
<form action="[%s self.host]" method="POST" enctype="text/html">
<fieldset>
<legend>Login</legend>
<p>Username:
<input type="text" size="8" maxlength="8" name="username">
<p>Password:
<input type="password" size="8" name="password">
<p>
<input type="button" name="Send" value="Login" onClick="Aktion"> 
</fieldset> 
</form>
""" 





# list of all open frames
# framelist = {} # dict of id() => frame
sessionlist = {} # dict of id() => frame
        
#mainframe = None

#def Initialize():
#   global mainframe

class LinoServer(BaseHTTPServer.HTTPServer):
    def __init__(self, server_address):
        BaseHTTPServer.HTTPServer.__init__(self,
                                           server_address,
                                           LinoRequestHandler)

        self._abort = 0
        
        # register signal handler
        signal.signal(signal.SIGABRT, self.quit)
        signal.signal(signal.SIGINT,  self.quit)
        signal.signal(signal.SIGTERM, self.quit)


    def server_bind(self):
        SocketServer.TCPServer.server_bind(self)
        
        # LS: I don't understand why BaseHTTPServer implements this
        # strange behaviour:
        
        # host, port = self.socket.getsockname()
        # self.server_name = socket.getfqdn(host)
        # self.server_port = port
        
        # perhaps these two variables are needed?
        self.server_name = self.server_address[0]
        self.server_port = self.server_address[1]
    
 
    def serve_in_thread(self):
        """Start the main serving loop in its own thread."""
        thread.start_new_thread(self.serve_forever, ())

    def serve_forever(self):
        """Handle one request at a time until we die."""
        sys.stderr.write("LinoServer on %s:%d\n" %
                         (self.server_address))
        while not self._abort:
            self.handle_request()

    def die(self):
        """Abort this server instance's serving loop."""
        self._abort = 1

        # make request to self so server wakes up
        import httplib
        req = httplib.HTTP('%s:%d' % self.server_address)
        req.connect()
        req.putrequest('DIE', '/')
        req.endheaders()
        del req

    def quit(self,signo, stackframe):
       """Signal handler for aborting signals."""
       print "Interrupted! %s, %s" % (repr(signo),repr(stackframe))
       self.die()
       ##sys.exit(0)
  

# copied from cookbook/python/http/server1.py
# modified to suit my needs
def urlParse(url):
    """ return path as list and query string as dictionary
        strip / from path
        ignore empty values in query string
        for example:
            if url is: /xyz?a1=&a2=0%3A1
            then result is: (['xyz'], { 'a2' : '0:1' } )
            if url is: /a/b/c/
            then result is: (['a', 'b', 'c'], None )
            if url is: /?
            then result is: ([], {} )
    """
    x = url.split('?')
    pathlist = filter(None, x[0].split('/'))
    d = {}
    if len(x) > 1:
        for kv in x:
            y = kv.split('=')
            k = y[0]
            try:
                v = urllib.unquote_plus(y[1])
                if v:               # ignore empty values
                    d[k] = v
            except:
                pass
    print "url = %s" % repr(url)
    print "pathlist = %s" % repr(pathlist)
    print "d = %s" % repr(d)
    
    return (pathlist, d)

class Session:
   def __init__(self)
   pass

class LinoRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
   
   cookie = Cookie.SimpleCookie()

   def version_string(self):
      return lino.version_string()

   def do_GET(self):
      """
      Serve a GET request.
      http://localhost/demo&frame=123456&action=2
      """

      #print self.path
      #print "<HEADERS>"
      #print self.headers
      #print "</HEADERS>"

      # print self.headers["Cookie"]
      self.cookie = Cookie.SimpleCookie()
      
      self.cookie["Session"] = None
      # self.cookie["Frame"].max_age = 60
      # self.cookie["User"] = None
      print "headers = %s" % repr(self.headers)
      try:
         c = self.headers["Cookie"]
      except KeyError:
         pass
      else:
         self.cookie.load(c)
         
      # print "cookie:"
      # print self.cookie

      self.session = None
      sessid = self.cookie["Session"].value
      
      #print "frameid : %s"  % repr(frameid)
      #print "%d active sessions:" % len(sessionlist)
      #for k,v in sessionlist.items():
      #   print "%s => %s" % (repr(k),repr(v))

      try:
         i = int(sessid)
      except ValueError:
         # sessid = None
         print "sessid %s : ignored. Not integer" % repr(sessid)
         self.session = Session()
         sessionlist[id(self.session)] = self.session
         self.cookie["Session"] = id(self.session)
      else:
         try:
            self.session = sessionlist[i]
         except KeyError, e:
            print "%d : invalid session specified" % i
            # print "KeyError: %s", e
            #self.send_error(400,"invalid frame specified")
            #return
         
      
      #if self.cookie["User"] == None:
      #   self.send_login()
      #   return

      # C["Lino.Session"] = None
      #self.send_header(C.output())
      
      (pathlist,d) = urlParse(self.path)


      
      # a = self.path.split("/")
      # a[0] is always empty since path starts always with "/"
      if len(pathlist) == 0:
         s = "you must specify an area"
         self.send_error(401,s)
         return
         
      self.area = pathlist[0]
      if self.area != "demo":
         s = "%s : unknown area" % repr(pathlist)
         self.send_error(401,s)
         return

      warnings = ""

      frame = lino.app.mainframe
      
      for actionName in pathlist[1:]:
         a = getattr(frame,actionName)
         frame = a.Execute()
         if frame:
            if len(frame.warnings) > 0:
               warnings += frame.warnings
         else:
            warnings += "<br>no frame returned" 

      if frame:
         self.send_frame(frame)
         return
      
      self.send_error(400,"")

   def send_frame(self,frame):
      """Send a HTTP response."""
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.wfile.write(self.cookie.output())
      # print "HTTP send: %s" % self.req.cookie.output()
      self.end_headers()
      
      p = parser.StreamParser(self.wfile,globals(),locals())
      
      p.parse(__head__)
      # frame.HtmlRender(self.wfile)
      # p.parse(__foot__) #,self.wfile))
      
      
               

   def do_HEAD(self):
      """Serve a HEAD request."""
      if 1:
          raise "What's a HEAD request?"
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()

        # self.send_error(404, "File not found")


class Application:

   def __init__(self):
      self.mainframe = MainFrame(_("Main Menu"))
      addr = ('localhost', 8888)
      self.server = LinoServer( addr )

   def run(self):      

      if sys.platform == 'win32':
         # run threaded server
         self.server.serve_in_thread()
         
         # main thread accepts signal
         i = 0
         while not self.server._abort:
            i += 1
            print "\|/-"[i%4], "\r",
            time.sleep(1)
      else:
         # not tested
         # if run as root, change to configured user
         httpd_user = None
         if os.getuid() == 0:
            if not httpd_user:
               print "Won't run as root. " \
                     + "Set the httpd_user config variable!"
               sys.exit(1)
            
         import pwd
         try:
            pwentry = pwd.getpwnam(httpd_user)
         except KeyError:
            print "Can't find httpd_user '%s'!" % (httpd_user,)
            sys.exit(1)

         uid = pwentry[2]
         os.setreuid(uid, uid)

         self.server.serve_forever() 
