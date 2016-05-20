# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines most of the classes needed for
:doc:`/admin/printing`.

"""

from __future__ import unicode_literals
from builtins import object

import logging
logger = logging.getLogger(__name__)

import os
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import rt
from lino.modlib.plausibility.choicelists import Checker


# from lino.core import actions
from lino.utils.choosers import chooser
from lino.core.model import Model
from lino.mixins.duplicable import Duplicable


from .choicelists import BuildMethods
from .utils import PrintableObject
from .actions import (DirectPrintAction, CachedPrintAction,
                      ClearCacheAction, EditTemplate)


def register_build_method(bm):
    # not used.
    BuildMethods.add_item_instance(bm)


def build_method_choices():
    return BuildMethods.choices


class PrintableType(Model):
    """Base class for models that specify the
    :attr:`TypedPrintable.type`.

    .. attribute:: build_method

        A pointer to an item of
        :class:`lino.modlib.printing.choicelists.BuildMethods`.

    .. attribute:: template

        The name of the file to be used as template.
    
        If this field is empty, Lino will use the filename returned by
        :meth:`lino.modlib.printing.Plugin.get_default_template`.
    
        The list of choices for this field depend on the
        :attr:`build_method`.  Ending must correspond to the
        :attr:`build_method`.

    """

    templates_group = None
    """
    Default value for `templates_group` is the model's full name.
    """

    class Meta(object):
        abstract = True

    build_method = BuildMethods.field(blank=True, null=True)
    template = models.CharField(_("Template"), max_length=200, blank=True)

    @classmethod
    def get_template_groups(cls):
        """Note that `get_template_groups` is a **class method** on
        `PrintableType` but an **instance method** on `Printable`.

        """
        return [cls.templates_group]  # or full_model_name(cls)

    @chooser(simple_values=True)
    def template_choices(cls, build_method):
        return cls.get_template_choices(
            build_method,
            cls.get_template_groups())

    @classmethod
    def get_template_choices(cls, build_method, template_groups):
        if not build_method:
            build_method = BuildMethods.get_system_default()
        return rt.find_template_config_files(
            build_method.template_ext, *template_groups)


class Printable(PrintableObject):
    """Mixin for models whose instances have a "print" action (i.e. for
    which Lino can generate a printable document).

    Extended by :class:`CachedPrintable` and :class:`TypedPrintable`.

    .. attribute:: do_print

        The action used to print this object.
        This is an instance of
        :class:`DirectPrintAction` or :class:`CachedPrintAction` by
        default.  And if :mod:`lino_xl.lib.excerpts` is installed,
        then :func:`set_excerpts_actions
        <lino_xl.lib.excerpts.set_excerpts_actions>` possibly replaces
        :attr:`do_print` by a
        :class:`lino_xl.lib.excerpts.CreateExcerpt` instance.

    .. attribute:: edit_template

    """

    do_print = DirectPrintAction()

    edit_template = EditTemplate()


class CachedPrintable(Duplicable, Printable):
    """
    Mixin for Models that generate a unique external file at a
    determined place when being printed.
    
    Adds a "Print" button, a "Clear cache" button and a `build_time`
    field.
    
    The "Print" button of a :class:`CachedPrintable
    <lino.mixins.printable.CachedPrintable>` transparently handles the
    case when multiple rows are selected.  If multiple rows are
    selected (which is possible only when :attr:`cell_edit
    <lino.core.tables.AbstractTable.cell_edit>` is True), then it will
    automatically:
    
    - build the cached printable for those objects who don't yet have
      one
      
    - generate a single temporary pdf file which is a merge of these
      individual cached printable docs

    .. attribute:: build_time

        Timestamp of the built target file. Contains `None`
        if no build hasn't been called yet.

    """

    do_print = CachedPrintAction()
    do_clear_cache = ClearCacheAction()

    build_time = models.DateTimeField(
        _("build time"), null=True, editable=False)

    build_method = BuildMethods.field(blank=True, null=True)

    class Meta(object):
        abstract = True

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
        elem.build_time = datetime.datetime.fromtimestamp(t)
        elem.save()


class TypedPrintable(CachedPrintable):
    """A :class:`CachedPrintable` that uses a "Type" for deciding which
    template to use on a given instance.
    
    A TypedPrintable model must define itself a field ``type`` which
    is a ForeignKey to a Model that implements :class:`PrintableType`.
    
    Alternatively you can override :meth:`get_printable_type` if you
    want to name the field differently. An example of this is
    :attr:`ml.sales.SalesDocument.imode`.

    """

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
    """Checks for missing cache files on all objects which inherit
    :class:`CachedPrintable`.

    When a CachedPrintable has a non-empty :attr:`build_time
    <CachedPrintable.build_time>` field, this means that the target
    file has been built.  That file might no longer exists for several
    reasons:

    - it has really beeen removed from the cache directory.

    - we are working in a copy of the database, using a different
      cache directory.

    - the computed name of the file has changed due to a change in
      configuration or code.

    An easy quick "fix" would be to set `build_time` to None, but this
    is not automatic because in cases of real data loss a system admin
    might want to have at least that timestamp in order to search for
    the lost file.

    """
    model = CachedPrintable
    verbose_name = _("Check for missing target files")
    
    def get_plausibility_problems(self, obj, fix=False):
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
