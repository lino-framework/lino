## Copyright 2003-2005 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


import re
from lino.misc.txt2html import txt2html

class MemoParser:

    def __init__(self,cmds):
        self.cmds = cmds

    def parse(self,renderer,txt):

        if txt.startswith("#raw"):
            txt = txt[4:]
            
        #if False:
        #   txt = reSTify(txt)
        #else:
        #   txt = txt2html(txt) 

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
                    #   renderer.write(txt2html(piece + " returned " + repr(renderText)))
            renderer.write(txt2html(line) + '\n')
            # self.write(line + '</p>\n')

        #return self.html

    #def write(self,txt):
    #   self.html += txt

if __name__ == "__main__":
    
    p = MemoParser({})
    print p.parse(r"""This is a [ref http://www.foo.bar/very/\
    long/\
    filename.html reference with a long URL].
    """)
