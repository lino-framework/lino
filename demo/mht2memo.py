"""
Parse a .mht file as created by MS Word when clicking "File / Save as" 
and "Single file Web page". 
Print a simplified HTML version of the content of this file.

"""
import sys
import os.path
import email
from lino.htgen import Document
if len(sys.argv) != 2:
        print "input filename required"
        exit(-1)
filename=sys.argv[1]
basename,ext=os.path.splitext(filename)
d=Document()
if ext.lower() == ".mht":
  msg=email.message_from_file(open(filename,"r"))
  for part in msg.walk():
    if part.get_content_type() == "text/html":
      #print part.get_payload()
      d.load_html(part.get_payload(decode=True))
else:      
  d.load_html(open(filename,"r").read())
    
# d.toxml() would also print <HTML> and <HEAD> and <BODY> tags,
# d.body.toxml() would also print <BODY> and </BODY> tags,
# but I want only the text between <BODY> and </BODY>
for p in d.body.content:
  print p.toxml().encode('ascii', 'xmlcharrefreplace')


