class MemoParser:
   def __init__(self,doc):
      self.doc = doc

   def parse(self,txt):
      self.buf = ''
      self.p = 'p'
      self.newpara = False
      for line in txt.split('\n'):
         if len(line) == 0:
            self.newpara = True
         else:
            while True:
               pos = line.find('<')
               if pos == -1:
                  break
               elif pos > 0:
                  self.write(line[:pos])
                  line = line[pos:]

               pos = line.find('>')
               piece = line[:pos+1]
               tag = line[1:pos].lower()
               # print tag
               line = line[pos+1:]
               if tag == "ul":
                  self.flush()
                  self.doc.beginList()
                  self.p = 'p'
               elif tag == "ol":
                  self.flush()
                  self.doc.beginList()
                  self.p = 'p'
               elif tag == "/ol":
                  self.flush()
                  self.doc.endList()
                  self.p = 'p'
               elif tag == "/ul":
                  self.flush()
                  self.doc.endList()
                  self.p = 'p'
               elif tag == "li":
                  self.flush()
                  self.p = 'li'
               elif tag == "table":
                  self.flush()
                  self.doc.beginTable()
                  self.p = 'p'
               elif tag == "/table":
                  self.flush()
                  self.doc.endTable()
                  self.p = 'p'
               elif tag == "tr":
                  self.flush()
                  self.doc.beginRow()
                  self.p = 'p'
               elif tag == "/tr":
                  self.flush()
                  self.doc.endRow()
                  self.p = 'p'
               elif tag == "td":
                  self.flush()
                  self.doc.beginCell()
                  self.p = 'p'
               elif tag == "/td":
                  self.flush()
                  self.doc.endCell()
                  self.p = 'p'
               else:
                  renderText = self.doc.renderer.renderTag(tag)
                  if renderText == None:
                     self.write(piece)
                  else:
                     self.write(renderText)
         
         self.write(line + '\n')
      self.flush()

   def write(self,txt):
      if self.newpara:
         self.flush()
         self.newpara = False
      self.buf += txt

   def flush(self):
      if len(self.buf) > 0:
         p = getattr(self.doc,self.p)
         p(self.buf)
         self.buf = ''
      

def parseMemo(doc,txt):
   p = MemoParser(doc)
   p.parse(txt)
