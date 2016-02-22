# -*- coding: UTF-8 -*-
# Copyright 2006-2016 Luc Saffre
# License: BSD (see file COPYING for details)

r""" A simple markup parser that expands "commands" found in an input
string to produce a resulting output string.  Commands are in the form
``[KEYWORD ARGS]``.  The caller defines itself all commands, there are
no predefined commands.

..  This document is part of the Lino test suite. You can test only
    this document with::

        $ python setup.py test -s tests.UtilsTests.test_memo


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
message is inserted into the result.  The whole traceback is being
logged to the lino logger.

To demonstrate this, our example implementation has a bug, it doesn't
support the case of having only an URL without TEXT:

>>> print(p.parse('This is a [url http://xyz.com].'))
[DEBUG] url2html() got 'http://xyz.com'
This is a [ERROR need more than 1 value to unpack in '[url http://xyz.com]' at position 10-30].

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
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)


import re
COMMAND_REGEX = re.compile(r"\[(\w+)\s*((?:[^[\]]|\[.*?\])*?)\]")
#                                       ===...... .......=

EVAL_REGEX = re.compile(r"\[=((?:[^[\]]|\[.*?\])*?)\]")

from lino.utils.xmlgen import etree


class Parser(object):

    safe_mode = False

    def __init__(self, **context):
        self.commands = dict()
        self.context = context

    def register_command(self, cmd, func):
        self.commands[cmd] = func

    def eval_match(self, matchobj):
        expr = matchobj.group(1)
        try:
            return self.format_value(eval(expr, self.context))
        except Exception as e:
            logger.exception(e)
            return self.handle_error(matchobj, e)

    def format_value(self, v):
        if etree.iselement(v):
            return str(etree.tostring(v))
        return str(v)

    def cmd_match(self, matchobj):
        cmd = matchobj.group(1)
        params = matchobj.group(2)
        params = params.replace('\\\n', '')
        cmdh = self.commands.get(cmd, None)
        if cmdh is None:
            return matchobj.group(0)
        try:
            return self.format_value(cmdh(self, params))
        except Exception as e:
            logger.exception(e)
            return self.handle_error(matchobj, e)

    def handle_error(self, mo, e):
        #~ return mo.group(0)
        msg = "[ERROR %s in %r at position %d-%d]" % (
            e, mo.group(0), mo.start(), mo.end())
        logger.error(msg)
        return msg

    def parse(self, s, **context):
        #~ self.context = context
        self.context.update(context)
        s = COMMAND_REGEX.sub(self.cmd_match, s)
        if not self.safe_mode:
            s = EVAL_REGEX.sub(self.eval_match, s)
        return s


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
