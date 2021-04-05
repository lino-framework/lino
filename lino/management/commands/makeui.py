# -*- coding: UTF-8 -*-
# Copyright 2011 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Generate the local files for running :mod:`lino.ui.qx`.
"""
from __future__ import print_function

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
from django.utils.translation import gettext as _
from django.utils.encoding import force_str
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import loading

import lino
from lino.core import dbtables
from lino.core import kernel
from lino.core import actions
from lino.core.utils import app_labels
from lino.utils import confirm
import rstgen
from lino.core.menus import Menu, MenuItem
from lino.utils import jsgen
from lino.management.commands.makedocs import GeneratingCommand


def a2class(a):
    #~ return 'lino.%s' % a
    return 'lino.%s_%s_%s' % (a.actor.app_label, a.actor._actor_name, a.name)


#~ from importlib import import_module
#~ m = import_module(settings.ROOT_URLCONF)
#~ m.ui.make_local_files()

class Command(GeneratingCommand):
    help = """Writes files (.js, .html, .css) for this Site.
    """

    def handle(self, *args, **options):
        #~ options.update(output_dir=QXAPP_PATH)
        if args:
            print("Warning : ignored arguments", args)
        QXAPP_PATH = os.path.join(
            settings.QOOXDOO_PATH, 'lino_apps', settings.SITE.project_name)
        args = [QXAPP_PATH]
        super(Command, self).handle(*args, **options)

        args = [sys.executable]
        args.append(
            os.path.join(settings.QOOXDOO_PATH, 'tool', 'bin', 'generator.py'))
        args.append('source')
        args.append('build')
        os.chdir(self.output_dir)
        subprocess.call(args)

    def generate_files(self):
        settings.SITE.setup()
        from lino.ui import qx
        src = join(dirname(qx.__file__), 'qxapp_init', 'source')
        dest = join(self.output_dir, 'source')
        #~ dest = join(self.output_dir,'qxapp','source')
        if os.path.exists(dest):
            rmtree(dest)
        copytree(src, dest)
        self.tmpl_dir = join(dirname(qx.__file__), 'tmpl')
        from lino.ui.qx.urls import ui
        context = dict(
            py2js=jsgen.py2js,
            jsgen=jsgen,
            a2class=a2class,
            models=models, settings=settings)
        for fn in ('config.json', 'generate.py', 'Manifest.json'):
        #~ for fn in ('config.json',):
            self.generate(fn + '.tmpl',
                          join(self.output_dir, fn), **context)
                #~ join(self.output_dir,'qxapp',fn),**context)

        self.generate_class_file(
            'lino.Application', 'Application.js.tmpl', **context)
        #~ self.generate('Application',application_lines(self))
        for rpt in (kernel.master_tables
                    + kernel.slave_tables
                    + list(kernel.generic_slaves.values())):
            rh = rpt.get_handle()
            #~ js += "Ext.namespace('Lino.%s')\n" % rpt
            #~ f.write("Ext.namespace('Lino.%s')\n" % rpt)
            context.update(rh=rh)
            for a in rpt.get_actions():
                if isinstance(a, dbtables.ShowTable):
                    context.update(action=a)
                    self.generate_class_file(
                        a2class(a), 'XyzTableWindow.js.tmpl', **context)
                if isinstance(a, actions.ShowDetail):
                    context.update(action=a)
                    self.generate_class_file(a2class(a),
                                             'XyzDetailWindow.js.tmpl',
                                             **context)
        for d in (join(self.output_dir, 'source', 'translation'),
                  join(self.output_dir, 'source', 'script'),
                  join(self.output_dir, 'source', 'resource', 'lino')):
            settings.SITE.makedirs_if_missing(d)

    #~ def generate(self,fn,lines):
    def generate_class_file(self, class_name, tpl, **kw):
        assert class_name.startswith("lino."), class_name
        #~ class_name = "lino." + class_name
        fn = class_name.replace('.', os.path.sep)
        fn += '.js'
        fn = os.path.join(self.output_dir, 'source', 'class', fn)
        kw.update(class_name=class_name)
        self.generate(tpl, fn, **kw)
        #~ os.makedirs(os.path.dirname(fn))
        #~ fd = codecs.open(fn,'w',encoding='UTF-8')
        #~ for ln in lines:
            #~ fd.write(ln + "\n")
        #~ fd.close()
        #~ self.generated_count += 1
