import os
#~ from xml.dom import minidom
from lxml import etree


XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
XHTML = "{%s}" % XHTML_NAMESPACE

XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"
XSD = "{%s}" % XSD_NAMESPACE

#~ NSMAP = {None : XHTML_NAMESPACE} # the default namespace (no prefix)
NSMAP = dict(xsd=XSD_NAMESPACE)


def xsd2xg(fn,nsname):
    tree = etree.parse(fn) 
    root = tree.getroot()
    yield "from lino.utils import xmlgen as xg"
    yield "class %s(xg.Namespace):" % nsname
    yield "  url = %r" % str(root.get('targetNamespace'))
    indent = '  '
    for e in root:
        if e.tag == XSD + 'complexType':
            na = e.get('name',None)
            if na is None:
                yield indent + "# skipped nameless %s" % e.tag
                continue
            yield indent + "# %s" % e.tag
            yield indent + "class %s(xg.Container):" % na
            for ee in e:
                #~ seq = e.getElementsByTagName('xsd:sequence')[0]
                if ee.tag == XSD + 'sequence':
                    #~ seq = e.attributes.get('sequence',None)
                    #~ if seq:
                    for item in ee:
                        na = item.get('name',None)
                        if na is None: continue
                        ta = item.get('type',None)
                        if ta is None:
                            yield indent*2 + "class %s(): pass" % na
                        else:
                            if ':' in ta:
                                typename = ta.replace(':','.')
                            else:
                                typename = nsname + '.' + ta
                            yield indent*2 + "class %s(%s): pass" % (na,typename)
        elif e.tag == XSD + 'simpleType':
            na = e.get('name',None)
            if na is None:
                yield indent + "# skipped nameless %s" % e.tag
                continue
            yield indent + "# %s" % e.tag
            yield indent + "class %s(xg.Container):" % na
        else:
            yield indent + "# unhandled element %s" % e.tag


fn = os.path.join('XSD','RetrieveTIGroupsV3.xsd')
for ln in xsd2xg(fn,'tx25'):
    print ln
    