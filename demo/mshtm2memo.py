from lino.htgen import Document
s=open("tmp.htm","r").read().decode("latin1")
d=Document()
d.memo(s)
print d.toxml().encode('ascii', 'xmlcharrefreplace')


