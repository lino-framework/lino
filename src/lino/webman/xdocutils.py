import os,sys
import traceback

from os.path import abspath, basename, dirname, normpath, join, exists

# from docutils import core #import publish_string, publish_file
from docutils import core, io
from docutils.writers import html4css1
import em
from StringIO import StringIO
from textwrap import dedent

from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst.directives.body import line_block
from docutils.parsers.rst import Parser
from docutils.parsers.rst.states import Inliner
from docutils import nodes, statemachine

## 	return line_block(name, arguments, options,
## 							content.splitlines(),
## 							lineno,
## 							content_offset, block_text, state, state_machine,
## 							node_class=nodes.literal_block)




## from docutils.parsers.rst import directives
## from docutils.parsers.rst.languages import en
## registry = directives._directive_registry
## registry['script'] = ('lino.timtools.txt2html','exec_script')
## #registry['script'] = ('txt2html','exec_script')
## en.directives['script'] = 'script'


class Writer(html4css1.Writer):
	def __init__(self,webmod=None):
		html4css1.Writer.__init__(self)
		#self.translator_class = MyHtmlTranslator
		self.webmod = webmod
		# self.leftArea = leftArea
		self.namespace = dict(globals())
		self.namespace['webmod'] = webmod
		self.namespace['writer'] = self
		register_directive('exec',self.exec_exec)
	

	def exec_exec(self,
					  name, arguments, options, content, lineno,
					  content_offset, block_text, state, state_machine):
		if not content:
			error = state_machine.reporter.error(
				'The "%s" directive is empty; content required.' % (name),
				nodes.literal_block(block_text, block_text), line=lineno)
			return [error]
		text = '\n'.join(content)
		text = dedent(text)
		_stdout = sys.stdout
		sys.stdout = StringIO()
		try:
			exec text in self.namespace,self.namespace
		except Exception,e:
			traceback.print_exc(None,sys.stderr)
			#print e
		stdout_text = sys.stdout.getvalue()
		sys.stdout = _stdout
		# sys.stderr.write(stdout_text)
		insert_lines = statemachine.string2lines(stdout_text,
															  convert_whitespace=1)
		state_machine.insert_input(insert_lines, "exec")
		return []
	
	exec_exec.content = 1
	
	def translate(self):
		
		"""
		translate() is called by write() and must place the HTML
		output to self.output
		
		"""
		visitor = self.translator_class(self.document)
		self.document.walkabout(visitor)
		
		self.head_prefix = visitor.head_prefix
		self.stylesheet = visitor.stylesheet
		self.head = visitor.head
		self.body_prefix = visitor.body_prefix
		self.body_pre_docinfo = visitor.body_pre_docinfo
		self.docinfo = visitor.docinfo
		self.body = visitor.body
		self.body_suffix = visitor.body_suffix

		if self.webmod.leftArea is not None:
			html = self.webmod.leftArea()
			self.body_prefix.append('''<table class="mainTable">
			<tr>
			<td valign="top" class="leftArea">
			''')
			self.body_prefix.append(html)
			self.body_prefix.append('''</td>
			<td class="textArea">''')
			self.body_suffix.insert(0,'</td></tr></table>')
			
		if self.webmod.bottomArea is not None:
			html = self.webmod.bottomArea()
			self.body_suffix.append('<div class="bottomArea">')
			self.body_suffix.append(html)
			self.body_suffix.append('</div>')
			
		if self.webmod.topArea is not None:
			raise NotImplementedError
		
		self.output = self.astext()

	def astext(self):
		return ''.join(self.head_prefix + self.head
							+ self.stylesheet + self.body_prefix
							+ self.body_pre_docinfo + self.docinfo
							+ self.body
							+ self.body_suffix)





class WebmanInliner(Inliner):
	
	def __init__(self, webmod,roles={}):
		roles['fileref'] = self.fileref_role
		roles['pageref'] = self.pageref_role
		Inliner.__init__(self,roles)
		self.webmod = webmod
	
	def fileref_role(self, role, rawtext, text, lineno):
		if self.webmod.filerefBase is not None:
			if text.startswith('/'):
				localfile = normpath(join(self.webmod.filerefBase,text[1:]))
			else:
				localfile = normpath(join(self.webmod.filerefBase,text))
			#localfile = join(self.webmod.filerefBase,normpath(text))
			if not exists(localfile):
				msg = self.reporter.error('%s : no such file' % localfile,
												  line=lineno)
				prb = self.problematic(text, text, msg)
				return [prb], [msg]
		if self.webmod.filerefURL is None:
			uri = None
		else:
			uri = self.webmod.filerefURL % text
		filename = basename(text)
		return [nodes.reference(rawtext, filename, refuri=uri)], []
	
	def pageref_role(self, role, rawtext, text, lineno):
		# doesn't work
		
		if self.webmod.filerefBase is None:
			return [rawtext],[]
		else:
			if text.startswith('/'):
				localfile = normpath(join(self.webmod.filerefBase,text[1:]))
			else:
				localfile = normpath(join(self.webmod.filerefBase,text))
				
			if exists(localfile+".txt"):
				uri = localfile+".html"
			elif os.path.isdir(localfile):
				uri = localfile+"/index.html"
			else:
				msg = self.reporter.error(\
					'pageref to unkonwn page "%s"' % localfile,
					line=lineno)
				prb = self.problematic(text, text, msg)
				return [prb], [msg]
		return [nodes.reference(rawtext, text, refuri=uri)], []
				


def publish(webmod,source):
	description = ('Lino WebMan publisher.	 '
						+ core.default_description)

	parser = Parser(rfc2822=0, inliner=WebmanInliner(webmod))
	pub = core.Publisher(writer=Writer(webmod),
								parser=parser,
								destination_class=io.StringOutput)
									
	pub.set_components('standalone', 'restructuredtext', None)
	pub.process_command_line(webmod.argv,
									 description=description,
									 **webmod.defaults)
	pub.set_source(None, source)
	return pub.publish() #enable_exit=enable_exit)
		


