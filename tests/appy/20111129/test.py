r"""

If I repeat a paragraph using the following formula::

  do text for pp in properties_list()

and if `properties_list()` is a generator function, 
then appy.pod works only correctly 
if the generator function actually yields values.

The following test works:

>>> run_test(1,[
... Property("Computer","good"),
... Property("Singing","very good")])
[u'Computer', u'Singing']
Generated file result1.odt

If it is an empty generator
        
But the following expected result doesn't work:

>>> run_test(2,[])
[]
Generated file result1.odt

It gives the following traceback instead:

Traceback (most recent call last):
  File "test.py", line 44, in <module>
    run_test(2,[])
  File "test.py", line 33, in run_test
    renderer.run()
  File "l:\snapshots\appy-0.6.7\appy\pod\renderer.py", line 347, in run
    self.currentParser.parse(self.contentXml)
  File "l:\snapshots\appy-0.6.7\appy\shared\xml_parser.py", line 195, in parse
    self.parser.parse(inputSource)
  File "c:\Python27\lib\xml\sax\expatreader.py", line 107, in parse
    xmlreader.IncrementalParser.parse(self, source)
  File "c:\Python27\lib\xml\sax\xmlreader.py", line 123, in parse
    self.feed(buffer)
  File "c:\Python27\lib\xml\sax\expatreader.py", line 207, in feed
    self._parser.Parse(data, isFinal)
  File "c:\Python27\lib\xml\sax\expatreader.py", line 304, in end_element
    self._cont_handler.endElement(name)
  File "l:\snapshots\appy-0.6.7\appy\pod\pod_parser.py", line 279, in endElement
    e.currentBuffer.action.execute()
  File "l:\snapshots\appy-0.6.7\appy\pod\actions.py", line 76, in execute
    self.do()
  File "l:\snapshots\appy-0.6.7\appy\pod\actions.py", line 198, in do
    del context[self.iter]
KeyError: u'pp'

Tested also on 0.7.0

A workaround is to change the formula in the .odt template 
to wrap the iterator manually into `list`:

  do text for pp in list(properties_list())

Not urgent, but worth a closer look.

"""


import os
import os.path

from appy.pod.renderer import Renderer

class Property():
    def __init__(self,property,value):
      self.property = property
      self.value = value
    def __unicode__(self):
        return unicode(self.value)
 

def run_test(n,pp_list):
    tpl = os.path.join(os.path.abspath(os.path.dirname(__file__)),'cv.odt')
    def properties_list():
        for p in pp_list:
            yield p
    context = dict(properties_list=properties_list)

    print [unicode(pp.property) for pp in properties_list()]
      
    target = 'result%s.odt' % n
    if os.path.exists(target): 
        os.remove(target)
    renderer = Renderer(tpl, context, target)
    renderer.run()
    print "Generated file", target

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

