# -*- coding: UTF-8 -*-
# Copyright 2006-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

r""" A simple markup parser that expands "commands" found in an input
string to produce a resulting output string.  Commands are in the form
``[KEYWORD ARGS]``.  The caller defines itself all commands, there are
no predefined commands.

..  This document is part of the Lino test suite.  You can test it
    individually with::

        $ doctest lino/utils/memo.py

A concrete real-world specification is in :doc:`/specs/noi/memo`


Usage example
-------------

Instantiate a parser:

>>> from lino.utils.memo import Parser
>>> p = Parser()

We declare a "command handler" function `url2html` and register it:

>>> def url2html(parser, s):
...     print("[DEBUG] url2html() got %r" % s)
...     if not s: return "XXX"
...     url, text = s.split(None,1)
...     return '<a href="%s">%s</a>' % (url,text)
>>> p.register_command('url', url2html)

The intended usage of our example handler is ``[url URL TEXT]``, where
URL is the URL to link to, and TEXT is the label of the link:

>>> print(p.parse('This is a [url http://xyz.com test].'))
[DEBUG] url2html() got 'http://xyz.com test'
This is a <a href="http://xyz.com">test</a>.


A command handler will be called with one parameter: the portion of
text between the KEYWORD and the closing square bracket.  Not
including the whitespace after the keyword.  It must return the text
which is to replace the ``[KEYWORD ARGS]`` fragment.  It is
responsible for parsing the text that it receives as parameter.

If an exception occurs during the command handler, the final exception
message is inserted into the result.  

To demonstrate this, our example implementation has a bug, it doesn't
support the case of having only an URL without TEXT (we use an
ellipsis because the error message varies with Python versions):

>>> print(p.parse('This is a [url http://xyz.com].'))  #doctest: +ELLIPSIS
[DEBUG] url2html() got 'http://xyz.com'
This is a [ERROR ... in ...'[url http://xyz.com]' at position 10-30].


Newlines preceded by a backslash will be removed before the command
handler is called:

>>> print(p.parse('''This is [url http://xy\
... z.com another test].'''))
[DEBUG] url2html() got 'http://xyz.com another test'
This is <a href="http://xyz.com">another test</a>.

The whitespace between the KEYWORD and ARGS can be any whitespace,
including newlines:

>>> print(p.parse('''This is a [url
... http://xyz.com test].'''))
[DEBUG] url2html() got 'http://xyz.com test'
This is a <a href="http://xyz.com">test</a>.

The ARGS part is optional (it's up to the command handler to react
accordingly, our handler function returns XXX in that case):

>>> print(p.parse('''This is a [url] test.'''))
[DEBUG] url2html() got ''
This is a XXX test.

The ARGS part may contain pairs of square brackets:

>>> print(p.parse('''This is a [url 
... http://xyz.com test with [more] brackets].'''))
[DEBUG] url2html() got 'http://xyz.com test with [more] brackets'
This is a <a href="http://xyz.com">test with [more] brackets</a>.

Fragments of text between brackets that do not match any registered
command will be left unchanged:

>>> print(p.parse('''This is a [1] test.'''))
This is a [1] test.

>>> print(p.parse('''This is a [foo bar] test.'''))
This is a [foo bar] test.

>>> print(p.parse('''Text with only [opening square bracket.'''))
Text with only [opening square bracket.

Special handling
----------------

Leading and trailing spaces are always removed from command text:

>>> print(p.parse("[url http://example.com Trailing space  ]."))
[DEBUG] url2html() got 'http://example.com Trailing space'
<a href="http://example.com">Trailing space</a>.

>>> print(p.parse("[url http://example.com   Leading space]."))
[DEBUG] url2html() got 'http://example.com   Leading space'
<a href="http://example.com">Leading space</a>.

Non-breaking and zero-width spaces are treated like normal spaces:

>>> print(p.parse(u"[url\u00A0http://example.com example.com]."))
[DEBUG] url2html() got 'http://example.com example.com'
<a href="http://example.com">example.com</a>.

>>> print(p.parse(u"[url \u200bhttp://example.com example.com]."))
[DEBUG] url2html() got 'http://example.com example.com'
<a href="http://example.com">example.com</a>.

>>> print(p.parse(u"[url&nbsp;http://example.com example.com]."))
[DEBUG] url2html() got 'http://example.com example.com'
<a href="http://example.com">example.com</a>.

Limits
------

A single closing square bracket as part of ARGS will not produce the
desired result:

>>> print(p.parse('''This is a [url
... http://xyz.com The character "\]"].'''))
[DEBUG] url2html() got 'http://xyz.com The character "\\'
This is a <a href="http://xyz.com">The character "\</a>"].

Execution flow statements like `[if ...]` and `[endif ...]` or ``[for
...]`` and ``[endfor ...]`` would be nice.



The ``[=expression]`` form
--------------------------

Instantiate a new parser with and without a context:

>>> print(p.parse('''\
... The answer is [=a*a*5-a].''', a=3))
The answer is 42.

>>> print(p.parse('''<ul>[="".join(['<li>%s</li>' % (i+1) for i in range(5)])]</ul>'''))
<ul><li>1</li><li>2</li><li>3</li><li>4</li><li>5</li></ul>

"""
from __future__ import unicode_literals

