import sys
from bookland import psfile, EAN13, EAN13Symbol,BooklandError

ISBNFONT = "OCRB"      #  Doesn't have to be OCR-B
EAN13FONT = "OCRB"
UPC5FONT = "OCRB"

ean13font=EAN13FONT
isbnfont=ISBNFONT
upc5font = UPC5FONT

zone=None
heightMultiplier=1.0
commandLine=""
barWidthReduction=0

input = "5415006160675"

outfile = "tmp.eps"


try:

   ps = psfile()
   ctrl = EAN13(input)


   ean13Symbol = EAN13Symbol(input,
                             ean13font,
                             heightMultiplier,
                             barWidthReduction)

   ps.orbb(ean13Symbol.bb())

   comments = [] # "","foo"]
   
   ps.lines = ps.header(
      input,
      comments,
      ean13font,isbnfont,upc5font) + \
      [ "ean13font" ] + \
      ean13Symbol.pslines() +\
      [ "isbnfont" ] + \
      ean13Symbol.psTopCenterText("%s %s" % (
      "name",ctrl.s),isbnfont)

   ps.lines.append("%% this is a comment")
   ps.lines=ps.lines + ps.trailer()
   ps.setbb()


   ps.out(outfile)
   
   if outfile:
      sys.stderr.write("Output written to %s\n" % outfile)
except BooklandError, message:
   sys.stderr.write(BooklandError + ": " + message + "\n")
   sys.exit(1)



## class Barcode(Flowable):
##    def __init__(self,txt):
##       self.txt = txt

##    def getbits(self,txt):
##       leftTxt = txt[0:5]
##       bits = "0" * 9 # left light margin (minimum 9 modules wide)
##       bits += "101"  # left-hand guard bars
##       for c in leftTxt:
##          i = int(c)
         
##       # The bars in the center comprise the fixed center bar pattern,
##       # encoded 01010 :

##       bits += "01010"
      
         
         
         
         


   
