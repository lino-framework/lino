#
#	Ypage parser.  -- part of Snakelets.
#	(c) Irmen de Jong 
#

import sre
import tokenizer
import types
import os
import codecs


class ParserError(Exception):
	def __init__(self, msg, linenum):
		msg = msg+" @"+str(linenum)
		Exception.__init__(self, msg)

	
def isWhitespace(text):
	return type(text) in types.StringTypes and (len(text)==0 or text.isspace())
		

# the objects of the AST

class AbstractSyntaxElement:
	def __str__(self):
		return repr(self)
	def __repr__(self):
		return "<"+self.__class__.__name__+">"
		
class Declaration(AbstractSyntaxElement):
	def __init__(self, name, value):
		self.name=name.strip()
		self.value=value.strip()
		
class TextBlock(AbstractSyntaxElement):
	def __init__(self, text):
		self.text=text
	def mergeText(self,text):
		self.text+=text

class Whitespace(TextBlock):
	pass

class Comment(AbstractSyntaxElement):   # NO TextBlock!
	def __init__(self, text):
		self.text=text
	
class URLCall(AbstractSyntaxElement):   # NO TextBlock!
	def __init__(self, url):
		self.url=url

class URLForward(AbstractSyntaxElement):   # NO TextBlock!
	def __init__(self, url):
		self.url=url

class Expression(AbstractSyntaxElement):
	def __init__(self, text):
		self.text=text.strip()

class Script(AbstractSyntaxElement, list):
	def __init__(self, text, lst=[], stripIndent=0):
		list.__init__(self,lst)
		self.text=text.rstrip()
		if stripIndent:
			self.text=self.stripIndent(self.text)
	def stripIndent(self, text):
		# strip starting indents
		lines=self.text.split('\n')
		if lines:
			if not lines[0]:
				del lines[0]
			indent=len(lines[0])-len(lines[0].lstrip())
			if indent:
				lines=[line[indent:] for line in lines]
		return '\n'.join(lines)
	def __repr__(self):
		s=["<Script:"]
		for c in self:
			s.append(",")
			s.append(repr(c))
		s.append('/Script>')
		return ''.join(s)
	def isStartOfBlock(self):
		# if it ends with a : or with a : followed by a comment, it's a block start
		return self.text.endswith(':') or sre.match("[^:#]*:[ \t]*(#.*)?$", self.text)
	def isEndScript(self):
		return self.text=="end"
	def isEndAndNewBlock(self):
		return sre.match(r"^else:",self.text) or sre.match(r"^elif\s.+:",self.text)
		
class ScriptEndBlock(AbstractSyntaxElement,list):
	def __init__(self, content=None):
		if content is not None:
			self.append(content)
		
class Document(AbstractSyntaxElement, list):
	def __repr__(self):
		s=["[DOCUMENT:"]
		for c in self:
			s.append(",")
			s.append(repr(c))
		s.append(']')
		return ''.join(s)
	



# The parser.
# Parses a tokenized stream into a AST, with a few
# syntax checks along the way.

# <ypage> --> DeclarationBlock DocBody <None>
# DeclarationBlock --> (WS Declaration)*
# DocBody --> (Text | Comment | Expression ) *

