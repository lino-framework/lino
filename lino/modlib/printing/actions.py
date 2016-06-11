# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines actions for :doc:`/admin/printing`.

"""

from __future__ import unicode_literals
from builtins import str

import logging
logger = logging.getLogger(__name__)

import os
import shutil
import datetime

from django.conf import settings
from django.utils.timezone import make_aware

from lino.core.actions import Action, ShowDetailAction, GridEdit
from lino.api import rt, _
from lino.core import dbutils

from lino.core.roles import SiteStaff
from lino.utils.xmlgen.html import E
from lino.utils.media import TmpMediaFile
from lino.utils.pdf import merge_pdfs

from .choicelists import BuildMethods

davlink = settings.SITE.plugins.get('davlink', None)
has_davlink = davlink is not None and settings.SITE.use_java


class BasePrintAction(Action):
    """
    Base class for all "Print" actions.
    """
    sort_index = 50
    url_action_name = 'print'
    label = _('Print')
    build_method = None

    def __init__(self, build_method=None, label=None, **kwargs):
        super(BasePrintAction, self).__init__(label, **kwargs)
        if build_method is not None:
            self.build_method = build_method

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
            # logger.info("20121221 makedirs_if_missing %s",os.path.dirname(filename))
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

    def run_from_ui(self, ar, **kw):
        elem = ar.selected_rows[0]
        if self.build_method is None:
            bm = elem.get_build_method()
        elif isinstance(self.build_method, str):
            bm = BuildMethods.get_by_value(self.build_method)
        else:
            bm = self.build_method
        bm.build(ar, self, elem)
        mf = bm.get_target(self, elem)
        leaf = mf.parts[-1]
        self.notify_done(ar, bm, leaf, mf.url, **kw)


class DirectPrintAction(BasePrintAction):
    """Print using a hard-coded template and without cache.

    """
    url_action_name = None
    icon_name = 'printer'
    tplname = None

    def __init__(self, label=None, tplname=None, build_method=None, **kw):
        super(DirectPrintAction, self).__init__(build_method, label, **kw)
        if tplname is not None:
            self.tplname = tplname

    def get_print_templates(self, bm, obj):
        # assert bm is self.build_method
        if self.tplname:
            return [self.tplname + bm.template_ext]
        return obj.get_print_templates(bm, self)


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
            # qs = [ar.actor.get_row_by_pk(pk) for pk in ar.selected_pks]
            mf = self.print_multiple(ar, ar.selected_rows)
            ar2.success(open_url=mf.url)
            # kw.update(refresh_all=True)
            # return kw
        msg = _("This will print %d rows.") % len(ar.selected_rows)
        ar.confirm(ok, msg, _("Are you sure?"))

    def print_multiple(self, ar, qs):
        pdfs = []
        for obj in qs:
            # assert isinstance(obj,CachedPrintable)
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

    The action available only when :mod:`lino.modlib.davlink` is
    installed, and only for users with `SiteStaff` role.

    If it is available, then it still works only when

    - your site has a local config directory
    - your :xfile:`webdav` directory (1) is published by your server under
      "/webdav" and (2) has a symbolic link named `config` which points
      to your local config directory.
    - the local config directory is writable by `www-data`

    **Factory template versus local template**
    
    The action automatically copies a factory template to the local
    config tree if necessary. Before doing so, it will ask for
    confirmation: :message:`Before you can edit this template we must
    create a local copy on the server.  This will exclude the template
    from future updates.`

    """
    sort_index = 51
    url_action_name = 'edit_tpl'
    label = _('Edit Print Template')
    required_roles = set([SiteStaff])

    def attach_to_actor(self, actor, name):
        if not settings.SITE.is_installed('davlink'):
            return False
        return super(EditTemplate, self).attach_to_actor(actor, name)

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
        for grp in reversed(groups):
            # subtle: if there are more than 1 groups
            parts = [grp, leaf]
            local_file = os.path.join(lcd.name, *parts)
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
                rt.makedirs_if_missing(os.path.dirname(local_file))
                shutil.copy(filename, local_file)
                doit(ar2)

            msg = _(
                "Before you can edit this template we must create a "
                "local copy on the server. "
                "This will exclude the template from future updates.")
            ar.info("Gonna copy %s to %s",
                    rt.relpath(filename), rt.relpath(local_file))
            ar.confirm(ok, msg, _("Are you sure?"))
                

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

    # def disabled_for(self,obj,request):
    #     if not obj.build_time:
    #         return True

    def get_action_permission(self, ar, obj, state):
        # obj may be None when Lino asks whether this action
        # should be visible in the UI
        if obj is not None and not obj.build_time:
            return False
        return super(ClearCacheAction, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar):
        elem = ar.selected_rows[0]

        def doit(ar):
            elem.clear_cache()
            ar.success(_("%s printable cache has been cleared.") %
                       elem, refresh=True)

        t = elem.get_cache_mtime()
        if t is not None:
            # set microseconds to those of the stored field because
            # Django DateTimeField can have microseconds precision or
            # not depending on the database backend.

            t = datetime.datetime(
                t.year, t.month, t.day, t.hour,
                t.minute, t.second, elem.build_time.microsecond)
            if settings.USE_TZ:
                t = make_aware(t)
            if t != elem.build_time:
                # logger.info("20140313 %r != %r", t, elem.build_time)
                return ar.confirm(
                    doit,
                    _("This will discard all changes in the generated file."),
                    _("Are you sure?"))
        return doit(ar)


