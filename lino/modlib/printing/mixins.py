# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines most of the classes needed for
:doc:`/admin/printing`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import shutil
import os
from os.path import join, dirname
import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import rt
from lino.utils.xmlgen.html import E

davlink = settings.SITE.plugins.get('davlink', None)
has_davlink = davlink is not None and settings.SITE.use_java


# from lino.core import actions
from lino.core.actions import Action, ShowDetailAction, GridEdit
from lino.core import dbutils
from lino.utils.choosers import chooser
from lino.core.model import Model
from lino.mixins.duplicable import Duplicable

from lino.core.roles import SiteStaff

from lino.utils.media import TmpMediaFile
from lino.utils.pdf import merge_pdfs


from .choicelists import BuildMethods


def register_build_method(bm):
    # not used.
    BuildMethods.add_item_instance(bm)


def build_method_choices():
    return BuildMethods.choices


class BasePrintAction(Action):

    """
    Base class for all "Print" actions.
    """
    sort_index = 50
    url_action_name = 'print'
    label = _('Print')

    def attach_to_actor(self, actor, name):
        if not dbutils.resolve_app('system'):
            return False
        # if actor.__name__ == 'ExcerptsByProject':
        #     logger.info("20140401 attach_to_actor() %r", self)
        return super(BasePrintAction, self).attach_to_actor(actor, name)

    def is_callable_from(self, caller):
        # including ShowEmptyTable which is subclass of
        # ShowDetailAction. But not callable from InsertRow.
        return isinstance(caller, (GridEdit, ShowDetailAction))

    def get_print_templates(self, bm, elem):
        return elem.get_print_templates(bm, self)

    def before_build(self, bm, elem):
        """Return the target filename if a document needs to be built,
        otherwise return ``None``.
        """
        elem.before_printable_build(bm)
        filename = bm.get_target_name(self, elem)
        if not filename:
            return
        if os.path.exists(filename):
            logger.debug(u"%s %s -> overwrite existing %s.",
                         bm, elem, filename)
            os.remove(filename)
        else:
            #~ logger.info("20121221 makedirs_if_missing %s",os.path.dirname(filename))
            rt.makedirs_if_missing(os.path.dirname(filename))
        logger.debug(u"%s : %s -> %s", bm, elem, filename)
        return filename

    def notify_done(self, ar, bm, leaf, url, **kw):
        help_url = ar.get_help_url("print", target='_blank')
        msg = _("Your printable document (filename %(doc)s) "
                "should now open in a new browser window. "
                "If it doesn't, please consult %(help)s "
                "or ask your system administrator.")
        msg %= dict(doc=leaf, help=E.tostring(help_url))
        kw.update(message=msg, alert=True)
        if bm.use_webdav and has_davlink and ar.request is not None:
            kw.update(
                open_davlink_url=ar.request.build_absolute_uri(url))
        else:
            kw.update(open_url=url)
        ar.success(**kw)
        return


class DirectPrintAction(BasePrintAction):
    """Print using a hard-coded template and no cache.

    """
    url_action_name = None
    icon_name = 'printer'

    def __init__(self, label=None, tplname=None, build_method=None, **kw):
        super(DirectPrintAction, self).__init__(label, **kw)
        self.build_method = build_method
        self.tplname = tplname

    def get_print_templates(self, bm, obj):
        #~ assert bm is self.build_method
        if self.tplname:
            return [self.tplname + bm.template_ext]
        return obj.get_print_templates(bm, self)

    def run_from_ui(self, ar, **kw):
        elem = ar.selected_rows[0]
        bm = elem.get_build_method()
        bm.build(ar, self, elem)
        mf = bm.get_target(self, elem)
        # if ar.request is not None and bm.use_webdav and has_davlink:
        #     url = ar.request.build_absolute_uri(url)
        #     kw.update(open_davlink_url=url)
        # else:
        #     kw.update(open_url=url)
        # ar.success(**kw)
        leaf = mf.parts[-1]
        self.notify_done(ar, bm, leaf, mf.url, **kw)


class CachedPrintAction(BasePrintAction):

    """A print action which uses a cache for the generated printable
    document and builds is only when it doesn't yet exist.

    """

    # select_rows = False
    http_method = 'POST'
    icon_name = 'printer'

    def before_build(self, bm, elem):
        if elem.build_time:
            return
        return BasePrintAction.before_build(self, bm, elem)

    def run_from_ui(self, ar, **kw):

        if len(ar.selected_rows) == 1:
            obj = ar.selected_rows[0]
            bm = obj.get_build_method()
            mf = bm.get_target(self, obj)

            leaf = mf.parts[-1]
            if obj.build_time is None:
                obj.build_target(ar)
                ar.info("%s has been built.", leaf)
            else:
                ar.info("Reused %s from cache.", leaf)

            self.notify_done(ar, bm, leaf, mf.url, **kw)
            ar.set_response(refresh=True)
            return

        def ok(ar2):
            #~ qs = [ar.actor.get_row_by_pk(pk) for pk in ar.selected_pks]
            mf = self.print_multiple(ar, ar.selected_rows)
            ar2.success(open_url=mf.url)
            #~ kw.update(refresh_all=True)
            #~ return kw
        msg = _("This will print %d rows.") % len(ar.selected_rows)
        ar.confirm(ok, msg, _("Are you sure?"))

    def print_multiple(self, ar, qs):
        pdfs = []
        for obj in qs:
            #~ assert isinstance(obj,CachedPrintable)
            if obj.printed_by_id is None:
                obj.build_target(ar)
            pdf = obj.get_target_name()
            assert pdf is not None
            pdfs.append(pdf)

        mf = TmpMediaFile(ar, 'pdf')
        rt.makedirs_if_missing(os.path.dirname(mf.name))
        merge_pdfs(pdfs, mf.name)
        return mf