class Parser(object):
	def __init__(self, stream, filename, inputEncoding):
		self.tokenizer=tokenizer.Tokenizer(stream,filename)
		self.fileLocation = os.path.dirname(filename)
		self.inputEncoding=inputEncoding
		self.tokens=self.tokenizer.getTokens()
		self.currentToken=None
		self.previousToken=None
		self.scriptNesting=0
		self.nextToken()
		self.includedDeclarations=[]
		
	def nextToken(self):
		try:
			self.previousToken=self.currentToken
			self.currentToken=self.tokens.next()
			return self.currentToken
		except StopIteration:
			# end of input
			self.currentToken=None
			return None
	def undoToken(self):
		self.currentToken, self.previousToken = self.previousToken, None
		
	def parse(self):
		ast=Document()
		declarations = self.parseDeclarationBlock()
		ast.extend(self.parseDocBody())
		if self.currentToken is None:
			declarations.extend(self.includedDeclarations)
			declarations.reverse()
			for d in declarations:
				ast.insert(0,d)   # place declarations at the front.
			return ast
		else:
			raise ParserError("trailing garbage at end of file", self.tokenizer.getLocationStr())

	def processWhitespaceAndComments(self):
		ast=[]
		while isWhitespace(self.currentToken) or self.currentToken==tokenizer.TOK_COMMENTOPEN:
			self.skipComment()
			if isWhitespace(self.currentToken):
				ast.append(Whitespace(self.currentToken))
				self.nextToken()
			else:
				break
		return ast
	
	def skipComment(self):
		if self.currentToken==tokenizer.TOK_COMMENTOPEN:
			while self.currentToken!=tokenizer.TOK_COMMENTCLOSE:
				self.nextToken()
				if not self.currentToken:
					raise ParserError("missing comment closing tag", self.tokenizer.getLocationStr())
			self.nextToken() # skip the comment closing tag
				
				
	# Returns the parsed declarations in the DeclarationBlock at the
	# beginning of the document. On exit, the curToken is the first
	# non-whitespace token (or None at EOF).
	# tested and okay
	def parseDeclarationBlock(self):
		ast=[]
		while self.currentToken==tokenizer.TOK_DECLARATIONOPEN or type(self.currentToken) in types.StringTypes:
			ast.extend(self.processWhitespaceAndComments())
			if self.currentToken==tokenizer.TOK_DECLARATIONOPEN:
				self.nextToken()
				if type(self.currentToken) in types.StringTypes:
					name, value = self.currentToken.split('=',1)
					ast.append(Declaration(name.strip(), value.strip()))
					if self.nextToken()==tokenizer.TOK_SCRIPTCLOSE:
						self.nextToken()
					else:
						raise ParserError("close token expected", self.tokenizer.getLocationStr())
				else:
					raise ParserError("text expected", self.tokenizer.getLocationStr())
			else:
				# it is not a decl, we must be finished
				break
		return ast


	
	# DocBody        --> (Text | Comment | Expression | Script | Instruction ) *
	# DocBodyInBlock --> (Text | Comment | Expression | No_EndBlock_Script ) *
	def parseDocBody(self, inBlock=0):
		ast=[]
		while 1:
			if type(self.currentToken) in types.StringTypes:		# Text
				ast.append(TextBlock(self.currentToken))
				self.nextToken()
			elif self.currentToken==tokenizer.TOK_COMMENTOPEN:
				self.skipComment()
			elif self.currentToken==tokenizer.TOK_EXPRESSIONOPEN:
				ast.append(self.parseExpression())
			elif self.currentToken==tokenizer.TOK_SCRIPTOPEN:
				if inBlock:
					script=self.parseScript()
					if script[0].isEndScript(): 
						return ast,None
					elif script[0].isEndAndNewBlock():
						return ast,script
					ast.extend(script)
				else:
					script=self.parseScript()
					if len(script)==1 and script[0].text.lower()=="end":
						raise ParserError("block ended while not in block", self.tokenizer.getLocationStr())
					ast.extend(script)
			elif self.currentToken==tokenizer.TOK_INSTRUCTIONOPEN:
				# processing instruction
				self.nextToken()
				if type(self.currentToken) in types.StringTypes:
					instruction, value = self.currentToken.split('=',1)
					self.processInstruction(instruction.lower(), value, ast)
					if self.nextToken()==tokenizer.TOK_SCRIPTCLOSE:
						self.nextToken()
					else:
						raise ParserError("close token expected", self.tokenizer.getLocationStr())
				else:
					raise ParserError("text expected", self.tokenizer.getLocationStr())
			else:
				# end of docbody
				break
		return ast
	
	# Expression -> ExpressionOpen TextBlock ExpressionClose
	def parseExpression(self):
		if self.currentToken==tokenizer.TOK_EXPRESSIONOPEN:
			self.nextToken()
			if type(self.currentToken) in types.StringTypes:
				expr=Expression(self.currentToken)
				self.nextToken()
				if self.currentToken==tokenizer.TOK_SCRIPTCLOSE:
					self.nextToken()
					return expr
				else:
					raise ParserError("expression close expected", self.tokenizer.getLocationStr())
			else:
				raise ParserError("text expected", self.tokenizer.getLocationStr())
		else:
			raise ParserError("expression expected", self.tokenizer.getLocationStr())

	
	# Script --> ScriptFragment | ScriptBlock
	# ScriptFragment --> ScriptOpen text-without-: ScriptClose
	def parseScript(self):
		if self.currentToken==tokenizer.TOK_SCRIPTOPEN:
			self.nextToken()
			if type(self.currentToken) in types.StringTypes:
				scriptNode=Script(self.currentToken, stripIndent=1)
				closeTok = self.nextToken()
				if closeTok in (tokenizer.TOK_SCRIPTCLOSE, tokenizer.TOK_SCRIPTCLOSEKEEPB):
					self.nextToken()
					if closeTok==tokenizer.TOK_SCRIPTCLOSEKEEPB or scriptNode.isStartOfBlock():
						newscript=self.parseScriptBlock(scriptNode)
						if newscript is not None:
							ast=[scriptNode]
							ast.extend(newscript)
							return ast
					return [scriptNode]
				else:
					raise ParserError("script close expected", self.tokenizer.getLocationStr())
			else:
				raise ParserError("text expected", self.tokenizer.getLocationStr())
		else:
			raise ParserError("script expected", self.tokenizer.getLocationStr())
		
	# ScriptBlock --> ScriptOpen text-with-: ScriptClose DocBody ScriptOpen 'end' ScriptClose
	def parseScriptBlock(self, scriptNode):
		# the initial script node is already parsed and passed in
		(body,script)=self.parseDocBody(inBlock=1)
		if len(body)>1:
			scriptNode.extend(body)
		return script

	def processInstruction(self, instr, value, ast):
		value=value.strip()
		if value.startswith('"'): value=value[1:]
		if value.endswith('"'): value=value[:-1]
		if instr=="include":
			filename=os.path.join(self.fileLocation, value)
			print "PARSING INCLUDED FILE",filename
			try:
				includeStream = self.openIncludedFile(filename, encoding=self.inputEncoding)
			except Exception,x:
				raise ParserError("error including file '%s': %s" % (value, x), self.tokenizer.getLocationStr())

			parsed=Parser(includeStream, filename, self.inputEncoding).parse()
			includeStream.close()
			for item in parsed:
				if isinstance(item, Declaration):
					self.includedDeclarations.append(item)
			ast.append(Comment("BEGIN INCLUDE %s" % value ))
			ast.extend(parsed)
			ast.append(Comment("END INCLUDE %s" % value ))
		elif instr=="includeraw":
			filename=os.path.join(self.fileLocation, value)
			print "INCLUDING RAW FILE",filename
			try:
				includedFile = self.openIncludedFile(filename, raw=1)
				included = includedFile.read()
				includedFile.close()
			except Exception, x:
				raise ParserError("error including file '%s': %s" % (value, x), self.tokenizer.getLocationStr())
			ast.append(Comment("BEGIN INCLUDERAW %s" % value ))
			ast.append(TextBlock(included))
			ast.append(Comment("END INCLUDERAW %s" % value ))
		elif instr=="call":
			ast.append(URLCall(value))
		elif instr=="forward":
			ast.append(URLForward(value))
		else:
			raise ParserError("unknown instruction", self.tokenizer.getLocationStr())

	def openIncludedFile(self, filename, encoding=None, raw=0):
		if raw:
			return file(filename,"rb")
		elif encoding:
			return codecs.open(filename, mode="rb", encoding=encoding)
		else:
			return file(filename, "r")


