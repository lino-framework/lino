from twisted.web import static
import time
import os


d = '''\
<HTML>
<HEAD>
<TITLE>
twistd on asterix
</TITLE>
</HEAD>

<h1>Twisted web server on asterix</h1>

<UL>
''' 

for fname in os.listdir("../www"):
	if fname.endswith('.rpy'):
		d += '''<LI><a href="%s">%s</a></li>''' % (fname,fname)

d += '''\
</UL>
<hr noshade>
<p align="right">(generated %s</p>
</BODY></HTML>
''' % time.ctime()

resource = static.Data(d, 'text/html')
