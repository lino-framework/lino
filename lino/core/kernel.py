# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

"""This defines the :class:`Kernel` class.

The "kernel" of a Lino site is (like `SITE` itself) a "de facto
singleton".  It encapsulates a bunch of functionality which remains an
independent class/object instance and is not merged into the Site
because it gets imported and instantiated only when Django has
finished the models loading.

TODO: Rename this to something else.  Because "kernel" suggests
something which is loaded *in first place*, but this object is
rather loaded at the end (of the startup process).

"""


import logging
logger = logging.getLogger(__name__)

import os
from os.path import join, dirname, exists

import sys
import atexit
from pkg_resources import Requirement, resource_filename, DistributionNotFound

from django.conf import settings
from django.core import exceptions
from django.utils.encoding import force_unicode
from django.utils.encoding import force_text

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from lino.core.signals import database_ready
from django.conf.urls import patterns, include
from django.conf.urls import url

from django.utils.translation import ugettext_lazy as _

import lino

from lino import dd

from lino.utils import class_dict_items
from lino.core.requests import ActorRequest

from lino.core import layouts
from lino.core import actors
from lino.core import actions
from lino.core import fields
from lino.core import dbtables
from lino.core import tables
from lino.core import constants
from lino.core import web
from lino.core.signals import pre_ui_build, post_ui_build

from lino.ui import store as ext_store

from lino.core.dbutils import is_devserver
from lino.ui.render import TextRenderer
from lino.ui import views

from .plugin import Plugin
from .ddh import DisableDeleteHandler


def set_default_verbose_name(f):
    """If the verbose_name of a ForeignKey was not set by user code,
    Django sets it to ``field.name.replace('_', ' ')``.  We replace
    this default value by ``f.rel.to._meta.verbose_name``.  This rule
    holds also for virtual FK fields.

    """
    if f.verbose_name == f.name.replace('_', ' '):
        f.verbose_name = f.rel.to._meta.verbose_name


class CallbackChoice(object):
    #~ def __init__(self,name,label,func):

    def __init__(self, name, func, label):
        self.name = name
        #~ self.index = index
        self.func = func
        self.label = label


