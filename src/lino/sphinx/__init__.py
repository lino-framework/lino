## Copyright 2009 Luc Saffre

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

from docutils import nodes, utils
import posixpath

def srcref_role(typ, rawtext, etext, lineno, 
               inliner, options={}, content=[]):
    env = inliner.document.settings.env
    baseuri = env.config.srcref_base_uri
    text = utils.unescape(etext)
    refnode = nodes.reference('', '', refuri=posixpath.join(baseuri, text))
    refnode += nodes.literal(text, text)
    return [refnode], []
    
# 20081226 21:01 Georg Brandl in sphinx-dev@googlegroups.com:
# may cause UnicodeEncodeError if non-asci section headers exist
from itertools import groupby
def handle_finished(app, error):
    labels = app.builder.env.labels.items()
    labels.sort(key=lambda x: x[1])
    outfile = open(os.path.join(app.builder.srcdir, 'labels.txt'), 'w')
    for docname, items in groupby(labels, key=lambda x: x[1][0]):
        outfile.write('Labels in %s\n%s\n' % (
          docname, '-' * (len(docname) + 10)))
        for label in items:
            outfile.write('%s %s\n' % (
              label[0].ljust(30), label[1][2]))
        outfile.write('\n')
    outfile.close()

def setup(app):
    app.add_role('srcref', srcref_role)
    app.add_config_value('srcref_base_uri', 
      'http://example.com/source', True)
    app.add_description_unit('xfile','xfile',
      'pair: %s; file')
    app.add_description_unit('parsercmd','parsercmd',
      'pair: %s; parser command')
    app.add_description_unit('configcmd','configcmd',
      'pair: %s; configuration command')
    app.add_description_unit('staticmod','staticmod',
      'pair: %s; static module')
    #app.connect('build-finished', handle_finished)
    