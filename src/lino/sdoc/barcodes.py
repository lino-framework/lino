"""
these classes are for use by PdfRenderer (defined in pdf.py)

"""
from reportlab.platypus.flowables import Flowable
from reportlab.lib import colors 
from reportlab.lib.units import inch, mm

import bookland
"""
barCodeSymbol.moduleHeight


"""

class Bar:
    def __init__(self,bit,long=False):
        self.bit = bit
        self.long = long
        self.width = 1      # thickness in modules
        
    def inc(self):
        self.width += 1

    def draw(self,canvas,barCodeSymbol,x):
       if self.bit == "0":
          return
       canvas.setLineWidth(self.width*barCodeSymbol.moduleWidth*inch)
       #canvas.setFillColor(self.fillcolor)
       canvas.setStrokeColor(colors.black)
       top = barCodeSymbol.moduleHeight * inch
       bottom = 12
       if self.bit == "L":
          bottom -= 6
       # x = x * barCodeSymbol.moduleWidth
       canvas.line(x,bottom,x,top)
       
       

class BarcodeFlowable(Flowable):
   '''A barcode symbol as flowable. Works only with EAN13.'''
   def __init__(self, barCodeSymbol):
      Flowable.__init__(self)
      assert hasattr(barCodeSymbol,'font')
      "name of font to use for printing human-readable text"
      
      assert hasattr(barCodeSymbol,'bits')
      
      """string of 0,1 and L characters. each character stands for one
      "bit" or "module". 0 means white, 1 means black, L means long
      black"""
      
      
      assert hasattr(barCodeSymbol,'moduleHeight')
      "module height in points"
      assert hasattr(barCodeSymbol,'patternWidth')
      "width in inch"
      
      self.lightMargin = 9 * barCodeSymbol.moduleWidth * inch
      self.barCodeSymbol = barCodeSymbol
      self.width = self.barCodeSymbol.patternWidth * inch \
                   + self.lightMargin * 2
      self.height = self.barCodeSymbol.moduleHeight * inch
      #self.vAlign = "TOP"
      #self.hAlign="LEFT"
      #self.leftIndent=0
      
##    def wrap(self, *args):
##       # print "x = ", self.size[0] / mm
##       # print "y = ", self.size[1] / mm
##       # print self.barCodeSymbol.bits
##       return self.size
   
   def draw(self):
      canvas = self.canv
      # print canvas.pagesize
      #canvas.setLineWidth(6)
      #canvas.setFillColor(self.fillcolor)
      #canvas.setStrokeColor(self.strokecolor)
      #canvas.translate(self.xoffset+self.size,0)
      #canvas.rotate(90)
      #canvas.scale(self.scale, self.scale)
      #hand(canvas, debug=0, fill=1)
      bars = []
      bar=Bar(self.barCodeSymbol.bits[0])
      for bit in self.barCodeSymbol.bits[1:]:
         if bit==bar.bit:
            bar.inc()
         else:
            bars.append(bar)
            bar=Bar(bit)
      bars.append(bar)
      textHeight = 6
      textMargin = 5
      x = self.lightMargin + 1
      for bar in bars:
         bar.draw(canvas,self.barCodeSymbol,x)
         x += bar.width * self.barCodeSymbol.moduleWidth * inch

      # canvas.setFont(self.barCodeSymbol.font,12)
      # canvas.setFont("OCR-B",12)
      canvas.setFont("Helvetica",11)

      canvas.drawString(0,0 ,
                        self.barCodeSymbol.ean13.n[0])
      canvas.drawString(self.lightMargin+textMargin,0 ,
                        self.barCodeSymbol.ean13.n[1:7])
      canvas.drawString(self.lightMargin+textMargin
                        +6*7*self.barCodeSymbol.moduleWidth*inch
                        +3,0 ,
                        self.barCodeSymbol.ean13.n[7:])

      canvas.setLineWidth(0.0001)
      # canvas.rect(0,0,self.width,self.height)
