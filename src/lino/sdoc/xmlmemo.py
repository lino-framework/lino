#not used. Memos are in fact not valid XML so that i prefer to write
#my own little parser for them...

from xml.sax import ContentHandler, ErrorHandler, parseString
from xml.sax._exceptions import SAXParseException

class MemoHandler(ContentHandler):
   def __init__(self,doc):
      self.doc = doc
      self._txt = ""
      self.feature_validation = False
      self.p = "p"


   def endDocument(self):
      self.flush()
      
   def startElement(self, name, attrs):
      self.flush()
      if name == 'ol':
         self.doc.beginList()
      elif name == 'ul':
         self.doc.beginList()
      elif name == 'li':
         self.p = "li"
      
   def endElement(self, name):
      self.p = "p"
      if name == 'ol':
         self.doc.endList()
      elif name == 'ul':
         self.doc.endList()
      elif name == 'li':
         self.doc.li(self._txt)
         self._txt = ""

   def flush(self):
      if len(self._txt) > 0:
         p = getattr(self.doc,self.p)
         p(self._txt)
         self._txt = ""
         
   def characters(self,txt):
      self._txt += str(txt)

class MemoErrorHandler(ErrorHandler):
   def error(self,e):
      print "Ignoring: " + str(e)
      
eh = MemoErrorHandler()


def parseMemo1(doc,txt):
    h = MemoHandler(doc)
    #try:
    parseString(txt,h,eh)
    #except SAXParseException, e:
    #   print "Note: " + str(e)

