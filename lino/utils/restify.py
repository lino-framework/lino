#coding: utf-8
"""
Just a copy & paste of the :mod:`docutils.examples` module (as instructed there).

:func:`restify` is an alias for :func:`html_body`.

:func:`latex_body` deduced from :func:`html_body`

"""

#~ import traceback
from docutils import core, io

def html_parts(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=1):
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer_name='html', settings_overrides=overrides)
    return parts

def html_body(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', output_encoding='unicode',
              doctitle=1, initial_header_level=1):
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see :func:`html_parts` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    parts = html_parts(
        input_string=input_string, source_path=source_path,
        destination_path=destination_path,
        input_encoding=input_encoding, doctitle=doctitle,
        initial_header_level=initial_header_level)
    fragment = parts['html_body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    #~ print __file__, repr(fragment)
    return fragment
    
    
from docutils import writers 
from docutils.writers import html4css1

class HTMLTranslator(html4css1.HTMLTranslator):
    """
    Suppress surrounding DIV tag. Used by :func:`restify`.
    """
    #~ def visit_document(self, node):
        #~ self.head.append('<title>%s</title>\n'
                         #~ % self.encode(node.get('title', '')))

    def depart_document(self, node):
        self.fragment.extend(self.body)
        # I just removed the following two lines:
        #~ self.body_prefix.append(self.starttag(node, 'div', CLASS='document'))
        #~ self.body_suffix.insert(0, '</div>\n')
        # skip content-type meta tag with interpolated charset value:
        self.html_head.extend(self.head[1:])
        # was only useful to understand what's happening:
        #~ print self.body_prefix
        #~ print self.body_suffix
        #~ raise Exception("foo")
        self.html_body.extend(self.body_prefix[1:] + self.body_pre_docinfo
                              + self.docinfo + self.body
                              + self.body_suffix[:-1])
        assert not self.context, 'len(context) = %s' % len(self.context)
        
class Writer(html4css1.Writer):

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = HTMLTranslator


def restify(input_string,source_path=None, destination_path=None,
            input_encoding='unicode', doctitle=1, initial_header_level=1):
    u"""
    Renders the given reST string into a unicode HTML chunk without 
    any surrounding tags like ``<HTML>``, ``<BODY>``, and especially 
    ``<DIV class="document">`` (this last one requires the above 
    :class:`HTMLTranslator` subclass,  thanks to `Günter Milde's hint 
    <http://sourceforge.net/mailarchive/message.php?msg_id=27467363>`_
    and `example code 
    <http://docutils.sourceforge.net/sandbox/html4strict/html4strict.py>`_).
    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer=Writer(), 
        settings_overrides=overrides)
    fragment = parts['html_body']
    #~ if output_encoding != 'unicode':
        #~ fragment = fragment.encode(output_encoding)
    #~ print __file__, repr(fragment)
    return fragment
    
  
def old_restify(s,**kw):
    """
    (Didn't work when the reST text contained a root title).
    See :doc:`/blog/2011/0525`.
    """
    html = html_body(s,**kw)
    if html.startswith('<div class="document">\n') and html.endswith('</div>\n'):
        return html[23:-7]
    raise Exception("Error: restify() got unexpected HTML: %r" % html)


def latex_parts(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=1):
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        #~ writer_name='latex2e', 
        writer_name='newlatex2e', 
        settings_overrides=overrides)
    return parts

def latex_body(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', output_encoding='unicode',
              doctitle=1, initial_header_level=1):
    parts = latex_parts(
        input_string=input_string, source_path=source_path,
        destination_path=destination_path,
        input_encoding=input_encoding, doctitle=doctitle,
        initial_header_level=initial_header_level)
    #~ print parts.keys()
    fragment = parts['body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    return fragment
    
def rst2latex(input_string, 
              source_path=None, 
              input_encoding='unicode',
              doctitle=1, 
              initial_header_level=1):
    """
    returns a dict containing the following keys::
    
      'body', 
      'latex_preamble', 
      'head_prefix', 
      'requirements', 
      'encoding', 
      'abstract', 
      'title', 
      'fallbacks', 
      'stylesheet', 
      'version', 
      'body_pre_docinfo', 
      'dedication', 
      'subtitle', 
      'whole', 
      'docinfo', 
      'pdfsetup'

    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    #~ doc = core.publish_doctree(source=input_string, 
                #~ source_path=source_path,
                #~ 'input_encoding': input_encoding)
    
    parts = core.publish_parts(source=input_string, 
        source_path=source_path,
        #~ writer_name='latex2e', 
        writer_name='latex2e', 
        settings_overrides=overrides)
    return parts
    #~ print parts.keys()
    #~ f = file('tmp.txt','w')
    #~ f.write(repr(parts.keys())+'\n\n')
    #~ f.write(repr(parts))
    #~ f.close()
    #~ return parts['body']
    
    
  


if __name__ == '__main__':
    test = u"""
Test example
============

This is a reST__ document containg non-ascii latin-1 chars::

  Ä Ë Ï Ö Ü 
  ä ë ï ö ü ÿ
  à è ì ò ù 
  á é í ó ú
  ã õ ñ 
  ç ß 

__ http://docutils.sf.net/rst.html

A list:

  - item 1
  - item 2
  - item 3


"""
    print restify(test)
    #~ print latex_body(test)



