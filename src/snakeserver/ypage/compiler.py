import sys
import parser
import tokenizer
import codecs
import sre
import os

linesep='\n'   # os.linesep doesn't work.

class CompilerError(Exception):
	pass

class PageCompiler:
	def __init__(self):
		pass
		
	def compilePage(self, filename, outputStream):
		self.declarations={}
		self.imports=[]
		self.gobbleWS=0
		self.outputEncoding=None
		self.contentType=None
		self.indentChars='\t' # tabs
		self.session=1 # default: use session
		self.requiresUser=0  # default: do not require user
		self.inputEncoding, self.outputEncoding=self.determineInputOutputEncodings(filename)
		if self.outputEncoding:
			outputStream=codecs.getwriter("UTF-8")(outputStream)	# compiled page is always writtin in UTF-8
		try:
			try:
				pageSourceStream=None
				if self.inputEncoding:
					pageSourceStream=codecs.open(filename,mode="rb",encoding=self.inputEncoding)
				else:
					# use regular file because input encoding is default (not specified).
					pageSourceStream=file(filename,"r")
				syntaxtree=parser.Parser(pageSourceStream, filename, self.inputEncoding).parse()
			finally:
				if pageSourceStream:
					pageSourceStream.close()		# otherwise .y file remains opened until GC'd.
	
			if self.outputEncoding:
				if sys.version_info[:2]>=(2,3):
					outputStream.write("# -*- coding: UTF-8 -*-"+linesep)	# compiled page is always writtin in UTF-8
				else:
					raise CompilerError("You need Python 2.3 or newer to use the outputEncoding option!")
			self.generateCode(syntaxtree,outputStream,0)
		except (tokenizer.TokenizerError, parser.ParserError), px:
			raise CompilerError(px)

	def determineInputOutputEncodings(self, filename):
		inputEnc=outputEnc=None
		for line in file(filename,"r").readlines(1000)[:10]: # first 10 lines
			m=sre.match(r"\s*<%@\s*(.+)\s*=\s*(.+)\s*%>\s*$", line)
			if m:
				(name,value)=m.groups()
				if name.lower()=='inputencoding':
					inputEnc=value
				elif name.lower()=='outputencoding':
					outputEnc=value
		return (inputEnc, outputEnc)

	def _addTextBlock(self, astlist, child):
		if len(astlist)>0 and isinstance(astlist[-1], parser.TextBlock):
			astlist[-1].text+=child.text
		else:
			astlist.append(child)

	def optimize(self, ast):
		optimized=[]
		prev=None
		for child in ast:
			if isinstance(child, parser.Script):
				script=parser.Script
				optimized.append(parser.Script(child.text, self.optimize(child)))
			elif isinstance(child, parser.Comment):
				optimized.append(child)
			elif isinstance(child, parser.Whitespace):
				if not self.gobbleWS:
					self._addTextBlock(optimized, child)
			elif isinstance(child, parser.TextBlock):
				if self.gobbleWS and not isinstance(prev, parser.Expression):
					newTxt=child.text.lstrip()
					if newTxt:
						self._addTextBlock(optimized, parser.TextBlock(newTxt))
				else:
					self._addTextBlock(optimized, child)
			else:
				optimized.append(child)
			prev=child
		return optimized
	
	def processDeclarations(self, syntaxtree, out):
		gatheredWhitespace=""
		while isinstance(syntaxtree[0],  parser.Declaration) or isinstance(syntaxtree[0], parser.Whitespace):
			c=syntaxtree[0]
			del syntaxtree[0]
			if isinstance(c, parser.Whitespace):
				gatheredWhitespace += c.text
				continue

			c.name=c.name.lower()

			if c.name=='import':
				if c.value.split()[0] in ("import", "from"):
					self.imports.append(c.value)
				else:
					raise ImportError("invalid import statement: "+c.value)
			elif c.name=='gobblews':
				if c.value.lower() in ('yes','no'):
					self.gobbleWS = c.value.lower()=='yes'
				else:
					raise CompilerError("gobblews must be yes or no")
			elif c.name=='session':
				if c.value.lower() in ('yes','no', 'user'):
					self.session = c.value.lower() in ('yes', 'user')
					self.requiresUser = c.value.lower() == 'user'
				else:
					raise CompilerError("session must be yes, no or user")
			elif c.name=='outputencoding':
				if self.outputEncoding!=c.value:
					raise RuntimeError("output encoding is parsed wrongly")
			elif c.name=='inputencoding':
				if self.inputEncoding!=c.value:
					raise RuntimeError("input encoding is parsed wrongly")
			elif c.name=='contenttype':
				self.contentType=c.value
			elif c.name=='indent':
				v=c.value.lower()
				if v=='8spaces':
					self.indentChars=' '*8
				if v=='4spaces':
					self.indentChars=' '*4
				elif v=='tab':
					self.indentChars='\t'
				else:
					raise ValueError("indent type must be tab or 4spaces or 8spaces")
			else:
				raise ValueError("unknown declaration: %s=%s" % (c.name, c.value))
			
		for imp in self.imports:
			out.write(imp+linesep)
		
		if self.gobbleWS:
			return ""
		return gatheredWhitespace
		
		
	def generateCode(self,c,out,blockindent):
		indent=self.indentChars*blockindent
		
		if isinstance(c, parser.Document):
			gatheredWhitespace=self.processDeclarations(c, out)
			if gatheredWhitespace and not self.gobbleWS:
				c.insert(0,parser.Whitespace(gatheredWhitespace))
			c=self.optimize(c)
			if self.outputEncoding:
				out.write("import codecs"+linesep)
			out.write("from snakeserver.YpageEngine import Ypage"+linesep)
			out.write("class Page(Ypage):"+linesep)
			out.write(self.indentChars+"def needsSession(self): return "+str(self.session)+linesep)
			out.write(self.indentChars+"def requiresUser(self): return "+str(self.requiresUser)+linesep)
			if self.outputEncoding:
				out.write(self.indentChars+("def getPageEncoding(self): return '%s'" % self.outputEncoding) +linesep)
			if self.contentType:
				out.write(self.indentChars+("def getPageContentType(self): return '%s'" % self.contentType) +linesep)
			out.write(self.indentChars+"def create(self,out,_request,_response):"+linesep)
			out.write(self.indentChars*2+"_w=out.write"+linesep)
			for child in c:
				self.generateCode(child, out, blockindent+2)
		elif isinstance(c,  parser.Declaration):
			if c.name=='import':
				if c.value.split()[0] in ("import", "from"):
					self.imports.append(c.value)
				else:
					raise ImportError("invalid import statement: "+c.value)
			self.declarations[c.name]=c.value
		elif isinstance(c,parser.Comment):
			out.write(indent+'# '+c.text+linesep)
		elif isinstance(c,parser.URLCall):
			out.write(indent+('_w(self.include("%s", _request, _response))' % c.url )+ linesep)
		elif isinstance(c,parser.URLForward):
			out.write(indent+('raise Ypage.PageForwardURL("%s")' % c.url )+ linesep)
		elif isinstance(c,parser.TextBlock):
			text=c.text.replace("\\","\\\\").replace("\n","\\n").replace('"','\\"')
			if isinstance(c,parser.Whitespace) and self.gobbleWS:
				return
			if self.outputEncoding:
				out.write(indent+'_w(u"'+text+'")'+linesep)
			else:
				out.write(indent+'_w("'+text+'")'+linesep)
		elif isinstance(c, parser.Expression):
			if self.outputEncoding:
				out.write(indent + "_w(unicode("+c.text+"))"+linesep)
			else:
				out.write(indent + "_w(str("+c.text+"))"+linesep)
		elif isinstance(c, parser.Script):
			lines=[indent+line for line in c.text.split('\n')]
			out.write(linesep.join(lines)+linesep)
			for child in c:
				self.generateCode(child, out, blockindent+1)
		else:
			raise ValueError("invalid syntax "+repr(c))
	

def main(args):
	compiler=PageCompiler()
	if args[2]=='-':
		output=sys.stdout
	else:
		output=file(args[2],"wb")
	compiler.compilePage(args[1], output)

if __name__=="__main__":
	import sys
	main(sys.argv)
	
