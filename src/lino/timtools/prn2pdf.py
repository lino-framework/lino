#coding: latin1

"""
prn2pdf converts a stream containing text and simple formatting
printer control sequences into a PDF file.  

USAGE :
  prn2pdf [options] FILE

  where FILE is the .prn file to be converted 
  
OPTIONS :
  -o, --output FILE        write result to file FILE
  -b, --batch              don't start Acrobat Reader on the generated
                           pdf file
  -h, --help               display this text

See :pageref:`docs/prn2pdf` for more documentation.
  
"""


import sys, os, getopt
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,mm
from reportlab.lib.pagesizes import letter, A4

from lino import __version__, copyleft
#from lino.misc import gpl

class Status:
	"""
	could be used to save/restore the status of the textobject
	"""
	def __init__(self,size=10,
					 psfontname="Courier",
					 bold=False,
					 ital=False,
					 leading=14.4):
		self.ital = ital
		self.bold = bold
		self.psfontname = psfontname
		self.size = size
		self.leading = leading
		self.lpi = None


class PdfPage:
	def __init__(self,filename):
		self.commands = {
			chr(12) : self.formFeed,
			chr(27)+"l" : self.setLpi,
			chr(27)+"c" : self.setCpi,
			chr(27)+"b" : self.setBold,
			chr(27)+"i" : self.setItalic,
			chr(27)+"L" : self.setPageLandscape,
			chr(27)+"I" : self.insertImage,
			}
		
		self.canvas = canvas.Canvas(filename,
											 pagesize=A4)
		self.pageWidth,self.pageHeight = A4

		#self.canvas.setAuthor("Generated using prn2pdf")
		#self.canvas.setSubject("http://my.tele2.ee/lsaffre/comp/prn2pdf.htm")

		self.margin = 5 * mm
		

		self.status = Status()
		#self.oldStatus = None # used by *untilEol cmds
		
		self.page = 0

		self.textobject = None


##		def background(self):
##			self.canvas.drawImage('logo2.jpg',
##										 self.margin,
##										 self.pageHeight-(2*self.margin)-25*mm,
##										 25*mm,25*mm)
									 
##			textobject = self.canvas.beginText()
##			textobject.setTextOrigin(self.margin+26*mm,
##											 self.pageHeight-(2*self.margin))
##			textobject.setFont("Times-Bold", 12)
##			textobject.textLine("Rumma & Ko	OÜ")
##			textobject.setFont("Times-Roman", 10)
##			textobject.textLine("Tartu mnt. 71-5")
##			textobject.textLine("10115 Tallinn")
##			textobject.textLine("Eesti")
##			self.canvas.drawText(textobject)

	def beginPage(self):
		#self.background()
		self.page += 1
		assert self.textobject is None
		if self.pageHeight < self.pageWidth:
			# if landscape mode
			self.canvas.rotate(90)
			self.canvas.translate(0,-210*mm)
			
		self.textobject = self.canvas.beginText()
		self.textobject.setTextOrigin(self.margin,
												self.pageHeight-(2*self.margin))
		self.textobject.setFont("Courier", 10)
	
	def endPage(self):
		if self.textobject is None:
			# a formfeed without any preceding text generates a blank page
			self.beginPage()
			
		self.canvas.drawText(self.textobject)
		self.canvas.showPage()
		self.textobject = None
		
	def setPageLandscape(self,line):
		assert self.textobject is None, \
				 'setLandscape after first text has been printed'
		if self.pageHeight > self.pageWidth:
			# only if not already
			self.pageHeight, self.pageWidth = (
				self.pageWidth,self.pageHeight)
			self.canvas.setPageSize(
				(self.pageHeight,self.pageWidth))
		return 0


	def done(self):
		if not self.textobject is None:
			self.endPage()
		try:
			self.canvas.save()
		except IOError,e:
			print "ERROR : could not save pdf file:"
			print e
			sys.exit(-1)
			
	def setFont(self):
		psfontname = self.status.psfontname
		if self.status.bold:
			psfontname += "-Bold"
			if self.status.ital:
				psfontname += "Oblique"
		elif self.status.ital:
			psfontname += "-Oblique"
			
		if self.textobject is None:
			self.beginPage()
		if self.status.lpi is not None:
			self.status.leading = 72 / self.status.lpi
		self.textobject.setFont(psfontname,
										self.status.size,
										self.status.leading)


	def toText(self,text):
		if self.textobject is None:
			#if self.page == 2:
			#	 print repr(text)
			self.beginPage()

		# Schade, dass PDF oder reportlab scheinbar nicht Unicode
		# unterstützt. Deshalb muss ich die Box-Character hier durch
		# Minusse & Co ersetzen...

		text = text.replace(chr(179),"|")
		text = text.replace(chr(180),"+")
		text = text.replace(chr(185),"+")
		text = text.replace(chr(186),"|")
		text = text.replace(chr(187),"+")
		text = text.replace(chr(188),"+")
		text = text.replace(chr(191),"+")
		text = text.replace(chr(192),"+")
		text = text.replace(chr(193),"+")
		text = text.replace(chr(194),"+")
		text = text.replace(chr(195),"+")
		text = text.replace(chr(196),"-")
		text = text.replace(chr(193),"+")
		text = text.replace(chr(200),"+")
		text = text.replace(chr(201),"+")
		text = text.replace(chr(202),"+")
		text = text.replace(chr(203),"+")
		text = text.replace(chr(204),"+")
		text = text.replace(chr(205),"-")
		text = text.replace(chr(206),"+")
		text = text.replace(chr(217),"+")
		text = text.replace(chr(218),"+")
		
		text = text.decode("cp850")
		text = text.encode("iso-8859-1","replace")
				
		self.textobject.textOut(text)
		

	def FindFirstCtrl(self,line):
		firstpos = None
		firstctrl = None
		for ctrl in self.commands.keys():
			pos = line.find(ctrl)
			if pos != -1 and (firstpos == None or pos < firstpos):
				firstctrl = ctrl
				firstpos = pos
		return (firstpos,firstctrl)
	

	def PrintLine(self,line):

		#if not self.oldStatus is None:
		#	 self.restoreStatus()
		(pos,ctrl) = self.FindFirstCtrl(line)
		while pos != None:
			if pos > 0:
				self.toText(line[0:pos])

			line = line[pos+len(ctrl):]
			meth = self.commands[ctrl]
			nbytes = meth(line)
			if nbytes > 0:
				line = line[nbytes:]
			#print "len(%s) is %d" % (repr(ctrl),len(ctrl))
			(pos,ctrl) = self.FindFirstCtrl(line)

		if line == "\r\n": return
		if len(line) == 0: return
		
		self.toText(line)
		self.textobject.textLine()
		#self.c.drawString(self.xpos, self.ypos, line)
		#self.ypos -= self.linespacing 

