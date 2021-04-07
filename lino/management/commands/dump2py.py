# -*- coding: UTF-8 -*-
# Copyright 2013-2021 by Rumma & Ko Ltd.
# License: GNU Affero General Public License v3 (see file COPYING for details)

from io import open
import logging ; logger = logging.getLogger(__name__)

import os
from decimal import Decimal
import argparse

from clint.textui import progress

from django.db import models
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DatabaseError
from django.utils.timezone import make_naive, is_aware, utc

from lino.utils import puts
from lino.core.utils import sorted_models_list, full_model_name
from lino.core.choicelists import ChoiceListField

from lino.utils.mldbc.fields import BabelCharField, BabelTextField


def is_pointer_to_contenttype(f):
    if not settings.SITE.is_installed('contenttypes'):
        return False
    if not isinstance(f, models.ForeignKey):
        return False
    return f.remote_field.model is settings.SITE.models.contenttypes.ContentType


def write_create_function(model, stream):
    fields = [f for f in model._meta.get_fields()
              if f.concrete and f.model is model]
    for f in fields:
        if getattr(f, 'auto_now_add', False):
            # raise Exception("%s.%s.auto_now_add is True : values will be lost!" % (
            #     full_model_name(model), f.name))
            logger.warning(
                "%s.%s.auto_now_add is True : values will be lost!",
                full_model_name(model), f.name)
            # f.auto_now_add = False
    stream.write('def create_%s(%s):\n' % (
        model._meta.db_table, ', '.join([
            f.attname for f in fields
            if not getattr(f, '_lino_babel_field', False)])))
    for f in fields:
        if f.model is model:
            pre = '    '
        else:
            pre = '#   '
        if isinstance(f, models.DecimalField):
            stream.write(
                pre+'if %s is not None: %s = Decimal(%s)\n' % (
                    f.attname, f.attname, f.attname))
        elif isinstance(f, ChoiceListField):
            lstname = 'settings.SITE.models.{0}.{1}'.format(
                f.choicelist.app_label, f.choicelist.__name__)
            ln = pre+'if {0}: {0} = {1}.get_by_value({0})\n'
            ln = '#' + ln # no longer needed but maybe useful as a comment
            stream.write(ln.format(f.attname, lstname))
        elif is_pointer_to_contenttype(f):
            stream.write(
                pre+'%s = new_content_type_id(%s)\n' % (
                    f.attname, f.attname))

    if model._meta.parents:
        if len(model._meta.parents) != 1:
            msg = "%s : model._meta.parents is %r" % (
                model, model._meta.parents)
            raise Exception(msg)
        pm, pf = list(model._meta.parents.items())[0]
        fields = [f for f in fields if f != pf]

    stream.write("    kw = dict()\n")
    for f in fields:
        if f.model is model:
            pre = '    '
        else:
            pre = '#   '
        if getattr(f, '_lino_babel_field', False):
            continue
        elif isinstance(f, (BabelCharField, BabelTextField)):
            stream.write(
                pre + 'if %s is not None: kw.update(bv2kw(%r,%s))\n' % (
                    f.attname, f.attname, f.attname))
        else:
            stream.write(
                pre + 'kw.update(%s=%s)\n' % (f.attname, f.attname))

    if model._meta.parents:
        stream.write(
            '    return create_mti_child(%s, %s, %s, **kw)\n\n' % (
                full_model_name(pm, '_'), pf.attname,
                full_model_name(model, '_')))
    else:
        stream.write('    return %s(**kw)\n\n' %
                          full_model_name(model, '_'))



