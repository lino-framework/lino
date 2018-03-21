# -*- coding: UTF-8 -*-
"""Just a copy & paste of the :mod:`docutils.examples` module (as
instructed there).

:func:`restify` is an alias for :func:`html_body`.

:func:`latex_body` deduced from :func:`html_body`.

"""
from __future__ import print_function

#~ import traceback
from docutils import core, io, nodes, utils


# Copied from doctest:
import re
# This regular expression finds the indentation of every non-blank
# line in a string.
_INDENT_RE = re.compile('^([ ]*)(?=\S)', re.MULTILINE)


def min_indent(s):
    "Return the minimum indentation of any non-blank line in `s`"
    indents = [len(indent) for indent in _INDENT_RE.findall(s)]
    if len(indents) > 0:
        return min(indents)
    else:
        return 0


def doc2rst(s):
    if s is None:
        return u''
    s = s.expandtabs()
    # If all lines begin with the same indentation, then strip it.
    mi = min_indent(s)
    if mi > 0:
        s = '\n'.join([l[mi:] for l in s.split('\n')])
    return s


def abstract(o, indent=0):
    s = doc2rst(o.__doc__).strip()
    if not s:
        return '(no docstring)'
    paras = s.split('\n\n', 1)
    par = paras[0]
    if indent:
        par = (' ' * indent).join(par.splitlines())
    return par


#~ from docutils.parsers.rst import roles
#~ def doc_role(typ, rawtext, text, lineno, inliner,
             #~ options={}, content=[]):
    #~ node = nodes.reference(rawtext, reftype=role, refdomain=domain,
                                 #~ refexplicit=has_explicit_title)
    #~ return [node], []
#~ roles.register_local_role('doc', docrole)
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

    # settings_default_overrides = dict(newlines=False)

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = HTMLTranslator


# simply importing the sphinx.roles module causes these text roles to
# be installed:

import sphinx.roles

from docutils.parsers.rst import roles

try:
    from sphinx.util.nodes import split_explicit_title
except ImportError:  # sphinx 0.6.6 didn't have this
    import re
    explicit_title_re = re.compile(r'^(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)

    def split_explicit_title(text):
        """Split role content into title and target, if given."""
        match = explicit_title_re.match(text)
        if match:
            return True, match.group(1), match.group(2)
        return False, text, text


def install_sphinx_emu():
    """
    install some roles to emulate sphinx.
    """
    def mod_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
        has_explicit_title, title, target = split_explicit_title(text)
        ref = 'http://not_implemented/' + target
        return [nodes.reference(rawtext, utils.unescape(title), refuri=ref,
                                **options)], []
    roles.register_local_role('mod', mod_role)

    def class_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
        has_explicit_title, title, target = split_explicit_title(text)
        ref = 'http://not_implemented/' + target
        return [nodes.reference(rawtext, utils.unescape(title), refuri=ref,
                                **options)], []
    roles.register_local_role('class', class_role)

    def srcref_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
        has_explicit_title, title, target = split_explicit_title(text)
        ref = 'http://not_implemented/' + target
        return [nodes.reference(rawtext, utils.unescape(title), refuri=ref,
                                **options)], []
    roles.register_local_role('srcref', srcref_role)

#~ import sphinx
#~ print sphinx.__file__


def restify(input_string, source_path=None, destination_path=None,
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
    return fragment  #.decode('utf8')


def rst2odt(input_string, source_path=None, destination_path=None,
            input_encoding='unicode', doctitle=1, initial_header_level=1):
    """
    Renders the given reST string into ODT xml.
    """
    from docutils.writers.odf_odt import Writer, Reader

    class MyWriter(Writer):

        def assemble_my_parts(self):
            writers.Writer.assemble_parts(self)
            self.parts['content'] = self.visitor.content_astext()
            #~ f = tempfile.NamedTemporaryFile()
            #~ zfile = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
            #~ content = self.visitor.content_astext()
            #~ self.write_zip_str(zfile, 'content.xml', content)
            #~ self.write_zip_str(zfile, 'mimetype', self.MIME_TYPE)
            #~ s1 = self.create_manifest()
            #~ self.write_zip_str(zfile, 'META-INF/manifest.xml', s1)
            #~ s1 = self.create_meta()
            #~ self.write_zip_str(zfile, 'meta.xml', s1)
            #~ s1 = self.get_stylesheet()
            #~ self.write_zip_str(zfile, 'styles.xml', s1)
            #~ s1 = self.get_settings()
            #~ self.write_zip_str(zfile, 'settings.xml', s1)
            #~ self.store_embedded_files(zfile)
            #~ zfile.close()
            #~ f.seek(0)
            #~ whole = f.read()
            #~ f.close()
            #~ self.parts['whole'] = whole
            #~ self.parts['encoding'] = self.document.settings.output_encoding
            #~ self.parts['version'] = docutils.__version__

    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer=MyWriter(),
        reader=Reader(),
        settings_overrides=overrides)
    print(20120311, list(parts.keys()))
    print(20120311, parts['content'])
    raise Exception("20120311")
    fragment = parts['whole']
    fragment = parts['html_body']
    #~ if output_encoding != 'unicode':
        #~ fragment = fragment.encode(output_encoding)
    #~ print __file__, repr(fragment)
    return fragment


def old_restify(s, **kw):
    """
    (Didn't work when the reST text contained a root title).
    See :blogref:`20110525`.
    """
    html = html_body(s, **kw)
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
    returns a dict containing the following keys:

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
  
A table:

  =========== ===========================
  terav       pehme
  =========== ===========================
  **s**\ upp  **z**\ oom
  **š**\ okk  **ž**\ urnaal, **ž**\ anre
  =========== ===========================



"""
    print(rst2odt(test))
    #~ print restify(test)
    #~ print latex_body(test)
