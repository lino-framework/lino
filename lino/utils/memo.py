# -*- coding: UTF-8 -*-
## Copyright 2006-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

r"""
``memo`` is a simple universal markup parser that expands "commands" 
found in an input string to produce a resulting output string. 
Commands are in the form ``[KEYWORD ARGS]``. 
The caller defines itself all commands, there are no predefined commands.

Usage example
-------------

Instatiate a parser:

>>> p = Parser()

We declare a "command handler" function `url2html` and register it:

>>> def url2html(s):
...     print "[DEBUG] url2html() got %r" % s
...     if not s: return "XXX"
...     url,text = s.split(None,1)
...     return '<a href="%s">%s</a>' % (url,text)
>>> p.register_command('url',url2html)

The intended usage of our example handler is 
``[url URL TEXT]``, where URL is the URL 
to link to, and TEXT is the label of the link:

>>> print p.parse('This is a [url http://xyz.com test].')
[DEBUG] url2html() got 'http://xyz.com test'
This is a <a href="http://xyz.com">test</a>.


A command handler will be called with one parameter:
the portion of text between the KEYWORD and the 
closing square bracket. Not including the whitespace 
after the keyword.
It must return the text which is to replace 
the ``[KEYWORD ARGS]`` fragment.
It is responsible for parsing 
the text that it receives as parameter.
Our example implementation has a bug, 
it doesn't support the case of having only an URL without TEXT:

>>> print p.parse('This is a [url http://xyz.com].')
[DEBUG] url2html() got 'http://xyz.com'
This is a [ERROR need more than 1 value to unpack in '[url http://xyz.com]' at position 10-30].

Newlines preceded by a backslash will be removed 
before the command handler is called:

>>> print p.parse('''This is [url http://xy\
... z.com another test].''')
[DEBUG] url2html() got 'http://xyz.com another test'
This is <a href="http://xyz.com">another test</a>.

The whitespace between the KEYWORD and ARGS can be any 
whitespace, including newlines:

>>> print p.parse('''This is a [url 
... http://xyz.com test].''')
[DEBUG] url2html() got 'http://xyz.com test'
This is a <a href="http://xyz.com">test</a>.

The ARGS part is optional
(it's up to the command handler to react accordingly,
our handler function returns XXX in that case):

>>> print p.parse('''This is a [url] test.''')
[DEBUG] url2html() got ''
This is a XXX test.

The ARGS part may contain pairs of square brackets:

>>> print p.parse('''This is a [url 
... http://xyz.com test with [more] brackets].''')
[DEBUG] url2html() got 'http://xyz.com test with [more] brackets'
This is a <a href="http://xyz.com">test with [more] brackets</a>.


Fragments of text between brackets that do not match 
any registered command will be left unchanged:

>>> print p.parse('''This is a [1] test.''')
This is a [1] test.

>>> print p.parse('''This is a [foo bar] test.''')
This is a [foo bar] test.

>>> print p.parse('''Text with only [opening square bracket.''')
Text with only [opening square bracket.


Limits
------

A single closing square bracket as part of ARGS will not 
produce the desired result:

>>> print p.parse('''This is a [url 
... http://xyz.com The character "\]"].''')
[DEBUG] url2html() got 'http://xyz.com The character "\\'
This is a <a href="http://xyz.com">The character "\</a>"].

Built-in commands like `[if ...]`, `[endif ...]`, `[=<expression>]`,... 
would be nice.


"""

import re

REGEX = re.compile(r"\[(\w+)\s*((?:[^[\]]|\[.*?\])*?)\]")

class Parser(object):
  
    def __init__(self):
        self.commands = dict()

    def register_command(self,cmd,func):
        self.commands[cmd] = func

    def cmd_match(self,matchobj):
        cmd = matchobj.group(1)
        params = matchobj.group(2)
        params = params.replace('\\\n','')
        h = self.commands.get(cmd,None)
        if h is None:
            return matchobj.group(0)
        try:
            return h(params)
        #~ except KeyError,e:
        except Exception,e:
            return self.handle_error(matchobj,e)
            
    def handle_error(self,mo,e):
        #~ return mo.group(0)
        return "[ERROR %s in %r at position %d-%d]" %(
          e, mo.group(0), mo.start(),mo.end())
        

    def parse(self,s):
        s = REGEX.sub(self.cmd_match,s)
        return s


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

