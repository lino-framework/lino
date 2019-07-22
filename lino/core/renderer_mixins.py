# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Defines :class:`JsCacheRenderer`.
"""

from __future__ import unicode_literals
from __future__ import print_function
import six
# str = six.text_type
from builtins import str
from builtins import object

import logging

logger = logging.getLogger(__name__)

from django.conf import settings

from django.utils import translation

import os
import time

from lino.core import kernel
from lino.modlib.users.utils import get_user_profile, with_user_profile
from lino.modlib.users.choicelists import UserTypes


class JsCacheRenderer():
    """
    Mixin for:
    :class:`lino_react.react.renderer.Renderer`,
    :class:`lino.modlib.extjs.ext_renderer.ExtRenderer` and
    :class:`lino_extjs6.extjs.ext_renderer.ExtRenderer`.

    Includes linoweb.js cacheing functionality.


    """
    lino_web_template = "extjs/linoweb.js"

    def __init__(self):
        self.prepare_layouts()

    def write_lino_js(self, f):
        """

        :param f: File object
        :return: 1
        """
        raise NotImplementedError("Need to implement a lino_web.js writing script")

        user_type = get_user_profile()

        context = dict(
            ext_renderer=self,
            site=settings.SITE,
            settings=settings,
            lino=lino,
            language=translation.get_language(),
            # ext_requests=constants,
            constants=constants,
            extjs=self.plugin,  # 20171227
        )

        context.update(_=_)

        tpl = self.linolib_template()

        f.write(tpl.render(**context) + '\n')

        return 1

    def prepare_layouts(self):

        self.actors_list = [
            rpt for rpt in kernel.master_tables
                           + kernel.slave_tables
                           + list(kernel.generic_slaves.values())
                           + kernel.virtual_tables
                           + kernel.frames_list
                           + list(kernel.CHOICELISTS.values())]

        # self.actors_list.extend(
        #     [a for a in kernel.CHOICELISTS.values()
        #      if settings.SITE.is_installed(a.app_label)])

        # don't generate JS for abstract actors
        self.actors_list = [a for a in self.actors_list
                            if not a.is_abstract()]

        # Lino knows three types of form layouts:

        self.form_panels = set()
        self.param_panels = set()
        self.action_param_panels = set()

        def add(res, collector, fl, formpanel_name):
            # res: an actor class or action instance
            # collector: one of form_panels, param_panels or
            # action_param_panels
            # fl : a FormLayout
            if fl is None:
                return
            if fl._datasource is None:
                return  # 20130804

            if fl._datasource != res:
                fl._other_datasources.add(res)
                # if str(res).startswith('newcomers.AvailableCoaches'):
                #     logger.info("20150716 %s also needed by %s", fl, res)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py {2}: {0} != {1}".format(
                #         fl._datasource, res, fl))

            if False:
                try:
                    lh = fl.get_layout_handle(self.plugin)
                except Exception as e:
                    logger.exception(e)
                    raise Exception("Could not define %s for %r: %s" % (
                        formpanel_name, res, e))

                # lh.main.loosen_requirements(res)
                for e in lh.main.walk():
                    e.loosen_requirements(res)

            if fl not in collector:
                fl._formpanel_name = formpanel_name
                fl._url = res.actor_url()
                collector.add(fl)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py collected {}".format(fl))

        for res in self.actors_list:
            add(res, self.form_panels, res.detail_layout,
                "%s.DetailFormPanel" % res)
            add(res, self.form_panels, res.insert_layout,
                "%s.InsertFormPanel" % res)
            add(res, self.param_panels, res.params_layout,
                "%s.ParamsPanel" % res)

            for ba in res.get_actions():
                if ba.action.parameters:
                    add(res, self.action_param_panels,
                        ba.action.params_layout,
                        "%s.%s_ActionFormPanel" % (res, ba.action.action_name))

    def lino_js_parts(self):
        user_type = get_user_profile()
        filename = 'lino_'
        file_type = self.lino_web_template.rsplit(".")[-1]
        if user_type is not None:
            filename += user_type.value + '_'
        filename += translation.get_language() + '.' + file_type
        return ('cache', file_type, filename)

    def linolib_template(self):
        # env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        #     os.path.dirname(__file__)))
        # return env.get_template('linoweb.js')
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        return env.get_template(self.lino_web_template)

    def build_site_cache(self, force=False):
        """
        Build the site cache files under `/media/cache`, especially the
        :xfile:`lino*.js` files, one per user user_type and language.
        """
        # if not self.is_prepared:
        #     self.prepare_layouts()
        #     self.is_prepared = True

        if settings.SITE.never_build_site_cache:
            logger.debug(
                "Not building site cache because `settings.SITE.never_build_site_cache` is True")
            return
        if not os.path.isdir(settings.MEDIA_ROOT):
            logger.debug(
                "Not building site cache because " +
                "directory '%s' (settings.MEDIA_ROOT) does not exist.",
                settings.MEDIA_ROOT)
            return

        started = time.time()
        # logger.info("20140401 build_site_cache started")

        settings.SITE.on_each_app('setup_site_cache', force)

        settings.SITE.makedirs_if_missing(
            os.path.join(settings.MEDIA_ROOT, 'upload'))
        settings.SITE.makedirs_if_missing(
            os.path.join(settings.MEDIA_ROOT, 'webdav'))

        if force or settings.SITE.build_js_cache_on_startup:
            count = 0
            for lng in settings.SITE.languages:
                with translation.override(lng.django_code):
                    for user_type in UserTypes.objects():
                        count += with_user_profile(
                            user_type, self.build_js_cache, force)
            logger.info("%d lino*.js files have been built in %s seconds.",
                        count, time.time() - started)

    def build_js_cache(self, force):
        """Build the :xfile:`lino*.js` file for the current user and the
        current language.  If the file exists and is up to date, don't
        generate it unless `force` is `True`.

        This is called

        - on each request if :attr:`build_js_cache_on_startup
          <lino.core.site.Site.build_js_cache_on_startup>` is `False`.

        - with `force=True` when
          :class:`lino.modlib.lino.models.BuildSiteCache` action is
          run.

        """
        fn = os.path.join(*self.lino_js_parts())

        def write(f):
            self.write_lino_js(f)

        return settings.SITE.kernel.make_cache_file(fn, write, force)