class EditTemplate(BasePrintAction):
    """Edit the print template, i.e. the file specified by
    :meth:`Printable.get_print_templates`.

    The action becomes automatically visible for users with
    `UserLevel` "manager" and when :mod:`lino.modlib.davlink` is
    installed.

    If it is visible, then it still works only when your
    :xfile:`webdav` directory (1) is published by your server under
    "/webdav" and (2) has a symbolic link named `config` which points
    to your local config directory. And (3) the local config directory
    must be writable by `www-data`.

    """
    sort_index = 51
    url_action_name = 'edit_tpl'
    label = _('Edit Print Template')
    required_roles = set([SiteStaff])

    def run_from_ui(self, ar, **kw):

        lcd = settings.SITE.confdirs.LOCAL_CONFIG_DIR
        if lcd is None:
            # ar.info("No local config directory in %s " %
            #         settings.SITE.confdirs)
            raise Warning("No local config directory. "
                          "Contact your system administrator.")

        elem = ar.selected_rows[0]
        bm = elem.get_build_method()
        leaf = bm.get_template_leaf(self, elem)

        filename = bm.get_template_file(ar, self, elem)
        local_file = None
        groups = elem.get_template_groups()
        assert len(groups) > 0
        for grp in groups:
            parts = [grp, leaf]
            local_file = join(lcd.name, *parts)
            if filename == local_file:
                break

        parts = ['webdav', 'config'] + parts
        url = settings.SITE.build_media_url(*parts)
        if ar.request is not None:
            url = ar.request.build_absolute_uri(url)

        if not has_davlink:
            msg = "cp %s %s" % (filename, local_file)
            ar.info(msg)
            raise Warning("Java is not enabled. "
                          "Contact your system administrator.")
            
        def doit(ar):
            ar.info("Going to open url: %s " % url)
            ar.success(open_davlink_url=url)
            # logger.info('20140313 EditTemplate %r', kw)
    
        if filename == local_file:
            doit(ar)
        else:
            def ok(ar2):
                logger.info(
                    "%s made local template copy %s", ar.user, local_file)
                rt.makedirs_if_missing(dirname(local_file))
                shutil.copy(filename, local_file)
                doit(ar2)

            msg = _(
                "Before you can edit this template we must create a "
                "local copy on the server. "
                "This will exclude the template from future updates.")
            ar.info("Gonna copy %s to %s",
                    rt.relpath(filename), rt.relpath(local_file))
            ar.confirm(ok, msg, _("Are you sure?"))
                

# http://10.171.37.173/api/excerpts/ExcerptTypes/5?an=detail


class ClearCacheAction(Action):

    """
    Defines the :guilabel:`Clear cache` button on a Printable record.
    
    The `run_from_ui` method has an optional keyword argmuent
     `force`. This is set to True in `docs/tests/debts.rst`
     to avoid compliations.
    
    """
    sort_index = 51
    url_action_name = 'clear'
    label = _('Clear cache')
    icon_name = 'printer_delete'

    #~ def disabled_for(self,obj,request):
        #~ if not obj.build_time:
            #~ return True

    def get_action_permission(self, ar, obj, state):
        # obj may be None when Lino asks whether this action
        # should be visible in the UI
        if obj is not None and not obj.build_time:
            return False
        return super(ClearCacheAction, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        elem = ar.selected_rows[0]

        def doit(ar):
            elem.clear_cache()
            ar.success(_("%s printable cache has been cleared.") %
                       elem, refresh=True)

        t = elem.get_cache_mtime()
        if t is not None and t != elem.build_time:
            logger.info(
                "20140313 %r != %r", elem.get_cache_mtime(), elem.build_time)
            return ar.confirm(
                doit,
                _("This will discard all changes in the generated file."),
                _("Are you sure?"))
        return doit(ar)


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

    class Meta:
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


class Printable(object):
    """Mixin for models whose instances have a "print" action (i.e. for
    which Lino can generate a printable document).

    Extended by :class:`CachedPrintable` and :class:`TypedPrintable`.

    .. attribute:: do_print

        The action used to print this object.
        This is an instance of
        :class:`DirectPrintAction` or :class:`CachedPrintAction` by
        default.  And if :mod:`lino.modlib.excerpts` is installed,
        then :func:`set_excerpts_actions
        <lino.modlib.excerpts.set_excerpts_actions>` possibly replaces
        :attr:`do_print` by a
        :class:`lino.modlib.excerpts.CreateExcerpt` instance.

    .. attribute:: edit_template

    """

    do_print = DirectPrintAction()

    edit_template = EditTemplate()

    def before_printable_build(self, bm):
        pass

    def get_template_groups(self):
        return [self.__class__.get_template_group()]

    def filename_root(self):
        return self._meta.app_label + '.' + self.__class__.__name__ \
            + '-' + str(self.pk)

    def get_print_templates(self, bm, action):
        """
        Return a list of filenames of templates for the specified
        build method.  Returning an empty list means that this item is
        not printable.  For subclasses of :class:`SimpleBuildMethod`
        the returned list may not contain more than 1 element.

        """
        return [bm.get_default_template(self)]

    def get_default_build_method(self):
        return BuildMethods.get_system_default()

    def get_build_method(self):
        # TypedPrintable  overrides this
        return self.get_default_build_method()


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

    build_method = BuildMethods.field()

    class Meta:
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
            return self.build_method.get_target_name(
                self.do_print, self)

    def get_target_url(self):
        return self.build_method.get_target_url(
            self.do_print, self)

    def get_cache_mtime(self):
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

    class Meta:
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

    def get_build_method(self):
        if not self.build_method:
            return self.get_default_build_method()
        return self.build_method
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
