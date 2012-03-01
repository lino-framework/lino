import os
from xml.dom import minidom 

def elements(node):
    e = node.firstChild
    while e is not None:
        if e.nodeType == minidom.Node.ELEMENT_NODE:
            yield e
        e = e.nextSibling

def xsd2xg(fn,nsname):
    dom = minidom.parse(fn) 
    yield "from lino.utils import xmlgen as xg"
    yield "class %s(xg.Namespace):" % nsname
    yield "  url = %r" % str(dom.documentElement.attributes.get('targetNamespace').value)
    #~ e = dom.documentElement.firstChild
    #~ while e is not None:
    indent = '  '
    for e in elements(dom.documentElement):
        if e.tagName == 'xsd:complexType':
            na = e.attributes.get('name',None)
            if na is None:
                yield indent + "# skipped nameless %s" % e.tagName
                continue
            yield indent + "# %s" % e.tagName
            yield indent + "class %s(xg.Container):" % na.value
            for ee in elements(e):
                #~ seq = e.getElementsByTagName('xsd:sequence')[0]
                if ee.tagName == 'xsd:sequence':
                    #~ seq = e.attributes.get('sequence',None)
                    #~ if seq:
                    for item in elements(ee):
                        na = item.attributes.get('name',None)
                        if na is None: continue
                        ta = item.attributes.get('type',None)
                        if ta is None:
                            yield indent*2 + "class %s(): pass" % na.value
                        else:
                            if ':' in ta.value:
                                typename = ta.value.replace(':','.')
                            else:
                                typename = nsname + '.' + ta.value
                            yield indent*2 + "class %s(%s): pass" % (na.value,typename)
        elif e.tagName == 'xsd:simpleType':
            na = e.attributes.get('name',None)
            if na is None:
                yield indent + "# skipped nameless %s" % e.tagName
                continue
            yield indent + "# %s" % e.tagName
            yield indent + "class %s(xg.Container):" % na.value
        else:
            yield indent + "# unhandled element %s" % e.tagName
    #~ e = e.nextSibling


fn = os.path.join('XSD','RetrieveTIGroupsV3.xsd')
#~ for i,ln in enumerate(text_lines(dom)):
for ln in xsd2xg(fn,'tx25'):
    #~ print "%d:%s" % (i,ln)
    print ln
    