##		def saveStatus(self):
##			assert self.oldStatus is None
##			self.oldStatus = self.status
##			self.status = Status(self.status.size,
##										self.status.psfontname,
##										self.status.bold,
##										self.status.ital,
##										self.status.leading
##										)

##		def restoreStatus(self):
##			self.status = self.oldStatus
##			self.oldStatus = None
##			self.setFont()

	## methods called if ctrl sequence is found :

	def setLpi(self,line):
		par = line.split(None,1)[0]
		lpi = int(par)
		# if lpi != 6:
		# ignore 6lpi because this is the standard.
		# In a pdf file it's better to use 
		self.status.lpi = lpi
		self.setFont()
		return len(par)+1
		
	def setCpi(self,line):
		par = line.split(None,1)[0]
		cpi = int(par) # ord(line[0])
		if cpi == 10:
			self.status.size = 12
			self.status.leading = 14
		elif cpi == 12:
			self.status.size = 10
			self.status.leading = 12
		elif cpi == 15:
			self.status.size = 8
			self.status.leading = 10
		elif cpi == 17:
			self.status.size = 7
			self.status.leading = 8
		elif cpi == 20:
			self.status.size = 6
			self.status.leading = 8
		elif cpi == 5:
			self.status.size = 24
			self.status.leading = 28
		else:
			raise "%s : bad cpi size" % par
		self.setFont()
		return len(par)+1
		 

		
	def insertImage(self,line):
		params = line.split(None,3)
		if len(params) < 3:
			raise "%s : need 3 parameters" % repr(params)
		# picture size must be givin in mm :
		w = float(params[0]) * mm #*self.status.size
		h = float(params[1]) * mm #*self.status.leading
		# position of picture is the current text cursor 
		(x,y) = self.textobject.getCursor()
		if x == 0 and y == 0:
			# print "no text has been processed until now"
			x = self.margin + x
			y = self.pageHeight-(2*self.margin)-h - y
		else:
			# but picture starts on top of charbox:
			y += self.status.leading
			
		filename = params[2]
		self.canvas.drawImage(filename,
									 x,y-h,
									 w,h)
		return len(params[0])+len(params[1])+len(params[2])+3
	
		
	def setItalic(self,line):
		if line[0] == "0":
			self.status.ital = False
		elif line[0] == "1":
			self.status.ital = True
		self.setFont()
		return 1
	
	def setBold(self,line):
		if line[0] == "0":
			self.status.bold = False
		elif line[0] == "1":
			self.status.bold = True
		self.setFont()
		return 1
	
	def setUnderline(self,line):
		if line[0] == "0":
			pass
		elif line[0] == "1":
			pass
		return 1
		
	def formFeed(self,line):
		self.endPage()
		# self.beginPage()
		return 0


def main(argv):
	print "prn2pdf" # version " + __version__
	print copyleft('2002-2004','Luc Saffre')



	try:
		opts, args = getopt.getopt(argv,
											"h?o:b",
											["help", "output=","batch"])

	except getopt.GetoptError:
		print __doc__
		sys.exit(-1)

	if len(args) != 1:
		print __doc__
		sys.exit(-1)

	inputfile = args[0]
	(root,ext) = os.path.splitext(inputfile)
	outputfile = root + ".pdf"
	if len(ext) == 0:
		inputfile += ".prn"

	showOutput=True
	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		if o in ("-o", "--output"):
			outputfile = a
		if o in ("-b", "--batch"):
			showOutput=False
			
	(root,ext) = os.path.splitext(outputfile)
	if ext.lower() != ".pdf":
		outputfile += ".pdf"
		
	p = PdfPage(outputfile)
	try:
		f = file(inputfile)
		for line in f.readlines():
			p.PrintLine(line)
	except IOError,e:
		print e
		sys.exit(-1)

	p.done()
	
	
	if showOutput:
		os.system("start %s" % outputfile)
