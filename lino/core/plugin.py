# -*- coding: UTF-8 -*-
# Copyright 2008-2018 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.

"""This defines the :class:`Plugin` class.

See :doc:`/dev/plugins` before reading this.


"""
# from future import standard_library
# standard_library.install_aliases()
# from builtins import object

import os
from os.path import exists, join, dirname, isdir, abspath

# from urllib.parse import urlencode
from six.moves.urllib.parse import urlencode
import inspect


class Plugin(object):
    """The base class for all plugin descriptors.

    For an introduction, see :doc:`/dev/plugins`.

    Plugin descriptors get defined and configured before Django models
    start to load.  Lino creates one :class:`Plugin` instance for
    every installed plugin and makes it globally available in
    :attr:`dd.plugins.FOO <lino.core.site.Site.plugins>` (where `FOO`
    is the `app_label` of the plugin).

    The :class:`Plugin` class is comparable to Django's `AppConfig
    <https://docs.djangoproject.com/en/1.11/ref/applications/>`_ class
    which has been added in version 1.7., but there is at least one
    important difference: in Lino the :class:`Plugin` instances for
    all installed plugins are available (in :attr:`dd.plugins
    <lino.core.site.Site.plugins>`) *before* Django starts to load the
    first :xfile:`models.py`.  This is possible because Plugins are
    defined in :xfile:`__init__.py` files of your plugins. As a
    consequence, unlike Django's `AppConfig`, you *cannot* define a
    `Plugin` in your :xfile:`models.py` file, you *must* define it in
    your plugins's :xfile:`__init__.py`.

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
    """A list of names of plugins needed by this plugin.
    
    The default implementation of :meth:`get_required_plugins` returns this list.

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

    menu_group = None
    """The name of another plugin to be used as menu group.

    See :meth:`get_menu_group`.
    """

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
        """
        Set the given parameter(s) of this Plugin instance.  Any number of
        parameters can be specified as keyword arguments.

        Raise an exception if caller specified a key that does not
        have a corresponding attribute.
        """
        for k, v in list(kw.items()):
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

    def get_required_plugins(self):
        """Return a list of names of plugins needed by this plugin.

        The default implementation returns :attr:`needs_plugins`.

        Lino will automatically install these plugins if necessary.

        Note that Lino will add them *before* your plugin.

        Note that only the app_label (not the whole plugin name) is used when
        testing whether a plugin is installed. IOW if a plugin says it requires
        a plugin "stdlib.foo" and an application already has some plugin
        "mylib.foo" installed, "mylib" satisfies "stdlib.foo".


        """

        return self.needs_plugins

    def get_used_libs(self, html=None):
        return []

    def on_init(self):
        """
        This will be called when the Plugin is being instantiated (i.e.
        even before the :class:`Site` instantiation has finished. Used
        by :mod:`lino.modlib.users` to set :attr:`user_model`.
        """
        pass

    def on_plugins_loaded(self, site):
        """
        Called exactly once on each installed plugin, when the
        :class:`Site` has loaded all plugins, but *before* calling
        :meth:`setup_plugins`.  All this happens before settings are
        ready and long before the models modules start to load.

        This is used for initializing default values of plugin
        attributes which (a) depend on other plugins but (b) should be
        overridable in :meth:`lino.core.site.Site.setup_plugins`.

        For example :mod:`groups` used this to set a default value to
        the :attr:`commentable_model` for :mod:`comments` plugin.

        Or :mod:`lino.modlib.checkdata` uses it to set
        `responsible_user` to "robin" when it is a demo site.
        """
        pass

    def on_site_startup(self, site):
        """
        This will be called exactly once, when models are ready.
        """
        pass
    
    def post_site_startup(self, site):
        """
        This will be called exactly once, when models are ready.
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
        """
        This is called during startup, when all models modules have been
        imported, and before Lino starts to analyze them.
        """
        pass

    def on_ui_init(self, kernel):
        """
        This is called when the kernel is being instantiated.
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
        """
        Override this to return a list of url patterns to be added to the
        Site's patterns.
        """
        return []

    def get_css_includes(self, site):
        return []

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        """
        Yield or return a list of textlines to add to the `<head>` of the
        html page.
        """
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
        """
        Return the plugin (a :class:`Plugin` instance) into whose menu
        this plugin should add its menu commands.

        This returns `self` by default, unless 

        - this plugin defines an explicit :attr:`menu_group`. In this
          case return the named plugin.

        - this plugin was automatically installed because some other
          plugin needs it. In this case return that other plugin.

        When a plugin A is automatically being installed because
        needed by a plugin B which is itself being installed
        automatically because needed by a third plugin C, then
        :meth:`A.get_menu_group
        <lino.core.plugins.Plugin.get_menu_group>` returns C (and not
        B).  A case where this happens is
        :mod:`lino_welfare.modlib.pcsw` which needs
        :mod:`lino_xl.lib.coachings` which in turn needs
        :mod:`lino_xl.lib.clients`.
        """
        if self.menu_group:
            if self.menu_group in self.site.plugins:
                return self.site.plugins.get(self.menu_group)

        needed_by = self
        while needed_by.needed_by is not None:
            needed_by = needed_by.needed_by
        return needed_by

    def setup_user_prefs(self, up):
        """
        Called when a :class:`lino.core.userprefs.UserPrefs` get
        instantiated.
        """
        pass
    
    def get_dashboard_items(self, user):
        """Return or yield a sequence of items to be rendered on the
        dashboard.

        Called by :meth:`lino.core.site.Site.get_dashboard_items`.

        Every item is expected to be either an instance of
        :class:`lino.core.dashboard.DashboardItem`, or a
        :class:`lino.core.actors.Actor`. 

        Tables are shown with a limit of
        :attr:`lino.core.tables.AbstractTable.preview_limit` rows.

        """
        return []

    def setup_layout_element(self, el):
        pass
    
    