# test methods		
				
def syntaxTreeToStr(c):
	s=""
	if isinstance(c, Document):
		for child in c:
			s+=syntaxTreeToStr(child)
	elif isinstance(c,  Declaration):
		s+="<%%@%s=%s@%%>" % (c.name, c.value)
	elif isinstance(c,URLCall):
		s+='\n----> CALL URL HERE: '+c.url+'\n'
	elif isinstance(c,URLForward):
		s+='\n----> FORWARD URL HERE: '+c.url+'\n'
	elif isinstance(c,Comment):
		s+='\n# '+c.text+'\n'
	elif isinstance(c,TextBlock):
		if isinstance(c,Whitespace):
			s+='['+c.text+']'
		else:
			s+='{'+c.text+'}'
	elif isinstance(c, Expression):
		s+="<%%=%s%%>" % c.text
	elif isinstance(c, Script):
		s+="<%SCRIPTID:"+`id(c)`+"\t"+c.text+"%>"
		for child in c:
			s+=syntaxTreeToStr(child)
		s+="<%end SCRIPTID:"+`id(c)`+"%>"
	else:
		raise ValueError("invalid syntax "+repr(c))

	return s
	
def main(args):
	parser = Parser(open(args[1], "r"), args[1], None)
	syntaxtree=parser.parse()
	print syntaxtree
	print '*'*70
	print syntaxTreeToStr(syntaxtree),


if __name__=="__main__":
	import sys
	main(sys.argv)
	
