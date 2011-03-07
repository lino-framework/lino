# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)

import os
from optparse import make_option 

from Cheetah.Template import Template as CheetahTemplate

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode 
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import loading
#~ from django.db import models
#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.core import actors
#~ from lino.utils import get_class_attr

import re
import lino
from lino.core.coretools import app_labels
from lino.utils import confirm
from lino.utils.config import find_config_file
from lino.utils import rstgen 
from lino.utils import babel

# http://snippets.dzone.com/posts/show/2375
curry = lambda func, *args, **kw:\
            lambda *p, **n:\
                 func(*args + p, **dict(kw.items() + n.items()))
                 
# Copied from doctest:

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
        return s
    s = s.expandtabs()
    # If all lines begin with the same indentation, then strip it.
    mi = min_indent(s)
    if mi > 0:
        s = '\n'.join([l[mi:] for l in s.split('\n')])
    return s



def model_overview(model):
    headers = ["name","type"]
    #~ formatters = [
      #~ lambda f: f.name,
      #~ lambda f: f.__class__.__name__,
    #~ ]
    headers.append("verbose name")
    #~ for lng in babel.AVAILABLE_LANGUAGES:
        #~ headers.append("verbose name (" + lng + ")")
    #~ headers.append("help text")
    #~ formatters.append(lambda f: f.help_text)
    def verbose_name(f):
        babel.set_language('en')
        label_en = force_unicode(_(f.verbose_name))
        babel_labels = []
        for lng in babel.AVAILABLE_LANGUAGES:
            if lng != 'en':
                babel.set_language(lng)
                label = force_unicode(_(f.verbose_name))
                if label != label_en:
                    babel_labels.append(label)
        if babel_labels:
            label_en += " (%s)" % ",".join(babel_labels)
        return label_en
        
    def rowfmt(f):
        cells = [
          f.name,
          f.__class__.__name__,
          verbose_name(f)
        ]
        #~ for lng in babel.AVAILABLE_LANGUAGES:
            #~ babel.set_language(lng)
            #~ cells.append(force_unicode(_(f.verbose_name)))
        #~ cells.append(f.help_text)
        return cells
    rows = [ rowfmt(f) for f in model._meta.fields ]
    return rstgen.table(headers,rows)
  

class Command(BaseCommand):
    help = """Writes a Sphinx documentation tree about models on this Site.
    """
    
    args = "output_dir"
    
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', 
            dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
        make_option('--overwrite', action='store_true', 
            dest='overwrite', default=False,
            help='Overwrite existing files.'),
    ) 
    
    #~ def handle(self, *args, **options):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("No output_dir specified.")
            
        self.output_dir = os.path.abspath(args[0])
        #~ self.overwrite
        #~ self.output_dir = os.path.abspath(output_dir)
        self.generated_count = 0
        self.options = options
        
        logger.info("Running Lino autodoc to %s.", self.output_dir)
            
        #~ fd = codecs.open(fn,'w',encoding='UTF-8')
        
        self.generate('index.rst.tmpl','index.rst')
        for a in loading.get_apps():
            app_label = a.__name__.split('.')[-2]
            self.generate('app.rst.tmpl','%s.rst' % app_label, 
                app=a, 
                app_label=app_label, 
                models=models.get_models(a,include_auto_created=True),
                )
        logger.info("Generated %s files",self.generated_count)
            
    def generate(self,tplname,fn,**context):

        tplname = 'makedocs/' + tplname
        tpl_filename = find_config_file(tplname)
        if tpl_filename is None:
            raise Exception("No file %s found" % tplname)
            
        fn = os.path.join(self.output_dir,fn)
        
        if os.path.exists(fn) and not self.options.get('overwrite'):
            if not confirm("Overwrite existing file %s (y/n) ?" % fn):
                logger.info("Skipping %s because file exists.",fn)
                return 
        
        logger.info("Generating %s from %s",fn,tplname)
        context.update(
          lino=lino,
          #~ models=models,
          settings=settings,
          header=rstgen.header,
          h1=curry(rstgen.header,1),
          table=rstgen.table,
          doc=doc2rst,
          #~ py2rst=rstgen.py2rst,
          model_overview=model_overview,
          app_labels=app_labels)
        #~ d = dict(site=site)
        #~ print 20110223, [m for m in models.get_models()]
        tpl = CheetahTemplate(file(tpl_filename).read(),namespaces=[context])
        s = unicode(tpl)
        #~ print s
        file(fn,'w').write(s.encode('utf-8'))
        self.generated_count += 1
        
