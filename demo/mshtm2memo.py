import sys
from lino.htgen import Document
if len(sys.argv) != 2:
        print "input filename required"
        exit(-1)
s=open(sys.argv[1],"r").read().decode("latin1")
d=Document()
d.memo(s)
print d.toxml().encode('ascii', 'xmlcharrefreplace')


