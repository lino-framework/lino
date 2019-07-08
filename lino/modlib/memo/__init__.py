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

    front_end = 'extjs'
    # front_end = 'lino_react.react'

    def on_plugins_loaded(self, site):

        # front_end = None
        #
        # for k in self.front_end_candidates:
        #     try:
        #         m = import_module(k)
        #     except ImportError:
        #         continue
        #     front_end = m
        #     break

        self.parser = Parser()

        def url2html(parser, s):
            url_text = s.split(None, 1)
            if len(url_text) == 1:
                url = text = url_text[0]
            else:
                url, text = url_text
            return '<a href="%s" target="_blank">%s</a>' % (url, text)

        self.parser.register_command('url', url2html)

