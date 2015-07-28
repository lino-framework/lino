# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

"""This defines the :class:`Kernel` class.

The "kernel" of a Lino site is (like `SITE` itself) a "de facto
singleton", available to application code as ``SITE.kernel`` (and its
alias for backwards compatibility: ``SITE.ui``).

The kernel is instantiated at the end of the startup process, when the
:settings`SITE` has been instantiated and models have been loaded.  It
encapsulates a bunch of functionality which becomes available only
then.

TODO: Rename "kernel" to something else.  Because "kernel" suggests
something which is loaded *in first place*, but

"""


import logging
logger = logging.getLogger(__name__)

import os
from os.path import join, dirname, exists

import sys
import time
import codecs
import atexit

from django.conf import settings
from django.core import exceptions
from django.utils.encoding import force_text

from django.db import models
from django.db.models import loading
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext_lazy as _

from lino.utils import puts
from lino.utils import codetime
from lino.core import layouts
from lino.core import actors
from lino.core import actions
from lino.core import fields
from lino.core import dbtables
from lino.core import tables
from lino.core import constants
from lino.core import web
from lino.core import views
from lino.utils import class_dict_items
from lino.core.requests import ActorRequest
from lino.core.model import Model
from lino.core.store import Store
from lino.core.renderer import HtmlRenderer, TextRenderer
from lino.core.signals import (pre_ui_build, post_ui_build,
                               pre_analyze, post_analyze)
from .plugin import Plugin
from .ddh import DisableDeleteHandler
from .utils import resolve_model
from .utils import is_devserver
from .utils import full_model_name as fmn


def set_default_verbose_name(f):
    """If the verbose_name of a ForeignKey was not set by user code,
    Django sets it to ``field.name.replace('_', ' ')``.  We replace
    this default value by ``f.rel.to._meta.verbose_name``.  This rule
    holds also for virtual FK fields.

    """
    if f.verbose_name == f.name.replace('_', ' '):
        f.verbose_name = f.rel.to._meta.verbose_name

CLONEABLE_ATTRS = frozenset("""ah request user subst_user
bound_action create_kw known_values param_values
action_param_values""".split())

GFK_TARGETS = (models.AutoField, models.IntegerField)


class CallbackChoice(object):
    #~ def __init__(self,name,label,func):

    def __init__(self, name, func, label):
        self.name = name
        #~ self.index = index
        self.func = func
        self.label = label


class Callback(object):
    """A callback is a question that rose during an AJAX action.
    The original action is pending until we get a request
    that answers the question.

    TODO: move all callback-related code out of
    :mod:`lino.core.kernel` into to a separate module and install it
    as a "kernel plugin" in a similar way as :mod:`lino.core.web` and
    :mod:`lino.utils.config`.

    """
    title = _('Confirmation')
    #~ def __init__(self,yes,no):

    def __init__(self, ar, message):
        self.message = message
        self.choices = []
        self.choices_dict = {}
        self.ar = ar

    def __repr__(self):
        return "Callback(%r)" % self.message

    def set_title(self, title):
        self.title = title

    def add_choice(self, name, func, label):
        """
        Add a possible answer to this callback.
        - name: "yes", "no", "ok" or "cancel"
        - func: a callable to be executed when user selects this choice
        - the label of the button
        """
        assert not name in self.choices_dict
        allowed_names = ("yes", "no", "ok", "cancel")
        if not name in allowed_names:
            raise Exception("Sorry, name must be one of %s" % allowed_names)
        cbc = CallbackChoice(name, func, label)
        self.choices.append(cbc)
        self.choices_dict[name] = cbc
        return cbc


