# -*- coding: UTF-8 -*-
# Copyright 2009-2013 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

import os
from os.path import join, dirname, exists

import sys
import atexit
#~ import collections
from pkg_resources import Requirement, resource_filename, DistributionNotFound

from django.conf import settings

from django.utils.encoding import force_text

from django.db.models import loading
from django.utils.importlib import import_module
from django.utils.functional import LazyObject

from django.db import models
#from django.shortcuts import render_to_response
#from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from djangosite.signals import database_ready
from django.conf.urls import patterns, url, include


# from django.core.urlresolvers import reverse
# from django.shortcuts import render_to_response, get_object_or_404
# from django.contrib.sites.models import Site, RequestSite
# from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.template import RequestContext, Context, loader
# from django.utils.http import urlquote, base36_to_int
# from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _

# from djangosite.dbutils import obj2unicode

import lino

from lino import dd

from lino.utils import class_dict_items
from lino.core.requests import BaseRequest

from lino.core import layouts
from lino.core import actors
from lino.core import actions
from lino.core import dbtables
from lino.core import tables
from lino.core import constants
from lino.core import web
from lino.core.signals import pre_ui_build, post_ui_build

from lino.ui import store as ext_store

from lino.core.dbutils import is_devserver
from lino.ui.render import PlainRenderer, TextRenderer
from lino.ui import views

ACTION_RESPONSES = frozenset((
    'message', 'success', 'alert',
    'errors',
    'html',
    'goto_record_id',
    'refresh', 'refresh_all',
    'close_window',
    'xcallback',
    'open_url', 'open_davlink_url',
    #~ 'console_message',
    'info_message',
    'warning_message',
    'eval_js'))
"""
Action responses supported by `Lino.action_handler`
(defined in :xfile:`linolib.js`).
"""


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

    def __init__(self, message):

    #~ def __init__(self,message,answers,labels=None):
        self.message = message
        self.choices = []
        self.choices_dict = {}
        #~ self.answers = {}
        #~ self.labels = labels
        #~ self.yes = yes
        #~ self.no = no

        #~ d = Decision(yes,no)
        #~ self.pending_dialogs[d.hash()] = d

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


class DisableDeleteHandler():
    """Used to find out whether a known object can be deleted or not.
    Lino's default behaviour is to forbit deletion if there is any
    other object in the database that refers to this. To implement
    this, Lino installs a DisableDeleteHandler instance on each model
    during :func:`analyze_models`. In an attribute `_lino_ddh`.

    """

    def __init__(self, model):
        self.model = model
        self.fklist = []

    def add_fk(self, model, fk):
        self.fklist.append((model, fk))

    def __str__(self):
        return ','.join([m.__name__ + '.' + fk.name for m, fk in self.fklist])

    def disable_delete_on_object(self, obj):
        #~ print 20101104, "called %s.disable_delete(%s)" % (obj,self)
        #~ h = getattr(self.model,'disable_delete',None)
        #~ if h is not None:
            #~ msg = h(obj,ar)
        #~     if msg is not None:
            #~     return msg
        for m, fk in self.fklist:
            #~ kw = {}
            #~ kw[fk.name] = obj
            #~ if not getattr(m,'allow_cascaded_delete',False):
            if not fk.name in m.allow_cascaded_delete:
                n = m.objects.filter(**{fk.name: obj}).count()
                if n:
                    msg = _("Cannot delete %(self)s \
                    because %(count)d %(refs)s refer to it.") % dict(
                        self=obj, count=n,
                        refs=m._meta.verbose_name_plural
                        or m._meta.verbose_name + 's')
                    #~ print msg
                    return msg
        return None


