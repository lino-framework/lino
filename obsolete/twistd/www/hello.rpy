from twisted.web import static
import time

now = time.ctime()

d = '''\
<HTML><HEAD><TITLE>hello.rpy</TITLE>

<H1>Hello World, It is Now %(now)s</H1>

<UL>
''' % vars()

for i in range(10):
    d += "<LI>%(i)s" % vars()

d += '''\
</UL>
</BODY></HTML>
'''

resource = static.Data(d, 'text/html')
