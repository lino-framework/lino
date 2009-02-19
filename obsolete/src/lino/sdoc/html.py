import os, types
from lino.sdoc.document import Document
from lino.sdoc.renderer import Renderer
from lino.sdoc.tables import TableInstance, TableRow
from lino.sdoc.lists import ListInstance
from lino.sdoc.environment import Body


HTML_BEGIN = """
  <html>
  <head>
  <title>%s</title>
  <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
  <link rel=stylesheet type="text/css" href="www.css">
  <meta name="KEYWORDS" content="">
  <meta name="GENERATOR" content="pds2html">
  <meta name="author" content="">
  <meta name="date" content="%s">
  <head>

  <body>

  <table class="main">
  <tr>
  <td class="left" width="15%%">

  this is the left margin

  <td>


"""
HTML_END = """
  </td>
  </tr>
  </table>

  here comes the bottom line

  </body>
  </html>
"""


class HtmlRenderer(Renderer):
   
   outputExt = 'html'

   def onBeginDocument(self,doc):
      self._sdoc = doc
      self.fd = file(self.getFilename(),"w")
      self.fd.write(HTML_BEGIN % (doc.getTitle(),'yyyy-mm-dd'))
      
   def onEndDocument(self,doc):
      self.fd.write(HTML_END)
      del self._sdoc
      self.fd.close()
      
   def onBeginEnvironment(self,e):
      if isinstance(e,Body):
         pass # raise 'allowed only once'
      elif isinstance(e,TableInstance):
         p = e.getParent()
         p.toStory('<table border="1">')
         p.toStory('<tr>')
         for col in e.model.columns:
            if col.label is None:
               p.toStory('<th></th>')
            else:
               p.toStory('<th>%s</th>'%col.label)
         p.toStory('</tr>')
      elif isinstance(e,TableRow):
         pass
      elif isinstance(e,ListInstance):
         e.getParent().toStory('<UL>')
      #elif isinstance(e,ListItem):
      #   if e.bulletText is None:
      #      return '<LI>'
      #   else:
      #      return '<LI value="%s">' % e.bulletText
      #elif isinstance(e,BarcodeFlowable):
      #   return
      else:
         raise '%s : unknown environment' % repr(e)

   def onEndEnvironment(self,e):
      
      if isinstance(e,Body):
         pass
         # self.render(e.getStory())
         # raise 'allowed only once'
         # return e.getStory()
      elif isinstance(e,TableInstance):
         e.getParent().toStory("</table>")
      elif isinstance(e,TableRow):
         p = e.getParent().getParent()
         p.toStory('<tr>')
         for cell in e.cells:
            p.toStory('<td>')
            p.toStory(cell)
            p.toStory('</td>')
         p.toStory('</tr>')
      elif isinstance(e,ListInstance):
         e.getParent().toStory('</UL>')
         #p = e.getParent()
         #p.toStory('<UL>')
         #for item in e.items:
         #   p.toStory('<li>')
         #   p.toStory(item)
         #   p.toStory('</li>')
         #p.toStory('</UL>')
      #elif isinstance(e,ListItem):
      #   return '</LI>'
      else:
         raise '%s : unknown environment' % repr(e)

   def render(self,story):
      if type(story) is types.StringType:
         self.fd.write(story + '\n')
      else:
         for elem in story:
            # print repr(elem)
            self.fd.write(elem + '\n')

         
   def getPageNumber(self):
      return 1
   

   def compilePara(self,txt,style):
      if style.getName() == "Heading1":
         return "<H1>%s</H1>" % txt
      if style.getName() == "Heading2":
         return "<H2>%s</H2>" % txt
      if style.wrap:
         return "<p>%s</p>" % txt
      return """<pre>%s</pre>""" % txt
         
   def compileListItem(self,txt,style,bulletText):
      if bulletText is None:
         return self.compilePara(txt,style)
      return '<li value="' \
             + bulletText \
             + '">' + txt + '</li>'
      
   def compileBarcode(self,barCodeSymbol,style):
      return('<p>[%s]</p>' % barCodeSymbol.ean13.s)

   def compileBackgroundPainter(self,func):
      return ''
	
   def writeTable(self,tableInstance):
      write = self.fd.write
      for row in tableInstance.rows:
         write("<tr>\n")
         for cell in row:
            write('<td>\n')
            for elem in cell:
               self.writeElement(elem)
            write("\n</td>\n")
         write("</tr>\n")


   def writeList(self,listInstance):
      write = self.fd.write
      write('<ol>\n')
      for i in listInstance.getItems():
         write("<li>\n")
         for elem in i.elems:
            self.writeElement(elem)
         write("</li>\n")
      write("</ol>\n")

   def renderTag(self,tag):
      return None

##    def setTitle(self,title):
##       "Sets the document title. Does not print it."
##       self.title = title
      
##    def getTitle(self):
##       "Returns the document title."
##       return self.title


