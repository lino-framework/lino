import os

localRoot = ""
targetRoot = ""
SRC_ROOT = os.path.join(os.path.dirname(__file__),"..","..","..")
SRC_ROOT = os.path.abspath(SRC_ROOT)
print "SRC_ROOT =", SRC_ROOT

def fileref(filename):
	href = "../../"+filename
	return url(href,filename)
	
def url(url,label=None,title=None):
	if label is None:
		label = url
	if title is None:
		title = ""
	r= """

.. raw:: html

   <a href="%(url)s" title="%(title)s">%(label)s</a>
""" % locals()
	# print r
	return r
