# Copyright 2014-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""

.. autosummary::
   :toctree:

    loader
    renderer

"""

from copy import copy
from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Jinja templates")

    def post_site_startup(self, site):
    # def on_ui_init(self, kernel):
        """
        This is being called from
        :meth:`lino.core.kernel.Kernel.kernel_startup`.

        Adds a `jinja_env` attribute to `settings.SITE`.

        Lino has an automatic and currently not configurable method
        for building Jinja's template loader. It looks for
        a "config" subfolder in the following places:

        - the project directory :attr:`lino.core.site.Site.project_dir`
        - the directories of each installed app

        """
        from .renderer import JinjaRenderer
        self.renderer = JinjaRenderer(self)

        # internal backwards compat:
        # kernel.site.jinja_env = self.renderer.jinja_env
        # TODO: remove above lines and convert old code

    def list_templates(self, ext, *groups):
        """Return a list of possible choices for a field that contains a
        template name.

        """
        # logger.info("20140617 list_templates(%r, %r)", ext, groups)
        if len(groups):
            retval = []
            for group in groups:
                #~ prefix = os.path.join(*(group.split('/')))
                def ff(fn):
                    return fn.startswith(group) and fn.endswith(ext)
                lst = self.renderer.jinja_env.list_templates(filter_func=ff)
                L = len(group) + 1
                retval += [i[L:] for i in lst]
            return retval
        return self.renderer.jinja_env.list_templates(extensions=[ext])

    def render_from_request(self, request, template_name, **context):
        """Render the named Jinja template, replacing ar.renderer by the
        Site's default renderer.
        Adds some more context names.
        """
        from lino.core import requests
        context.update(request=request)
        ar = requests.BaseRequest(
            # renderer=settings.SITE.plugins.jinja.renderer,
            renderer=self.site.kernel.default_renderer,
            request=request)
        # self.site.logger.info(
        #     "20160529 render_from_request() %s",
        #     self.site.kernel.default_renderer)

        context = ar.get_printable_context(**context)
        context.update(ar=ar)  # probably useless because done by
                               # get_printable_context()
        template = self.renderer.jinja_env.get_template(template_name)
        # u = ar.get_user()
        # print("20170607", u)
        return template.render(**context)
    
    def render_jinja(self, ar, tplname, context):
        """Render the named Jinja template, replacing ar.renderer by the
        Jinja renderer.

        """
        tpl = self.renderer.jinja_env.get_template(tplname)
        sar = copy(ar)
        sar.renderer = self.renderer
        context.update(ar=sar)
        return tpl.render(**context)


def get_environment(**options):
    # print 20160116, options
    from django.conf import settings
    return settings.SITE.plugins.jinja.renderer.jinja_env


