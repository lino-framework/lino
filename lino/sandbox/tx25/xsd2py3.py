import os
#~ from xml.dom import minidom
from lxml import etree


XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"
XSD = "{%s}" % XSD_NAMESPACE

NSMAP = dict(xsd=XSD_NAMESPACE)


def xsd2py(fn,nsname):
    tree = etree.parse(fn) 
    root = tree.getroot()
    yield "from lino.utils.bcss import Namespace"
    yield "%s = Namespace(%r,%r):" % (nsname,nsname,str(root.get('targetNamespace'))
    for e in root:
        if e.tag == XSD + 'complexType':
            na = e.get('name',None)
            if na is None:
                yield indent + "# skipped nameless %s" % e.tag
                continue
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
for ln in xsd2py(fn,'tx25'):
    print ln
    