class Command(BaseCommand):
    # tmpl_dir = ''
    # args = "output_dir"

    def add_arguments(self, parser):
        parser.add_argument(
            'output_dir',
            help='The directory where to write output files.')
        parser.add_argument('--noinput', action='store_false',
                            dest='interactive', default=True,
                            help='Do not prompt for input of any kind.')
        parser.add_argument('--tolerate', action='store_true',
                            dest='tolerate', default=False,
                            help='Tolerate database errors.')
        parser.add_argument('-o', '--overwrite', action='store_true',
                            dest='overwrite', default=False,
                            help='Overwrite existing files.')
        parser.add_argument('-m', '--max-row-count', type=int,
                            dest='max_row_count', default=50000,
                            help='Maximum number of rows per file.')

    def write_files(self):
        puts("Writing {0}...".format(self.main_file))
        self.stream = open(self.main_file, 'wt')
        current_version = settings.SITE.version

        self.stream.write('''\
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This is a Python dump created using dump2py.
# DJANGO_SETTINGS_MODULE was %r, TIME_ZONE was %r.

''' % (settings.SETTINGS_MODULE, settings.TIME_ZONE))

        self.stream.write('''
from __future__ import unicode_literals

import logging
logger = logging.getLogger('%s')

''' % __name__)

        self.stream.write('SOURCE_VERSION = %r\n' % str(current_version))
        self.stream.write('''
import os
import six
from decimal import Decimal
from datetime import datetime
from datetime import time, date
from django.conf import settings
from django.utils.timezone import make_aware, utc
from django.core.management import call_command
# from django.contrib.contenttypes.models import ContentType
from lino.utils.dpy import create_mti_child
from lino.utils.dpy import DpyLoader
from lino.core.utils import resolve_model

if settings.USE_TZ:
    def dt(*args):
        return make_aware(datetime(*args), timezone=utc)
else:
    def dt(*args):
        return datetime(*args)

def new_content_type_id(m):
    if m is None: return m
    ct = settings.SITE.models.contenttypes.ContentType.objects.get_for_model(m)
    if ct is None: return None
    return ct.pk

def pmem():
    # Thanks to https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
    process = psutil.Process(os.getpid())
    print(process.memory_info().rss)

def execfile(fn, *args):
    logger.info("Execute file %s ...", fn)
    six.exec_(compile(open(fn, "rb").read(), fn, 'exec'), *args)
    # pmem()  # requires pip install psutil

''')
        s = ','.join([
            '%s=values[%d]' % (lng.name, lng.index)
            for lng in settings.SITE.languages])
        self.stream.write('''
def bv2kw(fieldname, values):
    """
    Needed if `Site.languages` changed between dumpdata and loaddata
    """
    return settings.SITE.babelkw(fieldname, %s)

''' % s)
        self.models = sorted_models_list()

        if settings.SITE.is_installed('contenttypes'):
            from django.contrib.contenttypes.models import ContentType
            self.models = [m for m in self.models
                           if not issubclass(m, ContentType)]

        if settings.SITE.is_installed('sessions'):
            from django.contrib.sessions.models import Session
            self.models = [m for m in self.models
                           if not issubclass(m, Session)]

        for model in self.models:
            self.stream.write('%s = resolve_model("%s")\n' % (
                full_model_name(model, '_'), full_model_name(model)))
        self.stream.write('\n')
        self.models = self.sort_models(self.models)
        self.stream.write('\n')
        for model in self.models:
            write_create_function(model, self.stream)
        self.stream.write('\n')
        #~ used_models = set()

        self.stream.write("""

def main(args):
    loader = DpyLoader(globals(), quick=args.quick)
    from django.core.management import call_command
    call_command('initdb', interactive=args.interactive)
    os.chdir(os.path.dirname(__file__))
    loader.initialize()
    args = (globals(), locals())

""")

        max_row_count = self.options['max_row_count']
        for model in progress.bar(self.models):
            try:
                qs = model.objects.all()
                total_count = qs.count()
            except DatabaseError as e:
                self.database_errors += 1
                if not self.options['tolerate']:
                    raise
                self.stream.write('\n')
                logger.warning("Tolerating database error %s in %s",
                               e, model._meta.db_table)
                msg = ("The data of table {0} has not been dumped"
                       "because an error {1} occured.").format(
                           model._meta.db_table, e)
                self.stream.write('raise Exception("{0}")\n'.format(msg))
                continue

            fields = [f for f in model._meta.get_fields()
                      if f.concrete and f.model is model]
            fields = [
                f for f in fields
                if not getattr(f, '_lino_babel_field', False)]

            chunks = []  # list of tuples (i, filename, queryset)
            if total_count > max_row_count:
                num_files = (total_count // max_row_count) + 1
                for i in range(num_files):
                    o1 = max_row_count * i
                    o2 = max_row_count * (i+1)
                    t = (i+1,
                         '%s_%d.py' % (model._meta.db_table, i+1),
                         qs[o1:o2])
                    chunks.append(t)
            else:
                chunks.append((1, '%s.py' % model._meta.db_table, qs))
            for i, filename, qs in chunks:
                self.stream.write('    execfile("%s", *args)\n' % filename)
                filename = os.path.join(self.output_dir, filename)
                # puts("Writing {0}...".format(filename))
                # stream = file(filename, 'wt')
                stream = open(filename, 'wt')
                stream.write('# -*- coding: UTF-8 -*-\n')
                txt = "%d objects" % total_count
                if len(chunks) > 1:
                    txt += " (part %d of %d)" % (i, len(chunks))
                stream.write(
                    'logger.info("Loading %s to table %s...")\n' % (
                        txt, model._meta.db_table))

                stream.write(
                    "# fields: %s\n" % ', '.join(
                        [f.name for f in fields]))
                for obj in qs:
                    self.count_objects += 1
                    #~ used_models.add(model)
                    stream.write('loader.save(create_%s(%s))\n' % (
                        obj._meta.db_table,
                        ','.join([self.value2string(obj, f) for f in fields])))
                stream.write('\n')
                if i == len(chunks):
                    stream.write('loader.flush_deferred_objects()\n')

                stream.close()

            #~ self.stream.write('\nfilename = os.path.join(os.path.dirname(__file__),"%s.py")\n' % )

        self.stream.write(
            '    loader.finalize()\n')
        # 20180416 why was the following message commented out?
        # reactivated it because otherwise we have no log entry when
        # the process has finished.
        self.stream.write(
            '    logger.info("Loaded %d objects", loader.count_objects)\n')
        self.stream.write(
            "    call_command('resetsequences')\n")

        self.stream.write("""
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Restore the data.')
    parser.add_argument('--noinput', dest='interactive',
        action='store_false', default=True,
        help="Don't ask for confirmation before flushing the database.")
    parser.add_argument('--quick', dest='quick',
        action='store_true',default=False,
        help='Do not call full_clean() on restored instances.')

    args = parser.parse_args()
    main(args)
""")
        #~ self.stream.write('\nsettings.SITE.load_from_file(globals())\n')
        self.stream.close()

    def sort_models(self, unsorted):
        sorted = []
        hope = True
        """
        20121120 if we convert the list to a set, we gain some performance
        for the ``in`` tests, but we obtain a random sorting order for all
        independent models, making the double dump test less evident.
        """
        #~ 20121120 unsorted = set(unsorted)
        while len(unsorted) and hope:
            hope = False
            guilty = dict()
            #~ puts("hope for", [m.__name__ for m in unsorted])
            for model in unsorted:
                deps = set([f.remote_field.model
                            for f in model._meta.fields
                            if f.remote_field is not None and f.remote_field.model is not model and f.remote_field.model in unsorted])
                #~ deps += [m for m in model._meta.parents.keys()]
                for m in sorted:
                    if m in deps:
                        deps.remove(m)
                if len(deps):
                    guilty[model] = deps
                else:
                    sorted.append(model)
                    unsorted.remove(model)
                    hope = True
                    break

                #~ ok = True
                #~ for d in deps:
                    #~ if d in unsorted:
                        #~ ok = False
                #~ if ok:
                    #~ sorted.append(model)
                    #~ unsorted.remove(model)
                    #~ hope = True
                    #~ break
                #~ else:
                    #~ guilty[model] = deps
                #~ print model.__name__, "depends on", [m.__name__ for m in deps]
        if unsorted:
            assert len(unsorted) == len(guilty)
            msg = "There are %d models with circular dependencies :\n" % len(
                unsorted)
            msg += "- " + '\n- '.join([
                full_model_name(m) + ' (depends on %s)' % ", ".join([
                    full_model_name(d) for d in deps])
                for m, deps in guilty.items()])
            if False:
                # we don't write them to the .py file because they are
                # in random order which would cause false ddt to fail
                for ln in msg.splitlines():
                    self.stream.write('\n# %s' % ln)
            logger.info(msg)
            sorted.extend(unsorted)
        return sorted

    def value2string(self, obj, field):
        if isinstance(field, (BabelCharField, BabelTextField)):
            #~ return repr([repr(x) for x in dbutils.field2args(obj,field.name)])
            return repr(settings.SITE.field2args(obj, field.name))
        # value = field._get_val_from_obj(obj)
        value = field.value_from_object(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if value is None:
        #~ if value is None or value is NOT_PROVIDED:
            return 'None'
        if isinstance(field, models.DateTimeField):
            if is_aware(value):
                d = make_naive(value, timezone=utc)
            else:
                d = value
            return 'dt(%d,%d,%d,%d,%d,%d)' % (
                d.year, d.month, d.day, d.hour, d.minute, d.second)
        if isinstance(field, models.TimeField):
            d = value
            return 'time(%d,%d,%d)' % (d.hour, d.minute, d.second)
        if is_pointer_to_contenttype(field):
            ContentType = settings.SITE.models.contenttypes.ContentType
            ct = ContentType.objects.get(pk=value)
            return full_model_name(ct.model_class(), '_')
            #~ return "'"+full_model_name(ct.model_class())+"'"
            #~ return repr(tuple(value.app_label,value.model))
        if isinstance(field, models.DateField):
            d = value
            return 'date(%d,%d,%d)' % (d.year, d.month, d.day)
            #~ return 'i2d(%4d%02d%02d)' % (d.year,d.month,d.day)
        if isinstance(value, (float, Decimal)):
            return repr(str(value))
        if isinstance(value, int):
            return str(value)
        return repr(field.value_to_string(obj))

    def handle(self, *args, **options):
        # if len(args) != 1:
        #     raise CommandError("No output_dir specified.")
            # print("No output_dir specified.")
            # sys.exit(-1)
        # import lino
        # lino.startup()
        output_dir = options['output_dir']
        self.output_dir = os.path.abspath(output_dir)
        # self.output_dir = os.path.abspath(args[0])
        self.main_file = os.path.join(self.output_dir, 'restore.py')
        self.count_objects = 0
        self.database_errors = 0
        if os.path.exists(self.output_dir):
            if options['overwrite']:
                pass
                # TODO: remove all files?
            else:
                raise CommandError(
                    "Specified output_dir %s already exists. "
                    "Delete it yourself if you dare!" % self.output_dir)
        else:
            os.makedirs(self.output_dir)

        self.options = options

        #~ logger.info("Running %s to %s.", self, self.output_dir)
        self.write_files()
        logger.info("Wrote %s objects to %s and siblings." % (
            self.count_objects, self.main_file))
        if self.database_errors:
            raise CommandError(
                "There were %d database errors. "
                "The dump in %s is not complete.",
                self.database_errors, self.output_dir)
