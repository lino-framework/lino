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

#~ import functional
import os
from optparse import make_option 

from Cheetah.Template import Template as CheetahTemplate

from django.db import models
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import loading
#~ from django.db import models
#~ from django.contrib.contenttypes.models import ContentType
#~ from lino.core import actors
#~ from lino.utils import get_class_attr


import lino
from lino.core.coretools import app_labels
#~ from lino.utils import *
from lino.utils.config import find_config_file
from lino.utils import rstgen 

# http://snippets.dzone.com/posts/show/2375
curry = lambda func, *args, **kw:\
            lambda *p, **n:\
                 func(*args + p, **dict(kw.items() + n.items()))


class Command(BaseCommand):
    help = """Writes a Sphinx documentation tree about models on this Site.
    """
    
    args = "output_dir"
    
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
    ) 
    
    #~ def handle(self, *args, **options):
    def handle(self, output_dir, **options):
        #~ if len(args) != 1:
            #~ raise CommandError("Requires exactly 1 argument")
            
        #~ self.output_dir = os.path.abspath(args[0])
        self.output_dir = os.path.abspath(output_dir)
        self.generated_count = 0
        
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
        
        #~ if os.path.exists(fn):
            #~ logger.info("Skipping %s because file exists.",fn)
            #~ return 
        
        logger.info("Generating %s from %s",fn,tplname)
        context.update(
          lino=lino,
          #~ models=models,
          settings=settings,
          header=rstgen.header,
          h1=curry(rstgen.header,1),
          table=rstgen.table,
          py2rst=rstgen.py2rst,
          app_labels=app_labels)
        #~ d = dict(site=site)
        #~ print 20110223, [m for m in models.get_models()]
        tpl = CheetahTemplate(file(tpl_filename).read(),namespaces=[context])
        s = unicode(tpl)
        #~ print s
        file(fn,'w').write(s.encode('utf-8'))
        self.generated_count += 1
        