class Callback(object):

    """
    A callback is a question that rose during an AJAX action.
    The original action is pending until we get a request
    that answers the question.
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
<lino.core.site_def.Site.kernel>`.

    """

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
        self.pending_threads = {}
        self.site = site
        self.GFK_LIST = []
        self.kernel_startup(site)

        if site.build_js_cache_on_startup is None:
            site.build_js_cache_on_startup = not (
                settings.DEBUG or is_devserver())

        web.site_setup(site)

        for a in actors.actors_list:
            if a.get_welcome_messages is not None:
                site._welcome_actors.append(a)

        pre_ui_build.send(self)

        # self.plain_renderer = PlainRenderer(self)
        self.text_renderer = TextRenderer(self)
        self.reserved_names = [getattr(constants, n)
                               for n in constants.URL_PARAMS]

        names = set()
        for n in self.reserved_names:
            if n in names:
                raise Exception("Duplicate reserved name %r" % n)
            names.add(n)

        for p in site.installed_plugins:
            if isinstance(p, Plugin):
                p.on_ui_init(self)

        ui = self.site.plugins.resolve(self.site.default_ui)
        if ui is None:
            raise Exception(
                "No installed app labelled %r"
                % self.site.default_ui)
        ui.url_prefix = None
        self.default_renderer = ui.renderer

        post_ui_build.send(self)

        # trigger creation of params_layout.params_store
        for res in actors.actors_list:
            for ba in res.get_actions():
                if ba.action.params_layout is not None:
                    ba.action.params_layout.get_layout_handle(self)
        # logger.info("20140227 Kernel.__init__() done")

    def kernel_startup(kernel, self):
        """This is a part of a Lino site startup.  The Django Model
        definitions are done, now Lino analyzes them and does certain
        actions:

        - Verify that there are no more pending injects Install a
          :class:`DisableDeleteHandler
          <lino.core.ddh.DisableDeleteHandler>` for each Model into
          `_lino_ddh`.

        - Install :class:`lino.dd.Model` attributes and
          methods into Models that don't inherit from it.

        """
        if len(sys.argv) == 0:
            process_name = 'WSGI'
        else:
            process_name = ' '.join(sys.argv)
        #~ logger.info("Started %s on %r (PID %s).", process_name,self.title,os.getpid())
        logger.info("Started %s (using %s) --> PID %s",
                    process_name, settings.SETTINGS_MODULE, os.getpid())
        logger.info(self.welcome_text())

        def goodbye():
            logger.info("Done %s (PID %s)", process_name, os.getpid())
        atexit.register(goodbye)

        models_list = models.get_models(include_auto_created=True)
        # this also triggers django.db.models.loading.cache._populate()

        if self.user_model:
            self.user_model = dd.resolve_model(
                self.user_model,
                strict="Unresolved model '%s' in user_model.")

        if self.project_model:
            self.project_model = dd.resolve_model(
                self.project_model,
                strict="Unresolved model '%s' in project_model.")

        for app_name_model, p in self.override_modlib_models.items():
            # app_name_model is the full installed app module name +
            # the model name. It certainly contains at least one dot.
            m = '.'.join(app_name_model.split('.')[-2:])
            dd.resolve_model(
                m,
                strict="%s plugin tries to extend unresolved model '%%s'" %
                p.__class__.__module__)

        for model in models_list:
            #~ print 20130216, model
            #~ fix_field_cache(model)

            model._lino_ddh = DisableDeleteHandler(model)

            dd.Model.django2lino(model)

            if isinstance(model.hidden_columns, basestring):
                model.hidden_columns = frozenset(
                    dd.fields_list(model, model.hidden_columns))

            if isinstance(model.active_fields, basestring):
                model.active_fields = frozenset(
                    dd.fields_list(model, model.active_fields))

            if isinstance(model.allow_cascaded_delete, basestring):
                model.allow_cascaded_delete = frozenset(
                    dd.fields_list(model, model.allow_cascaded_delete))

            if isinstance(model.allow_stale_generic_foreignkey, basestring):
                model.allow_stale_generic_foreignkey = frozenset(
                    dd.fields_list(model,
                                   model.allow_stale_generic_foreignkey))

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

        self.setup_choicelists()
        self.setup_workflows()

        for model in models_list:

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
                    #~ f.rel.to = dd.resolve_model(f.rel.to,strict=True)
                    if isinstance(f.rel.to, basestring):
                        raise Exception("%s %s relates to %r (models are %s)" %
                                        (model, f.name, f.rel.to, models_list))
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
                p.before_analyze(self)

        dd.pre_analyze.send(self, models_list=models_list)
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
                if isinstance(v, dd.VirtualField):
                    v.attach_to_model(model, k)

        #~ logger.info("20130817 attached model vfs")

        actors.discover()

        logger.debug("actors.initialize()")
        for a in actors.actors_list:
            a.class_init()

        dbtables.discover()
        #~ choosers.discover()
        actions.discover_choosers()

        #~ from lino.core import ui
        #~ ui.site_setup(self)

        for a in actors.actors_list:
            a.on_analyze(self)

        dd.post_analyze.send(self, models_list=models_list)

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
        """Yield all database objects in database for which the given
        GenericForeignKey gfk points to the object `obj`.
        """
        if len(self.GFK_LIST) == 0:
            return  # e.g. if contenttypes is not installed
        obj_ct = ContentType.objects.get_for_model(obj.__class__)
        for gfk in self.GFK_LIST:
            kw = dict()
            kw[gfk.fk_field] = obj.pk
            kw[gfk.ct_field] = obj_ct
            ct = ContentType.objects.get_for_model(gfk.model)
            yield gfk, ct.get_all_objects_for_this_type(**kw)

    def abandon_response(self):
        return self.success(_("User abandoned"))

    def get_urls(self):
        raise NotImplementedError()

    def field2elem(self, lui, field, **kw):
        pass

    def run_callback(self, request, thread_id, button_id):
        """
        Return an existing (pending) callback.
        This is called from `lino.ui.views.Callbacks`.
        """
        # logger.info("20131212 get_callback %s %s", thread_id, button_id)

        # 20140304 Also set a renderer so that callbacks can use it
        # (feature needed by beid.FindByBeIdAction).

        ar = ActorRequest(request, renderer=self.default_renderer)

        thread_id = int(thread_id)
        cb = self.pending_threads.pop(thread_id, None)
        #~ d = self.pop_thread(int(thread_id))
        if cb is None:
            logger.debug("No callback %r in %r" % (
                thread_id, self.pending_threads.keys()))
            ar.error("Unknown callback %r" % thread_id)
            return self.render_action_response(ar)

        # e.g. SubmitInsertClient must set `data_record` in the
        # callback request ("ar2", not "ar"), i.e. the methods to
        # create an instance and to fill `data_record` must run on the
        # callback request.  So the callback request must be a clone
        # of the original request.  New since 20140421
        ar.actor = cb.ar.actor
        ar.ah = cb.ar.ah
        ar.bound_action = cb.ar.bound_action
        ar.create_kw = cb.ar.create_kw
        ar.known_values = cb.ar.known_values
        ar.param_values = cb.ar.param_values
        ar.action_param_values = cb.ar.action_param_values
        ar.data_iterator = cb.ar.data_iterator

        # for k in ('data_record', 'goto_record_id'):
        #     v = cb.ar.response.get(k, None)
        #     if v is not None:
        #         ar.response[k] = v
                
        for c in cb.choices:
            if c.name == button_id:
                c.func(ar)
                return self.render_action_response(ar)

        ar.error("Invalid button %r for callback" % (button_id, thread_id))
        return self.render_action_response(ar)

        #~ m = getattr(d,button_id)
        #~ rv = m(request)
        #~ if button_id == 'yes':
            #~ rv = d.yes()
        #~ elif button_id == 'no':
            #~ rv = d.no()
        #~ return self.render_action_response(rv)

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
            if a.parameters is not None and not a.no_params_window:
                ar.set_response(close_window=True)
            a.run_from_ui(ar)
        except exceptions.ValidationError as e:
            def fieldlabel(name):
                de = ar.ah.actor.get_data_elem(name)
                return force_unicode(getattr(de, 'verbose_name', name))
            md = getattr(e, 'message_dict', None)
            if md is not None:
                e = '<br>'.join(["%s : %s" % (fieldlabel(k), v)
                                for k, v in md.items()])
            else:
                e = '<br>'.join(e.messages)
            ar.error(e, alert=True)

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
            ll = layouts.ListLayout(
                h.actor.get_column_names(ar),
                h.actor,
                hidden_elements=h.actor.hidden_columns
                | h.actor.hidden_elements)
            h.list_layout = ll.get_layout_handle(self)
        else:
            h.list_layout = None

        if h.actor.params_layout:
            h.params_layout_handle = h.actor.make_params_layout_handle(self)

        h.store = ext_store.Store(h)

    def render_action_response(self, ar):
        """Builds a JSON response from response information stored in given
        ActionRequest.

        """
        # logger.info("20140430 render_action_response %s", ar.response)
        return views.json_response(ar.response, ar.content_type)

    def row_action_button(self, *args, **kw):
        """
        See :meth:`ExtRenderer.row_action_button`
        """
        return self.default_renderer.row_action_button(*args, **kw)

    def get_media_urls(self):
        #~ print "20121110 get_media_urls"
        from lino.core.dbutils import is_devserver
        from django.conf import settings

        urlpatterns = []

        logger.debug("Checking /media URLs ")
        prefix = settings.MEDIA_URL[1:]
        if not prefix.endswith('/'):
            raise Exception("MEDIA_URL %r doesn't end with a '/'!" %
                            settings.MEDIA_URL)

        # if not self.site.extjs_base_url:
        #     self.setup_media_link(urlpatterns, 'extjs', 'extjs_root')

        # if self.site.use_bootstrap:
        #     if not self.site.bootstrap_base_url:
        #         self.setup_media_link(urlpatterns,
        #             'bootstrap', 'bootstrap_root')

        for p in self.site.installed_plugins:
            if isinstance(p, Plugin):
                p.setup_media_links(self, urlpatterns)

        if self.site.use_tinymce:
            if not self.site.tinymce_base_url:
                self.setup_media_link(urlpatterns, 'tinymce', 'tinymce_root')
        if self.site.use_jasmine:
            self.setup_media_link(urlpatterns, 'jasmine', 'jasmine_root')

        try:
            src = resource_filename(
                Requirement.parse("lino"), "lino/media")
        except DistributionNotFound:
            # if it is not installed using pip, link directly to the source
            # tree
            src = join(dirname(lino.__file__), 'media')

        self.setup_media_link(urlpatterns, 'lino', source=src)

        #~ logger.info("20130409 is_devserver() returns %s.",is_devserver())
        if is_devserver():
            urlpatterns += patterns('django.views.static',
                                    (r'^%s(?P<path>.*)$' % prefix, 'serve',
                                     {'document_root': settings.MEDIA_ROOT,
                                      'show_indexes': True}),
                                    )

        return urlpatterns

    def get_patterns(self):
        # self.site.startup()

        database_ready.send(self.site)

        urlpatterns = self.get_media_urls()

        # urlpatterns += patterns(
        #     '', ('^$', self.default_renderer.plugin.get_index_view()))

        for p in self.site.installed_plugins:
            if isinstance(p, Plugin):
                # urlpatterns += p.get_patterns(self)
                pat = p.get_patterns(self)
                if p.url_prefix:
                    urlpatterns += patterns(
                        '', url('^' + p.url_prefix + "/?",
                                include(pat)))
                else:
                    urlpatterns += pat

        if self.site.django_admin_prefix:  # experimental
            from django.contrib import admin
            admin.autodiscover()
            urlpatterns += patterns('',
                                    ('^' + self.site.django_admin_prefix[1:]
                                     + "/", include(admin.site.urls))
                                    )

        return urlpatterns

    def setup_media_link(self, urlpatterns, short_name,
                         attr_name=None, source=None):
        if not exists(settings.MEDIA_ROOT):
            logger.info("MEDIA_ROOT does not exist: %s",
                        settings.MEDIA_ROOT)
            return
        prefix = settings.MEDIA_URL[1:]
        target = join(settings.MEDIA_ROOT, short_name)
        if exists(target):
            logger.debug("media path exists: %s", target)
            return
        if attr_name is not None:
            # usage is deprecated
            source = getattr(self.site, attr_name)
            if not source:
                raise Exception(
                    "%s does not exist and SITE.%s is not set." % (
                        target, attr_name))
            if not exists(source):
                raise Exception("SITE.%s (%s) does not exist" %
                                (attr_name, source))
        elif not exists(source):
            raise Exception("%s does not exist" % source)
        if is_devserver():
            logger.debug("django.views.static serving /%s%s from %s",
                         prefix, short_name, source)
            urlpatterns.extend(
                patterns(
                    'django.views.static',
                    (r'^%s%s/(?P<path>.*)$' % (prefix, short_name),
                     'serve', {
                         'document_root': source,
                         'show_indexes': False})))
        else:
            symlink = getattr(os, 'symlink', None)
            if symlink is None:
                logger.warning("Cannot create symlink %s -> %s.",
                               target, source)
                #~ raise Exception("Cannot run a production server on an OS that doesn't have symlinks")
            else:
                logger.info("Create symlink %s -> %s.", target, source)
                try:
                    symlink(source, target)
                except OSError as e:
                    raise OSError(
                        "Failed to create symlink %s -> %s : %s",
                        target, source, e)
