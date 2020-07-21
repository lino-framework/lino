from builtins import str
# -*- coding: UTF-8 -*-
# Copyright 2011 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import logging
logger = logging.getLogger(__name__)

import os
import sys
from optparse import make_option
from os.path import join

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import loading

import lino
#from lino.core.utils import app_labels
from lino.utils import curry
import rstgen
from lino.utils.restify import doc2rst, abstract
from lino.core import kernel

from lino.api.dd import full_model_name


def fieldtype(f):
    if isinstance(f, models.ForeignKey):
        return f.__class__.__name__ + " to " + refto(f.remote_field.model)
    return f.__class__.__name__


def report_ref(rpt):
    return settings.SITE.source_name + '.' + str(rpt)
    #~ return ":ref:`%s.%s`" % (settings.SITE.source_name,str(rpt))


def model_ref(model):
    return settings.SITE.source_name + '.' + model._meta.app_label + '.' + model.__name__


def refto(x):
    if x is None:
        return '`None`'
    if issubclass(x, models.Model):
        return ':doc:`' + x.__name__ + ' <' + full_model_name(x) + '>`'
    #~ if isinstance(x,Field):
    return ':ref:`' + x.verbose_name + ' <' + settings.SITE.source_name \
        + '.' + full_model_name(x.model) + '.' + x.name + '>`'


def model_overview(model):
    headers = ["name", "type"]
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
        settings.SITE.set_language(None)
        label_en = force_text(_(f.verbose_name))
        babel_labels = []
        for lng in settings.SITE.languages[1:]:
            dbutils.set_language(lng.django_code)
            label = force_text(_(f.verbose_name))
            if label != label_en:
                babel_labels.append(label)
        if babel_labels:
            label_en += " (%s)" % ",".join(babel_labels)
        return label_en

    def rowfmt(f):
        cells = [
            f.name,
            fieldtype(f),
            verbose_name(f)
        ]
        #~ for lng in babel.AVAILABLE_LANGUAGES:
            #~ babel.set_language(lng)
            #~ cells.append(force_text(_(f.verbose_name)))
        #~ cells.append(f.help_text)
        return cells
    rows = [rowfmt(f) for f in model._meta.fields]
    s = rstgen.table(headers, rows)

    model_reports = [r for r in kernel.master_tables if r.model is model]
    if model_reports:
        s += '\n\nMaster tables: %s\n\n' % rptlist(model_reports)
    if getattr(model, '_lino_slaves', None):
        s += '\n\nSlave tables: %s\n\n' % rptlist(list(model._lino_slaves.values()))
        #~ s += '\n\nSlave reports: '
        #~ s += ', '.join([name for name,rpt in model._lino_slaves.items()])
        #~ s += '\n\n'
    return s


def rptlist(l):
    return ', '.join([
        ":ref:`%s (%s) <%s>`" % (str(rpt),
                                 force_text(rpt.label), report_ref(rpt))
        for rpt in l])


def model_referenced_from(model):
    #~ headers = ["name","description"]
    #~ rows = []
    def ddhfmt(ddh):
        return ', '.join([':ref:`%s.%s`' % (model_ref(model), fk.name)
                          for model, fk in ddh.fklist])
    return ddhfmt(model._lino_ddh)
    #~ rows.append(['_lino_ddh',ddhfmt(model._lino_ddh)])
    #~ return rstgen.table(headers,rows)


class GeneratingCommand(BaseCommand):
    tmpl_dir = ''
    args = "output_dir"

    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false',
                    dest='interactive', default=True,
                    help='Do not prompt for input of any kind.'),
        #~ make_option('--overwrite', action='store_true',
        #~ dest='overwrite', default=False,
        #~ help='Overwrite existing files.'),
    )

    def create_parser(self, prog_name, subcommand):
        self.subcommand = subcommand
        return super(GeneratingCommand, self).create_parser(prog_name, subcommand)

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("No output_dir specified.")

        self.output_dir = os.path.abspath(args[0])
        if not os.path.exists(self.output_dir):
            raise CommandError("Specified output_dir %s does not exist." %
                               self.output_dir)
        #~ self.overwrite
        #~ self.output_dir = os.path.abspath(output_dir)
        self.generated_count = 0
        self.options = options

        logger.info("Running %s to %s.", self, self.output_dir)
        self.generate_files()
        logger.info("Generated %s files", self.generated_count)

    def generate(self, tplname, fn, **context):
        from lino.api import rt
        from Cheetah.Template import Template as CheetahTemplate

        #~ if self.tmpl_dir:
            #~ tplname = join(self.tmpl_dir,tplname)
        #~ tplname = self.subcommand + '/' + tplname
        tpl_filename = rt.find_config_file(tplname, self.tmpl_dir)
        if tpl_filename is None:
            raise Exception("No file %s found" % tplname)
        if isinstance(tpl_filename, str):
            tpl_filename = tpl_filename.encode(sys.getfilesystemencoding())
        tpl_filename = os.path.abspath(tpl_filename)
        fn = join(self.output_dir, fn)

        #~ if os.path.exists(fn):
            #~ if not self.options.get('overwrite'):
                #~ if not confirm("Overwrite existing file %s (y/n) ?" % fn):
                    #~ logger.info("Skipping %s because file exists.",fn)
                    #~ return
        #~ else:
            #~ mkdir_if(os.path.dirname(fn))

        settings.SITE.makedirs_if_missing(os.path.dirname(fn))

        logger.info("Generating %s", fn)
        #~ logger.info("Generating %s from %s",fn,tpl_filename)

        def app_labels():
            return [p.app_label for p in settings.SITE.installed_plugins]
        context.update(
            lino=lino,
            #~ models=models,
            settings=settings,
            app_labels=app_labels)
        #~ d = dict(site=site)
        #~ print 20110223, [m for m in models.get_models()]
        #~ print 20110315, context
        tpl = CheetahTemplate(file=tpl_filename, namespaces=[context])
        #~ tpl = CheetahTemplate(file(tpl_filename).read(),namespaces=[context])
        s = str(tpl)
        #~ print s
        file(fn, 'w').write(s.encode('utf-8'))
        self.generated_count += 1


class Command(GeneratingCommand):
    help = """Writes a Sphinx documentation tree about models on this Site.
    """
    tmpl_dir = 'makedocs'

    def generate_files(self):

        from lino.ui.extjs3 import UI
        #~ UI = settings.SITE.get_ui_class
        ui = UI(make_messages=True)
        # ~ # install Lino urls under root location (`/`)
        #~ ui = urlpatterns = ui.get_patterns()
        #~ settings.SITE.setup()
        ui.make_linolib_messages()

        context = dict(
            header=rstgen.header,
            h1=curry(rstgen.header, 1),
            table=rstgen.table,
            doc=doc2rst,
            loading=loading,
            models=models,
            abstract=abstract,
            refto=refto,
            #~ py2rst=rstgen.py2rst,
            full_model_name=full_model_name,
            model_overview=model_overview,
            model_referenced_from=model_referenced_from,
            model_ref=model_ref,
        )
        self.generate('index.rst.tmpl', 'index.rst', **context)
        for a in loading.get_apps():
            app_label = a.__name__.split('.')[-2]
            app_models = models.get_models(a, include_auto_created=True)
            context.update(
                app=a,
                app_label=app_label,
                app_models=app_models
            )
            self.generate('app.rst.tmpl', '%s.rst' % app_label, **context)
            for model in app_models:
                context.update(
                    model=model,
                )
                self.generate('model.rst.tmpl', '%s.rst' %
                              full_model_name(model), **context)
