import os
import BaseHTTPServer

NAME = ''
PORT = 8910
WEBDAV_ROOT = 'W:\\'

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  
    def do_GET(self):
        """Serve a GET request."""
        #~ print self.client_address, self.path
        #~ filename = "file://W:%s" % self.path
        parts = self.path.split('/')
        filename = os.path.join(WEBDAV_ROOT,*parts)
        if os.path.exists(filename):
            os.startfile(filename)
        else:
            self.log_message("File %r not found",filename)

httpd = BaseHTTPServer.HTTPServer((NAME,PORT), MyHandler)
print "serving at port", PORT
httpd.serve_forever()
