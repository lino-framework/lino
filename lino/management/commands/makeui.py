# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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
Generate the local files for running :mod:`lino.ui.qx`.
"""

import logging
logger = logging.getLogger(__name__)

import sys
import os
from os.path import join, dirname
from optparse import make_option 
import codecs
import subprocess
import re
from shutil import copytree, rmtree

#~ from Cheetah.Template import Template as CheetahTemplate

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

import lino
from lino import reports
from lino.core.coretools import app_labels
from lino.utils import confirm
from lino.utils.config import find_config_file
from lino.utils import rstgen 
from lino.utils import babel
from lino.utils.menus import Menu, MenuItem
#~ from lino.utils.jsgen import py2js
from lino.utils import jsgen
from lino.tools import makedirs_if_missing
from lino.management.commands.makedocs import GeneratingCommand

def a2class(a):
    #~ return 'lino.%s' % a
    return 'lino.%s_%s_%s' % (a.actor.app_label,a.actor._actor_name,a.name)
    
    
#~ from django.utils.importlib import import_module
#~ m = import_module(settings.ROOT_URLCONF)    
#~ m.ui.make_local_files()
    
class Command(GeneratingCommand):
    help = """Writes files (.js, .html, .css) for this Site.
    """
    
    def handle(self, *args, **options):
        #~ options.update(output_dir=QXAPP_PATH)
        if args:
            print "Warning : ignored arguments", args
        QXAPP_PATH = os.path.join(settings.QOOXDOO_PATH,'lino_apps',settings.LINO.project_name)    
        args = [QXAPP_PATH]
        super(Command,self).handle(*args, **options)
        
        args = [ sys.executable ]
        args.append(os.path.join(settings.QOOXDOO_PATH, 'tool', 'bin', 'generator.py'))
        args.append('source')
        args.append('build')
        os.chdir(self.output_dir)
        subprocess.call(args)
        
    def generate_files(self):
        settings.LINO.setup()
        from lino.ui import qx
        src = join(dirname(qx.__file__),'qxapp_init','source')
        dest = join(self.output_dir,'source')
        #~ dest = join(self.output_dir,'qxapp','source')
        if os.path.exists(dest):
            rmtree(dest)
        copytree(src,dest)
        self.tmpl_dir = join(dirname(qx.__file__),'tmpl')
        from lino.ui.qx.urls import ui
        context = dict(
          py2js=jsgen.py2js,
          jsgen=jsgen,
          a2class=a2class,
          models=models,settings=settings)
        for fn in ('config.json','generate.py','Manifest.json'):
        #~ for fn in ('config.json',):
            self.generate(fn+'.tmpl',
                join(self.output_dir,fn),**context)
                #~ join(self.output_dir,'qxapp',fn),**context)
            
        self.generate_class_file('lino.Application','Application.js.tmpl',**context)
        #~ self.generate('Application',application_lines(self))
        for rpt in (reports.master_reports 
          + reports.slave_reports 
          + reports.generic_slaves.values()):
            rh = rpt.get_handle(ui) 
            #~ js += "Ext.namespace('Lino.%s')\n" % rpt
            #~ f.write("Ext.namespace('Lino.%s')\n" % rpt)
            context.update(rh=rh)
            for a in rpt.get_actions():
                if isinstance(a,reports.GridEdit):
                    context.update(action=a)
                    self.generate_class_file(a2class(a),'XyzTableWindow.js.tmpl',**context)
                if isinstance(a,reports.ShowDetailAction):
                    context.update(action=a)
                    self.generate_class_file(a2class(a),
                        'XyzDetailWindow.js.tmpl',
                        **context)
        for d in (join(self.output_dir,'source','translation'),
                  join(self.output_dir,'source','script'),
                  join(self.output_dir,'source','resource','lino')):
            makedirs_if_missing(d)            
            
        


    #~ def generate(self,fn,lines):
    def generate_class_file(self,class_name,tpl,**kw):
        assert class_name.startswith("lino."), class_name
        #~ class_name = "lino." + class_name
        fn = class_name.replace('.',os.path.sep)
        fn += '.js'
        fn = os.path.join(self.output_dir,'source','class',fn)
        kw.update(class_name=class_name)
        self.generate(tpl,fn,**kw)
        #~ os.makedirs(os.path.dirname(fn))
        #~ fd = codecs.open(fn,'w',encoding='UTF-8')
        #~ for ln in lines:
            #~ fd.write(ln + "\n")
        #~ fd.close()
        #~ self.generated_count += 1
        

        
