# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre.
# License: BSD, see LICENSE for more details.

from os.path import exists

from urllib import urlencode


class Plugin(object):

    verbose_name = None
    """
    TODO: if this is not None, then Lino will automatically
    add a UserGroup.
    """

    needs_plugins = []

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

    ui_label = None

    media_base_url = None
    media_root = None
    media_name = None

    url_prefix = None

    site_js_snippets = []

    renderer = None

    def __init__(self, site, app_label, app_name, app_module, needed_by):
        """This is called when the Site object *instantiates*, i.e.  you may
        not yet import `django.conf.settings`.  But you get the `site`
        object being instantiated.

        """
        # site.logger.info("20140226 Plugin.__init__() %s",
        #                  app_label)
        if site._startup_done:
            raise Exception(20140227)
        self.site = site
        self.app_name = app_name
        self.app_label = app_label
        self.app_module = app_module
        self.needed_by = needed_by
        if self.verbose_name is None:
            self.verbose_name = app_label.title()
        # import pdb; pdb.set_trace()
        # super(Plugin, self).__init__()

    def configure(self, **kw):
        for k, v in kw.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

    def get_used_libs(self, html=None):
        return []

    def on_site_startup(self, site):
        pass

    def extends_from(self):
        # return the name of the module from which this module inherits.
        for p in self.__class__.__bases__:
            if issubclass(p, Plugin):
                return p.__module__
        raise Exception("20140825 extends_from failed")

    def before_analyze(self, site):
        """This is called when the kernel is being instantiated.
        """
        pass

    def on_ui_init(cls, kernel):
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

    def get_patterns(self, ui):
        """Return a list of url patterns to be added to the Site's patterns.

        """
        return []

    def get_css_includes(self, site):
        return []

    def get_js_includes(self, settings, language):
        return []

    def get_head_lines(cls, site, request):
        return []

    def build_media_url(self, *parts, **kw):
        if self.media_base_url:
            url = self.media_base_url + '/'.join(parts)
            if len(kw):
                url += "?" + urlencode(kw)
            return url
        return self.buildurl('media', self.media_name, *parts, **kw)

    def build_plain_url(self, *args, **kw):
        if self.url_prefix:
            return self.buildurl(self.url_prefix, *args, **kw)
        return self.buildurl(*args, **kw)

    def buildurl(self, *args, **kw):
        url = self.site.site_prefix + ("/".join(args))
        if len(kw):
            url += "?" + urlencode(kw)
        return url

    def setup_media_links(self, ui, urlpatterns):
        if self.media_name is None:
            return

        if self.media_base_url:
            return

        source = self.media_root
        if not source:
            # raise Exception("%s.media_root is not set." % self)
            return

        if not exists(source):
            raise Exception(
                "Directory %s (specified in %s.media_root) does not exist" %
                (source, self))
        ui.setup_media_link(urlpatterns, self.media_name, source=source)


