# Copyright 2015-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
This initializes the `SITE.jinja_env` object.  Compare with
:mod:`lino.utils.config` which also walks through the `config`
directories. TODO: do only one common loop for both.
"""

from os.path import join, dirname, isdir
import datetime
import jinja2

from django.conf import settings

from django.utils.translation import ugettext
from django.utils.translation import pgettext

from etgen import html as xghtml
from etgen.html import E, tostring

from lino.utils import iif
from lino.utils import format_date
from lino.utils.jinja import Counter
from lino.utils import SumCollector
from lino.core.renderer import HtmlRenderer
from lino.core.requests import BaseRequest
from lino.api import rt

from html import escape

SUBDIR_NAME = 'config'


# class JinjaRenderer(MailRenderer):
class JinjaRenderer(HtmlRenderer):

    tableattrs = dict()
    cellattrs = dict()

    def __init__(self, *args, **kwargs):
        super(JinjaRenderer, self).__init__(*args, **kwargs)

        loaders = []
        prefix_loaders = {}

        paths = list(settings.SITE.get_settings_subdirs(SUBDIR_NAME))
        if True:  # settings.SITE.is_local_project_dir:
            p = join(settings.SITE.cache_dir, SUBDIR_NAME)
            if isdir(p):
                paths.append(p)
        #~ logger.info("20130717 web.py paths %s",paths)
        if len(paths) > 0:
            loaders.append(jinja2.FileSystemLoader(paths))

        def func(name, m):
            #~ logger.info("20130717 jinja loader %s %s",name,SUBDIR_NAME)
            if isdir(join(dirname(m.__file__), SUBDIR_NAME)):
                loader = jinja2.PackageLoader(name, SUBDIR_NAME)
                loaders.append(loader)
                prefix_loaders[name] = loader
        settings.SITE.for_each_app(func)

        loaders.insert(0, jinja2.PrefixLoader(prefix_loaders, delimiter=":"))

        #~ loaders = reversed(loaders)
        #~ print 20130109, loaders
        self.jinja_env = jinja2.Environment(
            #~ extensions=['jinja2.ext.i18n'],
            loader=jinja2.ChoiceLoader(loaders))
        #~ jinja_env = jinja2.Environment(trim_blocks=False)

        #~ from django.utils import translation

        #~ jinja_env.install_gettext_translations(translation)

        def as_table(action_spec):
            a = settings.SITE.models.resolve(action_spec)
            ar = a.request(
                user=settings.SITE.user_model.get_anonymous_user())
            return self.as_table(ar)

        def as_table2(ar):
            # 20150810
            # ar.renderer = settings.SITE.plugins.bootstrap3.renderer
            ar.renderer = self

            t = xghtml.Table()
            ar.dump2html(t, ar.sliced_data_iterator, header_links=False)

            #~ print ar.get_total_count()
            return tostring(t.as_element())
            #~ return tostring(E.ul(*[E.li(ar.summary_row(obj)) for obj in ar]),method="html")

        def as_ul(action_spec):
            a = settings.SITE.models.resolve(action_spec)
            ar = a.request(
                user=settings.SITE.user_model.get_anonymous_user())
            # 20150810
            ar.renderer = self
            # ar.renderer = settings.SITE.plugins.bootstrap3.renderer
            return tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]))

        self.jinja_env.globals.update(
            settings=settings,
            site=settings.SITE,
            dtos=format_date.fds,  # obsolete
            dtosl=format_date.fdl,  # obsolete
            as_ul=as_ul,
            as_table=as_table2,
            iif=iif,
            str=str,
            len=len,
            E=E,
            tostring=tostring,
            ar=BaseRequest(renderer=settings.SITE.kernel.default_renderer),
            # _=_,
            now=datetime.datetime.now(),
            mtos=settings.SITE.decfmt,  # obsolete
            decfmt=settings.SITE.decfmt,
            fds=format_date.fds,
            fdm=format_date.fdm,
            fdl=format_date.fdl,
            fdf=format_date.fdf,
            fdmy=format_date.fdmy,
            babelattr=settings.SITE.babelattr,
            babelitem=settings.SITE.babelitem,  # obsolete
            tr=settings.SITE.babelitem,
            # dd=dd,
            rt=rt,
            escape=escape,
            Counter=Counter,
            SumCollector=SumCollector,
            # lino=self.modules,  # experimental
            # site_config=self.site_config,

        )

        def translate(s):
            return ugettext(str(s))
        self.jinja_env.globals.update(_=translate)

        def ptranslate(ctx, s):
            return pgettext(ctx.decode('utf8'), s.decode('utf8'))
        self.jinja_env.globals.update(pgettext=pgettext)

        #~ print __file__, 20121231, self.jinja_env.list_templates('.html')

    # def show_table(self, *args, **kwargs):
    #     e = super(JinjaRenderer, self).show_table(*args, **kwargs)
    #     return tostring(e)

    def show_story(self, *args, **kwargs):
        """Render the story and return it as a string."""
        e = super(JinjaRenderer, self).show_story(*args, **kwargs)
        return tostring(e)
