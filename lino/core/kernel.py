# -*- coding: UTF-8 -*-
# Copyright 2009-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This defines the :class:`Kernel` class.

The "kernel" of a Lino site is (like `SITE` itself) a "de facto
singleton", available to application code as ``SITE.kernel`` (and its
alias for backwards compatibility: ``SITE.ui``).

The kernel is instantiated at the end of the startup process, when the
:setting:`SITE` has been instantiated and models have been loaded.  It
encapsulates a bunch of functionality which becomes available only
then.

TODO: Rename "kernel" to "environment".  Because "kernel" suggests
something which is loaded *in first place*. That's not true for Lino's
"kernel".  it should be renamed to :mod:`lino.core.env` (for
"environment") because it represents the runtime environment of a Lino
application.

"""
from __future__ import unicode_literals, print_function
import six
from builtins import object

import logging ; logger = logging.getLogger(__name__)

import os
from os.path import join, dirname, exists

import sys
import time
# import copy
import codecs
import atexit
import threading
from importlib import import_module


from django.apps import AppConfig
from django.apps import apps
from django.conf import settings
from django.core import exceptions
from django.utils.encoding import force_text
from django.core.exceptions import PermissionDenied
from django.db.utils import DatabaseError

from django.db import models

from django.utils.translation import ugettext_lazy as _

import lino  # for is_testing
from lino.utils import codetime
from lino.core import layouts
from lino.core import actors
from lino.core import actions
from lino.core import frames
from lino.core import fields
from lino.core import dbtables
from lino.core import choicelists
from lino.core import workflows
from lino.core import tables
from lino.core import constants
from lino.utils.memo import Parser
from etgen.html import E
from lino.core.requests import ActorRequest
from lino.core.model import Model
from lino.core.roles import UserRole
from lino.core.store import Store
from lino.core.renderer import HtmlRenderer, TextRenderer
from lino.core.gfks import ContentType, GenericForeignKey
from lino.core.signals import (pre_ui_build, post_ui_build,
                               pre_startup, post_startup,
                               pre_analyze, post_analyze)

from .exceptions import ChangedAPI
from .plugin import Plugin
from .ddh import DisableDeleteHandler
from .utils import resolve_model
from .utils import is_devserver, UnresolvedModel
from .utils import full_model_name as fmn
from .utils import obj2str
from .utils import get_models
from .utils import resolve_fields_list
from .utils import djangoname
from .utils import class_dict_items

# from .inject import collect_virtual_fields
from .fields import set_default_verbose_name


startup_rlock = threading.RLock()  # Lock() or RLock()?



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
    """
    This is the class of the object stored in :attr:`Site.kernel
    <lino.core.site.Site.kernel>`.

    .. attribute:: memo_parser

        An instance of :class:`lino.utils.memo.Parser`.

    """
    default_ui = None
    admin_ui = None

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

        # from importlib import import_module
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
        # self.widgets = WidgetFactory()

        self.kernel_startup(site)
        # logger.info("20140227 Kernel.__init__() done")


    _code_mtime = None

    @property
    def code_mtime(self):
        # We set `code_mtime` only after kernel_startup() because
        # codetime watches only those modules which are already
        # imported.
        if self._code_mtime is None:
            self._code_mtime = codetime()
        return self._code_mtime
        

    def kernel_startup(self, site):
        """This is a part of a Lino site startup.  The Django Model
        definitions are done, now Lino analyzes them and does certain
        actions:

        - Install a :class:`DisableDeleteHandler
          <lino.core.ddh.DisableDeleteHandler>` for each Model into
          `_lino_ddh`.

        - Install :class:`lino.core.model.Model` attributes and
          methods into Models that don't inherit from it.

        """
        # logger.info("20161219 kernel_startup")
        if site.history_aware_logging:
            if len(sys.argv) == 0:
                process_name = 'WSGI'
            else:
                process_name = ' '.join(sys.argv)

            logger.info("Started %s (using %s) --> PID %s",
                        process_name, settings.SETTINGS_MODULE, os.getpid())

            def goodbye():
                logger.info("Done %s (PID %s)", process_name, os.getpid())
            atexit.register(goodbye)

        models_list = get_models(include_auto_created=True)
        # this also triggers django.db.models.loading.cache._populate()

        site.setup_model_spec(site, 'user_model')
        site.setup_model_spec(site, 'project_model')

        for app_name_model, p in site.override_modlib_models.items():
            # app_name_model is the full installed app module name +
            # the model name. It certainly contains at least one dot.
            m = '.'.join(app_name_model.split('.')[-2:])
            resolve_model(
                m,
                strict="{!r} tries to extend unresolved model '%s'".format(
                    p.__module__))
                # strict="%s plugin tries to extend unresolved model '%%s'" %
                # p.__class__.__module__)

        for model in models_list:
            #~ print 20130216, model
            #~ fix_field_cache(model)

            # if hasattr(model, '_lino_ddh'):
            if '_lino_ddh' in model.__dict__:
                raise Exception("20150831 %s", model)
            model._lino_ddh = DisableDeleteHandler(model)

            Model.django2lino(model)

            if isinstance(model.hidden_columns, six.string_types):
                model.hidden_columns = frozenset(
                    fields.fields_list(model, model.hidden_columns))

            if isinstance(model.active_fields, six.string_types):
                model.active_fields = frozenset(
                    fields.fields_list(model, model.active_fields))

            if isinstance(model.allow_cascaded_delete, six.string_types):
                model.allow_cascaded_delete = frozenset(
                    fields.fields_list(model, model.allow_cascaded_delete))

            if isinstance(model.allow_cascaded_copy, six.string_types):
                model.allow_cascaded_copy = frozenset(
                    fields.fields_list(model, model.allow_cascaded_copy))

            # Note how to inherit this from from parent model.
            if model.quick_search_fields is None:
                fields_list = []
                for field in model._meta.fields:
                    if isinstance(field, (models.CharField, models.TextField)):
                        fields_list.append(field)
                model.quick_search_fields = tuple(fields_list)
            else:
                resolve_fields_list(model, 'quick_search_fields')

            if model.quick_search_fields_digit is None:
                fields_list = []
                for field in model._meta.fields:
                    if isinstance(field, (
                            models.IntegerField, models.AutoField)):
                        fields_list.append(field)
                model.quick_search_fields_digit = tuple(fields_list)
            else:
                resolve_fields_list(model, 'quick_search_fields_digit')
                
            if model._meta.abstract:
                raise Exception("Tiens?")

            # site.modules.define(model._meta.app_label, model.__name__, model)

            # Django 1.10 : The private attribute virtual_fields of
            # Model._meta is deprecated in favor of private_fields.
            for f in model._meta.private_fields:
                if isinstance(f, GenericForeignKey):
                    self.GFK_LIST.append(f)
            self.GFK_LIST.sort(key=lambda f: str(f))

        site.load_actors()

        # raise Exception("20190102 {!r}".format(site.models.courses.CoursesByLine.detail_link))

        # vip_classes = (layouts.BaseLayout, fields.Dummy)
        # for a in models.get_apps():
        #     app_label = a.__name__.split('.')[-2]

        #     for k, v in a.__dict__.items():
        #         if isinstance(v, type) and issubclass(v, vip_classes):
        #             site.modules.define(app_label, k, v)

        #         if k.startswith('setup_'):
        #             site.modules.define(app_label, k, v)

        site.user_roles = []
        if site.user_types_module:
            m = import_module(site.user_types_module)
            for k in dir(m):
                v = getattr(m, k)
                if not v is UserRole:
                    if isinstance(v, type) and issubclass(v, UserRole):
                        if v.__module__ != site.user_types_module:
                            site.user_roles.append(v)
            site.user_roles.sort(key=djangoname)

        # site.setup_choicelists()
        
        # site.setup_workflows()

        # Check for nullable charfields.
        # Initialize _lino_ddh for all models.
        for model in models_list:
            if model._meta.auto_created:
                continue  # automatic intermediate models created by
                          # ManyToManyField should not disable delete
            # for f, m in model._meta.get_fields_with_model():
            for f in model._meta.get_fields():
                m = f.model

                # no longer needed with Django 1.11+ (?)
                # Refuse nullable CharFields, but don't trigger on
                # NullableCharField (which is a subclass of CharField).
                # if f.__class__ is models.CharField and f.null:
                #     msg = "Nullable CharField %s in %s" % (f.name, model)
                #     raise Exception(msg)
                if isinstance(f, models.ForeignKey):
                    if isinstance(f.remote_field.model, six.string_types):
                        raise Exception("Could not resolve target %r of "
                                        "ForeignKey '%s' in %s "
                                        "(models are %s)" %
                                        (f.remote_field.model, f.name, model, models_list))

                    set_default_verbose_name(f)

                    """
                    If JobProvider is an MTI child of Company,
                    then mti.delete_child(JobProvider) must not fail on a
                    JobProvider being referred only by objects that can refer
                    to a Company as well.
                    """
                    if not hasattr(f.remote_field.model, '_lino_ddh'):
                        msg = "20150824 {1} (needed by {0}) "\
                              "has no _lino_ddh"
                        raise Exception(msg.format(
                            f.remote_field, f.remote_field.model))
                    f.remote_field.model._lino_ddh.add_fk(m or model, f)

            fieldnames = {f.name for f in model._meta.get_fields()}
            # print("20190627 checking ", model, fieldnames)
            for m, k, v in class_dict_items(model):
                if isinstance(v, fields.VirtualField) and k in fieldnames:
                    f = model._meta.get_field(k)
                    if f.__class__ is v.__class__:
                        # a copy of the virtual field in parent has already been attached
                        # print("20190627 ignoring", m, k, v, f)
                        continue
                    raise ChangedAPI(
                        "{} field {}.{} hidden by virtual field of same name.".format(
                            f.__class__.__name__, fmn(model), k))




        # Protect the foreign keys by removing Django's default
        # behaviour of having on_delete with CASCADE as default.
        
        self.protect_foreignkeys(models_list)
        
        if site.workflows_module:
            import_module(site.workflows_module)

        for p in site.installed_plugins:
            if isinstance(p, Plugin):
                p.before_analyze()

        # logger.info("20150429 Gonna send pre_analyze signal")
        pre_analyze.send(site, models_list=models_list)
        # logger.info("20150429 pre_analyze signal done")
        # MergeActions are defined in pre_analyze.
        
        # MergeAction needs the info in _lino_ddh to correctly find
        # keep_volatiles

        site.setup_actions()

        if site.custom_layouts_module:
            import_module(site.custom_layouts_module)

        for model in models_list:
            model.on_analyze(site)

        #~ logger.info("20130817 attached model vfs")

        # Attach virtual fields to the model that declares them   This must be
        # done before calling Model.site_setup(), e.g. because
        # pcsw.Person.site_setup() declares `is_client` as imported field.

        for model in models_list:
            model.collect_virtual_fields()

        # for vt in virtual_tables:
        #     if vt.model is not None:
        #         assert vt.model._lino_default_table is None
        #         vt.model._lino_default_table = vt
        #         collect_virtual_fields(vt.model)

        # # set the verbose_name of the detail_link field on each model
        # for model in models_list:
        #     for vf in model._meta.private_fields:
        #         if vf.name == 'detail_link':
        #             # if vf.verbose_name  == 'detail_link':
        #             # vf.verbose_name = model._meta.verbose_name
        #
        #             # note that the verbose_name of a virtual field is a copy
        #             # of the verbose_name of its return_type (see
        #             # VirtualField.lino_resolve_type)
        #             vf.verbose_name = model._meta.verbose_name
        #             vf.return_type.verbose_name = model._meta.verbose_name
        #             # if model.__name__ == "Course":
        #             #     print("20181212", model)
        #             break

        # Install help texts to all database fields:
        for model in models_list:
            for f in model._meta.get_fields():
                site.install_help_text(f, model, f.name)
                
        actors.discover()

        logger.debug("actors.initialize()")
        for a in actors.actors_list:
            a.class_init()

        register_actors()

        # Create default tables. Every model for which there is no
        # table at all, will now get an automatically created default
        # table.  This includes automatic models created by
        # ManyToManyField.
        for model in models_list:
            # Not getattr but __dict__.get because of the mixins.Listings
            # trick:
            rpt = model.__dict__.get('_lino_default_table', None)
            # rpt = getattr(model,'_lino_default_table',None)
            # logger.debug('20111113 %s._lino_default_table = %s',model,rpt)
            if rpt is None:
                rpt = dbtables.table_factory(model)
                if rpt is None:
                    raise Exception("table_factory() failed for %r." % model)
                # print ("20170104 No table for {}, created default table.".format(model))
                register_model_table(rpt)
                rpt.class_init()
                # rpt.collect_actions()
                model._lino_default_table = rpt

        
        #~ choosers.discover()
        actions.discover_choosers()

        for a in actors.actors_list:
            a.on_analyze(site)

        for a in actors.actors_list:
            if issubclass(a, tables.AbstractTable) and not a.abstract:
                try:
                    a.setup_columns()
                except DatabaseError:
                    logger.debug(
                        "Ignoring DatabaseError in %s.setup_columns", a)

        post_analyze.send(site, models_list=models_list)

        if False:
            logger.info("Languages: %s. %d apps, %d models, %s actors.",
                        ', '.join([li.django_code for li in site.languages]),
                        len(site.modules),
                        len(models_list),
                        len(actors.actors_list))

        #~ logger.info(settings.INSTALLED_APPS)

        site.setup_layouts()

        site.on_each_app('site_setup')
        # Deprecated. Use custom_layouts_module instead.


        # Actor.after_site_setup() is called after the plugins's
        # site_setup().  Example: pcsw.site_setup() adds a detail to
        # properties.Properties, the base class for
        # properties.PropsByGroup.  The latter would not install a
        # `detail_action` during her after_site_setup() and also would
        # never get it later.
        
        # In a first loop we run it on actors who are being used as
        # default tables for a model. Because the defining_actor of
        # model actions will be the first actor to which they get
        # attached.

        later = []
        for a in actors.actors_list:
            if isinstance(a.model, type) and issubclass(a.model, models.Model) \
                    and a == a.model.get_default_table():
                a.after_site_setup(site)
            else:
                later.append(a)
        for a in later:
            a.after_site_setup(site)

        # choicelists.ChoiceList.after_site_setup(site)
        # workflows.Workflow.after_site_setup(site)
        # workflows.Workflow.after_site_setup(site)
        # actors.Actor.after_site_setup(site)

        # site.resolve_virtual_fields()

        self.memo_parser = Parser()

        def url2html(parser, s):
            url_text = s.split(None, 1)
            if len(url_text) == 1:
                url = text = url_text[0]
            else:
                url, text = url_text
            return '<a href="%s" target="_blank">%s</a>' % (url, text)

        self.memo_parser.register_command('url', url2html)

        if 'LINO_BUILD_CACHE_ON_STARTUP' in os.environ:
            site.build_js_cache_on_startup = True
        if site.build_js_cache_on_startup is None:
            site.build_js_cache_on_startup = not (
                settings.DEBUG or is_devserver())

        # web.site_setup(site)

        for a in actors.actors_list:
            
            site.install_help_text(a)
            if a.parameters is not None:
                for name, fld in a.parameters.items():
                    site.install_help_text(fld, a, name)

            for ba in a.get_actions():
                # site.install_help_text(
                #     ba.action.__class__, ba.action.action_name)
                # site.install_help_text(ba.action, a, ba.action.action_name)
                # site.install_help_text(ba.action, ba.action.__class__)
                if a.model is not None:
                    site.install_help_text(
                        ba.action, a.model, ba.action.action_name)
                site.install_help_text(
                    ba.action, a, ba.action.action_name)
                site.install_help_text(ba.action.__class__)
                # site.install_help_text(
                #     ba.action, ba.action.__class__,
                #     attrname=ba.action.action_name)

                if ba.action.parameters is not None:
                    for name, fld in ba.action.parameters.items():
                        site.install_help_text(
                            fld, ba.action.__class__, name)
            
        self.reserved_names = [getattr(constants, n)
                               for n in constants.URL_PARAMS]

        names = set()
        for n in self.reserved_names:
            if n in names:
                raise Exception("Duplicate reserved name %r" % n)
            names.add(n)

        pre_ui_build.send(self)

        # 20160530
        # self.html_renderer = HtmlRenderer(self)
        # self.text_renderer = TextRenderer(self)

        for p in site.installed_plugins:
            p.on_ui_init(self)

        site.resolve_virtual_fields()

        for p in self.site.installed_plugins:
            if p.app_name == self.site.default_ui:
                p.url_prefix = None
                self.default_renderer = p.renderer
                self.default_ui = p
                self.html_renderer = HtmlRenderer(p)
                self.text_renderer = TextRenderer(p)
                break
        if self.site.admin_ui is not None:
            for p in self.site.installed_plugins:
                if p.app_name == self.site.admin_ui:
                    self.admin_ui  = p

        # 20160530

        for a in actors.actors_list:
            
            if a.get_welcome_messages is not None:
                site.add_welcome_handler(
                    a.get_welcome_messages, a, "get_welcome_messages")
            if a.welcome_message_when_count is not None:
                
                def handler(cls):
                
                    def get_welcome_messages(ar):
                        sar = ar.spawn(cls)
                        # if not cls.get_view_permission(ar.get_user().user_type):
                        if not sar.get_permission():
                            # raise Exception(20160814)
                            return
                        num = sar.get_total_count()
                        if num > cls.welcome_message_when_count:
                            chunks = [six.text_type(_("You have "))]
                            txt = _("{0} items in {1}").format(num, cls.label)
                            chunks.append(ar.href_to_request(sar, txt))
                            chunks.append('.')
                            yield E.span(*chunks)
                    return get_welcome_messages
               
                site.add_welcome_handler(
                    handler(a), a, 'welcome_message_when_count')

        post_ui_build.send(self)

        # trigger creation of params_layout.params_store
        for res in actors.actors_list:
            for ba in res.get_actions():
                if ba.action.params_layout is not None:
                    ba.action.params_layout.get_layout_handle(
                        self.default_ui)
        # logger.info("20161219 kernel_startup done")

    def protect_foreignkeys(self, models_list):
        """Change `on_delete` from CASCADE (Django's default value) to PROTECT
        for foreignkeys that need to be protected.

        Basically we protect all FK fields that are not listed in
        their model's :attr:`allow_cascaded_delete
        <lino.core.model.Model.allow_cascaded_delete>`. With one
        exception: pointers to the MTI parent of a :class:`Polymorphic
        <lino.mixins.polymorphic.Polymorphic>` must not
        become protected (because Lino handles it automatically, see
        :meth:`lino.mixins.polymorphic.Polymorphic.disable_delete`).

        """

        from lino.mixins.polymorphic import Polymorphic

        def must_protect(m, fk, model):
            # Whether the given foreign key fk
            if fk.name in m.allow_cascaded_delete:
                return False
            if m is model:  # FK to self
                return True
            # if issubclass(m, model) or issubclass(model, m):
            if issubclass(m, model):
                if issubclass(m, Polymorphic):
                    # they have an MTI relation
                    return False
            return True

        for model in models_list:
            for m, fk in model._lino_ddh.fklist:
                assert fk.remote_field.model is model
                if fk.remote_field.on_delete == models.CASCADE:
                    if must_protect(m, fk, model):
                        # 20170921 removed disturbing debug message 
                        # msg = (
                        #     "Setting {0}.{1}.on_delete to PROTECT because "
                        #     "field is not specified in "
                        #     "allow_cascaded_delete.").format(fmn(m), fk.name)
                        # logger.debug(msg)
                        fk.remote_field.on_delete = models.PROTECT
                else:
                    if fk.name in m.allow_cascaded_delete:
                        msg = ("{0}.{1} specified in allow_cascaded_delete "
                               "but on_delete is not CASCADE").format(
                            fmn(m), fk.name)
                        raise Exception(msg)
    
                    if fk.remote_field.on_delete == models.SET_NULL:
                        if not fk.null:
                            msg = ("{0}.{1} has on_delete SET_NULL but "
                                   "is not nullable ")
                            msg = msg.format(fmn(m), fk.name, fk.remote_field.model)
                            raise Exception(msg)

                    else:
                        msg = ("{0}.{1} has custom on_delete").format(
                            fmn(m), fk.name, fk.remote_field.on_delete)
                        logger.debug(msg)
                
    def get_generic_related(self, obj):
        """Yield a series of `(gfk, fk_field, queryset)` tuples which together
         will return all database objects for which the given
         GenericForeignKey gfk points to the object `obj`. See also
         :doc:`/dev/gfks`.

        """
        if len(self.GFK_LIST) == 0:
            return  # e.g. if contenttypes is not installed

        from django.contrib.contenttypes.models import ContentType

        if not isinstance(obj._meta.pk, GFK_TARGETS):
            # raise Exception("20150330 %s", obj._meta.pk)
            return  # e.g. Country.iso_code is a CharField, cannot
                    # point to a country using GFK
        obj_ct = ContentType.objects.get_for_model(obj.__class__)
        # logger.info("20150330 ok %s", obj_ct)
        for gfk in self.GFK_LIST:
            fk_field = gfk.model._meta.get_field(gfk.fk_field)
            # fk_field, remote_model, direct, m2m = \
            #     gfk.model._meta.get_field_by_name(gfk.fk_field)
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
    
        Each yielded object has two special attributes:
    
        - `_message` : a textual description of the problem
        - `_todo` : 'delete', 'clear' or 'manual'

        Note: the "clear" action should not run automatically, at
        least not for :mod:`lino.modlib.changes`.

        """
        gfks = [f for f in self.GFK_LIST if f.model is model]
        if len(gfks):
            for gfk in gfks:
                fk_field = gfk.model._meta.get_field(gfk.fk_field)
                # fk_field, remote_model, direct, m2m = \
                #     gfk.model._meta.get_field_by_name(gfk.fk_field)
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

        thread_id = thread_id
        cb = self.pending_threads.pop(thread_id, None)
        if cb is None:
            ar = ActorRequest(request, renderer=self.default_renderer)
            logger.debug("No callback %r in %r" % (
                thread_id, list(self.pending_threads.keys())))
            ar.error("Unknown callback %r" % thread_id)
            return ar.renderer.render_action_response(ar)

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
                a = ar.bound_action.action
                if self.site.log_each_action_request and not a.readonly:
                    logger.info("run_callback {0} {1} {2}".format(
                        thread_id, cb.message, c.name))
                    # ar.info(cb.message)
                try:
                    c.func(ar)
                except Warning as e:
                    ar.error(e, alert=True)
                return ar.renderer.render_action_response(ar)

        ar.error("Invalid button %r for callback %r" % (button_id, thread_id))
        return ar.renderer.render_action_response(ar)

    def add_callback(self, ar, *msgs):
        """
        Returns an *action callback* which will initiate a dialog thread by
        asking a question to the user and suspending execution until
        the user's answer arrives in a next HTTP request.

        Calling this from an Action's :meth:`run_from_ui
        <lino.core.actions.Action.run_from_ui>` method will interrupt
        the execution, send the specified message back to the user,
        adding the executables `yes` and optionally `no` to a queue of
        pending "dialog threads".

        The client will display the prompt and will continue this
        thread by requesting
        :class:`lino.modlib.extjs.views.Callbacks`.
        """
        if len(msgs) > 1:
            msg = '\n'.join([force_text(s) for s in msgs])
        else:
            msg = msgs[0]
        # logger.info("20160526 add_callback(%s)", msg)
        return Callback(ar, msg)

    def set_callback(self, ar, cb):
        """
        """
        k = "{0:x}".format(hash(cb))
        self.pending_threads[k] = cb
        # logger.info("20160526 Stored %r in %r" % (
        #     h, self.pending_threads))

        buttons = dict()
        for c in cb.choices:
            buttons[c.name] = c.label

        ar.success(
            cb.message, xcallback=dict(
                id=k,
                title=cb.title,
                buttons=buttons))

    def run_action(self, ar):
        """Run the action, catching some exceptions in order to report them
        in a user-friendly way.

        """
        
        if not ar.get_permission():
            msg = "{} has no permission to run this request".format(
                ar.get_user())
            msg = "No permission to run {}".format(ar)
            # raise Exception(msg)
            raise PermissionDenied(msg)
        
        a = ar.bound_action.action
        if not a.readonly:
            if self.site.readonly:
                ar.error(_("Server is in readonly mode"), alert=True)
                return ar.renderer.render_action_response(ar)
            if self.site.log_each_action_request:
                flds = []
                A = flds.append
                a = ar.bound_action.action
                # A(a.__class__.__module__+'.'+a.__class__.__name__)
                A(ar.get_user().username)
                A(ar.bound_action.full_name())
                A(obj2str(ar.master_instance))
                A(obj2str(ar.selected_rows))
                # A(format_request(ar.request))
                logger.info("run_action {0}".format(' '.join(flds)))
                # logger.info("run_action {0}".format(ar))
        try:
            a.run_from_ui(ar)
            if a.parameters and not a.no_params_window:
                ar.set_response(close_window=True)
        except exceptions.ValidationError as e:
            # logger.info("20150127 run_action %r", e)
            ar.error(ar.ah.actor.error2str(e), alert=True)
        except Warning as e:
            ar.error(e, alert=True)

        return ar.renderer.render_action_response(ar)

    def setup_handle(self, h, ar):
        """
        Additional setup of an actor handle.  This is called lazily for
        every actor handle because it potentially requires other actor
        handles to be instantiated.

        ar is usually None, except for actors with dynamic handle
        """
        # logger.info('20121010 Kernel.setup_handle() %s', h.actor)

        # 20170905 IntracomInvoices
        # if h.actor.is_abstract():
        #     return

        if isinstance(h, tables.TableHandle):
            he = set(h.actor.hidden_columns | h.actor.hidden_elements)
            ll = layouts.ColumnsLayout(
                h.actor.get_column_names(ar),
                h.actor, hidden_elements=he)
            h.list_layout = ll.get_layout_handle(self.default_ui)
        else:
            h.list_layout = None

        if h.actor.params_layout:
            h.params_layout_handle = h.actor.make_params_layout_handle()
        h.store = Store(h)
        # logger.info("18072017, h:|%s|, h.store:|%s| #1955"%(h, h.store))

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
        if not force and not self._must_build and exists(fn):
            mtime = os.stat(fn).st_mtime
            if mtime > self.code_mtime:
                logger.debug("%s (%s) is up to date.", fn, time.ctime(mtime))
                return 0

        # The following message is important to see in a developer
        # console because the process takes some time and when
        # developing you are watching at such messages. It should
        # *not* be shown when running unit tests because its occurence
        # is not (easily) predictable.  OTOH we would like it to be
        # logged on a production site as well.
        if self.site.is_demo_site:
            logger.debug("Building %s ...", fn)
        else:
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

    
def site_startup(self):    
    """This is being imported and called from
    :meth:`lino.core.site.Site.startup`. It is implemented here in
    order to avoid local imports.

    """
    with startup_rlock:

        # if self.cache_dir is not None:
        #     raise Exception("No cache_dir is defined. "
        #                     "Check your LINO_CACHE_ROOT and project_name.")

        if self._starting_up:
            # This is needed because Django imports the
            # settings module twice. The phenomen is not fully
            # explained, but without this test we had the startup
            # code being run twice, which caused various error
            # messages (e.g. Duplicate label in workflow setup)

            # print("20161219 starting up (pid:%s)" % os.getpid())
            
            return

        if self._startup_done:
            # print("20161219 startup already done (pid:%s)" % os.getpid())
            return

        self._starting_up = True

        # print(
        #     "20161219 Site.startup() %s (pid:%s)" % (self, os.getpid()))
        
        # print "20151010 Site.startup()"

        # if AFTER17:
        #     print "20151010 Site.startup() gonna call django.setup"
        #     import django
        #     django.setup()

        for a in apps.get_app_configs():
            self.models.define(six.text_type(a.label), a.models_module)

        # print("20181230 SITE.models ready {}".format(self.models.keys()))
        # the following was equivalent of above until Django 1.9
        
        # for p in self.installed_plugins:
        #     # m = loading.load_app(p.app_name, False)
        #     # In Django17+ we cannot say can_postpone=False,
        #     # and we don't need to, because anyway we used it
        #     # just for our hack in `lino.models`
        #     # load_app(app_name) is deprecated
        #     # from django.apps import apps
        #     # m = apps.load_app(p.app_name)
        #     try:
        #         app_config = AppConfig.create(p.app_name)
        #         try:
        #             app_config.import_models()
        #         except AttributeError:
        #             raise Exception("Failed to import models for {}".format(p))
        #         # app_config.import_models(
        #         #     apps.all_models[app_config.label])
        #         apps.app_configs[app_config.label] = app_config
        #         apps.clear_cache()
        #         m = app_config.models_module
        #     except ImportError:
        #         logger.debug("No module {0}.models", p.app_name)
        #         # print(rrrr)

        #     self.models.define(six.text_type(p.app_label), m)

        pre_startup.send(self)

        for p in self.installed_plugins:
            p.on_site_startup(self)

        # for k, v in self.models.items():
        #     self.actors.setdefault(k, v)

        # self.user_interfaces = tuple([
        #     p for p in self.installed_plugins if p.ui_label is not None])

        # logger.info("20150428 user_interfaces %s", self.user_interfaces)

        # from lino.core.kernel import Kernel
        self.kernel = Kernel(self)
        # self.kernel.kernel_startup(self)
        # self.ui = self.kernel  # internal backwards compat

        self.do_site_startup()

        for p in self.installed_plugins:
            p.post_site_startup(self)

        # print("20161219 Site.startup() done")
        post_startup.send(self)
        self._startup_done = True

        
    
CHOICELISTS = {}
master_tables = []
slave_tables = []
generic_slaves = {}
frames_list = []
virtual_tables = []
abstract_tables = []

def get_choicelist(i):
    return CHOICELISTS[i]


def choicelist_choices():
    """Return a list of all choicelists defined for this application."""
    l = []
    for k, v in CHOICELISTS.items():
        if v.verbose_name_plural is None:
            text = v.__name__
        else:
            text = v.verbose_name_plural
        l.append((k, text))

    l.sort(key=lambda x: x[0])
    return l

def is_candidate(T):
    if T.filter or T.exclude or T.known_values:
        return False
    if not T.use_as_default_table:
        return False
    return True


def register_actors():
    """This is being called at startup.
    
    - Each model can receive a number of "slaves".
      Slaves are tables whose data depends on an instance
      of another model (their master).

    - For each model we want to find out the "default table".
      The "choices table" for a foreignkey field is also currently
      simply the pointed model's default table.
      :modattr:`_lino_default_table`

    """

    logger.debug("Analyzing Tables...")
    # logger.debug("20111113 Register Table actors...")
    for rpt in actors.actors_list:
        if rpt.abstract:
            abstract_tables.append(rpt)
        elif issubclass(rpt, dbtables.Table):
            if rpt is not dbtables.Table:
                register_model_table(rpt)
        elif issubclass(rpt, tables.VirtualTable):
            if rpt not in (tables.VirtualTable, tables.VentilatedColumns):
                virtual_tables.append(rpt)
        elif issubclass(rpt, frames.Frame) and rpt is not frames.Frame:
            register_frame(rpt)
        elif issubclass(rpt, choicelists.ChoiceList):
            if rpt not in (choicelists.ChoiceList, workflows.Workflow):
                register_choicelist(rpt)


    # logger.debug("Create default tables...")
    # for model in get_models():
    #     # Note that automatic models (created by ManyToManyField with
    #     # a `through`) do not yet exist here.
        
    #     # Not getattr but __dict__.get because of the mixins.Listings
    #     # trick:
    #     rpt = model.__dict__.get('_lino_default_table', None)
    #     # rpt = getattr(model,'_lino_default_table',None)
    #     # logger.debug('20111113 %s._lino_default_table = %s',model,rpt)
    #     if rpt is None:
    #         rpt = table_factory(model)
    #         if rpt is None:
    #             raise Exception("table_factory() failed for %r." % model)
    #         # print ("20170104 No table for {}, created default table.".format(model))
    #         register_model_table(rpt)
    #         rpt.class_init()
    #         # rpt.collect_actions()
    #         model._lino_default_table = rpt

    logger.debug("Analyze %d slave tables...", len(slave_tables))
    for rpt in slave_tables:
        if isinstance(rpt.master, six.string_types):
            raise Exception("20150216 unresolved master")
        if isinstance(rpt.master, UnresolvedModel):
            continue
        if not isinstance(rpt.master, type):
            raise Exception(
                "20160712 invalid master {!r} in {}".format(
                    rpt.master, rpt))
            
        if issubclass(rpt.master, models.Model):
            # rpt.master = resolve_model(rpt.master)
            slaves = getattr(rpt.master, "_lino_slaves", None)
            if slaves is None:
                slaves = {}
                rpt.master._lino_slaves = slaves
            slaves[rpt.actor_id] = rpt
        # logger.debug("20111113 %s: slave for %s",rpt.actor_id, rpt.master.__name__)
    # logger.debug("Assigned %d slave reports to their master.",len(slave_tables))

    # logger.debug("reports.setup() done")

def register_frame(frm):
    frames_list.append(frm)

def register_choicelist(cl):
    #~ print '20121209 register_choicelist', cl
    #~ k = cl.stored_name or cl.__name__
    k = cl.stored_name or cl.actor_id
    if k in CHOICELISTS:
        raise Exception(
            "Cannot register %r : actor name '%s' "
            "already defined by %r" % (cl, k, CHOICELISTS[k]))
        # logger.warning("ChoiceList name '%s' already defined by %s",
        #                k, CHOICELISTS[k])
    CHOICELISTS[k] = cl



def register_model_table(rpt):
    # logger.debug("20120103 register_report %s", rpt.actor_id)

    if rpt.model is None:
        # logger.debug("20111113 %s is an abstract report", rpt)
        return
    
    lst = rpt.model._lino_tables + [rpt]
    rpt.model._lino_tables = lst
    if rpt.master is None:
        # 20170905 if not rpt.model._meta.abstract:
        if not rpt.is_abstract():
            # logger.debug("20120102 register %s : master report", rpt.actor_id)
            master_tables.append(rpt)
        if '_lino_default_table' not in rpt.model.__dict__:
            if is_candidate(rpt):
                rpt.model._lino_default_table = rpt
    elif rpt.master is ContentType:
        # logger.debug("register %s : generic slave for %r", rpt.actor_id, rpt.master_key)
        generic_slaves[rpt.actor_id] = rpt
    else:
        # logger.debug("20120102 register %s : slave for %r", rpt.actor_id, rpt.master_key)
        slave_tables.append(rpt)