class Kernel(object):
    """This is the class of the object stored in `settings.SITE.ui`. It is
    (like SITE itself) a "de facto singleton".  But it remains an
    independent class/object instance (and is not merged into the
    Site) because it gets imported and instantiated only when Django
    has finished the models loading.
    
    TODO: Either rename `SITE.ui` to `SITE.kernel`, or rename this to
    something else.  Because "kernel" suggests something which is
    loaded *in first place*, but this object is rather loaded at the
    end (of the startup process).

    """

    def __init__(self, site):
        self.pending_threads = {}
        self.site = site
        self.kernel_startup(site)

        if site.build_js_cache_on_startup is None:
            site.build_js_cache_on_startup = not (
                settings.DEBUG or is_devserver())

        web.site_setup(site)

        for a in actors.actors_list:
            if a.get_welcome_messages is not None:
                site._welcome_actors.append(a)

        pre_ui_build.send(self)

        self.plain_renderer = PlainRenderer(self)
        self.text_renderer = TextRenderer(self)
        self.reserved_names = [getattr(constants, n)
                               for n in constants.URL_PARAMS]

        self.default_renderer = self.plain_renderer

        names = set()
        for n in self.reserved_names:
            if n in names:
                raise Exception("Duplicate reserved name %r" % n)
            names.add(n)

        from lino.utils import codetime
        self.mtime = codetime()
        #~ logger.info("20130610 codetime is %s", datetime.datetime.fromtimestamp(self.mtime))

        for p in site.installed_plugins:
            p.on_ui_init(self)

        post_ui_build.send(self)

        # trigger creation of params_layout.params_store
        for res in actors.actors_list:
            for ba in res.get_actions():
                if ba.action.parameters:
                    ba.action.params_layout.get_layout_handle(self)

    def kernel_startup(kernel, self):
        """
        This is the code that runs when you call 
        This is a part of a Lino site setup.
        The Django Model definitions are done, now Lino analyzes them and does certain actions.

        - Verify that there are no more pending injects
        - Install a DisableDeleteHandler for each Model into `_lino_ddh`
        - Install :class:`lino.dd.Model` attributes and methods into Models that
          don't inherit from it.

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
            self.user_model = dd.resolve_model(self.user_model,
                                               strict="Unresolved model '%s' in user_model.")

        if self.project_model:
            self.project_model = dd.resolve_model(
                self.project_model,
                strict="Unresolved model '%s' in project_model.")

        for m,p in self.override_modlib_models.items():
            dd.resolve_model(
                m,
                strict="%s plugin tries to extend unresolved model '%%s'" %
                p.__class__.__module__)

        for model in models_list:
            #~ print 20130216, model
            #~ fix_field_cache(model)

            model._lino_ddh = DisableDeleteHandler(model)

            for k in dd.Model.LINO_MODEL_ATTRIBS:
                if not hasattr(model, k):
                    #~ setattr(model,k,getattr(dd.Model,k))
                    setattr(model, k, dd.Model.__dict__[k])
                    #~ model.__dict__[k] = getattr(dd.Model,k)
                    #~ logger.info("20121127 Install default %s for %s",k,model)

            if isinstance(model.hidden_columns, basestring):
                model.hidden_columns = frozenset(
                    dd.fields_list(model, model.hidden_columns))

            if model._meta.abstract:
                raise Exception("Tiens?")

            self.modules.define(model._meta.app_label, model.__name__, model)

            for f in model._meta.virtual_fields:
                if isinstance(f, generic.GenericForeignKey):
                    settings.SITE.GFK_LIST.append(f)

        for a in models.get_apps():
            #~ for app_label,a in loading.cache.app_store.items():
            app_label = a.__name__.split('.')[-2]
            #~ logger.info("Installing %s = %s" ,app_label,a)

            for k, v in a.__dict__.items():
                if isinstance(v, type) and issubclass(v, layouts.BaseLayout):
                    #~ print "%s.%s = %r" % (app_label,k,v)
                    self.modules.define(app_label, k, v)
                #~ if isinstance(v,type) and issubclass(v,dd.Plugin):
                    #~ self.plugins.append(v)

                #~ if isinstance(v,type)  and issubclass(v,dd.Module):
                    #~ logger.info("20120128 Found module %s",v)
                if k.startswith('setup_'):
                    self.modules.define(app_label, k, v)

        self.setup_choicelists()
        self.setup_workflows()

        for model in models_list:

            for f, m in model._meta.get_fields_with_model():
                #~ if isinstance(f,models.CharField) and f.null:
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
                        # ~ f.rel.to._lino_ddh.add_fk(model,f) # 20120728
                        f.rel.to._lino_ddh.add_fk(m or model, f)

        dd.pre_analyze.send(self, models_list=models_list)
        # MergeActions are defined in pre_analyze.
        # And MergeAction needs the info in _lino_ddh to correctly find
        # keep_volatiles

        for model in models_list:

            """
            Virtual fields declared on the model must have 
            been attached before calling Model.site_setup(), 
            e.g. because pcsw.Person.site_setup() 
            declares `is_client` as imported field.
            """

            model.on_analyze(self)

            for k, v in class_dict_items(model):
                if isinstance(v, dd.VirtualField):
                    v.attach_to_model(model, k)

        #~ logger.info("20130817 attached model vfs")

        actors.discover()

        actors.initialize()
        dbtables.discover()
        #~ choosers.discover()
        actions.discover_choosers()

        #~ from lino.core import ui
        #~ ui.site_setup(self)

        for a in actors.actors_list:
            a.on_analyze(self)

        #~ logger.info("20130121 GFK_LIST is %s",['%s.%s'%(full_model_name(f.model),f.name) for f in settings.SITE.GFK_LIST])
        dd.post_analyze.send(self, models_list=models_list)

        logger.info("Languages: %s. %d apps, %d models, %s actors.",
                    ', '.join([li.django_code for li in self.languages]),
                    len(self.modules),
                    len(models_list),
                    len(actors.actors_list))

        #~ logger.info(settings.INSTALLED_APPS)

        self.on_each_app('site_setup')

        """
        Actor.after_site_setup() is called after the apps' site_setup().
        Example: pcsw.site_setup() adds a detail to properties.Properties, 
        the base class for properties.PropsByGroup. 
        The latter would not 
        install a `detail_action` during her after_site_setup() 
        and also would never get it later.
        """
        for a in actors.actors_list:
            a.after_site_setup(self)

        #~ self.on_site_startup()

        self.resolve_virtual_fields()

        #~ logger.info("20130827 startup_site done")

    def abandon_response(self):
        return self.success(_("User abandoned"))

    def get_urls(self):
        raise NotImplementedError()

    def field2elem(self, lui, field, **kw):
        pass

    def get_callback(self, request, thread_id, button_id):
        """
        Return an existing (pending) callback.
        This is called from `lino.ui.views.Callbacks`.
        """
        # logger.info("20131212 get_callback %s %s", thread_id, button_id)
        ar = BaseRequest(request)
        thread_id = int(thread_id)
        cb = self.pending_threads.pop(thread_id, None)
        #~ d = self.pop_thread(int(thread_id))
        if cb is None:
            # logger.info("20131212 No callback %r in %r" % (
            #     thread_id, self.pending_threads.keys()))
            ar.error("Unknown callback %r" % thread_id)
            return self.render_action_response(ar.response)
        for c in cb.choices:
            if c.name == button_id:
        #~ rv = c.func(request)
                c.func(ar)
                return self.render_action_response(ar.response)

        ar.error("Invalid button %r for callback" % (button_id, thread_id))
        return self.render_action_response(ar.response)

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
        Calling this from an Action's :meth:`Action.run` method will
        interrupt the execution, send the specified message back to
        the user, adding the executables `yes` and optionally `no` to a queue
        of pending "dialog threads".
        The client will display the prompt and will continue this thread
        by requesting :class:`lino.ui.extjs3.views.Callbacks`.
        """
        if len(msgs) > 1:
            msg = '\n'.join([force_text(s) for s in msgs])
        else:
            msg = msgs[0]

        return Callback(msg)

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

        ar.response.update(
            success=True,
            message=cb.message,
            xcallback=dict(id=h,
                           title=cb.title,
                           buttons=buttons))

    def check_action_response(self, rv):
        """
        Raise an exception if the action responded using an unknown keyword.
        """

        #~ if rv is None:
            #~ rv = self.success()

        #~ elif isinstance(rv,Callback):

        for k in rv.keys():
            if not k in ACTION_RESPONSES:
                raise Exception("Unknown key %r in action response." % k)
        return rv

    def run_action(self, ar):
        """
        """
        try:
            ar.bound_action.action.run_from_ui(ar)
            return self.render_action_response(ar.response)
        except Warning as e:
            ar.error(unicode(e), alert=True)
            #~ r = dict(
              #~ success=False,
              #~ message=unicode(e),
              #~ alert=True)
            return self.render_action_response(ar.response)
        #~ removed 20130913
        #~ except Exception as e:
            #~ if len(ar.selected_rows) == 0:
                #~ msg = unicode(e)
            #~ else:
                #~ elem = ar.selected_rows[0]
                #~ if isinstance(elem,models.Model):
                    #~ elem = obj2unicode(elem)
                #~ msg = _(
                  #~ "Action \"%(action)s\" failed for %(record)s:") % dict(
                  #~ action=ar.bound_action.full_name(),
                  #~ record=elem)
                #~ msg += "\n" + unicode(e)
            #~ msg += '.\n' + unicode(_(
              #~ "An error report has been sent to the system administrator."))
            #~ logger.warning(msg)
            #~ logger.exception(e)
            #~ r = self.error(e,msg,alert=_("Oops!"))
            #~ return self.render_action_response(r)

    def setup_handle(self, h, ar):
        """
        ar is usually None, except for actors with dynamic handle
        """
        if h.actor.is_abstract():
            return

        #~ logger.info('20121010 ExtUI.setup_handle() %s',h.actor)

        if isinstance(h, tables.TableHandle):
            ll = layouts.ListLayout(
                h.actor.get_column_names(ar),
                h.actor,
                hidden_elements=h.actor.hidden_columns
                | h.actor.hidden_elements)
            h.list_layout = ll.get_layout_handle(self)
        else:
            h.list_layout = None

        if h.actor.parameters:
            h.params_layout_handle = h.actor.make_params_layout_handle(self)

        h.store = ext_store.Store(h)

    def render_action_response(self, rv):
        """
        Builds a JSON response from given dict ``rv``, 
        checking first whether there are only allowed keys 
        (defined in :attr:`ACTION_RESPONSES`)
        """
        rv = self.check_action_response(rv)
        return views.json_response(rv)

    def row_action_button(self, *args, **kw):
        """
        See :meth:`ExtRenderer.row_action_button`
        """
        return self.default_renderer.row_action_button(*args, **kw)

    def get_media_urls(self):
        #~ print "20121110 get_media_urls"
        from django.conf.urls import patterns, url, include
        from lino.core.dbutils import is_devserver
        from django.conf import settings

        urlpatterns = []

        logger.debug("Checking /media URLs ")
        prefix = settings.MEDIA_URL[1:]
        if not prefix.endswith('/'):
            raise Exception("MEDIA_URL %r doesn't end with a '/'!" %
                            settings.MEDIA_URL)

        if not self.site.extjs_base_url:
            self.setup_media_link(urlpatterns,'extjs', 'extjs_root')
        if self.site.use_bootstrap:
            if not self.site.bootstrap_base_url:
                self.setup_media_link(urlpatterns,
                    'bootstrap', 'bootstrap_root')
        for p in self.site.installed_plugins:
            p.setup_media_links(self, urlpatterns)

        if self.site.use_tinymce:
            if not self.site.tinymce_base_url:
                self.setup_media_link(urlpatterns,
                    'tinymce', 'tinymce_root')
        if self.site.use_jasmine:
            self.setup_media_link(urlpatterns,
                'jasmine', 'jasmine_root')
        if self.site.use_eid_jslib:
            self.setup_media_link(urlpatterns,
                'eid-jslib', 'eid_jslib_root')

        try:
            self.setup_media_link(urlpatterns,
                'lino', source=resource_filename(
                    Requirement.parse("lino"), "lino/media"))
        except DistributionNotFound:
            # if it is not installed using pip, link directly to the source
            # tree
            self.setup_media_link(urlpatterns,
                'lino', source=join(dirname(lino.__file__), 'media'))

        #~ logger.info("20130409 is_devserver() returns %s.",is_devserver())
        if is_devserver():
            urlpatterns += patterns('django.views.static',
                                    (r'^%s(?P<path>.*)$' % prefix, 'serve',
                                     {'document_root': settings.MEDIA_ROOT,
                                      'show_indexes': True}),
                                    )

        return urlpatterns

    def get_pages_urls(self):
        from django.conf.urls import patterns, url, include
        from django import http
        from django.views.generic import View
        from lino import dd
        pages = dd.resolve_app('pages')

        class PagesIndex(View):

            def get(self, request, ref='index'):
                if not ref:
                    ref = 'index'

                #~ print 20121220, ref
                obj = pages.lookup(ref, None)
                if obj is None:
                    raise http.Http404("Unknown page %r" % ref)
                html = pages.render_node(request, obj)
                return http.HttpResponse(html)

        return patterns('',
                        (r'^(?P<ref>\w*)$', PagesIndex.as_view()),
                        )

    def get_plain_urls(self):

        from django.conf.urls import patterns, url, include
        from lino.ui import views
        urlpatterns = []
        rx = '^'
        urlpatterns = patterns(
            '',
            (rx + r'$', views.PlainIndex.as_view()),
            (rx + r'(?P<app_label>\w+)/(?P<actor>\w+)$',
             views.PlainList.as_view()),
            (rx + r'(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
             views.PlainElement.as_view()),
        )
        return urlpatterns

    def get_patterns(self):
        # self.site.startup()

        database_ready.send(self.site)

        urlpatterns = self.get_media_urls()

        for p in self.site.installed_plugins:
            urlpatterns += p.get_patterns(self)

        # if self.site.use_extjs and self.site.admin_prefix:
        #     urlpatterns += patterns(
        #         '',
        #         ('^' + self.site.admin_prefix, include(self.get_ext_urls())))

        if self.site.plain_prefix:
            urlpatterns += patterns(
                '',
                ('^' + self.site.plain_prefix + "/",
                 include(self.get_plain_urls()))
            )

        if self.site.django_admin_prefix:  # experimental
            from django.contrib import admin
            admin.autodiscover()
            urlpatterns += patterns('',
                                    ('^' + self.site.django_admin_prefix[1:]
                                     + "/", include(admin.site.urls))
                                    )

        if not self.site.plain_prefix:
            urlpatterns += self.get_plain_urls()

        # if self.site.use_extjs:
        #     if not self.site.admin_prefix:
        #         urlpatterns += self.get_ext_urls()
        #     else:
        #         urlpatterns += self.get_pages_urls()

        #~ print 20131021, urlpatterns
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
            #~ logger.info("20130409 path exists: %s",target)
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
            #~ logger.info("django.views.static serving /%s%s from %s",prefix,short_name,source)
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
                logger.info("Cannot create symlink %s -> %s.",
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