from builtins import str
from builtins import object
import logging ; logger = logging.getLogger(__name__)
# from inspect import getsourcefile
import re
import inspect

from etgen import etree


COMMAND_REGEX = re.compile(r"\[(\w+)\s*((?:[^[\]]|\[.*?\])*?)\]")
#                                       ===...... .......=

EVAL_REGEX = re.compile(r"\[=((?:[^[\]]|\[.*?\])*?)\]")

class Parser(object):
    """The memo parser. """

    safe_mode = False

    def __init__(self, **context):
        self.commands = dict()
        self.context = context
        self.renderers = dict()

    def register_command(self, cmd, func):
        # print("20170210 register_command {} {}".format(cmd, func))
        self.commands[cmd] = func

    def register_renderer(self, cl, func):
        # print("20181205", str(cl))
        # if str(cl).endswith("Person'>"):
        #     raise Exception("20181205")

        frame, filename, line_number, function_name, lines, index = \
        inspect.stack()[2]
        # print(frame, filename, line_number, function_name, lines, index)
        func._defined_in = "function {} in {}".format(function_name, filename)

        if cl in self.renderers:
            def fmt(x):
                return x._defined_in
            ex = self.renderers[cl]
            raise Exception(
                "Duplicate renderer for %s : %s and %s", cl, fmt(ex), fmt(func))
        self.renderers[cl] = func

    def register_django_model(
            self, name, model, cmd=None, rnd=None, title=str):
        """
        Register the given string `name` as command for referring to
        database rows of the given Django database model `model`.

        Optional keyword arguments are 

        - `cmd` the command handler used by :meth:`parse`
        - `rnd` the renderer function for :meth:`obj2memo`
        - `title` a function which returns a string to be used as title
        """
        # print("20170210 register_django_model {} {}".format(name, model))
        if rnd is None:
            def rnd(obj):
                return "[{} {}] ({})".format(name, obj.id, title(obj))
        if cmd is None:
            def cmd(parser, s):
                """
Insert a reference to the specified database object.

The first argument is mandatory and specifies the primary key.
All remaining arguments are used as the text of the link.

                """
                args = s.split(None, 1)
                if len(args) == 1:
                    pk = s
                    txt = None
                else:
                    pk = args[0]
                    txt = args[1]

                ar = parser.context['ar']
                kw = dict()
                # dd.logger.info("20161019 %s", ar.renderer)
                pk = int(pk)
                obj = model.objects.get(pk=pk)
                # try:
                # except model.DoesNotExist:
                #     return "[{} {}]".format(name, s)
                if txt is None:
                    txt = "#{0}".format(obj.id)
                    kw.update(title=title(obj))
                e = ar.obj2html(obj, txt, **kw)
                # return str(ar)
                return etree.tostring(e)

        self.register_command(name, cmd)
        self.register_renderer(model, rnd)
            
        
    def eval_match(self, matchobj):
        expr = matchobj.group(1)
        try:
            return self.format_value(eval(expr, self.context))
        except Exception as e:
            # don't log an exception because that might cause lots of
            # emails to the admins.
            # logger.warning(e)
            return self.handle_error(matchobj, e)

    def format_value(self, v):
        if etree.iselement(v):
            return str(etree.tostring(v))
        return str(v)

    def cmd_match(self, matchobj):
        cmd = matchobj.group(1)
        cmdh = self.commands.get(cmd, None)
        if cmdh is None:
            return matchobj.group(0)
        
        params = matchobj.group(2)
        params = params.replace('\\\n', ' ')
        params = params.replace(u'\xa0', ' ')
        params = params.replace(u'\u200b', ' ')
        params = params.replace('&nbsp;', ' ')
        params = str(params.strip())
        try:
            return self.format_value(cmdh(self, params))
        except Exception as e:
            # logger.warning(e)
            # don't log an exception because that might cause lots of
            # emails to the admins.
            return self.handle_error(matchobj, e)

    def handle_error(self, mo, e):
        #~ return mo.group(0)
        msg = "[ERROR %s in %r at position %d-%d]" % (
            e, mo.group(0), mo.start(), mo.end())
        # logger.debug(msg)
        return msg

    def parse(self, s, **context):
        """
        Parse the given string `s`, replacing memo commands by their
        result.
        """
        #~ self.context = context
        self.context.update(context)
        s = COMMAND_REGEX.sub(self.cmd_match, s)
        if not self.safe_mode:
            s = EVAL_REGEX.sub(self.eval_match, s)
        return s

    def obj2memo(self, obj, **options):
        """Render the given database object as memo markup.

        This works only for objects for which there is a renderer.
        Renderers are defined by :meth:`register_renderer`.

        """
        h = self.renderers.get(obj.__class__)
        if h is None:
            return "**{}**".format(obj)
        return h(obj, **options)
        

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