class Kernel(object):
    """This is the class of the object stored in :attr:`Site.kernel
<lino.core.site.Site.kernel>`.

    """
    default_ui = None

    # _singleton_instance = None

    # @classmethod
    # def instance(cls, site):
    #     if cls._singleton_instance is None:
    #         cls._singleton_instance = cls(site)
    #     elif cls._singleton_instance.site is not site:
    #         site.logger().info("Overriding SITE instance")
    #         cls._singleton_instance.site = site
    #     return cls._singleton_instance

    def __init__(self, site):
        # logger.info("20140227 Kernel.__init__() a")

        # from django.utils.importlib import import_module
        # # For every plugin, Lino checks whether the package contains a
        # # module named `ui` and, if yes, imports this module. The
        # # benefit of this is that all "Lino extensions" to the models
        # # can be moved out of :xfile:`models.py` into a separate file
        # # :xfile:`ui.py`.
        # # print '\n'.join([p.app_name for p in self.installed_plugins])
        # for p in site.installed_plugins:
        #     # fn = dirname(inspect.getfile(p.app_module))
        #     # fn = join(fn, 'ui.py')
        #     try:
        #         x = p.app_name + '.ui'
        #         import_module(x)
        #         logger.info("20150416 imported %s", x)
        #     except Exception as e:
        #     # except ImportError as e:
        #         if str(e) != "No module named ui":
        #             logger.warning("Failed to import %s : %s", x, e)
        #             # raise Exception("Failed to import %s : %s" % (x, e))

        self.pending_threads = {}
        self.site = site
        self.GFK_LIST = []
        self.kernel_startup(site)
        self.code_mtime = codetime()
        # We set `code_mtime` only after kernel_startup() because
        # codetime watches only those modules which are already
        # imported.

        if site.build_js_cache_on_startup is None:
            site.build_js_cache_on_startup = not (
                settings.DEBUG or is_devserver())

        web.site_setup(site)

        for a in actors.actors_list:
            if a.get_welcome_messages is not None:
                # site._welcome_actors.append(a)
                site.add_welcome_handler(a.get_welcome_messages)

        pre_ui_build.send(self)

        self.html_renderer = HtmlRenderer(self)
        self.text_renderer = TextRenderer(self)
        self.reserved_names = [getattr(constants, n)
                               for n in constants.URL_PARAMS]

        names = set()
        for n in self.reserved_names:
            if n in names:
                raise Exception("Duplicate reserved name %r" % n)
            names.add(n)

        for p in site.installed_plugins:
            p.on_ui_init(self)

        ui = None
        if self.site.default_ui is not None:
            ui = self.site.plugins.resolve(self.site.default_ui)
            if ui is None:
                raise Exception(
                    "No installed app labelled %r"
                    % self.site.default_ui)
            ui.url_prefix = None
        else:
            for p in self.site.installed_plugins:
                if p.ui_handle_attr_name is not None:
                    ui = p
                    break
            # if ui is None:
            #     raise Exception("No user interface in {0}".format(
            #         [u.app_name for u in self.site.installed_plugins]))
        if ui is not None:
            self.default_renderer = ui.renderer
            self.default_ui = ui

        post_ui_build.send(self)

        if self.default_ui is not None:

            # trigger creation of params_layout.params_store
            for res in actors.actors_list:
                for ba in res.get_actions():
                    if ba.action.params_layout is not None:
                        ba.action.params_layout.get_layout_handle(
                            self.default_ui)
        # logger.info("20140227 Kernel.__init__() done")

    def kernel_startup(kernel, self):
        """This is a part of a Lino site startup.  The Django Model
        definitions are done, now Lino analyzes them and does certain
        actions:

        - Verify that there are no more pending injects Install a
          :class:`DisableDeleteHandler
          <lino.core.ddh.DisableDeleteHandler>` for each Model into
          `_lino_ddh`.

        - Install :class:`lino.core.model.Model` attributes and
          methods into Models that don't inherit from it.

        """
        if len(sys.argv) == 0:
            process_name = 'WSGI'
        else:
            process_name = ' '.join(sys.argv)

        logger.info("Started %s (using %s) --> PID %s",
                    process_name, settings.SETTINGS_MODULE, os.getpid())
        # puts(self.welcome_text())

        def goodbye():
            logger.info("Done %s (PID %s)", process_name, os.getpid())
        atexit.register(goodbye)

        models_list = loading.get_models(include_auto_created=True)
        # this also triggers django.db.models.loading.cache._populate()

        self.setup_model_spec(self, 'user_model')
        self.setup_model_spec(self, 'project_model')

        for app_name_model, p in self.override_modlib_models.items():
            # app_name_model is the full installed app module name +
            # the model name. It certainly contains at least one dot.
            m = '.'.join(app_name_model.split('.')[-2:])
            resolve_model(
                m,
                strict="%s plugin tries to extend unresolved model '%%s'" %
                p.__class__.__module__)

        for model in models_list:
            #~ print 20130216, model
            #~ fix_field_cache(model)

            model._lino_ddh = DisableDeleteHandler(model)

            Model.django2lino(model)

            if isinstance(model.hidden_columns, basestring):
                model.hidden_columns = frozenset(
                    fields.fields_list(model, model.hidden_columns))

            if isinstance(model.active_fields, basestring):
                model.active_fields = frozenset(
                    fields.fields_list(model, model.active_fields))

            if isinstance(model.allow_cascaded_delete, basestring):
                model.allow_cascaded_delete = frozenset(
                    fields.fields_list(model, model.allow_cascaded_delete))

            if model._meta.abstract:
                raise Exception("Tiens?")

            # self.modules.define(model._meta.app_label, model.__name__, model)

            for f in model._meta.virtual_fields:
                if isinstance(f, generic.GenericForeignKey):
                    kernel.GFK_LIST.append(f)

        # vip_classes = (layouts.BaseLayout, fields.Dummy)
        # for a in models.get_apps():
        #     app_label = a.__name__.split('.')[-2]

        #     for k, v in a.__dict__.items():
        #         if isinstance(v, type) and issubclass(v, vip_classes):
        #             self.modules.define(app_label, k, v)

        #         if k.startswith('setup_'):
        #             self.modules.define(app_label, k, v)

        if self.user_profiles_module:
            from django.utils.importlib import import_module
            import_module(self.user_profiles_module)
        
        self.setup_choicelists()
        self.setup_workflows()

        for model in models_list:
            if model._meta.auto_created:
                continue  # automatic intermediate models created by
                          # ManyToManyField should not disable delete
            for f, m in model._meta.get_fields_with_model():

                # Refuse nullable CharFields, but don't trigger on
                # NullableCharField (which is a subclass of CharField).

                if f.__class__ is models.CharField and f.null:
                    msg = "Nullable CharField %s in %s" % (f.name, model)
                    raise Exception(msg)
                    #~ if f.__class__ is models.CharField:
                        #~ raise Exception(msg)
                    #~ else:
                        #~ logger.info(msg)
                elif isinstance(f, models.ForeignKey):
                    # f.rel.to = resolve_model(f.rel.to, strict=True)
                    if isinstance(f.rel.to, basestring):
                        raise Exception("Could not resolve target %r of "
                                        "ForeignKey '%s' in %s "
                                        "(models are %s)" %
                                        (f.rel.to, f.name, model, models_list))
                    set_default_verbose_name(f)

                    """
                    If JobProvider is an MTI child of Company,
                    then mti.delete_child(JobProvider) must not fail on a
                    JobProvider being refered only by objects that can refer
                    to a Company as well.
                    """
                    if hasattr(f.rel.to, '_lino_ddh'):
                        f.rel.to._lino_ddh.add_fk(m or model, f)

        for p in self.installed_plugins:
            if isinstance(p, Plugin):
                p.before_analyze()

        # logger.info("20150429 Gonna send pre_analyze signal")
        pre_analyze.send(self, models_list=models_list)
        # logger.info("20150429 pre_analyze signal done")
        # MergeActions are defined in pre_analyze.
        # And MergeAction needs the info in _lino_ddh to correctly find
        # keep_volatiles

        for model in models_list:

            """Virtual fields declared on the model must have been attached
            before calling Model.site_setup(), e.g. because
            pcsw.Person.site_setup() declares `is_client` as imported
            field.

            """

            model.on_analyze(self)

            for k, v in class_dict_items(model):
                if isinstance(v, fields.VirtualField):
                    v.attach_to_model(model, k)

        #~ logger.info("20130817 attached model vfs")

        actors.discover()

        logger.debug("actors.initialize()")
        for a in actors.actors_list:
            a.class_init()

        dbtables.discover()
        #~ choosers.discover()
        actions.discover_choosers()

        for a in actors.actors_list:
            a.on_analyze(self)

        post_analyze.send(self, models_list=models_list)

        if False:
            logger.info("Languages: %s. %d apps, %d models, %s actors.",
                        ', '.join([li.django_code for li in self.languages]),
                        len(self.modules),
                        len(models_list),
                        len(actors.actors_list))

        #~ logger.info(settings.INSTALLED_APPS)

        self.on_each_app('site_setup')

        # Actor.after_site_setup() is called after the apps'
        # site_setup().  Example: pcsw.site_setup() adds a detail to
        # properties.Properties, the base class for
        # properties.PropsByGroup.  The latter would not install a
        # `detail_action` during her after_site_setup() and also would
        # never get it later.

        for a in actors.actors_list:
            a.after_site_setup(self)

        #~ self.on_site_startup()

        self.resolve_virtual_fields()

        #~ logger.info("20130827 startup_site done")

    def get_generic_related(self, obj):
        """Yield a series of `(gfk, fk_field, queryset)` tuples which together
         will return all database objects for which the given
         GenericForeignKey gfk points to the object `obj`. See also
         :doc:`/dev/gfks`.

        """
        if len(self.GFK_LIST) == 0:
            return  # e.g. if contenttypes is not installed

        if not isinstance(obj._meta.pk, GFK_TARGETS):
            # raise Exception("20150330 %s", obj._meta.pk)
            return  # e.g. Country.iso_code is a CharField, cannot
                    # point to a country using GFK
        obj_ct = ContentType.objects.get_for_model(obj.__class__)
        # logger.info("20150330 ok %s", obj_ct)
        for gfk in self.GFK_LIST:
            fk_field, remote_model, direct, m2m = \
                gfk.model._meta.get_field_by_name(gfk.fk_field)
            kw = dict()
            kw[gfk.fk_field] = obj.pk
            kw[gfk.ct_field] = obj_ct
            ct = ContentType.objects.get_for_model(gfk.model)
            yield gfk, fk_field, ct.get_all_objects_for_this_type(**kw)

    def get_broken_generic_related(self, model):
        """Yield all database objects of this model which have some broken
        GFK field.
    
        This is a slow query which does an additional database request
        for each row. (Is there a possibility to do this in a single
        SQL query?)
    
        Each yeld object has two special attributes:
    
        - `_message` : a textual description of the problem
        - `_todo` : 'delete', 'clear' or 'manual'

        Note: the "clear" action should not run automatically, at
        least not for :mod:`lino.modlib.changes`.

        See also :ref:`lino.tutorial.watch`.

        """
        gfks = [f for f in self.GFK_LIST if f.model is model]
        if len(gfks):
            for gfk in gfks:
                fk_field, remote_model, direct, m2m = \
                    gfk.model._meta.get_field_by_name(gfk.fk_field)
                kw = {gfk.ct_field+'__isnull': False}
                qs = model.objects.filter(**kw)
                for obj in qs:
                    fk = getattr(obj, gfk.fk_field)
                    ct = getattr(obj, gfk.ct_field)
                    pointed_model = ct.model_class()
                    # pointed_model = ContentType.objects.get_for_id(ct)
                    try:
                        pointed_model.objects.get(pk=fk)
                    except pointed_model.DoesNotExist:
                        msg = "Invalid primary key {1} for {2} in `{0}`"
                        obj._message = msg.format(
                            gfk.fk_field, fk, fmn(pointed_model))
                        if gfk.name in model.allow_cascaded_delete:
                            obj._todo = 'delete'
                        elif fk_field.null:
                            obj._todo = 'clear'
                        else:
                            obj._todo = 'manual'
                        yield obj

    def abandon_response(self):
        return self.success(_("User abandoned"))

    def field2elem(self, lui, field, **kw):
        pass

    def run_callback(self, request, thread_id, button_id):
        """Continue the action which was started in a previous request and
        which asked for user interaction via a :class:`Callback`.

        This is called from `lino.core.views.Callbacks`.

        """
        # logger.info("20131212 get_callback %s %s", thread_id, button_id)

        # 20140304 Also set a renderer so that callbacks can use it
        # (feature needed by beid.FindByBeIdAction).

        thread_id = int(thread_id)
        cb = self.pending_threads.pop(thread_id, None)
        if cb is None:
            ar = ActorRequest(request, renderer=self.default_renderer)
            logger.debug("No callback %r in %r" % (
                thread_id, self.pending_threads.keys()))
            ar.error("Unknown callback %r" % thread_id)
            return self.render_action_response(ar)

        # e.g. SubmitInsertClient must set `data_record` in the
        # callback request ("ar2"), not the original request ("ar"),
        # i.e. the methods to create an instance and to fill
        # `data_record` must run on the callback request.  So the
        # callback request must be a clone of the original request.
        # New since 20140421
        ar = cb.ar.actor.request_from(cb.ar)
        for k in CLONEABLE_ATTRS:
            setattr(ar, k, getattr(cb.ar, k))

        for c in cb.choices:
            if c.name == button_id:
                c.func(ar)
                return self.render_action_response(ar)

        ar.error("Invalid button %r for callback" % (button_id, thread_id))
        return self.render_action_response(ar)

    def add_callback(self, ar, *msgs):
        """
        Returns an "action callback" which will initiate a dialog thread
        by asking a question to the user and suspending execution until
        the user's answer arrives in a next HTTP request.

        Implementation notes:
        Calling this from an Action's
        :meth:`run_from_ui <lino.core.actions.Action.run_from_ui>` method will
        interrupt the execution, send the specified message back to
        the user, adding the executables `yes` and optionally `no` to a queue
        of pending "dialog threads".
        The client will display the prompt and will continue this thread
        by requesting :class:`lino.modlib.extjs3.views.Callbacks`.
        """
        if len(msgs) > 1:
            msg = '\n'.join([force_text(s) for s in msgs])
        else:
            msg = msgs[0]

        return Callback(ar, msg)

    def set_callback(self, ar, cb):
        """
        """
        h = hash(cb)
        self.pending_threads[h] = cb
        # logger.info("20131212 Stored %r in %r" % (
        #     h, self.pending_threads))

        buttons = dict()
        for c in cb.choices:
            buttons[c.name] = c.label

        ar.success(
            cb.message, xcallback=dict(
                id=h,
                title=cb.title,
                buttons=buttons))

    def run_action(self, ar):
        """Run the action, catching some exceptions in order to report them
        in a user-friendly way.

        """
        a = ar.bound_action.action
        try:
            a.run_from_ui(ar)
            if a.parameters and not a.no_params_window:
                ar.set_response(close_window=True)
        except exceptions.ValidationError as e:
            # logger.info("20150127 run_action %r", e)
            ar.error(ar.ah.actor.error2str(e), alert=True)
        except Warning as e:
            ar.error(unicode(e), alert=True)

        return self.render_action_response(ar)

    def setup_handle(self, h, ar):
        """
        ar is usually None, except for actors with dynamic handle
        """
        #~ logger.info('20121010 ExtUI.setup_handle() %s',h.actor)

        if h.actor.is_abstract():
            return

        if isinstance(h, tables.TableHandle):
            ll = layouts.ColumnsLayout(
                h.actor.get_column_names(ar),
                h.actor,
                hidden_elements=h.actor.hidden_columns
                | h.actor.hidden_elements)
            h.list_layout = ll.get_layout_handle(self.default_ui)
        else:
            h.list_layout = None

        if h.actor.params_layout:
            h.params_layout_handle = h.actor.make_params_layout_handle(self)

        h.store = Store(h)

    def render_action_response(self, ar):
        """Builds a JSON response from response information stored in given
        ActionRequest.

        """
        return views.json_response(ar.response, ar.content_type)

    def row_action_button(self, *args, **kw):
        """
        See :meth:`ExtRenderer.row_action_button`
        """
        return self.default_renderer.row_action_button(*args, **kw)

    _must_build = False

    def must_build_site_cache(self):
        self._must_build = True
        
    def make_cache_file(self, fn, write, force=False):
        """Make the specified cache file.  This is used internally at server
        startup.

        """
        # cachedir = self.site.cache_dir.child('static', 'cache', 'js')
        # if not exists(settings.STATIC_ROOT):
        #     logger.info("STATIC_ROOT does not exist: %s", settings.STATIC_ROOT)
        #     return 0
        fn = join(settings.MEDIA_ROOT, fn)
        # fn = join(settings.STATIC_ROOT, fn)
        # fn = join(self.site.cache_dir, fn)
        if not force and not self._must_build and os.path.exists(fn):
            mtime = os.stat(fn).st_mtime
            if mtime > self.code_mtime:
                logger.debug("%s (%s) is up to date.", fn, time.ctime(mtime))
                return 0

        logger.info("Building %s ...", fn)
        self.site.makedirs_if_missing(dirname(fn))
        f = codecs.open(fn, 'w', encoding='utf-8')
        try:
            write(f)
            f.close()
            return 1
        except Exception:
            f.close()
            if not self.site.keep_erroneous_cache_files:  #
                os.remove(fn)
            raise
        #~ logger.info("Wrote %s ...", fn)

    # def setup_static_link(self, urlpatterns, short_name,
    #                       attr_name=None, source=None):
