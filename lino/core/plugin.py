# -*- coding: UTF-8 -*-
# Copyright 2008-2016 Luc Saffre.
# License: BSD, see LICENSE for more details.

"""This defines the :class:`Plugin` class.
See :doc:`/dev/plugins` before reading this.


"""
from future import standard_library
standard_library.install_aliases()
from builtins import object

import os
from os.path import exists, join, dirname, isdir, abspath

from urllib.parse import urlencode
import inspect


class Plugin(object):
    """The base class for all plugins.

    For an introduction, see :doc:`/dev/plugins`.

    A :class:`Plugin` is an optional descriptor for an app which gets
    defined and configured before Django models start to load.
    Lino creates one :class:`Plugin` instance for every installed app.

    The :class:`Plugin` class is comparable to Django's `AppConfig
    <https://docs.djangoproject.com/en/1.7/ref/applications/>`_ class
    which has been added in version 1.7., but there is at least one
    fundamental difference: in Lino the :class:`Plugin` instances for
    all installed apps are available (in :attr:`dd.plugins
    <lino.core.site.Site.plugins>`) when the :xfile:`settings.py` file
    has been loaded and *before* Django starts to load the first
    :xfile:`models.py`.  This is possible because Plugins are defined
    in your app's :xfile:`__init__.py` file.

    Unlike Django's `AppConfig`, you *cannot* define a `Plugin` in
    your :xfile:`models.py` file, you *must* define it in your app's
    :xfile:`__init__.py`.  This limitation has the advantage of making
    certain things possible which are not possible in plain Django.

    Plugins get instiantiated when the :class:`Site` object
    instantiates (i.e. before Django settings are ready).

    """

    verbose_name = None
    """The verbose name of this plugin, as shown to the user.  This can be
    a lazily translated string.

    """

    short_name = None
    """The abbreviated name of this plugin, shown to the user in places
    where shortness is important, e.g. as the label of the tabs of a
    detail layout.  This can be a lazily translated string. Defaults
    to :attr:`verbose_name`.

    """
    
    needs_plugins = []
    """A list of names of plugins on which this plugin depends.

    Lino will automatically add these to your
    `INSTALLED_APPS` if necessary.
    Note that Lino will add them *after* your app.
    To have them *before* your app, specify them explicitly.

    """

    needed_by = None
    """If not None, then it is the Plugin instance which caused this
    plugin to automatically install.

    """

    extends_models = None
    """If specified, a list of model names for which this app provides a
    subclass.

    For backwards compatibility this has no effect
    when :setting:`override_modlib_models` is set.

    """

    disables_plugins = []
    """A list of strings with names of plugins to **not** install even
    though they are yeld by :meth:`get_installed_apps
    <lino.core.site.Site.get_installed_apps>`. This is applied as an
    additional plugin filter even after :meth:`get_apps_modifiers
    <lino.core.site.Site.get_apps_modifiers>`.

    The plugin names can be either the full name or just the
    app_label.

    This list is allowed to contain names of plugins which are not
    installed at all.

    Usage example: The :mod:`lino.modlib.tinymce` works only with
    ExtJS 3, and we currently believe that we will never need it in
    ExtJS 6.  When switching back and forth between
    :mod:`lino.modlib.extjs` and :mod:`lino_extjs6.extjs6`, we had to
    remove it explicitly by also defining a :meth:`get_apps_modifiers
    <lino.core.site.Site.get_apps_modifiers>` method::

        def get_apps_modifiers(self, **kw):
            kw = super(Site, self).get_apps_modifiers(**kw)
            kw.update(tinymce=None)
            return kw

    Now :mod:`lino_extjs6.extjs6` has :attr:`disables_plugins` set to
    ``['tinymce']`` and we no longer need above code because Lino now
    removes it automatically when ExtJS 6 is being used.

    """

    ui_label = None

    ui_handle_attr_name = None
    """Currently implemented by :mod:`lino.modlib.extjs`,
    :mod:`lino.modlib.bootstrap3`."""

    media_base_url = None
    """
    Remote URL base for media files.

    """

    media_root = None
    """
    Local path where third-party media files are installed.

    Only used if this app has :attr:`media_base_url` empty and
    :attr:`media_name` non-empty, *and* if the :xfile:`media`
    directory has no entry named :attr:`media_name`.

    """

    media_name = None
    """
    Either `None` (default) or a non-empty string with the name of the
    subdirectory of your :xfile:`media` directory which is expected to
    contain media files for this app.

    `None` means that there this app has no media files of her own.

    Best practice is to set this to the `app_label`.  Will be ignored
    if :attr:`media_base_url` is nonempty.

    """

    url_prefix = None
    """
    The url prefix under which this app should ask to
    install its url patterns.
    """

    site_js_snippets = []
    """
    List of js snippets to be injected into the `lino_*.js` file.

    """

    renderer = None
    """The renderer used by this plugin. See :doc:`/dev/rendering`."""

    def __init__(self, site, app_label, app_name, app_module, needed_by):
        """This is called when the Site object *instantiates*, i.e.  you may
        not yet import `django.conf.settings`.  But you get the `site`
        object being instantiated.

        Parameters:

        :site:       The :class:`Site` instance
        :app_label:  e.g. "contacts"
        :app_name:   e.g. "lino_xl.lib.contacts"
        :app_module: The module object corresponding to the
                     :xfile:`__init__.py` file.

        """
        # site.logger.info("20140226 Plugin.__init__() %s",
        #                  app_label)
        if site._startup_done:  # djangotest.TestCase.__call__
            raise Exception(20140227)
        self.site = site
        self.app_name = app_name
        self.app_label = app_label
        self.app_module = app_module
        self.needed_by = needed_by
        if self.verbose_name is None:
            self.verbose_name = app_label.title()
        if self.short_name is None:
            self.short_name = self.verbose_name
        self.on_init()
        # import pdb; pdb.set_trace()
        # super(Plugin, self).__init__()

    def configure(self, **kw):
        """Set the given parameter(s) of this Plugin instance.  Any number of
        parameters can be specified as keyword arguments.

        Raise an exception if caller specified a key that does not
        have a corresponding attribute.

        """
        for k, v in list(kw.items()):
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

    def get_used_libs(self, html=None):
        return []

    def on_init(self):
        """This will be called when the Plugin is being instantiated (i.e.
        even before the :class:`Site` instantiation has finished. Used by
        :mod:`lino.modlib.users` to set :attr:`user_model`.

        """
        pass

    def on_site_startup(self, site):
        """This will be called exactly once, when models are ready.

        """
        pass

    @classmethod
    def extends_from(cls):
        """Return the plugin from which this plugin inherits."""
        # for p in self.__class__.__bases__:
        for p in cls.__bases__:
            if issubclass(p, Plugin):
                return p
        # raise Exception("20140825 extends_from failed")

    @classmethod
    def get_subdir(cls, name):
        """Get the absolute path of the named subdirectory if it exists."""
        p = dirname(inspect.getfile(cls))
        p = abspath(join(p, name))
        if isdir(p):
            return p
        # print("20150331 %s : no directory %s" % (cls, p))

    def before_analyze(self):
        """This is called during startup, when all models modules have been
        imported, and before Lino starts to analyze them.

        """
        pass

    def on_ui_init(self, kernel):
        """This is called when the kernel is being instantiated.
        """
        pass

    def __repr__(self):
        l = []
        for k in ('media_name', 'media_root', 'media_base_url',
                  'extends_models', 'needed_by'):
            v = getattr(self, k, None)
            if v is not None:
                l.append('%s=%s' % (k, v))
        if len(l) == 0:
            return self.app_name
        return "%s (%s)" % (self.app_name, ', '.join(l))

    def get_patterns(self):
        """Return a list of url patterns to be added to the Site's patterns.

        """
        return []

    def get_css_includes(self, site):
        return []

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        """Yield or return a list of textlines to add to the `<head>` of the
        html page."""
        return []

    def get_body_lines(cls, site, request):
        return []

    def get_row_edit_lines(self, e, panel):
        return []

    def build_static_url(self, *parts, **kw):
        raise Exception("Renamed to build_lib_url")

    def build_lib_url(self, *parts, **kw):
        if self.media_base_url:
            url = self.media_base_url + '/'.join(parts)
            if len(kw):
                url += "?" + urlencode(kw)
            return url
        return self.site.build_static_url(self.media_name, *parts, **kw)

    def build_plain_url(self, *args, **kw):
        if self.url_prefix:
            return self.site.buildurl(self.url_prefix, *args, **kw)
        return self.site.buildurl(*args, **kw)

    def get_menu_group(self):
        """Return the plugin into whose menu this plugin wants to be inserted.
        If this plugin was automatically installed because some other
        plugin needs it, return that other plugin. Otherwise return
        this plugin.

        Used by :mod:`lino.modlib.languages`.
        Returns a :class:`Plugin` instance.

        """
        return self.needed_by or self

