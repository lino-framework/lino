#!/usr/bin/python
import os
import cgi
import datetime
#import cgitb
# cgitb.enable()
# print "Content-Type: text/html"     # HTML is following
print "Content-Type: text/plain"
print                               # blank line, end of headers
# print "<TITLE>getip.py</TITLE>"
# print "<body>"
# print "<H1>This is my first CGI script</H1>"
# print "Hello, world!"

#~ cgi.print_environ_usage()
#~ cgi.print_environ()
# cgi.test()

f = file('/var/log/getip/getip.log', 'w')

#form = cgi.FieldStorage()
now = datetime.datetime.now()
q = cgi.parse()
# print repr(q)
#name = form['name'].getvalue()
name = q['name'][0]
if name:
    msg = "%s - %s IP address is %s" % (now,
                                        name, os.environ.get('REMOTE_ADDR', None))
    f.write(msg)
    # print msg
    print os.environ.get('REMOTE_ADDR', None)
else:
    f.write("%s - invalid request:\n" % now)
    for kv in os.environ.items():
        f.write("  %s = %s\n" % kv)
    print "Sorry"

f.close()
# print "</body>"
