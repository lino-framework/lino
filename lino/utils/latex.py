## Copyright 2009 Luc Saffre
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

"""
Based on http://www.djangosnippets.org/snippets/102/

Added by LS:

20090621
- template can now also be a list or tuple of filenames
- renamed parameter "type" to "outtype" 
- support for templates containing non-ascii data

"""
import subprocess 
from subprocess import call, PIPE
#from os import remove, rename
import os
#from os.path import dirname
import tempfile #from tempfile import NamedTemporaryFile
from django.template import loader, Context

def process_latex(template, context={}, outtype='pdf', outfile=None):
    """
    Processes a template as a LaTeX source file.
    Output is either being returned or stored in outfile.
    At the moment only pdf output is supported.
    """
    if type(template) in (list, tuple):
        t = loader.select_template(template)
    else:
        t = loader.get_template(template)
    c = Context(context)
    r = t.render(c)
    r = r.encode("utf-8")
    fd,base = tempfile.mkstemp() # NamedTemporaryFile(delete=False)
    tex = os.fdopen(fd)
    tex.write(r)
    #tex.flush()
    #base = tex.name
    #print "base:",base
    tex.close()
    items = "log aux pdf dvi png".split()
    names = dict((x, '%s.%s' % (base, x)) for x in items)
    output = names[outtype]

    if outtype == 'pdf' or outtype == 'dvi':
        pdflatex(base, outtype)
    elif outtype == 'png':
        pdflatex(base, 'dvi')
        call(['dvipng', '-bg', '-transparent',
              names['dvi'], '-o', names['png']],
              cwd=os.path.dirname(base), 
              stdout=PIPE, stderr=PIPE)

    os.remove(names['log'])
    os.remove(names['aux'])
    os.remove(base)

    if not outfile:
        o = file(output).read()
        os.remove(output)
        return o
    else:
        os.rename(output, outfile)

def pdflatex(outfile, outtype='pdf'):
    dirname,filename = os.path.split(outfile)
    print "dirname:", dirname
    print "filename:", filename
    subprocess.check_call(
      ['pdflatex', '-interaction=nonstopmode',
                            '-output-format', outtype, 
                            filename],
               cwd=dirname) #, stdout=PIPE, stderr=PIPE)
