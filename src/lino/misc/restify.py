#coding: latin-1
"""
by Nicola Paolucci
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/193890

added by LS:
- output encoding
- exec directive

"""
from docutils import core, io
from docutils.writers.html4css1 import Writer,HTMLTranslator

class NoHeaderHTMLTranslator(HTMLTranslator):
    def __init__(self, document):
        HTMLTranslator.__init__(self,document)
        self.head_prefix = ['','','','','']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []


_w = Writer()
_w.translator_class = NoHeaderHTMLTranslator

_namespace={}


import sys
import traceback
from StringIO import StringIO
from docutils import nodes, statemachine
from docutils.parsers.rst.directives import register_directive
from textwrap import dedent
from docutils.utils import SystemMessage

def exec_exec( name, arguments, options, content, lineno,
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
    exec text in _namespace,_namespace
    #try:
    #   exec text in _namespace,_namespace
    #except Exception,e:
    #   traceback.print_exc(None,sys.stderr)
        #print e
    stdout_text = sys.stdout.getvalue()
    sys.stdout = _stdout
    # sys.stderr.write(stdout_text)
    insert_lines = statemachine.string2lines(stdout_text,
                                             convert_whitespace=1)
    state_machine.insert_input(insert_lines, "exec")
    return []
    
exec_exec.content = 1
register_directive('exec',exec_exec)

def reSTify(s,
            source_path=None,
            namespace=None,
            settings=None):
    if namespace is None:
        namespace = {}
    global _namespace
    _namespace = namespace
    return core.publish_string(s,
                               source_path,
                               settings_overrides=settings,
                               writer=_w)
##  try:
##      return core.publish_string(s,
##                                          settings_overrides=settings,
##                                          writer=_w)
##  except SystemMessage,e:
##      return str(e)+"\n"+s


def inspect(filename,
            source_path=None,
            ):
    "returns the document object before any transforms)"
    from docutils.core import Publisher
    pub = Publisher(
                    source_class=io.FileInput,
                    )
    pub.set_reader('standalone',None,"restructuredtext")
    pub.process_programmatic_settings(None,None,None)
    pub.set_source(source_path=source_path)
    pub.set_io()
    return pub.reader.read(pub.source, pub.parser, pub.settings)
    


if __name__ == '__main__':
    test = """
Test example of reST__ document
containg non-ascii latin-1 chars:
Ä Ë Ï Ö Ü 
ä ë ï ö ü ÿ
à è ì ò ù 
á é í ó ú
ã õ ñ 
ç ß 

__ http://docutils.sf.net/rst.html

- item 1
- item 2
- item 3

"""
    print reSTify(test,output_encoding='latin-1') 
