# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


import os
import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_aware

from lino.api import rt
from lino.modlib.checkdata.choicelists import Checker

from lino.utils.choosers import chooser
from lino.core.model import Model
from lino.mixins.duplicable import Duplicable


from .choicelists import BuildMethods
from .actions import (DirectPrintAction, CachedPrintAction,
                      ClearCacheAction, EditTemplate)


def weekdays(d):
    for i in range(5):
        yield d
        d += datetime.timedelta(days=1)

def register_build_method(bm):
    # not used.
    BuildMethods.add_item_instance(bm)


def build_method_choices():
    return BuildMethods.choices


class PrintableType(Model):

    templates_group = None

    class Meta(object):
        abstract = True

    build_method = BuildMethods.field(blank=True, null=True)
    template = models.CharField(_("Template"), max_length=200, blank=True)

    @classmethod
    def get_template_groups(cls):
        """Note that `get_template_groups` is a **class method** on
        `PrintableType` but an **instance method** on `Printable`.

        """
        return [str(cls.templates_group)]  # or full_model_name(cls)

    @chooser(simple_values=True)
    def template_choices(cls, build_method):
        return cls.get_template_choices(
            build_method,
            cls.get_template_groups())

    @classmethod
    def get_template_choices(cls, build_method, template_groups):
        if not build_method:
            build_method = BuildMethods.get_system_default()
        if not build_method:
            return []
        return rt.find_template_config_files(
            build_method.template_ext, *template_groups)


class Printable(Model):

    class Meta(object):
        abstract = True

    @classmethod
    def get_printable_demo_objects(cls):

        qs = cls.objects.all()
        if qs.count() > 0:
            yield qs[0]

    @classmethod
    def get_template_group(cls):
        # used by excerpts and printable
        return cls._meta.app_label + '/' + cls.__name__

    def get_body_template(self):
        return ''

    # def get_excerpt_type(self):
    #     "Return the primary ExcerptType for the given model."
    #     ContentType = settings.SITE.models.contenttypes.ContentType
    #     ct = ContentType.objects.get_for_model(
    #         self.__class__)
    #     return self.__class__.objects.get(primary=True, content_type=ct)

    def get_excerpt_options(self, ar, **kw):
        return kw

    def get_print_language(self):
        # same as EmptyTableRow.get_print_language
        return settings.SITE.DEFAULT_LANGUAGE.django_code

    def get_template_groups(self):
        return [self.__class__.get_template_group()]

    def get_print_templates(self, bm, action):
        return [bm.get_default_template(self)]

    def get_default_build_method(self):
        return BuildMethods.get_system_default()

    def get_build_method(self):
        # TypedPrintable  overrides this
        return self.get_default_build_method()

    def get_build_options(self, bm, **opts):
        # header_center
        return opts

    def get_printable_context(self, ar=None, **kw):
        # same as lino.utils.report.EmptyTableRow.get_printable_context
        if ar is not None:
            kw = ar.get_printable_context(**kw)
        kw.update(this=self)  # for backward compatibility
        kw.update(obj=self)  # preferred in new templates
        kw.update(language=self.get_print_language() or \
                  settings.SITE.DEFAULT_LANGUAGE.django_code)
        kw.update(site=settings.SITE)
        kw.update(weekdays=weekdays)
        return kw

    def before_printable_build(self, bm):
        pass


class CachedPrintable(Duplicable, Printable):

    class Meta(object):
        abstract = True

    do_print = CachedPrintAction()
    do_clear_cache = ClearCacheAction()
    edit_template = EditTemplate()

    build_time = models.DateTimeField(
        _("build time"), null=True, editable=False)

    build_method = BuildMethods.field(blank=True, null=True)

    def full_clean(self, *args, **kwargs):
        if not self.build_method:
            self.build_method = self.get_default_build_method()
        super(CachedPrintable, self).full_clean(*args, **kwargs)

    def on_duplicate(self, ar, master):
        super(CachedPrintable, self).on_duplicate(ar, master)
        self.build_time = None
        self.build_method = None

    def get_target_name(self):
        if self.build_time:
            return self.get_build_method().get_target_name(
                self.do_print, self)

    def get_build_method(self):
        return self.build_method or self.get_default_build_method()

    def get_target_url(self):
        return self.build_method.get_target_url(
            self.do_print, self)

    def get_cache_mtime(self):
        """Return the modification time (a `datetime`) of the generated cache
        file, or `None` if no such file exists.

        """
        filename = self.get_target_name()
        if not filename:
            return None
        try:
            t = os.path.getmtime(filename)
        except OSError:
            return None
        return datetime.datetime.fromtimestamp(t)

    def clear_cache(self):
        self.build_time = None
        self.save()

    def build_target(elem, ar):
        bm = elem.get_build_method()
        t = bm.build(ar, elem.__class__.do_print, elem)
        if t is None:
            raise Exception("%s : build() returned None?!")
        # t is a file timestamp as returned by os.path.getmtime()
        # expressend as the number of seconds since the epoch.
        t = datetime.datetime.fromtimestamp(t)
        if settings.USE_TZ:
            t = make_aware(t)
        elem.build_time = t
        elem.save()


class TypedPrintable(CachedPrintable):

    type = None

    class Meta(object):
        abstract = True

    def get_printable_type(self):
        return self.type

    def get_template_groups(self):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable, self).get_template_groups()
        return ptype.get_template_groups()

    def get_default_build_method(self):
        ptype = self.get_printable_type()
        if ptype and ptype.build_method:
            return ptype.build_method
        return super(TypedPrintable, self).get_default_build_method()

    # def get_build_method(self):
    #     if not self.build_method:
    #         return self.get_default_build_method()
    #     return self.build_method
        # ptype = self.get_printable_type()
        # if ptype and ptype.build_method:
        #     return ptype.build_method
        # return super(TypedPrintable, self).get_build_method()

    def get_print_templates(self, bm, action):
        ptype = self.get_printable_type()
        if ptype is None:
            return super(TypedPrintable, self).get_print_templates(bm, action)

        if ptype.template:
            return [ptype.template]
        return [bm.get_default_template(self)]


class CachedPrintableChecker(Checker):
    model = CachedPrintable
    verbose_name = _("Check for missing target files")

    def get_checkdata_problems(self, obj, fix=False):
        if obj.build_time is not None:
            t = obj.get_cache_mtime()
            if t is None:
                msg = _("Seems to have been built ({bt}), "
                        "but cache file is missing .")
                params = dict(bt=obj.build_time)
                yield (False, msg.format(**params))
                # if fix:
                #     obj.build_time = None
                #     obj.full_clean()
                #     obj.save()

CachedPrintableChecker.activate()
