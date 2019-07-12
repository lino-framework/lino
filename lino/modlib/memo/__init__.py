# Copyright 2008-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""See :doc:`/specs/memo`.

Every Lino site has a global memo parser stored in `SITE.plugins.memo.parser`.



"""

from importlib import import_module

from lino.api import ad

from .parser import Parser


class Plugin(ad.Plugin):

    """Base class for this plugin.

    .. attribute:: parser

        An instance of :class:`lino.modlib.memo.parser.Parser`.

    """

    needs_plugins = ['lino.modlib.gfks']

    front_end = None
    # front_end = 'extjs'
    # front_end = 'lino_react.react'
    # front_end = 'bootstrap3'
    """The front end to use when writing previews.
    
    If this is `None`, Lino will use the default front end
    (:attr:`lino.core.site.Site.default_ui`).
    
    Used on sites that are available via more than one web front ends.  The
    site maintainer must then decide which front end is the primary one.
    
    For example, if you have two sites jane (extjs) and hobbit (react), in the
    :xfile:`settings.py` file for Jane you will say::

        def get_installed_apps(self):
            yield super(Site, self).get_installed_apps()
            yield 'lino_react.react'
    
        def get_plugin_configs(self):
            for i in super(Site, self).get_plugin_configs():
                yield i
            yield ('memo', 'front_end', 'react')
    
    
    """

    def on_plugins_loaded(self, site):

        self.parser = Parser()

        def url2html(parser, s):
            url_text = s.split(None, 1)
            if len(url_text) == 1:
                url = text = url_text[0]
            else:
                url, text = url_text
            return '<a href="%s" target="_blank">%s</a>' % (url, text)

        self.parser.register_command('url', url2html)

    def post_site_startup(self, site):

        if self.front_end is None:
            self.front_end = site.kernel.default_ui
        else:
            self.front_end = site.plugins.resolve(self.front_end)

        # front_end = None
        #
        # for k in self.front_end_candidates:
        #     try:
        #         m = import_module(k)
        #     except ImportError:
        #         continue
        #     front_end = m
        #     break

