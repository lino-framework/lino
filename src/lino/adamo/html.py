#coding: latin1

import re

import htmlentitydefs

#from lino.misc.restify import reSTify

def txt2html(txt):
	txt2 = ''
	for c in txt:
		o = ord(c)
		if o < 128:
			txt2 += c
		else:
			try:
				txt2 += "&%s;" % htmlentitydefs.codepoint2name[o]
			except KeyError:
				txt2 += "&#%d;" % o
	return txt2
		



class MemoParser:

	def __init__(self,cmds):
		self.cmds = cmds

	def parse(self,renderer,txt):

		if txt.startswith("#raw"):
			txt = txt[4:]
			
		#if False:
		#	txt = reSTify(txt)
		#else:
		#	txt = txt2html(txt) 

		txt = re.sub(r'\\\n\s*','',txt)

		#regex  = re.compile(r'\\\n\s*')
		#txt = txt.repl('\\\n','\n')
		#self.html = ''
		first = True
		for line in txt.split('\n\n'):
			if first:
				first = False
			else:
				renderer.write('\n<p>')

			while True:
				pos = line.find('[')
				if pos == -1:
					break
				elif pos > 0:
					renderer.write(txt2html(line[:pos]))
					line = line[pos:]

				pos = line.find(']')
				piece = line[:pos+1]
				tag = line[1:pos]
				# print tag
				line = line[pos+1:]
				cmd = tag.split(None,1)
				try:
					f = self.cmds[cmd[0].lower()]
				except KeyError:
					renderer.write(txt2html(piece))
				else:
					if len(cmd) > 1:
						params = cmd[1]
					else:
						params = None
					try:
						f(renderer,params)
					except Exception,e:
						renderer.write(txt2html(piece + " : " + str(e)))
					#if renderText is not None:
					#	renderer.write(txt2html(piece + " returned " + repr(renderText)))
			renderer.write(txt2html(line) + '\n')
			# self.write(line + '</p>\n')

		#return self.html

	#def write(self,txt):
	#	self.html += txt

if __name__ == "__main__":
	
	p = MemoParser({})
	print p.parse(r"""This is a [ref http://www.foo.bar/very/\
	long/\
	filename.html reference with a long URL].
	""")
