#
#	Ypage tokenizer -- part of Snakelets.
#	(c) Irmen de Jong 
#

from __future__ import generators

class TokenizerError(Exception):
	def __init__(self, tokenizer, msg):
		msg = msg+" @"+str(tokenizer.getLocationStr())
		Exception.__init__(self, msg)


# special token IDs
TOK_DECLARATIONOPEN   = 1000
TOK_EXPRESSIONOPEN    = 1001
TOK_SCRIPTOPEN        = 1002
TOK_SCRIPTCLOSE       = 1003
TOK_SCRIPTCLOSEKEEPB  = 1004
TOK_COMMENTOPEN       = 1005
TOK_COMMENTCLOSE      = 1006
TOK_INSTRUCTIONOPEN   = 1007

# stream reader that can peek ahead and unread a character
class BufferedChars(object):
	def __init__(self, tokenizer, stream):
		self.stream=stream
		self.chars=[]
		self.nextIdx=0
		self.tokenizer=tokenizer
		self.previousChar=None
		self.linenumber=0
		
	def next(self):
		try:
			self.previousChar = self.chars[self.nextIdx-1]
			self.nextIdx+=1
			return self.chars[self.nextIdx-1]
		except IndexError:
			self.linenumber+=1
			if self.chars:
				self.previousChar = self.chars[-1]
			self.chars=self.stream.readline()
			if self.chars:
				self.nextIdx=1
				return self.chars[0]
			else:
				# end of stream
				self.nextIdx=-1
				return ''

	def peek(self):
		return self.chars[self.nextIdx]
		
	def previous(self):
		return self.previousChar
		#if self.nextIdx>=2:
		#	return self.chars[self.nextIdx-2]
		#else:
		#	raise TokenizerError(self.tokenizer, "cannot return last char: buffer empty")

	def unread(self):
		self.nextIdx-=1
		if self.nextIdx<1:
			raise TokenizerError(self.tokenizer, "cannot unread char: buffer empty")

	def getLineNumber(self):
		return self.linenumber
	def getColumn(self):
		return self.nextIdx
		
			
# Stream tokenizer (using generators so memory friendly)
class Tokenizer(object):
	def __init__(self, stream, filename):
		self.chars=BufferedChars(self, stream)
		self.filename=filename
		
	def getLocationStr(self):
		return "line %d col %d (file: %s)" % (self.chars.getLineNumber(), self.chars.getColumn(), self.filename)
	
	def getTokens(self):			# a generator!
		buffer=[]
		while 1:
			c= self.chars.next()
			if not c:
				break
			elif c=='<' and self.chars.peek()=='%':
				# <% open tag. First yield the buffer that we have accumulated until now.
				if buffer:
					yield ''.join(buffer)
					buffer=[]
				self.chars.next()
				next=self.chars.peek()
				if next=='@':
					self.chars.next()
					yield TOK_DECLARATIONOPEN
				elif next=='$':
					self.chars.next()
					yield TOK_INSTRUCTIONOPEN
				elif next=='=':
					self.chars.next()
					yield TOK_EXPRESSIONOPEN
				elif next=='!':
					# could be a comment <%!--
					self.chars.next()
					if self.chars.next()=='-':
						if self.chars.next()=='-':
							yield TOK_COMMENTOPEN
							continue
						self.chars.unread()
					self.chars.unread()
					# hm, it is not <%!--, just a script.
					yield TOK_SCRIPTOPEN
				else:
					yield TOK_SCRIPTOPEN
			elif c=='-' and self.chars.peek()=='%':
				# could be comment close: --%>
				if self.chars.previous()=='-':
					self.chars.next() # skip the %
					if self.chars.peek()=='>':
						self.chars.next()
						# yield the buffer upto the previous char
						if len(buffer)>1:
							yield ''.join(buffer[:-1])
						buffer=[]
						yield TOK_COMMENTCLOSE
						continue
					else:
						self.chars.unread() # rollback the %
				# it's a normal '-', append it
				buffer.append('-') 
			elif c=='%' and self.chars.peek()=='>':
				if self.chars.previous()=='\\':
					# it's a \%> close tag
					tag = TOK_SCRIPTCLOSEKEEPB
					del buffer[-1] # get rid of the \
				else:
					tag = TOK_SCRIPTCLOSE
				# %> close tag.
				if buffer:
					yield ''.join(buffer)
					buffer=[]
				yield tag
				self.chars.next() # read the '>'
				# accumulate any whitespace charactes up to and including newline
				while 1:
					c=self.chars.next()
					if not c.isspace():
						self.chars.unread()
						break
					if c=='\n':
						if self.chars.previous()=='\r':
							buffer[-1]='\n'  # replace \r\n by \n
						else:
							buffer.append(c)
						break
					buffer.append(c)
				if buffer:
					# yield a separate whitespace text block
					yield ''.join(buffer)
					buffer=[]
			else:
				# add the char to the buffer
				if c=='\n' and self.chars.previous()=='\r':
					buffer[-1]='\n'   # replace \r\n by \n
				else:
					buffer.append(c)
				
		# yield the remaining buffer, if any.
		if buffer:
			yield ''.join(buffer)
			buffer=[]




# test method
				
def main2(args):
	tok = Tokenizer(open(args[1], "r"), args[1])
	for t in tok.getTokens():
		print `t`

def main(args):
	tok = Tokenizer(open(args[1], "r"), args[1])
	s=""
	for t in tok.getTokens():
		if t==TOK_DECLARATIONOPEN:
			s+="<%@"
		elif t==TOK_INSTRUCTIONOPEN:
			s+="<%$"
		elif t==TOK_EXPRESSIONOPEN:
			s+="<%="
		elif t==TOK_SCRIPTOPEN:
			s+="<%"
		elif t==TOK_SCRIPTCLOSE:
			s+="%>"
		elif t==TOK_SCRIPTCLOSEKEEPB:
			s+="\\%>"
		elif t==TOK_COMMENTOPEN:
			s+="<%!--"
		elif t==TOK_COMMENTCLOSE:
			s+="--%>"
		elif type(t)==type(''):
			s+="{"+t+"}"
		else:
			raise ValueError("invalid token "+repr(t))
	print '*'*70
	print s,


if __name__=="__main__":
	import sys
	main(sys.argv)
	
